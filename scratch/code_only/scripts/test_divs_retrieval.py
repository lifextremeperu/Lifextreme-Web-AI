import os
from dotenv import load_dotenv
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer

# 1. Cargar credenciales
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Cargando modelo de búsqueda (BGE-M3)...")
embedder = SentenceTransformer('BAAI/bge-m3')

def test_query(pregunta: str):
    print(f"\n==========================================")
    print(f"🔍 PREGUNTA: '{pregunta}'")
    print(f"==========================================")
    
    # 2. Convertir la pregunta en vectores (1024 dimensiones)
    query_embedding = embedder.encode(pregunta).tolist()
    
    # 3. Buscar en la bóveda de Supabase
    try:
        response = supabase.rpc(
            'match_knowledge_chunks',
            {
                'query_embedding': query_embedding,
                'match_threshold': 0.3, # Similitud mínima (0.3 es bastante flexible)
                'match_count': 3        # Traer los 3 mejores resultados
            }
        ).execute()
        
        resultados = response.data
        
        if not resultados:
            print("❌ No se encontró nada relevante en la base de datos.")
            return
            
        print(f"✅ Se encontraron {len(resultados)} resultados relevantes:\n")
        
        for i, res in enumerate(resultados, 1):
            similitud = res.get('similarity', 0) * 100
            meta = res.get('metadata', {})
            origen = meta.get('archivo_origen', 'Desconocido')
            region = meta.get('region', 'Desconocido')
            texto = res.get('content', '')
            
            print(f"RESULTADO #{i} (Similitud: {similitud:.1f}%)")
            print(f"📂 Origen: {origen} (Región: {region.upper()})")
            print(f"📄 Extracto: {texto[:300]}...\n")
            
    except Exception as e:
        print(f"Error al conectar con Supabase: {e}")

if __name__ == "__main__":
    # ¡Prueba con algo que sepas que está en los 6 PDFs de ICA!
    test_query("¿Qué tours o actividades se pueden hacer en Lunahuaná?")
    test_query("¿Dónde queda el cañón de los perdidos?")
