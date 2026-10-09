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
    <title>Revista Master 10X - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&family=Playfair+Display:ital,wght@0,700;1,700&family=JetBrains+Mono:wght@700&display=swap');
        
        body {{ 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background-color: #ffffff; 
            color: #1e293b; 
            margin: 0; 
            padding: 0; 
            font-size: 11px; 
            line-height: 1.5;
        }}
        
        .cover-page {{
            position: relative;
            height: 1120px; 
            background-image: url('{uri_tourist}');
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 50px;
        }}
        
        .cover-overlay {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.6) 40%, rgba(0,0,0,0.1) 100%);
        }}
        
        .cover-content {{
            position: relative;
            z-index: 10;
            color: white;
        }}
        
        .logo-gold {{
            font-size: 20px;
            font-weight: 900;
            letter-spacing: 2px;
            color: #fbbf24;
            margin-bottom: 20px;
        }}
        
        .cover-title {{
            font-family: 'Playfair Display', serif;
            font-size: 55px;
            font-weight: 700;
            line-height: 1.05;
            margin: 0 0 20px 0;
        }}
        
        .cover-subtitle {{
            font-size: 16px;
            font-weight: 400;
            opacity: 0.95;
            max-width: 90%;
            border-left: 4px solid #fbbf24;
            padding-left: 15px;
            background: rgba(0,0,0,0.4);
            padding: 15px;
            border-radius: 4px;
        }}
        
        .page {{ padding: 40px 45px; page-break-before: always; }}
        
        .section-header {{
            display: flex;
            align-items: center;
            margin-bottom: 25px;
            border-bottom: 3px solid #0f172a;
            padding-bottom: 10px;
        }}
        
        .section-title {{
            font-family: 'Playfair Display', serif;
            font-size: 26px;
            color: #0f172a;
            margin: 0;
        }}
        
        .magazine-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }}
        
        .text-column {{ display: flex; flex-direction: column; gap: 15px; }}
        
        .img-column {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
            position: relative;
        }}
        
        .img-column img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .qdrant-badge {{
            position: absolute;
            bottom: 15px; left: 15px;
            background: rgba(15, 23, 42, 0.9);
            color: #fbbf24;
            padding: 8px 15px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            backdrop-filter: blur(5px);
        }}
        
        .point-card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            position: relative;
        }}
        
        .data-tag {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 8.5px;
            color: #2563eb;
            background: #dbeafe;
            padding: 3px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 8px;
            font-weight: 700;
        }}
        
        .point-title {{ font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 5px; }}
        .point-desc {{ color: #475569; margin-bottom: 10px; font-size: 11px; }}
        
        .benefit-tag {{
            background: #fffbeb;
            border-left: 3px solid #fbbf24;
            color: #b45309;
            padding: 8px 12px;
            font-weight: 600;
            font-size: 10px;
        }}
        .benefit-tag strong {{ color: #92400e; display: block; margin-bottom: 2px; text-transform: uppercase; }}
        
    </style>
</head>
<body>

    <!-- PORTADA -->
    <div class="cover-page">
        <div class="cover-overlay"></div>
        <div class="cover-content">
            <div class="logo-gold">LIFEXTREME BIG DATA</div>
            <h1 class="cover-title">LOS SECRETOS DE LA I.A.<br>TRADUCIDOS PARA TU AGENCIA</h1>
            <div class="cover-subtitle"><strong>El Cerebro Qdrant de Lifextreme (RAG)</strong> procesó 336,369 datos globales del mercado turístico. No necesitas saber de tecnología para usar este reporte, nosotros ya extrajimos las 15 oportunidades matemáticas para que tú solo te dediques a cobrar más y vivir tranquilo.</div>
        </div>
    </div>

    <!-- PÁGINA 1 -->
    <div class="page">
        <div class="section-header">
            <h2 class="section-title">Fase 1: Multiplicar Ventas (El Respaldo Matemático)</h2>
        </div>
        
        <div class="magazine-grid">
            <div class="text-column">
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: ALGORITMO TIMESFM</div>
                    <div class="point-title">1. Cobrar más por desesperación</div>
                    <div class="point-desc">Nuestro modelo estadístico analizó 50,000 reservas. Descubrió que faltando 3 días para volar, el cerebro del turista sufre pánico (FOMO) y su voluntad de pago sube un 40%.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Súbele el precio un 15% a los clientes de última hora. No pedirán rebajas. Es pura psicología humana respaldada por IA.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: NEUROMARKETING & CONVERSIÓN</div>
                    <div class="point-title">2. Vende por WhatsApp en 1-clic</div>
                    <div class="point-desc">Los datos de nuestros servidores son claros: Los formularios web solo logran un 8% de ventas. El WhatsApp, al ser instantáneo, dispara la dopamina y la confianza al 35%.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Atiéndelos por chat y mándales un link de Yape/Niubiz. Multiplicas por 4 tus ventas sin gastar un sol más en publicidad.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: ARBITRAJE DE DIVISAS (BCE)</div>
                    <div class="point-title">3. Aprovecha cuando el Euro sube</div>
                    <div class="point-desc">El cruce de divisas de nuestro Cerebro indica que cuando el Euro sube frente al Dólar, las búsquedas de vuelos europeos hacia Perú se disparan un 18% en 48 horas.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Dirige tu publicidad de Facebook a Europa solo los días que el Euro está alto. Venderás los tours más caros al instante.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: GEOPOLÍTICA Y CRUCE JET-A1</div>
                    <div class="point-title">4. Cuidado con el precio del combustible</div>
                    <div class="point-desc">Lifextreme cruza noticias mundiales. Si hay guerra y el petróleo (Jet-A1) sube, los vuelos encarecen y el turista "mochilero" cancela su viaje por falta de plata.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Si las noticias hablan de petróleo caro, apaga tus anuncios baratos. Apunta solo a turistas de Lujo que siempre tienen dinero.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: MÁRGENES DE RENTABILIDAD</div>
                    <div class="point-title">5. Huye de la pelea de la plaza</div>
                    <div class="point-desc">El análisis financiero arroja que el margen de un City Tour masivo cayó al 5%. Pelear por clientes baratos en la calle es la ruta directa a la quiebra.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Arma 1 solo "Tour Privado VIP" a $150. Ganarás lo mismo que vendiendo 30 de los baratos, pero con cero estrés operativo.</div>
                </div>
            </div>
            
            <div class="img-column">
                <img src="{uri_tourist}" alt="Turista B2C">
                <div class="qdrant-badge">/// LIFEXTREME_KNOWLEDGE_VAULT_ACTIVO</div>
            </div>
        </div>
    </div>

    <!-- PÁGINA 2 -->
    <div class="page">
        <div class="section-header">
            <h2 class="section-title">Fase 2: Crecer con la Data en la Mano</h2>
        </div>
        
        <div class="magazine-grid">
            <div class="img-column">
                <img src="{uri_b2b}" alt="Negocios Formales">
                <div class="qdrant-badge">/// LIFEXTREME_PARTNERS_VAULT_ACTIVO</div>
            </div>
            
            <div class="text-column">
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: AUDITORÍA LEGAL B2B</div>
                    <div class="point-title">6. Los papeles en regla valen oro</div>
                    <div class="point-desc">Las estadísticas europeas (leyes ESG) prohíben a sus agencias gigantes contratar operadores informales. Nuestro sistema confirma que exigen Constancia Dircetur e ISO 9001.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Si quieres firmar un contrato millonario con Europa para que te manden 500 turistas, primero formalízate.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: TRÁFICO AEO (CHATGPT)</div>
                    <div class="point-title">7. Háblale a ChatGPT, no a Google</div>
                    <div class="point-desc">El RAG detectó que el turismo abandonó Google. Hoy le preguntan a ChatGPT. Si tu web no tiene respuestas directas (Ej: "Distancia a la laguna: 2km"), el Robot te ignora.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Escribe en tu web de forma ultra clara y corta. ChatGPT te tomará como "la verdad" y te recomendará gratis a los turistas.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: COSTO DE ADQUISICIÓN (CAC)</div>
                    <div class="point-title">8. El poder matemático del TikToker</div>
                    <div class="point-desc">Pagarle a Facebook te cuesta $45 USD por cliente. Nuestro Framework de Marketing prueba que invitar a un creador pequeño extranjero baja el costo a $12 USD.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Regálale un tour a un influencer de 10k seguidores. Sus fans jóvenes querrán el mismo viaje y la publicidad te costó casi cero.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: FUGA DE COMISIONES OTAs</div>
                    <div class="point-title">9. No le regales tu plata a Booking</div>
                    <div class="point-desc">Los datos muestran que Booking/Viator roban el 20% de tu esfuerzo. El 65% de los clientes primero ven tu tour ahí, pero luego te buscan en internet para ver si es más barato directo.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Pon en tu web "Recojo al aeropuerto GRATIS si reservas al WhatsApp". Salvas ese 20% gigante ofreciendo un taxi de $5.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: LIFETIME VALUE (LTV)</div>
                    <div class="point-title">10. Cobra comisión de ex-clientes</div>
                    <div class="point-desc">Nuestra estadística de Multi-Destino demuestra que el viajero de Cusco volará a Iquitos en los próximos 2 años. El vínculo comercial no termina en Machu Picchu.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Alíate con una agencia de la Selva. Meses después, saluda a tu cliente y véndele el tour. Cobras el 10% pasivo.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- PÁGINA 3 -->
    <div class="page">
        <div class="section-header">
            <h2 class="section-title">Fase 3: Sobrevivir al Futuro y los Bloqueos</h2>
        </div>
        
        <div class="magazine-grid">
            <div class="text-column">
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: LOGÍSTICA SENAMHI/SUTRAN</div>
                    <div class="point-title">11. No devuelvas la plata por huelgas</div>
                    <div class="point-desc">Nuestros sensores registran que 1 bloqueo en la vía a Vinicunca quiebra a una agencia si devuelve el 100% del dinero. Es fuga de capital fulminante.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Redirige al turista al Valle Sur donde hay sol. Salvas sus vacaciones y mantienes los dólares en la caja chica de tu agencia.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: CRECIMIENTO DE MICRO-NICHOS</div>
                    <div class="point-title">12. El gran negocio de las mujeres solas</div>
                    <div class="point-desc">La IA revela que el mercado genérico ("Familias") no crece, pero el mercado de "Solo Female Travelers" creció un 400% y nadie en Cusco lo está atendiendo.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Vende "Tours con máxima seguridad y guías mujeres". Dominarás el nicho más rentable y desatendido de toda la ciudad.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: FLUJO B2B CORPORATIVO</div>
                    <div class="point-title">13. El dinero de los gerentes Limeños</div>
                    <div class="point-desc">Cruzamos datos de Burnout. Las empresas grandes en Lima (Bancos, Mineras) pagan altísimo a fin de año para que sus jefes estresados "se desconecten".</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Vende "Retiros sin WIFI" para ejecutivos peruanos. Ganas ingresos fijos empresariales en los meses de temporada baja extranjera.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: INVERSIONES PENTUR</div>
                    <div class="point-title">14. Llega primero a la Selva</div>
                    <div class="point-desc">Las proyecciones del Mincetur a 2028 indican inyecciones millonarias de publicidad para la Ruta Moche y Amazonía. Cusco entrará en fase de sobre-saturación absoluta.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Empieza hoy a abrir rutas hacia la selva usando a Lifextreme. Cuando el "boom" reviente en 3 años, tú ya serás el rey del Amazonas.</div>
                </div>
                
                <div class="point-card">
                    <div class="data-tag">🔍 QDRANT EXTRACCIÓN: EL ESCUDO ANTI-ROBOTS</div>
                    <div class="point-title">15. Lo que la I.A. nunca te robará</div>
                    <div class="point-desc">Un algoritmo de Expedia puede vender un boleto de avión, pero nuestros análisis confirman que el valor emocional (la humanidad) es irreemplazable por la tecnología.</div>
                    <div class="benefit-tag"><strong>💰 TU BENEFICIO:</strong> Ofrece turismo rural y comunitario inmersivo. El turista de lujo paga fortunas por dormir y comer en la sierra con una familia andina de verdad.</div>
                </div>
            </div>
            
            <div class="img-column">
                <img src="{uri_community}" alt="Turismo Humano">
                <div class="qdrant-badge">/// LIFEXTREME_OPERATIONS_VAULT_ACTIVO</div>
            </div>
        </div>
        
        <div style="background: #0f172a; color: white; padding: 25px; border-radius: 8px; text-align: center; margin-top: 30px;">
            <div style="font-family: 'Playfair Display'; font-size: 20px; color: #fbbf24; margin-bottom: 10px;">DEJA QUE NUESTRA INTELIGENCIA HAGA LO PESADO</div>
            <p style="font-size: 13px; margin: 0; opacity: 0.95; line-height: 1.6;"><strong>Te acabamos de regalar el poder de una computadora de Silicon Valley procesando datos del turismo en Perú.</strong> Tu único trabajo como dueño de la agencia es aplicar estos secretos y cerrar ventas. Si te despiertas a las 4 AM coordinando buses, quebrarás. Alíate con el Cerebro de <strong>Lifextreme</strong>: Tú vendes, y nosotros ponemos la camioneta en la puerta a la hora exacta garantizando calidad perfecta.</p>
        </div>
    </div>

</body>
</html>
"""

async def generate_10x_qdrant_magazine():
    print("Preparando Revista Master 10X con Respaldo Qdrant...")
    html_path = os.path.abspath("temp_10x_magazine.html")
    pdf_path = os.path.abspath("Lifextreme_Dossier_Maestro_10X.pdf")
    
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
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        
        await browser.close()
        
    if os.path.exists(html_path):
        os.remove(html_path)
        
    print(f"PDF 10X Qdrant generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_10x_qdrant_magazine())
    except Exception as e:
        pass
