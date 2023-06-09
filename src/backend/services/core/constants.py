import os
from datetime import timedelta
from pathlib import Path

# Project configuration
BASE_DIR = Path(__file__).resolve().parent.parent


# Security configuration
PASSWORD_SALT = os.getenv('PASS_SALT', '')


# Roles configuration
DEFAULT_ROLE = os.getenv('DEFAULT_ROLE', '')
ROLES = ['user', 'admin']
ROLE_ACTIONS = ['add', 'remove']


# JWT configuration
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

ACCESS_TOKEN_EXP = timedelta(days=1)
REFRESH_TOKEN_EXP = timedelta(days=60)
