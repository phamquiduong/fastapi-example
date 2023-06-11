import logging.config
import os
from pathlib import Path

from core.settings import settings


class __LogHelper:
    def __init__(self, log_dir: str, log_level: str,
                 log_format: str, log_time_format: str,
                 log_handlers: list[str]) -> None:
        self.log_dir = log_dir
        self.log_level = log_level
        self.log_format = log_format
        self.log_time_format = log_time_format
        self.log_handlers = log_handlers

    def __create_log_folder(self):
        if 'file' in self.log_handlers:
            Path(self.log_dir).mkdir(parents=True, exist_ok=True)

    def __config(self):
        self.__create_log_folder()

        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': self.log_format,
                    'datefmt': self.log_time_format
                },
            },
            'handlers': {
                'console': {
                    'level': self.log_level,
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                },
                'file': {
                    'level': self.log_level,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'default',
                    'filename': self.log_dir / 'file.log',
                    'maxBytes': 15_728_640,       # 15M * 1024K * 1024B
                    'backupCount': 10,
                },
            },
            'loggers': {
                'log': {
                    'handlers': self.log_handlers,
                    'level': self.log_level,
                    'propagate': True,
                }
            },
        }

        logging.config.dictConfig(config=config)

    def get_logger(self):
        self.__config()
        return logging.getLogger('log')


logger = __LogHelper(
    log_dir=settings.log_dir,
    log_level=settings.log_level,
    log_format=settings.log_format,
    log_time_format=settings.log_time_format,
    log_handlers=settings.log_handlers,
).get_logger()
