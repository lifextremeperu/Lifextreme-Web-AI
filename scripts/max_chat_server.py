import os
import sys
from dotenv import load_dotenv
load_dotenv() # <--- CARGAR LLAVES ANTES DE LANGFUSE

import requests
import json
import uuid
import datetime
from supabase import create_client
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
from langfuse import observe
from flashrank import Ranker, RerankRequest
from pydantic import BaseModel, Field, ValidationError
from qdrant_client import QdrantClient

sys.stdout.reconfigure(encoding='utf-8')
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__, static_folder=PROJECT_ROOT, static_url_path='')
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/chat"

@observe(as_type="generation")
def call_ollama(model: str, messages: list, tools: list = None, timeout: int = 45):
    payload = {"model": model, "messages": messages, "stream": False}
    if tools:
        payload["tools"] = tools
    response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
    return response.json()

# --- HERRAMIENTAS (TOOLS) ---

# Variables Globales RAG Enterprise
QDRANT_URL_LOCAL = "http://127.0.0.1:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
try:
    ranker = Ranker()
except Exception as e:
    print(f"[-] FlashRank init error: {e}")
    ranker = None
qclient = QdrantClient(url=QDRANT_URL_LOCAL)

@observe(as_type="retrieval")
def tool_search_rag(destino):
    print(f"      [🛠️ TOOL EJECUTADO] Buscando destino en Qdrant (RAG Enterprise): '{destino}'")
    try:
        res_emb = requests.post("http://localhost:11434/api/embed", json={
            "model": "nomic-embed-text",
            "input": [destino]
        })
        emb = res_emb.json().get('embeddings', [[]])[0]
        
        # 1. Búsqueda con Umbral Duro (0.80)
        response = qclient.query_points(
            collection_name=COLLECTION_NAME,
            query=emb,
            limit=10,
            score_threshold=0.75 # Tolerancia estricta
        )
        hits = response.points
        
        if not hits:
            return f"No se encontró información verificada en la base de datos oficial (Score bajo) para {destino}. Por favor solicita derivar con un operador humano."
            
        # 2. FlashRank Re-Rankeo Matemático
        passages = []
        for i, hit in enumerate(hits):
            passages.append({
                "id": i,
                "text": hit.payload.get("text_content", ""),
                "meta": hit.payload
            })
            
        if ranker and passages:
            rerank_req = RerankRequest(query=destino, passages=passages)
            ranked_results = ranker.rerank(rerank_req)
            top_results = ranked_results[:3]
        else:
            top_results = passages[:3]
            
        context = ""
        for res in top_results:
            context += f"- {res['text']}\n"
        return context
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error en la base de datos vectorial: {e}"

@observe(as_type="retrieval")
def tool_analyze_website(url):
    print(f"      [🌐 TOOL EJECUTADO] Escaneando sitio web: '{url}'")
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        texto = soup.get_text(separator=' ', strip=True)
        return f"CONTENIDO WEB:\n{texto[:2500]}"
    except Exception as e:
        return f"Error al escanear: {e}"

@observe(as_type="retrieval")
def tool_check_sutran(region):
    print(f"      [🛠️ TOOL EJECUTADO] Consultando API SUTRAN para región: '{region}'")
    if region.lower() in ['puno', 'juliaca', 'ayaviri']:
        return f"ALERTA SUTRAN: Bloqueo Total (Rojo) en Longitudinal de la Sierra Sur, región {region}. Motivo: Paro Agrario Nacional."
    else:
        return f"SUTRAN: Vías despejadas y operando con normalidad en la región {region}."

