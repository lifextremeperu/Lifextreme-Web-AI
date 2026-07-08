import os
from supabase import create_client, Client
from dotenv import load_dotenv

def check_rag():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    print("Consultando estado real de Supabase (sin límite)...")
    try:
        # Contar total en knowledge_chunks (Base bruta original de 34k)
        res_chunks = supabase.table("knowledge_chunks").select("id", count="exact").limit(1).execute()
        total_chunks = res_chunks.count if hasattr(res_chunks, 'count') else 0
        
        # Contar total en knowledge_vectors (Nueva base Nomic)
        res_vectors = supabase.table("knowledge_vectors").select("id", count="exact").limit(1).execute()
        total_vectors = res_vectors.count if hasattr(res_vectors, 'count') else 0
        
        # Obtener un resumen de las regiones únicas
        res_regiones = supabase.table("knowledge_vectors").select("region").execute()
        regiones = set([r.get("region", "desconocido").capitalize() for r in res_regiones.data])
        
        print("\n=== REPORTE REAL SUPABASE ===")
        print(f"Total Base Original (Chunks): {total_chunks} registros (Incluye Sudamérica/Perú bruto)")
        print(f"Total Base Vectorizada (Nomic): {total_vectors} vectores listos para RAG")
        print(f"Regiones vectorizadas actualmente: {', '.join(regiones)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_rag()
