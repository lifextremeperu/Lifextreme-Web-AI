import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estatutos - Objeto Social Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
        
        body { 
            font-family: 'Times New Roman', serif; 
            margin: 0; 
            padding: 50px 80px; 
            background: #ffffff; 
            color: #000000; 
            font-size: 14px; 
            line-height: 1.6;
            text-align: justify;
        }
        
        h1 {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            text-decoration: underline;
            margin-bottom: 30px;
        }
        
        h2 {
            font-size: 14px;
            font-weight: bold;
            margin-top: 25px;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        
        .meta {
            margin-bottom: 40px;
            font-weight: bold;
        }
        
        p {
            margin-bottom: 15px;
        }
    </style>
</head>
<body>

    <h1>ESTATUTOS DE CONSTITUCIÓN: OBJETO SOCIAL EXPANSIVO Y TECNOLÓGICO</h1>
    
    <div class="meta">
        EMPRESA: LIFEXTREME<br>
        ENFOQUE JURÍDICO: Tecnología de Amplio Espectro, Turismo, Big Data & Logística.
    </div>

    <h2>ARTÍCULO: DEL OBJETO SOCIAL</h2>
    <p>La sociedad tiene por objeto principal y específico dedicarse a las siguientes actividades, sin que esta enumeración sea limitativa, pudiendo abarcar cualquier actividad lícita conexa, directa o indirecta, que apruebe la Junta General:</p>

    <h2>1. OPERACIONES LOGÍSTICAS Y TURISMO ESCALABLE (B2B Y B2C)</h2>
    <p>La prestación de servicios integrales de turismo receptivo, interno y egresivo. El diseño, operación, comercialización y ejecución de paquetes turísticos, expediciones, turismo de aventura, turismo vivencial y corporativo. La representación, intermediación y gestión de redes de agencias de viajes (B2B), asumiendo la tercerización operativa, logística y de transporte terrestre de pasajeros a nivel nacional e internacional. La suscripción de alianzas estratégicas, consorcios y franquicias con entidades nacionales y extranjeras para la explotación de la cadena de valor turística.</p>

    <h2>2. INTELIGENCIA ARTIFICIAL, BIG DATA Y DESARROLLO TECNOLÓGICO</h2>
    <p>La investigación, desarrollo, implementación y comercialización de sistemas de Inteligencia Artificial (IA), aprendizaje automático (Machine Learning), procesamiento de lenguaje natural (NLP) y bases de datos vectoriales. El procesamiento masivo de datos (Big Data) para el análisis predictivo de mercados, comportamiento del consumidor y fijación dinámica de precios (Dynamic Pricing). El diseño, arquitectura y mantenimiento de modelos de Recuperación Aumentada por Generación (RAG), motores de búsqueda, automatización de procesos robóticos (RPA) y agentes autónomos.</p>

    <h2>3. DESARROLLO DE SOFTWARE, SAAS Y PLATAFORMAS DIGITALES</h2>
    <p>El desarrollo, programación, licenciamiento y venta de software, aplicaciones móviles, plataformas web y sistemas de planificación de recursos empresariales (ERP) o gestión de relaciones con clientes (CRM). La provisión de software como servicio (SaaS) y computación en la nube (Cloud Computing). La creación, gestión y monetización de interfaces de programación de aplicaciones (APIs), bases de datos y ecosistemas digitales orientados a la gestión hotelera, transporte, logística y turismo.</p>

    <h2>4. CONSULTORÍA EMPRESARIAL E INTELIGENCIA DE NEGOCIOS (BUSINESS INTELLIGENCE)</h2>
    <p>La prestación de servicios de consultoría integral en transformación digital, estrategia corporativa, auditoría de procesos y marketing científico. El análisis estadístico, cruce de variables macroeconómicas, geopolíticas y climatológicas para la emisión de reportes de Inteligencia de Negocios orientados a la optimización financiera de empresas de terceros. El asesoramiento legal, comercial y técnico para la obtención de certificaciones de calidad (ISOs, DIRCETUR, ESG) por parte de agencias asociadas.</p>

    <h2>5. TECNOLOGÍA FINANCIERA (FINTECH), E-COMMERCE Y MEDIOS DE PAGO</h2>
    <p>La gestión, intermediación y facilitación de pasarelas de pago electrónico, comercio electrónico (E-commerce) y transacciones digitales internacionales. La estructuración de sistemas de arbitraje de divisas, gestión de activos digitales y tokenización de servicios. La creación de plataformas para la liquidación instantánea de reservas, gestión de riesgo financiero y optimización del costo de adquisición de clientes (CAC) mediante canales digitales.</p>

    <h2>6. MARKETING CUANTITATIVO Y NEUROMARKETING</h2>
    <p>La explotación de servicios de publicidad digital, posicionamiento en motores de búsqueda orientados a Inteligencia Artificial (AEO - Answer Engine Optimization) y SEO tradicional. El diseño de campañas de neuromarketing basadas en datos biométricos y conductuales, gestión de redes sociales, alianzas con creadores de contenido (Influencers) y automatización del embudo de ventas (Funnels) para la maximización del valor del ciclo de vida del cliente (LTV).</p>

    <p><strong>Cláusula de Cierre Expansivo:</strong> Para el cumplimiento de su objeto social, la sociedad podrá realizar todos los actos y celebrar todos los contratos, convenios y operaciones financieras, industriales y comerciales, de representación y mandato, que las leyes peruanas e internacionales permitan, ya sea de forma directa, a través de terceros o en asociación con personas naturales o jurídicas nacionales o extranjeras.</p>

</body>
</html>
"""

async def generate_legal_pdf():
    print("Generando PDF Legal del Objeto Social...")
    html_path = os.path.abspath("temp_legal.html")
    pdf_path = os.path.abspath("Objeto_Social_Lifextreme.pdf")
    
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
        
    print(f"PDF Legal generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_legal_pdf())
    except Exception as e:
        pass
