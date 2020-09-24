import logging
import os
from logging.handlers import RotatingFileHandler

import telegram
from dotenv import load_dotenv

load_dotenv()


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=self.bot_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_telegram_handler(bot_token=None, chat_id=None):
    tg_logs_handler = TelegramLogsHandler(bot_token, chat_id)
    tg_logs_handler.setFormatter(logging.Formatter(
        '%(asctime)-.19s - %(name)s -  %(lineno)d - %(levelname)s -'
        ' %(message)s'
    ))
    tg_logs_handler.setLevel(logging.WARNING)
    return tg_logs_handler


def get_file_handler():
    """ Logger для записи в файл"""

    file_handler = RotatingFileHandler('simple.log', maxBytes=30000,
                                       backupCount=1)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)-.19s - %(name)s -  %(lineno)d - %(levelname)s -'
        ' %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    return file_handler


def get_console_handler():
    """ Logger для вывода в консоль"""
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(message)s'
    ))
    console_handler.setLevel(logging.DEBUG)
    return console_handler


def get_logger(name):
    bot_token = os.getenv('TELEGRAM_BOT')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_console_handler())
    logger.addHandler(get_telegram_handler(bot_token, chat_id))

    return logger
