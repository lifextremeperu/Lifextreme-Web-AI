import os
import sys
import sqlite3
import pandas as pd
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import argparse
import time
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import urllib3

# Suprimir advertencias de SSL al usar verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

# Configuración
EXCEL_PATH = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\AGENCIAS Y OPERADORES\AGENCIAS DE VIAJES 01-08-2022 DIVIDIDO.xlsx"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "outreach_tracker.db")

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:8b"

ZOHO_EMAIL = "contacto@lifextreme.store"
ZOHO_PASSWORD = os.getenv("ZOHO_PASSWORD", "TU_PASSWORD_AQUI")
ZOHO_SMTP = "smtp.zoho.com"
ZOHO_PORT = 465

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prospects (
            ruc TEXT PRIMARY KEY,
            razon_social TEXT,
            nombre_comercial TEXT,
            web TEXT,
            region TEXT,
            email TEXT,
            status TEXT DEFAULT 'PENDING',
            sent_date TEXT,
            pitch_text TEXT,
            enriched_profile TEXT
        )
    ''')
    
    # Agregar columna si no existe (por si venimos de version anterior)
    try:
        cursor.execute("ALTER TABLE prospects ADD COLUMN enriched_profile TEXT")
    except sqlite3.OperationalError:
        pass # La columna ya existe
        
    # Check if empty
    cursor.execute("SELECT COUNT(*) FROM prospects")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("[*] Base de datos vacía. Importando desde Excel...")
        try:
            df = pd.read_excel(EXCEL_PATH, header=None)
            header_idx = 0
            for i in range(10):
                row_vals = [str(x).upper() for x in df.iloc[i].values]
                if any("RUC" in v for v in row_vals) and any("CORREO" in v for v in row_vals):
                    header_idx = i
                    break
                    
            df = pd.read_excel(EXCEL_PATH, skiprows=header_idx)
            df.columns = [str(c).strip().upper() for c in df.columns]
            
            email_col = next((c for c in df.columns if 'CORREO' in c), None)
            ruc_col = next((c for c in df.columns if 'RUC' in c), None)
            razon_col = next((c for c in df.columns if 'RAZ' in c and 'SOCIAL' in c), None)
            comercial_col = next((c for c in df.columns if 'COMERCIAL' in c), None)
            web_col = next((c for c in df.columns if 'WEB' in c), None)
            region_col = next((c for c in df.columns if 'DEPARTAMENTO' in c or 'PROVINCIA' in c), None)
            
            if not email_col:
                print("[-] No se encontro columna de correo electronico.")
                conn.close()
                return

            df = df.dropna(subset=[email_col])
            
            inserted = 0
            for _, row in df.iterrows():
                email = str(row.get(email_col, '')).strip()
                if '@' not in email:
                    continue
                    
                ruc = str(row.get(ruc_col, '')) if ruc_col else ''
                razon_social = str(row.get(razon_col, '')) if razon_col else ''
                nombre_comercial = str(row.get(comercial_col, razon_social)) if comercial_col else razon_social
                web = str(row.get(web_col, '')) if web_col else ''
                region = str(row.get(region_col, '')) if region_col else ''
                
                try:
                    cursor.execute('''
                        INSERT INTO prospects (ruc, razon_social, nombre_comercial, web, region, email)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (ruc, razon_social, nombre_comercial, web, region, email))
                    inserted += 1
                except sqlite3.IntegrityError:
                    pass
                    
            conn.commit()
            print(f"[+] Se importaron {inserted} agencias válidas a la base de datos de prospección.")
        except Exception as e:
            print(f"[-] Error leyendo el Excel: {e}")
            
    conn.close()

