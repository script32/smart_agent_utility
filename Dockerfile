FROM python:3.11-slim

WORKDIR /app

# Dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    gcc build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar todo el código al contenedor
COPY . .

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto para FastAPI
EXPOSE 8000

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]