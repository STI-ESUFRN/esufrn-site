FROM python:3.11.0-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME=/etc/poetry \
    PROJECT_DIR=/app \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="$POETRY_HOME/bin:$PATH"


WORKDIR $PROJECT_DIR

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gettext=0.21-4 \
    libcurl4=7.74.0-1.3+deb11u3 \
    curl=7.74.0-1.3+deb11u3 \
    netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 10001 python \
    && useradd -m -u 10000 -g python -s /bin/bash python

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.toml poetry.lock pyproject.toml .

COPY --chown=python:python . .
RUN poetry install --only main
WORKDIR /$PROJECT_DIR/src

USER python
EXPOSE 8000
ENTRYPOINT ["../docker/entrypoint.sh"]
