#!/bin/sh

# Recopilar archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Ejecutar las migraciones de la base de datos
echo "Running database migrations..."
python manage.py migrate --noinput

# Ejecutar el comando del CMD
exec "$@"