def extract_json_with_llm(text_content, empresa):
    prompt = f"""
Extrae la siguiente información estratégica de la empresa "{empresa}" basada SOLO en el texto de su web proporcionado.
Devuelve el resultado ESTRICTAMENTE en formato JSON, sin texto adicional.
Si no encuentras un dato, pon "No encontrado".

Formato esperado:
{{
    "nivel_digitalizacion": "¿Tienen motor de reservas (carrito/pagos) o solo formulario/WhatsApp?",
    "publico_objetivo": "¿En qué idiomas está la web o en qué moneda venden (USD/PEN)?",
    "catalogo_tours": "¿Qué tipo de turismo venden principalmente? (Ej. Aventura, Clásico, Lujo, Místico)",
    "propuesta_valor": "¿Qué los hace únicos según su web? (Ej. Sostenibles, operadores directos, experiencia)",
    "certificaciones_reputacion": "¿Tienen sellos de TripAdvisor, MINCETUR, SERNANP o similares?"
}}

Texto de la web para analizar:
{text_content[:1500]} # LIMITADO A 1500 CARACTERES PARA EVITAR SOBRECARGA
"""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        text = response.json().get("response", "").strip()
        # Clean potential markdown markdown blocks
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    except Exception as e:
        print(f"[-] Error en extracción LLM: {e}")
        return "{}"

def fetch_website_text(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
            
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        try:
            # Intento con HTTPS y verify=False
            response = requests.get(url, headers=headers, timeout=10, verify=False)
        except requests.exceptions.RequestException:
            # Si falla HTTPS, intenta HTTP
            url = url.replace('https://', 'http://')
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extraer texto limpio
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ')
        return " ".join(text.split())
    except Exception as e:
        return ""

def fallback_duckduckgo(empresa, region):
    print("      [-] Falló el scraping directo. Activando Plan B (DuckDuckGo)...")
    ddgs = DDGS()
    query = f"{empresa} agencia de viajes {region} acerca de nosotros"
    snippets = []
    try:
        results = ddgs.text(query, region='pe-es', max_results=3)
        for r in results:
            snippets.append(r.get('body', ''))
            snippets.append(r.get('title', ''))
    except Exception as e:
        print(f"      [-] Error en DuckDuckGo: {e}")
    return " ".join(snippets)

def perform_enrichment(limit=5):
    print(f"[*] Iniciando fase de ENRIQUECIMIENTO (Investigando {limit} agencias con web)...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ruc, nombre_comercial, region, web FROM prospects WHERE status = 'PENDING' AND web IS NOT NULL AND web != '' AND web != 'nan' LIMIT ?", (limit,))
    targets = cursor.fetchall()
    
    if not targets:
        print("[-] No hay agencias PENDING con web válida para enriquecer.")
        conn.close()
        return

    for ruc, empresa, region, web in targets:
        print(f"\n[>>>] Investigando la web de: {empresa} ({web})")
        
        combined_text = fetch_website_text(web)
        
        if len(combined_text) < 100:
            combined_text = fallback_duckduckgo(empresa, region)
            
        if len(combined_text) < 50:
            print("      [-] No se encontró información en la web ni en buscadores.")
            profile_json = '{"error": "Agencia sin huella digital"}'
        else:
            print("      [+] Analizando datos encontrados con IA (Qwen2.5 a 1500 caracteres max)...")
            profile_json = extract_json_with_llm(combined_text, empresa)
            
        print("      [✔] Perfil estratégico extraído:")
        print(profile_json)
        
        cursor.execute("UPDATE prospects SET status = 'ENRICHED', enriched_profile = ? WHERE ruc = ?", (profile_json, ruc))
        conn.commit()
        
        print("      [⏳] Descansando 5 segundos para no saturar...")
        time.sleep(5) 
        
    conn.close()
    print("\n[✔] Fase de enriquecimiento finalizada.")

def get_qdrant_insights(region):
    try:
        client = QdrantClient(QDRANT_URL)
        dept = region.split('/')[0].strip().lower() if region else "peru"
        records, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=5,
            with_payload=True,
            with_vectors=False
        )
        insights = []
        for r in records:
            if r.payload.get("region", "").lower() == dept:
                insights.append(r.payload.get("text_content", ""))
        return "\n".join(insights[:3])
    except:
        return ""

