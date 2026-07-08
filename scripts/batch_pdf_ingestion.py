import os
import sys
import re
import time
import glob
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from pypdf import PdfReader

def extract_prompt_from_master():
    master_path = Path("data/knowledge/prompts/pipeline_prompts_maestros.md")
    with open(master_path, 'r', encoding='utf-8') as f:
        content = f.read()
    bloque_match = re.search(r'# BLOQUE 2 — PROMPT AGENTE CARTÓGRAFO.*?```(.*?)```', content, re.DOTALL)
    if bloque_match:
        return bloque_match.group(1).strip()
    return "Extrae los 15 módulos más críticos."

def extract_region_from_filename(filename):
    match = re.search(r'PERTUR_([A-Za-záéíóúÁÉÍÓÚñÑ]+)_', filename, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return "desconocido"

def process_pdf(pdf_path, region):
    output_dir = Path(f"data/knowledge/{region}")
    output_dir.mkdir(parents=True, exist_ok=True)
    modulos_path = output_dir / "modulos_cartografo.txt"
    
    if modulos_path.exists():
        print(f"[-] Saltando {region.capitalize()}: El índice ya existe.")
        return
        
    print(f"\n[>>>] PROCESANDO REGIÓN: {region.upper()}")
    print(f"[+] Extrayendo texto del PDF localmente: {os.path.basename(pdf_path)}")
    
    try:
        reader = PdfReader(pdf_path)
        pdf_text = ""
        # Extraer solo las primeras 50 páginas para no saturar el contexto de Ollama
        for page in reader.pages[:50]:
            pdf_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"[-] Error leyendo PDF: {e}")
        return
        
    prompt_template = extract_prompt_from_master()
    prompt_base = prompt_template.replace("[DEPARTAMENTO]", region.capitalize()).replace("[PAÍS]", "Perú")
    
    instruccion_pdf = """
    🚨 DIRECTIVA ESPECIAL (INGESTA DE PDF OFICIAL PERTUR):
    A continuación se proporciona el texto extraído del Plan Estratégico Regional de Turismo oficial.
    TU MISIÓN ES LEER ESTE DOCUMENTO OFICIAL Y EXTRAER LA INTELIGENCIA DE ALLÍ.
    Extrae los 15 módulos más críticos y de mayor potencial mencionados en el PERTUR.
    Respeta el formato <modulos_generados> exactamente como se te pide.
    """
    
    final_prompt = f"{instruccion_pdf}\n\nTEXTO DEL PDF:\n{pdf_text[:30000]}\n\nINSTRUCCIONES:\n{prompt_base}"
    
    try:
        print("[+] Conectando a Ollama Local (llama3)...")
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "prompt": final_prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_ctx": 8192}
        })
        response.raise_for_status()
        result_text = response.json().get("response", "")
        
        modulos_match = re.search(r'<modulos_generados>(.*?)</modulos_generados>', result_text, re.DOTALL)
        if modulos_match:
            with open(modulos_path, "w", encoding="utf-8") as f:
                f.write(modulos_match.group(1).strip())
            print(f"[+] ¡ÉXITO! 15 Módulos de {region.capitalize()} extraídos y guardados en {modulos_path}")
        else:
            print(f"[-] Error de formato para {region}. Guardando crudo...")
            with open(output_dir / "modulos_pdf_error.txt", "w", encoding="utf-8") as f:
                f.write(result_text)
                
    except Exception as e:
        print(f"[-] Error generando contenido para {region}: {e}")

def main():
    load_dotenv()
    sys.stdout.reconfigure(encoding='utf-8')
    
    pdf_dir = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\PENTUR"
    pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    print("===================================================================")
    print(f" 🚀 INGESTA MASIVA DE PDFs (OLLAMA LOCAL) -> {len(pdfs)} Documentos")
    print("===================================================================")
    
    for pdf_path in pdfs:
        # Excluir duplicados si los hay
        if "(1)" in pdf_path: continue
        
        region = extract_region_from_filename(os.path.basename(pdf_path))
        if region != "desconocido":
            process_pdf(pdf_path, region)

if __name__ == "__main__":
    main()
