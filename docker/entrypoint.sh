#!/bin/bash

# Entrypoint script for production deployment
# This script runs before starting the Django application

set -e

echo "Starting Broadband B2C Platform..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

# Wait for Redis to be ready
echo "Waiting for Redis..."
REDIS_HOST=$(echo $REDIS_URL | cut -d'/' -f3 | cut -d':' -f1)
REDIS_PORT=$(echo $REDIS_URL | cut -d'/' -f3 | cut -d':' -f2)
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 0.1
done
echo "Redis is ready!"

# Generate any missing migration files (dev only)
echo "Generating migrations..."
python manage.py makemigrations --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create cache tables if needed
# python manage.py createcachetable

echo "Setup complete! Starting application..."

# Execute the main command
exec "$@"
