import os
import sys
import json
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

def get_local_embedding(text):
    # Usar el modelo local nomic-embed-text para tener consistencia con la DB
    url = "http://localhost:11434/api/embed"
    response = requests.post(url, json={"model": "nomic-embed-text", "input": text})
    if response.status_code == 200:
        return response.json().get("embeddings", [])[0]
    return None

def extract_graph_entities_local(text_content):
    url = "http://localhost:11434/api/chat"
    
    prompt = f"""
    Eres un experto en Grafos de Conocimiento (Knowledge Graphs).
    Tu tarea es extraer entidades (Nodos) y relaciones (Aristas) del siguiente texto operativo.
    
    TEXTO:
    {text_content}
    
    Extrae la información en estricto formato JSON con la siguiente estructura, respondiendo ÚNICAMENTE con el JSON, sin texto extra, sin markdown ni backticks:
    {{
        "nodes": [
            {{"node_id": "identificador_unico_en_minusculas", "node_name": "Nombre Legible", "node_type": "Lugar|Organizacion|Proyecto|Infraestructura", "description": "Breve descripcion"}}
        ],
        "edges": [
            {{"source_node_id": "id_nodo_1", "target_node_id": "id_nodo_2", "relation_type": "conecta_con|depende_de|financia|afecta_a|pertenece_a"}}
        ]
    }}
    """
    
    payload = {
        "model": "phi3:latest",
        "messages": [
            {"role": "system", "content": "You must only respond with valid JSON object without any additional text or formatting."},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "format": "json"  # Forzamos JSON en Ollama
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        content = response.json().get("message", {}).get("content", "")
        
        # Limpiar posibles backticks si el modelo los añade a pesar de todo
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        print(f"Error extrayendo entidades con Ollama local: {e}")
        return None

def main():
    print("=== Iniciando Extracción GraphRAG Piloto (LOCAL OLLAMA) ===")
    load_dotenv()
    
    # Supabase config
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Extraer una muestra de FQSAs de Cusco para el piloto
    print("Obteniendo FQSAs de muestra...")
    res = supabase.table("knowledge_vectors").select("text_content").ilike("vector_id", "cusco%").limit(5).execute()
    fqsas = res.data
    
    if not fqsas:
        print("No se encontraron FQSAs de Cusco para la prueba.")
        return
        
    for idx, fqsa in enumerate(fqsas):
        text = fqsa.get("text_content", "")
        print(f"\nProcesando FQSA {idx+1}...")
        
        graph_data = extract_graph_entities_local(text)
        if not graph_data:
            continue
            
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        print(f"  Encontrados {len(nodes)} nodos y {len(edges)} aristas.")
        
        # Insertar Nodos
        for node in nodes:
            try:
                emb = get_local_embedding(node["description"])
                if emb:
                    node["embedding"] = emb
                supabase.table("knowledge_nodes").upsert(node, on_conflict="node_id").execute()
            except Exception as e:
                print(f"  Error insertando nodo {node.get('node_id')}: {e}")
                
        # Insertar Aristas
        for edge in edges:
            try:
                # Verificar que ambos nodos existan antes de insertar la arista
                supabase.table("knowledge_edges").insert(edge).execute()
            except Exception as e:
                pass
                
    print("\n=== Extracción Piloto Completada ===")

if __name__ == "__main__":
    main()
