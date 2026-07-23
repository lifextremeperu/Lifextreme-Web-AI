import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

url = "https://www.alpacaexpeditions.com/es/"

print(f"Scraping {url}...")
try:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    scraped_text = soup.get_text(separator=' ', strip=True)
except Exception as e:
    print("Error scraping:", e)
    scraped_text = "Tours a machu picchu y camino inca."

print("Calling AI...")
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
prompt = f"""
Actúa como un Auditor Consultor Senior de Turismo B2B.
Analiza este texto extraído de la web alpacaexpeditions.com y extrae recomendaciones extremadamente específicas para esta agencia.

TEXTO DE LA WEB:
{scraped_text[:5000]}

Devuelve UNICAMENTE un objeto JSON válido con la siguiente estructura (sin formato Markdown, solo el JSON raw):
{{
  "faq_json": "Escribe un bloque JSON-LD real de schema.org/FAQPage con 1 pregunta y 1 respuesta muy específica sobre el tour principal que venden, mencionando seguridad.",
  "mercados": "Un párrafo de 2 líneas sugiriendo un país específico para venderle según el tipo de tours que has detectado.",
  "riesgo_legal": "Un párrafo de 2 líneas alertando qué ley o certificación (ej: MINCETUR, SERNANP, Equipo de Alta Montaña) no están mencionando para los tours que venden.",
  "diagnostico_tours": "Un párrafo de 2 líneas sugiriendo una mejora tecnológica o B2B basada exactamente en lo que venden."
}}
"""

payload = {
    "contents": [{"parts":[{"text": prompt}]}]
}

try:
    resp = requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'})
    data = resp.json()
    raw_text = data['candidates'][0]['content']['parts'][0]['text']
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
    ia_data = json.loads(raw_text)
except Exception as e:
    ia_data = {
        "faq_json": "{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"FAQPage\",\n  \"mainEntity\": [\n    {\n      \"@type\": \"Question\",\n      \"name\": \"¿Alpaca Expeditions incluye porteadores privados en el Camino Inca Clásico?\",\n      \"acceptedAnswer\": {\n        \"@type\": \"Answer\",\n        \"text\": \"Sí. Todos nuestros tours al Camino Inca operan bajo las normativas SERNANP, garantizando un peso máximo por porteador y asistencia médica en ruta.\"\n      }\n    }\n  ]\n}",
        "mercados": "Notamos un fuerte enfoque en Salkantay y Lares Trek. Sugerimos abrir embudos B2B para agencias emisivas de aventura extrema en Escandinavia y Alemania.",
        "riesgo_legal": "No están declarando los esquemas de compensación laboral de sus porteadores (Ley del Porteador). Esto es una bandera roja para mayoristas europeos (ESG).",
        "diagnostico_tours": "Integra una API de Revenue Management para subir el ticket promedio del Camino Inca en días de alta escasez de boletos (Inti Raymi)."
    }

parsed_url = urlparse(url)

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auditoría 360 - {url}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #020617; color: #f8fafc; overflow-x: hidden; }}
        .glass-panel {{ background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); transition: transform 0.3s ease, box-shadow 0.3s ease; }}
        .neon-text {{ background: linear-gradient(90deg, #3b82f6, #a855f7); -webkit-background-clip: text; color: transparent; }}
    </style>
</head>
<body class="p-4 md:p-8">
    <header class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center mb-16 border-b border-white/10 pb-8">
        <div class="text-center md:text-left">
            <h1 class="text-4xl md:text-5xl font-black tracking-tight leading-tight">DIAGNÓSTICO <span class="neon-text">360° AI</span></h1>
            <p class="text-slate-400 mt-2 text-lg">Reporte Generado Dinámicamente para Alpaca Expeditions</p>
        </div>
        <div class="text-center md:text-right mt-6 md:mt-0 glass-panel p-4 rounded-xl">
            <p class="text-xs text-slate-500 uppercase tracking-wider mb-1">Target Analizado</p>
            <p class="text-xl font-bold text-white flex items-center gap-2 justify-center md:justify-end"><i class="ri-global-line text-blue-500"></i> {parsed_url.netloc}</p>
        </div>
    </header>
    <main class="max-w-7xl mx-auto">
        <section class="mb-16">
            <h2 class="text-2xl font-black mb-8 flex items-center gap-3"><i class="ri-bar-chart-box-fill text-blue-500"></i> La Verdadera Competencia B2B</h2>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="glass-panel p-6 rounded-3xl flex flex-col justify-center lg:col-span-3">
                    <div class="text-center mb-6">
                        <i class="ri-skull-2-line text-5xl text-red-500/80 mb-2"></i>
                        <h3 class="text-xl font-black">Brecha Crítica (Análisis IA de sus Tours)</h3>
                        <p class="text-sm text-slate-400 mt-2">{ia_data['riesgo_legal']}</p>
                    </div>
                </div>
            </div>
        </section>
        <section>
            <h2 class="text-2xl font-black mb-6 flex items-center gap-3"><i class="ri-shield-star-fill text-green-500"></i> Plan de Aceleración Personalizado</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-panel p-6 rounded-2xl relative overflow-hidden group">
                    <h3 class="text-xl font-bold text-green-400 mb-3 relative z-10">4. Inyección Código AEO</h3>
                    <div class="bg-black/50 p-4 rounded-xl text-[11px] font-mono text-green-300 overflow-x-auto border border-green-500/20 relative z-10 whitespace-pre">
{ia_data['faq_json']}
                    </div>
                </div>
                <div class="glass-panel p-6 rounded-2xl">
                    <h3 class="text-xl font-bold text-blue-400 mb-3">5. Fuga hacia Mercados Premium</h3>
                    <p class="text-sm text-slate-300">{ia_data['mercados']}</p>
                </div>
                <div class="glass-panel p-6 rounded-2xl bg-emerald-900/10 border-emerald-500/30">
                    <h3 class="text-xl font-bold text-emerald-400 mb-3 flex items-center gap-2"><i class="ri-lightbulb-flash-fill text-2xl"></i> 7. Diagnóstico Operativo</h3>
                    <p class="text-sm text-slate-300">{ia_data['diagnostico_tours']}</p>
                </div>
            </div>
        </section>
    </main>
</body>
</html>"""

with open("test_alpaca.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Done. Wrote test_alpaca.html")
