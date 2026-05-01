FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para Reflex (curl, unzip para Bun)
RUN apt-get update && apt-get install -y curl unzip

# Copiar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Inicializar Reflex y exponer puertos (3000 Frontend, 8001 Reflex Backend)
EXPOSE 3000
EXPOSE 8001

# Ejecutar Reflex
CMD ["reflex", "run", "--frontend-port", "3000", "--backend-port", "8001", "--env", "dev"]
