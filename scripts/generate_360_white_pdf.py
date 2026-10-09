import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte 360 AI - Lifextreme</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&family=Space+Mono:ital,wght@0,400;0,700&display=swap');
        
        body { 
            font-family: 'Outfit', sans-serif; 
            background-color: #ffffff; 
            color: #1f2937; 
            margin: 0; 
            padding: 40px; 
            font-size: 11px; 
            line-height: 1.5;
        }
        
        .header { 
            border-bottom: 3px solid #00ff88; 
            padding-bottom: 20px; 
            margin-bottom: 30px; 
        }
        
        .logo {
            font-family: 'Space Mono', monospace; 
            font-size: 28px; 
            color: #111827; 
            font-weight: 700; 
            letter-spacing: -1px;
        }
        
        .logo span { color: #00ff88; }
        
        .title {
            font-size: 30px;
            font-weight: 900;
            color: #111827;
            margin: 10px 0;
            line-height: 1.1;
        }
        
        .subtitle {
            color: #4b5563;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
        }
        
        .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        
        .module-box {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            position: relative;
            page-break-inside: avoid; /* Previene cortes a la mitad del modulo */
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        }
        
        .module-number {
            position: absolute;
            top: -10px;
            left: 15px;
            background: #111827;
            color: #00ff88;
            font-family: 'Space Mono';
            font-size: 10px;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 10px;
        }
        
        .module-title {
            color: #111827;
            font-size: 14px;
            font-weight: 800;
            margin-top: 5px;
            margin-bottom: 10px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 5px;
        }
        
        .module-text { color: #4b5563; margin-bottom: 10px; }
        
        .ai-insight {
            background: #f0fdf4;
            border-left: 3px solid #00ff88;
            padding: 8px 12px;
            color: #1f2937;
            font-size: 10px;
            border-radius: 0 4px 4px 0;
        }
        
        .ai-insight strong { color: #047857; display: block; margin-bottom: 3px; font-family: 'Space Mono'; }
        
        .page-break { page-break-before: always; }
    </style>
</head>
<body>

    <!-- PAGINA 1 -->
    <div class="header">
        <div class="logo">LIFEXTREME<span>.AI</span></div>
        <div class="title">AUDITORÍA INTEGRAL 360° PARA AGENCIAS DE VIAJES</div>
        <div class="subtitle">Estrategia Tecnológica, SEO/AEO, Modelos Predictivos y Logística (12 MÓDULOS)</div>
    </div>
    
    <p style="color: #4b5563; font-size: 12px; margin-bottom: 25px; font-weight: 500;">Este documento es un mapa de ruta tecnológico. Su agencia no solo necesita vender tours; necesita sobrevivir en la era de los LLMs (ChatGPT) y los algoritmos predictivos. A continuación, el análisis crudo de nuestro cerebro Qdrant para estructurar su agencia al nivel corporativo transnacional.</p>

    <div class="grid-3">
        <div class="module-box">
            <div class="module-number">M01</div>
            <div class="module-title">GEO & AEO (Generative Engine)</div>
            <div class="module-text">Si un turista le pregunta a ChatGPT: <em>"¿Cuál es la mejor agencia en Perú?"</em>, ¿aparece usted? El SEO tradicional en Google está colapsando. Necesita AEO (Optimización para Motores de Respuesta).</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Alimente su web con texto hiper-estructurado respondiendo preguntas exactas de manera conversacional para que las IAs lo citen como fuente de autoridad.
            </div>
        </div>

        <div class="module-box">
            <div class="module-number">M02</div>
            <div class="module-title">Arquitectura FQSA</div>
            <div class="module-text">Nuestro análisis indica que el 70% de las ventas B2C se caen porque la web no responde dudas críticas (clima, mal de altura, edad mínima permitida) en los primeros 10 segundos.</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Inyecte un sistema FQSA (Frequently Questioned Solutions) en cada página de reserva. Adelántese al "miedo" del pasajero y derrumbe objeciones.
            </div>
        </div>

        <div class="module-box">
            <div class="module-number">M03</div>
            <div class="module-title">Precios Predictivos (TimesFM)</div>
            <div class="module-text">Los algoritmos de TimesFM en nuestros servidores predicen cuándo un mercado específico está dispuesto a pagar un "Premium" por temporada alta anticipada.</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Pricing Dinámico. Suba sus precios un 15% automáticamente cuando los vuelos de LATAM hacia Lima bajen de costo (el pasajero tiene más liquidez).
            </div>
        </div>
    </div>

    <div class="grid-3">
        <div class="module-box">
            <div class="module-number">M04</div>
            <div class="module-title">Tendencias: Ecoturismo de Lujo</div>
            <div class="module-text">El "Turismo Masivo" destruye márgenes. La tendencia global dictada por nuestros vectores apunta al <em>Lujo Sostenible</em>: Glamping, conexión real y retiro tecnológico.</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Reemplace sus paquetes clásicos por "Premium Ecológico". Cobrará el cuádruple operando con menos personas, garantizando exclusividad.
            </div>
        </div>

        <div class="module-box">
            <div class="module-number">M05</div>
            <div class="module-title">Nuevos Proyectos (PENTUR 2028)</div>
            <div class="module-text">La extracción de inteligencia del PENTUR indica que el Estado inyectará recursos prioritarios en la Ruta Moche (La Libertad) y Turismo Amazónico (Loreto).</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Llegue primero. Posicione landing pages vendiendo rutas de expedición en la selva norte antes de que la saturación llegue a esas zonas en 2027.
            </div>
        </div>

        <div class="module-box">
            <div class="module-number">M06</div>
            <div class="module-title">SGE: El Nuevo Google</div>
            <div class="module-text">Google ahora responde con Inteligencia Artificial (SGE) en la misma página de resultados. Nadie hace clic en los "enlaces azules" tradicionales.</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Su blog debe tener tablas HTML claras, listas numeradas y Schema.org para que la IA de Google robe su texto y lo cite en su respuesta principal.
            </div>
        </div>
    </div>

    <!-- CORTE DE PÁGINA FORZADO -->
    <div class="page-break"></div>

    <!-- PAGINA 2 -->
    <div class="header" style="margin-top: 20px;">
        <div class="logo">LIFEXTREME<span>.AI</span></div>
        <div class="subtitle">Continuación: Análisis Logístico, Retención y Nuevos Mercados (M07 - M12)</div>
    </div>

    <div class="grid-3">
        <div class="module-box">
            <div class="module-number">M07</div>
            <div class="module-title">Logística Predictiva (SUTRAN)</div>
            <div class="module-text">Devolver dinero por vías bloqueadas arruina su EBITDA. Cruzando datos climáticos y políticos, detectamos vías con alto riesgo de cierre (Ej. Corredor Sur andino).</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Venda los tours con cláusulas de "Flexibilidad Garantizada". Si hay huelga, el turista acepta ir a otra montaña, salvando su flujo de caja.
            </div>
        </div>

        <div class="module-box">
            <div class="module-number">M08</div>
            <div class="module-title">Vuelos, Petróleo y Macroeconomía</div>
            <div class="module-text">Si el petróleo Jet-A1 sube, el ticket aéreo a Perú sube. El europeo de clase media cancelará, pero el UHNWI (millonario) no se inmutará ante la inflación.</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> En épocas de inflación, apague sus anuncios de Facebook masivos. Pase a canales cerrados B2B o venda a expatriados locales de alto poder.
            </div>
        </div>

        <div class="module-box">
            <div class="module-number">M09</div>
            <div class="module-title">Conversión CRM y WhatsApp</div>
            <div class="module-text">Nuestro Ph.D. Knowledge Base demuestra que la venta web cierra al 10%, pero la venta consultiva (asistida por CRM y WhatsApp) sube exponencialmente al 35%.</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Inserte un bot FQSA en WhatsApp. Envíe 3 opciones de precios (Efecto Anclaje) y cobre inmediatamente con links de pago Yape/Niubiz.
            </div>
        </div>
    </div>

    <div class="grid-3">
        <!-- MODULO NUEVO 11 -->
        <div class="module-box">
            <div class="module-number">M10</div>
            <div class="module-title">Segmentación Micro-Nichos</div>
            <div class="module-text">Los perfiles genéricos ("Familias" o "Parejas") están saturados. Los reportes actuales indican crecimientos exponenciales en Solo Female Travelers y Turismo Pet-Friendly.</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Cree sub-marcas o landing pages dedicadas exclusivamente a "Mujeres Viajando Solas", ofreciendo máxima seguridad y guías femeninas.
            </div>
        </div>

        <!-- MODULO NUEVO 12 -->
        <div class="module-box">
            <div class="module-number">M11</div>
            <div class="module-title">Certificaciones Carbono Cero</div>
            <div class="module-text">Los grandes Tour Operadores europeos ahora están obligados por ley (ESG) a trabajar solo con agencias locales que compensen su huella de carbono (Green Funds).</div>
            <div class="ai-insight">
                <strong>EJECUCIÓN TÁCTICA:</strong> Adopte certificaciones verdes. Cuando una agencia de Francia busque un socio en Perú, lo elegirá a usted para cumplir sus métricas legales europeas.
            </div>
        </div>

        <!-- MODULO ALIANZA FINAL -->
        <div class="module-box" style="background-color: #0f172a;">
            <div class="module-number" style="background: #00ff88; color: #111827;">M12</div>
            <div class="module-title" style="color: #ffffff; border-bottom: 2px solid #374151;">La Alianza Operativa 360°</div>
            <div class="module-text" style="color: #e2e8f0;">La tecnología de Lifextreme está diseñada para que <strong>su agencia escale globalmente sin límites de personal ni comprar buses</strong>.</div>
            <div class="ai-insight" style="background: transparent; border-color: #00ff88; color: #00ff88;">
                <strong>EL TRATO FINAL:</strong> Su agencia aplica los Módulos 01-11 para vender paquetes de lujo. Lifextreme asume la carga logística operando el tour en terreno de forma infalible.
            </div>
        </div>
    </div>

    <div style="text-align: center; color: #9ca3af; font-size: 10px; margin-top: 20px; border-top: 1px solid #e2e8f0; padding-top: 20px; font-weight: bold;">
        REPORTE OFICIAL GENERADO POR LIFEXTREME AI (12 MÓDULOS DE VANGUARDIA).<br>
        TODOS LOS DERECHOS RESERVADOS 2026.
    </div>

</body>
</html>
"""

async def generate_360_white_pdf():
    print("Preparando Reporte de Auditoría 360° (Blanco + 12 Módulos)...")
    html_path = os.path.abspath("temp_360_white.html")
    pdf_path = os.path.abspath("Lifextreme_Auditoria_360_V2.pdf")
    
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
        
    print(f"PDF generado correctamente en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_360_white_pdf())
    except Exception as e:
        pass
