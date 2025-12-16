#!/bin/bash

# Exit on error
set -e

echo "=========================================="
echo "Starting Inventory Management API"
echo "=========================================="

echo "Waiting for PostgreSQL..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2>&1; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "✓ PostgreSQL is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput
echo "✓ Migrations completed!"

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✓ Superuser created: {username} / {password}')
else:
    print(f'✓ Superuser "{username}" already exists')
    # Optional: Update password in case it was changed
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f'✓ Password reset to: {password}')
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected!"

echo "=========================================="
echo "Starting Gunicorn server..."
echo "API will be available at http://localhost:8000"
echo "=========================================="

# Start Gunicorn
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    --log-level info