FROM python:3.14-slim


# Forces streams to be unbuffered
ENV PYTHONUNBUFFERED=1


# Install Python package
COPY requirements.txt /
RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt


# Create src folder
WORKDIR /src
COPY /src /src


# Run server
CMD "uvicorn main:app --host 0.0.0.0 --port 8000"
