import os
import json
import sys
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Forzar codificacion UTF-8 en consola Windows
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ID = "project-7ccd00cc-f448-42df-90a"
REGION = "us-central1"

print(f"[1] Iniciando configuracion Vertex AI en proyecto: {PROJECT_ID}...")

import subprocess
from google.oauth2 import credentials

# Obtener token
gcloud = r'C:\Users\ASUS\AppData\Local\Google\google-cloud-sdk\bin\gcloud.cmd'
env = os.environ.copy()
env['CLOUDSDK_PYTHON'] = r'C:\Python313\python.exe'

try:
    token = subprocess.check_output([gcloud, 'auth', 'print-access-token'], env=env, text=True).strip()
    creds = credentials.Credentials(token)
    
    embeddings = VertexAIEmbeddings(
        model_name="text-embedding-004", 
        project=PROJECT_ID, 
        location=REGION,
        credentials=creds
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

print("[3] Generando Vectores de IA y guardando en ChromaDB...")
print("    Esto tomará unos minutos porque se procesarán 6,555 textos en lotes de 250.")
try:
    # Vertex AI soporta maximo 250 instancias o 20000 tokens por peticion
    batch_size = 50
    vectorstore = None
    
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        print(f"    Procesando lote {i//batch_size + 1}/{(len(docs)//batch_size) + 1}...")
        if vectorstore is None:
            vectorstore = Chroma.from_documents(
                documents=batch, 
                embedding=embeddings, 
                persist_directory=DB_DIR
            )
        else:
            vectorstore.add_documents(documents=batch)
            
    print(f"\n[EXITO] Cerebro Vectorial guardado exitosamente en: {DB_DIR}/")
except Exception as e:
    print(f"\n[ERROR] Falló la vectorización: {e}")
