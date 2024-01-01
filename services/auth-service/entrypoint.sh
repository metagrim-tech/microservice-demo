#!/usr/bin/env sh
set -ex

# Extract the postgres hostname and port from the supplied args.
arg="$1"

HOST="${arg%%:*}"
PORT="${arg#*:}"

# Make sure the service can communicate with the DB before proceeding.
until nc -w 1 -z ${HOST} ${PORT}; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
sleep 2
>&2 echo "Postgres is up - executing command"

# Make sure the service automatically runs alembic migrations before proceeding.
until export PYTHONPATH=./src && alembic upgrade head; do
  >&2 echo "Alembic is unavailable - sleeping"
  sleep 1
done
sleep 2
>&2 echo "Alembic is up - executing command"

# Run app
cd /app && export PYTHONPATH=./src && python3 src/auth_service
