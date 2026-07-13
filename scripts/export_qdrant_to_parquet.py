import os
import pandas as pd
from qdrant_client import QdrantClient

def export_to_parquet():
    print("===================================================================")
    print(" INICIANDO EXTRACCION DE VECTORES PARA PHOENIX (3D) ")
    print("===================================================================")
    
    try:
        client = QdrantClient(url="http://127.0.0.1:6333")
        collection_name = "Lifextreme_Knowledge"
        
        print("[*] Conectando a Qdrant Local...")
        
        # Scrollear todos los vectores con paginación para evitar timeouts
        records = []
        next_page = None
        while True:
            batch, next_page = client.scroll(
                collection_name=collection_name,
                limit=1000,
                offset=next_page,
                with_payload=True,
                with_vectors=True
            )
            records.extend(batch)
            print(f"[*] Descargando lote... Total acumulado: {len(records)}")
            if next_page is None:
                break
        
        if not records:
            print("[-] No se encontraron vectores en la base de datos.")
            return

        print(f"[*] Se encontraron {len(records)} vectores. Procesando...")
        
        data = []
        for r in records:
            # Extraer vector y payload crítico para el mapeo 3D
            data.append({
                "id": str(r.id),
                "text": r.payload.get("text_content", "Sin texto"),
                "tier": r.payload.get("tier", 3),
                "region": r.payload.get("region", "global"),
                "source": r.payload.get("source", "desconocido"),
                "vector": r.vector
            })
            
        # Convertir a DataFrame de Pandas
        df = pd.DataFrame(data)
        
        # Guardar como archivo Parquet (formato ultra comprimido y óptimo para IA)
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "qdrant_export.parquet")
        
        df.to_parquet(output_file)
        
        print("===================================================================")
        print(f" EXTRACCION COMPLETADA EXITOSAMENTE.")
        print(f" Total de neuronas exportadas: {len(df)}")
        print(f" Archivo guardado en: {output_file}")
        print(" Siguiente paso: Sube este archivo a Google Drive para usar en Colab.")
        print("===================================================================")
        
    except Exception as e:
        print(f"[-] Error crítico durante la exportación: {e}")

if __name__ == "__main__":
    export_to_parquet()
