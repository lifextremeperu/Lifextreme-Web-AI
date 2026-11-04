import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID", "1567214643934527488")
DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY", "")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "lifextreme_internal_2026")
PORT = int(os.getenv("DISCORD_AGENT_PORT", "8008"))
