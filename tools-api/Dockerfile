# pull the official docker image
FROM python:3.9.2-slim

# set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.12

RUN pip install "poetry==$POETRY_VERSION" \
    && apt-get update && apt-get install -y libpq-dev gcc \
    && pip install psycopg2

# set work directory
WORKDIR /tools-api

# install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# copy project
COPY . .
