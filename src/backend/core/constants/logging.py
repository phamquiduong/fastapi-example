import os

from core.constants.common import BASE_DIR

# Logging configuration
LOG_DIR = BASE_DIR / '.log'
LOG_LEVEL = os.getenv('LOG_LEVEL')
LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s'
LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
