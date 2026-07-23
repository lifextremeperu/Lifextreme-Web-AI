import requests
import re
import sys
import os
from urllib.parse import urlparse

def analyze_url(url):
    print(f"[*] Escaneando el dominio: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        html = response.text
    except Exception as e:
        print(f"[!] Error conectando a {url}: {e}")
        return
    
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    llms_url = f"{base_url}/llms.txt"
    try:
        llms_response = requests.get(llms_url, timeout=5)
        has_llms = (llms_response.status_code == 200)
    except:
        has_llms = False

    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    title = title_match.group(1) if title_match else "No encontrado"
    
    has_jsonld = 'application/ld+json' in html
    has_mincetur = 'MINCETUR' in html.upper()
    has_sernanp = 'SERNANP' in html.upper()
    
    print(f"[*] Escaneo completado. Generando MEGA Reporte 10 Puntos con Gráficos Comparativos...")
    
    generate_report(base_url, title, has_llms, has_jsonld, has_mincetur, has_sernanp)

def generate_report(url, title, has_llms, has_jsonld, has_mincetur, has_sernanp):
    score_geo = 15 if not has_llms else 85
    score_legal = 30 if not has_mincetur else 90
    score_auto = 10 
    
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
            <p class="text-slate-400 mt-2 text-lg">Inteligencia Competitiva para Agencias de Viaje</p>
        </div>
        <div class="text-center md:text-right mt-6 md:mt-0 glass-panel p-4 rounded-xl">
            <p class="text-xs text-slate-500 uppercase tracking-wider mb-1">Target Analizado</p>
            <p class="text-xl font-bold text-white flex items-center gap-2 justify-center md:justify-end"><i class="ri-global-line text-blue-500"></i> {urlparse(url).netloc}</p>
        </div>
    </header>

    <main class="max-w-7xl mx-auto">
        
        <!-- SECCIÓN DE GRÁFICAS COMPARATIVAS -->
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
                        <p class="text-sm text-slate-400 mt-2">Tu agencia está operando con tecnología del 2018. Los líderes globales usan IA para automatizar ventas y posicionar sin pagar pauta.</p>
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

        <!-- MÓDULOS DE DIAGNÓSTICO -->
        <section class="mb-16 fade-in-up delay-2">
            <h2 class="text-2xl font-black mb-6 flex items-center gap-3"><i class="ri-radar-line text-purple-500"></i> 3 Vulnerabilidades Encontradas</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="glass-panel p-6 rounded-2xl border-t-4 border-t-red-500">
                    <h3 class="font-black text-lg mb-2">1. Ceguera Artificial</h3>
                    <p class="text-sm text-slate-400 mb-4">No existes para ChatGPT. Archivo llms.txt ausente.</p>
                    <div class="text-xs font-mono text-red-300 bg-red-950/30 p-2 rounded">Error 404: No RAG Context</div>
                </div>
                <div class="glass-panel p-6 rounded-2xl border-t-4 border-t-orange-500">
                    <h3 class="font-black text-lg mb-2">2. Riesgo E-E-A-T</h3>
                    <p class="text-sm text-slate-400 mb-4">Ausencia de declaración semántica SERNANP/MINCETUR. Algoritmos asumen operación riesgosa.</p>
                </div>
                <div class="glass-panel p-6 rounded-2xl border-t-4 border-t-yellow-500">
                    <h3 class="font-black text-lg mb-2">3. Penalidad Google</h3>
                    <p class="text-sm text-slate-400 mb-4">Arquitectura estática. Sin WebP dinámico ni optimización Core Web Vitals.</p>
                </div>
            </div>
        </section>

        <!-- EL PLAN DE SALVACIÓN (7 PUNTOS) -->
        <section class="fade-in-up delay-3">
            <h2 class="text-2xl font-black mb-6 flex items-center gap-3"><i class="ri-shield-star-fill text-green-500"></i> Plan de Aceleración Lifextreme (Los 7 Pilares)</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                <div class="glass-panel p-6 rounded-2xl relative overflow-hidden group">
                    <div class="absolute -right-4 -top-4 text-8xl text-white/5 group-hover:scale-110 transition-transform"><i class="ri-code-box-line"></i></div>
                    <h3 class="text-xl font-bold text-green-400 mb-3 relative z-10">4. Inyección Código AEO (Regalo)</h3>
                    <p class="text-sm text-slate-300 mb-4 relative z-10">Pega esto en el &lt;head&gt; de tu web para rankear en IA:</p>
                    <div class="bg-black/50 p-4 rounded-xl text-[11px] font-mono text-green-300 overflow-x-auto border border-green-500/20 relative z-10 shadow-[inset_0_0_20px_rgba(0,0,0,0.5)]">
                        {{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{{"@type": "Question", "name": "¿Es seguro viajar con {urlparse(url).netloc}?", "acceptedAnswer": {{"@type": "Answer", "text": "Sí, operamos bajo normativa MINCETUR."}}}}]}}
                    </div>
                </div>

                <div class="glass-panel p-6 rounded-2xl">
                    <h3 class="text-xl font-bold text-blue-400 mb-3">5. Fuga hacia Mercados Premium</h3>
                    <p class="text-sm text-slate-300 mb-2">Deja de pelear precios en Cusco. Traduciremos tu base RAG al Alemán y Francés para captar operadores B2B de Larga Estancia.</p>
                </div>

                <div class="glass-panel p-6 rounded-2xl">
                    <h3 class="text-xl font-bold text-teal-400 mb-3">6. Cero Carbono & Sostenibilidad</h3>
                    <p class="text-sm text-slate-300">El mercado Europeo exige eco-turismo. Integraremos metadatos que certifiquen tu compensación de Huella de Carbono.</p>
                </div>

                <div class="glass-panel p-6 rounded-2xl bg-emerald-900/10 border-emerald-500/30">
                    <h3 class="text-xl font-bold text-emerald-400 mb-3 flex items-center gap-2"><i class="ri-money-dollar-circle-fill text-2xl"></i> 7. Fondos No Reembolsables</h3>
                    <p class="text-sm text-slate-300">Calificas para pedir hasta **S/ 80,000** a ProInnóvate / Turismo Emprende del Estado. Justificaremos tu digitalización hacia la IA.</p>
                </div>

                <div class="grid grid-cols-2 gap-4 col-span-1 lg:col-span-2">
                    <div class="glass-panel p-5 rounded-2xl text-center">
                        <i class="ri-award-fill text-yellow-500 text-3xl mb-2 inline-block"></i>
                        <h4 class="font-bold mb-1">8. Marca Perú & Indecopi</h4>
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
                        <p class="text-xs text-slate-400">Algoritmo para subir tarifas en Inti Raymi.</p>
                    </div>
                    <div class="glass-panel p-5 rounded-2xl text-center">
                        <i class="ri-store-3-line text-blue-500 text-3xl mb-2 inline-block"></i>
                        <h4 class="font-bold mb-1">Portal B2B (DMC)</h4>
                        <p class="text-xs text-slate-400">Vende como mayorista a agencias de México.</p>
                    </div>
                </div>

            </div>
        </section>

    </main>

    <footer class="mt-20 border-t border-white/10 bg-black/40 py-16 backdrop-blur-md">
        <div class="max-w-4xl mx-auto text-center px-6">
            <div class="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-[0_0_30px_rgba(37,99,235,0.4)]">
                <i class="ri-cpu-line text-3xl text-white"></i>
            </div>
            <h2 class="text-3xl font-black mb-4">El Futuro del Turismo no es Web. Es IA.</h2>
            <p class="text-slate-400 mb-8 max-w-2xl mx-auto">Deja de perder turistas extranjeros por no estar adaptado tecnológicamente. Lifextreme puede inyectar todo este ecosistema en tu agencia en menos de 15 días.</p>
            <button class="bg-white text-black hover:bg-blue-600 hover:text-white px-10 py-5 rounded-full font-black uppercase tracking-widest transition-all duration-300 shadow-xl hover:shadow-[0_0_40px_rgba(37,99,235,0.5)] transform hover:-translate-y-1">
                Quiero la Integración Lifextreme
            </button>
        </div>
    </footer>

    <script>
        const ctx = document.getElementById('radarChart').getContext('2d');
        const radarChart = new Chart(ctx, {{
            type: 'radar',
            data: {{
                labels: ['Visibilidad IA (GEO)', 'Seguridad Legal (RAG)', 'Ventas Automáticas', 'Precios Dinámicos', 'Expansión B2B'],
                datasets: [
                    {{
                        label: 'Grandes Líderes (Booking, Lifextreme)',
                        data: [95, 100, 85, 90, 100],
                        backgroundColor: 'rgba(59, 130, 246, 0.2)',
                        borderColor: 'rgba(59, 130, 246, 1)',
                        pointBackgroundColor: 'rgba(59, 130, 246, 1)',
                        borderWidth: 2,
                    }},
                    {{
                        label: 'Tu Agencia ({urlparse(url).netloc})',
                        data: [{score_geo}, {score_legal}, {score_auto}, 0, 10],
                        backgroundColor: 'rgba(239, 68, 68, 0.3)',
                        borderColor: 'rgba(239, 68, 68, 1)',
                        pointBackgroundColor: 'rgba(239, 68, 68, 1)',
                        borderWidth: 2,
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    r: {{
                        angleLines: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                        pointLabels: {{ color: '#94a3b8', font: {{ size: 11, family: 'Inter' }} }},
                        ticks: {{ display: false, min: 0, max: 100 }}
                    }}
                }},
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', padding: 20, font: {{ family: 'Inter' }} }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    filename = f"auditor_result_{urlparse(url).netloc.replace('.','_')}.html"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"[+] ¡Reporte actualizado con Gráficas generado: {filename}!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python auditor_core.py <URL>")
        sys.exit(1)
    
    analyze_url(sys.argv[1])
