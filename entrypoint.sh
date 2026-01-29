#!/bin/sh
set -e

# Dockerローカル Postgres 待機
if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for database..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
  done
  echo "Database started"
fi

# マイグレーション
python manage.py migrate --noinput

# collectstatic は本番だけ実行
if [ "$DEBUG" = "False" ]; then
  python manage.py collectstatic --noinput
fi

exec "$@"