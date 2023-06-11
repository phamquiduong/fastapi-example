from sqlalchemy import text

from core.helper.database_helper import database_helper
from core.helper.log_helper import logger
from core.settings import settings

# Common SQL commands
CREATE_MIGRATION_TABLE_SQL = 'CREATE TABLE IF NOT EXISTS migrations (name varchar(255) PRIMARY KEY)'
INSERT_MIGRATION_SQL = "INSERT INTO migrations (name) VALUES ('{migration_name}')"
CHECK_MIGRATION_SQL = "SELECT true FROM migrations WHERE name = '{migration_name}' LIMIT 1"


class Migration:
    def __init__(self):
        self.migrations_folder = settings.base_dir / 'database/migrations' / settings.migrations_folder
        self.Session = database_helper.get_session()

        self.migrations_file = self.get_migrations_file()

        database_helper.try_connect()

    def run(self):
        self.init_migrations_table()

        for migration_file in self.migrations_file:
            migration_name = str(migration_file).split('/')[-1].split('.')[0]

            with open(migration_file) as file:
                sql_commands = file.read().split(';')

                if self.is_valid_migration(migration_name):
                    logger.info(f'Running migration {migration_name}')

                    try:
                        with self.Session() as session:
                            for sql_command in sql_commands:
                                session.execute(text(sql_command))
                            session.execute(text(INSERT_MIGRATION_SQL.format(migration_name=migration_name)))
                            session.commit()
                    except Exception as e:
                        logger.error(f'  -> Fail.. Detail: {str(e)}')

                    logger.info('  -> Success')

        logger.info('Migrate complete.')

    # Read migrations file
    def get_migrations_file(self):
        return sorted(self.migrations_folder.glob('*.sql'))

    def init_migrations_table(self):
        with self.Session() as session:
            session.execute(text(CREATE_MIGRATION_TABLE_SQL))
            session.commit()

    def is_valid_migration(self, migration_name: str):
        with self.Session() as session:
            query = session.execute(text(CHECK_MIGRATION_SQL.format(migration_name=migration_name)))
            return not query.fetchall()
