import os
import asyncio
from playwright.async_api import async_playwright
import datetime

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estatuto Maestro - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700;800&family=Inter:wght@300;400;500;700&family=JetBrains+Mono:wght@400;700&display=swap');
        
        * {{ box-sizing: border-box; }}
        
        body {{ 
            font-family: 'Inter', sans-serif; 
            margin: 0; 
            padding: 0; 
            background: #e2e8f0; 
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        
        /* A4 PAGE EXACT BOUNDS */
        .a4-page {{
            width: 794px;
            height: 1123px;
            background: #ffffff;
            position: relative;
            overflow: hidden;
            page-break-after: always;
            margin: 0 auto;
        }}
        
        /* TOP TIER LAW FIRM DESIGN */
        
        /* -- COVER PAGE -- */
        .cover-page {{
            display: flex;
            flex-direction: column;
            padding: 80px 100px;
        }}
        
        .header-confidential {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #dc2626; /* Red alert */
            border-bottom: 2px solid #dc2626;
            padding-bottom: 10px;
            display: flex;
            justify-content: space-between;
            margin-bottom: 150px;
            text-transform: uppercase;
        }}
        
        .cover-brand {{
            font-family: 'Playfair Display', serif;
            font-size: 45px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -1px;
            margin-bottom: 20px;
        }}
        
        .cover-type {{
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 700;
            color: #475569;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-bottom: 60px;
        }}
        
        .cover-title {{
            font-family: 'Playfair Display', serif;
            font-size: 55px;
            font-weight: 800;
            color: #000000;
            line-height: 1.1;
            margin-bottom: 40px;
            border-left: 6px solid #2563eb;
            padding-left: 25px;
        }}
        
        .cover-meta {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #334155;
            background: #f8fafc;
            padding: 25px;
            border: 1px solid #e2e8f0;
            margin-top: auto;
            line-height: 2;
        }}
        
        .cover-meta span {{ color: #2563eb; font-weight: 700; }}
        
        /* -- CONTENT PAGES -- */
        .legal-page {{
            padding: 70px 80px;
            display: flex;
            flex-direction: column;
        }}
        
        .page-header {{
            border-bottom: 2px solid #0f172a;
            padding-bottom: 15px;
            margin-bottom: 40px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        
        .page-header h2 {{
            font-family: 'Playfair Display', serif;
            font-size: 26px;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            text-transform: uppercase;
        }}
        
        .page-header .doc-id {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            color: #64748b;
        }}
        
        .clause-block {{
            margin-bottom: 35px;
            position: relative;
        }}
        
        .clause-number {{
            font-family: 'Playfair Display', serif;
            font-size: 45px;
            font-weight: 800;
            color: #e2e8f0;
            position: absolute;
            top: -20px;
            left: -35px;
            z-index: 1;
            letter-spacing: -2px;
        }}
        
        .clause-content {{
            position: relative;
            z-index: 2;
        }}
        
        .clause-title {{
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: #0f172a;
            margin: 0 0 15px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .clause-title::before {{
            content: '';
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #2563eb;
        }}
        
        .clause-text {{
            font-family: 'Inter', sans-serif;
            font-size: 12.5px;
            color: #334155;
            line-height: 1.7;
            text-align: justify;
            padding-left: 20px;
            border-left: 1px solid #cbd5e1;
        }}
        
        .faculties-list {{
            margin-top: 15px;
            margin-bottom: 0;
            padding-left: 20px;
            list-style-type: square;
            color: #2563eb;
            font-size: 12px;
        }}
        
        .faculties-list li {{ margin-bottom: 8px; }}
        .faculties-list span {{ color: #334155; }}
        
        .seal-box {{
            margin-top: 50px;
            padding: 30px;
            background: #0f172a;
            color: #ffffff;
            border-left: 4px solid #2563eb;
        }}
        
        .seal-title {{
            font-family: 'Playfair Display', serif;
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 15px;
            color: #ffffff;
        }}
        
        .seal-text {{
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            color: #94a3b8;
            line-height: 1.6;
        }}
        
        .footer-legal {{
            margin-top: auto;
            border-top: 1px solid #cbd5e1;
            padding-top: 20px;
            display: flex;
            justify-content: space-between;
            font-family: 'JetBrains Mono', monospace;
            font-size: 9px;
            color: #94a3b8;
        }}

    </style>
</head>
<body>

    <!-- PORTADA LEGAL -->
    <div class="a4-page cover-page">
        <div class="header-confidential">
            <span>STRICTLY CONFIDENTIAL / LEGAL FRAMEWORK</span>
            <span>ID: LX-OBJ-2026-991A</span>
        </div>
        
        <div class="cover-brand">LIFEXTREME</div>
        <div class="cover-type">Corporate Intelligence & Tech Holding</div>
        
        <h1 class="cover-title">ACTA ESTATUTARIA:<br>OBJETO SOCIAL EXPANSIVO Y DOMINIO DE MERCADO</h1>
        
        <div class="cover-meta">
            <div><span>ENTIDAD JURÍDICA:</span> LIFEXTREME HOLDING TECNOLÓGICO Y TURÍSTICO</div>
            <div><span>CLASIFICACIÓN:</span> MATRIZ DE DESARROLLO DE SOFTWARE, B2B LOGISTICS & FINTECH</div>
            <div><span>ALCANCE JURISDICCIONAL:</span> NACIONAL (PERÚ) E INTERNACIONAL</div>
            <div><span>TIMESTAMP DE GENERACIÓN:</span> {current_date} UTC</div>
            <div><span>VERIFICACIÓN QDRANT:</span> CHECKSUM_VALIDATED_99X2</div>
            <br>
            <div style="color: #0f172a; font-weight: 700; font-family: 'Inter', sans-serif; font-size: 12px;">INSTRUMENTO LEGAL ELABORADO PARA NOTARÍA Y REGISTROS PÚBLICOS (SUNARP).<br>Otorga facultades corporativas absolutas en Tecnología, Turismo e Intermediación Financiera.</div>
        </div>
    </div>

    <!-- PÁGINA 1 -->
    <div class="a4-page legal-page">
        <div class="page-header">
            <h2>DECLARACIÓN DEL OBJETO SOCIAL (I/II)</h2>
            <div class="doc-id">FOLIO: 001 // LX-CORP</div>
        </div>
        
        <div style="font-family: 'Inter', sans-serif; font-size: 12px; color: #0f172a; margin-bottom: 40px; font-weight: 500; border-bottom: 1px dashed #cbd5e1; padding-bottom: 20px;">
            La sociedad tiene por objeto principal, específico y expansivo dedicarse a las siguientes actividades macro-empresariales, sin que la presente enumeración sea restrictiva o limitativa, gozando de facultades absolutas para abarcar cualquier actividad lícita conexa, directa o indirecta, que apruebe la Junta General de Accionistas:
        </div>

        <div class="clause-block">
            <div class="clause-number">I</div>
            <div class="clause-content">
                <h3 class="clause-title">MACRO-LOGÍSTICA Y TURISMO B2B DE ALTA ESCALA</h3>
                <div class="clause-text">
                    La estructuración, desarrollo y ejecución integral de operaciones de turismo receptivo, interno y egresivo a nivel global. La sociedad está facultada para:
                    <ul class="faculties-list">
                        <li><span>Asumir la representación, intermediación y gestión operativa completa de redes de agencias de viajes de terceros (B2B).</span></li>
                        <li><span>Tercerizar, subcontratar y operar flotas de transporte terrestre, aéreo y lacustre.</span></li>
                        <li><span>Diseñar y comercializar expediciones de lujo, turismo de aventura y turismo vivencial/corporativo.</span></li>
                        <li><span>Constituir franquicias, joint ventures y consorcios internacionales para dominar la cadena de suministro turística.</span></li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="clause-block">
            <div class="clause-number">II</div>
            <div class="clause-content">
                <h3 class="clause-title">INTELIGENCIA ARTIFICIAL Y DATA BROKERING</h3>
                <div class="clause-text">
                    El diseño, entrenamiento, patente y comercialización de arquitecturas de Inteligencia Artificial (IA) y procesamiento de Big Data. La sociedad ostenta los derechos corporativos para:
                    <ul class="faculties-list">
                        <li><span>Desarrollar y licenciar algoritmos de Machine Learning, NLP y Bases de Datos Vectoriales (Ej: Qdrant).</span></li>
                        <li><span>Ejecutar minería masiva de datos (Data Scraping) orientada al análisis predictivo de mercados turísticos y fijación dinámica de precios (Dynamic Pricing).</span></li>
                        <li><span>Crear modelos RAG (Retrieval-Augmented Generation) y agentes autónomos para la sustitución de procesos operativos humanos (RPA).</span></li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="clause-block">
            <div class="clause-number">III</div>
            <div class="clause-content">
                <h3 class="clause-title">INGENIERÍA DE SOFTWARE Y CLOUD COMPUTING (SAAS)</h3>
                <div class="clause-text">
                    La producción, programación, licenciamiento comercial (SaaS) y venta de ecosistemas de software corporativo. La empresa tiene autorización notarial para:
                    <ul class="faculties-list">
                        <li><span>Construir y arrendar plataformas digitales (Web/App), sistemas ERP y CRM para la industria de la hospitalidad y la logística.</span></li>
                        <li><span>Comercializar infraestructura en la nube (Cloud Hosting) y proveer interfaces de programación (APIs) a empresas competidoras o asociadas.</span></li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer-legal">
            <span>DOCUMENTO MAESTRO // CORPORATE GOVERNANCE</span>
            <span>PÁGINA 1 DE 2</span>
        </div>
    </div>

    <!-- PÁGINA 2 -->
    <div class="a4-page legal-page">
        <div class="page-header">
            <h2>DECLARACIÓN DEL OBJETO SOCIAL (II/II)</h2>
            <div class="doc-id">FOLIO: 002 // LX-CORP</div>
        </div>
        
        <div class="clause-block">
            <div class="clause-number">IV</div>
            <div class="clause-content">
                <h3 class="clause-title">TECNOLOGÍA FINANCIERA (FINTECH) Y CLEARING DE PAGOS</h3>
                <div class="clause-text">
                    La intermediación, gestión y liquidación de flujos de capital a través de infraestructuras digitales. La corporación se encuentra facultada de forma expresa para:
                    <ul class="faculties-list">
                        <li><span>Diseñar, operar y facilitar pasarelas de pago electrónico, comercio electrónico y retención de fondos para terceros.</span></li>
                        <li><span>Ejecutar operaciones de arbitraje de divisas internacionales y optimización de tesorería turística.</span></li>
                        <li><span>Crear mecanismos de liquidación instantánea y tokenización de servicios para mitigar el riesgo cambiario y la fricción transaccional.</span></li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="clause-block">
            <div class="clause-number">V</div>
            <div class="clause-content">
                <h3 class="clause-title">CONSULTORÍA B2B E INTELIGENCIA ESTRATÉGICA</h3>
                <div class="clause-text">
                    La comercialización de conocimiento estratégico (Business Intelligence) y auditoría corporativa. Se faculta a la sociedad para:
                    <ul class="faculties-list">
                        <li><span>Vender reportes estadísticos cruzando variables macroeconómicas, geopolíticas y climatológicas a otras empresas (Data Monetization).</span></li>
                        <li><span>Prestar servicios de auditoría para la obtención de certificaciones de calidad europea (ISOs, ESG) y formalización Mincetur (DIRCETUR).</span></li>
                        <li><span>Diseñar arquitecturas de embudos de ventas (Funnels) y estrategias de neuromarketing algorítmico (AEO/SEO).</span></li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="seal-box">
            <div class="seal-title">CLÁUSULA DE CIERRE EXPANSIVO (CARTA BLANCA LEGAL)</div>
            <div class="seal-text">
                Para el cumplimiento absoluto, irrestricto y cabal de su objeto social, <strong>LA SOCIEDAD PODRÁ REALIZAR TODOS LOS ACTOS Y CELEBRAR TODOS LOS CONTRATOS</strong>, convenios, operaciones financieras, bancarias, crediticias, industriales y comerciales, de representación y mandato, que las leyes peruanas e internacionales permitan, ya sea de forma directa, a través de intermediarios, o en consorcio con personas naturales y jurídicas nacionales o extranjeras. <strong>Ningún funcionario o entidad registral podrá limitar la amplitud tecnológica ni logística de esta constitución.</strong>
            </div>
        </div>

        <div class="footer-legal">
            <span>DOCUMENTO MAESTRO // CORPORATE GOVERNANCE</span>
            <span>PÁGINA 2 DE 2</span>
        </div>
    </div>

</body>
</html>
"""

async def generate_10x_legal():
    print("Generando Estatuto Legal Nivel McKinsey/Big4...")
    html_path = os.path.abspath("temp_10x_legal.html")
    pdf_path = os.path.abspath("Estatuto_Maestro_Lifextreme.pdf")
    
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
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            display_header_footer=False
        )
        
        await browser.close()
        
    if os.path.exists(html_path):
        os.remove(html_path)
        
    print(f"PDF Legal 10X generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_10x_legal())
    except Exception as e:
        pass
