FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear carpeta para SQLite por si se usa ese motor
RUN mkdir -p /app/data

EXPOSE 5000

CMD ["python", "app.py"]