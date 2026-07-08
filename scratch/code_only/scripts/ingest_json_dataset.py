import os
import sys
import json
from google.cloud import aiplatform
from langchain_google_vertexai import VertexAIEmbeddings, VectorSearchVectorStore
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

# Forzar codificacion UTF-8
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "project-7ccd00cc-f448-42df-90a")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
DATASET_PATH = r"data\knowledge\lifextreme\knowledge_base.json"

print(f"[1] Leyendo Dataset CIXTUR desde {DATASET_PATH}...")
try:
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    faqs = dataset.get('data', [])
    print(f"    Se encontraron {len(faqs)} preguntas y respuestas estructuradas.")
except Exception as e:
    print(f"Error leyendo el JSON: {e}")
    sys.exit(1)

print("\n[2] Inicializando Vertex AI y Embeddings...")
try:
    embeddings = VertexAIEmbeddings(
        model_name="text-embedding-004", 
        project=PROJECT_ID, 
        location=REGION
    )
    index_id = os.getenv("VECTOR_SEARCH_INDEX_ID")
    endpoint_id = os.getenv("VECTOR_SEARCH_ENDPOINT_ID")
    
    if not index_id or not endpoint_id:
        print("ERROR: VECTOR_SEARCH_INDEX_ID o VECTOR_SEARCH_ENDPOINT_ID no definidos.")
        print("Por favor, configura las variables de entorno primero.")
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

print("\n[3] Preparando Documentos para Langchain...")
docs = []
for faq in faqs:
    # Combinamos pregunta y respuesta para que la IA entienda el contexto completo
    content = f"PREGUNTA: {faq.get('question', '')}\nRESPUESTA: {faq.get('answer', '')}"
    metadata = {
        "id": faq.get('id', ''),
        "category": faq.get('category', 'General'),
        "source": "CIXTUR_DATASET"
    }
    docs.append(Document(page_content=content, metadata=metadata))

print(f"\n[4] Generando Vectores de IA para {len(docs)} fragmentos...")
print("    Esto tomará unos minutos. Langchain enviará lotes a Vertex AI Vector Search...")

try:
    # Ingesta en vivo por lotes de 50 para evitar limite de 20k tokens de la API
    batch_size = 50
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        vectorstore.add_documents(documents=batch)
        print(f"    Lote inyectado: {min(i+batch_size, len(docs))}/{len(docs)}")
        
    print(f"\n[EXITO] {len(docs)} FAQs inyectadas exitosamente en el Cerebro Vectorial de Google Cloud!")
except Exception as e:
    print(f"\n[ERROR] Falló la vectorización: {e}")
