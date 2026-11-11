"""
build_expediente_pdf.py — Compilador Corporativo de Expedientes a PDF A4
Estándar Big-4 AI Assurance & GovTech Perú (Diseño RAGAS Certificado)
======================================================================
- Paleta Oficial: Deep Navy (#0F3D5E) + Gold Accent (#D4AF37)
- Cabecera Institucional Ejecutiva con franja dorada
- Tablas ejecutivas con bordes limpios (sin bugs de bgcolor)
- Cuadros periciales y de evidencia (.ev-box)
- Numeración y foliado oficial en cada página
"""

import io
import re
import sys
from pathlib import Path
import fitz

sys.stdout.reconfigure(encoding="utf-8")

# Paleta Ejecutiva Oficial (Diseño RAGAS Certificado)
NAVY_PRIMARY = "#0F3D5E"
GOLD_SECONDARY = "#D4AF37"
SLATE_DARK = "#1E293B"
SLATE_LIGHT = "#F8FAFC"
BORDER_COLOR = "#CBD5E1"


def _inline_format(text: str) -> str:
    """Aplica formato inline seguro (negrita, cursiva, código)."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # Restaurar entidades necesarias
    text = text.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    text = text.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    text = text.replace("&lt;code&gt;", "<code>").replace("&lt;/code&gt;", "</code>")
    return text


def md_to_ragas_html(md_content: str) -> str:
    """Convierte el markdown del expediente al formato HTML ejecutivo idéntico al reporte RAGAS."""
    lines = md_content.splitlines()
    body_parts = []
    header_html = []
    header_done = False
    in_table = False
    in_list = False
    in_quote = False

    for line in lines:
        s = line.strip()

        # Cabecera superior inicial (H1, subtítulo institucional y metadatos)
        if not header_done:
            if s.startswith("# "):
                title_text = s[2:].strip()
                header_html.append(f"<h1>{_inline_format(title_text)}</h1>")
                continue
            elif s.startswith("## EXPEDIENTE") or s.startswith("## "):
                sub_text = s[3:].strip()
                header_html.append(f"<p class='header-sub'>{_inline_format(sub_text)}</p>")
                continue
            elif s == "---":
                header_done = True
                continue
            elif s:
                header_html.append(f"<p class='header-meta'>{_inline_format(s)}</p>")
                continue
            else:
                continue

        # Saltos de página explícitos
        if "<div" in s and "page-break" in s:
            if in_table:
                body_parts.append("</tbody></table>")
                in_table = False
            if in_list:
                body_parts.append("</ul>")
                in_list = False
            if in_quote:
                body_parts.append("</div>")
                in_quote = False
            body_parts.append("<div style='break-after: page; page-break-after: always; height: 1pt;'></div>")
            continue

        # Tablas Markdown
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(set(c) <= set(":- ") for c in cells if c):
                continue  # Línea separadora markdown |---|---|
            if not in_table:
                if in_list:
                    body_parts.append("</ul>")
                    in_list = False
                if in_quote:
                    body_parts.append("</div>")
                    in_quote = False
                body_parts.append("<table class='exec-table'><thead><tr>")
                for c in cells:
                    body_parts.append(f"<th>{_inline_format(c)}</th>")
                body_parts.append("</tr></thead><tbody>")
                in_table = True
            else:
                body_parts.append("<tr>")
                for c in cells:
                    body_parts.append(f"<td>{_inline_format(c)}</td>")
                body_parts.append("</tr>")
            continue
        else:
            if in_table:
                body_parts.append("</tbody></table>")
                in_table = False

        # Línea en blanco
        if not s:
            if in_list:
                body_parts.append("</ul>")
                in_list = False
            if in_quote:
                body_parts.append("</div>")
                in_quote = False
            continue

        # Bloques de cita / Resoluciones / Anexos
        if s.startswith(">"):
            if not in_quote:
                if in_list:
                    body_parts.append("</ul>")
                    in_list = False
                body_parts.append("<div class='ev-box'>")
                in_quote = True
            clean_q = s.lstrip(">").strip()
            body_parts.append(f"<p style='margin:2pt 0;'>{_inline_format(clean_q)}</p>")
            continue
        else:
            if in_quote:
                body_parts.append("</div>")
                in_quote = False

        # Encabezados
        if s.startswith("## "):
            if in_list:
                body_parts.append("</ul>")
                in_list = False
            body_parts.append(f"<h2>{_inline_format(s[3:])}</h2>")
        elif s.startswith("### "):
            if in_list:
                body_parts.append("</ul>")
                in_list = False
            body_parts.append(f"<h3>{_inline_format(s[4:])}</h3>")
        elif s.startswith("#### "):
            if in_list:
                body_parts.append("</ul>")
                in_list = False
            body_parts.append(f"<h4>{_inline_format(s[5:])}</h4>")
        elif s.startswith(("* ", "- ")):
            if not in_list:
                body_parts.append("<ul>")
                in_list = True
            body_parts.append(f"<li>{_inline_format(s[2:])}</li>")
        elif re.match(r"^\d+\.\s+", s):
            if not in_list:
                body_parts.append("<ul>")
                in_list = True
            body_parts.append(f"<li>{_inline_format(s)}</li>")
        elif s == "---":
            body_parts.append("<div class='gold-divider'></div>")
        else:
            body_parts.append(f"<p>{_inline_format(s)}</p>")

    if in_table:
        body_parts.append("</tbody></table>")
    if in_list:
        body_parts.append("</ul>")
    if in_quote:
        body_parts.append("</div>")

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<style>
    body {{
        font-family: Helvetica, Arial, sans-serif;
        font-size: 8.5pt;
        line-height: 1.36;
        color: {SLATE_DARK};
    }}
    .header {{
        background-color: {NAVY_PRIMARY};
        color: #ffffff;
        padding: 13pt 15pt;
        margin-bottom: 9pt;
        border-bottom: 3.5pt solid {GOLD_SECONDARY};
    }}
    .header h1 {{
        font-size: 13pt;
        margin: 0 0 4pt 0;
        color: #ffffff;
        font-weight: bold;
        line-height: 1.25;
    }}
    .header-sub {{
        font-size: 9.8pt;
        font-weight: bold;
        color: {GOLD_SECONDARY};
        margin: 2pt 0 6pt 0;
    }}
    .header-meta {{
        font-size: 7.8pt;
        color: #E2E8F0;
        margin: 1.5pt 0;
    }}
    h2 {{
        font-size: 10.5pt;
        color: {NAVY_PRIMARY};
        border-bottom: 1.8pt solid {GOLD_SECONDARY};
        padding-bottom: 2.5pt;
        margin-top: 10pt;
        margin-bottom: 4.5pt;
        font-weight: bold;
    }}
    h3 {{
        font-size: 9pt;
        color: {NAVY_PRIMARY};
        margin-top: 8pt;
        margin-bottom: 3pt;
        font-weight: bold;
    }}
    h4 {{
        font-size: 8.4pt;
        color: #334155;
        margin-top: 6pt;
        margin-bottom: 2pt;
        font-weight: bold;
    }}
    p {{
        margin: 2pt 0 3.5pt 0;
        font-size: 8.3pt;
    }}
    ul {{
        margin: 2pt 0 5pt 12pt;
        padding: 0;
    }}
    li {{
        margin-bottom: 2pt;
        font-size: 8.1pt;
    }}
    table.exec-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 5pt;
        margin-bottom: 8pt;
        font-size: 7.6pt;
    }}
    table.exec-table th {{
        background-color: {NAVY_PRIMARY};
        color: #ffffff;
        padding: 4.5pt 4pt;
        border: 0.5pt solid {BORDER_COLOR};
        text-align: left;
        font-weight: bold;
    }}
    table.exec-table td {{
        padding: 3.8pt 4pt;
        border: 0.5pt solid {BORDER_COLOR};
        vertical-align: top;
    }}
    table.exec-table tbody tr:nth-child(even) td {{
        background-color: {SLATE_LIGHT};
    }}
    .ev-box {{
        background-color: {SLATE_LIGHT};
        border-left: 3pt solid {NAVY_PRIMARY};
        padding: 4pt 7pt;
        margin: 4pt 0 6pt 0;
        font-size: 8pt;
    }}
    .gold-divider {{
        height: 1.5pt;
        background-color: {GOLD_SECONDARY};
        margin: 8pt 0;
    }}
    code {{
        background: #F1F5F9;
        color: {NAVY_PRIMARY};
        padding: 1pt 3pt;
        border-radius: 2pt;
        font-size: 7.8pt;
        font-family: monospace;
    }}
</style>
</head>
<body>
    <div class="header">
        {"".join(header_html)}
    </div>
    {"".join(body_parts)}
</body>
</html>"""


