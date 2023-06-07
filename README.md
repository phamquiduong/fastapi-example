## FastAPI Source Code
- Django source code customizations by me


## Developed by
- Python last release
- FastAPI framework lastest version
- Sqlite3 or MySQL


## Installation Python3
- Visit https://www.python.org/ and download the lastest version
- Install Python and Remember tick on `Add Python 3.x to PATH` ([Image](https://docs.blender.org/manual/vi/latest/_images/about_contribute_install_windows_installer.png))

#### Note
- In windows 10 and later, you can install Python in Microsoft Store
- In linux or Mac OS, command python and pip is `python3` and `pip3`


### Using virtual environment (not required)
In windows 8.1 and later you must allow create virtual environment. Open powershell as administrator and run this command
```bash
    Set-ExecutionPolicy Unrestricted -Force
```

And then create a virtual environment by command
```bash
    python -m venv .venv

    # In Windows active environment by command
    .\.venv\Scripts\activate

    # In Linux or Mac OS active environment by command
    source .venv/bin/activate
```


### Using docker compose (not required)
```bash
    # Change directory to docker folder
    cd .docker

    # Copy environment file
    cp .env.example .env

    # Docker build
    docker-compose build

    # Start docker
    docker-compose up

        # If start at background
        docker-compose up -d

        # Build again and run in background
        docker-compose up --build -d

        # Note: If you running mysql database docker. Add profile to the command
        docker-compose up --profile mysql --build -d

    # Stop docker
    docker-compose down
```


## Setup .env file
You can configure the environment file base on example file
```bash
    cp .env.example .env

    # Setup Database
    ##   You can config connect in SQLALCHEMY_DATABASE_URL. Default using sqlite3
    ###      note: empty string or disable key to using mysql.
```


## Installation Python Package
```bash
    pip install -r requirements.txt
```


## Migrate Database
```bash
    # Create or upgrade the database with the latest model version
    python manage.py migrate
```

## Run server
```bash
    python manage.py runserver <HOST> <port>
    # Host address of the server: Default: 127.0.0.1. If you want to public the server address host address is 0.0.0.0
    # Port of the server: Default: 8000. You can change the port to 80

    # Run the server example command: python manage.py runserver 0.0.0.0 80
```

And now you can visit `localhost/docs` to view the API documentation
