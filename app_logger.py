import logging
from logging.handlers import RotatingFileHandler


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)

def get_telegram_handler():
    """ logger для отправки в telegram"""
    telegram_handler =TelegramLogsHandler()
    telegram_handler.setFormatter(logging.Formatter(
        '%(asctime)-.19s - %(name)s -  %(lineno)d - %(levelname)s -'
        ' %(message)s'
    ))
    telegram_handler.setLevel(logging.WARNING)
    return telegram_handler


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
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_console_handler())
    logger.addHandler(get_telegram_handler())
    return logger
