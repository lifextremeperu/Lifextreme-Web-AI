import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

def get_local_embedding(text):
    url = "http://localhost:11434/api/embed"
    response = requests.post(url, json={"model": "nomic-embed-text", "input": text})
    if response.status_code == 200:
        return response.json().get("embeddings", [])[0]
    return None

def main():
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)
    
    query = "El puente de la Ruta Sur hacia Cusco está bloqueado, ¿a quién afecta?"
    print(f"--- CONSULTA GRAPHRAG ---")
    print(f"Pregunta: {query}\n")
    
    # 1. Búsqueda Vectorial sobre los NODOS (Graph Entrypoint)
    query_emb = get_local_embedding(query)
    
    try:
        # Llamar al RPC match_graph_nodes que creamos en setup_graphrag.sql
        # Nota: Si el SQL no se ha corrido, esto fallará. En ese caso usamos select() simulado.
        res = supabase.rpc("match_graph_nodes", {"query_embedding": query_emb, "match_threshold": 0.3, "match_count": 2}).execute()
        nodes = res.data
    except Exception as e:
        print("RPC 'match_graph_nodes' falló (Probablemente aún no has corrido el script SQL en Supabase).")
        nodes = []
        
    if not nodes:
        print("No se encontraron nodos principales para la consulta.")
        return
        
    print("1. Nodos semilla detectados (Entrada al Grafo):")
    for n in nodes:
        print(f"  - {n['node_name']} ({n['node_id']})")
        
    # 2. Travesía del Grafo (Encontrar vecinos)
    # Extraemos todos los IDs de los nodos semilla
    node_ids = [n['node_id'] for n in nodes]
    
    # Buscar aristas donde el origen o destino sea uno de los nodos semilla
    edges_res = supabase.table("knowledge_edges").select("*").in_("source_node_id", node_ids).execute()
    edges = edges_res.data
    
    edges_res2 = supabase.table("knowledge_edges").select("*").in_("target_node_id", node_ids).execute()
    edges.extend(edges_res2.data)
    
    print("\n2. Relaciones encontradas (Travesía del Grafo):")
    connected_nodes = set(node_ids)
    for edge in edges:
        print(f"  - [{edge['source_node_id']}] --({edge['relation_type']})--> [{edge['target_node_id']}]")
        connected_nodes.add(edge['source_node_id'])
        connected_nodes.add(edge['target_node_id'])
        
    print(f"\n3. Sub-grafo construido con {len(connected_nodes)} nodos interconectados.")
    print("   -> Ahora este contexto enriquecido con relaciones lógicas se envía a MAX (B2C) o CORE (B2B) para generar la respuesta final.")
    
if __name__ == "__main__":
    main()
