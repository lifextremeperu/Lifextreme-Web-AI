import os
os.environ['OPENAI_API_KEY'] = 'ollama'
os.environ['OPENAI_BASE_URL'] = 'http://localhost:11434/v1'

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .max_agent import process_message
import uvicorn
import traceback

app = FastAPI(title="Lifextreme MAX AI OS v2.0 - RAG Real")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/webhook/lifextreme")
async def chat_webhook(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        if not message:
            raise HTTPException(status_code=400, detail="message is required")
        
        history      = data.get("history", [])
        user_context = data.get("profile", {})
        
        response = await process_message(
            prompt=message,
            history=history,
            user_data=user_context
        )
        # response es un dict con keys: mensaje, datos_cotizacion, action_required
        return response

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        return {
            "mensaje": (
                "Disculpa, estoy teniendo un problema tecnico. "
                "Escríbenos por WhatsApp: +51 958 050 928 y te atendemos al instante."
            ),
            "datos_cotizacion": None,
            "action_required": None,
            "error": str(e)[:200]
        }

@app.get("/health")
def health():
    return {
        "status": "LIFEXTREME MAX OS online",
        "rag": "Supabase knowledge_vectors (101,737 vectores)",
        "llm": "qwen2.5:7b via Ollama",
        "embedding": "nomic-embed-text"
    }
