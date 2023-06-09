import logging.config
import os
from pathlib import Path

from core.constants.common import BASE_DIR

Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': LOG_FORMAT,
            'datefmt': LOG_TIME_FORMAT
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': LOG_DIR / 'file.log',
            'maxBytes': 15_728_640,       # 15M * 1024K * 1024B
            'backupCount': 10,
        },
    },
    'loggers': {
        'log': {
            'handlers': os.getenv('HANDLERS').split(','),
            'level': LOG_LEVEL,
            'propagate': True,
        }
    },
}

logging.config.dictConfig(LOGGING)

logger = logging.getLogger('log')
