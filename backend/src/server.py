from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .max_agent import process_message
from .market_agent import market_agent
from .operations_agent import OpsAgent
from .models import PerfilUsuario
import uvicorn

app = FastAPI(title="Lifextreme AI OS v1.0")
ops = OpsAgent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/webhook/lifextreme")
async def chat_webhook(request: Request):
    data = await request.json()
    message = data.get("message")
    history = data.get("history", [])
    user_context = data.get("profile", {})
    perfil = PerfilUsuario(
        nivel_experiencia=user_context.get("nivel", "Intermedio"),
        interes_principal="Expedición",
        es_socio_elite=user_context.get("es_elite", False)
    )
    response = await process_message(message, history=history, user_data=perfil)
    return response.dict()

@app.post("/market/research")
async def market_research(topic: str):
    """Lanza una misión de investigación de mercado."""
    result = await market_agent.run(f"Investiga profundamente sobre: {topic}")
    return result.data

@app.get("/ops/health")
async def system_health():
    """Reporte de salud operativa de Lifextreme."""
    return await ops.check_system_health()

@app.get("/health")
def health():
    return {"status": "LIFEXTREME OS is online 🏔️"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
