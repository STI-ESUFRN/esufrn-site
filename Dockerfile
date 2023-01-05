FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV APP_HOME=/usr/src/app

WORKDIR $APP_HOME

RUN apk update && \
    apk add gcc musl-dev mariadb-connector-c-dev

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

COPY entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

COPY .env .

WORKDIR $APP_HOME/src

ENTRYPOINT ["../entrypoint.sh"]
