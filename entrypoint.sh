#!/bin/sh

# Ejecutar las migraciones de la base de datos
echo "Running database migrations..."
python manage.py migrate --noinput

# Ejecutar el comando del CMD
exec "$@"
