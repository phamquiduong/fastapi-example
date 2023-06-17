from core.helper.database_helper import database_helper


def get_session():
    Session = database_helper.get_session()
    session = Session()
    try:
        yield session
    finally:
        session.close()
