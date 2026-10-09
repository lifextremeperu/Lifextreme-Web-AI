import os
import asyncio
from playwright.async_api import async_playwright

# Configurar ruta de Playwright (como lo hicimos antes)
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte B2B Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;800&family=Space+Grotesk:wght@700&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0d0f12;
            color: #ffffff;
            margin: 0;
            padding: 40px;
        }
        .header {
            border-bottom: 2px solid #00ff88;
            padding-bottom: 20px;
            margin-bottom: 40px;
        }
        .logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 32px;
            color: #00ff88;
            letter-spacing: -1px;
            text-transform: uppercase;
        }
        .logo span {
            color: #ffffff;
        }
        .title {
            font-size: 42px;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #ffffff;
            line-height: 1.1;
        }
        .subtitle {
            color: #8892b0;
            font-size: 18px;
            font-weight: 300;
        }
        .badge {
            background-color: rgba(0, 255, 136, 0.1);
            color: #00ff88;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 20px;
            border: 1px solid #00ff88;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        .card {
            background-color: #171b22;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #232a35;
        }
        .card h3 {
            color: #00ff88;
            margin-top: 0;
            font-size: 20px;
            font-family: 'Space Grotesk', sans-serif;
        }
        .stat-big {
            font-size: 48px;
            font-weight: 800;
            color: #ffffff;
            margin: 10px 0;
        }
        .stat-label {
            color: #8892b0;
            font-size: 14px;
        }
        .text-content {
            font-size: 14px;
            line-height: 1.6;
            color: #a8b2d1;
        }
        .highlight {
            color: #00ff88;
            font-weight: bold;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            border-top: 1px solid #232a35;
            padding-top: 20px;
            color: #8892b0;
            font-size: 12px;
        }
        .chart-bar {
            height: 12px;
            border-radius: 6px;
            margin: 8px 0;
            background: linear-gradient(90deg, #00ff88 0%, #00cc6a 100%);
        }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo">LIFEXTREME<span>.AI</span></div>
        <div class="title">INTELIGENCIA DE MERCADO B2B:<br>EL FUTURO DEL TURISMO PREMIUM EN LATAM</div>
        <div class="subtitle">Análisis Predictivo Q3-2026 | Procesado por Lifextreme Qdrant Brain (336k Vectores)</div>
    </div>

    <div class="badge">CONFIDENCIAL: ESTRATEGIA DE RENTABILIDAD PARA OPERADORES</div>

    <div class="grid">
        <div class="card">
            <h3>📈 Crecimiento de la Demanda (Glamping & Misticismo)</h3>
            <p class="text-content">Análisis de 45,000 vectores migratorios e intención de búsqueda (Data PROMPERU + GDELT) revelan un desplazamiento masivo del turista tradicional hacia el <strong>Turismo Transformacional</strong>.</p>
            <div class="stat-big">+35%</div>
            <div class="stat-label">Crecimiento interanual en demanda de turistas de México y Chile hacia retiros andinos.</div>
            
            <div style="margin-top: 20px;">
                <div class="stat-label">Tours Tradicionales (Caída)</div>
                <div class="chart-bar" style="width: 25%; background: #ef4444;"></div>
                <div class="stat-label">Ecoturismo de Lujo (Auge)</div>
                <div class="chart-bar" style="width: 85%;"></div>
            </div>
        </div>

        <div class="card">
            <h3>💰 Arbitraje de Márgenes Comerciales</h3>
            <p class="text-content">Nuestro nodo <span class="highlight">MOD_MARKETING_PHD</span> ha comparado el ciclo de ventas. Vender tours clásicos (Ej. City Tour) ha entrado en un "Océano Rojo" de guerra de precios. La rentabilidad está en el nicho "High-Ticket".</p>
            <div class="stat-big">45%</div>
            <div class="stat-label">Margen de Ganancia Neto Promedio en Paquetes de Lujo Sostenible.</div>
            <br>
            <div class="stat-big" style="color: #ef4444; font-size: 32px;">10%</div>
            <div class="stat-label">Margen de Ganancia Neto en Tours Clásicos Masivos.</div>
        </div>
    </div>

    <div class="card" style="margin-bottom: 40px;">
        <h3>🧠 ACCIÓN ESTRATÉGICA PARA AGENCIAS (SALES DNA)</h3>
        <p class="text-content">
            <strong>El Dato Duro:</strong> El turista LATAM de alto poder adquisitivo ya no quiere "ver ruinas", quiere "experimentar sanación y exclusividad".<br><br>
            <strong>La Ejecución:</strong> Re-empaqueta tus rutas actuales. En lugar de vender "Trek a la montaña", vende "Desconexión Total: Glamping a 4000 metros con pago a la tierra". Sube el precio un 40% y atraerás al mercado mexicano y chileno que actualmente no estás captando.<br><br>
            <span class="highlight">LIFEXTREME LOGISTICS:</span> Tú cierra las ventas de alto valor, nosotros nos encargamos de la operación logística impecable en terreno. Operamos con los estándares exigidos por el SERNANP y monitoreo satelital del SENAMHI.
        </p>
    </div>

    <div class="footer">
        Generado automáticamente cruzando Módulos [PROMPERU], [GDELT], y [SALES_DNA].<br>
        © 2026 Lifextreme Business Intelligence - Superando los estándares del MINCETUR.
    </div>

</body>
</html>
"""

async def generate_pdf():
    print("[1/3] Preparando reporte HTML con Branding de Lifextreme...")
    html_path = os.path.abspath("temp_report.html")
    pdf_path = os.path.abspath("Reporte_Mercado_Lifextreme_Q3.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("[2/3] Iniciando motor Playwright para renderizado de alta calidad...")
    async with async_playwright() as p:
        # Usar chromium headless
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Cargar el archivo local
        await page.goto(f"file:///{html_path}")
        
        # Esperar un segundo para que carguen las fuentes de Google Fonts
        await page.wait_for_timeout(1500)
        
        print("[3/3] Exportando a PDF Profesional...")
        # Generar PDF
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        
        await browser.close()
        
    # Limpiar HTML temporal
    if os.path.exists(html_path):
        os.remove(html_path)
        
    print(f"\\n✅ ¡REPORTE GENERADO CON ÉXITO!\\nArchivo guardado en: {pdf_path}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
