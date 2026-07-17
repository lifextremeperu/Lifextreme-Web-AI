import json
import time
import httpx
import sys
sys.stdout.reconfigure(encoding='utf-8')
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

# Configuración
QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_URL = "http://localhost:11434/api/embed"
COLLECTION = "Lifextreme_Knowledge"
TENANT_ID = "lifextreme"
GROUND_TRUTH_FILE = "data/ground_truth_benchmark.json"

def get_embedding(text):
    try:
        response = httpx.post(OLLAMA_URL, json={
            "model": "nomic-embed-text",
            "input": text
        }, timeout=30.0)
        return response.json().get('embeddings', [[]])[0]
    except Exception as e:
        print(f"Error obteniendo embedding: {e}")
        return []

def main():
    print("==================================================")
    print(" 📊 LIFEXTREME RAG BENCHMARK (GROUND TRUTH TEST)  ")
    print("==================================================")
    
    try:
        qclient = QdrantClient(url=QDRANT_URL)
        # Verificar conexion
        qclient.get_collections()
    except Exception as e:
        print(f"Error conectando a Qdrant: {e}. Asegúrate de que el contenedor Docker esté corriendo.")
        return

    with open(GROUND_TRUTH_FILE, 'r', encoding='utf-8') as f:
        benchmark_data = json.load(f)
        
    print(f"Cargadas {len(benchmark_data)} preguntas de evaluación.\n")
    
    hits = 0
    total = len(benchmark_data)
    
    start_time = time.time()
    
    for item in benchmark_data:
        q_id = item['id']
        question = item['question']
        expected = item['expected_answer_snippet'].lower().strip()
        
        # 1. Vectorizar pregunta
        emb = get_embedding(question)
        if not emb:
            print(f"[{q_id}] Fallo embedding.")
            continue
            
        # 2. Buscar en Qdrant (Filtrando por tenant_id SaaS)
        tenant_filter = Filter(
            must=[
                FieldCondition(
                    key="tenant_id",
                    match=MatchValue(value=TENANT_ID)
                )
            ]
        )
        
        try:
            results = qclient.query_points(
                collection_name=COLLECTION,
                query=emb,
                query_filter=tenant_filter,
                limit=3
            ).points
            
            # 3. Evaluar
            # Consideramos un "Hit" si el texto recuperado contiene palabras clave de la respuesta esperada
            # Para una evaluación estricta, verificamos si al menos una parte del expected snippet está en los top 3
            
            # Simplificamos la comparación: extraer palabras clave del snippet
            expected_words = set([w for w in expected.split() if len(w) > 4])
            
            found = False
            for res in results:
                retrieved_text = res.payload.get("text_content", "").lower()
                # Comprobar intersección de palabras clave
                match_count = sum(1 for w in expected_words if w in retrieved_text)
                if len(expected_words) == 0 or match_count >= (len(expected_words) * 0.3): # 30% match
                    found = True
                    break
                    
            if found:
                hits += 1
                status = "✅ HIT "
            else:
                status = "❌ MISS"
                
            print(f"{status} | P: {question[:50]}...")
            
        except Exception as e:
            print(f"[{q_id}] Error en Qdrant: {e}")
            
    end_time = time.time()
    
    print("\n==================================================")
    print(" 📈 RESULTADOS DEL BENCHMARK")
    print("==================================================")
    print(f"Total Preguntas Evaluadas : {total}")
    print(f"Preguntas con Hit (Top 3) : {hits}")
    hit_rate = (hits / total) * 100 if total > 0 else 0
    print(f"Hit Rate (Precisión RAG)  : {hit_rate:.1f}%")
    print(f"Tiempo total              : {end_time - start_time:.2f} segundos")
    print("==================================================")

if __name__ == "__main__":
    main()
