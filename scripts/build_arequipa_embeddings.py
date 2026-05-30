import os
import sys
import json
import glob
from google.cloud import aiplatform
from langchain_google_vertexai import VertexAIEmbeddings, VectorSearchVectorStore
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "lifextreme-arequipa-agent")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
INDEX_ID = os.getenv("VECTOR_SEARCH_INDEX_ID")
ENDPOINT_ID = os.getenv("VECTOR_SEARCH_ENDPOINT_ID")
GCS_BUCKET = "lifextreme-knowledge-arequipa"

print("[1] Iniciando Maniobra Batch Masiva para AREQUIPA...")

# 1. Wrapper Inteligente para los Embeddings
class SmartVertexEmbeddings(VertexAIEmbeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        all_embeddings = []
        batch_size = 50
        print(f"    Calculando vectores matemáticos para {len(texts)} textos...")
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            try:
                emb = super().embed_documents(batch)
                all_embeddings.extend(emb)
                print(f"    Calculados: {min(i+batch_size, len(texts))}/{len(texts)}")
            except Exception as e:
                print(f"    Error en lote, reintentando con batch de 10... {e}")
                for j in range(0, len(batch), 10):
                    small_batch = batch[j:j+10]
                    all_embeddings.extend(super().embed_documents(small_batch))
        return all_embeddings

embeddings = SmartVertexEmbeddings(
    model_name="text-embedding-004", 
    project=PROJECT_ID, 
    location=REGION
)

# 2. Inicializar el VectorStore
print(f"[2] Conectando a Vertex AI Vector Search (Index: {INDEX_ID})...")
vectorstore = VectorSearchVectorStore.from_components(
    project_id=PROJECT_ID,
    region=REGION,
    gcs_bucket_name=GCS_BUCKET,
    gcp_credentials=None,
    embedding=embeddings,
    index_id=INDEX_ID,
    endpoint_id=ENDPOINT_ID
)

# 3. Leer los datos minados
print("[3] Consolidando las FQSAs Profundas de Arequipa...")
docs = []
archivos_json = glob.glob("data/knowledge/arequipa/fqsas_deep/*.json")

total_fqsas = 0
for ruta_archivo in archivos_json:
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        datos = json.load(f)
        destino_id = datos.get("destino_id", "DESCONOCIDO")
        enfoques = datos.get("fqsas", {})
        
        for angulo, preguntas in enfoques.items():
            for p in preguntas:
                pregunta = p.get("pregunta", "")
                respuesta = p.get("respuesta", "")
                if pregunta == "ERROR": continue
                
                # Crear el documento para vectorizar
                contenido = f"PREGUNTA: {pregunta}\nRESPUESTA: {respuesta}"
                metadatos = {
                    "source": "arequipa_expert",
                    "modulo": destino_id,
                    "angulo": angulo
                }
                docs.append(Document(page_content=contenido, metadata=metadatos))
                total_fqsas += 1

print(f"    [+] Se encontraron {total_fqsas} FQSAs válidas listas para el cerebro.")

if total_fqsas == 0:
    print("    [-] No hay datos para subir. Terminando.")
    sys.exit(0)

# 4. Ingesta Masiva
print(f"\n[4] ¡DISPARO MASIVO INICIADO! Subiendo al Bucket {GCS_BUCKET}...")
print("    - Langchain calculará todos los vectores en tu PC.")
print("    - Subirá el archivo JSONL a tu Bucket.")
print("    - Le ordenará a Google Cloud que reinicie su cerebro con los nuevos datos.")

try:
    vectorstore.add_documents(documents=docs)
    print("\n========================================================")
    print("✅ ¡EXITO! LA ORDEN FUE ENVIADA A GOOGLE CLOUD")
    print("========================================================")
    print("Ya puedes cerrar esta ventana. Vertex AI está actualizando su base de datos en la nube.")
    print("El proceso en la nube tardará unos 30-45 minutos en reflejarse.")
except Exception as e:
    print(f"\n[ERROR CRITICO]: {e}")
