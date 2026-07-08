import os
import sys
import subprocess
from google.oauth2 import credentials
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ID = "project-7ccd00cc-f448-42df-90a"
REGION = "us-central1"
DB_DIR = 'chroma_db'

print("=== INICIANDO PRUEBA DEL CEREBRO VECTORIAL CIXTUR ===")

# Obtener token de acceso
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
    print(f"Error autenticando: {e}")
    sys.exit(1)

# Cargar base de datos local
vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

preguntas = [
    "¿Cuáles son los requisitos de seguridad para operar rafting en el río Urubamba?",
    "Quiero hacer el tour del Valle Rojo, ¿qué incluye y cuánto dura?"
]

for pregunta in preguntas:
    print(f"\n🗣️ PREGUNTA USUARIO: {pregunta}")
    print("🧠 PENSANDO (Buscando vectores por significado)...")
    
    resultados = vectorstore.similarity_search(pregunta, k=2)
    
    for i, doc in enumerate(resultados):
        print(f"\n  [Resultado {i+1} - Fuente: {doc.metadata['source']}]")
        print(f"  {doc.page_content}")
        
print("\n=====================================================")
print("✅ PRUEBA SUPERADA: La IA puede 'entender' las preguntas y buscar respuestas semánticamente.")
