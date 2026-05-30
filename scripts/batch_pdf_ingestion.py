import os
import sys
import re
import time
import glob
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig, Part

def extract_prompt_from_master():
    master_path = Path("data/knowledge/prompts/pipeline_prompts_maestros.md")
    with open(master_path, 'r', encoding='utf-8') as f:
        content = f.read()
    bloque_match = re.search(r'# BLOQUE 2 — PROMPT AGENTE CARTÓGRAFO.*?```(.*?)```', content, re.DOTALL)
    return bloque_match.group(1).strip()

def extract_region_from_filename(filename):
    match = re.search(r'PERTUR_([A-Za-záéíóúÁÉÍÓÚñÑ]+)_', filename, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return "desconocido"

def process_pdf(client, pdf_path, region):
    output_dir = Path(f"data/knowledge/{region}")
    output_dir.mkdir(parents=True, exist_ok=True)
    modulos_path = output_dir / "modulos_cartografo.txt"
    
    if modulos_path.exists():
        print(f"[-] Saltando {region.capitalize()}: El índice ya existe.")
        return
        
    print(f"\n[>>>] PROCESANDO REGIÓN: {region.upper()}")
    print(f"[+] Leyendo archivo PDF en memoria (Vertex AI mode): {os.path.basename(pdf_path)}")
    
    # Vertex AI requiere enviar el archivo crudo en Base64/Bytes si no usamos Cloud Storage
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
        
    pdf_part = Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")
    print(f"[+] Archivo cargado en memoria ({len(pdf_bytes) / 1024 / 1024:.2f} MB)")
    
    prompt_template = extract_prompt_from_master()
    prompt = prompt_template.replace("[DEPARTAMENTO]", region.capitalize()).replace("[PAÍS]", "Perú")
    
    instruccion_pdf = """
    ================================================================================================
    🚨 DIRECTIVA ESPECIAL (INGESTA DE PDF OFICIAL PERTUR):
    Te estoy adjuntando el Plan Estratégico Regional de Turismo oficial.
    TU MISIÓN ES LEER ESTE DOCUMENTO OFICIAL Y EXTRAER LA INTELIGENCIA DE ALLÍ.
    Extrae los 15 módulos más críticos y de mayor potencial mencionados en el PERTUR.
    Respeta el formato <modulos_generados> exactamente como se te pide.
    ================================================================================================
    """
    prompt = prompt.replace("PASO 1 — DIAGNÓSTICO DEL DESTINO", instruccion_pdf + "\nPASO 1 — DIAGNÓSTICO DEL DESTINO")
    
    try:
        print("[+] Conectando a Vertex AI y analizando PDF...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[pdf_part, prompt],
            config=GenerateContentConfig(temperature=0.2, max_output_tokens=8192)
        )
        
        modulos_match = re.search(r'<modulos_generados>(.*?)</modulos_generados>', response.text, re.DOTALL)
        if modulos_match:
            with open(modulos_path, "w", encoding="utf-8") as f:
                f.write(modulos_match.group(1).strip())
            print(f"[+] ¡ÉXITO! 15 Módulos de {region.capitalize()} extraídos y guardados en {modulos_path}")
        else:
            print(f"[-] Error de formato para {region}. Guardando crudo...")
            with open(output_dir / "modulos_pdf_error.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
                
    except Exception as e:
        print(f"[-] Error generando contenido para {region}: {e}")

def main():
    load_dotenv()
    sys.stdout.reconfigure(encoding='utf-8')
    
    pdf_dir = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\PENTUR"
    pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    print("===================================================================")
    print(f" 🚀 INGESTA MASIVA DE PDFs (VERTEX AI NATIVE) -> {len(pdfs)} Documentos")
    print("===================================================================")
    
    # FORZAMOS VERTEX AI EN EL SCRIPT (Ignoramos la API KEY)
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'lifextreme-arequipa-agent'
    os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
    
    # El cliente automáticamente tomará el service_account.json definido en GOOGLE_APPLICATION_CREDENTIALS en el .env
    client = genai.Client(http_options=HttpOptions(api_version='v1'))
    
    for pdf_path in pdfs:
        # Excluir duplicados si los hay
        if "(1)" in pdf_path: continue
        
        region = extract_region_from_filename(os.path.basename(pdf_path))
        if region != "desconocido":
            process_pdf(client, pdf_path, region)
            time.sleep(5) # Protección contra cuotas de Vertex AI

if __name__ == "__main__":
    main()
