import json
import os

import dialogflow_v2
from dotenv import load_dotenv

load_dotenv()


def get_project_id():
    """ Получить id проекта"""
    path_json_config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    with open(path_json_config, 'r') as f:
        config_json = json.load(f)
        return config_json['project_id']


def open_json():
    """ Открыть файл с вопросами для создания intent"""
    with open('questions.json', 'r', encoding='utf8') as f:
        return json.load(f)


def great_dict_intent(intents, name):
    """ Создать словарь - intent для отправки dialogflow"""
    messages = intents[name]['answer']
    training_phrases = []
    for training_phrase in intents[name]['questions']:
        training_phrases.append({"parts": [{"text": training_phrase}]})

    intent = {"display_name": name,
              "messages": [{"text": {"text": [messages]}}],
              "training_phrases": training_phrases
              }
    return intent


def add_invents():
    """ add intent in dialogflow"""
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(get_project_id())
    questions = open_json()
    for question in questions.keys():
        print(question)
        intent = great_dict_intent(questions, question)
        response = client.create_intent(parent, intent)


def save_invents():
    """ save  and lern intent in dialogflow"""
    client = dialogflow_v2.AgentsClient()
    parent = client.project_path(get_project_id())
    response = client.train_agent(parent)

    def callback(operation_future):
        # Handle result.
        result = operation_future.result()

    response.add_done_callback(callback)
    # Handle metadata.
    metadata = response.metadata()
    print(metadata)


def main():
    add_invents()
    save_invents()


if __name__ == '__main__':
    main()
