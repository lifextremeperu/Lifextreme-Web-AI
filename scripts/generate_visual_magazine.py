import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

img_tourist = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\cusco_business_tourist_1791572148790.jpg"
img_community = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\amazon_community_tourism_1791572171378.jpg"
img_b2b = r"C:\Users\ASUS\.gemini\antigravity\brain\722c29e4-a526-4adc-b44c-643f1d34113e\corporate_travel_pyme_1791572199630.jpg"

# Create file URIs
uri_tourist = "file:///" + img_tourist.replace("\\", "/")
uri_community = "file:///" + img_community.replace("\\", "/")
uri_b2b = "file:///" + img_b2b.replace("\\", "/")

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Guía Visual PYMES - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
        
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
            height: 1120px; /* A4 approx */
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
            background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.3) 50%, rgba(0,0,0,0.1) 100%);
        }}
        
        .cover-content {{
            position: relative;
            z-index: 10;
            color: white;
        }}
        
        .logo-gold {{
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 2px;
            color: #fbbf24;
            margin-bottom: 20px;
            text-transform: uppercase;
        }}
        
        .cover-title {{
            font-family: 'Playfair Display', serif;
            font-size: 55px;
            font-weight: 700;
            line-height: 1.1;
            margin: 0 0 20px 0;
        }}
        
        .cover-subtitle {{
            font-size: 18px;
            font-weight: 400;
            opacity: 0.9;
            max-width: 80%;
        }}
        
        .page {{
            padding: 40px 50px;
            page-break-before: always;
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #fbbf24;
            padding-bottom: 10px;
        }}
        
        .section-title {{
            font-family: 'Playfair Display', serif;
            font-size: 28px;
            color: #0f172a;
            margin: 0;
        }}
        
        .magazine-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}
        
        .text-column {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .img-column {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        
        .img-column img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .point-card {{
            background: #f8fafc;
            border-left: 4px solid #fbbf24;
            padding: 15px;
            border-radius: 0 8px 8px 0;
        }}
        
        .point-title {{
            font-size: 14px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 5px;
        }}
        
        .point-desc {{
            color: #475569;
            margin-bottom: 10px;
        }}
        
        .benefit-tag {{
            background: #fffbeb;
            color: #b45309;
            padding: 6px 10px;
            border-radius: 4px;
            font-weight: 700;
            font-size: 10px;
            display: inline-block;
        }}
        
    </style>
</head>
<body>

    <!-- PORTADA VISUAL -->
    <div class="cover-page">
        <div class="cover-overlay"></div>
        <div class="cover-content">
            <div class="logo-gold">LIFEXTREME PYME</div>
            <h1 class="cover-title">CÓMO HACER CRECER<br>TU AGENCIA HOY</h1>
            <div class="cover-subtitle">Olvídate de la teoría complicada. 15 consejos reales y visuales para vender más rápido, formalizarte y asegurar el futuro de tu negocio en Cusco.</div>
        </div>
    </div>

    <!-- PÁGINA 1: VENTAS RAPIDAS -->
    <div class="page">
        <div class="section-header">
            <h2 class="section-title">Fase 1: Trucos para Vender Más Rápido</h2>
        </div>
        
        <div class="magazine-grid">
            <div class="text-column">
                <div class="point-card">
                    <div class="point-title">1. Cobrar más por desesperación</div>
                    <div class="point-desc">Cuando un turista te escribe faltando 3 días para su viaje, está apurado. Súbele el precio un 15%.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Ganas más dinero por el mismo tour.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">2. Vende por WhatsApp en 1-clic</div>
                    <div class="point-desc">La gente odia llenar formularios largos. Mándales un link de Yape/Niubiz por chat para que paguen al instante.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Cierras la venta antes de que se arrepientan.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">3. Aprovecha si el Euro sube</div>
                    <div class="point-desc">Si el Euro está alto, el europeo siente que todo en Perú es baratísimo. Lanza tus anuncios allá esos días.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Te compran sin pedirte ni un sol de rebaja.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">4. Cuidado con el precio de los vuelos</div>
                    <div class="point-desc">Si las noticias dicen que la gasolina y los vuelos subieron, el turista normal se queda sin dinero.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Ahorras publicidad enfocándote solo en turistas ricos.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">5. Huye de la pelea de la plaza</div>
                    <div class="point-desc">No pelees por un tour barato de $20. Arma un Tour Privado a $150 con un auto limpio y un vino.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Vendes menos cantidad, pero ganas el triple sin estrés.</div>
                </div>
            </div>
            
            <div class="img-column">
                <img src="{uri_tourist}" alt="Turista comprando en celular">
            </div>
        </div>
    </div>

    <!-- PÁGINA 2: FORMALIZACION -->
    <div class="page">
        <div class="section-header">
            <h2 class="section-title">Fase 2: Crecer a las Grandes Ligas</h2>
        </div>
        
        <div class="magazine-grid">
            <div class="img-column">
                <img src="{uri_b2b}" alt="Negocios B2B formales">
            </div>
            
            <div class="text-column">
                <div class="point-card">
                    <div class="point-title">6. Los papeles en regla valen oro</div>
                    <div class="point-desc">Las agencias gigantes de Europa quieren enviarte clientes, pero por sus leyes, exigen certificados (DIRCETUR, ISO).</div>
                    <div class="benefit-tag">💰 BENEFICIO: Eres la primera opción para contratos millonarios.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">7. Háblale a ChatGPT, no a Google</div>
                    <div class="point-desc">Los turistas planean sus viajes preguntándole a la I.A. Escribe respuestas súper claras en tu web para que te cite.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Consigues publicidad gratis de la Inteligencia Artificial.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">8. Invita a un TikToker</div>
                    <div class="point-desc">Regálale un tour a un influencer joven de otro país en lugar de pagar anuncios carísimos en Facebook.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Consigues miles de clientes jóvenes a costo cero.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">9. No le regales tu plata a Booking</div>
                    <div class="point-desc">Ofrece en tu web un "Recojo al aeropuerto GRATIS" si te reservan directo por WhatsApp.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Salvas el 20% de comisión que te quitan las plataformas.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">10. Cobra comisión de ex-clientes</div>
                    <div class="point-desc">Si tu turista de Cusco se va a Iquitos, recomiéndale una agencia amiga en la selva.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Ganas dinero extra meses después sin mover un bus.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- PÁGINA 3: FUTURO Y COMUNIDAD -->
    <div class="page">
        <div class="section-header">
            <h2 class="section-title">Fase 3: El Futuro Anti-Robots</h2>
        </div>
        
        <div class="magazine-grid">
            <div class="text-column">
                <div class="point-card">
                    <div class="point-title">11. El gran negocio de las mujeres solas</div>
                    <div class="point-desc">El grupo que más viaja hoy son mujeres solas. Ofréceles guías mujeres y máxima seguridad.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Dominarás este nicho millonario casi sin competencia.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">12. El dinero de los gerentes Limeños</div>
                    <div class="point-desc">Llama a grandes empresas en Lima y ofréceles "Retiros de Fin de Semana" para sus jefes estresados.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Las empresas pagan altísimo en temporada baja.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">13. Llega primero a la Selva</div>
                    <div class="point-desc">Cusco ya está lleno. El gobierno pronto invertirá millones en promocionar la Amazonía.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Si abres rutas en la selva hoy, serás el líder mañana.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">14. No devuelvas la plata si llueve</div>
                    <div class="point-desc">Si hay un bloqueo en la vía, no devuelvas el dinero. Ofréceles al instante una ruta alternativa con sol.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Salvas el día del turista y tu dinero no se escapa.</div>
                </div>
                
                <div class="point-card">
                    <div class="point-title">15. Lo que un robot nunca te robará</div>
                    <div class="point-desc">Un robot no puede abrazar. El turista rico paga fortunas por dormir y cocinar con una familia andina o nativa.</div>
                    <div class="benefit-tag">💰 BENEFICIO: Vendes experiencias 100% humanas imposibles de copiar.</div>
                </div>
            </div>
            
            <div class="img-column">
                <img src="{uri_community}" alt="Turismo comunitario y humano">
            </div>
        </div>
        
        <div style="background: #0f172a; color: white; padding: 25px; border-radius: 8px; text-align: center; margin-top: 30px;">
            <div style="font-family: 'Playfair Display'; font-size: 20px; color: #fbbf24; margin-bottom: 10px;">DEJA QUE LIFEXTREME HAGA LO PESADO</div>
            <p style="font-size: 13px; margin: 0; opacity: 0.9;">Tu único trabajo es conseguir tus papeles y conversar con clientes. Si te quedas despierto a las 4 AM coordinando buses, quebrarás. Alíate con nosotros: Tú vendes, y <strong>Lifextreme</strong> pone la camioneta en la puerta a la hora exacta.</p>
        </div>
    </div>

</body>
</html>
"""

async def generate_visual_magazine_pdf():
    print("Preparando Revista Visual de PYMES...")
    html_path = os.path.abspath("temp_magazine.html")
    pdf_path = os.path.abspath("Lifextreme_Guia_Visual_PYMES.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(f"file:///{html_path}")
        await page.wait_for_timeout(2000) # Wait for local images to load
        
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        
        await browser.close()
        
    if os.path.exists(html_path):
        os.remove(html_path)
        
    print(f"PDF Revista Visual generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_visual_magazine_pdf())
    except Exception as e:
        pass
