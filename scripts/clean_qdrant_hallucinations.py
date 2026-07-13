import httpx
import json

QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION = "Lifextreme_Knowledge"

def main():
    print(f"Limpiando alucinaciones en {COLLECTION}...")
    
    bad_keywords = [
        "no hay información", "no hay informacion", "no se menciona", 
        "no hay mención", "parque de aventura y", "deporte x", "vía z",
        "no se registra barranquismo", "no se encontró información"
    ]
    
    ids_to_delete = []
    
    # Obtener todos los vectores (scroll)
    offset = None
    while True:
        payload = {
            "limit": 1000,
            "with_payload": True,
            "with_vector": False
        }
        if offset:
            payload["offset"] = offset
            
        r = httpx.post(f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll", json=payload)
        if r.status_code != 200:
            print("Error conectando a Qdrant")
            break
            
        data = r.json().get("result", {})
        points = data.get("points", [])
        if not points:
            break
            
        for p in points:
            text = p.get("payload", {}).get("text_content", "").lower()
            if any(bad in text for bad in bad_keywords):
                ids_to_delete.append(p.get("id"))
                
        offset = data.get("next_page_offset")
        if not offset:
            break
            
    print(f"Se encontraron {len(ids_to_delete)} vectores alucinados o negativos.")
    
    if ids_to_delete:
        print("Eliminando vectores de Qdrant...")
        delete_payload = {
            "points": ids_to_delete
        }
        r_del = httpx.post(f"{QDRANT_URL}/collections/{COLLECTION}/points/delete", json=delete_payload)
        if r_del.status_code == 200:
            print("✅ Limpieza completada con éxito.")
        else:
            print(f"❌ Error al eliminar: {r_del.text}")
    else:
        print("✅ No hay nada que limpiar. Todo correcto.")

if __name__ == "__main__":
    main()
