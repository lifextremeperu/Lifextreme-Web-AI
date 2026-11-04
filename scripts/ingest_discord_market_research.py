"""
Script para ingerir el Estudio de Mercado de Discord y Perfiles de Clientes en Qdrant.
Crea la colección 'Lifextreme_Market_Research' o la inserta en 'Lifextreme_Knowledge'.
Usa Ollama (nomic-embed-text) o llamadas HTTP estándar hacia Qdrant.
"""
import os
import json
import uuid
import urllib.request
import urllib.error

QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
OLLAMA_URL = "http://localhost:11434/api/embed"
COLLECTION = "Lifextreme_Market_Research"

def get_embedding(text: str):
    """Obtener embedding de 768 dimensiones vía Ollama nomic-embed-text."""
    data = json.dumps({"model": "nomic-embed-text", "input": text}).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode())
            return res.get("embeddings", [[]])[0]
    except Exception as e:
        print(f"Error generando embedding: {e}")
        return None

def create_collection_if_needed(collection_name: str):
    url = f"{QDRANT_URL}/collections/{collection_name}"
    payload = json.dumps({
        "vectors": {
            "size": 768,
            "distance": "Cosine"
        }
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"Colección '{collection_name}' creada o ya existente.")
    except urllib.error.HTTPError as e:
        if e.code == 409 or e.code == 400:
            print(f"Colección '{collection_name}' ya estaba creada.")
        else:
            print(f"Código HTTP creación: {e.code}")
    except Exception as e:
        print(f"No se pudo conectar a Qdrant en {QDRANT_URL}: {e}")

def main():
    json_path = "data/knowledge/market_research/discord_marketing_strategy_peru.json"
    if not os.path.exists(json_path):
        print(f"No se encontró {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        doc = json.load(f)

    print("=== INGESTA DE INVESTIGACIÓN DE MERCADO LIFEXTREME ===")
    print("Documento cargado correctamente.")

    # Generar fragmentos semánticos (chunks)
    chunks = []
    
    # 1. Hallazgos clave y demografía Discord Perú
    disc_data = doc["key_findings"]["discord_market_in_peru"]
    chunks.append({
        "section": "Metricas y Demografia Discord Peru",
        "content": f"Métricas de Discord en el mercado peruano: {disc_data['monthly_traffic_peru_ips']}. "
                   f"Demografía objetivo: {disc_data['demographic_profile']}. "
                   f"Permanencia promedio de usuario: {disc_data['session_duration']}. "
                   f"Penetración regional en LATAM: {disc_data['regional_penetration_latam']}."
    })

    # 2. Diagnóstico de la informalidad y desconfianza en el turismo de aventura en Perú
    prob = doc["key_findings"]["problem_statement_peru_adventure"]
    chunks.append({
        "section": "Problema del Turismo de Aventura y Oportunidad de Formalizacion",
        "content": f"Diagnóstico sectorial de aventura en Perú: {prob['informality_rate']}. "
                   f"Nivel de desconfianza de los turistas: {prob['perceived_risk']}. "
                   f"Tasa de abandono de usuarios: {prob['churn_rate']}. "
                   f"Solución de Lifextreme: {prob['lifextreme_solution']}."
    })

    # 3. Perfiles de Clientes (Personas)
    for p in doc["key_findings"]["customer_personas"]:
        chunks.append({
            "section": f"Perfil de Cliente: {p['role_tier']}",
            "content": f"Customer Persona {p['role_tier']} en Lifextreme: {p['description']} "
                       f"Necesidades operativas: {p['needs']} "
                       f"Gancho de conversión comercial: {p['conversion_hook']}."
        })

    # 4. Embudo de Marketing y Conversión (TOFU, MOFU, BOFU)
    funnel = doc["key_findings"]["marketing_funnel_architecture"]
    chunks.append({
        "section": "Embudo de Marketing TOFU-MOFU-BOFU con Discord",
        "content": f"TOFU: Canales {', '.join(funnel['top_of_funnel_tofu']['channels'])}. Lead Magnet: {funnel['top_of_funnel_tofu']['lead_magnet']}. CTA: {funnel['top_of_funnel_tofu']['cta']}. "
                   f"MOFU: Actividades en Discord {funnel['middle_of_funnel_mofu']['activity']}. Objetivo: {funnel['middle_of_funnel_mofu']['objective']}. "
                   f"BOFU: Cierre de reservas {funnel['bottom_of_funnel_bofu']['activity']} mediante pasarelas locales peruanas y aprovisionamiento automático de roles."
    })

    print(f"Total chunks semánticos generados: {len(chunks)}")
    create_collection_if_needed(COLLECTION)

    # Intentar subir a Qdrant si está levantado
    points = []
    for c in chunks:
        emb = get_embedding(c["content"])
        if emb:
            points.append({
                "id": str(uuid.uuid4()),
                "vector": emb,
                "payload": {
                    "source": doc["source"],
                    "section": c["section"],
                    "content": c["content"],
                    "category": doc["category"],
                    "country": doc["country"]
                }
            })
    
    if points:
        upload_url = f"{QDRANT_URL}/collections/{COLLECTION}/points"
        upload_data = json.dumps({"points": points}).encode('utf-8')
        req = urllib.request.Request(upload_url, data=upload_data, headers={"Content-Type": "application/json"}, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"¡Éxito! Inyectados {len(points)} vectores en Qdrant ('{COLLECTION}').")
        except Exception as e:
            print(f"Aviso de subida directa: {e}. Los datos quedaron persistidos en el archivo JSON listo para el batch.")
    else:
        print("Embeddings no generados (verificar si Ollama o Qdrant están activos en este puerto).")

if __name__ == "__main__":
    main()
