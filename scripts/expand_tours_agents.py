import json
import argparse
import os
import requests
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from supabase import create_client, Client

# IMPORTANTE: Este script requiere la librería de OpenAI o LangChain configurada para apuntar a Ollama local.
# pip install pydantic openai

import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    from openai import OpenAI
except ImportError:
    print("Por favor instala openai: pip install openai")
    exit(1)

# ==============================================================================
# 1. DEFINICIÓN DE ESTRUCTURAS PYDANTIC (EL MOLDE ESTRICTO)
# ==============================================================================
class ItineraryStep(BaseModel):
    day: int
    desc: str

class SensoryVariants(BaseModel):
    landscape: str
    comfort: str
    action: str

class TourStep(BaseModel):
    n: str = Field(description="Icono: 'G' (Inicio), 'dot' (Fin), o clase remixicon ej 'ri-mountain-fill'")
    t: str = Field(description="Título corto del paso (ej: 'Huaraz')")
    d: str = Field(description="Descripción muy corta (ej: 'Inicio' o '5,000m')")

class FaqItem(BaseModel):
    q: str = Field(description="Pregunta frecuente long-tail (ej: ¿Cuál es la mejor época para ir?)")
    a: str = Field(description="Respuesta directa y detallada")

class TourModel(BaseModel):
    id: int
    title: str = Field(description="Título SEO del Tour (max 60 chars)")
    dept: str = Field(description="Departamento en Perú")
    price: float
    duration: str
    difficulty: str
    img: str = Field(description="URL de imagen (ej: Unsplash)")
    detail: str = Field(description="Descripción corta (max 100 chars)")
    last_verified: str = Field(description="Fecha actual formato YYYY-MM-DD para frescura RAG")
    direct_answer_block: str = Field(description="Bloque AEO de 40-60 palabras respondiendo la duda principal del tour directamente")
    faqs: List[FaqItem] = Field(description="5 a 8 preguntas frecuentes para Schema FAQPage")
    genInfo: dict = Field(description="Diccionario con cancelPolicy, duration, availability, guide, groupSize")
    whatYouDo: List[str] = Field(description="4 viñetas de lo que hará el cliente")
    fullItinerary: List[ItineraryStep]
    inc: List[str] = Field(description="Lista de inclusiones")
    notSuitable: List[str] = Field(description="Lista de no apto para")
    meetingPoint: str
    importantInfo: str
    steps: List[TourStep]
    sensoryVariants: SensoryVariants

class DepartmentTours(BaseModel):
    tours: List[TourModel] = Field(description="Exactamente 5 tours para el departamento")

# ==============================================================================
# 2. CONFIGURACIÓN DEL CLIENTE LLM (Apuntando a Ollama Local o OpenAI)
# ==============================================================================
# Configurar para Ollama Local (Llama3) u otro modelo
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama' # No requiere key real
)

# ==============================================================================
# 3. PROMPT MULTI-AGENTE
# ==============================================================================
SYSTEM_PROMPT = """
Eres el Cerebro Comercial de Lifextreme, un sistema Multi-Agente experto en Turismo de Aventura Extrema en Perú.
Tu misión es actuar como 4 agentes combinados:
1. Analista de Mercado: Elige los 5 tours de aventura/trekking/supervivencia más rentables y buscados del departamento solicitado.
2. Copywriter Neuromarketing: Redacta títulos SEO épicos, itinerarios emocionantes y textos sensoriales (SensoryVariants) para cerrar ventas.
3. SEO Local Master (AEO): Genera el `direct_answer_block` de 40-60 palabras, las `faqs` reales (long-tail) y asigna `last_verified` con la fecha de hoy.
4. Arquitecto de Datos: Devuelve EXACTAMENTE un JSON estructurado según el esquema Pydantic proporcionado.

REGLAS ESTRICTAS:
- Genera EXACTAMENTE 5 tours.
- El departamento solicitado es el objetivo.
- Dificultad debe ser 'Baja', 'Media', 'Alta', 'Técnica' o 'Experto'.
- El campo 'steps' de cada tour debe tener exactamente 2 o 3 pasos (Inicio, Medio, Fin). Usa 'G' para inicio, 'dot' para fin.
- Solo devuelve JSON, sin markdown, sin texto fuera del JSON.
"""

# ==============================================================================
# 2.5. RAG CONTEXT (SUPABASE)
# ==============================================================================
def get_department_context(department: str) -> str:
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("⚠️ Variables SUPABASE_URL o SUPABASE_KEY faltantes. Procediendo SIN contexto RAG.")
        return ""
        
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # 1. Obtener embedding de Ollama
        url = "http://localhost:11434/api/embed"
        response = requests.post(url, json={"model": "nomic-embed-text", "input": f"Tours y turismo de aventura extremo en {department}, Peru"})
        query_vector = response.json().get("embeddings", [])[0]
        
        # 2. Buscar en Supabase
        res = supabase.rpc(
            "match_knowledge_vectors", 
            {"query_embedding": query_vector, "match_threshold": 0.3, "match_count": 5}
        ).execute()
        
        contextos = res.data if res.data else []
        texto_contexto = "\n---\n".join([c.get("text_content", "") for c in contextos])
        if texto_contexto:
            print(f"✅ Contexto RAG recuperado para {department} ({len(contextos)} fragmentos).")
            return f"\n\nCONTEXTO REAL DE NUESTRA BASE DE DATOS PARA {department.upper()}:\n" + texto_contexto
        else:
            print(f"⚠️ No se encontró contexto específico para {department} en la base de datos.")
            return ""
            
    except Exception as e:
        print(f"❌ Error al conectar con RAG Supabase: {e}")
        return ""

def generate_tours(department: str, start_id: int):
    print(f"🚀 Iniciando Enjambre de Agentes para el departamento: {department}...")
    
    # Construimos las instrucciones de schema Pydantic
    schema_json = DepartmentTours.model_json_schema()
    
    rag_context = get_department_context(department)
    
    user_prompt = f"""
    Genera los 5 mejores tours de aventura para el departamento de {department}.
    Asigna los IDs secuencialmente comenzando desde {start_id}.
    {rag_context}
    
    El JSON DEBE cumplir con este esquema.
    IMPORTANTE: El JSON devuelto debe ser un objeto con una única clave raíz llamada "tours" que contenga la lista de 5 tours.
    {json.dumps(schema_json, indent=2)}
    """
    
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama3:8b",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result_str = response.choices[0].message.content
            result_json = json.loads(result_str)
            
            # Validar con Pydantic
            validated_data = DepartmentTours(**result_json)
            return validated_data
            
        except Exception as e:
            print(f"⚠️ Intento {attempt + 1}/3 falló: {e}")
            if attempt == 2:
                print(f"❌ Error final tras 3 intentos. Abortando {department}.")
                return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Agent Tour Expander")
    parser.add_argument("--dept", type=str, required=True, help="Departamento de Perú (ej: Ancash, Ica)")
    parser.add_argument("--start_id", type=int, default=100, help="ID inicial para los nuevos tours")
    
    args = parser.parse_args()
    
    tours_data = generate_tours(args.dept, args.start_id)
    
    if tours_data:
        filename = f"tours_{args.dept.lower()}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(tours_data.model_dump_json(indent=4))
        
        print(f"✅ ¡Éxito! 5 tours generados y validados para {args.dept}.")
        print(f"📄 Datos guardados en {filename}.")
        print("Siguiente paso: Inyectar este JSON en js/data.js usando tu script de CI/CD.")
    else:
        print(f"❌ Falló la generación para {args.dept}. Abortando.")
        exit(1)
