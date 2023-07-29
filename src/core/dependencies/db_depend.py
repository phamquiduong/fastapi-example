from core.helper.database_helper import db_helper


def get_session():
    session = db_helper.get_session()()
    try:
        yield session
    finally:
        session.close()
