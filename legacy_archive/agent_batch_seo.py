import os
import sys
import json
import time
import requests
from qdrant_client import QdrantClient
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Constantes
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
MODEL_EMBED = "nomic-embed-text"
MODEL_LLM = "llama3:8b" 

# Directorio de Borradores
OUTPUT_DIR = Path("data/blog/drafts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 12 Temas del Piloto
TEMAS = [
    # Perfil: Turistas (B2C)
    {"id": "01_turistas", "perfil": "Turistas", "tema": "Prevención del Soroche y Clima Extremo en Cusco 2026", "region": "Cusco"},
    {"id": "02_turistas", "perfil": "Turistas", "tema": "Guía de Turismo Comunitario: Cómo visitar comunidades legalmente y con respeto", "region": "Nacional"},
    {"id": "03_turistas", "perfil": "Turistas", "tema": "Huelgas y Bloqueos: Rutas alternas y derechos del turista en Perú", "region": "Sur del Perú"},
    {"id": "04_turistas", "perfil": "Turistas", "tema": "Seguridad en Huaraz: Todo lo que debes exigirle a tu agencia de trekking", "region": "Áncash"},
    
    # Perfil: Operadores/Guías (B2B Logístico)
    {"id": "05_operadores", "perfil": "Operadores Turísticos", "tema": "Protocolos Exactos de Evacuación Médica del SERNANP", "region": "Nacional"},
    {"id": "06_operadores", "perfil": "Operadores Turísticos", "tema": "Certificaciones de MINCETUR y Equipo Obligatorio de Aventura", "region": "Nacional"},
    {"id": "07_operadores", "perfil": "Operadores Turísticos", "tema": "La Ley del Porteador 2026: Pesos máximos y prevención de multas", "region": "Cusco"},
    {"id": "08_operadores", "perfil": "Operadores Turísticos", "tema": "Derecho de Paso: Cómo resolver conflictos con Comunidades Campesinas", "region": "Nacional"},

    # Perfil: Agencias/Inversionistas (B2B Estratégico)
    {"id": "09_agencias", "perfil": "Dueños de Agencias", "tema": "Cómo redactar Proyectos para ganar los fondos de Turismo Emprende", "region": "Nacional"},
    {"id": "10_agencias", "perfil": "Dueños de Agencias", "tema": "Responsabilidad Civil: Cómo blindar tu agencia ante accidentes mortales", "region": "Nacional"},
    {"id": "11_agencias", "perfil": "Dueños de Agencias", "tema": "Seguros Turísticos Internacionales: Guía de homologación para agencias peruanas", "region": "Nacional"},
    {"id": "12_agencias", "perfil": "Dueños de Agencias", "tema": "Impacto Financiero del Fenómeno del Niño en la Ruta Sur", "region": "Sur del Perú"}
]

def obtener_embedding(texto):
    try:
        res = requests.post(OLLAMA_EMBED_URL, json={"model": MODEL_EMBED, "input": texto})
        if res.status_code == 200:
            return res.json().get('embeddings', [])[0]
    except Exception as e:
        print(f"[!] Error generando embedding: {e}")
    return None

def extraer_fqsa(qclient, region, tema):
    query = f"Reglamentos, leyes, datos financieros y tácticos sobre: {tema} en {region}."
    vector = obtener_embedding(query)
    if not vector: return ""
    
    try:
        resultados = qclient.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=5
        ).points
        contexto = ""
        for i, res in enumerate(resultados):
            texto = res.payload.get('text', '')
            fuente = res.payload.get('source', 'Desconocido')
            contexto += f"\n[Fragmento {i+1} | Fuente: {fuente}]:\n{texto}\n"
        return contexto
    except Exception as e:
        print(f"[!] Error en Qdrant: {e}")
        return ""

