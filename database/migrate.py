import os
import time

from sqlalchemy import text

from core.constants import BASE_DIR
from core.helper.file_helper import read_file
from core.logging import logger
from database.config import SessionLocal, try_connection

MIGRATIONS_FOLDER = BASE_DIR / 'database/migrations' / os.getenv('MIGRATION_FOLDER')

# Common SQL commands
CREATE_MIGRATION_TABLE_SQL = 'CREATE TABLE IF NOT EXISTS migrations (name varchar(255) PRIMARY KEY)'
INSERT_MIGRATION_SQL = "INSERT INTO migrations (name) VALUES ('{migration_name}')"
CHECK_MIGRATION_SQL = "SELECT true FROM migrations WHERE name = '{migration_name}' LIMIT 1"


class Migration:
    def __init__(self):
        try_connection()
        self.get_migrations_file()
        self.init_migrations_table()

    def run(self):
        for migration_file in self.migrations_file:
            sql_commands = read_file(migration_file).split(';')

            migration_name = str(migration_file).split('/')[-1].split('.')[0]

            migration_success = False
            while not migration_success and self.is_valid_migration(migration_name):
                logger.info(f'Running migration {migration_name}')
                try:
                    with SessionLocal() as session:
                        for sql_command in sql_commands:
                            session.execute(text(sql_command))
                        session.execute(text(INSERT_MIGRATION_SQL.format(migration_name=migration_name)))
                        session.commit()
                        migration_success = True
                except Exception as e:
                    logger.error(f'Running migration {migration_name} fail.. Try in next 5s.\n    Detail: {str(e)}')
                    time.sleep(5)

                logger.info(f'Running migration {migration_name} successfully')

        logger.info('Migrate complete.')

    # Read migrations file
    def get_migrations_file(self):
        self.migrations_file = sorted(MIGRATIONS_FOLDER.glob('*.sql'))

    def init_migrations_table(self):
        with SessionLocal() as session:
            session.execute(text(CREATE_MIGRATION_TABLE_SQL))
            session.commit()

    def is_valid_migration(self, migration_name: str):
        with SessionLocal() as session:
            query = session.execute(text(CHECK_MIGRATION_SQL.format(migration_name=migration_name)))
            return not query.fetchall()
