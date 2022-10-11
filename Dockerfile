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
    $APP_HOME \
    $APP_HOME/staticfiles \
    $APP_HOME/media

COPY ./src $APP_HOME

# RUN addgroup -S app && \
#     adduser -S app -G app
# RUN chown -R app:app \
#     $APP_HOME \
#     $APP_HOME/staticfiles \
#     $APP_HOME/media

# USER app

WORKDIR $APP_HOME

ENTRYPOINT ["./entrypoint.sh"]
