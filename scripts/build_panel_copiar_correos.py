import json
import os

PROSPECTS_JSON = "reportes_b2b/prospectos_top10_piloto.json"
EMAILS_DIR = "reportes_b2b/emails_personalizados"
OUT_HTML = "reportes_b2b/panel_copiar_10_correos.html"
PUBLIC_BASE = "https://www.lifextreme.com.pe"


def build_subject(p):
    err = (p.get("audit") or {}).get("error") or ""
    if "502" in err or "500" in err:
        return f"{p['saludo_nombre']}, revisé la web de {p['agencia']} hoy (error detectado) + propuesta Cusco"
    return f"{p['saludo_nombre']}, diagnóstico rápido de {p['agencia']} + Claude Cowork In-Office (Cusco)"


def prepare_html(raw_html):
    html = raw_html.replace('href="../../agendar-capacitacion.html', f'href="{PUBLIC_BASE}/agendar-capacitacion.html')
    html = html.replace('href="../agendar-capacitacion.html', f'href="{PUBLIC_BASE}/agendar-capacitacion.html')
    html = html.replace('src="../assets/', f'src="{PUBLIC_BASE}/reportes_b2b/assets/')
    html = html.replace('href="../assets/', f'href="{PUBLIC_BASE}/reportes_b2b/assets/')
    return html