def convert_md_to_pdf(input_md_path: str, output_pdf_path: str, brand_colors: dict | None = None) -> str:
    """
    Convierte el Expediente Técnico Markdown en un PDF A4 impecable
    con diseño corporativo Big-4 (RAGAS Style) sin glitches de color.
    """
    md_path = Path(input_md_path)
    md_content = md_path.read_text(encoding="utf-8")
    full_html = md_to_ragas_html(md_content)

    out_path = Path(output_pdf_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar copia HTML de respaldo (.print.html)
    html_backup = out_path.with_suffix(".print.html")
    html_backup.write_text(full_html, encoding="utf-8")

    # Renderizado en memoria A4 con PyMuPDF fitz.Story
    MEDIABOX = fitz.paper_rect("a4")
    WHERE = MEDIABOX + (36, 40, -36, -40)  # Márgenes ejecutivos A4

    story = fitz.Story(html=full_html)
    buf = io.BytesIO()
    writer = fitz.DocumentWriter(buf)

    more = 1
    while more:
        dev = writer.begin_page(MEDIABOX)
        more, _ = story.place(WHERE)
        story.draw(dev)
        writer.end_page()
    writer.close()

    # Agregar encabezado y pie de página institucional en cada página
    buf.seek(0)
    doc = fitz.open("pdf", buf.read())
    total_pages = len(doc)
    for idx, page in enumerate(doc, 1):
        # Línea superior azul institucional
        page.draw_line(
            fitz.Point(36, 26),
            fitz.Point(MEDIABOX.width - 36, 26),
            color=(0.059, 0.239, 0.369),  # #0F3D5E
            width=1.5,
        )
        page.insert_text(
            fitz.Point(36, 21),
            "EXPEDIENTE TÉCNICO DE GOBERNANZA IA & CUMPLIMIENTO LEGAL | ISO/IEC 42001 & LEY 31814",
            fontsize=7.2,
            color=(0.35, 0.40, 0.48),
        )
        # Línea inferior dorada
        page.draw_line(
            fitz.Point(36, MEDIABOX.height - 28),
            fitz.Point(MEDIABOX.width - 36, MEDIABOX.height - 28),
            color=(0.831, 0.686, 0.216),  # #D4AF37
            width=1.0,
        )
        page.insert_text(
            fitz.Point(36, MEDIABOX.height - 16),
            "Consorcio Auditor: Ing. Arquitectura IA | Mg. Psicología | Mg. Educación | Mg. Antropología — Cusco, Perú",
            fontsize=7.2,
            color=(0.35, 0.40, 0.48),
        )
        page.insert_text(
            fitz.Point(MEDIABOX.width - 95, MEDIABOX.height - 16),
            f"Página {idx} de {total_pages}",
            fontsize=7.5,
            color=(0.2, 0.2, 0.2),
        )

    doc.save(str(out_path))
    doc.close()

    print(f"PDF generado exitosamente ({total_pages} páginas A4): {out_path}")
    return str(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python scripts/build_expediente_pdf.py <entrada.md> <salida.pdf>")
        sys.exit(1)
    convert_md_to_pdf(sys.argv[1], sys.argv[2])
