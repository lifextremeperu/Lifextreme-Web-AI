"""
LIFEXTREME - MIGRACIÓN ATÓMICA DE DOMINIO A 'lifextreme.com.pe'
Este script automatiza la actualización de todas las referencias de dominio
en el código fuente: SEO canónico, OpenGraph, JSON-LD schemas, sitemaps, .env y prompts del bot.
Ejecutar mañana una vez adquirido y configurado el dominio en Vercel.
"""

import os
import re

OLD_DOMAIN = "lifextreme.store"
NEW_DOMAIN = "lifextreme.com.pe"

FILES_TO_UPDATE = [
    "index.html",
    "sitemap.xml",
    "sentinel-machupicchu.html",
    "blog.html",
    "empresa.html",
    "registro-guia.html",
    "embajadores.html",
    "seguros.html",
    "terminos.html",
    "privacidad.html",
    "cookies.html",
    "politica-proveedores.html",
    "esnna.html",
    "reclamaciones.html",
    "vr-experience.html",
    "open-source.html",
    ".env",
    "backend/discord_agent/rag_service.py",
    "promptfooconfig.yaml"
]

def migrate_domain():
    print(f"=== MIGRACIÓN ATÓMICA: {OLD_DOMAIN} -> {NEW_DOMAIN} ===")
    total_files = 0
    total_replacements = 0

    for file_path in FILES_TO_UPDATE:
        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            occurrences = content.count(OLD_DOMAIN)
            if occurrences > 0:
                new_content = content.replace(OLD_DOMAIN, NEW_DOMAIN)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                total_files += 1
                total_replacements += occurrences
                print(f"[OK] {file_path}: {occurrences} reemplazos realizados.")
        except Exception as e:
            print(f"[ERROR] En {file_path}: {e}")

    print("--------------------------------------------------")
    print(f"RESUMEN: {total_replacements} referencias migradas con éxito en {total_files} archivos.")
    print("Próximos pasos:")
    print("1. En Vercel: Settings -> Domains -> Añadir 'www.lifextreme.com.pe' y 'lifextreme.com.pe'")
    print("2. En NIC.pe / Punto.pe: Apuntar los registros DNS CNAME y A recomendados por Vercel.")
    print("3. En Google Search Console: Registrar la nueva propiedad https://www.lifextreme.com.pe")
    print("==================================================")

if __name__ == "__main__":
    migrate_domain()
