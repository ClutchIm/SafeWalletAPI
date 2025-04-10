#!/bin/sh
mkdir -p /app/logs

echo "Ожидание PostgreSQL..."
while ! nc -z "$DB_HOST" 5432; do sleep 1; done
echo "PostgreSQL запущен."

echo "Применяем миграции..."
python manage.py migrate --noinput

sleep 5

echo "Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000