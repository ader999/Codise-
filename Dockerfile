FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Dar permisos de ejecución al entrypoint por si se perdieron en el copiado
RUN chmod +x entrypoint.sh

# Configurar el puerto
EXPOSE 8000

# Script de entrada para correr migraciones en inicio
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto para arrancar la app con Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
