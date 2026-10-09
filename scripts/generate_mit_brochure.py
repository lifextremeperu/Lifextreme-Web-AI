import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

img_tourist = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\cusco_business_tourist_1791572148790.jpg"
img_community = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\amazon_community_tourism_1791572171378.jpg"
img_b2b = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\corporate_travel_pyme_1791572199630.jpg"

uri_tourist = "file:///" + img_tourist.replace("\\", "/")
uri_community = "file:///" + img_community.replace("\\", "/")
uri_b2b = "file:///" + img_b2b.replace("\\", "/")

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>MIT Level Brochure - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&family=IBM+Plex+Mono:wght@400;600&display=swap');
        
        * {{ box-sizing: border-box; }}
        
        body {{ 
            font-family: 'Inter', sans-serif; 
            margin: 0; 
            padding: 0; 
            background: #e5e5e5; /* Solo fondo del navegador, el PDF solo agarra las pages */
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        
        /* DIMENSIONES A4 EXACTAS PARA EVITAR ESPACIOS EN BLANCO */
        .a4-page {{
            width: 794px;
            height: 1123px;
            background: #ffffff;
            position: relative;
            overflow: hidden;
            page-break-after: always;
            margin: 0 auto;
        }}
        
        /* PORTADA */
        .cover-img {{
            width: 100%;
            height: 65%;
            object-fit: cover;
            position: absolute;
            top: 0; left: 0;
        }}
        
        .cover-text-box {{
            position: absolute;
            bottom: 0; left: 0;
            width: 100%;
            height: 35%;
            background: #000000;
            color: white;
            padding: 40px 50px;
        }}
        
        .mit-badge {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            color: #00ff88;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 20px;
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
            display: inline-block;
        }}
        
        .cover-title {{
            font-size: 46px;
            font-weight: 900;
            line-height: 1.05;
            margin: 0 0 15px 0;
            letter-spacing: -1.5px;
        }}
        
        .cover-subtitle {{
            font-size: 14px;
            color: #a3a3a3;
            max-width: 80%;
            line-height: 1.6;
        }}
        
        /* PAGINAS DE CONTENIDO */
        .content-page {{
            padding: 50px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        
        .page-header {{
            border-bottom: 3px solid #000;
            padding-bottom: 15px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        
        .page-header h2 {{
            margin: 0;
            font-size: 28px;
            font-weight: 900;
            letter-spacing: -1px;
            color: #000;
        }}
        
        .page-header .phase-tag {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 12px;
            background: #000;
            color: #fff;
            padding: 5px 10px;
        }}
        
        .module-list {{
            display: flex;
            flex-direction: column;
            gap: 25px;
            flex-grow: 1;
        }}
        
        .module-row {{
            display: flex;
            gap: 20px;
            border-top: 1px solid #e5e5e5;
            padding-top: 20px;
        }}
        
        .module-number {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 24px;
            font-weight: 600;
            color: #000;
            width: 40px;
        }}
        
        .module-content {{
            flex: 1;
        }}
        
        .module-title {{
            font-size: 18px;
            font-weight: 800;
            margin: 0 0 8px 0;
            color: #000;
        }}
        
        .qdrant-tag {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 9px;
            color: #4b5563;
            background: #f3f4f6;
            padding: 3px 8px;
            margin-bottom: 10px;
            display: inline-block;
        }}
        
        .module-desc {{
            font-size: 12px;
            color: #374151;
            line-height: 1.5;
            margin-bottom: 12px;
        }}
        
        .benefit-box {{
            background: #000;
            color: #fff;
            padding: 10px 15px;
            font-size: 11px;
            border-left: 4px solid #00ff88;
        }}
        
        .benefit-box strong {{
            color: #00ff88;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 10px;
            text-transform: uppercase;
            display: block;
            margin-bottom: 3px;
        }}
        
        .footer {{
            border-top: 1px solid #000;
            padding-top: 15px;
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 10px;
            color: #000;
        }}
        
        /* PAGINAS CON IMAGEN (SPLIT) */
        .split-page {{
            display: flex;
            flex-direction: column;
        }}
        
        .split-top {{
            height: 45%;
            width: 100%;
            position: relative;
        }}
        
        .split-top img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .img-caption {{
            position: absolute;
            bottom: 0; left: 0;
            background: #000;
            color: #00ff88;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 10px;
            padding: 8px 15px;
        }}
        
        .split-bottom {{
            height: 55%;
            padding: 30px 50px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

    </style>
</head>
<body>

    <!-- PAGINA 1: PORTADA -->
    <div class="a4-page">
        <img class="cover-img" src="{uri_tourist}" alt="Turista">
        <div class="cover-text-box">
            <div class="mit-badge">LIFEXTREME BIG DATA INTELLIGENCE // RESEARCH REPORT</div>
            <h1 class="cover-title">LA VENTAJA ASIMÉTRICA:<br>CÓMO ESCALAR TU AGENCIA</h1>
            <div class="cover-subtitle">Procesamos 336,369 nodos de datos turísticos globales usando Qdrant (IA). Este reporte destila ese conocimiento matemático en 15 instrucciones ejecutivas simples para que el dueño de una PYME en Cusco multiplique su rentabilidad hoy mismo.</div>
        </div>
    </div>

    <!-- PAGINA 2: MODULOS 1 AL 4 -->
    <div class="a4-page content-page">
        <div>
            <div class="page-header">
                <h2>I. Optimización de Ingresos (Pricing & Macro)</h2>
                <div class="phase-tag">FASE 01</div>
            </div>
            
            <div class="module-list">
                <div class="module-row">
                    <div class="module-number">01</div>
                    <div class="module-content">
                        <div class="qdrant-tag">DATA.SOURCE: ALGORITMO TIMESFM / MODELO DE ESCASEZ</div>
                        <h3 class="module-title">Cobrar el "Impuesto a la Urgencia"</h3>
                        <div class="module-desc">Las matemáticas prueban que faltando 3 días para volar, el turista sufre FOMO (Miedo a quedarse sin cupo). Su voluntad de pago aumenta drásticamente porque su prioridad ya no es ahorrar, sino asegurar el servicio.</div>
                        <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Incrementa automáticamente tus precios un 15% a los clientes de última hora. Pagarán sin pedir rebajas.</div>
                    </div>
                </div>
                
                <div class="module-row">
                    <div class="module-number">02</div>
                    <div class="module-content">
                        <div class="qdrant-tag">DATA.SOURCE: NEUROMARKETING & TASAS DE FRICCIÓN</div>
                        <h3 class="module-title">Cierre Directo por WhatsApp (1-Clic)</h3>
                        <div class="module-desc">El análisis de conversión revela que los formularios web gigantes solo logran un 8% de cierre (alta fricción cognitiva). El chat de WhatsApp es inmediato y dispara la dopamina del consumidor.</div>
                        <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Elimina pasos. Envía un link de pago (Niubiz/Yape) por el chat. Multiplicarás el cierre al 35% el mismo día.</div>
                    </div>
                </div>
                
                <div class="module-row">
                    <div class="module-number">03</div>
                    <div class="module-content">
                        <div class="qdrant-tag">DATA.SOURCE: ARBITRAJE DE DIVISAS (BCE)</div>
                        <h3 class="module-title">Aprovechar los picos del Euro</h3>
                        <div class="module-desc">Existe una correlación directa entre la moneda y la demanda. Cuando el Euro se fortalece frente al Dólar, las búsquedas europeas de "Tours Perú" suben un 18% en 48 horas porque su liquidez aumenta.</div>
                        <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Inyecta tu presupuesto publicitario en Europa exclusivamente los días que el Euro amanezca en alza.</div>
                    </div>
                </div>
                
                <div class="module-row">
                    <div class="module-number">04</div>
                    <div class="module-content">
                        <div class="qdrant-tag">DATA.SOURCE: GEOPOLÍTICA & COMBUSTIBLE (JET-A1)</div>
                        <h3 class="module-title">El Petróleo dicta tu demanda</h3>
                        <div class="module-desc">Cusco no es una burbuja. Cuando ocurren crisis bélicas globales, el crudo sube y los tickets de avión encarecen. El turista de clase media cancela automáticamente su viaje a Sudamérica.</div>
                        <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Si las noticias avisan de petróleo caro, apaga tus anuncios para "mochileros" y enfócate solo en turistas VIP.</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <span>LIFEXTREME BIG DATA LABS</span>
            <span>PAGE // 02</span>
        </div>
    </div>

    <!-- PAGINA 3: IMAGEN B2B + MODULOS 5 AL 7 -->
    <div class="a4-page split-page">
        <div class="split-top">
            <img src="{uri_b2b}" alt="Reunión B2B Formal">
            <div class="img-caption">VISIÓN CORPORATIVA B2B // ALIANZAS GLOBALES</div>
        </div>
        <div class="split-bottom">
            <div>
                <div class="page-header" style="margin-bottom: 20px;">
                    <h2>II. Formalización y Guerra de Mercados</h2>
                    <div class="phase-tag">FASE 02</div>
                </div>
                
                <div class="module-list" style="gap: 15px;">
                    <div class="module-row" style="padding-top: 15px;">
                        <div class="module-number">05</div>
                        <div class="module-content">
                            <div class="qdrant-tag">DATA.SOURCE: AUDITORÍA DE MÁRGENES OPERATIVOS</div>
                            <h3 class="module-title">El Océano Rojo de la Plaza de Armas</h3>
                            <div class="module-desc">La guerra de precios masiva destruye la utilidad de una PYME dejándola en 5%. Empaquetar lujo privado dispara el margen líquido. Pelear por volumen es firmar la quiebra.</div>
                            <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Arma un Tour Privado a $150. Venderás 1 y ganarás lo mismo que peleando por 30 turistas baratos.</div>
                        </div>
                    </div>
                    
                    <div class="module-row" style="padding-top: 15px;">
                        <div class="module-number">06</div>
                        <div class="module-content">
                            <div class="qdrant-tag">DATA.SOURCE: LEGISLACIÓN EUROPEA (ESG)</div>
                            <h3 class="module-title">Los papeles en regla valen oro (ISOs)</h3>
                            <div class="module-desc">Las macro-agencias europeas no pueden subcontratar informalidad por leyes estrictas en sus países. Buscan agencias locales con Constancia Dircetur y normas ISO (9001/14001).</div>
                            <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Inicia el trámite de formalización turística. Es el escudo protector para ganar licitaciones B2B internacionales.</div>
                        </div>
                    </div>
                    
                    <div class="module-row" style="padding-top: 15px;">
                        <div class="module-number">07</div>
                        <div class="module-content">
                            <div class="qdrant-tag">DATA.SOURCE: AEO (ANSWER ENGINE OPTIMIZATION)</div>
                            <h3 class="module-title">Háblale a los Algoritmos de I.A.</h3>
                            <div class="module-desc">El SEO en Google está colapsando frente a herramientas de IA (ChatGPT, Perplexity) usadas para planear viajes. Las máquinas prefieren datos estructurados, preguntas y respuestas directas.</div>
                            <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Usa párrafos cortos y precisos en tu web. ChatGPT tomará tu data y te citará como fuente confiable gratis.</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer">
                <span>LIFEXTREME BIG DATA LABS</span>
                <span>PAGE // 03</span>
            </div>
        </div>
    </div>
    
    <!-- PAGINA 4: MODULOS 8 AL 11 -->
    <div class="a4-page content-page">
        <div>
            <div class="page-header">
                <h2>III. Retención de Capital y Marketing Táctico</h2>
                <div class="phase-tag">FASE 03</div>
            </div>
            
            <div class="module-list">
                <div class="module-row">
                    <div class="module-number">08</div>
                    <div class="module-content">
                        <div class="qdrant-tag">DATA.SOURCE: COSTO DE ADQUISICIÓN (CAC)</div>
                        <h3 class="module-title">Destruir el CAC con Micro-Influencers</h3>
                        <div class="module-desc">Pagarle a Meta Ads cuesta $45 USD por cliente. Invitar a creadores de TikTok jóvenes y extranjeros de nicho (10k-50k seguidores) baja el costo a casi $0. Sus comunidades copian todo lo que ven.</div>
                        <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Ofrece tours gratis a cambio de videos virales geolocalizados. Exposición global garantizada.</div>
                    </div>
                </div>
                
                <div class="module-row">
                    <div class="module-number">09</div>
                    <div class="module-content">
                        <div class="qdrant-tag">DATA.SOURCE: FUGA DE COMISIONES OTA</div>
                        <h3 class="module-title">Recuperación de Dinero Directo (D2C)</h3>
                        <div class="module-desc">Booking y Viator asfixian extrayendo el 20% de comisión. Las métricas confirman que el 65% de sus usuarios buscan la web oficial de tu PYME antes de pasar su tarjeta de crédito.</div>
                        <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Ofrece un "Traslado al Aeropuerto Gratis" en tu web si compran por WhatsApp. Salvarás ese 20% reteniendo el margen.</div>
                    </div>
                </div>
                
                <div class="module-row">
                    <div class="module-number">10</div>
                    <div class="module-content">
                        <div class="qdrant-tag">DATA.SOURCE: LIFETIME VALUE (LTV) MULTI-DESTINO</div>
                        <h3 class="module-title">Ingresos Pasivos a 6 Meses</h3>
                        <div class="module-desc">El ciclo del viajero prueba que tras visitar Cusco, es altamente probable que exploren la Selva (Iquitos/Tarapoto) en 1 o 2 años. El vínculo comercial no debe morir.</div>
                        <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Alíate con una PYME en la Amazonía. Escríbele a tus ex-clientes y recomienda a tu aliado a cambio del 10%.</div>
                    </div>
                </div>
                
                <div class="module-row">
                    <div class="module-number">11</div>
                    <div class="module-content">
                        <div class="qdrant-tag">DATA.SOURCE: LOGÍSTICA SENAMHI/SUTRAN</div>
                        <h3 class="module-title">El Algoritmo Anti-Reembolsos</h3>
                        <div class="module-desc">Una huelga campesina o nevada severa en Vinicunca causa reembolsos masivos (100% de fuga de caja chica). Operar de forma rígida es un suicidio financiero.</div>
                        <div class="benefit-box"><strong>💰 ACCIÓN RENTABLE:</strong> Si hay bloqueos, aplica "Flexibilidad Táctica". Desvía al turista al Valle Sur (sol garantizado). Cero devoluciones.</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <span>LIFEXTREME BIG DATA LABS</span>
            <span>PAGE // 04</span>
        </div>
    </div>

    <!-- PAGINA 5: IMAGEN COMUNIDAD + MODULOS 12 AL 15 -->
    <div class="a4-page split-page">
        <div class="split-top">
            <img src="{uri_community}" alt="Turismo Humano Auténtico">
            <div class="img-caption">EXPERIENCIA HUMANA // EL ESCUDO ANTI-ROBOTS</div>
        </div>
        <div class="split-bottom">
            <div>
                <div class="page-header" style="margin-bottom: 20px;">
                    <h2>IV. Expansión: Nuevos Horizontes</h2>
                    <div class="phase-tag">FASE 04</div>
                </div>
                
                <div class="module-list" style="gap: 12px;">
                    <div class="module-row" style="padding-top: 12px;">
                        <div class="module-number">12</div>
                        <div class="module-content">
                            <div class="qdrant-tag">DATA.SOURCE: CRECIMIENTO DE MICRO-NICHOS</div>
                            <h3 class="module-title">El Boom de las Mujeres Viajeras</h3>
                            <div class="module-desc">El nicho "Solo Female Travelers" experimenta un crecimiento de 400%. Ofrecer máxima seguridad y guías exclusivamente mujeres te garantiza liderazgo en un segmento sin competencia en Cusco.</div>
                        </div>
                    </div>
                    
                    <div class="module-row" style="padding-top: 12px;">
                        <div class="module-number">13</div>
                        <div class="module-content">
                            <div class="qdrant-tag">DATA.SOURCE: PSICOLOGÍA CORPORATIVA (BURNOUT)</div>
                            <h3 class="module-title">El Oro B2B Corporativo Peruano</h3>
                            <div class="module-desc">Las corporaciones en Lima pagan alto ticket anual para desconectar a sus gerentes con estrés crónico. Vender retiros B2B corporativos te dará ingresos sólidos en la temporada baja extranjera.</div>
                        </div>
                    </div>
                    
                    <div class="module-row" style="padding-top: 12px;">
                        <div class="module-number">14</div>
                        <div class="module-content">
                            <div class="qdrant-tag">DATA.SOURCE: INVERSIONES PENTUR Mincetur</div>
                            <h3 class="module-title">Anticiparse al Flujo Selvático</h3>
                            <div class="module-desc">Cusco entrará en saturación. Las proyecciones estatales a 2028 apuntan a inyectar capital en Amazonas y Ruta Moche. Operar con Lifextreme allí desde hoy te posiciona como pionero mañana.</div>
                        </div>
                    </div>
                    
                    <div class="module-row" style="padding-top: 12px;">
                        <div class="module-number">15</div>
                        <div class="module-content">
                            <div class="qdrant-tag">DATA.SOURCE: TENDENCIA GLOBAL ANTI-TECH</div>
                            <h3 class="module-title">Lo que la IA jamás podrá copiar</h3>
                            <div class="module-desc">Las supercomputadoras no pueden abrazar. El turista rico paga sumas exorbitantes por turismo vivencial puro (dormir y cocinar con una familia andina). Es una experiencia blindada contra el internet.</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer">
                <span>LIFEXTREME BIG DATA LABS</span>
                <span>PAGE // 05</span>
            </div>
        </div>
    </div>
    
    <!-- PAGINA 6: CONTRATAPA B2B -->
    <div class="a4-page" style="background: #000; color: white; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 100px;">
        <div style="width: 80px; height: 80px; border: 4px solid #00ff88; display: flex; justify-content: center; align-items: center; font-family: 'IBM Plex Mono'; font-size: 30px; font-weight: bold; margin-bottom: 40px; color: #00ff88;">LX</div>
        <h1 style="font-family: 'Playfair Display'; font-size: 45px; margin: 0 0 30px 0; line-height: 1.1;">TERCERIZA EL ESTRÉS.<br>MAXIMIZA EL INGRESO.</h1>
        <p style="font-size: 16px; color: #a3a3a3; max-width: 500px; line-height: 1.6; margin-bottom: 60px;">El dueño de una PYME que pasa las madrugadas coordinando logística está condenado a quebrar por agotamiento. <strong>Tu única función debe ser formalizar tu agencia, hablar con clientes y vender a Alto Ticket.</strong></p>
        
        <div style="border: 1px solid #333; padding: 40px; text-align: left; max-width: 500px;">
            <div style="font-family: 'IBM Plex Mono'; color: #00ff88; font-size: 12px; margin-bottom: 15px;">/// PROTOCOLO DE ALIANZA LIFEXTREME</div>
            <p style="margin: 0; font-size: 14px; line-height: 1.5; color: #fff;">Nosotros somos tu Departamento de Operaciones. Tú cierras la venta usando estos 15 datos científicos, y Lifextreme pondrá la camioneta y el guía en la puerta de tu cliente con precisión militar. Sin excusas. Sin estrés.</p>
        </div>
    </div>

</body>
</html>
"""

async def generate_mit_brochure_pdf():
    print("Preparando Brochure Nivel MIT con exactitud A4...")
    html_path = os.path.abspath("temp_mit_brochure.html")
    pdf_path = os.path.abspath("Lifextreme_Brochure_MIT_Qdrant.pdf")
    
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
        
    print(f"PDF MIT Brochure generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_mit_brochure_pdf())
    except Exception as e:
        pass
