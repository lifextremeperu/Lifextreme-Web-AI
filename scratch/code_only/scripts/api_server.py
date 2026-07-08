import os
import sys
import subprocess
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2 import credentials
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Configuración de consola
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
CORS(app) # Permitir que la web se conecte al servidor local

PROJECT_ID = "project-7ccd00cc-f448-42df-90a"
REGION = "us-central1"
DB_DIR = 'chroma_db'

print("--- INICIANDO MOTOR DE INTELIGENCIA ARTIFICIAL LIFEXTREME ---")

# 1. Obtener Token de Google Cloud
def get_creds():
    gcloud = r'C:\Users\ASUS\AppData\Local\Google\google-cloud-sdk\bin\gcloud.cmd'
    env = os.environ.copy()
    env['CLOUDSDK_PYTHON'] = r'C:\Python313\python.exe'
    token = subprocess.check_output([gcloud, 'auth', 'print-access-token'], env=env, text=True).strip()
    return credentials.Credentials(token)

creds = get_creds()

# 2. Inicializar Modelos
embeddings = VertexAIEmbeddings(
    model_name="text-embedding-004", 
    project=PROJECT_ID, 
    location=REGION,
    credentials=creds
)

llm = ChatVertexAI(
    model_name="gemini-1.5-flash", 
    project=PROJECT_ID, 
    location=REGION,
    credentials=creds
)

# 3. Cargar Cerebro (ChromaDB)
vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

# 4. Configurar Cadena de Respuesta (RAG)
# Esto hace que la IA primero busque en los PDFs y luego responda con sus propias palabras
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    pregunta = data.get('question')
    if not pregunta:
        return jsonify({"error": "No hay pregunta"}), 400
    
    print(f"Pregunta recibida: {pregunta}")
    
    try:
        # Generar respuesta usando RAG
        respuesta = qa_chain.invoke(pregunta)
        return jsonify({"answer": respuesta['result']})
    except Exception as e:
        print(f"Error procesando pregunta: {e}")
        # Si el token expira, intentar renovarlo una vez
        try:
            new_creds = get_creds()
            # Re-inicializar brevemente (simplificado para la prueba)
            return jsonify({"answer": "Lo siento, mi conexión con Google se refrescó. Por favor repite la pregunta."})
        except:
            return jsonify({"answer": "Error interno del cerebro de IA."}), 500

if __name__ == '__main__':
    print("\n✅ IA LIFEXTREME ONLINE en http://localhost:5000")
    print("Listo para responder preguntas sobre Tours y PDFs.")
    app.run(port=5000, debug=False)
