import logging.config

from core.settings import settings


class LogHelper:
    def __create_log_folder(self):
        if 'file' in settings.log_handlers:
            settings.log_dir.mkdir(parents=True, exist_ok=True)

    def config(self):
        self.__create_log_folder()

        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': settings.log_format,
                    'datefmt': settings.log_time_format
                },
            },
            'handlers': {
                'console': {
                    'level': settings.log_level,
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                },
                'file': {
                    'level': settings.log_level,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'default',
                    'filename': settings.log_dir / 'file.log',
                    'maxBytes': 15_728_640,       # 15M * 1024K * 1024B
                    'backupCount': 10,
                },
            },
            'loggers': {
                'log': {
                    'handlers': settings.log_handlers,
                    'level': settings.log_level,
                    'propagate': True,
                }
            },
        }

        logging.config.dictConfig(config=config)

    def get_logger(self):
        self.config()
        return logging.getLogger('log')


logger = LogHelper().get_logger()