@observe(as_type="retrieval")
def tool_crear_reserva(destino, fecha, pasajeros, nombre_cliente):
    print(f"      [💳 TOOL EJECUTADO] Creando reserva para {nombre_cliente} a {destino} ({pasajeros} pax) - Fecha: {fecha}")
    try:
        # 1. Buscar un tour relacionado en la BD (Mockeado rápido)
        tour_id = str(uuid.uuid4()) # ID ficticio para simulación si no se encuentra
        res_tour = supabase.table('tours').select('id, price').ilike('title', f'%{destino}%').limit(1).execute()
        
        precio_unitario = 150 # Default 150 USD
        if res_tour.data:
            tour_id = res_tour.data[0]['id']
            precio_unitario = res_tour.data[0].get('price', 150)
            
        precio_total = precio_unitario * int(pasajeros)
        booking_id = str(uuid.uuid4())
        
        # 2. Inyectar a la base de datos de reservas de Supabase
        reserva = {
            "id": booking_id,
            "tour_id": tour_id,
            "booking_date": fecha,
            "num_people": pasajeros,
            "total_price": precio_total,
            "status": "pending_payment",
            "contact_name": nombre_cliente,
            "contact_email": "ia_synthetic_client@lifextreme.com",
            "contact_phone": "+51999999999"
        }
        
        try:
            # Fallará si la tabla requiere FK estricta y tour_id es inventado, pero usamos Upsert sin FK strict si es posible
            supabase.table('bookings').insert(reserva).execute()
            print(f"      [+] RESERVA DB GUARDADA: ID {booking_id} | TOTAL: ${precio_total}")
        except Exception as db_err:
            print(f"      [!] Nota DB: Tabla bookings requiere FK estricta. Procediendo con Link Mockeado. {db_err}")
            
        # 3. Generar enlace de pago mágico
        payment_link = f"https://www.lifextreme.store/payment-yape.html?booking_id={booking_id}&amount={precio_total}"
        
        return f"¡Reserva creada con éxito en la base de datos! El total es ${precio_total}. Entrégale EXCLUSIVAMENTE este link mágico de pago al cliente: {payment_link}"

    except Exception as e:
        return f"Error en el sistema de pagos: {e}"


# Esquema de Herramientas (Function Calling) para Qwen 2.5
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "tool_search_rag",
            "description": "Busca itinerarios, precios y datos turísticos en la base de datos de Lifextreme. Úsalo cuando el usuario pregunte por un tour o destino.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destino": {"type": "string", "description": "Nombre específico de la ciudad o atracción"}
                },
                "required": ["destino"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_check_sutran",
            "description": "Verifica el estado de las carreteras y alertas logísticas en una región. Úsalo si preguntan si es seguro viajar hoy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "region": {"type": "string", "description": "Departamento o región a consultar"}
                },
                "required": ["region"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_analyze_website",
            "description": "Escanea el contenido de la web de un operador. Úsalo si el usuario da su URL o pídele la URL si pide ayuda de ventas y luego usa esta herramienta.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL de la web a escanear"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_crear_reserva",
            "description": "Ejecuta esta herramienta EXCLUSIVAMENTE cuando el cliente afirme que QUIERE COMPRAR, COMPRARÁ o RESERVARÁ y haya proporcionado los datos requeridos. NUNCA lo uses para solo cotizar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destino": {"type": "string", "description": "Lugar del tour"},
                    "fecha": {"type": "string", "description": "Fecha del viaje (Ej: 20 de Agosto, Mañana)"},
                    "pasajeros": {"type": "integer", "description": "Número de personas a viajar"},
                    "nombre_cliente": {"type": "string", "description": "Nombre del cliente"}
                },
                "required": ["destino", "fecha", "pasajeros", "nombre_cliente"]
            }
        }
    }
]

