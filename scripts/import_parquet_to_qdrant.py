import os
import sys
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

sys.stdout.reconfigure(encoding='utf-8')

# Configuración
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
PARQUET_PATH = "data/qdrant_export.parquet"
BATCH_SIZE = 1000

def main():
    print("==================================================")
    print("💾 INICIANDO RESTAURACIÓN MASIVA DESDE BACKUP PARQUET")
    print("==================================================")
    
    if not os.path.exists(PARQUET_PATH):
        print(f"[ERROR] No se encontró el archivo {PARQUET_PATH}")
        sys.exit(1)
        
    print(f"[*] Conectando a Qdrant en {QDRANT_URL}...")
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=60)
    except Exception as e:
        print(f"[ERROR] Falló conexión a Qdrant: {e}")
        sys.exit(1)
        
    print(f"[*] Cargando archivo Parquet de {os.path.getsize(PARQUET_PATH)/1024/1024:.2f} MB a la memoria RAM...")
    try:
        df = pd.read_parquet(PARQUET_PATH)
    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo Parquet: {e}")
        sys.exit(1)
        
    total_vectors = len(df)
    print(f"[+] Backup cargado con éxito. Se detectaron {total_vectors} vectores para restaurar.")
    print("[*] Iniciando inyección en lotes (batch)...")
    
    # Rellenar NaNs para evitar errores de Pydantic
    df.fillna('', inplace=True)
    
    points_to_upsert = []
    total_injected = 0
    
    for index, row in df.iterrows():
        try:
            # Crear payload dinámico excluyendo id y vector
            payload = {
                "text": str(row.get("text", "")),
                "tier": str(row.get("tier", "")),
                "region": str(row.get("region", "")),
                "source": str(row.get("source", ""))
            }
            
            point = PointStruct(
                id=str(row['id']),
                vector=list(row['vector']),
                payload=payload
            )
            points_to_upsert.append(point)
            
            if len(points_to_upsert) >= BATCH_SIZE:
                qclient.upsert(collection_name=COLLECTION_NAME, points=points_to_upsert)
                total_injected += len(points_to_upsert)
                points_to_upsert = []
                # Barra de progreso simple
                porcentaje = (total_injected / total_vectors) * 100
                print(f"    -> Progreso: {total_injected}/{total_vectors} vectores inyectados ({porcentaje:.2f}%)")
                
        except Exception as e:
            print(f"    [!] Error al procesar fila {index}: {e}")
            
    # Subir el remanente
    if points_to_upsert:
        qclient.upsert(collection_name=COLLECTION_NAME, points=points_to_upsert)
        total_injected += len(points_to_upsert)
        porcentaje = (total_injected / total_vectors) * 100
        print(f"    -> Progreso final: {total_injected}/{total_vectors} vectores inyectados ({porcentaje:.2f}%)")
        
    print("==================================================")
    print("✅ RESTAURACIÓN COMPLETADA CON ÉXITO")
    print("==================================================")
    
    # Consulta final para validar
    try:
        total_actual = qclient.get_collection(COLLECTION_NAME).points_count
        print(f"🧠 CEREBRO ONLINE: Total de vectores activos en Docker: {total_actual}")
    except Exception as e:
        print(f"⚠️ No se pudo obtener el conteo final: {e}")
        
    print("\nEl proceso ha finalizado. Puedes cerrar esta ventana.")

if __name__ == "__main__":
    main()
