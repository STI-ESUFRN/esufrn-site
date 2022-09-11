FROM python:3.10-alpine

ENV APP_HOME=/usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR $APP_HOME

RUN apk update \
    && apk add gcc musl-dev mariadb-connector-c-dev

RUN addgroup -S app && adduser -S app -G app

COPY pyproject.toml .
RUN pip install poetry
RUN poetry install

COPY ./scripts ./scripts
RUN sed -i 's/\r$//g' ./scripts/entrypoint.sh
RUN chmod +x ./scripts/entrypoint.sh

COPY . $APP_HOME

# RUN chown -R app:app $APP_HOME

# USER app

WORKDIR $APP_HOME/src

ENTRYPOINT ["../scripts/entrypoint.sh"]