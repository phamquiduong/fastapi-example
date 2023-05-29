from core.constants import ROLES
from database.config import SessionLocal
from users.crud import get_or_create_role


def create_roles():
    with SessionLocal() as db:
        for role_name in ROLES:
            get_or_create_role(db, role_name)
