import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Plan Maestro Ejecutivo - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;800&family=Inter:wght@300;400;600;700&display=swap');
        
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: 'Inter', sans-serif; 
            margin: 0; padding: 0; 
            background: #ffffff; color: #1e293b;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
        }}
        
        .a4-page {{
            width: 794px; height: 1123px;
            padding: 70px 80px;
            position: relative; overflow: hidden;
            page-break-after: always; margin: 0 auto;
            background: #ffffff;
        }}
        
        /* COVER PAGE */
        .cover {{ background: #0f172a; color: #ffffff; }}
        .cover-header {{ border-bottom: 2px solid #3b82f6; padding-bottom: 20px; margin-bottom: 150px; font-size: 14px; letter-spacing: 4px; color: #94a3b8; text-transform: uppercase; }}
        .cover-title {{ font-family: 'Playfair Display', serif; font-size: 55px; font-weight: 800; line-height: 1.1; margin-bottom: 40px; }}
        .cover-subtitle {{ font-size: 18px; color: #cbd5e1; font-weight: 300; line-height: 1.6; max-width: 90%; border-left: 4px solid #3b82f6; padding-left: 20px; }}
        .cover-meta {{ position: absolute; bottom: 80px; left: 80px; font-size: 12px; color: #64748b; font-family: monospace; line-height: 2; }}
        
        /* INNER PAGES */
        h1 {{ font-family: 'Playfair Display', serif; font-size: 32px; color: #0f172a; border-bottom: 3px solid #0f172a; padding-bottom: 10px; margin-bottom: 30px; text-transform: uppercase; }}
        h2 {{ font-family: 'Playfair Display', serif; font-size: 20px; color: #3b82f6; margin-top: 30px; margin-bottom: 15px; text-transform: uppercase; }}
        p {{ font-size: 14px; line-height: 1.7; color: #334155; margin-bottom: 15px; text-align: justify; }}
        
        .highlight-box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #3b82f6; padding: 25px; margin: 25px 0; }}
        .highlight-box h3 {{ margin: 0 0 10px 0; font-size: 16px; color: #0f172a; }}
        .highlight-box p {{ margin: 0; font-size: 13px; color: #475569; }}
        
        ul {{ padding-left: 20px; margin-bottom: 20px; }}
        li {{ font-size: 14px; line-height: 1.7; color: #334155; margin-bottom: 8px; }}
        
        .footer {{ position: absolute; bottom: 50px; left: 80px; right: 80px; border-top: 1px solid #cbd5e1; padding-top: 15px; display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 2px; }}
        
    </style>
</head>
<body>

    <!-- PORTADA -->
    <div class="a4-page cover">
        <div class="cover-header">DOCUMENTO MAESTRO // ESTRICTAMENTE CONFIDENCIAL</div>
        <h1 class="cover-title">EL GRAN PLAN MAESTRO<br>LIFEXTREME 2026</h1>
        <div class="cover-subtitle">
            Arquitectura corporativa, modelo de dominación tecnológica y hoja de ruta estratégica para el Holding Tecnológico Lifextreme y el Proyecto Pampa Ñusta.
        </div>
        <div class="cover-meta">
            PREPARADO POR: LIFEXTREME BIG DATA INTELLIGENCE<br>
            OBJETIVO: GO-TO-MARKET & ESTRUCTURA DE INVERSIÓN<br>
            VERSIÓN: 1.0 (MASTER PROTOCOL)
        </div>
    </div>

    <!-- PÁGINA 1: ARQUITECTURA -->
    <div class="a4-page">
        <h1>I. LA ARQUITECTURA DEL IMPERIO</h1>
        <p>Lifextreme ha dejado de ser una agencia de viajes tradicional para convertirse legal y operativamente en una <strong>Matriz Tecnológica (Tech Holding)</strong>. Nuestro núcleo ya no es la venta manual de pasajes, sino la ingesta masiva de datos, la predicción algorítmica y la tercerización logística.</p>
        
        <h2>1. El Escudo Legal (Objeto Social 10X)</h2>
        <p>Se ha blindado a la corporación mediante un estatuto nivel "Big 4". Las facultades notariales ahora permiten explícitamente el desarrollo de Inteligencia Artificial, Fintech (Clearing de pagos, arbitraje de divisas), y absorción B2B. Esto nos da inmunidad registral para pivotar y escalar sin restricciones estatales.</p>

        <h2>2. El Cerebro Tecnológico (RAG Stack)</h2>
        <div class="highlight-box">
            <h3>Qdrant + TimesFM + Flask</h3>
            <p>La infraestructura local posee memoria vectorial (Qdrant) alimentada por datos del clima, SUTRAN y variables macroeconómicas. Esto nos permite ejecutar "Dynamic Pricing" (subir precios por urgencia) y redirigir flotas logísticas milisegundos después de detectar un riesgo climático.</p>
        </div>

        <h2>3. El Dualismo Comercial (B2B y B2C)</h2>
        <p>El Holding opera como un depredador de dos cabezas, atacando ambos espectros del mercado para garantizar un flujo de caja ininterrumpido.</p>
        
        <div class="footer">
            <span>PLAN MAESTRO LIFEXTREME</span>
            <span>PÁGINA 1</span>
        </div>
    </div>

    <!-- PÁGINA 2: LÍNEAS DE NEGOCIO Y ACCIÓN -->
    <div class="a4-page">
        <h1>II. LAS DOS CABEZAS DEL HOLDING</h1>
        
        <h2>Línea 1: Lifextreme Logistics (B2B SaaS)</h2>
        <p><strong>Objetivo:</strong> Absorber la logística física de las PYMES de Cusco.<br>
        Las agencias pequeñas quiebran por costos fijos y riesgo. Nosotros actuamos como su "Backend Físico". Ellos consiguen al turista, nosotros operamos el tour con nuestros estándares ISO/ESG. Facturamos por volumen de operación tercerizada, convirtiéndonos en el "AWS (Amazon Web Services)" del turismo físico.</p>

        <h2>Línea 2: Pampa Ñusta (B2C High-Ticket)</h2>
        <p><strong>Objetivo:</strong> Turismo Inmersivo de Ultra Lujo y Conexión Espiritual.<br>
        Diseñado para el europeo/norteamericano de alto patrimonio que busca escapar de la matrix. Usamos la IA silenciosamente en el fondo para garantizar la seguridad extrema del viaje, mientras la cara frontal (Frontend) ofrece autenticidad, comunidad y retiros espirituales. Márgenes de ganancia superiores al 60%.</p>

        <h1>III. HOJA DE RUTA INMEDIATA (GO-TO-MARKET)</h1>
        <p>Para dejar la fase de desarrollo e inyectar capital real (Bootstrapping), se ejecutarán las siguientes órdenes inmediatas:</p>
        
        <ul>
            <li><strong>Despliegue B2B en Frío:</strong> Uso del "Guion de Ataque" vía WhatsApp directo a 50 dueños de agencias en Cusco para afiliar sus operaciones a nuestro panel C.O.R.E.</li>
            <li><strong>Encendido del Bot de Ventas:</strong> Conectar el script <code>agent_whatsapp_sales.py</code> mediante Ngrok o VPS para atender tráfico pagado (Facebook Ads) y probar el cierre autónomo de clientes B2C.</li>
            <li><strong>Envío a Inversionistas:</strong> Presentación del "Pitch Deck Interactivo" y del "Dossier Legal" a fondos semillas para demostrar que somos una Startup DeepTech rentable.</li>
        </ul>
        
        <div class="highlight-box" style="border-left-color: #10b981;">
            <h3>MANDATO FINAL</h3>
            <p>La tecnología está lista. Los protocolos legales están escritos. Los prototipos de interfaz están operativos. El siguiente paso es 100% comercial: Conectar el servidor a internet y empezar a capturar transacciones.</p>
        </div>

        <div class="footer">
            <span>PLAN MAESTRO LIFEXTREME</span>
            <span>PÁGINA 2</span>
        </div>
    </div>

</body>
</html>
"""

async def generate_master_pdf():
    print("Generando Documento Final (Plan Maestro)...")
    html_path = os.path.abspath("temp_master_plan.html")
    pdf_path = os.path.abspath("Plan_Maestro_Lifextreme_2026.pdf")
    
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
        
    print(f"PDF Plan Maestro generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_master_pdf())
    except Exception as e:
        print(e)
