import os
import sys
import re
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig

def extract_prompt_from_master():
    master_path = Path("data/knowledge/prompts/pipeline_prompts_maestros.md")
    with open(master_path, 'r', encoding='utf-8') as f:
        content = f.read()
    bloque_match = re.search(r'# BLOQUE 2 — PROMPT AGENTE CARTÓGRAFO.*?```(.*?)```', content, re.DOTALL)
    return bloque_match.group(1).strip()

def main():
    load_dotenv()
    sys.stdout.reconfigure(encoding='utf-8')
    
    pdf_path = r"C:\Users\ASUS\Downloads\Plan_estrategico_tursimo_PERTUR_Amazonas_2020_keyword_principal (1).pdf"
    
    if not os.path.exists(pdf_path):
        print(f"[-] ERROR: No se encontró el archivo PDF en la ruta:\n{pdf_path}")
        sys.exit(1)
        
    departamento = "amazonas"
    pais = "Perú"
    
    output_dir = Path(f"data/knowledge/{departamento}")
    output_dir.mkdir(parents=True, exist_ok=True)
    modulos_path = output_dir / "modulos_cartografo.txt"
    
    print("===================================================================")
    print(" 🚀 PILOTO DE INGESTA DE PDF OFICIAL (PERTUR) -> JSON ESTRUCTURADO ")
    print("===================================================================")
    
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'lifextreme-arequipa-agent'
    os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'False' # Usaremos la API de Gemini Studio para el File API que es más estable con PDFs
    
    # Intentar usar el File API de Gemini
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
             print("[-] Necesitamos GEMINI_API_KEY para usar el File API de Google AI Studio.")
             # Fallback a vertex si no hay key
             os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
             client = genai.Client(http_options=HttpOptions(api_version='v1'))
        else:
             client = genai.Client(api_key=api_key)
             
        print("[+] Conectando a Google AI...")
        print(f"[+] Subiendo PDF a la memoria de Gemini... (Esto puede tomar unos segundos)")
        
        uploaded_file = client.files.upload(file=pdf_path)
        print(f"[+] Archivo subido exitosamente: {uploaded_file.name}")
        
        # Esperar a que se procese el archivo (los PDFs grandes toman tiempo en ser escaneados por el OCR interno)
        print("[+] Esperando a que el motor de IA indexe el PDF...")
        while uploaded_file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)
            
        print("\n[+] PDF Procesado y listo para lectura.")
        
        print("[+] Preparando Prompt Cartógrafo para Amazonas...")
        prompt_template = extract_prompt_from_master()
        prompt = prompt_template.replace("[DEPARTAMENTO]", departamento.capitalize()).replace("[PAÍS]", pais)
        
        instruccion_pdf = """
        ================================================================================================
        🚨 DIRECTIVA ESPECIAL (INGESTA DE PDF OFICIAL):
        Te estoy adjuntando el "Plan Estratégico Regional de Turismo (PERTUR) de Amazonas".
        TU MISIÓN ES LEER ESTE DOCUMENTO OFICIAL Y EXTRAER LA INTELIGENCIA DE ALLÍ.
        NO INVENTES NADA QUE NO ESTÉ RESPALDADO POR ESTE DOCUMENTO.
        Extrae los 15 módulos más críticos y de mayor potencial mencionados en el PERTUR.
        Respeta el formato <modulos_generados> exactamente como se te pide.
        ================================================================================================
        """
        
        prompt = prompt.replace("PASO 1 — DIAGNÓSTICO DEL DESTINO", instruccion_pdf + "\nPASO 1 — DIAGNÓSTICO DEL DESTINO")
        
        print("[+] Analizando PDF y extrayendo 15 Módulos Maestros (Tier 1)...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_file, prompt],
            config=GenerateContentConfig(temperature=0.2, max_output_tokens=8192)
        )
        
        respuesta_texto = response.text
        
        print("[+] ¡Análisis completado! Guardando índice de Amazonas...")
        modulos_match = re.search(r'<modulos_generados>(.*?)</modulos_generados>', respuesta_texto, re.DOTALL)
        
        if modulos_match:
            nuevos_modulos = modulos_match.group(1).strip()
            with open(modulos_path, "w", encoding="utf-8") as f:
                f.write(nuevos_modulos)
            print(f"[+] ¡ÉXITO! Los módulos extraídos del PDF se guardaron en: {modulos_path}")
        else:
            print("[-] Error de formato. Guardando salida cruda.")
            with open(output_dir / "modulos_pdf_error.txt", "w", encoding="utf-8") as f:
                f.write(respuesta_texto)
                
    except Exception as e:
        print(f"[-] Error durante la ingesta del PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
