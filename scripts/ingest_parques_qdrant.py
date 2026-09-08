import json
import re
import uuid
import httpx
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
COLLECTION = "Lifextreme_Knowledge"

def extract_data_from_js(filepath):
    import subprocess
    import json
    
    # We will use Node.js to evaluate the file and extract the parks variable safely
    node_script = """
    const fs = require('fs');
    const content = fs.readFileSync('js/data.js', 'utf-8');
    // Mock window to avoid ReferenceError
    global.window = {};
    eval(content + "\\nfs.writeFileSync('temp_parks.json', JSON.stringify(parks));");
    """
    with open("temp_extract.cjs", "w") as f:
        f.write(node_script)
        
    subprocess.run(["node", "temp_extract.cjs"], check=True)
    
    with open("temp_parks.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    return data

def get_embedding(text: str) -> list[float]:
    response = httpx.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=60.0
    )
    response.raise_for_status()
    return response.json()["embedding"]

def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("===================================================================")
    print(" >>> INICIANDO INGESTA DE PARQUES DE AVENTURA EN QDRANT (LOCAL) ")
    print("===================================================================")
    
    js_path = "js/data.js"
    print(f"[+] Extrayendo datos de {js_path}...")
    parks = extract_data_from_js(js_path)
    print(f"[+] Encontrados {len(parks)} parques para vectorizar.")
    
    qdrant = QdrantClient(url=QDRANT_URL)
    
    points = []
    for idx, park in enumerate(parks):
        # Build the RAG text content
        region = park.get("region", "")
        name = park.get("name", "")
        category = park.get("category", "")
        desc = park.get("description", "")
        
        text_content = f"Destino de Aventura en {region}. Nombre: {name}. Categoría: {category}. Descripción: {desc}. ¡Ideal para reservas y turismo extremo!"
        
        print(f"    -> Vectorizando [{idx+1}/{len(parks)}]: {name} ({region})...")
        
        vector = get_embedding(text_content)
        
        # We need a unique deterministic UUID for Qdrant points to avoid duplicates
        point_id_seed = park.get("id", "") or name or str(idx)
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, point_id_seed))
        
        point = PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "region": region.lower(),
                "tier": 1,  # Alto valor comercial
                "modulo_nombre": category,
                "text_content": text_content
            }
        )
        points.append(point)
        
        # Batch insert every 20 points
        if len(points) >= 20:
            qdrant.upsert(collection_name=COLLECTION, points=points)
            points = []
            
    # Insert remaining points
    if points:
        qdrant.upsert(collection_name=COLLECTION, points=points)
        
    print("===================================================================")
    print(f" ✅ INGESTA RAG COMPLETADA: {len(parks)} parques subidos a Qdrant.")
    print("===================================================================")

if __name__ == "__main__":
    main()