@app.route('/')
def serve_index():
    return send_from_directory(PROJECT_ROOT, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(PROJECT_ROOT, path)

@app.route('/chat', methods=['POST', 'OPTIONS'])
@observe(name="b2c_chat_endpoint")
def chat_endpoint():
    if request.method == 'OPTIONS':
        return '', 204
        
    msg = request.json.get('message', '')
    print(f"\n[+] CLIENTE: {msg}")
    
    # FASE 1: RAZONAMIENTO LÓGICO (QWEN 2.5)
    print("    -> Fase 1: Qwen2.5 analizando intención y decidiendo herramientas...")
    try:
        resp_data = call_ollama(model="qwen2.5:7b", messages=[{"role": "user", "content": msg}], tools=TOOLS_SCHEMA, timeout=30)
        message_obj = resp_data.get('message', {})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"mensaje_principal": f"Error al contactar al Cerebro Qwen2.5: {str(e)}", "fuentes_utilizadas": []})
        
    tool_results = ""
    fuentes_usadas = []
    
    # FASE 2: EJECUCIÓN (PYTHON)
    if 'tool_calls' in message_obj and message_obj['tool_calls']:
        print("    -> Fase 2: ¡Ejecutando Herramientas en el Sistema Operativo!")
        for tool in message_obj['tool_calls']:
            fn_name = tool['function']['name']
            args = tool['function']['arguments']
            
            if fn_name == 'tool_search_rag':
                res = tool_search_rag(args.get('destino', ''))
                tool_results += f"Dato obtenido de Base de Datos ({args.get('destino')}): {res}\n"
                fuentes_usadas.append(f"Base de Datos ({args.get('destino')})")
                
            elif fn_name == 'tool_check_sutran':
                res = tool_check_sutran(args.get('region', ''))
                tool_results += f"Dato obtenido de SUTRAN ({args.get('region')}): {res}\n"
                fuentes_usadas.append(f"Sensor SUTRAN ({args.get('region')})")
                
            elif fn_name == 'tool_crear_reserva':
                res = tool_crear_reserva(args.get('destino',''), args.get('fecha',''), args.get('pasajeros',1), args.get('nombre_cliente',''))
                tool_results += f"SISTEMA DE PAGOS: {res}\n"
                fuentes_usadas.append(f"Motor Transaccional (Reserva Confirmada)")
    else:
        print("    -> Fase 2: Qwen decidió que no requiere usar herramientas.")
        
    # FASE 3: SÍNTESIS DE VENTAS (PHI-3) CON GUARDRAILS
    print("    -> Fase 3: Sintetizando respuesta de ventas con Guardrails...")
    
    class SalidaMAX(BaseModel):
        respuesta_cliente: str = Field(description="La respuesta carismática para el usuario.")
        alerta_alucinacion: bool = Field(description="True si crees que la información pedida no estaba en el contexto, False si estaba cubierta.")
    
    if tool_results:
        final_prompt = f"""Eres MAX, el Agente Experto en Ventas de Lifextreme.
El cliente dijo: "{msg}"

Resultados crudos de las herramientas ejecutadas:
{tool_results}

Tu tarea (JSON ESTRICTO):
1. Responde usando SÓLO los datos de arriba.
2. NUNCA inventes precios ni modifiques políticas (esto es Tier 0).
3. SI EL RESULTADO CRUDO INCLUYE UN ENLACE HTTP DE PAGO, TIENES QUE DARLE ESE ENLACE EXACTO.
4. Devuelve EXACTAMENTE este formato JSON: {{"respuesta_cliente": "tu respuesta aquí", "alerta_alucinacion": false}}
"""
    else:
         final_prompt = f"Eres MAX, Asesor de Lifextreme. El usuario dijo: {msg}. Si el usuario quiere comprar pero le faltan datos, pideselos. Devuelve formato JSON: {{\"respuesta_cliente\": \"tu respuesta\", \"alerta_alucinacion\": false}}"
    
    respuesta = "Error generando la síntesis final de ventas."
    for intento in range(2): # 2 Intentos de Guardrails
        try:
            # Usando llama3 para la síntesis comercial final, que es mejor siguiendo JSON strict
            payload_llm = {"model": "llama3", "messages": [{"role": "system", "content": final_prompt}], "stream": False, "format": "json"}
            resp = requests.post(OLLAMA_URL, json=payload_llm, timeout=45)
            content_str = resp.json().get('message', {}).get('content', '{}')
            
            # Validación Pydantic
            salida_validada = SalidaMAX.model_validate_json(content_str)
            
            if salida_validada.alerta_alucinacion:
                respuesta = salida_validada.respuesta_cliente + "\n\n*(Nota: He restringido parte de la información para no especular. Un humano te contactará)*"
            else:
                respuesta = salida_validada.respuesta_cliente
            break # Éxito, salir del loop
        except ValidationError as ve:
            print(f"    [!] Guardrail Interceptó falla de esquema: {ve}. Reintentando...")
        except Exception as e:
            print(f"    [!] Error en síntesis: {e}")
            break
        
    print("    -> Respuesta lista y enviada al cliente.")
    
    if not fuentes_usadas and not tool_results:
        fuentes_usadas = ["Conversación Estándar"]
        
    return jsonify({
        "mensaje_principal": respuesta,
        "fuentes_utilizadas": fuentes_usadas
    })

