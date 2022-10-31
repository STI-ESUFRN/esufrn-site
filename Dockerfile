FROM python:3.10-alpine

ENV APP_HOME=/usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR $APP_HOME

RUN apk update && \
    apk add gcc musl-dev mariadb-connector-c-dev

COPY pyproject.toml .
RUN pip install poetry
RUN poetry install --only main

COPY ./scripts/entrypoint.sh ./entrypoint.sh
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

RUN mkdir -p \
    $APP_HOME/src \
    $APP_HOME/src/staticfiles \
    $APP_HOME/src/media


ENTRYPOINT ["./entrypoint.sh"]
