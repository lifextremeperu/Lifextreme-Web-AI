import httpx
import json
from qdrant_client import QdrantClient

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_URL = "http://localhost:11434/api/embed"
COLLECTION = "Lifextreme_Knowledge"

def get_embedding(text):
    try:
        response = httpx.post(OLLAMA_URL, json={
            "model": "nomic-embed-text",
            "input": [text]
        }, timeout=30.0)
        return response.json().get('embeddings', [])[0]
    except Exception as e:
        print(f"Error Ollama: {e}")
        return None

def search_knowledge(qclient, query, top_k=10):
    emb = get_embedding(query)
    if not emb: return []
    
    try:
        r = httpx.post(f"{QDRANT_URL}/collections/{COLLECTION}/points/search", json={
            "vector": emb,
            "limit": top_k,
            "with_payload": True
        })
        if r.status_code == 200:
            return r.json().get("result", [])
    except Exception as e:
        print(f"Error Qdrant HTTP: {e}")
    return []

def main():
    qclient = QdrantClient(url=QDRANT_URL)
    
    perfiles = [
        {
            "nombre": "Perfil 1: Inversionista Extranjero (Sostenibilidad y Botánica)",
            "consulta": "Quiero invertir en un proyecto de Glamping o Ecoaldea de lujo en la sierra de Perú. Necesito saber qué plantas medicinales (botánica) puedo cultivar para ofrecer experiencias de bienestar, cómo integrar sistemas de permacultura, y qué marco legal de inversión privada me respalda."
        },
        {
            "nombre": "Perfil 2: Agencia de Viajes B2B (Operaciones y Aventura)",
            "consulta": "Soy un operador turístico que quiere vender paquetes de ciclismo de montaña y aventura extrema. Necesito información detallada sobre la Ciclovía Machupicchu o Ruta del Maíz, costos operativos, y normativas de MINCETUR o SUTRAN que deba cumplir para transporte y operación segura."
        }
    ]
    
    report_lines = []
    report_lines.append("# 🧪 TEST DE ESTRÉS: Trazabilidad Multimódulo de Lifextreme AI\n")
    
    for perfil in perfiles:
        report_lines.append(f"## 👤 {perfil['nombre']}")
        report_lines.append(f"**Consulta del Usuario:** *\"{perfil['consulta']}\"*\n")
        
        print(f"Buscando para: {perfil['nombre']}...")
        resultados = search_knowledge(qclient, perfil['consulta'])
        
        if not resultados:
            report_lines.append("> ❌ Sin resultados (Ollama o Qdrant apagados).\n")
            continue
            
        report_lines.append("### 🧠 Trazabilidad de Módulos (Top Resultados Encontrados):")
        report_lines.append("| Similitud | Módulo (Tier) | Archivo Fuente | Extracto del Conocimiento |")
        report_lines.append("|---|---|---|---|")
        
        for res in resultados:
            score = round(res.get("score", 0) * 100, 2)
            payload = res.get("payload", {})
            modulo = payload.get("modulo_nombre", "General")
            tier = payload.get("tier", "N/A")
            source = payload.get("source", "Desconocido")
            text = payload.get("text_content", "")[:150].replace("\n", " ") + "..."
            
            report_lines.append(f"| **{score}%** | `{modulo}` (Tier {tier}) | {source} | {text} |")
            
        report_lines.append("\n---\n")
        
    with open(r"C:\Users\ASUS\.gemini\antigravity\brain\53a890c3-72f0-4498-92dd-9eec52613903\artifacts\test_rag_profiles.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print("\n✅ Test completado. Reporte generado en artifacts/test_rag_profiles.md")

if __name__ == "__main__":
    main()
