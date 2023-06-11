from auth.crud.role_crud import get_role
from auth.crud.user_crud import get_or_create_user
from auth.schemas.user_schema import UserInSchema
from core.helper.database_helper import database_helper


def create_admin_user():
    database_helper.try_connect()
    Session = database_helper.get_session()

    email = input('Email address: ')
    password = input('Password: ')

    with Session() as session:
        user_in = UserInSchema(email=email, password=password)
        user = get_or_create_user(session=session, user=user_in)

        admin_role = get_role(session=session, role_name='admin', check_exist=False)
        user.roles = [admin_role]

        session.commit()
