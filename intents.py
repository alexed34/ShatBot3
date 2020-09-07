import dialogflow_v2
from dotenv import load_dotenv
import os
import json
load_dotenv()

def get_project_id():
    path_json_config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    with open(path_json_config, 'r') as f:
        config_json = json.load(f)
        return config_json['project_id']

def open_json():
    with open('questions.json', 'r', encoding='utf8') as f:
        return json.load(f)


def great_dict_intent(intents, name):
    messages = intents[name]['answer']
    training_phrases = []
    for training_phrase in intents[name]['questions']:
        training_phrases.append({"parts": [{"text": training_phrase}]})

    intent = {"display_name": name,
              "messages": [{"text": {"text": [messages]}}],
              "training_phrases": training_phrases
              }
    return intent


def main():
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(get_project_id())
    questions = open_json()
    for question in questions.keys():
        print(question)
        intent = great_dict_intent(questions, question)
        response = client.create_intent(parent, intent)



if __name__ == '__main__':
    main()