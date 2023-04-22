#!/usr/bin/env sh

set -e

# накатываем миграции
alembic upgrade head

# Запуск сервера
uvicorn server:app --reload --port 8000 --host 0.0.0.0
