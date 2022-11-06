FROM python:3.10-slim-buster

USER root

# install required packages
RUN apt-get update; \
    apt-get install gcc build-essential -y;

# install poetry
RUN pip install --upgrade pip; \
    pip install poetry; \
    poetry config virtualenvs.create false;

# install pip dependencies
WORKDIR /app
COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install --no-root --no-interaction --no-ansi

# copy app source
COPY . /app/

# entrypoint
WORKDIR /app
ENTRYPOINT ["uwsgi", "--ini",  "uwsgi.ini"]
