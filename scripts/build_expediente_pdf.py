"""
build_expediente_pdf.py — Fase 3 de DIRECTIVA DIR-AG-QDRANT-2026-001
Compila el Expediente Técnico en Markdown a PDF listo para imprenta (A4, paleta institucional, tablas y numeración)
usando PyMuPDF (fitz.Story) de alta velocidad o WeasyPrint.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def _md_to_clean_html(md_content: str, brand_colors: dict) -> str:
    primary = brand_colors.get("primary", "#0F3D5E")
    secondary = brand_colors.get("secondary", "#D4AF37")

    # Intentar usar librería markdown si está instalada, si no, conversor nativo con soporte de tablas
    try:
        import markdown
        html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code"])
    except ImportError:
        lines = md_content.splitlines()
        out = []
        in_table = False
        in_list = False
        for line in lines:
            s = line.strip()
            if not s:
                if in_table:
                    out.append("</table>")
                    in_table = False
                if in_list:
                    out.append("</ul>")
                    in_list = False
                continue
            if "<div" in s and "page-break" in s:
                if in_table:
                    out.append("</table>")
                    in_table = False
                if in_list:
                    out.append("</ul>")
                    in_list = False
                out.append('<hr style="margin: 18pt 0; border: 1px solid #ccc;"/>')
                continue
            if s.startswith("|") and s.endswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if all(set(c) <= set(":-") for c in cells if c):
                    continue
                if not in_table:
                    out.append('<table border="1" cellspacing="0" cellpadding="6" width="100%">')
                    in_table = True
                    row_html = "".join(
                        f'<th bgcolor="{primary}" style="color:white;font-weight:bold;text-align:left;">{_inline_md(c)}</th>'
                        for c in cells
                    )
                    out.append(f"<tr>{row_html}</tr>")
                else:
                    row_html = "".join(f"<td>{_inline_md(c)}</td>" for c in cells)
                    out.append(f"<tr>{row_html}</tr>")
                continue
            if in_table:
                out.append("</table>")
                in_table = False
            if s.startswith("# "):
                out.append(f'<h1>{_inline_md(s[2:])}</h1>')
            elif s.startswith("## "):
                out.append(f'<h2>{_inline_md(s[3:])}</h2>')
            elif s.startswith("### "):
                out.append(f'<h3>{_inline_md(s[4:])}</h3>')
            elif s.startswith("#### "):
                out.append(f'<h4>{_inline_md(s[5:])}</h4>')
            elif s.startswith(("* ", "- ")):
                if not in_list:
                    out.append("<ul>")
                    in_list = True
                out.append(f"<li>{_inline_md(s[2:])}</li>")
            elif re.match(r"^\d+\.\s+", s):
                if not in_list:
                    out.append("<ul>")
                    in_list = True
                out.append(f"<li>{_inline_md(s)}</li>")
            elif s == "---":
                out.append("<hr/>")
            else:
                out.append(f"<p>{_inline_md(s)}</p>")
        if in_table:
            out.append("</table>")
        if in_list:
            out.append("</ul>")
        html_body = "\n".join(out)

    css = f"""
    body {{
        font-family: sans-serif;
        color: #1e293b;
        line-height: 1.45;
        font-size: 9.5pt;
    }}
    h1 {{
        color: {primary};
        font-size: 16pt;
        margin-top: 8pt;
        margin-bottom: 4pt;
    }}
    h2 {{
        color: {primary};
        font-size: 12.5pt;
        margin-top: 12pt;
        margin-bottom: 4pt;
    }}
    h3 {{
        color: #334155;
        font-size: 10.5pt;
        margin-top: 8pt;
        margin-bottom: 3pt;
    }}
    p, li {{
        font-size: 9.2pt;
        margin-top: 2pt;
        margin-bottom: 3pt;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 6pt;
        margin-bottom: 8pt;
        font-size: 8.2pt;
    }}
    th {{
        background-color: {primary};
        color: #ffffff;
        padding: 5pt;
        font-weight: bold;
    }}
    td {{
        padding: 5pt;
        border: 1px solid #cbd5e1;
    }}
    """
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{html_body}</body></html>"


def _inline_md(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def convert_md_to_pdf(input_md_path: str, output_pdf_path: str, brand_colors: dict | None = None) -> str:
    """Convierte el Expediente en Markdown a un archivo PDF real listo para descargar e imprimir."""
    brand_colors = brand_colors or {"primary": "#0F3D5E", "secondary": "#D4AF37"}
    md_path = Path(input_md_path)
    md_content = md_path.read_text(encoding="utf-8")
    full_html = _md_to_clean_html(md_content, brand_colors)

    out_path = Path(output_pdf_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar también copia HTML de respaldo
    html_backup = out_path.with_suffix(".print.html")
    html_backup.write_text(full_html, encoding="utf-8")

    # Renderizado nativo en memoria a PDF A4 mediante PyMuPDF (fitz.Story)
    import io
    import fitz

    MEDIABOX = fitz.paper_rect("a4")
    WHERE = MEDIABOX + (36, 42, -36, -42)  # Márgenes ejecutivos A4

    story = fitz.Story(html=full_html)
    buf = io.BytesIO()
    writer = fitz.DocumentWriter(buf)

    page_num = 1
    more = 1
    while more:
        device = writer.begin_page(MEDIABOX)
        more, _ = story.place(WHERE)
        story.draw(device)
        writer.end_page()
        page_num += 1
    writer.close()

    # Agregar encabezado/pie de página institucional con numeración a cada página
    buf.seek(0)
    doc = fitz.open("pdf", buf.read())
    total_pages = len(doc)
    for idx, page in enumerate(doc, 1):
        # Línea superior dorada/azul
        page.draw_line(fitz.Point(36, 28), fitz.Point(MEDIABOX.width - 36, 28), color=(0.06, 0.24, 0.37), width=1.5)
        page.insert_text(
            fitz.Point(36, 23),
            "DIRECTIVA DIR-AG-QDRANT-2026-001 | EXPEDIENTE TÉCNICO DE GOBERNANZA IA & CUMPLIMIENTO LEGAL",
            fontsize=7.5,
            color=(0.35, 0.40, 0.48),
        )
        # Pie de página con numeración
        page.draw_line(
            fitz.Point(36, MEDIABOX.height - 30),
            fitz.Point(MEDIABOX.width - 36, MEDIABOX.height - 30),
            color=(0.83, 0.69, 0.22),
            width=1.0,
        )
        page.insert_text(
            fitz.Point(36, MEDIABOX.height - 18),
            "Comité Pericial: Ing. Arquitectura IA | Mg. Psicología | Mg. Educación | Mg. Antropología — Cusco, Perú",
            fontsize=7.5,
            color=(0.35, 0.40, 0.48),
        )
        page.insert_text(
            fitz.Point(MEDIABOX.width - 95, MEDIABOX.height - 18),
            f"Página {idx} de {total_pages}",
            fontsize=8,
            color=(0.2, 0.2, 0.2),
        )

    doc.save(str(out_path))
    doc.close()

    print(f"PDF generado exitosamente ({total_pages} páginas A4): {out_path}")
    return str(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python scripts/build_expediente_pdf.py <entrada.md> <salida.pdf> [color_primario] [color_secundario]")
        sys.exit(1)
    colors = {
        "primary": sys.argv[3] if len(sys.argv) > 3 else "#0F3D5E",
        "secondary": sys.argv[4] if len(sys.argv) > 4 else "#D4AF37",
    }
    convert_md_to_pdf(sys.argv[1], sys.argv[2], colors)
