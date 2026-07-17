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

OUTPUT_DIR = Path("data/blog/drafts_elite")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Top 10 de Élite (Valuación de Neuromarketing)
TEMAS = [
    {"id": "01", "perfil": "Turista Extranjero", "tema": "Evacuación Médica: ¿Quién paga el rescate en helicóptero si te accidentas en los Andes Peruanos?"},
    {"id": "02", "perfil": "Agencias Extranjeras B2B", "tema": "Responsabilidad Solidaria Legal: Por qué tu agencia extranjera puede quebrar si tu operador peruano choca un bus"},
    {"id": "03", "perfil": "Operadores y Guías Locales", "tema": "Guía SERNANP 2026: Las 10 infracciones más comunes que resultan en la expulsión de tu agencia"},
    {"id": "04", "perfil": "Turista Extranjero", "tema": "Estafas de Transporte: Lista negra de SUTRAN y cómo saber si tu bus turístico es ilegal"},
    {"id": "05", "perfil": "Turista General", "tema": "El Mito de la Hoja de Coca: Restricciones de aduanas internacionales al sacar productos de coca de Perú"},
    {"id": "06", "perfil": "Emprendedores Locales", "tema": "Turismo Emprende 2026: Los 5 errores burocráticos por los que el MINCETUR rechaza proyectos de S/ 80,000"},
    {"id": "07", "perfil": "Turista Nicho Místico", "tema": "Turismo Místico (Ayahuasca): Vacíos legales y por qué tu seguro de salud internacional no te cubrirá"},
    {"id": "08", "perfil": "Agencias Locales y Mayoristas", "tema": "La Nueva Ley del Porteador 2026: Cómo auditar a tu propia logística para evitar multas de S/ 50,000"},
    {"id": "09", "perfil": "Inversionistas", "tema": "Mapas de Riesgo Climático: Zonas rojas del Fenómeno del Niño donde los bancos te negarán préstamos para Eco-Lodges"},
    {"id": "10", "perfil": "Operadores y Turistas", "tema": "Huelgas en Perú: Mapa de rutas alternativas aéreas y ferroviarias cuando bloquean carreteras"}
]

HTML_CHATBOT = """
<div class="my-8 text-center">
    <a href="index.html#chat" class="inline-flex items-center justify-center gap-2 bg-slate-900 text-white font-bold py-4 px-8 rounded-xl hover:bg-slate-800 transition-all hover:scale-105 shadow-xl">
        <i class="ri-robot-2-fill text-2xl text-accent"></i> ¿Duda Legal Urgente? Consulta a MAX ahora
    </a>
</div>
"""

HTML_RESERVA = """
<div class="my-8 text-center bg-gray-50 p-6 rounded-2xl border border-gray-200">
    <h4 class="text-lg font-black text-slate-900 mb-4">No arriesgues tu operación logística</h4>
    <a href="index.html#booking" class="inline-flex items-center justify-center gap-2 bg-primary text-white font-bold py-4 px-8 rounded-xl hover:bg-indigo-700 transition-all hover:-translate-y-1 shadow-lg w-full md:w-auto">
        <i class="ri-shield-check-fill text-xl"></i> Reservar Expedición Certificada
    </a>
</div>
"""

HTML_LEAD_MAGNET = """
<div class="my-10 bg-gradient-to-r from-accent to-yellow-400 p-8 rounded-2xl shadow-xl text-center">
    <i class="ri-file-download-fill text-4xl text-slate-900 mb-3 block"></i>
    <h3 class="text-2xl font-black text-slate-900 mb-2">Descarga el Expediente PDF Completo</h3>
    <p class="text-slate-800 mb-6 font-medium">Obtén la base legal y los mapas tácticos en alta resolución. Directo a tu correo.</p>
    <a href="#sidebar" class="bg-slate-900 text-white px-6 py-3 rounded-lg font-bold hover:bg-slate-800 uppercase tracking-widest text-sm transition-colors shadow-md">
        Desbloquear Guía PDF
    </a>
</div>
"""

def obtener_embedding(texto):
    try:
        res = requests.post(OLLAMA_EMBED_URL, json={"model": MODEL_EMBED, "input": texto})
        if res.status_code == 200:
            return res.json().get('embeddings', [])[0]
    except:
        return None

