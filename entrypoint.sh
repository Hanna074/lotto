#!/bin/sh
# DB가 준비될 때까지 최대 30초 대기
echo "Waiting for database..."
for i in $(seq 1 30); do
  python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotto_project.settings')
django.setup()
from django.db import connection
connection.ensure_connection()
print('DB is ready!')
" 2>/dev/null && break
  echo "  ($i) DB not ready, retrying in 1s..."
  sleep 1
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn lotto_project.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -
