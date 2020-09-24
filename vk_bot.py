# -*- coding: utf-8 -*-
import json
import os
import random

import dialogflow_v2 as dialogflow
import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

import app_logger

load_dotenv()

logger = app_logger.get_logger(__name__)


def get_answer_dialogflow(texts):
    """Связывается с dialogflow, возращает ответы на вопросы через dialogflow"""
    logger.info('start get_answer_dialogflow')
    session_client = dialogflow.SessionsClient()
    path_json_config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    with open(path_json_config, 'r') as f:
        config_json = json.load(f)
    project_id = config_json['project_id']
    session_id = config_json['client_id']
    session = session_client.session_path(project_id, session_id)
    logger.debug('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(
        text=texts, language_code='ru-RU')
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    logger.debug('=' * 20)
    logger.debug('Query text: {}'.format(response.query_result.query_text))
    logger.debug('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence,
    ))
    logger.debug('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    if response.query_result.intent.is_fallback:
        return False
    return response.query_result.fulfillment_text


def main():
    vk_key = os.getenv('VKONTAKTE_KEY')
    vk_session = vk_api.VkApi(token=vk_key)
    vk_session_api = vk_session.get_api()
    logger.info('start bot vk info')
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            logger.info('get longpoll')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    text = get_answer_dialogflow(event.text)
                    if text:
                        vk_session_api.messages.send(
                            user_id=event.user_id,
                            message=text,
                            random_id=random.randint(1, 1000)
                        )
                        logger.info('answer to the question')

        except:
            logger.exception('Mistake vk_bot')
            return False


if __name__ == '__main__':
    main()
