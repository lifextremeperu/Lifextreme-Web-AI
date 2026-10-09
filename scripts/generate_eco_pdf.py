import os
import asyncio
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Cronograma de Ejecución y Financiamiento Sostenible</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,600&family=Source+Sans+Pro:wght@300;400;600&display=swap');
        
        body { 
            font-family: 'Source Sans Pro', sans-serif; 
            background-color: #f4f7f4; 
            color: #2b3a2f; 
            margin: 0; 
            padding: 40px; 
            font-size: 13px; 
        }
        
        .header { 
            text-align: center; 
            padding-bottom: 20px; 
            border-bottom: 2px solid #3d6a4f; 
            margin-bottom: 30px; 
        }
        
        .header h1 { 
            font-family: 'Playfair Display', serif; 
            font-size: 32px; 
            color: #1e3b2b; 
            margin: 0 0 10px 0; 
        }
        
        .header p { 
            color: #5c7a68; 
            font-size: 14px; 
            margin: 0; 
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        h2 { 
            font-family: 'Playfair Display', serif; 
            font-size: 22px; 
            color: #3d6a4f; 
            margin-top: 40px; 
            margin-bottom: 20px; 
            display: flex;
            align-items: center;
        }
        
        h2::before {
            content: "";
            display: inline-block;
            width: 12px;
            height: 12px;
            background-color: #6a994e;
            border-radius: 50%;
            margin-right: 12px;
        }
        
        table { 
            width: 100%; 
            border-collapse: collapse; 
            background-color: #ffffff; 
            border-radius: 8px; 
            overflow: hidden; 
            box-shadow: 0 4px 15px rgba(43, 58, 47, 0.05); 
        }
        
        th, td { 
            padding: 14px 18px; 
            text-align: left; 
            border-bottom: 1px solid #e9ece9; 
        }
        
        th { 
            background-color: #3d6a4f; 
            color: #ffffff; 
            font-weight: 600; 
            text-transform: uppercase; 
            font-size: 11px; 
            letter-spacing: 0.5px;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        .date-badge {
            background-color: #e5efe7;
            color: #3d6a4f;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 11px;
            white-space: nowrap;
        }
        
        .amount-badge {
            color: #2b7a0b;
            font-weight: 600;
            font-size: 13px;
        }
        
        .footer {
            margin-top: 50px;
            text-align: center;
            color: #8a9c8f;
            font-size: 11px;
            border-top: 1px solid #dce4dd;
            padding-top: 20px;
        }
    </style>
</head>
<body>

    <div class="header">
        <h1>Cronograma de Habilitación y Financiamiento</h1>
        <p>Proyectos de Conservación y Sostenibilidad (2026 - 2027)</p>
    </div>

    <!-- FASE 1 -->
    <h2>Fase 1: Habilitadores Legales y Administrativos (Oct - Dic 2026)</h2>
    <table>
        <tr>
            <th>Fecha Límite</th>
            <th>Entidad Rectora</th>
            <th>Instrumento o Trámite</th>
            <th>Acción Estratégica Requerida</th>
        </tr>
        <tr>
            <td><span class="date-badge">Octubre 2026</span></td>
            <td><strong>SUNAT</strong></td>
            <td>Exoneración de Impuesto a la Renta</td>
            <td>Presentar el Formulario 2119 y estatutos de inmediato.</td>
        </tr>
        <tr>
            <td><span class="date-badge">Octubre 2026</span></td>
            <td><strong>Red Filantrópica</strong></td>
            <td>Fiscal Sponsorship Agreement</td>
            <td>Firmar convenio Modelo C con un patrocinador internacional.</td>
        </tr>
        <tr>
            <td><span class="date-badge">Noviembre 2026</span></td>
            <td><strong>MINCETUR</strong></td>
            <td>Inscripción en el RNOBC</td>
            <td>Asesorar a la comunidad para su inscripción en el registro de Turismo.</td>
        </tr>
        <tr>
            <td><span class="date-badge">Diciembre 2026</span></td>
            <td><strong>SERNANP</strong></td>
            <td>Inicio de Expediente ACP</td>
            <td>Iniciar mapeo y reconocimiento de Área de Conservación Privada.</td>
        </tr>
    </table>

    <!-- FASE 2 -->
    <h2>Fase 2: Concursos Nacionales e Internacionales (2026 - 2027)</h2>
    <table>
        <tr>
            <th>Fecha Cierre</th>
            <th>Entidad Financiadora</th>
            <th>Nombre del Fondo</th>
            <th>Monto Máximo</th>
            <th>Enfoque de Postulación</th>
        </tr>
        <tr>
            <td><span class="date-badge">Continua</span></td>
            <td><strong>The Pollination Project</strong></td>
            <td>Daily Seed Grant</td>
            <td class="amount-badge">$500 USD</td>
            <td>Ideal para inicio sin historial; respuesta rápida.</td>
        </tr>
        <tr>
            <td><span class="date-badge">25 Oct 2026</span></td>
            <td><strong>Cultural Survival</strong></td>
            <td>Indigenous Youth Fellowship</td>
            <td class="amount-badge">$5,000 USD</td>
            <td>Proyectos liderados por jóvenes locales de 18 a 28 años.</td>
        </tr>
        <tr>
            <td><span class="date-badge">08 Ene 2027</span></td>
            <td><strong>New England Biolabs Foundation</strong></td>
            <td>Round 1 Grants (LOI)</td>
            <td class="amount-badge">$15,000 USD</td>
            <td>Resiliencia andina y conservación cultural biocultural.</td>
        </tr>
        <tr>
            <td><span class="date-badge">10 Feb 2027</span></td>
            <td><strong>Cultural Survival</strong></td>
            <td>Keepers of the Earth Fund</td>
            <td class="amount-badge">$10,000 USD</td>
            <td>Requiere cuenta bancaria o un Patrocinador Fiscal internacional.</td>
        </tr>
        <tr>
            <td><span class="date-badge">Feb - Mar 2027</span></td>
            <td><strong>ProInnóvate (PRODUCE)</strong></td>
            <td>Capital Semilla</td>
            <td class="amount-badge">S/ 67,000</td>
            <td>Presentar solución ClimateTech o AgriTech innovadora.</td>
        </tr>
        <tr>
            <td><span class="date-badge">Abr - May 2027</span></td>
            <td><strong>MINCETUR</strong></td>
            <td>Turismo Emprende</td>
            <td class="amount-badge">S/ 120,000</td>
            <td>Postulación apoyada en la comunidad inscrita en RNOBC.</td>
        </tr>
        <tr>
            <td><span class="date-badge">31 May 2027</span></td>
            <td><strong>Patagonia</strong></td>
            <td>Environmental Grants</td>
            <td class="amount-badge">$15,000 USD</td>
            <td>Acción directa sobre problemas estructurales (requiere patrocinador).</td>
        </tr>
        <tr>
            <td><span class="date-badge">01 Oct 2027</span></td>
            <td><strong>Rainforest Trust</strong></td>
            <td>Protected Areas Grant</td>
            <td class="amount-badge">$20,000 USD</td>
            <td>Expansión de áreas protegidas y conservación de hábitats vulnerables.</td>
        </tr>
    </table>

    <div class="footer">
        Documento Estratégico de Planificación de Fondos y Sostenibilidad<br>
        Confidencial - Uso Interno Exclusivo
    </div>

</body>
</html>
"""

async def generate_eco_pdf():
    print("Iniciando generación de reporte Eco/Naturaleza...")
    html_path = os.path.abspath("temp_eco_report.html")
    pdf_path = os.path.abspath("Cronograma_Fondos_Sostenibles.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(f"file:///{html_path}")
        await page.wait_for_timeout(1000) # Cargar fuentes orgánicas (Playfair Display)
        
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        
        await browser.close()
        
    if os.path.exists(html_path):
        os.remove(html_path)
        
    print(f"Reporte Ecológico guardado en: {pdf_path}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_eco_pdf())
    except Exception as e:
        pass
