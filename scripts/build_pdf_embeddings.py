import os
import sys
import subprocess
import shutil
from google.cloud import aiplatform
from langchain_google_vertexai import VertexAIEmbeddings, VectorSearchVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()

# Forzar codificacion UTF-8
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "project-7ccd00cc-f448-42df-90a")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
TMP_PDF_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME"

print(f"[1] Buscando PDFs localmente en: {TMP_PDF_DIR} ...")
if not os.path.exists(TMP_PDF_DIR):
    print(f"Error: La carpeta local {TMP_PDF_DIR} no existe.")
    sys.exit(1)

print("\n[2] Inicializando Vertex AI y Embeddings...")
class SmartVertexEmbeddings(VertexAIEmbeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        all_embeddings = []
        batch_size = 50
        print(f"    Calculando vectores matematicos locales para {len(texts)} fragmentos de PDF...")
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            try:
                emb = super().embed_documents(batch)
                all_embeddings.extend(emb)
                print(f"    Calculados: {min(i+batch_size, len(texts))}/{len(texts)}")
            except Exception as e:
                print(f"    Error en lote, reintentando con batch mas pequeño... {e}")
                for j in range(0, len(batch), 10):
                    small_batch = batch[j:j+10]
                    all_embeddings.extend(super().embed_documents(small_batch))
        return all_embeddings

try:
    embeddings = SmartVertexEmbeddings(
        model_name="text-embedding-004", 
        project=PROJECT_ID, 
        location=REGION
    )
    index_id = os.getenv("VECTOR_SEARCH_INDEX_ID")
    endpoint_id = os.getenv("VECTOR_SEARCH_ENDPOINT_ID")
    
    if not index_id or not endpoint_id:
        print("ERROR: VECTOR_SEARCH_INDEX_ID o VECTOR_SEARCH_ENDPOINT_ID no definidos.")
        sys.exit(1)
        
    vectorstore = VectorSearchVectorStore.from_components(
        project_id=PROJECT_ID,
        region=REGION,
        gcs_bucket_name="lifextreme-knowledge-cusco",
        gcp_credentials=None,
        embedding=embeddings,
        index_id=index_id,
        endpoint_id=endpoint_id
    )
except Exception as e:
    print(f"Error inicializando Vertex AI: {e}")
    sys.exit(1)

print("\n[3] Procesando y extrayendo texto de PDFs...")
all_docs = []
pdf_files = []

for root, dirs, files in os.walk(TMP_PDF_DIR):
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(root, file))

print(f"    Se encontraron {len(pdf_files)} PDFs locales. Cortando en fragmentos...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

procesados = 0
fallidos = 0
for pdf_path in pdf_files:
    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        splits = text_splitter.split_documents(docs)
        all_docs.extend(splits)
        procesados += 1
        if procesados % 10 == 0:
            print(f"    Leidos {procesados}/{len(pdf_files)} PDFs...")
    except Exception as e:
        fallidos += 1
        print(f"    Error leyendo {os.path.basename(pdf_path)}")

print(f"\n[4] ¡DISPARO MASIVO INICIADO! Procesando {len(all_docs)} fragmentos de PDF...")
print("    - Langchain calculará todos los vectores en tu PC.")
print("    - Subirá un archivo JSONL a tu Bucket.")
print("    - Le ordenará a Google Cloud que inyecte todo de golpe.")

try:
    # Ingesta masiva en un solo llamado
    vectorstore.add_documents(documents=all_docs)
            
    print(f"\n[EXITO] {len(all_docs)} fragmentos de PDF inyectados exitosamente en el Cerebro Vectorial de Google Cloud!")
    if fallidos > 0:
        print(f"Nota: {fallidos} PDFs no pudieron ser leidos por estar dañados o protegidos.")
        
except Exception as e:
    print(f"\n[ERROR] Falló la vectorización: {e}")
