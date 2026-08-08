import os
import sys
import glob
import json
import time
import requests
import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# ==========================================
# CONFIGURACIÓN 100% LOCAL (CERO NUBE)
# ==========================================
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL_EMBED = "nomic-embed-text"
MODEL_CHAT = "phi3:latest"

QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_CEO = "Lifextreme_CEO_Vault"
TENANT_ID = "ceo_private"

# Directorio base de los documentos de la empresa
DOCS_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME"

def init_qdrant_ceo():
    """Inicializa Qdrant asegurando la creación aislada de la colección CEO."""
    qclient = QdrantClient(url=QDRANT_URL)
    
    if not qclient.collection_exists(COLLECTION_CEO):
        print(f"[*] Bóveda confidencial {COLLECTION_CEO} no existe. Creando...")
        qclient.create_collection(
            collection_name=COLLECTION_CEO,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    else:
        print(f"[*] Bóveda confidencial {COLLECTION_CEO} conectada y aislada con éxito.")
        
    return qclient

def extract_financial_fqsas(text_content, doc_name):
    """Usa el LLM local para estructurar textos contables/estrategicos al CorporateSchema."""
    prompt = f"""
Eres el Analista Financiero B2B de Lifextreme. Tu objetivo es procesar documentos confidenciales del CEO.
Extrae la inteligencia financiera y operativa y devuélvela ESTRICTAMENTE como JSON:
{{
    "fqsas": [
        {{
            "q": "Pregunta estratégica (Ej. ¿Cuál es el costo del tour X? ¿Qué dice el contrato Y?)",
            "a": "Respuesta precisa."
        }}
    ]
}}

DOCUMENTO ({doc_name}):
{text_content[:20000]} # Limitamos para no sobrecargar Phi3 local
"""
    try:
        res = requests.post(OLLAMA_CHAT_URL, json={
            "model": MODEL_CHAT,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "format": "json",
            "stream": False
        })
        res.raise_for_status()
        result = res.json().get("message", {}).get("content", "{}")
        return json.loads(result).get("fqsas", [])
    except Exception as e:
        print(f"    [-] Error extrayendo inteligencia con {MODEL_CHAT}: {e}")
        return []

def generate_local_embeddings(texts):
    """Genera embeddings 100% locales."""
    response = requests.post(OLLAMA_EMBED_URL, json={
        "model": MODEL_EMBED,
        "input": texts
    })
    response.raise_for_status()
    return response.json().get("embeddings", [])

def main():
    print("===================================================================")
    print(" 💼 INICIANDO AGENTE FINANCIERO B2B (LÓBULO CEO PRIVADO) ")
    print("===================================================================")
    
    try:
        qclient = init_qdrant_ceo()
    except Exception as e:
        print(f"[-] No se pudo conectar a Qdrant Local: {e}")
        sys.exit(1)
        
    if not os.path.exists(DOCS_DIR):
        print(f"[-] ATENCIÓN: No se detecta el directorio confidencial en:\n    {DOCS_DIR}")
        print("    Verifica la ruta o conecta el disco duro correspondiente.")
        sys.exit(1)
        
    print(f"[+] Escaneando documentos corporativos en: {DOCS_DIR}")
    
    # Buscar archivos de texto plano, csv o markdown para procesar en primera fase
    doc_files = []
    for ext in ["*.txt", "*.csv", "*.md"]:
        doc_files.extend(glob.glob(os.path.join(DOCS_DIR, "**", ext), recursive=True))
        
    # Añadir también los insights estratégicos de PENTUR generados por la IA
    pentur_insights = glob.glob(r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\knowledge\peru\*\strategic_insights.json")
    doc_files.extend(pentur_insights)
        
    print(f"[+] Documentos iniciales legibles encontrados: {len(doc_files)}")
    
    vectores_subidos = 0
    
    for file_path in doc_files:
        doc_name = Path(file_path).name
        print(f"\n[>] Analizando documento: {doc_name}...")
        
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            fqsas = extract_financial_fqsas(content, doc_name)
            
            if not fqsas:
                print("    [-] No se extrajo inteligencia válida. Omitiendo.")
                continue
                
            print(f"    [+] {len(fqsas)} FQSAs extraídos. Vectorizando (Ollama)...")
            
            texts = [f"Doc: {doc_name}. P: {item.get('q','')} R: {item.get('a','')}" for item in fqsas]
            embeddings = generate_local_embeddings(texts)
            
            points = []
            for idx, emb in enumerate(embeddings):
                # Usar UUID5 para evitar duplicados EXACTOS si se corre 2 veces
                vector_id = f"{doc_name}_b2b_{idx}"
                vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, vector_id))
                
                payload = {
                    "document_name": doc_name,
                    "document_type": "strategic_internal",
                    "text_content": texts[idx],
                    "tenant_id": TENANT_ID
                }
                
                points.append(PointStruct(id=vector_uuid, vector=emb, payload=payload))
                
            qclient.upsert(collection_name=COLLECTION_CEO, points=points)
            vectores_subidos += len(points)
            print(f"    [✔] Bóveda Segura actualizada. (+{len(points)} vectores)")
            
        except Exception as e:
            print(f"    [-] Error procesando el archivo: {e}")
            
    print("===================================================================")
    print(f" ✅ LÓBULO CORPORATIVO ACTUALIZADO: {vectores_subidos} vectores en Lifextreme_CEO_Vault.")
    print("===================================================================")

if __name__ == "__main__":
    main()
