## FastAPI Source Code
- FastAPI customizations by PQD

<br>

## Developed by
- Python last release
- FastAPI framework lastest version
- Sqlite3

<br>

## Installation Python3 and Setup Virtual Environment
### Download Python in Windows OS And Mac OS
- Visit https://www.python.org/ and download the lastest version

    #### Note
    - In Windows OS install Python GUI and Remember tick on `Add Python 3.x to PATH` ([guidance image](https://docs.blender.org/manual/vi/latest/_images/about_contribute_install_windows_installer.png))
    - In windows 10 and later, you can install Python in Microsoft Store (not recommended)
    - In linux or Mac OS, command python and pip is `python3` and `pip3`


### Using virtual environment (not required)
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

    #### Note:
    - You can create and manage virtual environment in [VSCode](https://code.visualstudio.com/docs/python/environments) or [Pycharm](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html)


### Using docker compose (not required)
- Download docker desktop from https://www.docker.com/
- Install docker running following command
    ```bash
    # Change directory to docker folder
    cd docker

    # Copy environment file
    cp .env.example .env

    # Create network
    docker network create [COMPOSE_PROJECT_NAME]_network
        # COMPOSE_PROJECT_NAME is the project name setup in .env file

    # Docker build
    docker-compose build

    # Start docker-compose
    docker-compose up
        # Using -d option for run docker-compose in the background
        # Using --build option for build and up docker-compose

    # Down docker-compose
    docker-compose down
    ```

<br>

## Installation Python Packages
- Run this command to install all python packages
    ```bash
    pip install -r requirements.txt
    ```

<br>

## Setup project evirements variables
- You can configure the environment file base on example file
    ```bash
    # Change directory to docker folder
    cd docker/

    # Copy environment file 
    cp .env.example .env
        # Then edit some configuration settings for fastAPI
    ```

<br>

## Run server
- Run server by uvicorn
    ```bash
    # Change directory to source code folder
    cd src/

    # Run command to run server
    uvicorn main:app --host 0.0.0.0 --port 80 --env-file ../docker/.env --reload
        # --host: 127.0.0.1 (loopback address) or 0.0.0.0 (non-routable meta-address)
        # --port: port running server
        # --env-file: environment file
    ```

- And now you can visit `http://[HOST]:[PORT]/docs` (example: http://localhost/docs) to view the API documentation

## Thank you so much!
