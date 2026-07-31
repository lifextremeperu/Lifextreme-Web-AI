import httpx
import re
import csv
import asyncio
from bs4 import BeautifulSoup
import time

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
# Evitar correos basura comunes
EXCLUDE_EMAILS = ['sentry', 'wix', 'png', 'jpg', 'example']

async def extract_emails_from_url(client, url):
    if not url.startswith('http'):
        url = 'https://' + url
        
    emails = set()
    try:
        # Timeout corto para no quedarnos pegados
        response = await client.get(url, timeout=10.0, follow_redirects=True)
        text = response.text
        
        # Buscar en la página principal
        found = re.findall(EMAIL_REGEX, text)
        for e in found:
            e = e.lower()
            if not any(ex in e for ex in EXCLUDE_EMAILS):
                emails.add(e)
                
        # Intentar buscar en la página de contacto si no encontramos nada
        if not emails:
            contact_urls = [url + "/contacto", url + "/contact", url + "/contact-us"]
            for curl in contact_urls:
                try:
                    c_resp = await client.get(curl, timeout=5.0, follow_redirects=True)
                    found_c = re.findall(EMAIL_REGEX, c_resp.text)
                    for e in found_c:
                        e = e.lower()
                        if not any(ex in e for ex in EXCLUDE_EMAILS):
                            emails.add(e)
                except:
                    pass
                    
        return list(emails)
    except Exception as e:
        print(f"[-] Error accediendo a {url}: {e}")
        return []

async def main():
    print("=== EXTRACTOR AUTÓNOMO DE CORREOS LIFEXTREME ===")
    
    # Leer el archivo CSV existente de B2B
    input_file = "../Lifextreme_B2B_Prospects.csv"
    output_file = "../Lifextreme_B2B_Prospects_Con_Correo.csv"
    
    rows = []
    try:
        with open(input_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        print(f"No se encontró {input_file}. Ejecuta esto desde la carpeta scripts/")
        return

    print(f"[+] Procesando {len(rows)} agencias B2B...")
    
    # httpx doesn't verify SSL to prevent errors on bad agency sites
    async with httpx.AsyncClient(verify=False) as client:
        for row in rows:
            website = row.get('website', '').strip()
            if website:
                print(f"[*] Buscando correos en: {website}...")
                correos = await extract_emails_from_url(client, website)
                row['correos_encontrados'] = " | ".join(correos)
                print(f"    -> Encontrados: {row['correos_encontrados']}")
            else:
                row['correos_encontrados'] = ""
            
            # Pausa para no ser bloqueados por los servidores web
            time.sleep(1)

    # Guardar nuevo CSV
    if rows:
        fieldnames = list(rows[0].keys())
        with open(output_file, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            
        print(f"\n✅ Extracción completada. Guardado en: {output_file}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    asyncio.run(main())
