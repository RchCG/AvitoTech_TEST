# Используем базовый образ с Python 3.11-slim-bookworm
FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${PATH}:/root/.local/bin"

EXPOSE 8000


RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry update  # Обновление зависимостей
RUN poetry install --no-root  # Установка зависимостей

# Запуск приложения
CMD ["/app/entrypoint.sh"]

