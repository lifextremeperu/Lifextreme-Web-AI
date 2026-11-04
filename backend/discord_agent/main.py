"""
Microservicio Híbrido FastAPI + discord.py para Lifextreme.
Ejecuta concurrentemente en un único Event Loop con ciclo de vida (lifespan) asíncrono.
"""
import asyncio
import logging
from contextlib import asynccontextmanager
import discord
from discord.ext import commands
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import uvicorn

from .config import (
    DISCORD_BOT_TOKEN,
    API_SECRET_KEY,
    PORT
)
from .cogs_assistant import AssistantCog

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("lifextreme-discord")

# Configurar intents de Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!lfx ", intents=intents, help_command=None)

@bot.event
async def on_ready():
    logger.info(f"⚡ Bot conectado exitosamente a Discord como: {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Rutas & Expediciones en Perú 🏔️ | @Lifextreme Bot"
        )
    )

# Ciclo de vida asíncrono unificado con FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Registrar Cogs
    await bot.add_cog(AssistantCog(bot))
    
    # Iniciar bot de Discord en segundo plano sin bloquear FastAPI
    bot_task = None
    if DISCORD_BOT_TOKEN:
        logger.info("Iniciando conexión WebSocket de Discord...")
        bot_task = asyncio.create_task(bot.start(DISCORD_BOT_TOKEN))
    else:
        logger.warning("DISCORD_BOT_TOKEN no configurado en .env")

    yield

    # Cierre ordenado
    if not bot.is_closed():
        logger.info("Cerrando sesión de Discord...")
        await bot.close()
    if bot_task:
        bot_task.cancel()

app = FastAPI(
    title="Lifextreme Discord Agent API",
    version="1.0.0",
    lifespan=lifespan
)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización inválido"
        )
    return credentials.credentials

# Esquemas Pydantic
class RouteAnnouncement(BaseModel):
    title: str
    difficulty: str
    distance_km: float
    max_altitude_m: int
    summary: str
    route_url: HttpUrl
    image_url: Optional[HttpUrl] = None

class CommunityAlert(BaseModel):
    channel_name_or_id: Optional[str] = "general"
    title: str
    description: str
    color: int = 0x5865F2

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "bot_connected": bot.is_ready(),
        "bot_user": str(bot.user) if bot.user else None,
        "guilds_count": len(bot.guilds) if bot.is_ready() else 0
    }

@app.post("/api/v1/announce-route")
async def announce_route(payload: RouteAnnouncement, token: str = Security(verify_token)):
    """Despacha un Embed oficial de una nueva ruta al canal de Discord."""
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="El bot de Discord aún no está conectado al servidor.")
    
    # Buscar canal general o rutas
    target_channel = None
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name in ["rutas", "expediciones", "general"]:
                target_channel = channel
                break
        if target_channel:
            break

    if not target_channel:
        raise HTTPException(status_code=404, detail="No se encontró un canal de texto disponible en el servidor.")

    embed = discord.Embed(
        title=f"🏔️ Nueva Expedición: {payload.title}",
        url=str(payload.route_url),
        description=payload.summary,
        color=0xF59E0B
    )
    embed.add_field(name="Dificultad", value=payload.difficulty, inline=True)
    embed.add_field(name="Distancia", value=f"{payload.distance_km} km", inline=True)
    embed.add_field(name="Altitud Máxima", value=f"{payload.max_altitude_m} msnm", inline=True)
    if payload.image_url:
        embed.set_image(url=str(payload.image_url))
    embed.set_footer(text="Lifextreme Club • Aventura & Expediciones en Perú")

    await target_channel.send(content="⚡ **¡Atención Comunidad! Nueva ruta disponible en el catálogo:**", embed=embed)
    return {"status": "announced", "channel": target_channel.name}

if __name__ == "__main__":
    uvicorn.run("backend.discord_agent.main:app", host="0.0.0.0", port=PORT, reload=False)
