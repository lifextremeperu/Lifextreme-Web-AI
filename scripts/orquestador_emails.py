import csv
import smtplib
import time
import random
import os
import json
import httpx
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Cargar variables de entorno (GMAIL_USER, GMAIL_PASS)
load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER") # Tu correo de Gmail
GMAIL_PASS = os.getenv("GMAIL_PASS") # Tu Contraseña de Aplicación de Gmail (App Password)

# Limite anti-spam de Google
MAX_EMAILS_PER_DAY = 10 

async def generate_personalized_email(agency_name, agency_reviews):
    """
    Usa Llama 3 local para redactar un correo hiper-personalizado.
    """
    prompt = f"""
    Eres el Director Comercial de Lifextreme AI (identidad Ayni Evolve).
    Escribe un correo en frío CORTO y DIRECTO (máximo 4 párrafos cortos) al dueño de la agencia de turismo '{agency_name}'.
    Sabemos que tienen {agency_reviews} reviews en internet.
    
    Tono: Corporativo pero agresivo en ventas. B2B.
    Objetivo: Venderles la "Auditoría Estratégica B2B" (Dashboard RAG) o invitarlos a una demo.
    
    Reglas:
    - No uses saludos clichés.
    - Menciona su cantidad de reviews para que sepan que los investigamos.
    - No incluyas Asunto (Subject) aquí, solo el cuerpo del correo en texto plano (nada de markdown).
    - Despídete formalmente como "El Cerebro Lifextreme".
    """
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json().get("response", "").strip()
    except Exception as e:
        print(f"Error con Llama 3: {e}")
        return "Hola, tenemos tecnología RAG para optimizar sus ventas. Contáctenos."

def send_email(to_email, subject, body):
    """Envía el correo usando Gmail SMTP"""
    if not GMAIL_USER or not GMAIL_PASS:
        print("[-] ERROR: Faltan las credenciales de Gmail en el archivo .env")
        return False
        
    try:
        msg = MIMEMultipart()
        msg['From'] = f"Lifextreme AI <{GMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        text = msg.as_string()
        server.sendmail(GMAIL_USER, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"[-] Error enviando a {to_email}: {e}")
        return False

async def main():
    print("=== ORQUESTADOR DE COLD EMAIL (ANTI-SPAM) ===")
    
    input_file = "../Lifextreme_B2B_Prospects_Con_Correo.csv"
    
    try:
        with open(input_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            prospects = list(reader)
    except FileNotFoundError:
        print(f"[-] No se encontró {input_file}. Ejecuta primero scraper_correos.py")
        return

    enviados_hoy = 0
    
    for row in prospects:
        if enviados_hoy >= MAX_EMAILS_PER_DAY:
            print(f"[!] Límite de {MAX_EMAILS_PER_DAY} correos por día alcanzado para evitar baneo.")
            break
            
        correos = row.get('correos_encontrados', '').split(' | ')
        # Filtrar vacíos
        correos = [c.strip() for c in correos if c.strip()]
        
        if not correos:
            continue # No hay correo
            
        target_email = correos[0] # Usar el primero encontrado
        agency_name = row.get('name', 'su agencia')
        reviews = row.get('reviews_count', 'varias')
        
        print(f"[*] Generando correo personalizado para {agency_name} con Llama 3...")
        cuerpo = await generate_personalized_email(agency_name, reviews)
        asunto = f"Oportunidad Tecnológica Exclusiva para {agency_name}"
        
        print(f"[+] Enviando correo a {target_email}...")
        exito = send_email(target_email, asunto, cuerpo)
        
        if exito:
            print("    ✅ Correo enviado con éxito.")
            enviados_hoy += 1
            
            # Anti-Spam Jitter (Pausa aleatoria entre 30 y 90 minutos)
            # Para testeo, lo pondremos entre 3 y 10 segundos
            jitter_seconds = random.randint(3, 10) 
            print(f"    ⏳ Pausa anti-spam activada. Esperando {jitter_seconds} segundos...\n")
            time.sleep(jitter_seconds)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
