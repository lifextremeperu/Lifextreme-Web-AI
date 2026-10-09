import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dossier Científico y Neuromarketing - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Space+Grotesk:wght@700&display=swap');
        
        body { 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background-color: #f4f7f6; 
            color: #1a202c; 
            margin: 0; 
            padding: 30px 40px; 
            font-size: 12px; 
            line-height: 1.6;
        }
        
        .header { 
            text-align: center;
            padding-bottom: 20px; 
            border-bottom: 2px solid #cbd5e0;
            margin-bottom: 30px; 
        }
        
        .logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 32px; 
            color: #2d3748; 
            font-weight: 700; 
            letter-spacing: -1px;
        }
        .logo span { color: #3182ce; }
        
        .title {
            font-size: 26px;
            font-weight: 800;
            color: #2b6cb0;
            margin: 10px 0;
            line-height: 1.2;
            text-transform: uppercase;
        }
        
        .subtitle {
            color: #4a5568;
            font-size: 13px;
            font-weight: 600;
        }
        
        .module-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            page-break-inside: avoid;
            border-left: 6px solid #3182ce;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            align-items: center;
        }
        
        .module-content {
            display: flex;
            flex-direction: column;
        }
        
        .mod-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 10px;
        }
        
        .mod-tag {
            display: inline-block;
            background: #ebf8ff;
            color: #3182ce;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 15px;
            width: fit-content;
        }
        
        .text-block {
            margin-bottom: 15px;
        }
        
        .text-label {
            font-weight: 800;
            color: #2b6cb0;
            font-size: 11px;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        
        .chart-container {
            background: #f8fafc;
            border-radius: 8px;
            padding: 15px;
            border: 1px solid #e2e8f0;
            text-align: center;
        }
        
        .chart-title {
            font-size: 11px;
            font-weight: 800;
            color: #4a5568;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        
        /* SVGs styling */
        svg text { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; fill: #4a5568; }
        
        .insight-box {
            background: #f0fdf4;
            border-left: 3px solid #38a169;
            padding: 12px;
            margin-top: 10px;
            border-radius: 4px;
        }
        
        .page-break { page-break-before: always; }
        
    </style>
</head>
<body>

    <div class="header">
        <div class="logo">LIFEXTREME<span>.DATA</span></div>
        <h1 class="title">NEUROMARKETING Y BIG DATA APLICADA</h1>
        <div class="subtitle">Análisis Científico de Variables Macro-Económicas, Psicológicas y Políticas para Toma de Decisiones en Turismo.</div>
    </div>

    <!-- MODULO 1: PRECIOS PREDICTIVOS -->
    <div class="module-card">
        <div class="module-content">
            <div class="mod-tag">🧠 NEUROMARKETING & ALGORITMOS TIMESFM</div>
            <div class="mod-title">Precios Predictivos: Vender la Urgencia</div>
            <div class="text-block">
                <div class="text-label">LA CIENCIA DETRÁS DEL DATO:</div>
                <div>El consumidor latinoamericano sufre de "Procrastinación de Compra". Nuestros agentes <strong>TimesFM</strong> analizan la saturación de vuelos. Cuando quedan pocos asientos hacia Cusco, el cerebro del turista entra en estado de "Escasez" (FOMO).</div>
            </div>
            <div class="text-block">
                <div class="text-label">LA OPORTUNIDAD FÁCIL:</div>
                <div>En vez de mantener un precio fijo, usa la <strong>curva de urgencia</strong>. A medida que se acerca la fecha del viaje, incrementa el precio un 15%. El turista no cuestionará el precio porque su prioridad mental ya no es ahorrar, sino asegurar su espacio.</div>
            </div>
        </div>
        <div class="chart-container">
            <div class="chart-title">Curva de Elasticidad de Precio (TimesFM)</div>
            <svg viewBox="0 0 400 200" width="100%" height="150">
                <line x1="40" y1="160" x2="380" y2="160" stroke="#cbd5e0" stroke-width="2"/>
                <line x1="40" y1="20" x2="40" y2="160" stroke="#cbd5e0" stroke-width="2"/>
                <!-- Curve -->
                <path d="M 40 140 Q 200 140 280 80 T 360 30" fill="none" stroke="#3182ce" stroke-width="4"/>
                <!-- Highlight Point -->
                <circle cx="280" cy="80" r="6" fill="#e53e3e"/>
                <text x="290" y="75" fill="#e53e3e" font-weight="bold">+15% Ganancia</text>
                
                <text x="50" y="180">Mes Antes</text>
                <text x="180" y="180">15 Días Antes</text>
                <text x="320" y="180">3 Días Antes (Urgencia)</text>
                <text x="5" y="90" transform="rotate(-90 15,90)">Precio del Tour ($)</text>
            </svg>
            <div class="insight-box">
                <span style="color: #38a169; font-weight: 800;">Dato:</span> La voluntad de pago sube un 40% a 3 días del viaje.
            </div>
        </div>
    </div>

    <!-- MODULO 2: MACROECONOMIA Y PETROLEO -->
    <div class="module-card">
        <div class="module-content">
            <div class="mod-tag">🛢️ GEOPOLÍTICA & SUMINISTRO (JET-A1)</div>
            <div class="mod-title">El Petróleo dicta quién puede viajar a Perú</div>
            <div class="text-block">
                <div class="text-label">LA CIENCIA DETRÁS DEL DATO:</div>
                <div>Cusco no es una burbuja. Si hay conflictos en Medio Oriente, el petróleo (Jet-A1) sube. Esto encarece los vuelos de Europa a Lima en un 25%. El turista europeo de "clase media" cancela su viaje porque pierde liquidez.</div>
            </div>
            <div class="text-block">
                <div class="text-label">LA OPORTUNIDAD FÁCIL:</div>
                <div>Monitorea las noticias. Si la gasolina y los vuelos suben a nivel mundial, <strong>apaga tus anuncios para turistas normales</strong>. Empieza a apuntar tus ofertas únicamente a viajeros de Lujo (UHNWI), porque a un millonario no le importa si el vuelo cuesta $500 más.</div>
            </div>
        </div>
        <div class="chart-container">
            <div class="chart-title">Impacto del Precio del Petróleo en Demanda Turística</div>
            <svg viewBox="0 0 400 200" width="100%" height="150">
                <line x1="40" y1="160" x2="380" y2="160" stroke="#cbd5e0" stroke-width="2"/>
                <line x1="40" y1="20" x2="40" y2="160" stroke="#cbd5e0" stroke-width="2"/>
                <!-- Petroleo Line -->
                <path d="M 40 140 L 150 120 L 250 50 L 360 30" fill="none" stroke="#e53e3e" stroke-width="3" stroke-dasharray="5,5"/>
                <!-- Demanda Line -->
                <path d="M 40 50 L 150 70 L 250 130 L 360 150" fill="none" stroke="#3182ce" stroke-width="4"/>
                
                <text x="365" y="35" fill="#e53e3e" font-weight="bold">Precio Petróleo</text>
                <text x="365" y="155" fill="#3182ce" font-weight="bold">Turistas Regulares</text>
            </svg>
            <div class="insight-box">
                <span style="color: #38a169; font-weight: 800;">Táctica:</span> Cruce de datos Qdrant + GDELT muestra correlación inversa.
            </div>
        </div>
    </div>

    <!-- MODULO 3: PSICOLOGIA B2C - CONVERSION -->
    <div class="module-card">
        <div class="module-content">
            <div class="mod-tag">💬 PSICOLOGÍA DEL CONSUMIDOR (FQSA)</div>
            <div class="mod-title">El Miedo y la Fricción Matan la Venta Web</div>
            <div class="text-block">
                <div class="text-label">LA CIENCIA DETRÁS DEL DATO:</div>
                <div>El RAG de Lifextreme prueba que el cerebro reptiliano del turista siente "Peligro" al rellenar un formulario web gigante y esperar 24h. Su nivel de dopamina cae a cero. Las ventas web frías solo cierran un 8%.</div>
            </div>
            <div class="text-block">
                <div class="text-label">LA OPORTUNIDAD FÁCIL:</div>
                <div>Muda tus ventas a <strong>WhatsApp</strong>. Es un canal de "alta confianza y dopamina rápida". Respuestas inmediatas, envío de PDF bonito y un Link de pago 1-clic disparan la conversión al 35%.</div>
            </div>
        </div>
        <div class="chart-container">
            <div class="chart-title">Tasa de Conversión (Formulario vs WhatsApp)</div>
            <svg viewBox="0 0 400 200" width="100%" height="150">
                <!-- Bar 1 -->
                <rect x="100" y="130" width="60" height="30" fill="#a0aec0" rx="4"/>
                <text x="110" y="120" font-weight="bold" font-size="12">8%</text>
                <text x="85" y="180">Formulario Web</text>
                
                <!-- Bar 2 -->
                <rect x="250" y="40" width="60" height="120" fill="#38a169" rx="4"/>
                <text x="260" y="30" font-weight="bold" font-size="12" fill="#38a169">35%</text>
                <text x="235" y="180">Cierre WhatsApp</text>
                
                <line x1="40" y1="160" x2="380" y2="160" stroke="#cbd5e0" stroke-width="2"/>
            </svg>
            <div class="insight-box">
                <span style="color: #38a169; font-weight: 800;">Impacto:</span> x4 veces más ventas sin gastar 1 centavo extra en marketing.
            </div>
        </div>
    </div>
    
    <div class="page-break"></div>
    
    <div class="header" style="margin-top: 15px;">
        <div class="logo">LIFEXTREME<span>.DATA</span></div>
        <div class="subtitle">Continuación: Modelado Político y Posicionamiento de Máquinas</div>
    </div>

    <!-- MODULO 4: CRISIS POLITICAS Y LOGISTICA -->
    <div class="module-card">
        <div class="module-content">
            <div class="mod-tag">🚨 INTELIGENCIA SUTRAN / SENAMHI</div>
            <div class="mod-title">Decisiones Políticas vs Cero Reembolsos</div>
            <div class="text-block">
                <div class="text-label">LA CIENCIA DETRÁS DEL DATO:</div>
                <div>Una protesta campesina o un cierre del Mincetur en Machu Picchu significa la quiebra para una agencia tradicional, porque devuelve el 100% del dinero. Es una pérdida de liquidez fulminante.</div>
            </div>
            <div class="text-block">
                <div class="text-label">LA OPORTUNIDAD FÁCIL:</div>
                <div><strong>Rutas Secundarias Parametrizadas.</strong> Si los sensores detectan conflicto en la ruta al Valle Sur, los contratos de Lifextreme incluyen cláusulas de "Flexibilidad Turística". El turista acepta ir a otra zona segura (ej. Chinchero/Maras) automáticamente. No devuelves el dinero, solo desvías el flujo.</div>
            </div>
        </div>
        <div class="chart-container">
            <div class="chart-title">Estructura de Capital ante Huelgas</div>
            <svg viewBox="0 0 400 200" width="100%" height="150">
                <!-- Pie 1 -->
                <circle cx="120" cy="90" r="50" fill="#e53e3e"/>
                <path d="M 120 90 L 120 40 A 50 50 0 0 1 170 90 Z" fill="#c53030"/>
                <text x="80" y="160">Agencia Tradicional</text>
                <text x="90" y="175" fill="#e53e3e" font-weight="bold">(100% Reembolso)</text>
                
                <!-- Pie 2 -->
                <circle cx="280" cy="90" r="50" fill="#3182ce"/>
                <path d="M 280 90 L 280 40 A 50 50 0 0 1 330 90 Z" fill="#2b6cb0"/>
                <text x="240" y="160">Agencia Lifextreme</text>
                <text x="235" y="175" fill="#3182ce" font-weight="bold">(Redirección - 0% Pérdida)</text>
            </svg>
            <div class="insight-box">
                <span style="color: #38a169; font-weight: 800;">Protección:</span> Blindaje financiero total contra coyunturas sociopolíticas del Perú.
            </div>
        </div>
    </div>

    <!-- MODULO 5: SEO SEMANTICO (AEO) -->
    <div class="module-card">
        <div class="module-content">
            <div class="mod-tag">🤖 AEO (ANSWER ENGINE OPTIMIZATION)</div>
            <div class="mod-title">Hablarle a los Robots (No a los humanos)</div>
            <div class="text-block">
                <div class="text-label">LA CIENCIA DETRÁS DEL DATO:</div>
                <div>Los turistas ya no buscan en Google; le preguntan a ChatGPT o Perplexity. Estos "LLMs" no leen fotos bonitas, leen <em>Data Estructurada (Schema.org)</em> y Tablas de Datos. Si tu web no tiene esto, eres invisible para la Inteligencia Artificial.</div>
            </div>
            <div class="text-block">
                <div class="text-label">LA OPORTUNIDAD FÁCIL:</div>
                <div>Reestructura tu web. Añade secciones de "Preguntas y Respuestas Frecuentes" con textos hiper-claros (Ej: "La distancia a la Laguna Humantay es 2km"). Los bots de IA amarán esa claridad y te pondrán como la respuesta #1 cuando un turista les pregunte.</div>
            </div>
        </div>
        <div class="chart-container">
            <div class="chart-title">Evolución de Tráfico Web (2025-2027)</div>
            <svg viewBox="0 0 400 200" width="100%" height="150">
                <line x1="40" y1="160" x2="380" y2="160" stroke="#cbd5e0" stroke-width="2"/>
                <line x1="40" y1="20" x2="40" y2="160" stroke="#cbd5e0" stroke-width="2"/>
                
                <!-- Google SEO (Bajando) -->
                <path d="M 40 50 L 150 70 L 250 110 L 360 140" fill="none" stroke="#e53e3e" stroke-width="3"/>
                <!-- AI AEO (Subiendo) -->
                <path d="M 40 140 L 150 110 L 250 60 L 360 30" fill="none" stroke="#38a169" stroke-width="4"/>
                
                <text x="270" y="130" fill="#e53e3e" font-weight="bold">Búsqueda Google</text>
                <text x="270" y="45" fill="#38a169" font-weight="bold">Respuestas I.A.</text>
            </svg>
            <div class="insight-box">
                <span style="color: #38a169; font-weight: 800;">Supervivencia:</span> El tráfico orgánico ahora depende de ser citado por ChatGPT o Google SGE.
            </div>
        </div>
    </div>
    
    <div style="background: #2b6cb0; color: white; padding: 25px; border-radius: 12px; text-align: center; margin-top: 10px; box-shadow: 0 10px 20px rgba(43, 108, 176, 0.3);">
        <h2 style="margin-top: 0; font-family: 'Space Grotesk'; font-size: 22px;">EL RESPALDO DE LIFEXTREME</h2>
        <p style="font-size: 14px; margin-bottom: 0;">Esta información científica y psicológica proviene del RAG Cerebro de Lifextreme. Mientras usted usa estos datos para <strong>duplicar sus ventas y hablarle a la IA</strong>, nosotros aplicamos esta misma ciencia operando sus rutas en terreno con precisión militar.</p>
    </div>

</body>
</html>
"""

async def generate_scientific_pdf():
    print("Preparando Reporte Científico y Visual (Con Gráficos SVG)...")
    html_path = os.path.abspath("temp_scientific.html")
    pdf_path = os.path.abspath("Lifextreme_Dossier_Cientifico_Visual.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(f"file:///{html_path}")
        await page.wait_for_timeout(1000)
        
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        
        await browser.close()
        
    if os.path.exists(html_path):
        os.remove(html_path)
        
    print(f"PDF Científico Visual generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_scientific_pdf())
    except Exception as e:
        pass
