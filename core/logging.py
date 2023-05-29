import logging.config
import os
from pathlib import Path

from core.constants import BASE_DIR

# Logging configuration
__LOG_DIR = BASE_DIR / '.log'
__LOG_LEVEL = os.getenv('LOG_LEVEL')
__LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s'
__LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

Path(__LOG_DIR).mkdir(parents=True, exist_ok=True)

__LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': __LOG_FORMAT,
            'datefmt': __LOG_TIME_FORMAT
        },
    },
    'handlers': {
        'console': {
            'level': __LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': __LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': __LOG_DIR / 'file.log',
            'maxBytes': 15_728_640,       # 15M * 1024K * 1024B
            'backupCount': 10,
        },
    },
    'loggers': {
        'log': {
            'handlers': os.getenv('HANDLERS').split(','),
            'level': __LOG_LEVEL,
            'propagate': True,
        }
    },
}


logging.config.dictConfig(__LOGGING)

logger = logging.getLogger('log')
