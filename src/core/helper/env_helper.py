from dotenv import load_dotenv


def load_env(env_file: str = '.env'):
    if not load_dotenv(env_file):
        raise Exception('.env file not found')