def generate_personalized_pitch(empresa, region, profile_json, insights):
    prompt = f"""
Eres Max, el Director Comercial de Lifextreme AI, una plataforma SaaS B2B de Inteligencia Artificial para Turismo de Aventura.
Escribe un "Cold Email" corto, potente y MUY personalizado para venderle nuestro sistema a esta Agencia de Viajes.

DATOS EXTRAIDOS (INVESTIGACION PREVIA):
{profile_json}

CONTEXTO DE INTELIGENCIA DE LIFEXTREME SOBRE {region}:
{insights if insights else 'Contamos con alertas predictivas del clima y demanda en su zona.'}

INSTRUCCIONES DEL CORREO:
1. Dirígete por su nombre al titular o representante legal si lo encontramos en los datos. Si no, a la gerencia de {empresa}.
2. Usa Neuromarketing: menciona su giro de negocio y si su estado en SUNAT está activo. Si ves que no tienen tecnología moderna en los datos extraidos, ofréceles nuestra automatización RAG y motor de reservas IA.
3. Llamado a la acción (CTA): Invitarlos a probar el sistema o agendar una demo corta.
4. FIRMA: Despídete como "Max - Lifextreme AI Core".
5. SOLO devuelve el cuerpo del correo y el asunto en formato ASUNTO: [asunto] \n\n CUERPO: [cuerpo]

Escribe el correo ahora:
"""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.5}
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        text = response.json().get("response", "")
        asunto = f"Oportunidad de IA para {empresa}"
        cuerpo = text
        if "ASUNTO:" in text and "CUERPO:" in text:
            parts = text.split("CUERPO:")
            asunto = parts[0].replace("ASUNTO:", "").strip()
            cuerpo = parts[1].strip()
        return asunto, cuerpo
    except Exception as e:
        return None, None

def perform_outreach(dry_run=False, limit=10):
    print(f"[*] Iniciando fase de OUTREACH (Redactando {limit} correos)...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ruc, nombre_comercial, region, email, enriched_profile FROM prospects WHERE status = 'ENRICHED' LIMIT ?", (limit,))
    targets = cursor.fetchall()
    
    if not targets:
        print("[-] No hay agencias ENRICHED. Ejecuta primero con --enrich.")
        conn.close()
        return

    for ruc, empresa, region, email, enriched_profile in targets:
        print(f"\n[>>>] Prospectando: {empresa}")
        insights = get_qdrant_insights(region)
        print("      Redactando email de Neuromarketing usando el perfil investigado...")
        asunto, cuerpo = generate_personalized_pitch(empresa, region, enriched_profile, insights)
        
        if not asunto:
            continue
            
        print("-" * 50)
        print(f"📩 PARA: {email}")
        print(f"📌 ASUNTO: {asunto}")
        print("-" * 50)
        print(cuerpo)
        print("-" * 50)
        
        if dry_run:
            print("[DRY RUN] -> El correo NO ha sido enviado.")
        else:
            print("[!] Función de envío (Zoho) simulada por ahora...")
            # success = send_email(email, asunto, cuerpo)
            # update status to EMAILED...
            
        time.sleep(2)
        
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Hunter Agent - Lifextreme B2B Outreach")
    parser.add_argument("--enrich", action="store_true", help="Investiga a las agencias en internet.")
    parser.add_argument("--outreach", action="store_true", help="Redacta y envia correos a las agencias enriquecidas.")
    parser.add_argument("--dry-run", action="store_true", help="Solo redacta, no envía (para modo outreach).")
    parser.add_argument("--limit", type=int, default=10, help="Limite de agencias a procesar.")
    args = parser.parse_args()
    
    print("==================================================")
    print(" 🎯 AGENTE HUNTER: PROSPECCIÓN B2B (LIFEXTREME) ")
    print("==================================================")
    
    init_db()
    
    if not args.enrich and not args.outreach:
        print("[-] Debes especificar --enrich o --outreach. Usa -h para ayuda.")
        return
        
    if args.enrich:
        perform_enrichment(limit=args.limit)
        
    if args.outreach:
        perform_outreach(dry_run=args.dry_run, limit=args.limit)

if __name__ == "__main__":
    main()
