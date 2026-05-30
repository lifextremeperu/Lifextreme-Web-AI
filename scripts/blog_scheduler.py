"""
============================================================
LIFEXTREME - Scheduler Diario del Blog Agent
Genera un artículo automáticamente cada día a las 7:00 AM
============================================================
"""

import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Importar el agente
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from blog_agent import main as generar_articulo

# ── Logging ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/blog_scheduler.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ── Tarea programada ──────────────────────────────────────
async def tarea_diaria():
    log.info(f"⏰ Iniciando generación diaria de artículo: {datetime.now()}")
    try:
        articulo = await generar_articulo()
        log.info(f"✅ Artículo publicado: {articulo.titulo}")
    except Exception as e:
        log.error(f"❌ Error en generación diaria: {e}")

# ── Scheduler ─────────────────────────────────────────────
async def iniciar_scheduler():
    os.makedirs("logs", exist_ok=True)
    scheduler = AsyncIOScheduler()
    
    # Todos los días a las 7:00 AM hora de Cusco (UTC-5)
    scheduler.add_job(
        tarea_diaria,
        CronTrigger(hour=7, minute=0, timezone="America/Lima"),
        id="blog_diario",
        name="Generador Blog SEO Diario"
    )
    
    scheduler.start()
    log.info("🟢 Scheduler iniciado. Próxima publicación: mañana a las 7:00 AM")
    log.info("   Presiona Ctrl+C para detener.")
    
    try:
        # Generar uno inmediatamente al iniciar (opcional)
        print("\n¿Generar un artículo ahora mismo para probar? [s/n]: ", end="")
        respuesta = input().strip().lower()
        if respuesta == "s":
            await tarea_diaria()
        
        # Mantener corriendo
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        log.info("🔴 Scheduler detenido.")
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(iniciar_scheduler())
