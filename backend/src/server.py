import os
os.environ['OPENAI_API_KEY'] = 'ollama'
os.environ['OPENAI_BASE_URL'] = 'http://localhost:11434/v1'

import re
import json
import asyncio
import traceback
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .max_agent import process_message, process_message_stream
from .rag_service import find_matching_catalog_item
from .partner_agent import process_b2b_stream

app = FastAPI(title="Lifextreme MAX AI OS v2.5 - Hybrid Catalog + Qdrant + Groq LPU")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _extract_pax(text: str, history: list) -> int:
    """Detecta el numero de personas mencionado por el cliente en la conversacion."""
    combined = " ".join(
        [str(m.get("content", "")) for m in (history or []) if isinstance(m, dict) and m.get("role") == "user"]
        + [text]
    ).lower()
    m = re.search(r"(\d+)\s*(?:personas|amigos|adultos|viajeros|integrantes|pax|pasajeros)", combined)
    if m:
        val = int(m.group(1))
        if 1 <= val <= 50:
            return val
    if "pareja" in combined or "dos personas" in combined or "somos 2" in combined or "para 2" in combined:
        return 2
    return 1


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
        return response

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        return {
            "mensaje": (
                "Disculpa, estoy teniendo un problema técnico. "
                "Escríbenos por WhatsApp: +51 958 050 928 y te atendemos al instante."
            ),
            "datos_cotizacion": None,
            "action_required": None,
            "error": str(e)[:200]
        }


@app.post("/webhook/lifextreme/stream")
async def chat_webhook_stream(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        if not message:
            raise HTTPException(status_code=400, detail="message is required")

        history = data.get("history", [])
        user_context = data.get("profile", {})

        async def event_generator():
            try:
                full_chunks = []
                async for chunk in process_message_stream(message, history, user_context):
                    full_chunks.append(chunk)

                raw_text = "".join(full_chunks).strip()

                # 1. Extraer etiqueta [CARRITO: Tour | PrecioTotal | Pax] si el modelo la genero
                cotizacion = None
                cart_match = re.search(r"\[CARRITO:\s*([^|\]]+)\|\s*(\d+(?:\.\d+)?)\s*\|\s*(\d+)\s*\]", raw_text, re.IGNORECASE)
                if cart_match:
                    tour_name = cart_match.group(1).strip()
                    precio_total = int(float(cart_match.group(2)))
                    pax = int(cart_match.group(3)) or 1
                    if precio_total <= 0:
                        item = find_matching_catalog_item(tour_name) or find_matching_catalog_item(raw_text)
                        precio_total = (item["price_per_pax"] if item else 450) * pax
                    cotizacion = {
                        "tour": tour_name,
                        "precio_total": precio_total,
                        "pax": pax,
                        "monto_reserva_hoy": round(precio_total * 0.30),
                        "link_pago_niubiz": f"https://wa.me/51958050928?text=Hola%20Lifextreme,%20quiero%20reservar%20{tour_name}%20({pax}%20Pax)%20con%20el%2030%25%20(S/%20{round(precio_total*0.30)})"
                    }

                # Limpiar cualquier etiqueta [CARRITO...] completa o incompleta del texto visible
                clean_text = re.sub(r"\[CARR[^\]]*\]?", "", raw_text, flags=re.IGNORECASE).strip()

                # 2. Si no hubo etiqueta pero el usuario o MAX mencionan un tour concreto y reservar/precio, crear cotizacion automatica
                if not cotizacion:
                    matched_item = find_matching_catalog_item(clean_text) or find_matching_catalog_item(message)
                    if matched_item:
                        pax = _extract_pax(message, history)
                        precio_total = matched_item["price_per_pax"] * pax
                        cotizacion = {
                            "tour": matched_item["tour"],
                            "precio_total": precio_total,
                            "pax": pax,
                            "monto_reserva_hoy": round(precio_total * 0.30),
                            "link_pago_niubiz": f"https://wa.me/51958050928?text=Hola%20Lifextreme,%20quiero%20reservar%20{matched_item['tour']}%20({pax}%20Pax)%20con%20el%2030%25%20(S/%20{round(precio_total*0.30)})"
                        }

                # 3. Emitir en fragmentos de ~65 caracteres con micro-pausa de 20ms:
                #    GARANTIZA CERO SILABAS COMIDAS en cualquier navegador (incluso con JS en cache)
                step = 65
                for i in range(0, len(clean_text), step):
                    piece = clean_text[i:i + step]
                    yield f"data: {json.dumps({'chunk': piece})}\\n\n\n"
                    await asyncio.sleep(0.02)

                # 4. Emitir evento de cotizacion para activar el boton del Carrito de Compras
                if cotizacion:
                    yield f"data: {json.dumps({'cotizacion': cotizacion})}\\n\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\\n\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook/b2b/stream")
async def chat_webhook_b2b_stream(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        if not message:
            raise HTTPException(status_code=400, detail="message is required")

        history = data.get("history", [])
        user_context = data.get("profile", {})

        async def event_generator():
            try:
                async for chunk in process_b2b_stream(message, history, user_context):
                    yield f"data: {json.dumps({'chunk': chunk})}\\n\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\\n\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {
        "status": "LIFEXTREME MAX OS online",
        "qdrant_vectors": 336869,
        "collections": {
            "Lifextreme_FQSA_Knowledge": 176216,
            "Lifextreme_Knowledge": 160653
        },
        "catalog_items": {
            "tours": 40,
            "events": 28,
            "parks": 164,
            "guides": 4,
            "equips": 15,
            "total": 251
        },
        "rag": "Catalogo Oficial Web (40 Tours, 28 Eventos, 164 Parques) + Qdrant (336,869 vectores)",
        "llm": "Groq LPU (openai/gpt-oss-120b) + Ollama Fallback",
        "embedding": "FastEmbed Multilingual MiniLM-L12-v2 (384-dim)"
    }

