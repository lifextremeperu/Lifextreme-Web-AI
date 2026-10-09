import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Guía Básica PYMES - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Space+Grotesk:wght@700&display=swap');
        
        body { 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background-color: #ffffff; 
            color: #1e293b; 
            margin: 0; 
            padding: 30px; 
            font-size: 11.5px; 
            line-height: 1.5;
        }
        
        .header { 
            text-align: center;
            padding-bottom: 15px; 
            border-bottom: 3px solid #f59e0b;
            margin-bottom: 25px; 
        }
        
        .logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 32px; 
            color: #0f172a; 
            font-weight: 700; 
            letter-spacing: -1px;
        }
        .logo span { color: #f59e0b; }
        
        .title {
            font-size: 24px;
            font-weight: 800;
            color: #d97706;
            margin: 10px 0;
            line-height: 1.1;
            text-transform: uppercase;
        }
        
        .subtitle { color: #475569; font-size: 14px; font-weight: 600; margin-top: 10px; }
        
        .grid-3 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }
        
        .mod-card {
            background: #f8fafc;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.04);
            border: 1px solid #e2e8f0;
            page-break-inside: avoid;
            display: flex;
            flex-direction: column;
        }
        
        .icon-box {
            font-size: 45px;
            text-align: center;
            margin-bottom: 15px;
            background: white;
            padding: 10px;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: auto;
            margin-right: auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        .mod-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 15px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 12px;
            line-height: 1.2;
            text-align: center;
            height: 36px;
        }
        
        .mod-desc { 
            color: #334155; 
            margin-bottom: 15px; 
            font-weight: 500;
            flex-grow: 1;
        }
        
        .opp-box {
            background: #fffbeb;
            border: 1px dashed #f59e0b;
            border-radius: 6px;
            padding: 12px;
            font-size: 11px;
            color: #92400e;
        }
        .opp-box strong { 
            color: #b45309; 
            display: block; 
            margin-bottom: 4px;
            text-transform: uppercase;
            font-size: 10px;
        }
        
        .page-break { page-break-before: always; }
        
        .section-banner {
            background: #1e293b;
            color: white;
            padding: 10px 15px;
            font-weight: 800;
            font-size: 15px;
            border-radius: 6px;
            margin: 20px 0;
            text-transform: uppercase;
            text-align: center;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo">LIFEXTREME<span>.PYME</span></div>
        <h1 class="title">GUÍA PRÁCTICA: CÓMO HACER CRECER TU AGENCIA EN CUSCO</h1>
        <div class="subtitle">Explicado de forma sencilla. 15 consejos reales para ganar más dinero y trabajar más tranquilo.</div>
    </div>
    
    <div class="section-banner" style="background: #f59e0b;">PARTE 1: TRUCOS PARA VENDER MÁS RÁPIDO</div>

    <div class="grid-3">
        <!-- 1 -->
        <div class="mod-card">
            <div class="icon-box">🏃‍♂️</div>
            <div class="mod-title">Cobrar más cuando hay desesperación</div>
            <div class="mod-desc">Muchas agencias venden al mismo precio todo el año. Cuando un turista te escribe faltando solo 3 días para su viaje, está apurado y asustado de quedarse sin espacio.</div>
            <div class="opp-box"><strong>💰 TU BENEFICIO DIRECTO:</strong><br>Súbele el precio un 15% a los clientes de última hora. Ellos pagarán felices por la urgencia y tú ganas más dinero por el mismo tour.</div>
        </div>

        <!-- 2 -->
        <div class="mod-card">
            <div class="icon-box">✈️</div>
            <div class="mod-title">Cuidado con el precio de los vuelos</div>
            <div class="mod-desc">Si hay problemas en el mundo, la gasolina sube y los vuelos a Perú se vuelven carísimos. El turista normal se queda sin plata y cancela su viaje.</div>
            <div class="opp-box"><strong>💰 TU BENEFICIO DIRECTO:</strong><br>Si ves en las noticias que los vuelos están caros, deja de gastar publicidad en turistas normales. Empieza a ofrecer tours solo a turistas de lujo (ellos siempre tienen plata).</div>
        </div>

        <!-- 3 -->
        <div class="mod-card">
            <div class="icon-box">📱</div>
            <div class="mod-title">Vende por WhatsApp, olvida tu Web</div>
            <div class="mod-desc">A la gente le da muchísima flojera llenar formularios largos en páginas web. Se aburren y se van a buscar a otra agencia.</div>
            <div class="opp-box"><strong>💰 TU BENEFICIO DIRECTO:</strong><br>Atiéndelos por WhatsApp. Mándales un folleto bonito y un link de Yape/Niubiz ahí mismo. Comprarán emocionados desde su celular en un par de minutos.</div>
        </div>
    </div>

    <div class="grid-3">
        <!-- 4 -->
        <div class="mod-card">
            <div class="icon-box">💶</div>
            <div class="mod-title">Aprovecha cuando el Euro sube</div>
            <div class="mod-desc">Cuando el Euro vale mucho más que el dólar o el sol, los europeos sienten que todo en Perú es un remate baratísimo.</div>
            <div class="opp-box"><strong>💰 TU BENEFICIO DIRECTO:</strong><br>Si ves que el Euro amaneció alto, pon tus anuncios de Facebook enfocados solo en Europa. Te comprarán los tours más caros sin pedirte ni un solo sol de rebaja.</div>
        </div>
        
        <!-- 5 -->
        <div class="mod-card">
            <div class="icon-box">🥂</div>
            <div class="mod-title">Huye de la pelea de la Plaza de Armas</div>
            <div class="mod-desc">Pelearte en la calle por vender un City Tour a 20 dólares no deja ganancias, solo cansancio y dolores de cabeza.</div>
            <div class="opp-box"><strong>💰 TU BENEFICIO DIRECTO:</strong><br>Arma un "Tour Privado VIP" a $150 incluyendo un vinito y un auto limpio. Vendes uno solo y ganas lo mismo que vendiendo 30 de los baratos, pero sin estrés.</div>
        </div>

        <!-- 6 -->
        <div class="mod-card">
            <div class="icon-box">🌧️</div>
            <div class="mod-title">No devuelvas la plata si hay lluvias</div>
            <div class="mod-desc">Si hay un paro en la carretera o llueve mucho en la Montaña de 7 Colores, las agencias normales devuelven toda la plata y se quedan en cero.</div>
            <div class="opp-box"><strong>💰 TU BENEFICIO DIRECTO:</strong><br>Ofréceles al instante "cambiar la ruta" hacia una zona con sol (como el Valle Sur). Salvas el día del turista y el dinero no se escapa de tus bolsillos.</div>
        </div>
    </div>
    
    <div class="page-break"></div>
    <div class="header" style="margin-top: 10px; margin-bottom: 10px;">
        <div class="logo">LIFEXTREME<span>.PYME</span></div>
    </div>
    <div class="section-banner" style="background: #10b981;">PARTE 2: CRECER HASTA LAS GRANDES LIGAS</div>

    <div class="grid-3">
        <!-- 7 -->
        <div class="mod-card" style="border-top-color: #10b981;">
            <div class="icon-box">🤝</div>
            <div class="mod-title">Los papeles en regla valen oro (Mincetur/ISO)</div>
            <div class="mod-desc">Las agencias gigantes de Europa quieren enviarte cientos de turistas, pero por sus leyes, no pueden hacer negocios con agencias informales.</div>
            <div class="opp-box"><strong style="color: #047857;">💰 TU BENEFICIO DIRECTO:</strong><br>Tramita tu Constancia DIRCETUR y busca un certificado de calidad (ISO). Serás la primera opción de los europeos porque eres seguro y legal.</div>
        </div>
        
        <!-- 8 -->
        <div class="mod-card" style="border-top-color: #10b981;">
            <div class="icon-box">🤖</div>
            <div class="mod-title">Háblale a ChatGPT, no a Google</div>
            <div class="mod-desc">Pelear en Google contra Tripadvisor es imposible. Pero ahora los turistas planean sus viajes haciéndole preguntas a la Inteligencia Artificial (ChatGPT).</div>
            <div class="opp-box"><strong style="color: #047857;">💰 TU BENEFICIO DIRECTO:</strong><br>Escribe en tu web preguntas y respuestas claritas (Ej: "¿Cuánto se camina en Vinicunca? - 2 horas"). ChatGPT tomará tu respuesta y te recomendará gratis.</div>
        </div>

        <!-- 9 -->
        <div class="mod-card" style="border-top-color: #10b981;">
            <div class="icon-box">🤳</div>
            <div class="mod-title">Invita a un TikToker, no pagues Facebook</div>
            <div class="mod-desc">Gastar en publicidad tradicional es tirar la plata si eres pequeño. Los jóvenes ven un video en TikTok y quieren hacer exactamente el mismo viaje.</div>
            <div class="opp-box"><strong style="color: #047857;">💰 TU BENEFICIO DIRECTO:</strong><br>Regálale un tour a un influencer extranjero que tenga 10 mil seguidores. Es publicidad mundial que te costará cero dólares.</div>
        </div>
    </div>
    
    <div class="grid-3">
        <!-- 10 -->
        <div class="mod-card">
            <div class="icon-box">🛑</div>
            <div class="mod-title">No le regales tu plata a Booking</div>
            <div class="mod-desc">Las plataformas por internet te quitan el 20% de tu esfuerzo. Muchos turistas ven tu tour ahí, pero luego buscan el nombre de tu agencia en internet para ver si es más barato.</div>
            <div class="opp-box"><strong>💰 TU BENEFICIO DIRECTO:</strong><br>Pon un cartelazo en tu página: "Te recojo del aeropuerto GRATIS si reservas directo a mi WhatsApp". Pagar un taxi te cuesta $5, pero te ahorras regalarle $50 a Booking.</div>
        </div>

        <!-- 11 -->
        <div class="mod-card">
            <div class="icon-box">🌴</div>
            <div class="mod-title">Gana comisión cuando el turista se vaya</div>
            <div class="mod-desc">Un turista visita Cusco hoy, pero es casi seguro que el próximo año viajará a la Selva de Iquitos. ¿Por qué vas a dejar de ganar dinero con él?</div>
            <div class="opp-box"><strong>💰 TU BENEFICIO DIRECTO:</strong><br>Hazte amigo de una agencia en la Selva. Meses después, mándale un saludo al turista ofreciéndole la Selva. Si compra, tú cobras tu "comisión por recomendar" sin mover un dedo.</div>
        </div>

        <!-- 12 -->
        <div class="mod-card">
            <div class="icon-box">🧘‍♀️</div>
            <div class="mod-title">El gran negocio de las mujeres solas</div>
            <div class="mod-desc">Todo el mundo vende paquetes genéricos para "Familias". Hay muchísima competencia. Pero hay miles de mujeres en el mundo buscando viajar solas de forma segura.</div>
            <div class="opp-box"><strong>💰 TU BENEFICIO DIRECTO:</strong><br>Ofrece "Tours con Guías Mujeres y Seguridad Total". Serás el líder absoluto de este nicho en Cusco y te lloverán reservas.</div>
        </div>
    </div>

    <div class="page-break"></div>
    <div class="header" style="margin-top: 10px; margin-bottom: 10px;">
        <div class="logo">LIFEXTREME<span>.PYME</span></div>
    </div>
    <div class="section-banner" style="background: #2563eb;">PARTE 3: EL FUTURO (CÓMO NO QUEDARSE ATRÁS)</div>

    <div class="grid-3">
        <!-- 13 -->
        <div class="mod-card" style="border-top-color: #2563eb;">
            <div class="icon-box">👔</div>
            <div class="mod-title">El dinero de los Limeños estresados</div>
            <div class="mod-desc">No persigas solo a los gringos. En Lima hay gerentes de bancos y mineras muy cansados. Sus jefes tienen plata apartada para hacerlos descansar.</div>
            <div class="opp-box"><strong style="color: #1d4ed8;">💰 TU BENEFICIO DIRECTO:</strong><br>Llama a las empresas (B2B) y ofréceles "Retiros de Fin de Semana Sin Celular". Te pagarán muy bien y tendrás trabajo en temporada baja.</div>
        </div>

        <!-- 14 -->
        <div class="mod-card" style="border-top-color: #2563eb;">
            <div class="icon-box">🛶</div>
            <div class="mod-title">Llega primero a la Selva</div>
            <div class="mod-desc">Cusco ya está llenísimo de agencias. El gobierno pronto pondrá todo su dinero y publicidad en promocionar Loreto y el Norte de Perú.</div>
            <div class="opp-box"><strong style="color: #1d4ed8;">💰 TU BENEFICIO DIRECTO:</strong><br>Arma hoy mismo un par de rutas hacia la Amazonía usando a Lifextreme. Cuando todo el mundo quiera ir a la selva en unos años, tú ya serás el experto.</div>
        </div>

        <!-- 15 -->
        <div class="mod-card" style="border-top-color: #2563eb;">
            <div class="icon-box">🏔️</div>
            <div class="mod-title">Lo que un Robot nunca te podrá robar</div>
            <div class="mod-desc">Las aplicaciones de internet pueden vender pasajes rápidos, pero un robot de computadora jamás podrá abrazar ni hacerte probar una papa recién cosechada.</div>
            <div class="opp-box"><strong style="color: #1d4ed8;">💰 TU BENEFICIO DIRECTO:</strong><br>Ofrece al turista convivir y dormir con una familia andina local. Es un lujo humano por el que los ricos pagan muchísimo dinero hoy en día.</div>
        </div>
    </div>
    
    <div style="background: #0f172a; color: white; padding: 30px; border-radius: 12px; text-align: center; margin-top: 30px; border-bottom: 6px solid #f59e0b;">
        <h2 style="margin-top: 0; font-family: 'Space Grotesk'; font-size: 22px; color: #f59e0b;">TRABAJA MÁS INTELIGENTE, DEJA QUE LIFEXTREME HAGA LO PESADO</h2>
        <p style="font-size: 14px; margin-bottom: 0; line-height: 1.6;"><strong>Tu único trabajo como dueño de tu agencia es aplicar estas 15 ideas, conseguir tus papeles en el Mincetur y conversar con tus clientes.</strong> Si te despiertas a las 4 de la mañana para pelear con choferes o rogar por un bus, nunca vas a crecer. Conviértete en nuestro aliado: <strong>Tú vendes, y Lifextreme se encarga de que la camioneta esté en la puerta a la hora exacta.</strong></p>
    </div>

</body>
</html>
"""

async def generate_human_pymes_pdf():
    print("Preparando Guía Básica para Humanos...")
    html_path = os.path.abspath("temp_human_pymes.html")
    pdf_path = os.path.abspath("Lifextreme_Guia_Basica_PYMES.pdf")
    
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
        
    print(f"PDF Guía Básica generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_human_pymes_pdf())
    except Exception as e:
        pass
