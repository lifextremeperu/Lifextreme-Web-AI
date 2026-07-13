import sys
import json
from collections import Counter
from qdrant_client import QdrantClient

sys.stdout.reconfigure(encoding='utf-8')

QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION = "Lifextreme_Knowledge"

def main():
    try:
        qclient = QdrantClient(url=QDRANT_URL)
        if not qclient.collection_exists(COLLECTION):
            print("La colección no existe.")
            return

        info = qclient.get_collection(COLLECTION)
        print(f"Total de Vectores Activos: {info.points_count}")
        
        # Scroll para contar
        categorias = Counter()
        fuentes = Counter()
        
        print("\nCalculando desglose (esto puede tomar unos segundos)...")
        offset = None
        while True:
            response, next_offset = qclient.scroll(
                collection_name=COLLECTION,
                limit=10000,
                with_payload=True,
                with_vectors=False,
                offset=offset
            )
            
            for point in response:
                payload = point.payload
                cat = payload.get("modulo_nombre", "Desconocido")
                source = payload.get("source", "Desconocido")
                
                categorias[cat] += 1
                # Solo contar las principales fuentes
                fuentes[source] += 1
                
            offset = next_offset
            if offset is None:
                break
                
        print("\n--- Desglose por Categoría ---")
        for cat, count in categorias.most_common(20):
            print(f"- {cat}: {count} vectores")
            
        print("\n--- Top 10 Fuentes más densas ---")
        for src, count in fuentes.most_common(10):
            print(f"- {src}: {count} vectores")
            
    except Exception as e:
        print(f"Error generando reporte: {e}")

if __name__ == "__main__":
    main()
