import json
import logging
import os

import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import app_logger
load_dotenv()


logger = app_logger.getLogger(__name__)


def start(bot, update):
    """ Функция ответа одной фразы, используется при старте"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="Я бот, поговори со мной")


def echo(bot, update):
    """ Повторяет написанную фразу"""
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def answer(bot, update):
    """ Отвечает с помощью dialogflow,
    за связь с dialogflow отвечает detect_intent_texts()"""
    text = detect_intent_texts(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=text)


def caps(bot, update, args):
    """ В ответе пповторяет введенный текст большими буквами"""
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def detect_intent_texts(texts):
    """Связывается с dialogflow, возращает ответы на вопросы через dialogflow"""
    session_client = dialogflow.SessionsClient()
    path_json_config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    with open(path_json_config, 'r') as f:
        config_json = json.load(f)
    project_id = config_json['project_id']
    session_id = config_json['client_id']
    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(
        text=texts, language_code='ru-RU')
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text


def main():
    telegram_token = os.getenv('TELEGRAM_BOT')
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher

    caps_handler = CommandHandler('caps', caps, pass_args=True)
    dispatcher.add_handler(caps_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, answer)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
