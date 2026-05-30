import os
import sys
import re
import argparse
from pathlib import Path
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

def extract_prompt_from_master():
    master_path = Path("data/knowledge/prompts/pipeline_prompts_maestros.md")
    with open(master_path, 'r', encoding='utf-8') as f:
        content = f.read()
    bloque2_match = re.search(r'# BLOQUE 2 — PROMPT AGENTE CARTÓGRAFO.*?```(.*?)```', content, re.DOTALL)
    return bloque2_match.group(1).strip()

def main():
    load_dotenv()
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("departamento")
    parser.add_argument("--pais", default="Perú")
    args = parser.parse_args()
    
    departamento = args.departamento.lower()
    pais = args.pais
    
    print(f"[+] Inicializando Agente Cartógrafo DIRECTO para {departamento.capitalize()}...")
    
    prompt_template = extract_prompt_from_master()
    prompt = prompt_template.replace("[DEPARTAMENTO]", departamento.capitalize()).replace("[PAÍS]", pais)
    
    # Inicializar Vertex AI SDK oficial
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "lifextreme-arequipa-agent")
    location = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    vertexai.init(project=project_id, location=location)
    
    model = GenerativeModel("gemini-2.5-flash")
    
    print(f"[+] Conectando a Vertex AI Oficial...")
    try:
        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 8192, "temperature": 0.3}
        )
        respuesta_texto = response.text
    except Exception as e:
        print(f"[-] Error fatal: {e}")
        sys.exit(1)
        
    print("[+] ¡Respuesta recibida! Extrayendo módulos...")
    
    modulos_match = re.search(r'<modulos_generados>(.*?)</modulos_generados>', respuesta_texto, re.DOTALL)
    output_dir = Path(f"data/knowledge/{departamento}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if modulos_match:
        with open(output_dir / "modulos_cartografo.txt", "w", encoding="utf-8") as f:
            f.write(modulos_match.group(1).strip())
        print(f"[+] Módulos guardados exitosamente.")
    else:
        with open(output_dir / "modulos_cartografo.txt", "w", encoding="utf-8") as f:
            f.write(respuesta_texto)
        print("[-] Se guardó la salida cruda.")
        
    texto_sin_modulos = re.sub(r'<modulos_generados>.*?</modulos_generados>', '\n[... MÓDULOS OMITIDOS ...]\n', respuesta_texto, flags=re.DOTALL)
    with open(output_dir / "reporte_inteligencia.txt", "w", encoding="utf-8") as f:
        f.write(texto_sin_modulos)
        
    print("Misión Completada.")

if __name__ == "__main__":
    main()
