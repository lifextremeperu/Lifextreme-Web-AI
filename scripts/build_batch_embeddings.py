import os
import sys
import json
from google.cloud import aiplatform
from langchain_google_vertexai import VertexAIEmbeddings, VectorSearchVectorStore
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "project-7ccd00cc-f448-42df-90a")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
INDEX_ID = os.getenv("VECTOR_SEARCH_INDEX_ID")
ENDPOINT_ID = os.getenv("VECTOR_SEARCH_ENDPOINT_ID")
GCS_BUCKET = "lifextreme-knowledge-arequipa"

print("[1] Iniciando Maniobra Batch Masiva para AREQUIPA...")

# 1. Wrapper Inteligente para evitar el limite de 20k tokens
class SmartVertexEmbeddings(VertexAIEmbeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        all_embeddings = []
        batch_size = 50
        print(f"    Calculando vectores matematicos locales para {len(texts)} textos...")
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            try:
                emb = super().embed_documents(batch)
                all_embeddings.extend(emb)
                print(f"    Calculados: {min(i+batch_size, len(texts))}/{len(texts)}")
            except Exception as e:
                print(f"    Error en lote, reintentando con batch mas pequeño... {e}")
                # Fallback to size 10
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
print("[2] Conectando a Vertex AI Vector Search...")
vectorstore = VectorSearchVectorStore.from_components(
    project_id=PROJECT_ID,
    region=REGION,
    gcs_bucket_name=GCS_BUCKET,
    gcp_credentials=None,
    embedding=embeddings,
    index_id=INDEX_ID,
    endpoint_id=ENDPOINT_ID
)

# 3. Leer los datos de Arequipa
print("[3] Cargando los archivos JSON de Arequipa...")
docs = []
data_dir = 'data/knowledge/arequipa/fqsas_deep'

try:
    if not os.path.exists(data_dir):
        print(f"Error: No se encontró la carpeta {data_dir}")
        sys.exit(1)
        
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    # El formato de Arequipa tiene "fqsas" como array
                    items = data.get('fqsas', [])
                    for i, item in enumerate(items):
                        pregunta = item.get('pregunta', '')
                        respuesta = item.get('respuesta', '')
                        if pregunta and respuesta:
                            docs.append(Document(
                                page_content=f"PREGUNTA: {pregunta}\nRESPUESTA: {respuesta}",
                                metadata={"source": f"arequipa_{filename}", "id": item.get('id', str(i))}
                            ))
                except json.JSONDecodeError as e:
                    print(f"⚠️ Error decodificando {filename}: JSON incompleto ({e}). Saltando archivo parcial.")
                    
    print(f"    Total FQSAs cargadas en memoria: {len(docs)}")
except Exception as e:
    print(f"Error leyendo directorio: {e}")
    sys.exit(1)

# 4. Ingesta Masiva (Un solo disparo)
print(f"\n[4] ¡DISPARO MASIVO INICIADO! Procesando {len(docs)} documentos...")
print("    - Langchain calculará todos los vectores en tu PC.")
print("    - Subirá un archivo JSONL a tu Bucket.")
print("    - Le ordenará a Google Cloud que reinicie su cerebro con todos los datos a la vez.")

try:
    vectorstore.add_documents(documents=docs)
    print("\n========================================================")
    print("✅ ¡EXITO! LA ORDEN FUE ENVIADA A GOOGLE CLOUD")
    print("========================================================")
    print("Ya puedes cerrar esta ventana, apagar tu computadora e irte a descansar.")
    print("Vertex AI está actualizando su base de datos en la nube. Tomará unos 30-45 minutos.")
except Exception as e:
    print(f"\n[ERROR CRITICO]: {e}")
