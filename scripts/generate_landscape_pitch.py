import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

img_cover = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\amazon_community_tourism_1791572171378.jpg"
img_b2b = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\corporate_travel_pyme_1791572199630.jpg"
img_traction = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\cusco_business_tourist_1791572148790.jpg"

uri_cover = "file:///" + img_cover.replace("\\", "/")
uri_b2b = "file:///" + img_b2b.replace("\\", "/")
uri_traction = "file:///" + img_traction.replace("\\", "/")

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Pitch Deck - Pampa Ñusta</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Montserrat:wght@300;400;600;800&display=swap');
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{ 
            font-family: 'Montserrat', sans-serif; 
            background: #111512; 
            color: #e5e7eb;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        
        /* DIMENSIONES A4 LANDSCAPE EXACTAS PARA PRESENTACIONES */
        .slide-page {{
            width: 1123px;
            height: 794px;
            background: #0a0f0c;
            position: relative;
            overflow: hidden;
            page-break-after: always;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 60px 80px;
        }}
        
        /* FONDOS CON IMÁGENES */
        .bg-img {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            object-fit: cover;
            z-index: 1;
        }}
        
        .overlay {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(10, 15, 12, 0.85);
            z-index: 2;
        }}
        
        .content-layer {{
            position: relative;
            z-index: 10;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        
        h1, h2, h3, h4 {{
            font-family: 'Cinzel', serif;
            color: #c9a75c; /* Oro viejo */
            text-transform: uppercase;
        }}
        
        /* PORTADA */
        .title-main {{
            font-size: 55px;
            color: #ffffff;
            line-height: 1.1;
            margin: 20px 0;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.9);
        }}
        
        /* BLOQUES DE CONTENIDO */
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; text-align: left; margin-top: 40px; }}
        .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; text-align: center; margin-top: 40px; }}
        
        .box {{
            background: rgba(20, 20, 20, 0.9);
            border-left: 4px solid #c9a75c;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        .box-title {{ color: #ffffff; font-size: 22px; margin-bottom: 10px; }}
        .box-text {{ font-size: 14px; color: #d1d5db; line-height: 1.6; }}
        
        .metric-val {{ font-size: 50px; font-weight: 800; color: #10b981; margin-bottom: 5px; }}
        .metric-lbl {{ font-size: 14px; color: #9ca3af; text-transform: uppercase; letter-spacing: 2px; }}
        
    </style>
</head>
<body>

    <!-- SLIDE 1: PORTADA -->
    <div class="slide-page">
        <img class="bg-img" src="{uri_cover}">
        <div class="overlay" style="background: rgba(10, 15, 12, 0.6);"></div>
        <div class="content-layer" style="justify-content: center;">
            <h3 style="font-size: 20px; letter-spacing: 5px; color: #ffffff;">PROYECTO PAMPA ÑUSTA</h3>
            <h1 class="title-main">EL ALMA DE LOS ANDES,<br>LA MENTE DE SILICON VALLEY</h1>
            <p style="font-weight: 300; font-size: 18px; max-width: 800px; margin: 0 auto; color: #e5e7eb;">
                El primer consorcio turístico que fusiona la sabiduría ancestral comunitaria con modelos predictivos de Big Data e Inteligencia Artificial.
            </p>
            <div style="margin-top: 60px; font-size: 14px; letter-spacing: 3px; color: #c9a75c; border-top: 1px solid rgba(201,167,92,0.3); padding-top: 20px; display: inline-block;">
                PITCH DECK CONFIDENCIAL PARA INVERSIONISTAS
            </div>
        </div>
    </div>

    <!-- SLIDE 2: EL PROBLEMA -->
    <div class="slide-page">
        <div class="content-layer" style="justify-content: flex-start; text-align: center; padding-top: 50px;">
            <h2 style="font-size: 36px;">I. LA FALLA DEL MERCADO TRADICIONAL</h2>
            <div class="grid-2 box">
                <div>
                    <h3 class="box-title" style="color: #ef4444;">Márgenes Asfixiados</h3>
                    <p class="box-text">Las agencias PYME en Cusco sobreviven con un margen bruto del 5%. Pierden un 20% en comisiones (Booking/OTA) y asumen el 100% del riesgo climático y bloqueos (SUTRAN).</p>
                </div>
                <div>
                    <h3 class="box-title" style="color: #ef4444;">Aislamiento Corporativo</h3>
                    <p class="box-text">Las grandes agencias europeas buscan operadores en Perú, pero exigen certificaciones ISO y normativas ESG. El 90% del turismo andino es informal y no califica para estos contratos millonarios.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- SLIDE 3: LA SOLUCIÓN -->
    <div class="slide-page">
        <img class="bg-img" src="{uri_b2b}">
        <div class="overlay"></div>
        <div class="content-layer" style="justify-content: flex-start; padding-top: 50px;">
            <h2 style="font-size: 36px; margin-bottom: 20px;">II. NUESTRA VENTAJA INJUSTA (DEEP TECH)</h2>
            <p style="font-size: 18px;">Pampa Ñusta es un <strong style="color: #c9a75c;">Holding Tecnológico (B2B)</strong> disfrazado de turismo. No competimos por turistas, administramos la logística de quienes los traen.</p>
            
            <div class="grid-3">
                <div class="box" style="padding: 20px;">
                    <h4 class="box-title">Dynamic Pricing</h4>
                    <p class="box-text">Nuestra IA (TimesFM) cruza costos del Petróleo y clima para subir precios en picos de demanda. Cero pérdidas.</p>
                </div>
                <div class="box" style="padding: 20px;">
                    <h4 class="box-title">Escudo ESG / ISO</h4>
                    <p class="box-text">Asumimos la formalización. Cumplimos los estándares europeos para absorber los contratos mayoristas.</p>
                </div>
                <div class="box" style="padding: 20px;">
                    <h4 class="box-title">Cierre Autónomo</h4>
                    <p class="box-text">Base de datos vectorial (Qdrant) que atiende a turistas por WhatsApp, cerrando ventas 24/7.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- SLIDE 4: BUSINESS MODEL -->
    <div class="slide-page">
        <div class="content-layer" style="justify-content: flex-start; padding-top: 50px;">
            <h2 style="font-size: 36px;">III. CÓMO HACEMOS DINERO (REVENUE)</h2>
            <div class="box" style="margin-top: 40px;">
                <div class="grid-2" style="margin-top: 0;">
                    <div>
                        <h3 class="box-title" style="color: #10b981; font-size: 28px;">B2B Franchising</h3>
                        <p class="box-text">Alineamos a pequeñas agencias locales. Ellos venden, nosotros operamos su logística. Les cobramos un porcentaje fijo sobre el costo operativo. Es un modelo SaaS aplicado al mundo físico.</p>
                    </div>
                    <div>
                        <h3 class="box-title" style="color: #3b82f6; font-size: 28px;">B2C High-Ticket</h3>
                        <p class="box-text">Turismo vivencial místico de ultra-lujo. Vendemos directamente al turista corporativo/europeo experiencias inmersivas que no se pueden replicar, con márgenes operativos del +60%.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- SLIDE 5: TAM -->
    <div class="slide-page">
        <img class="bg-img" src="{uri_traction}">
        <div class="overlay"></div>
        <div class="content-layer" style="justify-content: center;">
            <h2 style="font-size: 36px;">IV. TAM & ESCALABILIDAD</h2>
            <div class="grid-3" style="margin-top: 50px;">
                <div>
                    <div class="metric-val">$4.2B</div>
                    <div class="metric-lbl">Mercado Turístico Perú</div>
                </div>
                <div>
                    <div class="metric-val">3.5M</div>
                    <div class="metric-lbl">Llegadas Internacionales</div>
                </div>
                <div>
                    <div class="metric-val">+45%</div>
                    <div class="metric-lbl">Crecimiento Post-Pandemia</div>
                </div>
            </div>
            <div class="box" style="margin-top: 60px; text-align: left;">
                <p class="box-text" style="font-size: 16px;"><strong style="color: #c9a75c;">La Escala:</strong> Al controlar la base de datos y la logística, Pampa Ñusta no escala construyendo hoteles. Escala absorbiendo la capacidad instalada de terceros mediante contratos inteligentes de riesgo mitigado.</p>
            </div>
        </div>
    </div>

    <!-- SLIDE 6: CIERRE -->
    <div class="slide-page">
        <div class="content-layer" style="justify-content: center; align-items: center;">
            <h2 style="font-size: 36px;">"Lo que la máquina no puede replicar"</h2>
            <p style="font-size: 22px; max-width: 800px; margin: 40px auto; line-height: 1.6; font-weight: 300;">
                La IA organizará los viajes a la velocidad de la luz, pero los humanos de alto patrimonio siempre pagarán fortunas por lo único que un algoritmo no tiene: <strong style="color: #ffffff;">Autenticidad y Conexión Espiritual.</strong>
            </p>
            <div style="margin-top: 50px; padding: 20px 40px; border: 2px solid #c9a75c;">
                <h3 style="margin-bottom: 10px; font-size: 28px;">ÚNETE A LA MATRIZ</h3>
                <p style="font-size: 16px; color: #9ca3af;">Ronda Semilla // 2026</p>
            </div>
        </div>
    </div>

</body>
</html>
"""

async def generate_pitch_pdf():
    print("Generando PDF de Presentación (Modo Landscape Perfecto)...")
    html_path = os.path.abspath("temp_pitch_landscape.html")
    pdf_path = os.path.abspath("Pitch_Deck_Pampa_Nusta_Final.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(f"file:///{html_path}")
        await page.wait_for_timeout(2000) 
        
        await page.pdf(
            path=pdf_path,
            width="1123px",
            height="794px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            display_header_footer=False
        )
        
        await browser.close()
        
    if os.path.exists(html_path):
        os.remove(html_path)
        
    print(f"PDF Pitch Deck Landscape generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_pitch_pdf())
    except Exception as e:
        print(e)
