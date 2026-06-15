import os
import sys
import requests
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def get_embedding(text):
    try:
        response = requests.post("http://localhost:11434/api/embed", json={
            "model": "nomic-embed-text",
            "input": [text]
        })
        return response.json()['embeddings'][0]
    except Exception as e:
        print(f"Error Ollama Embed: {e}")
        return None

def chat(prompt):
    try:
        response = requests.post("http://localhost:11434/api/chat", json={
            "model": "phi3:latest",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        })
        return response.json()['message']['content']
    except Exception as e:
        return f"Error Ollama Chat: {e}"

def test_max(query):
    print("=========================================================")
    print(f"👤 USUARIO: {query}")
    print("=========================================================\n")
    
    print("[1] Vectorizando la pregunta...")
    emb = get_embedding(query)
    
    print("[2] Buscando en Supabase (Base de Conocimiento RAG)...")
    res = supabase.rpc("match_knowledge_vectors", {
        "query_embedding": emb,
        "match_threshold": 0.3,
        "match_count": 5
    }).execute()
    
    context = ""
    for idx, match in enumerate(res.data):
        print(f"    -> [Match {idx+1} | Similitud: {match['similarity']:.2f}] {match.get('region', '').upper()} - {match.get('modulo_nombre', '')}")
        context += f"- {match.get('text_content', '')}\n"
        
    print("\n[3] Generando respuesta con MAX (Ollama Local)...")
    
    prompt = f"""Eres MAX, el Asesor Comercial y de Aventura Extrema de Lifextreme.
Tu tono es entusiasta, experto, servicial y persuasivo.
Usa estrictamente la información de nuestra base de datos para responder a la pregunta del usuario.

CONOCIMIENTO DE LIFEXTREME (RAG):
{context}

PREGUNTA DEL USUARIO:
{query}
"""
    
    respuesta = chat(prompt)
    print("\n🤖 MAX (Respuesta Final en Vivo):")
    print("---------------------------------------------------------")
    print(respuesta)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    query = "Hola MAX, quiero hacer trekking en Huaraz (Áncash) pero que no sea la típica Laguna 69 que está llena de gente. ¿Qué ruta secreta o menos conocida recomiendan que sea un verdadero reto y cómo es el clima?"
    test_max(query)