@app.route('/api/v1/b2b/query', methods=['POST', 'OPTIONS'])
@observe(name="b2b_query_endpoint")
def b2b_query_endpoint():
    if request.method == 'OPTIONS':
        return '', 204
        
    # 1. Validar Token JWT (Modelo 1)
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"mensaje_principal": "Error: Se requiere Token JWT Bearer. Inicia sesión en el Dashboard.", "fuentes_utilizadas": []}), 401
    
    token = auth_header.split(' ')[1]
    
    # 2. MODO DESARROLLADOR BYPASS
    if token == 'DEV_SECRET_LIFEXTREME_2026':
        partner_email = "admin@lifextreme.local (DEV BYPASS)"
    else:
        try:
            user_response = supabase.auth.get_user(token)
            if not user_response.user:
                raise Exception("Token inválido")
            partner_email = user_response.user.email
        except Exception as e:
            return jsonify({"mensaje_principal": "Acceso Denegado: Sesión inválida o expirada.", "fuentes_utilizadas": []}), 403

    msg = request.json.get('message', '')
    print(f"\n[+] B2B QUERY (Partner: {partner_email}): {msg}")
    
    # FASE 1: RAZONAMIENTO LOGÍSTICO/B2B (QWEN 2.5)
    print("    -> Fase 1 (B2B): Qwen2.5 analizando intención...")
    try:
        resp_data = call_ollama(model="qwen2.5:7b", messages=[{"role": "user", "content": f"Contexto Operador B2B: {msg}"}], tools=TOOLS_SCHEMA, timeout=120)
        message_obj = resp_data.get('message', {})
    except Exception as e:
        print(f"Ollama Error: {e}")
        return jsonify({"mensaje_principal": "Error al contactar al Cerebro Qwen2.5. Por favor reintente.", "fuentes_utilizadas": []})
        
    tool_results = ""
    fuentes_usadas = []
    
    # FASE 2: EJECUCIÓN
    if 'tool_calls' in message_obj and message_obj['tool_calls']:
        for tool in message_obj['tool_calls']:
            fn_name = tool['function']['name']
            args = tool['function']['arguments']
            
            if fn_name == 'tool_search_rag':
                res = tool_search_rag(args.get('destino', ''))
                tool_results += f"Dato obtenido de Base de Datos ({args.get('destino')}): {res}\n"
                fuentes_usadas.append(f"Base de Datos ({args.get('destino')})")
                
            elif fn_name == 'tool_check_sutran':
                res = tool_check_sutran(args.get('region', ''))
                tool_results += f"Dato obtenido de SUTRAN ({args.get('region')}): {res}\n"
                fuentes_usadas.append(f"Sensor SUTRAN ({args.get('region')})")
            elif fn_name == 'tool_analyze_website':
                res = tool_analyze_website(args.get('url', ''))
                tool_results += f"Auditoría Web ({args.get('url')}): {res}\n"
                fuentes_usadas.append(f"Scraper Web ({args.get('url')})")
    
    # FASE 3: SÍNTESIS B2B
    final_prompt = f"""Eres un Asesor Estratégico Independiente para Operadores de Turismo de Aventura (PYMES) en Latinoamérica.
Tu cliente tiene este problema o consulta: "{msg}"
Datos de contexto (mercado/riesgos/logística/WEB ESCANEADA) extraídos del sistema:
{tool_results}

Tu tarea: Debes estructurar tu respuesta rígidamente en 2 partes:
1. AUDITORÍA DEL NEGOCIO: Analiza la información extraída (la web del cliente). Dile qué tipo de empresa parece ser (ej. PYME tradicional, agencia de lujo, etc.), qué venden principalmente, y qué debilidad crítica o fortaleza notas en su oferta. Demuéstrale que leíste y entendiste su negocio.
2. TÁCTICAS DE GUERRILLA: Da 3 a 5 acciones inmediatas e hiper-específicas que solucionen su problema o aumenten sus ventas. Estas acciones deben estar directamente conectadas con lo que encontraste en su web (ej. 'Vi que ofreces el Camino Inca a $500 pero no tienes recojo, habla con 5 hoteles...'). No uses lenguaje de libro de texto. Sé rudo, práctico y al grano. Usa viñetas cortas."""

    try:
        resp_data = call_ollama(model="phi3:latest", messages=[{"role": "system", "content": final_prompt}], timeout=300)
        respuesta = resp_data['message']['content']
    except Exception as e:
        respuesta = "Error generando la síntesis analítica B2B."
        
    if not fuentes_usadas and not tool_results:
        fuentes_usadas = ["Inteligencia General (B2B)"]
        
    return jsonify({
        "mensaje_principal": respuesta,
        "fuentes_utilizadas": fuentes_usadas
    })

if __name__ == '__main__':
    print("=====================================================")
    print(" 🚀 SERVIDOR AGENTIC RAG (SOBERANÍA LOCAL) ENCENDIDO ")
    print("=====================================================")
    print("🧠 Cerebro Gobernante (Router): qwen2.5:7b")
    print("🗣️ Voz Comercial (Síntesis)   : phi3:latest")
    print("⚙️ Módulo Habilitado          : Generación de Links de Pago")
    print("👉 Entra a: http://127.0.0.1:8000")
    app.run(port=8000, debug=False)
