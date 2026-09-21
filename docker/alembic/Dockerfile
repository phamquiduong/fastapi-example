FROM python:3.14-slim


# Forces streams to be unbuffered
ENV PYTHONUNBUFFERED=1


# Install Python package
COPY migrations/requirements.txt /
RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt


# Create src folder
WORKDIR /migrations
COPY /migrations /migrations


# Run server
CMD alembic upgrade head
