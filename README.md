# FastAPI Source Code
- FastAPI source code customizations by PQD

<br>

# Developed by
- Python last release
- FastAPI framework lastest version
- Sqlite3 or MySQL Database

<br>

# Installation Python3 and Setup Virtual Environment
## Download Python in Windows OS And Mac OS
- Visit https://www.python.org/ and download the lastest version

    ### Note
    - In Windows OS install Python GUI and Remember tick on `Add Python 3.x to PATH` ([guidance image](https://docs.blender.org/manual/vi/latest/_images/about_contribute_install_windows_installer.png))
    - In windows 10 and later, you can install Python in Microsoft Store
    - In linux or Mac OS, command python and pip is `python3` and `pip3`


## Using virtual environment (not required)
- In windows 8.1/ 10/ 11 and later. You must allow create virtual environment. Open powershell as administrator and run this command
    ```bash
    Set-ExecutionPolicy Unrestricted -Force
    ```

- And then create a virtual environment by command
    ```bash
    python -m venv .venv

    # In Windows active environment by command
    .\.venv\Scripts\activate

    # In Linux or Mac OS active environment by command
    source .venv/bin/activate
    ```

    ### Note:
    - You can create and manage virtual environment in [VSCode](https://code.visualstudio.com/docs/python/environments) or [Pycharm](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html)


## Using docker compose (not required)
- Download docker desktop from https://www.docker.com/
- Install docker running following command
    ```bash
    # Change directory to docker folder
    cd docker

    # Copy environment file
    cp .env.example .env
        # Then edit some configuration settings for docker

    # Create network
    docker network create [COMPOSE_PROJECT_NAME]_network
        # COMPOSE_PROJECT_NAME is the project name setup in .env file

    # Docker build
    docker-compose build

    # Start docker
    docker-compose up
        # Using -d option for run docker-compose in the background
        # Using --build option for build docker-compose again

    # Stop docker
    docker-compose down
    ```

<br>

# Installation Python Packages
- Run this command to install all python packages
    ```bash
    pip install -r requirements.txt
    ```

<br>

# Setup project evirements variables
- You can configure the environment file base on example file
    ```bash
    # Change directory to docker folder
    cd src/

    # Copy environment file 
    cp .env.example .env
        # Then edit some configuration settings for fastAPI
    ```

<br>

# Migrate Database
- Create or upgrade the database with the latest model version
    ```bash
    # Change directory to docker folder
    cd src/

    # Run migrate into migrations folder (mysql or sqlite)
    python main.py migrate
    ```

<br>

# Create admin user
- Create or upgrade the database with the latest model version
    ```bash
    # Change directory to docker folder
    cd src/

    # Create admin user
    python main.py createsuperuser
        # Fill email address and password
    ```

<br>

# Run server
- Run server by uvicorn
    ```bash
    # Change directory to docker folder
    cd src/

    # Run server
    uvicorn main:app
        # using --host <HOST> to config host. Default is 127.0.0.1
        # using --port <PORT> to config port. Default is 8000
        # using --reload to config reload server when code changes
    ```

- And now you can visit `http://[HOST]:[PORT]/docs` (example: http://localhost/docs) to view the API documentation

<br>

# Project structure:
```
fastapi-base
├─ 📁docker
│  ├─ 📁mysql
│  ├─ 📁nginx
│  │  ├─ 📁config
│  │  │  ├─ 📄fastcgi_params
│  │  │  └─ 📄mime.types
│  │  ├─ 📄nginx-crontab
│  │  ├─ 📄nginx.conf.template
│  │  └─ 📄run_nginx.sh
│  ├─ 📄.env.example
│  ├─ 📄Dockerfile-nginx
│  ├─ 📄Dockerfile-py
│  └─ 📄docker-compose.yml
├─ 📁log
├─ 📁src
│  ├─ 📁__pycache__
│  ├─ 📁auth
│  │  ├─ 📁crud
│  │  │  ├─ 📁__pycache__
│  │  │  ├─ 📄role_crud.py
│  │  │  └─ 📄user_crud.py
│  │  ├─ 📁dependencies
│  │  │  ├─ 📁__pycache__
│  │  │  └─ 📄auth_depend.py
│  │  ├─ 📁helper
│  │  │  ├─ 📁__pycache__
│  │  │  ├─ 📄auth_helper.py
│  │  │  └─ 📄password_helper.py
│  │  ├─ 📁models
│  │  │  ├─ 📁__pycache__
│  │  │  └─ 📄user_role_model.py
│  │  ├─ 📁routes
│  │  │  ├─ 📁__pycache__
│  │  │  ├─ 📄__init__.py
│  │  │  ├─ 📄admin_router.py
│  │  │  ├─ 📄auth_router.py
│  │  │  └─ 📄user_router.py
│  │  └─ 📁schemas
│  │     ├─ 📁__pycache__
│  │     ├─ 📄role_schema.py
│  │     ├─ 📄token_schema.py
│  │     └─ 📄user_schema.py
│  ├─ 📁core
│  │  ├─ 📁__pycache__
│  │  ├─ 📁constants
│  │  │  ├─ 📁__pycache__
│  │  │  └─ 📄token_constant.py
│  │  ├─ 📁dependencies
│  │  │  ├─ 📁__pycache__
│  │  │  └─ 📄db_depend.py
│  │  ├─ 📁helper
│  │  │  ├─ 📁__pycache__
│  │  │  ├─ 📄bcrypt_helper.py
│  │  │  ├─ 📄database_helper.py
│  │  │  ├─ 📄env_helper.py
│  │  │  ├─ 📄jwt_helper.py
│  │  │  ├─ 📄log_helper.py
│  │  │  ├─ 📄phone_number_helper.py
│  │  │  └─ 📄token_helper.py
│  │  ├─ 📁schemas
│  │  │  ├─ 📁__pycache__
│  │  │  └─ 📄error_schema.py
│  │  └─ 📄settings.py
│  ├─ 📁database
│  │  ├─ 📁__pycache__
│  │  ├─ 📁migrations
│  │  │  ├─ 📁mysql
│  │  │  │  └─ 📄0001_create_user_role.sql
│  │  │  └─ 📁sqlite
│  │  │     └─ 📄0001_create_user_role.sql
│  │  ├─ 📄create_admin_user.py
│  │  └─ 📄migrate.py
│  ├─ 📄.env.example
│  └─ 📄main.py
├─ 📄.gitignore
├─ 📄README.md
└─ 📄requirements.txt
```