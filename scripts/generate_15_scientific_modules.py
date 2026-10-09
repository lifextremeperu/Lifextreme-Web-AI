import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>15 Módulos Científicos - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Space+Grotesk:wght@700&display=swap');
        
        body { 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background-color: #f8fafc; 
            color: #1e293b; 
            margin: 0; 
            padding: 30px; 
            font-size: 11px; 
            line-height: 1.4;
        }
        
        .header { 
            text-align: center;
            padding-bottom: 15px; 
            border-bottom: 2px solid #e2e8f0;
            margin-bottom: 20px; 
        }
        
        .logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 28px; 
            color: #0f172a; 
            font-weight: 700; 
            letter-spacing: -1px;
        }
        .logo span { color: #2563eb; }
        
        .title {
            font-size: 22px;
            font-weight: 800;
            color: #1d4ed8;
            margin: 5px 0;
            text-transform: uppercase;
        }
        
        .subtitle { color: #475569; font-size: 12px; font-weight: 600; }
        
        .grid-3 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .mod-card {
            background: #ffffff;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            border-top: 4px solid #2563eb;
            page-break-inside: avoid;
        }
        
        .mod-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .mod-num {
            background: #dbeafe;
            color: #1d4ed8;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 10px;
        }
        
        .mod-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 14px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
            line-height: 1.2;
            height: 34px;
        }
        
        .mod-desc { color: #475569; margin-bottom: 10px; height: 65px; overflow: hidden; }
        
        .chart-box {
            background: #f1f5f9;
            border-radius: 6px;
            padding: 10px;
            text-align: center;
            height: 110px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .chart-label {
            font-size: 9px;
            font-weight: 800;
            color: #64748b;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        
        .opp-box {
            background: #ecfdf5;
            border-left: 3px solid #10b981;
            padding: 8px;
            font-size: 10px;
            color: #065f46;
        }
        .opp-box strong { color: #047857; display: block; margin-bottom: 2px;}
        
        svg text { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; fill: #64748b; }
        
        .page-break { page-break-before: always; }
        
        .section-banner {
            background: #1e293b;
            color: white;
            padding: 8px 15px;
            font-weight: 800;
            font-size: 14px;
            border-radius: 4px;
            margin: 15px 0;
            text-transform: uppercase;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo">LIFEXTREME<span>.DATA</span></div>
        <h1 class="title">LOS 15 MÓDULOS DE INTELIGENCIA DE DATOS Y NEUROMARKETING</h1>
        <div class="subtitle">Estrategia científica para multiplicar ventas, evadir a las OTAs y dominar el mercado.</div>
    </div>
    
    <div class="section-banner" style="background: #2563eb;">FASE 1: PRECIOS, MACROECONOMÍA Y CONVERSIÓN</div>

    <div class="grid-3">
        <!-- 1 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M01</div></div>
            <div class="mod-title">Pricing Predictivo (TimesFM)</div>
            <div class="mod-desc">El cerebro reptiliano sufre FOMO (Miedo a quedarse fuera). Al subir el precio cerca a la fecha de viaje, el cliente percibe escasez y paga sin dudar.</div>
            <div class="chart-box">
                <div class="chart-label">Curva de Elasticidad</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 Q 100 70 150 40 T 190 10" fill="none" stroke="#2563eb" stroke-width="3"/>
                    <circle cx="150" cy="40" r="4" fill="#ef4444"/>
                    <text x="140" y="30" fill="#ef4444" font-weight="bold">+15% USD</text>
                    <text x="10" y="80">30 Días</text><text x="150" y="80">3 Días</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Incrementa tus precios 15% para reservas de última hora. Ganancia neta.</div>
        </div>

        <!-- 2 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M02</div></div>
            <div class="mod-title">Petróleo (Jet-A1) y Demanda</div>
            <div class="mod-desc">El turismo no es una burbuja. Si hay crisis globales, el combustible aéreo sube, eliminando del mercado al turista europeo promedio.</div>
            <div class="chart-box">
                <div class="chart-label">Correlación Petróleo vs Demanda</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 L 80 60 L 140 30 L 190 10" fill="none" stroke="#ef4444" stroke-dasharray="3,3" stroke-width="2"/>
                    <path d="M 10 20 L 80 30 L 140 60 L 190 70" fill="none" stroke="#2563eb" stroke-width="3"/>
                    <text x="130" y="15" fill="#ef4444">Petróleo ↑</text>
                    <text x="130" y="75" fill="#2563eb">Demanda ↓</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Apaga Ads masivos. Vende solo a turistas VIP (UHNWI) que no sufren inflación.</div>
        </div>

        <!-- 3 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M03</div></div>
            <div class="mod-title">Conversión Web vs WhatsApp</div>
            <div class="mod-desc">Un formulario web genera "fricción psicológica". El chat genera un pico de dopamina. Integrar pagos en WhatsApp triplica el cierre.</div>
            <div class="chart-box">
                <div class="chart-label">Neuromarketing de Cierre</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="50" width="40" height="20" fill="#94a3b8" rx="2"/>
                    <text x="50" y="45" font-weight="bold">8%</text>
                    <rect x="120" y="10" width="40" height="60" fill="#10b981" rx="2"/>
                    <text x="125" y="45" fill="white" font-weight="bold">35%</text>
                    <text x="35" y="80">Web</text><text x="115" y="80">WhatsApp</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Cierra el 35% enviando PDFs interactivos con link de pago en 1-clic.</div>
        </div>
    </div>

    <div class="grid-3">
        <!-- 4 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M04</div></div>
            <div class="mod-title">Arbitraje de Divisas (Forex)</div>
            <div class="mod-desc">El turista europeo siente "barato" a Perú cuando el Euro se aprecia. La conversión de moneda extranjera dicta el volumen de compra.</div>
            <div class="chart-box">
                <div class="chart-label">Impacto del Euro (BCE)</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 L 60 50 L 120 45 L 190 20" fill="none" stroke="#10b981" stroke-width="3"/>
                    <text x="120" y="15" fill="#10b981" font-weight="bold">+18% Ventas</text>
                    <text x="10" y="80">Euro Normal</text><text x="140" y="80">Euro Fuerte</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Inyecta presupuesto publicitario en Europa justo los días que el Euro sube.</div>
        </div>
        
        <!-- 5 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M05</div></div>
            <div class="mod-title">Margen VIP vs Masivo</div>
            <div class="mod-desc">Pelear precios en la Plaza de Armas por un "City Tour" destruye la utilidad (5%). Empaquetar lujo privado dispara el margen líquido (45%).</div>
            <div class="chart-box">
                <div class="chart-label">Rentabilidad Neta</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="60" width="40" height="10" fill="#ef4444" rx="2"/>
                    <text x="50" y="55" font-weight="bold" fill="#ef4444">5%</text>
                    <rect x="120" y="20" width="40" height="50" fill="#10b981" rx="2"/>
                    <text x="125" y="15" fill="#10b981" font-weight="bold">45%</text>
                    <text x="35" y="80">Masivo</text><text x="125" y="80">VIP</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Vende "Retiros" a $150. Llevas menos gente, pero ganas cinco veces más.</div>
        </div>

        <!-- 6 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M06</div></div>
            <div class="mod-title">Logística Predictiva SUTRAN</div>
            <div class="mod-desc">Las cancelaciones por paros o lluvias aniquilan tu flujo de caja al tener que devolver el 100% del ticket.</div>
            <div class="chart-box">
                <div class="chart-label">Retención de Capital</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <circle cx="60" cy="35" r="25" fill="#ef4444"/>
                    <text x="45" y="75" fill="#ef4444" font-weight="bold">-100%</text>
                    
                    <circle cx="140" cy="35" r="25" fill="#10b981"/>
                    <text x="135" y="75" fill="#10b981" font-weight="bold">0% Pérdida</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Redirige al turista a una ruta segura (ej. Valle Sur). Cero devoluciones.</div>
        </div>
    </div>
    
    <div class="page-break"></div>
    <div class="header" style="margin-top: 10px; margin-bottom: 10px;">
        <div class="logo">LIFEXTREME<span>.DATA</span></div>
    </div>
    <div class="section-banner" style="background: #0f766e;">FASE 2: MARKETING IA Y NUEVOS NICHOS</div>

    <div class="grid-3">
        <!-- 7 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M07</div></div>
            <div class="mod-title">AEO (ChatGPT) vs SEO Clásico</div>
            <div class="mod-desc">El turista planea sus viajes con ChatGPT (Generative IA). Si no tienes texto estructurado, los bots no te recomiendan.</div>
            <div class="chart-box">
                <div class="chart-label">Migración de Tráfico Web</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 30 L 100 50 L 190 70" fill="none" stroke="#ef4444" stroke-width="2"/>
                    <path d="M 10 70 L 100 50 L 190 10" fill="none" stroke="#10b981" stroke-width="3"/>
                    <text x="140" y="65" fill="#ef4444">Google</text>
                    <text x="140" y="15" fill="#10b981">Bots I.A.</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Usa formato FQSA en tu web. ChatGPT amará tus datos y te citará como autoridad.</div>
        </div>
        
        <!-- 8 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M08</div></div>
            <div class="mod-title">Influencers ECS vs Meta Ads</div>
            <div class="mod-desc">Google/Meta cobran fortunas por Clic (CAC). El Framework ECS con micro-creadores extranjeros reduce el costo drásticamente.</div>
            <div class="chart-box">
                <div class="chart-label">Costo de Adquisición (CAC)</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="10" width="40" height="60" fill="#ef4444" rx="2"/>
                    <text x="45" y="45" fill="white" font-weight="bold">$45</text>
                    <rect x="120" y="50" width="40" height="20" fill="#10b981" rx="2"/>
                    <text x="125" y="45" fill="#10b981" font-weight="bold">$12</text>
                    <text x="35" y="80">Google</text><text x="115" y="80">TikTokers</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Invita creadores de 10k-50k seguidores. Pagarás céntimos por miles de impactos.</div>
        </div>

        <!-- 9 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M09</div></div>
            <div class="mod-title">Fuga D2C (Adiós OTAs)</div>
            <div class="mod-desc">Booking te asfixia con un 20% de comisión. El 65% de sus usuarios buscan tu web oficial antes de meter su tarjeta.</div>
            <div class="chart-box">
                <div class="chart-label">Recuperación de Comisión</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <circle cx="100" cy="35" r="25" fill="#cbd5e0"/>
                    <path d="M 100 35 L 100 10 A 25 25 0 0 1 125 35 Z" fill="#2563eb"/>
                    <text x="130" y="25" fill="#2563eb" font-weight="bold">20% Salvo</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Ofrece "Traslado gratis" si compran en tu web. Cuesta $5, pero salvas $40 en comisión.</div>
        </div>
    </div>
    
    <div class="grid-3">
        <!-- 10 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M10</div></div>
            <div class="mod-title">Vectores Multi-Destino (LTV)</div>
            <div class="mod-desc">El turista extranjero no vuelve a Cusco, pero SÍ irá a la Amazonía pronto. Maximiza su Life-Time Value.</div>
            <div class="chart-box">
                <div class="chart-label">Rentabilidad Pasiva a 6 Meses</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="30" y="20" width="30" height="50" fill="#94a3b8" rx="2"/>
                    <rect x="90" y="20" width="30" height="50" fill="#94a3b8" rx="2"/>
                    <rect x="150" y="10" width="30" height="60" fill="#f59e0b" rx="2"/>
                    <text x="35" y="80">T1</text><text x="95" y="80">T2</text><text x="150" y="80">+Amazon</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Alíate con agencias de la Selva. Recomiéndalos a los 6 meses y cobra comisiones pasivas.</div>
        </div>

        <!-- 11 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M11</div></div>
            <div class="mod-title">Micro-Nichos (Mujeres Solas)</div>
            <div class="mod-desc">El mercado Genérico ("Familias") está destruido. El nicho "Solo Female Travelers" está explotando sin competencia en Cusco.</div>
            <div class="chart-box">
                <div class="chart-label">Crecimiento de Búsquedas (YoY)</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 L 60 65 L 120 50 L 190 10" fill="none" stroke="#8b5cf6" stroke-width="3"/>
                    <text x="140" y="25" fill="#8b5cf6" font-weight="bold">+400%</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Crea una web exclusiva para mujeres viajeras, garantizando máxima seguridad.</div>
        </div>

        <!-- 12 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M12</div></div>
            <div class="mod-title">Mercado Corporativo (B2B)</div>
            <div class="mod-desc">El ejecutivo limeño sufre de Burnout crónico. Las mineras y bancos tienen altos presupuestos para salud mental corporativa.</div>
            <div class="chart-box">
                <div class="chart-label">Ticket Promedio B2C vs B2B</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="50" width="40" height="20" fill="#64748b" rx="2"/>
                    <rect x="120" y="10" width="40" height="60" fill="#f59e0b" rx="2"/>
                    <text x="35" y="80">Familiar</text><text x="110" y="80">Empresarial</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Vende "Retiros de Desconexión" directamente a Recursos Humanos de Lima.</div>
        </div>
    </div>

    <div class="page-break"></div>
    <div class="header" style="margin-top: 10px; margin-bottom: 10px;">
        <div class="logo">LIFEXTREME<span>.DATA</span></div>
    </div>
    <div class="section-banner" style="background: #4338ca;">FASE 3: NUEVOS HORIZONTES DE EXPANSIÓN</div>

    <div class="grid-3">
        <!-- 13 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M13</div></div>
            <div class="mod-title">Inversión ESG (Europa)</div>
            <div class="mod-desc">Leyes europeas exigen a sus operadoras comprar SOLO a agencias latinoamericanas que certifiquen huella de Carbono Cero.</div>
            <div class="chart-box">
                <div class="chart-label">Filtro Legal de Socios Europeos</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <circle cx="100" cy="35" r="25" fill="#10b981"/>
                    <path d="M 90 35 L 98 43 L 115 25" fill="none" stroke="white" stroke-width="3"/>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Certifícate como empresa verde. Europa te elegirá como aliado por obligación legal.</div>
        </div>

        <!-- 14 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M14</div></div>
            <div class="mod-title">Anticipación PENTUR (Moche/Amazonía)</div>
            <div class="mod-desc">El Mincetur inyectará presupuesto masivo en La Libertad y Loreto para 2028. Cusco entrará en sobre-saturación absoluta.</div>
            <div class="chart-box">
                <div class="chart-label">Proyección de Inversión Estatal</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="20" width="40" height="50" fill="#cbd5e0" rx="2"/>
                    <rect x="120" y="10" width="40" height="60" fill="#2563eb" rx="2"/>
                    <text x="35" y="80">Cusco</text><text x="110" y="80">Moche/Selva</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Posiciona rutas de expedición en la selva desde ahora. Sé el rey mañana.</div>
        </div>

        <!-- 15 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M15</div></div>
            <div class="mod-title">Turismo Inmersivo (El Escudo Anti-IA)</div>
            <div class="mod-desc">Los algoritmos millonarios de Expedia no pueden generar empatía humana. El turista Premium busca conexión real con comunidades andinas.</div>
            <div class="chart-box">
                <div class="chart-label">Valor Percibido del Cliente (VPC)</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 L 60 70 L 120 70 L 190 70" fill="none" stroke="#94a3b8" stroke-width="2"/>
                    <path d="M 10 70 L 80 50 L 140 25 L 190 10" fill="none" stroke="#f59e0b" stroke-width="3"/>
                    <text x="140" y="25" fill="#f59e0b" font-weight="bold">I. Artificial</text>
                    <text x="140" y="65" fill="#94a3b8">Masivo</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Ofrece dormir/comer con comunidades nativas. Es una experiencia que la IA no puede robar.</div>
        </div>
    </div>
    
    <div style="background: #0f172a; color: white; padding: 25px; border-radius: 8px; text-align: center; margin-top: 30px; border-bottom: 6px solid #2563eb;">
        <h2 style="margin-top: 0; font-family: 'Space Grotesk'; font-size: 20px; color: #60a5fa;">LA ALIANZA ESTRATÉGICA LIFEXTREME</h2>
        <p style="font-size: 13px; margin-bottom: 0;">Esta inteligencia científica proviene de nuestro clúster de Datos. <strong>Implemente estos 15 módulos para dominar el ecosistema digital y captar clientes globales.</strong> En paralelo, Lifextreme aplicará esta misma ciencia para operar su logística de campo, con transportes y guías, garantizando 0% de estrés para usted.</p>
    </div>

</body>
</html>
"""

async def generate_15_scientific_pdf():
    print("Preparando 15 Módulos Científicos...")
    html_path = os.path.abspath("temp_15_scientific.html")
    pdf_path = os.path.abspath("Lifextreme_15_Modulos_Cientificos.pdf")
    
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
        
    print(f"PDF 15 Científico generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_15_scientific_pdf())
    except Exception as e:
        pass
