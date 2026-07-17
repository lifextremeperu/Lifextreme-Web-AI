import csv
import json
import os
import re

CSV_FILE = "tours_faq.csv"
INDEX_FILE = "index.html"

def generate_json_ld():
    print("[*] Generando JSON-LD para Optimización GEO...")
    faq_items = []
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            next(reader, None) # Skip header
            count = 0
            for row in reader:
                if not row or len(row) < 2: continue
                q = row[0].strip()
                a = row[1].strip()
                if not q or not a: continue
                
                # Para GEO, Schema.org FAQPage es excelente porque Google/Perplexity
                # extraen directamente las respuestas para sus overviews
                faq_items.append({
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a
                    }
                })
                count += 1
                if count >= 20: # Limitamos a los 20 más importantes para no saturar el HTML
                    break
                    
    except Exception as e:
        print(f"[-] Error leyendo CSV: {e}")
        return None

    if not faq_items:
        return None
        
    schema_data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_items
    }
    
    # También agregamos la metadata de la empresa (Organization)
    org_data = {
        "@context": "https://schema.org",
        "@type": "TravelAgency",
        "name": "Lifextreme",
        "url": "https://lifextreme.store",
        "description": "Agencia operadora de turismo de aventura en Perú.",
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "PE"
        }
    }
    
    return [org_data, schema_data]

def inject_into_html(json_ld_data):
    if not json_ld_data:
        print("[-] No hay datos JSON-LD para inyectar.")
        return
        
    print(f"[*] Inyectando etiquetas invisibles en {INDEX_FILE}...")
    
    json_ld_str = json.dumps(json_ld_data, ensure_ascii=False, indent=2)
    script_block = f"""\n    <!-- GEO SEO BLOCK START -->\n    <script type="application/ld+json">\n    {json_ld_str}\n    </script>\n    <!-- GEO SEO BLOCK END -->\n"""
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # Remover bloque anterior si existe
    html_content = re.sub(r'<!-- GEO SEO BLOCK START -->.*?<!-- GEO SEO BLOCK END -->', '', html_content, flags=re.DOTALL)
    
    # Insertar antes de </head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', script_block + '</head>')
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("[+] ¡Inyección exitosa! El archivo index.html ahora es 100% amigable para IA.")
    else:
        print("[-] No se encontró la etiqueta </head> en index.html")

def main():
    json_ld_data = generate_json_ld()
    inject_into_html(json_ld_data)

if __name__ == "__main__":
    main()
