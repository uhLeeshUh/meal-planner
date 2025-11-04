#!/bin/bash
set -e

echo "Waiting for database to be ready..."
# Wait for PostgreSQL to be ready (max 30 attempts, 2 seconds apart)
max_attempts=30
attempt=0

until python -c "
import os, sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
try:
    engine = create_engine(os.getenv('DATABASE_URL'))
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    sys.exit(0)
except (OperationalError, Exception):
    sys.exit(1)
" 2>/dev/null; do
  attempt=$((attempt + 1))
  if [ $attempt -ge $max_attempts ]; then
    echo "Database connection failed after $max_attempts attempts"
    exit 1
  fi
  echo "Database is unavailable - sleeping (attempt $attempt/$max_attempts)"
  sleep 2
done

echo "Database is ready! Running migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