def generar_articulo_extenso(articulo_data, contexto):
    prompt = f"""Eres el Escritor Jefe de Lifextreme AI. Tu tarea es escribir un artículo SEO EXTENSO (long-form) y de altísimo valor para el siguiente perfil: {articulo_data['perfil']}.

TEMA: {articulo_data['tema']}
REGIÓN APLICABLE: {articulo_data['region']}

BASE LEGAL/TÉCNICA DE QDRANT (ÚSALA OBLIGATORIAMENTE PARA DAR DATOS DUROS):
{contexto}

ESTRUCTURA ESTRICTA DEL ARTÍCULO (Usa formato Markdown):
1. H1: Título muy atractivo y SEO (Añade '2026').
2. Párrafo Introductorio: Atrapa al lector ({articulo_data['perfil']}) tocando su mayor dolor o miedo respecto al tema.
3. H2 y H3: Desarrolla el tema en profundidad (al menos 4 subsecciones). Cita leyes, multas, o tácticas reales usando el contexto.

INYECCIÓN DE MÓDULOS DE CONVERSIÓN (DEBES INCLUIR ESTOS TEXTOS EXACTAMENTE DONDE SE TE PIDE):
- Al final de la introducción, INSERTA EXACTAMENTE ESTO:
> **[BOTÓN_CHATBOT_MAX]** *"¿Tienes una duda urgente sobre este tema? Chatea ahora mismo con MAX, nuestro Asistente Legal impulsado por IA, y obtén respuesta en 5 segundos."*

- Al final del artículo, antes de la conclusión, INSERTA EXACTAMENTE ESTO:
> **[LEAD_MAGNET_PDF]** *"📚 [DESCARGA GRATIS] Obtén el Expediente Técnico en PDF sobre este tema. Déjanos tu correo aquí para desbloquearlo al instante."*

- En la conclusión final, INSERTA EXACTAMENTE ESTO:
> **[BOTÓN_RESERVA_TOUR]** *"Asegura tu logística. Reserva tu próxima expedición con operadores certificados por Lifextreme."*

4. REFERENCIAS Y FUENTES (H2): Lista las fuentes oficiales que usaste del contexto proporcionado.

NO INCLUYAS NINGÚN MENSAJE COMO "AQUÍ TIENES EL ARTÍCULO", SOLO DEVUELVE EL MARKDOWN PURO.
"""
    
    try:
        res = requests.post(OLLAMA_GENERATE_URL, json={
            "model": MODEL_LLM,
            "prompt": prompt,
            "stream": True
        }, stream=True)
        
        print("\n[Escritura IA en progreso...]")
        articulo = ""
        for line in res.iter_lines():
            if line:
                chunk = json.loads(line).get('response', '')
                print(chunk, end='', flush=True)
                articulo += chunk
        print("\n")
        return articulo
    except Exception as e:
        print(f"[!] Error en Ollama: {e}")
        return ""

def main():
    print("="*70)
    print(" 🏭 LIFEXTREME CONTENT FACTORY - PILOTO DE 12 ARTÍCULOS 🏭")
    print("="*70)
    print(f"Directorio de Borradores: {OUTPUT_DIR.absolute()}")
    print("Generando contenido extenso para Turistas, Operadores y Agencias...")
    print("="*70)
    
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
    except:
        print("[!] Asegúrate de que Qdrant esté corriendo en el puerto 6333.")
        return

    for i, item in enumerate(TEMAS):
        print(f"\n[{i+1}/12] Analizando: {item['tema']}")
        print(f"-> Perfil Objetivo: {item['perfil']}")
        
        contexto_real = extraer_fqsa(qclient, item['region'], item['tema'])
        
        if not contexto_real.strip():
            print("   [!] No se extrajeron vectores suficientes, pero se forzará la redacción.")
            
        articulo_md = generar_articulo_extenso(item, contexto_real)
        
        # Limpiar backticks si el modelo los añade
        if articulo_md.startswith("```markdown"):
            articulo_md = articulo_md[11:]
        if articulo_md.startswith("```"):
            articulo_md = articulo_md[3:]
        if articulo_md.endswith("```"):
            articulo_md = articulo_md[:-3]
        
        # Guardar en la bóveda de borradores
        filename = f"articulo_{item['id']}.md"
        ruta_salida = OUTPUT_DIR / filename
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(articulo_md.strip())
            
        print(f"✅ Guardado en Borradores: {filename}")
        print("*"*50)
        
        # Pequeña pausa para no sobrecalentar la GPU/CPU local
        if i < 11:
            print("[⏱️] Enfriando sistema por 10 segundos antes del próximo artículo...\n")
            time.sleep(10)

    print("\n==================================================")
    print("🎉 BATCH COMPLETADO: 12 Artículos Premium Generados.")
    print(f"📁 Revisa la carpeta: {OUTPUT_DIR.absolute()}")
    print("==================================================")

if __name__ == "__main__":
    main()
