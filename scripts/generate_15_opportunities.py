import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>15 Oportunidades - Agencias Cusco</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap');
        
        body { 
            font-family: 'Poppins', sans-serif; 
            background-color: #f8fafc; 
            color: #334155; 
            margin: 0; 
            padding: 30px; 
            font-size: 12px; 
            line-height: 1.5;
        }
        
        .header { 
            text-align: center;
            padding-bottom: 20px; 
            margin-bottom: 25px; 
        }
        
        .logo {
            font-size: 28px; 
            color: #0f172a; 
            font-weight: 900; 
            letter-spacing: -1px;
        }
        
        .logo span { color: #f59e0b; }
        
        .title {
            font-size: 30px;
            font-weight: 900;
            color: #2563eb;
            margin: 10px 0;
            line-height: 1.1;
        }
        
        .subtitle {
            color: #475569;
            font-size: 14px;
            font-weight: 500;
        }
        
        .section-header {
            background: #2563eb;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 16px;
            margin-top: 20px;
            margin-bottom: 20px;
            text-align: center;
            text-transform: uppercase;
        }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px; }
        
        .opp-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            position: relative;
            page-break-inside: avoid;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            border-top: 4px solid #2563eb;
        }
        
        .opp-number {
            background: #fef3c7;
            color: #d97706;
            font-weight: 900;
            font-size: 14px;
            padding: 4px 10px;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 8px;
        }
        
        .opp-title {
            font-size: 15px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 12px;
            line-height: 1.2;
        }
        
        .section-box {
            background: #f1f5f9;
            padding: 10px 12px;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        
        .section-label {
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            color: #2563eb;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
        }
        
        .result-box {
            background: #ecfdf5;
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px dashed #10b981;
        }
        
        .result-label {
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            color: #059669;
            margin-bottom: 4px;
        }
        
        .cta-box {
            background: linear-gradient(135deg, #1e40af, #2563eb);
            color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            margin-top: 30px;
            page-break-inside: avoid;
            box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
        }
        
        .cta-title {
            font-size: 20px;
            font-weight: 900;
            margin-bottom: 10px;
        }
        
        .page-break { page-break-before: always; }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo">LIFEXTREME<span>.B2B</span></div>
        <h1 class="title">LAS 15 OPORTUNIDADES DE ORO</h1>
        <div class="subtitle">Guía táctica para multiplicar ganancias y expandir tus horizontes frente a las grandes OTAs.</div>
    </div>

    <div class="section-header">MÓDULO I: CÓMO MAXIMIZAR LAS VENTAS DE HOY</div>

    <div class="grid-2">
        <!-- 1 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 1</div>
            <div class="opp-title">Precios Inteligentes (Cobrar más por urgencia)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Si un turista te escribe faltando 3 días para su viaje, súbele el precio al tour un 15%. Tienen urgencia y pagarán felices, igual que con las aerolíneas.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Más dinero en tu bolsillo por exactamente el mismo esfuerzo de siempre.</div>
            </div>
        </div>

        <!-- 2 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 2</div>
            <div class="opp-title">El Turista Europeo y su "Moneda Fuerte"</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Cuando el Euro vale más, el europeo siente que Perú está "baratísimo". Lanza tus ofertas en Europa exactamente esos días.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Atraes clientes que tienen dinero de sobra y no te pedirán rebajas.</div>
            </div>
        </div>

        <!-- 3 -->
        <div class="opp-card" style="border-top-color: #f59e0b;">
            <div class="opp-number">💡 Oportunidad 3</div>
            <div class="opp-title">Cobrar Caro por Exclusividad VIP</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Hay turistas que huyen de lo barato. Crea un tour "VIP Secreto" a $150 incluyendo cosas simples pero hermosas (ej. picnic privado). Cero descuentos.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Llevas menos gente, trabajas menos estrés, pero multiplicas tu ganancia.</div>
            </div>
        </div>

        <!-- 4 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 4</div>
            <div class="opp-title">Cierre de Ventas Mágico por WhatsApp</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>La gente es impaciente. Mándales un PDF interactivo por WhatsApp con un link de pago directo (Yape o Niubiz) en vez de correos largos.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Tus clientes pagan desde su celular en 2 minutos antes de arrepentirse.</div>
            </div>
        </div>
    </div>
    
    <div class="grid-2">
        <!-- 5 -->
        <div class="opp-card" style="border-top-color: #10b981;">
            <div class="opp-number">💡 Oportunidad 5</div>
            <div class="opp-title">Salvar la Venta (Cero devoluciones por clima)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>¿Está lloviendo en Vinicunca? ¡No devuelvas la plata! Ofréceles un "Cambio a Ruta Segura" llevándolos a Palccoyo donde hay sol.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>El turista viaja feliz y tu dinero no se escapa de tu caja fuerte.</div>
            </div>
        </div>

        <!-- 6 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 6</div>
            <div class="opp-title">Dile Adiós a la Comisión de Booking</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Booking te quita el 20%. En tu página pon un letrero enorme: <em>"Reserva directo por WhatsApp y gana un premio sorpresa o traslado gratis"</em>.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>El traslado te cuesta poco, pero recuperas ese 20% gigante.</div>
            </div>
        </div>
        
        <!-- 7 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 7</div>
            <div class="opp-title">Vender Paz Mental (Y derribar miedos)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Muchos turistas no compran por miedo a la altura. Escribe en tu web: <em>"No le temas a la altura, tenemos oxígeno a bordo"</em>.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Le das tranquilidad inmediata al indeciso y te compran a ti sin dudar.</div>
            </div>
        </div>

        <!-- 8 -->
        <div class="opp-card" style="border-top-color: #8b5cf6;">
            <div class="opp-number">💡 Oportunidad 8</div>
            <div class="opp-title">Mini-Influencers y el Efecto TikTok</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Pagar publicidad aburre. Invita a viajar a creadores extranjeros jóvenes con pocos pero fieles seguidores (10k a 50k).</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>No gastas casi nada y sus seguidores querrán el tour exactamente igual.</div>
            </div>
        </div>
        
        <!-- 9 -->
        <div class="opp-card">
            <div class="opp-number">💡 Oportunidad 9</div>
            <div class="opp-title">La Re-Venta Automática de por vida</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Ese turista de Cusco viajará a otro lugar pronto. Alíate con una agencia de la Selva. Mándale un saludo al turista meses después recomendándole a tu aliado.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Ganas comisión por la recomendación sin haber movido un solo bus.</div>
            </div>
        </div>

        <!-- 10 -->
        <div class="opp-card" style="border-top-color: #ec4899;">
            <div class="opp-number">💡 Oportunidad 10</div>
            <div class="opp-title">Libérate del Estrés Operativo Nocturno</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Un dueño estresado llamando buses de madrugada no tiene tiempo para vender. ¡Esa es tu peor trampa! Terceriza tu logística.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Tú te dedicas 100% a conversar y vender caro. Lifextreme pone los buses y opera todo por ti.</div>
            </div>
        </div>
    </div>
    
    <div class="page-break"></div>
    
    <div class="header" style="margin-top: 15px; margin-bottom: 10px; padding-bottom: 5px;">
        <div class="logo">LIFEXTREME<span>.B2B</span></div>
    </div>
    
    <div class="section-header" style="background: #047857; margin-top: 10px;">MÓDULO II: NUEVOS HORIZONTES (CÓMO NO SER DEVORADO POR LA I.A.)</div>
    <p style="text-align: center; font-weight: 500; font-size: 13px; color: #475569; margin-bottom: 20px;">Las grandes OTAs (Expedia, TripAdvisor) están usando robots millonarios. Para no desaparecer, tienes que moverte a donde sus robots no llegan. Aquí tienes 5 formas de crecer.</p>

    <div class="grid-2">
        <!-- 11 -->
        <div class="opp-card" style="border-top-color: #047857;">
            <div class="opp-number">💡 Oportunidad 11</div>
            <div class="opp-title">Atacar un Mercado en Crecimiento Extremo</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Las agencias gigantes venden a "Familias". Tú enfócate en el mercado que más crece en el mundo hoy: <strong>Mujeres Viajando Solas (Solo Female Travelers).</strong> Diseña una página web exclusiva solo para ellas, garantizando guías mujeres y máxima seguridad.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Te conviertes en la agencia número 1 del Perú para mujeres extranjeras. Cero competencia y alta rentabilidad.</div>
            </div>
        </div>

        <!-- 12 -->
        <div class="opp-card" style="border-top-color: #047857;">
            <div class="opp-number">💡 Oportunidad 12</div>
            <div class="opp-title">Explorar Nuevos Mercados Nacionales (Corporativo)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>No persigas solo a gringos. Las grandes empresas en Lima (bancos, mineras) tienen ejecutivos con muchísimo estrés crónico (Burnout). Véndeles "Retiros de Desconexión Digital" de fin de semana exclusivos para sus empleados.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Abres un mercado B2B Nacional que paga carísimo por proteger la salud mental de su equipo directivo.</div>
            </div>
        </div>

        <!-- 13 -->
        <div class="opp-card" style="border-top-color: #047857;">
            <div class="opp-number">💡 Oportunidad 13</div>
            <div class="opp-title">Oportunidades de Inversión Verde (Bonos Europeos)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Las leyes en Europa ahora obligan a sus agencias a comprar tours solo a empresas ecológicas. Invierte un poco de tus ganancias en un certificado de "Huella de Carbono Cero" o de protección de bosques amazónicos.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Cuando una agencia francesa gigante busque aliado en Cusco, te elegirá a ti porque le ayudas a cumplir sus requisitos legales europeos.</div>
            </div>
        </div>

        <!-- 14 -->
        <div class="opp-card" style="border-top-color: #047857;">
            <div class="opp-number">💡 Oportunidad 14</div>
            <div class="opp-title">Diseño de Nuevas Rutas (Anticiparse al PENTUR)</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Cusco y Machu Picchu están bellos, pero saturados. El Gobierno peruano inyectará millones en la <strong>Ruta Moche (La Libertad) y Turismo Amazónico (Loreto)</strong>. Diseña desde hoy un pequeño tour de expedición hacia la selva virgen de la mano de Lifextreme.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Cuando el mundo vuelva los ojos a la Amazonía peruana, tú ya serás el rey de esa ruta.</div>
            </div>
        </div>
        
        <!-- 15 -->
        <div class="opp-card" style="border-top-color: #047857; grid-column: 1 / -1;">
            <div class="opp-number">💡 Oportunidad 15</div>
            <div class="opp-title">El Horizonte Anti-IA: El Turismo Comunitario Inmersivo</div>
            <div class="section-box">
                <div class="section-label">🎯 CÓMO APROVECHARLA:</div>
                <div>Los robots de Expedia pueden vender un ticket de avión barato, pero jamás podrán vender la sensación de cosechar papas con una familia andina en las alturas del Valle Sagrado. Empieza a diseñar convenios con comunidades alejadas para que el turista duerma y coma con ellos. Es una experiencia 100% humana y emocional.</div>
            </div>
            <div class="result-box">
                <div class="result-label">💰 RESULTADO:</div>
                <div>Blindas tu agencia para el futuro. Ninguna Inteligencia Artificial podrá copiar ni abaratar una experiencia de conexión humana pura. El turista pagará cualquier precio por vivir algo auténtico que el internet no le puede dar.</div>
            </div>
        </div>
    </div>

    <div class="cta-box">
        <div class="cta-title">TÚ ENAMORAS AL CLIENTE. NOSOTROS HACEMOS QUE PASE.</div>
        <p style="font-size: 15px; line-height: 1.6; margin-bottom: 0;">Aplicar estas 15 oportunidades puede convertir tu agencia en una potencia inalcanzable para la competencia local. <strong>Lifextreme</strong> es tu socio ideal. Dedícate a vender estos nuevos horizontes y nosotros operaremos la logística en el mundo real.</p>
    </div>

</body>
</html>
"""

async def generate_opp_15_pdf():
    print("Preparando Reporte de 15 Oportunidades (Con Nuevos Horizontes)...")
    html_path = os.path.abspath("temp_opp_15.html")
    pdf_path = os.path.abspath("Lifextreme_Las_15_Oportunidades.pdf")
    
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
        
    print(f"PDF 15 Oportunidades generado correctamente en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_opp_15_pdf())
    except Exception as e:
        pass
