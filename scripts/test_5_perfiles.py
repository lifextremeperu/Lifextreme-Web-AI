import os
import sys
import json
import requests
from qdrant_client import QdrantClient

sys.stdout.reconfigure(encoding='utf-8')

QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_CHAT_URL = "http://localhost:11434/api/generate"
MODEL_EMBED = "nomic-embed-text"
MODEL_LLM = "llama3.2"  # o el modelo que estés usando localmente, ej: llama3, mistral

perfiles_pruebas = [
    {
        "perfil": "CEO / Operador de Turismo de Aventura",
        "pregunta": "Hay huelga en Sutran y lluvia intensa según Senamhi en la ruta Cusco-Puno, ¿qué protocolo legal y logístico aplico para no perder mi operación ni enfrentar demandas?"
    },
    {
        "perfil": "Consultor Legal / MINCETUR",
        "pregunta": "Un turista extranjero sufrió un accidente haciendo canotaje en Lunahuaná. Según la normativa nacional, ¿cuál es el protocolo de responsabilidad y el estándar de seguridad que debió cumplir la agencia?"
    },
    {
        "perfil": "Inversionista Extranjero / Banco",
        "pregunta": "Quiero invertir 2 millones de dólares en un Ecolodge de Alta Montaña en Huaraz. ¿Cuáles son los riesgos climáticos a 5 años y qué permisos del gobierno regional necesito?"
    },
    {
        "perfil": "Guía Oficial de Alta Montaña (Logística)",
        "pregunta": "Tengo un grupo de 15 personas para el Camino Inca mañana. Según el SERNANP y las normativas de Turismo Comunitario, ¿qué permisos y regulaciones debo cumplir si acampamos en zona campesina?"
    },
    {
        "perfil": "Estratega de Marketing (Agencia de Viajes)",
        "pregunta": "Los turistas de EE.UU. tienen miedo por las últimas alertas de viaje del Departamento de Estado. Crea un comunicado de prensa de mitigación basándote en la seguridad real operativa que manejamos en el sur del país."
    }
]

def obtener_embedding(texto):
    try:
        res = requests.post(OLLAMA_EMBED_URL, json={
            "model": MODEL_EMBED,
            "input": texto
        })
        if res.status_code == 200:
            return res.json().get('embeddings', [])[0]
        else:
            print(f"Error en Ollama Embed: {res.text}")
            return None
    except Exception as e:
        print(f"Error conectando a Ollama (Embed): {e}")
        return None

def buscar_contexto(qclient, vector, k=3):
    try:
        resultados = qclient.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=k
        )
        contexto_str = ""
        for i, res in enumerate(resultados):
            texto = res.payload.get("text", "")
            fuente = res.payload.get("source", "Desconocido")
            contexto_str += f"\n--- [Documento {i+1} | Fuente: {fuente}] ---\n{texto}\n"
        return contexto_str
    except Exception as e:
        print(f"Error consultando Qdrant: {e}")
        return ""

def generar_respuesta(perfil, pregunta, contexto):
    prompt = f"""Eres Lifextreme AI, el Oráculo Supremo del Turismo Peruano.
Responde de manera ejecutiva y precisa asumiendo el rol adecuado para ayudar a este usuario.
PERFIL DEL USUARIO: {perfil}
PREGUNTA: {pregunta}

Utiliza SOLAMENTE el siguiente contexto extraído de tu base de conocimiento legal y estratégica para responder. 
Si el contexto no tiene toda la respuesta, usa tus capacidades lógicas pero priorizando siempre las normativas peruanas adjuntas.

CONTEXTO:
{contexto}

RESPUESTA (Formato profesional):
"""
    try:
        res = requests.post(OLLAMA_CHAT_URL, json={
            "model": MODEL_LLM,
            "prompt": prompt,
            "stream": False
        })
        if res.status_code == 200:
            return res.json().get('response', '')
        else:
            return f"Error en Ollama Chat: {res.text}"
    except Exception as e:
        return f"Error conectando a Ollama (Chat): {e}"

def main():
    print("==========================================================")
    print("🚀 INICIANDO PRUEBA DE ESTRÉS: 5 PERFILES TURÍSTICOS (RAG)")
    print("==========================================================")
    
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
        total = qclient.get_collection(COLLECTION_NAME).points_count
        print(f"[*] Conectado a Qdrant. Base de conocimiento: {total} vectores activos.\n")
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a Qdrant: {e}")
        sys.exit(1)
        
    for i, test in enumerate(perfiles_pruebas):
        print(f"🔵 PRUEBA {i+1}/5 | PERFIL: {test['perfil']}")
        print(f"   PREGUNTA: {test['pregunta']}")
        print("   [*] Generando vector de búsqueda...")
        
        vector = obtener_embedding(test['pregunta'])
        if not vector:
            continue
            
        print("   [*] Buscando en los 27,500+ documentos (Qdrant)...")
        contexto = buscar_contexto(qclient, vector)
        
        print("   [*] Razonando respuesta con Ollama...\n")
        respuesta = generar_respuesta(test['perfil'], test['pregunta'], contexto)
        
        print("================ RESPUESTA DEL ORÁCULO ================")
        print(respuesta)
        print("=======================================================\n")
        
if __name__ == "__main__":
    main()
