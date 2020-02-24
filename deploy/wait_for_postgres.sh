#!/bin/bash

set -e
cmd="$@"

until PGPASSWORD=$DB_PASSWORD psql -v ON_ERROR_STOP=1 --host "$DB_HOST" --port "$DB_PORT" --username "$DB_USER" --password "$PGPASSWORD" --dbname "$DB_NAME" -c '\q'; do
  >&2 echo "[PSQL::WAITING] Ожидаю подключения к $DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
  sleep 3
done

>&2 echo "[PSQL::SUCCESS] Подключено к $DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
exec $cmd