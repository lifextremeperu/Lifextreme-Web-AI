import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Las 10 Oportunidades de Oro - Agencias Cusco</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap');
        
        body { 
            font-family: 'Poppins', sans-serif; 
            background-color: #f8fafc; 
            color: #334155; 
            margin: 0; 
            padding: 40px; 
            font-size: 13px; 
            line-height: 1.6;
        }
        
        .header { 
            text-align: center;
            padding-bottom: 25px; 
            margin-bottom: 30px; 
        }
        
        .logo {
            font-size: 32px; 
            color: #0f172a; 
            font-weight: 900; 
            letter-spacing: -1px;
        }
        
        .logo span { color: #f59e0b; }
        
        .title {
            font-size: 36px;
            font-weight: 900;
            color: #2563eb;
            margin: 10px 0;
            line-height: 1.1;
        }
        
        .subtitle {
            color: #475569;
            font-size: 16px;
            font-weight: 500;
        }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        
        .opp-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 25px;
            position: relative;
            page-break-inside: avoid;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            border-top: 5px solid #2563eb;
        }
        
        .opp-number {
            background: #fef3c7;
            color: #d97706;
            font-weight: 900;
            font-size: 16px;
            padding: 4px 12px;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        .opp-title {
            font-size: 18px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 15px;
            line-height: 1.2;
        }
        
        .section-box {
            background: #f1f5f9;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        .section-label {
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            color: #2563eb;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
        }
        
        .result-box {
            background: #ecfdf5;
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px dashed #10b981;
        }
        
        .result-label {
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            color: #059669;
            margin-bottom: 5px;
        }
        
        .cta-box {
            background: linear-gradient(135deg, #1e40af, #2563eb);
            color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            margin-top: 40px;
            page-break-inside: avoid;
            box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
        }
        
        .cta-title {
            font-size: 24px;
            font-weight: 900;
            margin-bottom: 15px;
        }
        
        .page-break { page-break-before: always; }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo">LIFEXTREME<span>.B2B</span></div>
        <h1 class="title">LAS 10 OPORTUNIDADES DE ORO</h1>
        <div class="subtitle">Guía simple y práctica para multiplicar las ventas y ganancias de tu Agencia de Viajes.</div>
    </div>

    <div class="grid-2">
        <!-- 1 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 1</div>
            <div class="opp-title">Precios Inteligentes (Cobrar más cuando hay prisa)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>¿Has visto que las aerolíneas te cobran más si compras el boleto a última hora? ¡Haz lo mismo! Si un turista latino te escribe faltando 3 días para su viaje, súbele el precio al tour un 15%. Tienen urgencia y pagarán felices.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Más dinero en tu bolsillo por el mismo tour de siempre.</div>
            </div>
        </div>

        <!-- 2 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 2</div>
            <div class="opp-title">El Turista Europeo y su "Moneda Fuerte"</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Cuando el Euro vale más que el dólar, los europeos sienten que viajar a Perú está "baratísimo". Lanza tus ofertas en Facebook dirigidas a Europa exactamente esos días.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Atraes clientes que no te pedirán rebajas porque tienen dinero de sobra.</div>
            </div>
        </div>

        <!-- 3 -->
        <div class="opp-card" style="border-top-color: #f59e0b;">
            <div class="opp-number">💡 Oportunidad 3</div>
            <div class="opp-title">Cobrar Caro por Exclusividad (Cero descuentos)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Hay turistas de lujo que huyen de los "tours masivos de $20". Crea un paquete VIP Oculto a $150 incluyendo cosas simples pero bonitas (un picnic privado o un pago a la tierra).</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Trabajas menos, llevas menos gente, pero multiplicas tu ganancia por cinco.</div>
            </div>
        </div>

        <!-- 4 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 4</div>
            <div class="opp-title">Cierre de Ventas Mágico por WhatsApp</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>La gente en internet es muy impaciente. En vez de mandarles correos aburridos, mándales un PDF bonito por WhatsApp con un botón de pago directo (Yape o Niubiz).</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Tus clientes pagan desde su celular en 2 minutos antes de arrepentirse.</div>
            </div>
        </div>
    </div>
    
    <div class="page-break"></div>

    <div class="grid-2">
        <!-- 5 -->
        <div class="opp-card" style="border-top-color: #10b981;">
            <div class="opp-number">💡 Oportunidad 5</div>
            <div class="opp-title">Salvar la Venta y Cero Devoluciones por Clima</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>¿Está lloviendo en Vinicunca? ¡No les devuelvas la plata! Ofréceles un "Cambio a Ruta Segura" llevándolos a Palccoyo o al Valle Sagrado Sur donde hay sol.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>El turista viaja feliz, agradece tu sinceridad y tu dinero no se escapa de la caja.</div>
            </div>
        </div>

        <!-- 6 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 6</div>
            <div class="opp-title">No le regales tus ganancias a Booking o Viator</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Las páginas de terceros te quitan hasta un 20% de comisión. En tu página web pon un letrero enorme: <em>"Reserva directo en nuestro WhatsApp y gana el traslado gratis al aeropuerto"</em>.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>El traslado te cuesta poco, pero recuperas ese 20% gigante de comisión.</div>
            </div>
        </div>

        <!-- 7 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 7</div>
            <div class="opp-title">El Truco de los "Mini-Influencers" en TikTok</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Pagar anuncios tradicionales ya casi no funciona. Mejor invita a viajar a creadores de TikTok extranjeros con pocos pero muy fieles seguidores (10 mil a 50 mil).</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Gastarás casi nada en publicidad, y sus seguidores querrán comprar el tour exactamente igual.</div>
            </div>
        </div>

        <!-- 8 -->
        <div class="opp-card" style="border-top-color: #8b5cf6;">
            <div class="opp-number">💡 Oportunidad 8</div>
            <div class="opp-title">Vender Paz Mental (Y derribar miedos)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Muchos turistas no compran por miedo a la altura y les da vergüenza preguntar. Escribe gigante en tu web: <em>"No le temas a la altura, tenemos oxígeno a bordo"</em>.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Le das tranquilidad inmediata al cliente indeciso y te compran a ti y no a la competencia.</div>
            </div>
        </div>
        
        <!-- 9 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 9</div>
            <div class="opp-title">La Re-Venta Automática (Ganar Dinero Extra)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Ese turista que ya viajó contigo a Cusco volverá a Perú pronto. Alíate con una agencia de la Selva o de Huaraz. A los 6 meses, mándale un saludito a tu cliente ofreciéndole esos nuevos destinos.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Ganas comisión por la recomendación sin haber movido un solo bus. Dinero pasivo.</div>
            </div>
        </div>

        <!-- 10 -->
        <div class="opp-card" style="border-top-color: #ec4899;">
            <div class="opp-number">💡 Oportunidad 10</div>
            <div class="opp-title">Libérate del Estrés Operativo Nocturno</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Un dueño de agencia estresado llamando buses a las 4 AM no tiene energía para hacer publicidad ni conseguir más clientes. ¡Esa es la peor trampa!</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Tú dedícate 100% a conversar con los clientes y cobrar paquetes Premium. <strong>Asóciate con Lifextreme:</strong> Nosotros ponemos las camionetas, los guías y operamos todo por ti en terreno.</div>
            </div>
        </div>
    </div>

    <div class="cta-box">
        <div class="cta-title">TRABAJA MÁS INTELIGENTE, NO MÁS DURO.</div>
        <p style="font-size: 15px; line-height: 1.6; margin-bottom: 0;">Aplicar estas 10 oportunidades puede transformar tu agencia en un negocio altamente rentable en pocas semanas. <strong>Lifextreme</strong> es tu socio ideal. Tú te encargas de enamorar al cliente y cerrar la venta, y nosotros hacemos que el tour sea mágico y perfecto en la vida real.</p>
    </div>

</body>
</html>
"""

async def generate_opp_pdf():
    print("Preparando Reporte Lúdico de Oportunidades...")
    html_path = os.path.abspath("temp_opp_dossier.html")
    pdf_path = os.path.abspath("Lifextreme_Las_10_Oportunidades.pdf")
    
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
        
    print(f"PDF Oportunidades generado correctamente en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_opp_pdf())
    except Exception as e:
        pass
