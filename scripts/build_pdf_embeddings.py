import os
import sys
import subprocess
from google.oauth2 import credentials
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Forzar codificacion UTF-8
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ID = "project-7ccd00cc-f448-42df-90a"
REGION = "us-central1"
DB_DIR = 'chroma_db'
SOURCE_DIR = r'D:\HUB-CUSCO-2026\apps\data\knowledge\lifextreme\sources'

print(f"[1] Autenticando con Google Cloud...")
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

print("[2] Leyendo PDFs locales...")
all_docs = []
pdf_files = []

for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(root, file))

print(f"    Se encontraron {len(pdf_files)} PDFs. Extrayendo texto (esto tomará un tiempo)...")

# Configuramos el cortador de texto: pedazos de 1000 caracteres, con 100 de superposicion para no cortar ideas a medias
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

procesados = 0
fallidos = 0
for pdf_path in pdf_files:
    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        # Cortamos el documento
        splits = text_splitter.split_documents(docs)
        # Añadir al arreglo total
        all_docs.extend(splits)
        procesados += 1
        if procesados % 10 == 0:
            print(f"    Leidos {procesados}/{len(pdf_files)} PDFs...")
    except Exception as e:
        fallidos += 1
        print(f"    Error leyendo {os.path.basename(pdf_path)}")

print(f"\n[3] Generando Vectores de IA para {len(all_docs)} fragmentos de texto...")
print("    Esto tomará unos minutos y se procesará en lotes para no saturar la API.")

try:
    # Vertex AI limita a 20000 tokens por request, usamos batch de 20 fragmentos por seguridad extrema
    batch_size = 20
    # Abrimos la base de datos existente de Cixtur
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    total_batches = (len(all_docs)//batch_size) + 1
    for i in range(0, len(all_docs), batch_size):
        batch = all_docs[i:i + batch_size]
        print(f"    Subiendo lote {i//batch_size + 1}/{total_batches}...")
        vectorstore.add_documents(documents=batch)
            
    print(f"\n[EXITO] {len(all_docs)} fragmentos de PDF inyectados exitosamente en el Cerebro: {DB_DIR}/")
    if fallidos > 0:
        print(f"Nota: {fallidos} PDFs no pudieron ser leidos por estar dañados o protegidos.")
except Exception as e:
    print(f"\n[ERROR] Falló la vectorización: {e}")
