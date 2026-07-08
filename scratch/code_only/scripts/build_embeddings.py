import os
import json
import sys
from langchain_google_vertexai import VertexAIEmbeddings, VectorSearchVectorStore
from langchain_core.documents import Document

# Forzar codificacion UTF-8 en consola Windows
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ID = "project-7ccd00cc-f448-42df-90a"
REGION = "us-central1"

print(f"[1] Iniciando configuracion Vertex AI en proyecto: {PROJECT_ID}...")

try:
    embeddings = VertexAIEmbeddings(
        model_name="text-embedding-004", 
        project=PROJECT_ID, 
        location=REGION
    )
except Exception as e:
    print(f"Error inicializando Vertex AI: {e}")
    sys.exit(1)

JSONL = 'data/cixtur_knowledge.jsonl'
DB_DIR = 'chroma_db'

print("[2] Leyendo Dataset Cixtur...")
docs = []
try:
    with open(JSONL, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            content = f"PREGUNTA: {data['prompt']}\nRESPUESTA: {data['completion']}"
            doc = Document(page_content=content, metadata={"source": data['source']})
            docs.append(doc)
    print(f"  -> {len(docs)} registros cargados.")
except Exception as e:
    print(f"Error leyendo JSONL: {e}")
    sys.exit(1)

print("[3] Generando Vectores de IA y guardando en Vertex AI Vector Search...")
try:
    index_id = os.getenv("VECTOR_SEARCH_INDEX_ID")
    endpoint_id = os.getenv("VECTOR_SEARCH_ENDPOINT_ID")
    
    if not index_id or not endpoint_id:
        print("ERROR: VECTOR_SEARCH_INDEX_ID o VECTOR_SEARCH_ENDPOINT_ID no están definidos.")
        print("Ejecuta primero python scripts/init_vertex_search.py")
        sys.exit(1)
        
    vectorstore = VectorSearchVectorStore.from_components(
        project_id=PROJECT_ID,
        region=REGION,
        gcp_credentials=None,
        embedding=embeddings,
        index_id=index_id,
        endpoint_id=endpoint_id
    )
    
    print("Enviando documentos a Vector Search (el proceso por lotes es automático)...")
    vectorstore.add_documents(documents=docs)
            
    print("\n[EXITO] Cerebro Vectorial guardado exitosamente en Vertex AI!")
except Exception as e:
    print(f"\n[ERROR] Falló la vectorización: {e}")
