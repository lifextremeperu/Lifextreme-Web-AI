"""
MIGRACIÓN SEGURA DE DOMINIO: lifextreme.store -> lifextreme.com.pe (FASE 3)
===========================================================================
Reglas de seguridad:
1. Actualiza todas las URLs web (`https://www.lifextreme.store`, `https://lifextreme.store`, `www.lifextreme.store`)
   a `https://www.lifextreme.com.pe` y `www.lifextreme.com.pe`.
2. Mantiene compatibilidad dual en CORS (`api/send-email.js`), scanner (`api/quantum-scan.js`),
   chatbot (`js/max-chatbot.js`) y logins demo (`partners/js/auth.js`) para que funcionen
   TANTO `.com.pe` como `.store` sin romper nada.
3. No altera los buzones `@lifextreme.store` en variables SMTP hasta que el usuario
   complete la verificación de Zoho Mail para `@lifextreme.com.pe`.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TARGET_FILES = [
    "index.html",
    "en/index.html",
    "pt/index.html",
    "sitemap.xml",
    "robots.txt",
    "llms.txt",
    "en/llms.txt",
    "seo-metatags.html",
    "ai-plugin.json",
    "hub.html",
    "vr-experience.html",
    "open-source.html",
    "seguridad-govtech.html",
    "quantum-ux-simulator.html",
    "privacidad.html",
    "politica-proveedores.html",
    "reclamaciones.html",
    "terminos.html",
    "community.html",
    "studio.html",
    "js/app.js",
    "js/config.js",
    "js/blog-engine.js",
    "js/gamification.js",
    "js/infrastructure.js",
    "js/seo-manager.js",
    "js/max-chatbot.js",
    "api/send-email.js",
    "api/quantum-scan.js",
    "partners/js/auth.js",
    "backend/src/rag_service.py",
    "backend/src/mcp_server.py",
    "backend/discord_agent/rag_service.py",
    "scripts/blog_agent.py",
    "scripts/generar_llms_txt.py",
    "submit_indexnow.ps1",
    "README.md",
]


def main() -> None:
    updated_count = 0

    # 1. Parches duales específicos (CORS, Quantum Scan, Max Chatbot, Partner Auth)
    send_email_path = PROJECT_ROOT / "api/send-email.js"
    if send_email_path.exists():
        txt = send_email_path.read_text(encoding="utf-8")
        txt = txt.replace(
            "origin.includes('lifextreme.store') || origin.includes('vercel.app')",
            "origin.includes('lifextreme.com.pe') || origin.includes('lifextreme.store') || origin.includes('vercel.app')",
        )
        txt = txt.replace("<strong>lifextreme.store</strong>", "<strong>lifextreme.com.pe</strong>")
        send_email_path.write_text(txt, encoding="utf-8")

    qscan_path = PROJECT_ROOT / "api/quantum-scan.js"
    if qscan_path.exists():
        txt = qscan_path.read_text(encoding="utf-8")
        txt = txt.replace(
            "normalizedUrl.includes('lifextreme.store')",
            "(normalizedUrl.includes('lifextreme.com.pe') || normalizedUrl.includes('lifextreme.store'))",
        )
        qscan_path.write_text(txt, encoding="utf-8")

    max_chat_path = PROJECT_ROOT / "js/max-chatbot.js"
    if max_chat_path.exists():
        txt = max_chat_path.read_text(encoding="utf-8")
        txt = txt.replace(
            "url.includes('max.lifextreme.store')",
            "url.includes('max.lifextreme.com.pe') || url.includes('max.lifextreme.store')",
        )
        max_chat_path.write_text(txt, encoding="utf-8")

    auth_path = PROJECT_ROOT / "partners/js/auth.js"
    if auth_path.exists():
        txt = auth_path.read_text(encoding="utf-8")
        # Limpiar reemplazo accidental en objeto sessionData si existe
        for line_to_remove in [
            "                    'partner@lifextreme.com.pe',\n                    'demo@lifextreme.com.pe',\n                    'inversionista@lifextreme.com.pe',\n                    'admin@lifextreme.store',\n                    id: 'partner-demo-fallback',",
            "                    'partner@lifextreme.com.pe',\r\n                    'demo@lifextreme.com.pe',\r\n                    'inversionista@lifextreme.com.pe',\r\n                    'admin@lifextreme.store',\r\n                    id: 'partner-demo-fallback',",
        ]:
            if line_to_remove in txt:
                txt = txt.replace(line_to_remove, "                    id: 'partner-demo-fallback',")
        if "'admin@lifextreme.com.pe'" not in txt:
            txt = txt.replace(
                "const bypassEmails = [\n                    'admin@lifextreme.store',",
                "const bypassEmails = [\n                    'admin@lifextreme.com.pe',\n                    'partner@lifextreme.com.pe',\n                    'demo@lifextreme.com.pe',\n                    'inversionista@lifextreme.com.pe',\n                    'admin@lifextreme.store',",
            )
        auth_path.write_text(txt, encoding="utf-8")

    # 2. Reemplazo seguro de URLs web (sin tocar @lifextreme.store ni max.lifextreme.store en endpoints activos)
    for rel in TARGET_FILES:
        f = PROJECT_ROOT / rel
        if not f.exists():
            continue
        original = f.read_text(encoding="utf-8")
        modified = original

        # Reemplazar URLs web con www y sin www (pero NO precedidas por @ ni max.)
        modified = modified.replace("https://www.lifextreme.store", "https://www.lifextreme.com.pe")
        modified = modified.replace("http://www.lifextreme.store", "https://www.lifextreme.com.pe")
        modified = modified.replace("https://lifextreme.store", "https://www.lifextreme.com.pe")
        modified = modified.replace("http://lifextreme.store", "https://www.lifextreme.com.pe")
        modified = modified.replace("www.lifextreme.store", "www.lifextreme.com.pe")

        if modified != original:
            f.write_text(modified, encoding="utf-8")
            updated_count += 1
            print(f"  [OK] Actualizado: {rel}")

    print(f"\nTotal archivos actualizados en Fase 3: {updated_count}")


if __name__ == "__main__":
    main()
