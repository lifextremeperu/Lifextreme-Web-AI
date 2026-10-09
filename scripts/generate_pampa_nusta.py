import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

img_community = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\amazon_community_tourism_1791572171378.jpg"
uri_community = "file:///" + img_community.replace("\\", "/")

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Memorándum de Inversión - Pampa Ñusta</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Montserrat:wght@300;400;600;800&display=swap');
        
        * {{ box-sizing: border-box; }}
        
        body {{ 
            font-family: 'Montserrat', sans-serif; 
            margin: 0; 
            padding: 0; 
            background: #111512; /* Fondo muy oscuro, casi negro bosque */
            color: #e5e7eb;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        
        /* DIMENSIONES A4 EXACTAS PARA PDF PERFECTO */
        .a4-page {{
            width: 794px;
            height: 1123px;
            background: #0f1411; /* Color base profundo */
            position: relative;
            overflow: hidden;
            page-break-after: always;
            margin: 0 auto;
        }}
        
        /* TEXTURAS Y BORDES MÍSTICOS/CORPORATIVOS */
        .a4-page::before {{
            content: '';
            position: absolute;
            top: 25px; bottom: 25px; left: 25px; right: 25px;
            border: 1px solid rgba(201, 167, 92, 0.3); /* Borde dorado sutil */
            pointer-events: none;
            z-index: 10;
        }}
        
        /* PORTADA */
        .cover-img {{
            width: 100%;
            height: 55%;
            object-fit: cover;
            position: absolute;
            top: 0; left: 0;
            opacity: 0.85;
            mask-image: linear-gradient(to bottom, black 50%, transparent 100%);
            -webkit-mask-image: linear-gradient(to bottom, black 50%, transparent 100%);
        }}
        
        .cover-content {{
            position: absolute;
            bottom: 0; left: 0;
            width: 100%;
            height: 50%;
            padding: 40px 60px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            z-index: 20;
        }}
        
        .project-name {{
            font-family: 'Cinzel', serif;
            color: #c9a75c; /* Oro viejo */
            font-size: 20px;
            letter-spacing: 6px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .pitch-title {{
            font-family: 'Cinzel', serif;
            font-size: 50px;
            color: #ffffff;
            line-height: 1.1;
            margin: 0 0 20px 0;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        }}
        
        .pitch-subtitle {{
            font-size: 13px;
            font-weight: 300;
            color: #d1d5db;
            line-height: 1.8;
            max-width: 90%;
            border-left: 2px solid #c9a75c;
            padding-left: 15px;
            margin-bottom: 30px;
        }}
        
        .investor-tag {{
            font-family: 'Cinzel', serif;
            font-size: 11px;
            color: #c9a75c;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-top: 1px solid rgba(201, 167, 92, 0.3);
            padding-top: 15px;
        }}
        
        /* PAGINAS DE CONTENIDO */
        .inner-page {{
            padding: 60px;
            display: flex;
            flex-direction: column;
            height: 100%;
        }}
        
        .header-mystic {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 1px solid rgba(201, 167, 92, 0.4);
            padding-bottom: 15px;
            margin-bottom: 35px;
        }}
        
        .header-mystic h2 {{
            font-family: 'Cinzel', serif;
            font-size: 26px;
            color: #c9a75c;
            margin: 0;
            letter-spacing: 2px;
        }}
        
        .grid-blocks {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 25px;
            flex-grow: 1;
        }}
        
        .block {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 25px;
            display: flex;
            gap: 20px;
        }}
        
        .block-icon {{
            font-family: 'Cinzel', serif;
            font-size: 24px;
            color: #c9a75c;
            font-weight: 700;
        }}
        
        .block-title {{
            font-family: 'Cinzel', serif;
            font-size: 16px;
            color: #ffffff;
            margin: 0 0 10px 0;
            letter-spacing: 1px;
        }}
        
        .block-text {{
            font-size: 12px;
            color: #9ca3af;
            line-height: 1.6;
            margin: 0 0 15px 0;
            font-weight: 300;
        }}
        
        .block-action {{
            background: rgba(201, 167, 92, 0.1);
            border-left: 3px solid #c9a75c;
            padding: 10px 15px;
            font-size: 11px;
            color: #e5e7eb;
        }}
        
        .block-action strong {{
            color: #c9a75c;
            text-transform: uppercase;
            font-family: 'Cinzel', serif;
            letter-spacing: 1px;
        }}
        
        .footer-mystic {{
            margin-top: auto;
            border-top: 1px solid rgba(201, 167, 92, 0.4);
            padding-top: 15px;
            display: flex;
            justify-content: space-between;
            font-family: 'Cinzel', serif;
            font-size: 10px;
            color: #c9a75c;
            letter-spacing: 2px;
        }}
        
        .quote-box {{
            text-align: center;
            padding: 40px;
            margin: auto 0;
        }}
        
        .quote-text {{
            font-family: 'Cinzel', serif;
            font-size: 22px;
            color: #ffffff;
            line-height: 1.4;
            margin-bottom: 20px;
        }}
        
        .quote-author {{
            font-size: 12px;
            color: #c9a75c;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
    </style>
</head>
<body>

    <!-- PORTADA -->
    <div class="a4-page">
        <img class="cover-img" src="{uri_community}" alt="Comunidad Andina">
        <div class="cover-content">
            <div class="project-name">PROYECTO PAMPA ÑUSTA</div>
            <h1 class="pitch-title">EL ALMA DE LOS ANDES,<br>LA MENTE DE SILICON VALLEY</h1>
            <div class="pitch-subtitle">
                Conectamos la profunda sabiduría ancestral y el turismo comunitario inmersivo con el análisis matemático de millones de datos globales. Este es el memorándum oficial para transformar nuestra sagrada tierra en el activo más rentable, seguro y humano del mercado internacional.
            </div>
            <div class="investor-tag">CONFIDENTIAL PITCH DECK // GLOBAL INVESTORS & PARTNERS</div>
        </div>
    </div>

    <!-- PÁGINA 1: CONOCIMIENTO Y VENTA -->
    <div class="a4-page inner-page">
        <div class="header-mystic">
            <h2>I. LA ALQUIMIA DEL VALOR (RENTABILIDAD)</h2>
            <span>01</span>
        </div>
        
        <div class="grid-blocks">
            <div class="block">
                <div class="block-icon">❂</div>
                <div>
                    <h3 class="block-title">El Tiempo y la Urgencia (Precios Dinámicos)</h3>
                    <p class="block-text">Así como la naturaleza tiene ciclos, el mercado tiene ritmos. Nuestros algoritmos (TimesFM) confirman que el forastero siente urgencia faltando 3 días para su viaje. Su necesidad de asegurar el espacio elimina la objeción del precio.</p>
                    <div class="block-action"><strong>EL RITO COMERCIAL:</strong> Aumentar el valor del servicio en 15% a última hora. El turista no cuestiona; agradece haber encontrado refugio.</div>
                </div>
            </div>
            
            <div class="block">
                <div class="block-icon">🜂</div>
                <div>
                    <h3 class="block-title">La Comunicación Directa (Cero Fricción)</h3>
                    <p class="block-text">El hombre moderno está cansado de la burocracia digital (formularios largos). Las estadísticas muestran que el chat instantáneo eleva la dopamina y la confianza, llevando el cierre de ventas del 8% al 35%.</p>
                    <div class="block-action"><strong>EL RITO COMERCIAL:</strong> Conversar de forma humana por WhatsApp y enviar un enlace de pago instantáneo.</div>
                </div>
            </div>
            
            <div class="block">
                <div class="block-icon">⚖</div>
                <div>
                    <h3 class="block-title">El Equilibrio de las Energías (Petróleo y Divisas)</h3>
                    <p class="block-text">Estamos conectados al mundo. Si el combustible global sube, el forastero promedio sufre. Si el Euro se fortalece, el europeo siente abundancia. La Inteligencia de Datos nos dice exactamente cuándo actuar.</p>
                    <div class="block-action"><strong>EL RITO COMERCIAL:</strong> Enfocar los recursos y anuncios publicitarios hacia Europa únicamente en los días de mayor abundancia cambiaria.</div>
                </div>
            </div>
        </div>
        
        <div class="footer-mystic">
            <span>LIFEXTREME BIG DATA // PAMPA ÑUSTA</span>
            <span>MEMORÁNDUM CORPORATIVO</span>
        </div>
    </div>

    <!-- PÁGINA 2: PROTECCIÓN Y ESTRUCTURA -->
    <div class="a4-page inner-page">
        <div class="header-mystic">
            <h2>II. EL ESCUDO Y LA RAÍZ (FORMALIZACIÓN)</h2>
            <span>02</span>
        </div>
        
        <div class="grid-blocks">
            <div class="block">
                <div class="block-icon">♅</div>
                <div>
                    <h3 class="block-title">Las Raíces Legales (Certificación Mincetur / ISOs)</h3>
                    <p class="block-text">Para que un árbol crezca alto, sus raíces deben ser profundas y formales. Los grandes inversionistas y corporaciones de Europa exigen certificaciones estrictas (Normas ESG, ISO 9001) para enviar a sus viajeros. La informalidad es debilidad.</p>
                    <div class="block-action"><strong>LA ESTRUCTURA CORPORATIVA:</strong> Iniciar la certificación DIRCETUR e ISO. Es la llave maestra para abrir bóvedas de contratos internacionales.</div>
                </div>
            </div>
            
            <div class="block">
                <div class="block-icon">𓂀</div>
                <div>
                    <h3 class="block-title">El Ojo que Todo lo Ve (Anticipación Climatológica)</h3>
                    <p class="block-text">El clima de los Andes es indomable. Una lluvia imprevista obliga a las agencias comunes a devolver el dinero, desangrando sus ahorros. Nuestra tecnología cruza datos satelitales en tiempo real para nunca retroceder, solo desviarnos.</p>
                    <div class="block-action"><strong>LA ESTRUCTURA CORPORATIVA:</strong> Redirigir la ruta del turista hacia zonas soleadas (Valle Sur). Cero reembolsos, cero pérdidas.</div>
                </div>
            </div>
            
            <div class="block">
                <div class="block-icon">❖</div>
                <div>
                    <h3 class="block-title">La Semilla que se Expande (Retención LTV)</h3>
                    <p class="block-text">Quien pisa esta tierra, siempre busca más. El turista que visita el Cusco, inevitablemente buscará la Amazonía. Dejar que se vaya a otra agencia es desperdiciar la semilla plantada.</p>
                    <div class="block-action"><strong>LA ESTRUCTURA CORPORATIVA:</strong> Crear alianzas B2B con la Selva. Recomendar a nuestro turista meses después y cobrar dividendos pasivos perpetuos.</div>
                </div>
            </div>
        </div>
        
        <div class="footer-mystic">
            <span>LIFEXTREME BIG DATA // PAMPA ÑUSTA</span>
            <span>MEMORÁNDUM CORPORATIVO</span>
        </div>
    </div>

    <!-- PÁGINA 3: EL ESPÍRITU Y LA IA -->
    <div class="a4-page inner-page">
        <div class="header-mystic">
            <h2>III. LO QUE LA MÁQUINA NO PUEDE ROBAR</h2>
            <span>03</span>
        </div>
        
        <div class="quote-box">
            <div class="quote-text">"Los algoritmos de Silicon Valley pueden predecir precios y comprar pasajes de avión a la velocidad de la luz. Pero jamás podrán mirar a los ojos a un forastero, jamás podrán tejer lana de alpaca bajo el sol, y jamás podrán abrazar."</div>
            <div class="quote-author">EL VALOR INMUTABLE DE PAMPA ÑUSTA</div>
        </div>
        
        <div class="grid-blocks" style="flex-grow: 0; margin-bottom: 40px;">
            <div class="block" style="background: rgba(201, 167, 92, 0.05); border-color: #c9a75c;">
                <div class="block-icon">⟁</div>
                <div>
                    <h3 class="block-title">Turismo Vivencial Auténtico (El Escudo Definitivo)</h3>
                    <p class="block-text">En un mundo devorado por la Inteligencia Artificial (ChatGPT, Expedia, Robots), el verdadero "Lujo" ya no son las cadenas de hoteles de cinco estrellas. El turista de alto patrimonio paga fortunas incalculables por "Humanidad Auténtica": convivir, comer y dormir con nuestra comunidad. Ese es nuestro monopolio.</p>
                    <div class="block-action"><strong>EL MANDATO FINAL:</strong> Lifextreme asume el peso tecnológico, logístico y de Big Data. La comunidad y la agencia asumen el contacto humano. Una alianza invencible.</div>
                </div>
            </div>
        </div>
        
        <div class="footer-mystic">
            <span>LIFEXTREME BIG DATA // PAMPA ÑUSTA</span>
            <span>MEMORÁNDUM CORPORATIVO</span>
        </div>
    </div>

</body>
</html>
"""

async def generate_pampa_nusta_pitch_pdf():
    print("Preparando Pitch Deck Corporativo y Místico (Pampa Ñusta)...")
    html_path = os.path.abspath("temp_pampa_pitch.html")
    pdf_path = os.path.abspath("Pampa_Nusta_Inversion_Corporativa.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(f"file:///{html_path}")
        await page.wait_for_timeout(2000) 
        
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            display_header_footer=False
        )
        
        await browser.close()
        
    if os.path.exists(html_path):
        os.remove(html_path)
        
    print(f"PDF Pitch Deck generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_pampa_nusta_pitch_pdf())
    except Exception as e:
        pass
