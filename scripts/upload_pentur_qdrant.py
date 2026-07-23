import sys
import os
import glob
import json
import uuid
import httpx
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_URL = "http://localhost:11434/api/embed"
COLLECTION = "Lifextreme_Knowledge"
TENANT_ID = "lifextreme"

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
        
    print("==================================================")
    print("🚀 INICIANDO SUBIDA DE INSIGHTS PENTUR A QDRANT")
    print("==================================================")
    
    qclient = QdrantClient(url=QDRANT_URL)
    
    # Ensure collection exists
    if not qclient.collection_exists(COLLECTION):
        print(f"[*] Creando colección {COLLECTION}...")
        qclient.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

    insights_files = glob.glob('data/knowledge/peru/*/strategic_insights.json')
    
    if not insights_files:
        print("[-] No se encontraron archivos strategic_insights.json.")
        return

    for fpath in insights_files:
        region = os.path.basename(os.path.dirname(fpath))
        with open(fpath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"[-] Error parseando JSON en {region}. Saltando.")
                continue
        
        # Build text to embed
        resumen = data.get('resumen_ejecutivo', '')
        oportunidades = ', '.join(data.get('oportunidades_negocio', []))
        riesgos = ', '.join(data.get('riesgos_inversion', []))
        
        text_content = f"Región: {data.get('region', region)}\nResumen Ejecutivo: {resumen}\nOportunidades de Negocio B2B: {oportunidades}\nRiesgos de Inversión: {riesgos}"
        
        print(f"[*] Obteniendo embedding para la región: {region.capitalize()}...")
        try:
            res = httpx.post(OLLAMA_URL, json={"model": "nomic-embed-text", "input": [text_content]}, timeout=120.0)
            res.raise_for_status()
            emb = res.json().get('embeddings', [])[0]
        except Exception as e:
            print(f"[-] Error conectando a Ollama para {region}: {e}")
            continue
        
        vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, text_content))
        
        payload = {
            "tenant_id": TENANT_ID,
            "vector_id": vector_uuid,
            "tier": 2, # Alto valor B2B
            "region": region,
            "modulo_nombre": "PENTUR_INSIGHTS",
            "source": f"PENTUR_{region.upper()}",
            "text_content": text_content,
            "json_data": json.dumps(data)
        }
        
        try:
            qclient.upsert(
                collection_name=COLLECTION,
                points=[PointStruct(id=vector_uuid, vector=emb, payload=payload)]
            )
            print(f"    [+] Insight de {region.capitalize()} inyectado en Qdrant exitosamente.")
        except Exception as e:
            print(f"    [-] Error insertando en Qdrant para {region}: {e}")

    print("==================================================")
    print("✅ SUBIDA PENTUR B2B A QDRANT COMPLETADA.")
    print("==================================================")

if __name__ == '__main__':
    main()