def main():
    with open(PROSPECTS_JSON, "r", encoding="utf-8") as f:
        prospects = json.load(f)

    items = []
    for idx, p in enumerate(prospects, 1):
        slug = p["slug"]
        html_path = os.path.join(EMAILS_DIR, f"{slug}.html")
        with open(html_path, "r", encoding="utf-8") as hf:
            html_body = prepare_html(hf.read())
        items.append({
            "idx": idx,
            "slug": slug,
            "agencia": p["agencia"],
            "saludo": p["saludo_nombre"],
            "email": p["email"],
            "telefono": p.get("telefono", ""),
            "subject": build_subject(p),
            "html": html_body,
        })

    data_json = json.dumps(items, ensure_ascii=False)

    page = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Panel de Envío Manual (10 Prospectos PYME) · Lifextreme</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; font-family: 'Segoe UI', Arial, sans-serif;
      background: #020618; color: #f8fafc;
      display: flex; height: 100vh; overflow: hidden;
    }}
    .sidebar {{
      width: 390px; min-width: 340px; background: #0f1324;
      border-right: 1px solid #2a3148; display: flex; flex-direction: column;
    }}
    .side-head {{
      padding: 18px 20px; border-bottom: 1px solid #2a3148;
      background: linear-gradient(90deg, #ff8e1d 0%, #f43f5e 100%);
      color: #020618;
    }}
    .side-head h1 {{ margin: 0; font-size: 16px; font-weight: 900; text-transform: uppercase; }}
    .side-head p {{ margin: 4px 0 0; font-size: 12px; font-weight: 700; opacity: 0.9; }}
    .list {{ overflow-y: auto; flex: 1; padding: 10px; }}
    .item {{
      padding: 12px 14px; border-radius: 10px; margin-bottom: 8px;
      background: #151b32; border: 1px solid #2a3148; cursor: pointer;
      transition: all 0.15s ease;
    }}
    .item:hover {{ border-color: #ff8e1d; }}
    .item.active {{ border-color: #ff8e1d; background: #1e2542; box-shadow: 0 0 0 1px #ff8e1d; }}
    .item.done {{ opacity: 0.55; border-color: #10b981; }}
    .item-top {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; }}
    .item-name {{ font-weight: 800; font-size: 14px; color: #ffffff; }}
    .item-email {{ font-size: 12px; color: #94a4bb; margin-top: 3px; }}
    .badge {{
      font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 999px;
      background: #2a3148; color: #ff8e1d;
    }}
    .item.done .badge {{ background: #064e3b; color: #34d399; }}
    .main {{ flex: 1; display: flex; flex-direction: column; background: #0b0f1d; }}
    .toolbar {{
      padding: 16px 24px; background: #0f1324; border-bottom: 1px solid #2a3148;
      display: flex; flex-direction: column; gap: 10px;
    }}
    .row {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
    .field-label {{ font-size: 11px; font-weight: 800; color: #94a4bb; width: 64px; text-transform: uppercase; }}
    .field-val {{
      flex: 1; background: #020618; border: 1px solid #2a3148; border-radius: 8px;
      padding: 8px 12px; font-size: 13px; color: #f8fafc; font-family: monospace;
    }}
    .btn {{
      border: none; border-radius: 8px; padding: 9px 14px; font-size: 12.5px;
      font-weight: 800; cursor: pointer; transition: transform 0.1s;
    }}
    .btn:active {{ transform: scale(0.97); }}
    .btn-copy {{ background: #2a3148; color: #ffffff; }}
    .btn-copy:hover {{ background: #3b4463; }}
    .btn-primary {{
      background: linear-gradient(90deg, #ff8e1d, #f43f5e); color: #ffffff;
      padding: 11px 18px; font-size: 13.5px;
    }}
    .btn-done {{ background: #065f46; color: #ffffff; }}
    .preview-wrap {{ flex: 1; padding: 18px 24px; overflow: hidden; display: flex; flex-direction: column; }}
    iframe {{
      flex: 1; width: 100%; border: 1px solid #2a3148; border-radius: 12px; background: #ffffff;
    }}
    .toast {{
      position: fixed; bottom: 24px; right: 24px; background: #ff8e1d; color: #020618;
      padding: 12px 20px; border-radius: 10px; font-weight: 900; font-size: 13px;
      display: none; box-shadow: 0 10px 25px rgba(0,0,0,0.5); z-index: 999;
    }}
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="side-head">
      <h1>10 Prospectos Piloto (Cusco)</h1>
      <p>Haz clic en cada agencia → Copia y pega en Zoho Mail</p>
    </div>
    <div class="list" id="prospectList"></div>
  </div>

  <div class="main">
    <div class="toolbar">
      <div class="row">
        <span class="field-label">Para:</span>
        <input class="field-val" id="toEmail" readonly />
        <button class="btn btn-copy" onclick="copyText('toEmail', 'Correo copiado')">Copiar Correo</button>
      </div>
      <div class="row">
        <span class="field-label">Asunto:</span>
        <input class="field-val" id="subjectText" readonly />
        <button class="btn btn-copy" onclick="copyText('subjectText', 'Asunto copiado')">Copiar Asunto</button>
      </div>
      <div class="row" style="justify-content: space-between; margin-top: 4px;">
        <div class="row">
          <button class="btn btn-primary" onclick="copyRichHtml()">1. Copiar Diseño Completo del Correo (Pegar con Ctrl+V en Zoho)</button>
          <button class="btn btn-copy" onclick="copyRawHtml()">Copiar Código HTML</button>
        </div>
        <button class="btn btn-done" id="btnToggleDone" onclick="toggleDone()">Marcar como Enviado</button>
      </div>
    </div>

    <div class="preview-wrap">
      <iframe id="previewFrame"></iframe>
    </div>
  </div>

  <div class="toast" id="toast"></div>

  <script>
    const ITEMS = {data_json};
    let currentIdx = 0;
    const STORAGE_KEY = 'lx_piloto_enviados_v1';
    let doneMap = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');

    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => t.style.display = 'none', 2200);
    }}

    function renderList() {{
      const list = document.getElementById('prospectList');
      list.innerHTML = '';
      ITEMS.forEach((item, i) => {{
        const isDone = !!doneMap[item.slug];
        const div = document.createElement('div');
        div.className = 'item' + (i === currentIdx ? ' active' : '') + (isDone ? ' done' : '');
        div.onclick = () => selectItem(i);
        div.innerHTML = `
          <div class="item-top">
            <span class="item-name">${{item.idx}}. ${{item.agencia}}</span>
            <span class="badge">${{isDone ? 'ENVIADO' : 'PENDIENTE'}}</span>
          </div>
          <div class="item-email">${{item.email}} · ${{item.saludo}}</div>
        `;
        list.appendChild(div);
      }});
    }}

    function selectItem(i) {{
      currentIdx = i;
      const item = ITEMS[i];
      document.getElementById('toEmail').value = item.email;
      document.getElementById('subjectText').value = item.subject;
      const frame = document.getElementById('previewFrame');
      frame.srcdoc = item.html;
      const isDone = !!doneMap[item.slug];
      document.getElementById('btnToggleDone').textContent = isDone ? 'Desmarcar Enviado' : 'Marcar como Enviado';
      renderList();
    }}

    function copyText(inputId, msg) {{
      const el = document.getElementById(inputId);
      navigator.clipboard.writeText(el.value).then(() => showToast(msg));
    }}

    async function copyRichHtml() {{
      const html = ITEMS[currentIdx].html;
      try {{
        const blobHtml = new Blob([html], {{ type: 'text/html' }});
        const blobText = new Blob([ITEMS[currentIdx].subject], {{ type: 'text/plain' }});
        await navigator.clipboard.write([new ClipboardItem({{ 'text/html': blobHtml, 'text/plain': blobText }})]);
        showToast('Diseño visual copiado! Pega con Ctrl+V dentro de Zoho Mail');
      }} catch (err) {{
        // Fallback seleccionando dentro del iframe
        const doc = document.getElementById('previewFrame').contentDocument;
        const range = doc.createRange();
        range.selectNodeContents(doc.body);
        const sel = doc.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        doc.execCommand('copy');
        sel.removeAllRanges();
        showToast('Diseño visual copiado (fallback)! Pega con Ctrl+V en Zoho');
      }}
    }}

    function copyRawHtml() {{
      navigator.clipboard.writeText(ITEMS[currentIdx].html).then(() => showToast('Código HTML copiado'));
    }}

    function toggleDone() {{
      const slug = ITEMS[currentIdx].slug;
      doneMap[slug] = !doneMap[slug];
      localStorage.setItem(STORAGE_KEY, JSON.stringify(doneMap));
      selectItem(currentIdx);
    }}

    selectItem(0);
  </script>
</body>
</html>
"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Panel creado: {OUT_HTML} ({len(items)} correos)")


if __name__ == "__main__":
    main()