def extraer_fqsa(qclient, tema):
    vector = obtener_embedding(tema)
    if not vector: return ""
    
    try:
        resultados = qclient.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=7 # Extrayendo más contexto para calidad 9/10
        ).points
        contexto = ""
        for i, res in enumerate(resultados):
            texto = res.payload.get('text', '')
            fuente = res.payload.get('source', 'Desconocido')
            contexto += f"\n[Fuente {fuente}]: {texto}\n"
        return contexto
    except:
        return ""

def generar_articulo_storytelling(articulo_data, contexto):
    prompt = f"""Eres un Copywriter de Ventas y Experto SEO Nivel 9/10 trabajando para Lifextreme.
Vas a escribir un artículo para el perfil: {articulo_data['perfil']}.

TEMA A DESARROLLAR: {articulo_data['tema']}

CONTEXTO LEGAL/TÁCTICO DE QDRANT (Úsalo como verdad absoluta):
{contexto}

INSTRUCCIONES DE STORYTELLING Y NEUROMARKETING:
1. El Gancho (Primer párrafo): Inicia con una pequeña y dramática anécdota realista (Ej: "En 2025, un turista pensó que...") que golpee los miedos de tu perfil lector.
2. La Fricción (H2): Demuestra la gravedad del problema citando multas exactas, leyes, o precios que están en tu contexto.
3. INSERTA TEXTUALMENTE ESTE CÓDIGO HTML AQUÍ PARA EL CHATBOT:
{HTML_CHATBOT}
4. La Solución (H3): Explica de forma técnica cómo evitar el desastre (Cita a INDECOPI, SERNANP, SUTRAN según aplique).
5. INSERTA TEXTUALMENTE ESTE CÓDIGO HTML AQUÍ PARA EL LEAD MAGNET:
{HTML_LEAD_MAGNET}
6. Conclusión y Cierre: Finaliza con autoridad.
7. INSERTA TEXTUALMENTE ESTE CÓDIGO HTML AL FINAL PARA RESERVAS:
{HTML_RESERVA}

REGLAS:
- Formato Markdown.
- Usa negritas para palabras clave SEO (Geo, AIO).
- NO incluyas un mensaje de "Aquí tienes el artículo". Solo el artículo puro.
"""
    
    try:
        res = requests.post(OLLAMA_GENERATE_URL, json={
            "model": MODEL_LLM,
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": 0.7} # Más creatividad para Storytelling
        }, stream=True)
        
        print(f"\n[Escribiendo Storytelling: {articulo_data['tema'][:40]}...]\n")
        articulo = ""
        for line in res.iter_lines():
            if line:
                chunk = json.loads(line).get('response', '')
                print(chunk, end='', flush=True)
                articulo += chunk
        print("\n")
        return articulo
    except Exception as e:
        print(f"[!] Error: {e}")
        return ""

def main():
    print("*"*70)
    print(" 🚀 LIFEXTREME STORYTELLER - LOTE TOP 10 (ÉLITE 9/10) 🚀")
    print("*"*70)
    
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
    except:
        print("[!] Conecta Qdrant en el puerto 6333.")
        return

    for i, item in enumerate(TEMAS):
        print(f"\n[{i+1}/10] Creando: {item['tema']}")
        
        contexto_real = extraer_fqsa(qclient, item['tema'])
        articulo_md = generar_articulo_storytelling(item, contexto_real)
        
        # Limpiar
        if articulo_md.startswith("```markdown"): articulo_md = articulo_md[11:]
        if articulo_md.startswith("```"): articulo_md = articulo_md[3:]
        if articulo_md.endswith("```"): articulo_md = articulo_md[:-3]
        
        filename = f"{item['id']}_Elite_{item['perfil'].replace(' ', '_')}.md"
        ruta_salida = OUTPUT_DIR / filename
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(articulo_md.strip())
            
        print(f"✅ Bóveda de Élite guardado: {filename}")
        
        if i < 9:
            print("[⏱️] Enfriamiento neuronal de 15 segundos...\n")
            time.sleep(15)

    print("\n✅ BÓVEDA DE ÉLITE TOP 10 COMPLETADA.")

if __name__ == "__main__":
    main()
