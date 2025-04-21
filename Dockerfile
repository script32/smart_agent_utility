FROM python:3.11-slim

# Instala dependencias del sistema necesarias para compilar algunos paquetes
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . .

# Asegura versiones estables
RUN pip install --upgrade pip setuptools wheel

# Instala semantic-kernel y el resto de las dependencias
RUN pip install semantic-kernel==1.28.1
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
