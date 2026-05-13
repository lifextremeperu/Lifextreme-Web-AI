# Usar una imagen de Python ligera
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar requerimientos e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la API y la base de datos de conocimiento
COPY main.py .
COPY ../chroma_db ./chroma_db

# Exponer el puerto 8000
EXPOSE 8000

# Comando para arrancar el servidor
CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8000"]
