FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY backend/discord_agent/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del agente
COPY backend/discord_agent /app/backend/discord_agent
COPY .env /app/.env

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 8008

CMD ["python", "-m", "backend.discord_agent.main"]
