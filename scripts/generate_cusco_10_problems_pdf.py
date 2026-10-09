import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dossier Ejecutivo: Agencias Cusco - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&family=Source+Sans+Pro:wght@400;600;700&display=swap');
        
        body { 
            font-family: 'Source Sans Pro', sans-serif; 
            background-color: #0b0f19; 
            color: #d1d5db; 
            margin: 0; 
            padding: 40px; 
            font-size: 12px; 
            line-height: 1.5;
        }
        
        .header { 
            border-bottom: 2px solid #273043; 
            padding-bottom: 20px; 
            margin-bottom: 30px; 
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-family: 'Montserrat', sans-serif; 
            font-size: 24px; 
            color: #ffffff; 
            font-weight: 900; 
            letter-spacing: -1px;
        }
        
        .logo span { color: #00ff88; }
        
        .meta {
            text-align: right;
            font-family: monospace;
            color: #6b7280;
            font-size: 10px;
        }
        
        .title-container { margin-bottom: 40px; }
        
        .title {
            font-family: 'Montserrat', sans-serif;
            font-size: 32px;
            font-weight: 900;
            color: #ffffff;
            margin: 0 0 10px 0;
            line-height: 1.1;
            text-transform: uppercase;
        }
        
        .subtitle {
            color: #9ca3af;
            font-size: 14px;
            font-weight: 400;
        }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }
        
        .problem-card {
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 8px;
            padding: 20px;
            position: relative;
            page-break-inside: avoid;
        }
        
        .card-number {
            position: absolute;
            top: -12px;
            left: 20px;
            background: #273043;
            color: #ffffff;
            font-family: 'Montserrat', sans-serif;
            font-weight: 900;
            font-size: 14px;
            padding: 4px 12px;
            border-radius: 4px;
            border: 1px solid #374151;
        }
        
        .card-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 16px;
            font-weight: 800;
            color: #ffffff;
            margin-top: 5px;
            margin-bottom: 15px;
            border-bottom: 1px solid #1f2937;
            padding-bottom: 8px;
        }
        
        .status-box {
            padding: 10px 12px;
            border-radius: 4px;
            margin-bottom: 12px;
        }
        
        .status-error {
            background-color: rgba(239, 68, 68, 0.05);
            border-left: 3px solid #ef4444;
        }
        
        .status-success {
            background-color: rgba(0, 255, 136, 0.05);
            border-left: 3px solid #00ff88;
        }
        
        .status-label {
            font-family: 'Montserrat', sans-serif;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 4px;
            letter-spacing: 0.5px;
        }
        
        .error-color { color: #ef4444; }
        .success-color { color: #00ff88; }
        
        .status-text { color: #9ca3af; font-size: 11px; }
        
        .cta-box {
            background-color: #00ff88;
            color: #0b0f19;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            margin-top: 40px;
            page-break-inside: avoid;
        }
        
        .cta-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 20px;
            font-weight: 900;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        
        .page-break { page-break-before: always; }
    </style>
</head>
<body>

    <!-- PÁGINA 1 -->
    <div class="header">
        <div class="logo">LIFEXTREME<span>.AI</span></div>
        <div class="meta">
            REPORTE B2B: CUSCO<br>
            EXTRACCIÓN: BIG DATA RAG
        </div>
    </div>
    
    <div class="title-container">
        <h1 class="title">LOS 10 ERRORES FATALES<br>DE LAS AGENCIAS EN CUSCO</h1>
        <div class="subtitle">Auditoría Ejecutiva: Diagnóstico de mercado y soluciones de Inteligencia de Datos para Operadores Turísticos.</div>
    </div>

    <div class="grid-2">
        <!-- 1 -->
        <div class="problem-card">
            <div class="card-number">01</div>
            <div class="card-title">La Trampa del Precio (Océano Rojo)</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">Compiten en la Plaza de Armas o Facebook rebajando el "City Tour" a márgenes de ganancia críticos ($5 - $10 USD).</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Empaquetamiento "High-Ticket". El turista millonario (UHNWI) no compra descuentos. Vender transformación y exclusividad ($150+) con experiencias privadas.</div>
            </div>
        </div>

        <!-- 2 -->
        <div class="problem-card">
            <div class="card-number">02</div>
            <div class="card-title">Fricción Web y Abandono</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">Dependen de un formulario de contacto arcaico ("Te responderemos en 24h"). Tasa de conversión estancada en 8%.</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Embudos vía Mensajería. Venta consultiva por WhatsApp con envíos de PDF automatizados y Link de pago directo. Conversión probada del 35%.</div>
            </div>
        </div>

        <!-- 3 -->
        <div class="problem-card">
            <div class="card-number">03</div>
            <div class="card-title">Inversión Inútil en Meta Ads</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">Queman presupuesto en Facebook con fotos de archivo genéricas segmentadas a "todo el mundo".</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Framework ECS en TikTok. Uso de Micro-Influencers extranjeros (10k-50k) auditados, bajando el Costo de Adquisición de Cliente (CAC) un 70%.</div>
            </div>
        </div>

        <!-- 4 -->
        <div class="problem-card">
            <div class="card-number">04</div>
            <div class="card-title">Manejo de Objeciones (Fricciones)</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">Ocultan los riesgos (mal de altura, clima). El cliente no confía o viaja asustado, resultando en quejas.</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Arquitectura web FQSA. Adelantarse al miedo: "Sabemos que temes a la altura; incluimos oxígeno y paramédico". Convertir objeciones en ventas.</div>
            </div>
        </div>
    </div>
    
    <div class="page-break"></div>

    <!-- PÁGINA 2 -->
    <div class="header" style="margin-top: 20px;">
        <div class="logo">LIFEXTREME<span>.AI</span></div>
        <div class="meta">ANÁLISIS CONTINUADO (05 - 10)</div>
    </div>

    <div class="grid-2">
        <!-- 5 -->
        <div class="problem-card">
            <div class="card-number">05</div>
            <div class="card-title">Dictadura de las OTAs (Booking/Viator)</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">Regalan entre el 18% y 25% de comisión por venta a plataformas de terceros, destruyendo el margen neto.</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Estrategia D2C (Direct-to-Consumer). Captar el cliente directamente compensándolo con "Upgrades" gratuitos, reteniendo el 100% del margen.</div>
            </div>
        </div>

        <!-- 6 -->
        <div class="problem-card">
            <div class="card-number">06</div>
            <div class="card-title">Logística Reactiva (El factor SUTRAN)</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">Venden Vinicunca, pero si hay huelga o nevada al día siguiente, cancelan todo y pierden la liquidez en reembolsos.</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Logística Predictiva. Si hay riesgo de cierre, aplicar inmediatamente un "Upsell de Seguridad" redirigiendo al cliente a Palccoyo. Cero reembolsos.</div>
            </div>
        </div>

        <!-- 7 -->
        <div class="problem-card">
            <div class="card-number">07</div>
            <div class="card-title">Invisibilidad de Micro-Nichos</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">Ofrecen "paquetes genéricos para familias" perdiéndose entre 5,000 agencias idénticas.</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Atacar vectores de alta rentabilidad sin competencia: Solo Female Travelers (Mujeres viajando solas) o Turismo Pet-Friendly VIP.</div>
            </div>
        </div>

        <!-- 8 -->
        <div class="problem-card">
            <div class="card-number">08</div>
            <div class="card-title">Falta de Upselling (LTV)</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">El turista compra un boleto y la relación comercial termina inmediatamente. No hay re-venta.</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Optimización del Life-Time Value (LTV). Ofrecer servicios adicionales (fotógrafo, menú premium) por WhatsApp días antes de su viaje.</div>
            </div>
        </div>
        
        <!-- 9 -->
        <div class="problem-card">
            <div class="card-number">09</div>
            <div class="card-title">Invisibilidad ante LLMs (AEO)</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">Gastan en SEO antiguo con palabras clave, ignorando que hoy el turista planifica su viaje preguntándole a ChatGPT.</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Answer Engine Optimization (AEO). Webs con datos estructurados para que las IAs como Google SGE y Perplexity citen a la agencia como autoridad.</div>
            </div>
        </div>

        <!-- 10 -->
        <div class="problem-card">
            <div class="card-number">10</div>
            <div class="card-title">Burnout y Operaciones Manuales</div>
            <div class="status-box status-error">
                <div class="status-label error-color">❌ Cómo Venden Hoy:</div>
                <div class="status-text">El dueño vende, alquila el bus, despacha y responde quejas de madrugada. Imposibilidad total de escalar el negocio.</div>
            </div>
            <div class="status-box status-success">
                <div class="status-label success-color">✅ Solución Lifextreme (Data):</div>
                <div class="status-text">Tercerización Operativa Tecnológica. La agencia se dedica 100% a cerrar ventas de Alto Valor; Lifextreme opera la logística cruda en terreno.</div>
            </div>
        </div>
    </div>

    <div class="cta-box">
        <div class="cta-title">DEJE DE COMPETIR. COMIENCE A DOMINAR EL MERCADO.</div>
        <p style="font-weight: 600; font-size: 14px; margin-bottom: 0;">Si su agencia sufre de 3 o más de estos problemas, está perdiendo capital a diario. Usted enfoque su equipo en ventas; Lifextreme pondrá los buses, los guías, la tecnología satelital y el respaldo logístico para operar sus rutas de forma impecable.</p>
    </div>

</body>
</html>
"""

async def generate_dossier_pdf():
    print("Preparando Dossier de los 10 Problemas (Dark Mode/Corporate)...")
    html_path = os.path.abspath("temp_dossier.html")
    pdf_path = os.path.abspath("Dossier_10_Problemas_Agencias_Cusco.pdf")
    
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
        
    print(f"PDF Dossier generado correctamente en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_dossier_pdf())
    except Exception as e:
        pass
