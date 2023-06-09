import logging
import os
import sys

from core.load_env import load_env


def main():
    # Load the environment variables
    load_env()

    args = iter(sys.argv[1:])
    action = next(args, '--help')

    if action in ('runserver', '-r'):
        host = next(args, '127.0.0.1')
        port = int(next(args, 8000))
        runserver(host=host, port=port)

    if action in ('migrate', '-m'):
        migrate()

    if action in ('--help', '-h'):
        show_help()


def runserver(host: str, port: int):
    import uvicorn

    from database.config import try_connection

    # Try to connect to the database
    try_connection()

    _port = int(os.getenv('NGINX_PORT') or port)
    _port = f':{_port}' if _port != 80 else ''
    print(f'\n* Server is running. Visit http://localhost{_port}/docs to view document\n')

    uvicorn.run(
        'app:app',
        host=host,
        port=port,
        reload=True,
        log_level=getattr(logging, os.getenv('UVICORN_LOG_LEVEL'))
    )


def migrate():
    from database.migrate import Migration
    Migration().run()


def show_help():
    print("""
*****************************************************************
*                 Server manager copyright PQD                  *
*****************************************************************

Actions:
    runserver | -r : run the server
        Options:
            host (str): default 127.0.0.1
            port (int): default 8000. Required if host is available
        Example: `python main.py runserver 0.0.0.0 80`

    migrate | -m: migrate the database

    --help, -h: show this help
""")


if __name__ == "__main__":
    main()
