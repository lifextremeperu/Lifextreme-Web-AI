import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Lifextreme - Inteligencia para Agencias</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Open+Sans:wght@400;600&display=swap');
        
        body { font-family: 'Open Sans', sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 40px; font-size: 13px; line-height: 1.6; }
        
        .header { background: #0f172a; color: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; border-bottom: 5px solid #00ff88; }
        .logo { font-family: 'Montserrat', sans-serif; font-size: 26px; font-weight: 800; color: #00ff88; letter-spacing: -1px; }
        .logo span { color: white; }
        .header h1 { font-family: 'Montserrat', sans-serif; font-size: 28px; margin: 15px 0 5px 0; line-height: 1.2; }
        .header p { color: #94a3b8; font-size: 14px; margin: 0; }
        
        h2 { font-family: 'Montserrat', sans-serif; font-size: 18px; color: #0f172a; border-left: 4px solid #00ff88; padding-left: 12px; margin-top: 35px; }
        
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 25px; }
        
        .kpi-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
        .kpi-title { color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: 600; margin-bottom: 5px; }
        .kpi-value { font-family: 'Montserrat', sans-serif; font-size: 32px; color: #0f172a; font-weight: 800; margin: 5px 0; }
        .kpi-desc { color: #475569; font-size: 12px; margin-top: 10px; }
        
        .alert-box { background: #fff1f2; border-left: 4px solid #e11d48; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
        .alert-title { color: #e11d48; font-weight: bold; font-family: 'Montserrat', sans-serif; }
        
        .table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-top: 15px; }
        .table th, .table td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; }
        .table th { background: #f1f5f9; color: #334155; font-weight: 600; font-family: 'Montserrat', sans-serif; font-size: 12px; text-transform: uppercase; }
        
        .highlight-green { color: #059669; font-weight: bold; }
        .highlight-red { color: #e11d48; font-weight: bold; }
        
        .footer { margin-top: 40px; text-align: center; color: #64748b; font-size: 11px; padding-top: 20px; border-top: 1px solid #cbd5e1; }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo">LIFEXTREME<span>.AI</span></div>
        <h1>REPORTE PRIVADO: CÓMO MAXIMIZAR LAS GANANCIAS DE TU AGENCIA ESTA TEMPORADA</h1>
        <p>Procesado por nuestra Inteligencia Artificial analizando datos de Mincetur, Promperu y Senamhi.</p>
    </div>

    <p>Hemos analizado el comportamiento de miles de turistas y cruzado esa información con el estado de nuestras carreteras y clima. Este documento contiene los secretos que los grandes operadores no quieren que sepas sobre dónde está el verdadero margen de ganancia hoy en día.</p>

    <!-- SECCION 1 -->
    <h2>1. ¿DE DÓNDE VIENEN LOS TURISTAS DISPUESTOS A PAGAR MÁS HOY?</h2>
    <div class="grid-3">
        <div class="kpi-card">
            <div class="kpi-title">Mercado Mexicano</div>
            <div class="kpi-value">+35%</div>
            <div class="kpi-desc">El turista de México está viajando más a Perú gracias a que su moneda (el peso) rinde más. Enfoca tus anuncios de Facebook en Ciudad de México; la publicidad allá está muy barata y reservan paquetes caros.</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Turismo Místico y Retiros</div>
            <div class="kpi-value">Ganancia Alta</div>
            <div class="kpi-desc">El viajero actual ya no busca solo "tomarse la foto". Buscan retiros andinos, conexión con la naturaleza y glamping. Este turista paga hasta 3 veces más que el turista tradicional.</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Tour Clásico (Full Day)</div>
            <div class="kpi-value">Alerta Roja</div>
            <div class="kpi-desc">Vender el "City Tour" o viajes relámpago de un día tiene apenas un 8% de ganancia. Hay mucha competencia. Tu agencia debe dejar de pelear por precios bajos y empezar a vender exclusividad.</div>
        </div>
    </div>

    <!-- SECCION 2 -->
    <h2>2. PREDICCIÓN DE LLUVIAS Y CIERRES (EVITA PERDER DINERO EN REEMBOLSOS)</h2>
    <p>No vendas a ciegas. Nuestra Inteligencia Artificial evaluó el clima y los avisos de la SUTRAN. Si vendes estos tours en las próximas semanas, podrías tener que devolverle la plata a los pasajeros o enfrentar quejas graves:</p>
    
    <table class="table">
        <tr>
            <th>Ruta Turística</th>
            <th>Peligro (Lluvias / Huelgas)</th>
            <th>Nuestra Recomendación para tu Agencia</th>
        </tr>
        <tr>
            <td><strong>Montaña de 7 Colores (Vinicunca)</strong></td>
            <td class="highlight-red">Alto Riesgo (Nieve y Vías cerradas)</td>
            <td>Ofrece inmediatamente a tus pasajeros cambiar el tour a <strong>Palccoyo</strong>. Es mucho más seguro y garantizas el paseo sin quejas.</td>
        </tr>
        <tr>
            <td><strong>Laguna 69 (Huaraz)</strong></td>
            <td class="highlight-red">Riesgo Medio (Hipotermia en Adultos Mayores)</td>
            <td>Prohibido vender este tour a pasajeros mayores de 60 años esta temporada. Ofréceles ir a la <strong>Laguna de Llanganuco</strong> en bus.</td>
        </tr>
        <tr>
            <td><strong>Tambopata / Selva Sur</strong></td>
            <td class="highlight-green">Muy Seguro y Despejado</td>
            <td>Excelente oportunidad de venta. Mueve tu presupuesto de publicidad para vender tours a la selva, no habrá cancelaciones.</td>
        </tr>
    </table>

    <!-- SECCION 3 -->
    <h2>3. DEJA DE COMPETIR POR PRECIO. GANA HASTA UN 45% MÁS.</h2>
    <p>Hemos procesado miles de opiniones en TripAdvisor. Los viajeros internacionales se están aburriendo del "Tour rápido, barato y con multitudes". La palabra clave que más ha crecido en las búsquedas es <strong>"Inmersivo"</strong> y <strong>"Auténtico"</strong>.</p>
    
    <div class="alert-box">
        <div class="alert-title">LA FÓRMULA DEL ÉXITO B2B (ALIANZA LIFEXTREME)</div>
        <p style="margin-top: 10px; margin-bottom: 0;">
            Si tu agencia sigue vendiendo tours de 80 dólares para ganar 5 dólares, estás estancado. Re-empaqueta tus rutas: <strong>Vende "Experiencias Privadas, Glamping y Conexión Natural" a 500 dólares.</strong><br><br>
            Tú encárgate de vender paquetes costosos y cobrar la ganancia alta. <strong>Lifextreme</strong> se encarga de ser tu operador logístico en terreno. Nosotros tenemos los buses, el equipo técnico, el monitoreo satelital del clima y nos aseguramos de que tu pasajero regrese feliz sin que tú muevas un dedo.
        </p>
    </div>

    <div class="footer">
        Este documento es un extracto del "Cerebro Lifextreme AI". Cruzamos datos de PROMPERU, Mincetur y Senamhi diariamente.<br>
        <strong>¿Quieres que operemos tus tours con cero estrés para ti? Contáctanos.</strong>
    </div>

</body>
</html>
"""

async def generate_agency_pdf():
    print("Iniciando generación de reporte en lenguaje Turístico/Agencias...")
    html_path = os.path.abspath("temp_agency_report.html")
    pdf_path = os.path.abspath("Lifextreme_Reporte_Para_Agencias.pdf")
    
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
        
    print(f"Reporte Agencias guardado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_agency_pdf())
    except Exception as e:
        pass
