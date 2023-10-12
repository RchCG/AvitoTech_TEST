#!/bin/sh

# Ожидание готовности основной базы данных
wait-for-it.sh -h db -p 5433 -t 60

# Ожидание готовности тестовой базы данных
wait-for-it.sh -h db_test -p 5434 -t 60

# Применение миграций для основной базы данных с помощью Alembic
alembic -c alembic.ini upgrade heads

# Применение миграций для тестовой базы данных с помощью Alembic (если необходимо)

# Запуск приложения
poetry run python main.py
