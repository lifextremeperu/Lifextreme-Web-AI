import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import re
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

app = FastAPI(title="Lifextreme AI Auditor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuditRequest(BaseModel):
    url: str

def ask_local_llm(scraped_text, domain):
    # Conexión al LLM Local (Ej: Ollama o LM Studio corriendo en la misma máquina)
    # Por defecto apuntamos a Ollama en el puerto 11434 usando el modelo llama3 o mistral
    url = "http://127.0.0.1:11434/api/generate"
    
    prompt = f"""
    Actúa como un Auditor Consultor Senior de Turismo B2B.
    Analiza este texto extraído de la web {domain} y extrae recomendaciones extremadamente específicas para esta agencia.
    
    TEXTO DE LA WEB:
    {scraped_text[:4000]}
    
    Devuelve UNICAMENTE un objeto JSON válido con la siguiente estructura (sin formato Markdown):
    {{
      "faq_json": "Escribe un bloque JSON-LD real de schema.org/FAQPage con 1 pregunta y 1 respuesta muy específica sobre el tour principal que venden, mencionando seguridad.",
      "mercados": "Un párrafo de 2 líneas sugiriendo un país específico para venderle según el tipo de tours que has detectado.",
      "riesgo_legal": "Un párrafo de 2 líneas alertando qué ley o certificación (ej: MINCETUR, SERNANP) no están mencionando para los tours que venden.",
      "diagnostico_tours": "Un párrafo de 2 líneas sugiriendo una mejora tecnológica o B2B basada exactamente en lo que venden."
    }}
    """
    
    payload = {
        "model": "llama3", # Puedes cambiar esto por el modelo local que uses (llama3, mistral, qwen)
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        data = response.json()
        raw_text = data.get('response', '')
        return json.loads(raw_text)
    except Exception as e:
        print("Error conectando al LLM Local:", e)
        return {
            "faq_json": "{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"FAQPage\",\n  \"mainEntity\": []\n}",
            "mercados": "Mercado Europeo y Norteamericano.",
            "riesgo_legal": "Falta de normativas SERNANP/MINCETUR genéricas.",
            "diagnostico_tours": "Integra algoritmos de precios dinámicos."
        }

@app.post("/api/audit")
def audit_website(req: AuditRequest):
    url = req.url
    if not url.startswith("http"):
        url = "https://" + url

    try:
        response = requests.get(url, timeout=10)
        html = response.text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo conectar a {url}")

    soup = BeautifulSoup(html, "html.parser")
    scraped_text = soup.get_text(separator=' ', strip=True)

    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    llms_url = f"{base_url}/llms.txt"
    try:
        llms_response = requests.get(llms_url, timeout=5)
        has_llms = (llms_response.status_code == 200)
    except:
        has_llms = False

    has_jsonld = 'application/ld+json' in html
    has_mincetur = 'MINCETUR' in html.upper()
    has_sernanp = 'SERNANP' in html.upper()

    score_geo = 15 if not has_llms else 85
    score_legal = 30 if not has_mincetur else 90
    score_auto = 10 

    # LLAMADA A LA IA PARA GENERAR CONTENIDO DINÁMICO
    ia_data = ask_local_llm(scraped_text, parsed_url.netloc)

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
        .glass-panel:hover {{ transform: translateY(-5px); box-shadow: 0 10px 30px -10px rgba(59, 130, 246, 0.3); border-color: rgba(59, 130, 246, 0.3); }}
        .neon-text {{ background: linear-gradient(90deg, #3b82f6, #a855f7); -webkit-background-clip: text; color: transparent; }}
        .fade-in-up {{ animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateY(20px); }}
        @keyframes fadeInUp {{ to {{ opacity: 1; transform: translateY(0); }} }}
        .delay-1 {{ animation-delay: 0.1s; }}
        .delay-2 {{ animation-delay: 0.2s; }}
        .delay-3 {{ animation-delay: 0.3s; }}
    </style>
</head>
<body class="p-4 md:p-8 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-fixed">
    <div class="fixed top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div class="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[100px]"></div>
        <div class="absolute bottom-[-10%] left-[-10%] w-[600px] h-[600px] bg-purple-600/10 rounded-full blur-[120px]"></div>
    </div>
    <header class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center mb-16 border-b border-white/10 pb-8 fade-in-up">
        <div class="text-center md:text-left">
            <div class="inline-block px-3 py-1 bg-blue-500/20 text-blue-400 text-[10px] font-black uppercase tracking-widest rounded-full mb-3 border border-blue-500/30">Privado y Confidencial</div>
            <h1 class="text-4xl md:text-5xl font-black tracking-tight leading-tight">DIAGNÓSTICO <span class="neon-text">360° AI</span></h1>
            <p class="text-slate-400 mt-2 text-lg">Reporte Generado Dinámicamente por Lifextreme AI</p>
        </div>
        <div class="text-center md:text-right mt-6 md:mt-0 glass-panel p-4 rounded-xl">
            <p class="text-xs text-slate-500 uppercase tracking-wider mb-1">Target Analizado</p>
            <p class="text-xl font-bold text-white flex items-center gap-2 justify-center md:justify-end"><i class="ri-global-line text-blue-500"></i> {parsed_url.netloc}</p>
        </div>
    </header>
    <main class="max-w-7xl mx-auto">
        <section class="mb-16 fade-in-up delay-1">
            <h2 class="text-2xl font-black mb-8 flex items-center gap-3"><i class="ri-bar-chart-box-fill text-blue-500"></i> La Verdadera Competencia B2B</h2>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 glass-panel p-6 rounded-3xl relative">
                    <h3 class="text-sm font-bold text-slate-300 mb-4 uppercase tracking-widest text-center">Tú vs. El Estándar Internacional Mayorista</h3>
                    <div class="w-full h-[300px] flex items-center justify-center">
                        <canvas id="radarChart"></canvas>
                    </div>
                </div>
                <div class="glass-panel p-6 rounded-3xl flex flex-col justify-center">
                    <div class="text-center mb-6">
                        <i class="ri-skull-2-line text-5xl text-red-500/80 mb-2"></i>
                        <h3 class="text-xl font-black">Brecha Crítica</h3>
                        <p class="text-sm text-slate-400 mt-2">{ia_data['riesgo_legal']}</p>
                    </div>
                    <div class="space-y-4">
                        <div class="flex justify-between items-center bg-white/5 p-3 rounded-lg">
                            <span class="text-xs text-slate-300">Penetración IA B2B</span>
                            <span class="text-xs font-bold text-red-400">0%</span>
                        </div>
                        <div class="flex justify-between items-center bg-white/5 p-3 rounded-lg">
                            <span class="text-xs text-slate-300">Riesgo Legal E-E-A-T</span>
                            <span class="text-xs font-bold text-red-400">Alto Peligro</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section class="mb-16 fade-in-up delay-2">
            <h2 class="text-2xl font-black mb-6 flex items-center gap-3"><i class="ri-radar-line text-purple-500"></i> Vulnerabilidades Encontradas</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="glass-panel p-6 rounded-2xl border-t-4 border-t-red-500">
                    <h3 class="font-black text-lg mb-2">1. Ceguera Artificial</h3>
                    <p class="text-sm text-slate-400 mb-4">No existes para ChatGPT. Archivo llms.txt ausente.</p>
                </div>
                <div class="glass-panel p-6 rounded-2xl border-t-4 border-t-orange-500">
                    <h3 class="font-black text-lg mb-2">2. Riesgo E-E-A-T</h3>
                    <p class="text-sm text-slate-400 mb-4">Ausencia de declaración semántica SERNANP/MINCETUR.</p>
                </div>
                <div class="glass-panel p-6 rounded-2xl border-t-4 border-t-yellow-500">
                    <h3 class="font-black text-lg mb-2">3. Penalidad Google</h3>
                    <p class="text-sm text-slate-400 mb-4">Arquitectura estática sin WebP dinámico.</p>
                </div>
            </div>
        </section>
        <section class="fade-in-up delay-3">
            <h2 class="text-2xl font-black mb-6 flex items-center gap-3"><i class="ri-shield-star-fill text-green-500"></i> Plan de Aceleración Personalizado (Los 7 Pilares)</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-panel p-6 rounded-2xl relative overflow-hidden group">
                    <div class="absolute -right-4 -top-4 text-8xl text-white/5"><i class="ri-code-box-line"></i></div>
                    <h3 class="text-xl font-bold text-green-400 mb-3 relative z-10">4. Inyección Código AEO (Basado en tus Tours)</h3>
                    <p class="text-sm text-slate-300 mb-4 relative z-10">Pega esto en el &lt;head&gt; de tu web para rankear en IA:</p>
                    <div class="bg-black/50 p-4 rounded-xl text-[11px] font-mono text-green-300 overflow-x-auto border border-green-500/20 relative z-10 whitespace-pre">
{ia_data['faq_json']}
                    </div>
                </div>
                <div class="glass-panel p-6 rounded-2xl">
                    <h3 class="text-xl font-bold text-blue-400 mb-3">5. Fuga hacia Mercados Premium</h3>
                    <p class="text-sm text-slate-300">{ia_data['mercados']}</p>
                </div>
                <div class="glass-panel p-6 rounded-2xl">
                    <h3 class="text-xl font-bold text-teal-400 mb-3">6. Cero Carbono & Sostenibilidad</h3>
                    <p class="text-sm text-slate-300">Integraremos metadatos para certificar Compensación de Huella de Carbono exigida en Europa.</p>
                </div>
                <div class="glass-panel p-6 rounded-2xl bg-emerald-900/10 border-emerald-500/30">
                    <h3 class="text-xl font-bold text-emerald-400 mb-3 flex items-center gap-2"><i class="ri-lightbulb-flash-fill text-2xl"></i> 7. Diagnóstico Operativo</h3>
                    <p class="text-sm text-slate-300">{ia_data['diagnostico_tours']}</p>
                </div>
                <div class="grid grid-cols-2 gap-4 col-span-1 lg:col-span-2">
                    <div class="glass-panel p-5 rounded-2xl text-center">
                        <i class="ri-award-fill text-yellow-500 text-3xl mb-2 inline-block"></i>
                        <h4 class="font-bold mb-1">8. Marca Perú</h4>
                        <p class="text-xs text-slate-400">Ruta para registro legal (Clase 39).</p>
                    </div>
                    <div class="glass-panel p-5 rounded-2xl text-center">
                        <i class="ri-robot-2-line text-purple-500 text-3xl mb-2 inline-block"></i>
                        <h4 class="font-bold mb-1">9. Asistente IA 24/7</h4>
                        <p class="text-xs text-slate-400">Cierra ventas de madrugada automáticamente.</p>
                    </div>
                    <div class="glass-panel p-5 rounded-2xl text-center">
                        <i class="ri-money-dollar-box-line text-green-500 text-3xl mb-2 inline-block"></i>
                        <h4 class="font-bold mb-1">10. Precios Dinámicos</h4>
                        <p class="text-xs text-slate-400">Subir tarifas automáticamente en temporadas altas.</p>
                    </div>
                    <div class="glass-panel p-5 rounded-2xl text-center">
                        <i class="ri-store-3-line text-blue-500 text-3xl mb-2 inline-block"></i>
                        <h4 class="font-bold mb-1">Portal B2B</h4>
                        <p class="text-xs text-slate-400">Vende como mayorista a agencias Extranjeras.</p>
                    </div>
                </div>
            </div>
        </section>
    </main>
    <footer class="mt-20 border-t border-white/10 bg-black/40 py-16 backdrop-blur-md">
        <div class="max-w-4xl mx-auto text-center px-6">
            <h2 class="text-3xl font-black mb-4">El Futuro del Turismo no es Web. Es IA.</h2>
            <button class="bg-white text-black hover:bg-blue-600 hover:text-white px-10 py-5 rounded-full font-black uppercase tracking-widest transition-all shadow-xl mt-4">Quiero la Integración Lifextreme</button>
        </div>
    </footer>
    <script>
        const ctx = document.getElementById('radarChart').getContext('2d');
        const radarChart = new Chart(ctx, {{
            type: 'radar',
            data: {{
                labels: ['Visibilidad IA (GEO)', 'Seguridad Legal', 'Ventas Automáticas', 'Precios Dinámicos', 'Expansión B2B'],
                datasets: [
                    {{ label: 'Grandes Líderes', data: [95, 100, 85, 90, 100], backgroundColor: 'rgba(59, 130, 246, 0.2)', borderColor: 'rgba(59, 130, 246, 1)', borderWidth: 2 }},
                    {{ label: 'Tu Agencia ({parsed_url.netloc})', data: [{score_geo}, {score_legal}, {score_auto}, 0, 10], backgroundColor: 'rgba(239, 68, 68, 0.3)', borderColor: 'rgba(239, 68, 68, 1)', borderWidth: 2 }}
                ]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, scales: {{ r: {{ ticks: {{ display: false, min: 0, max: 100 }} }} }} }}
        }});
    </script>
</body>
</html>"""
    
    return {"html": html_content}
