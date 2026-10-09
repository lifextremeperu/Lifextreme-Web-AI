import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Hoja de Ruta PYMES - Lifextreme</title>
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
        .logo span { color: #f59e0b; }
        
        .title {
            font-size: 20px;
            font-weight: 800;
            color: #d97706;
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
            border-top: 4px solid #f59e0b;
            page-break-inside: avoid;
        }
        
        .mod-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .mod-num {
            background: #fef3c7;
            color: #d97706;
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
            background: #fffbeb;
            border-left: 3px solid #f59e0b;
            padding: 8px;
            font-size: 10px;
            color: #92400e;
        }
        .opp-box strong { color: #b45309; display: block; margin-bottom: 2px;}
        
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
        <div class="logo">LIFEXTREME<span>.PYME</span></div>
        <h1 class="title">HOJA DE RUTA Y BUSINESS INTELLIGENCE PARA PYMES TURÍSTICAS</h1>
        <div class="subtitle">Cómo pasar de Agencia Pequeña a Corporación: Legalidad, Mincetur y Multiplicación de Ganancias.</div>
    </div>
    
    <div class="section-banner" style="background: #f59e0b;">FASE 1: RENTABILIDAD PURA (VENDER MÁS CON MENOS ESFUERZO)</div>

    <div class="grid-3">
        <!-- 1 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M01</div></div>
            <div class="mod-title">Pricing Predictivo (Ganar en Urgencia)</div>
            <div class="mod-desc">Tu PYME cobra igual todo el año. El cerebro reptiliano sufre FOMO (Miedo a quedarse sin lugar). Si le subes el precio a quien reserva faltando 3 días, pagará sin dudar.</div>
            <div class="chart-box">
                <div class="chart-label">Curva de Utilidad PYME</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 Q 100 70 150 40 T 190 10" fill="none" stroke="#f59e0b" stroke-width="3"/>
                    <circle cx="150" cy="40" r="4" fill="#ef4444"/>
                    <text x="140" y="30" fill="#ef4444" font-weight="bold">+15% USD</text>
                    <text x="10" y="80">30 Días</text><text x="150" y="80">3 Días</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> No malbarates a última hora. Incrementa tus precios 15% a los clientes apresurados.</div>
        </div>

        <!-- 2 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M02</div></div>
            <div class="mod-title">Petróleo (No quemes tu presupuesto)</div>
            <div class="mod-desc">El combustible dicta si el turista normal viajará a Cusco. Si el barril sube, los vuelos suben y el turista promedio cancela.</div>
            <div class="chart-box">
                <div class="chart-label">Cuándo invertir en Ads</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 L 80 60 L 140 30 L 190 10" fill="none" stroke="#ef4444" stroke-dasharray="3,3" stroke-width="2"/>
                    <path d="M 10 20 L 80 30 L 140 60 L 190 70" fill="none" stroke="#f59e0b" stroke-width="3"/>
                    <text x="130" y="15" fill="#ef4444">Petróleo ↑</text>
                    <text x="130" y="75" fill="#f59e0b">Demanda ↓</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Si el petróleo sube, apaga tus anuncios de Facebook para mochileros. Solo pauta a millonarios.</div>
        </div>

        <!-- 3 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M03</div></div>
            <div class="mod-title">Cierre por WhatsApp (El Fin del Formulario)</div>
            <div class="mod-desc">Una PYME no necesita una página web de $10,000 USD. Los formularios aburren. El turista quiere chat, PDF rápido y link de pago.</div>
            <div class="chart-box">
                <div class="chart-label">Neuromarketing de Cierre B2C</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="50" width="40" height="20" fill="#94a3b8" rx="2"/>
                    <text x="50" y="45" font-weight="bold">8%</text>
                    <rect x="120" y="10" width="40" height="60" fill="#10b981" rx="2"/>
                    <text x="125" y="45" fill="white" font-weight="bold">35%</text>
                    <text x="35" y="80">Formulario</text><text x="115" y="80">WhatsApp</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Usa Links de Niubiz en tu WhatsApp. Cierra la venta en 1-clic mientras el cliente está emocionado.</div>
        </div>
    </div>

    <div class="grid-3">
        <!-- 4 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M04</div></div>
            <div class="mod-title">Arbitraje de Divisas (Apunta a Europa)</div>
            <div class="mod-desc">Cuando el Euro sube, el europeo siente que Perú es baratísimo. Una PYME astuta monitorea esto.</div>
            <div class="chart-box">
                <div class="chart-label">Rentabilidad del Presupuesto Ads</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 L 60 50 L 120 45 L 190 20" fill="none" stroke="#10b981" stroke-width="3"/>
                    <text x="120" y="15" fill="#10b981" font-weight="bold">+18% Ventas</text>
                    <text x="10" y="80">Euro Débil</text><text x="140" y="80">Euro Fuerte</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Pon tus $50 de pauta publicitaria en Europa solo los días que el Euro amanece en alza.</div>
        </div>
        
        <!-- 5 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M05</div></div>
            <div class="mod-title">Margen VIP vs Guerra de Plazas</div>
            <div class="mod-desc">Para una agencia pequeña, pelear precios en la calle te llevará a la quiebra. Empaquetar lujo te da oxígeno financiero.</div>
            <div class="chart-box">
                <div class="chart-label">El Océano Rojo de la Plaza de Armas</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="60" width="40" height="10" fill="#ef4444" rx="2"/>
                    <text x="50" y="55" font-weight="bold" fill="#ef4444">5%</text>
                    <rect x="120" y="20" width="40" height="50" fill="#10b981" rx="2"/>
                    <text x="125" y="15" fill="#10b981" font-weight="bold">45%</text>
                    <text x="35" y="80">Masivo ($20)</text><text x="125" y="80">VIP ($150)</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Vende 1 tour privado a $150. Ganarás lo mismo que vendiendo 30 tours baratos, con cero estrés.</div>
        </div>

        <!-- 6 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M06</div></div>
            <div class="mod-title">Logística Predictiva (Cero Devoluciones)</div>
            <div class="mod-desc">Una sola lluvia o huelga en Vinicunca te hace devolver dinero que ya no tienes.</div>
            <div class="chart-box">
                <div class="chart-label">Blindaje de la Caja Chica PYME</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <circle cx="60" cy="35" r="25" fill="#ef4444"/>
                    <text x="45" y="75" fill="#ef4444" font-weight="bold">-100%</text>
                    
                    <circle cx="140" cy="35" r="25" fill="#10b981"/>
                    <text x="135" y="75" fill="#10b981" font-weight="bold">0% Pérdida</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Desvía automáticamente a tus turistas hacia el Valle Sur si el clima falla. Mantienes el dinero en casa.</div>
        </div>
    </div>
    
    <div class="page-break"></div>
    <div class="header" style="margin-top: 10px; margin-bottom: 10px;">
        <div class="logo">LIFEXTREME<span>.PYME</span></div>
    </div>
    <div class="section-banner" style="background: #10b981;">FASE 2: CERTIFICACIÓN Y ESTRATEGIA CORPORATIVA</div>

    <div class="grid-3">
        <!-- 7 NUEVO: MINCETUR E ISOs -->
        <div class="mod-card" style="border-top-color: #10b981;">
            <div class="mod-header"><div class="mod-num" style="background: #d1fae5; color: #047857;">M07</div></div>
            <div class="mod-title">Formalización (MINCETUR e ISOs)</div>
            <div class="mod-desc">El cliente extranjero B2B (Agencias Europeas) exige papeles. Si no estás en el Directorio Nacional Mincetur o no aspiras al ISO 9001/14001, nadie grande te contratará.</div>
            <div class="chart-box">
                <div class="chart-label">Ruta de Confianza B2B</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 20 40 L 70 40 L 120 40 L 170 40" stroke="#94a3b8" stroke-width="2" stroke-dasharray="2,2"/>
                    <circle cx="20" cy="40" r="10" fill="#94a3b8"/>
                    <circle cx="95" cy="40" r="12" fill="#3b82f6"/>
                    <circle cx="170" cy="40" r="15" fill="#10b981"/>
                    <text x="10" y="65">PYME</text><text x="75" y="65">DIRCETUR</text><text x="150" y="65">ISO 9001</text>
                </svg>
            </div>
            <div class="opp-box"><strong style="color: #047857;">OPORTUNIDAD:</strong> Inicia el trámite de Constancia Dircetur. Es el primer paso para ganar licitaciones millonarias.</div>
        </div>
        
        <!-- 8 -->
        <div class="mod-card" style="border-top-color: #10b981;">
            <div class="mod-header"><div class="mod-num" style="background: #d1fae5; color: #047857;">M08</div></div>
            <div class="mod-title">AEO (ChatGPT) vs SEO de Google</div>
            <div class="mod-desc">El turista planea sus viajes con ChatGPT. Como PYME, no puedes vencer a Tripadvisor en Google, pero SÍ puedes ganarle en ChatGPT.</div>
            <div class="chart-box">
                <div class="chart-label">Oportunidad para Agencias Pequeñas</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 30 L 100 50 L 190 70" fill="none" stroke="#ef4444" stroke-width="2"/>
                    <path d="M 10 70 L 100 50 L 190 10" fill="none" stroke="#10b981" stroke-width="3"/>
                    <text x="140" y="65" fill="#ef4444">Google (OTAs)</text>
                    <text x="140" y="15" fill="#10b981">ChatGPT (AEO)</text>
                </svg>
            </div>
            <div class="opp-box"><strong style="color: #047857;">OPORTUNIDAD:</strong> Escribe FAQs súper claras en tu web. ChatGPT tomará tu data y te pondrá primero.</div>
        </div>

        <!-- 9 -->
        <div class="mod-card" style="border-top-color: #10b981;">
            <div class="mod-header"><div class="mod-num" style="background: #d1fae5; color: #047857;">M09</div></div>
            <div class="mod-title">Influencers Extranjeros vs Ads</div>
            <div class="mod-desc">Pagar miles en Facebook te arruina. Como PYME, invita a un creador extranjero de TikTok con 10k seguidores a un tour gratis.</div>
            <div class="chart-box">
                <div class="chart-label">Costo de Adquisición (CAC PYME)</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="10" width="40" height="60" fill="#ef4444" rx="2"/>
                    <text x="45" y="45" fill="white" font-weight="bold">$45</text>
                    <rect x="120" y="50" width="40" height="20" fill="#10b981" rx="2"/>
                    <text x="125" y="45" fill="#10b981" font-weight="bold">$12</text>
                    <text x="35" y="80">Facebook</text><text x="115" y="80">TikToker</text>
                </svg>
            </div>
            <div class="opp-box"><strong style="color: #047857;">OPORTUNIDAD:</strong> Es el trueque moderno. Costo cero, exposición mundial a su comunidad específica.</div>
        </div>
    </div>
    
    <div class="grid-3">
        <!-- 10 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M10</div></div>
            <div class="mod-title">Recuperar Dinero de OTAs (Booking)</div>
            <div class="mod-desc">Viator/Booking te roban el 20%. Muchos turistas buscan tu PYME en Google antes de pagar. Atrápalos ahí.</div>
            <div class="chart-box">
                <div class="chart-label">Recuperación de Margen</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <circle cx="100" cy="35" r="25" fill="#cbd5e0"/>
                    <path d="M 100 35 L 100 10 A 25 25 0 0 1 125 35 Z" fill="#f59e0b"/>
                    <text x="130" y="25" fill="#f59e0b" font-weight="bold">20% Salvo</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Pon en tu web "Traslado al aeropuerto GRATIS si reservas al WhatsApp". Salvas miles de dólares.</div>
        </div>

        <!-- 11 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M11</div></div>
            <div class="mod-title">Comisiones Automáticas (LTV)</div>
            <div class="mod-desc">El turista se va de Cusco, pero irá a la Amazonía. ¿Por qué dejar de ganar dinero de él?</div>
            <div class="chart-box">
                <div class="chart-label">Dinero Pasivo de Ex-Clientes</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="30" y="20" width="30" height="50" fill="#94a3b8" rx="2"/>
                    <rect x="90" y="20" width="30" height="50" fill="#94a3b8" rx="2"/>
                    <rect x="150" y="10" width="30" height="60" fill="#f59e0b" rx="2"/>
                    <text x="35" y="80">Cusco</text><text x="95" y="80">Post</text><text x="150" y="80">+Selva</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Alíate con una PYME en Iquitos. Véndele a tu base de datos pasada y cobra 10% pasivo.</div>
        </div>

        <!-- 12 -->
        <div class="mod-card">
            <div class="mod-header"><div class="mod-num">M12</div></div>
            <div class="mod-title">El Micro-Nicho (Tu Mina de Oro)</div>
            <div class="mod-desc">No puedes competir vendiendo a "familias". Enfócate en Mujeres Viajando Solas (Solo Female Travelers).</div>
            <div class="chart-box">
                <div class="chart-label">Crecimiento del Nicho Femenino</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 L 60 65 L 120 50 L 190 10" fill="none" stroke="#f59e0b" stroke-width="3"/>
                    <text x="140" y="25" fill="#f59e0b" font-weight="bold">+400%</text>
                </svg>
            </div>
            <div class="opp-box"><strong>OPORTUNIDAD:</strong> Promete guías mujeres y máxima seguridad. Dominarás el nicho en Cusco al instante.</div>
        </div>
    </div>

    <div class="page-break"></div>
    <div class="header" style="margin-top: 10px; margin-bottom: 10px;">
        <div class="logo">LIFEXTREME<span>.PYME</span></div>
    </div>
    <div class="section-banner" style="background: #2563eb;">FASE 3: NUEVOS HORIZONTES DE EXPANSIÓN B2B</div>

    <div class="grid-3">
        <!-- 13 -->
        <div class="mod-card" style="border-top-color: #2563eb;">
            <div class="mod-header"><div class="mod-num" style="background: #dbeafe; color: #1d4ed8;">M13</div></div>
            <div class="mod-title">Mercado Corporativo Peruano</div>
            <div class="mod-desc">Los ejecutivos en Lima tienen estrés crónico (Burnout). Recursos Humanos tiene presupuestos anuales para "Team Buildings".</div>
            <div class="chart-box">
                <div class="chart-label">Ticket B2C vs B2B Corporativo</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="50" width="40" height="20" fill="#64748b" rx="2"/>
                    <rect x="120" y="10" width="40" height="60" fill="#2563eb" rx="2"/>
                    <text x="35" y="80">Gringo B2C</text><text x="110" y="80">Empresa B2B</text>
                </svg>
            </div>
            <div class="opp-box"><strong style="color: #1d4ed8;">OPORTUNIDAD:</strong> Ofrece "Retiros de Desconexión" corporativos facturando al por mayor en temporada baja.</div>
        </div>

        <!-- 14 -->
        <div class="mod-card" style="border-top-color: #2563eb;">
            <div class="mod-header"><div class="mod-num" style="background: #dbeafe; color: #1d4ed8;">M14</div></div>
            <div class="mod-title">Anticiparse al PENTUR (Moche/Amazonía)</div>
            <div class="mod-desc">El Mincetur inyectará presupuesto gigante en el norte y la selva para 2028. Cusco entrará en sobre-saturación absoluta de PYMES.</div>
            <div class="chart-box">
                <div class="chart-label">Inversión Estatal a Futuro</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <rect x="40" y="20" width="40" height="50" fill="#cbd5e0" rx="2"/>
                    <rect x="120" y="10" width="40" height="60" fill="#2563eb" rx="2"/>
                    <text x="35" y="80">Cusco</text><text x="110" y="80">Moche/Selva</text>
                </svg>
            </div>
            <div class="opp-box"><strong style="color: #1d4ed8;">OPORTUNIDAD:</strong> Usa a Lifextreme para abrir operación remota en Loreto hoy. Sé el rey mañana.</div>
        </div>

        <!-- 15 -->
        <div class="mod-card" style="border-top-color: #2563eb;">
            <div class="mod-header"><div class="mod-num" style="background: #dbeafe; color: #1d4ed8;">M15</div></div>
            <div class="mod-title">El Escudo Anti-Robot (Turismo Inmersivo)</div>
            <div class="mod-desc">Las grandes plataformas usan IA. Pero un robot jamás podrá organizar a un turista durmiendo en casa de un campesino andino.</div>
            <div class="chart-box">
                <div class="chart-label">Inmunidad Tecnológica de la PYME</div>
                <svg viewBox="0 0 200 80" width="100%" height="60">
                    <path d="M 10 70 L 60 70 L 120 70 L 190 70" fill="none" stroke="#94a3b8" stroke-width="2"/>
                    <path d="M 10 70 L 80 50 L 140 25 L 190 10" fill="none" stroke="#2563eb" stroke-width="3"/>
                    <text x="140" y="25" fill="#2563eb" font-weight="bold">I. Artificial</text>
                    <text x="140" y="65" fill="#94a3b8">Experiencia Local</text>
                </svg>
            </div>
            <div class="opp-box"><strong style="color: #1d4ed8;">OPORTUNIDAD:</strong> Lo rústico y lo humano es el nuevo lujo. El turista VIP paga fortunas por lo auténtico.</div>
        </div>
    </div>
    
    <div style="background: #0f172a; color: white; padding: 25px; border-radius: 8px; text-align: center; margin-top: 30px; border-bottom: 6px solid #f59e0b;">
        <h2 style="margin-top: 0; font-family: 'Space Grotesk'; font-size: 20px; color: #f59e0b;">TERCERIZA EL ESTRÉS. MAXIMIZA EL INGRESO.</h2>
        <p style="font-size: 13px; margin-bottom: 0;"><strong>El dueño de una PYME debe estar dedicado 100% a aplicar estas estrategias, a formalizarse (Mincetur/ISOs) y a vender Alto Ticket.</strong> Si se queda despierto a las 4 AM coordinando buses, su agencia quebrará. Alíese con <strong>Lifextreme</strong>: Nosotros somos su "Departamento Operativo Externo". Nosotros ponemos el bus, el guía y absorbemos el estrés logístico de terreno.</p>
    </div>

</body>
</html>
"""

async def generate_pymes_roadmap_pdf():
    print("Preparando Hoja de Ruta B2B para PYMES...")
    html_path = os.path.abspath("temp_pymes_roadmap.html")
    pdf_path = os.path.abspath("Lifextreme_Hoja_De_Ruta_PYMES.pdf")
    
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
        
    print(f"PDF PYMES generado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_pymes_roadmap_pdf())
    except Exception as e:
        pass
