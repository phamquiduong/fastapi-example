from dotenv import load_dotenv

from core.constants import BASE_DIR


def __load_env():
    load_dotenv(BASE_DIR / '.env')


load_env = __load_env()
