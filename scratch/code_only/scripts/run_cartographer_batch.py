import os
import sys
import re
import argparse
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument("departamento")
    parser.add_argument("--pais", default="Perú")
    parser.add_argument("--batch", type=int, required=True, help="Número de bloque (ej: 3, 4)")
    args = parser.parse_args()
    
    departamento = args.departamento.lower()
    pais = args.pais
    batch_num = args.batch
    
    output_dir = Path(f"data/knowledge/{departamento}")
    modulos_existentes_path = output_dir / "modulos_cartografo.txt"
    
    modulos_previos_texto = ""
    if modulos_existentes_path.exists():
        with open(modulos_existentes_path, 'r', encoding='utf-8') as f:
            modulos_previos_texto = f.read()
            
    nombres_previos = []
    for linea in modulos_previos_texto.split('\n'):
        if linea.startswith("MÓDULO:"):
            nombres_previos.append(linea.replace("MÓDULO:", "").strip())
            
    lista_exclusiones = "\n".join([f"- {n}" for n in nombres_previos])
    
    print(f"[+] Inicializando Agente Cartógrafo (BLOQUE {batch_num}) para {departamento.capitalize()}...")
    print(f"[+] Detectados {len(nombres_previos)} módulos previos. Excluyendo...")
    
    prompt_template = extract_prompt_from_master()
    prompt = prompt_template.replace("[DEPARTAMENTO]", departamento.capitalize()).replace("[PAÍS]", pais)
    
    start_idx = ((batch_num - 1) * 15) + 1
    end_idx = batch_num * 15
    
    instruccion_dinamica = f"""
    ================================================================================================
    🚨 INSTRUCCIÓN CRÍTICA DE BLOQUE {batch_num}:
    YA HEMOS MAPEADO {len(nombres_previos)} MÓDULOS DE ESTA REGIÓN.
    ESTOS SON LOS MÓDULOS QUE YA EXISTEN Y QUE ESTÁ ESTRICTAMENTE PROHIBIDO REPETIR:
    {lista_exclusiones}
    
    TU MISIÓN AHORA ES GENERAR LOS SIGUIENTES 15 MÓDULOS (TIER {batch_num}). Módulos del {start_idx} al {end_idx}.
    Concéntrate en destinos secundarios, rutas alternativas, turismo vivencial, y ecosistemas ocultos.
    NO MENCIONES NADA DE LA LISTA ANTERIOR.
    ================================================================================================
    """
    
    prompt = prompt.replace("PASO 1 — DIAGNÓSTICO DEL DESTINO", instruccion_dinamica + "\nPASO 1 — DIAGNÓSTICO DEL DESTINO")
    
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'lifextreme-arequipa-agent'
    os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
    
    try:
        client = genai.Client(http_options=HttpOptions(api_version='v1'))
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(temperature=0.4, max_output_tokens=8192)
        )
        respuesta_texto = response.text
    except Exception as e:
        print(f"[-] Error fatal: {e}")
        sys.exit(1)
        
    print(f"[+] ¡Respuesta Bloque {batch_num} recibida! Extrayendo módulos...")
    modulos_match = re.search(r'<modulos_generados>(.*?)</modulos_generados>', respuesta_texto, re.DOTALL)
    
    if modulos_match:
        nuevos_modulos = modulos_match.group(1).strip()
        with open(modulos_existentes_path, "a", encoding="utf-8") as f:
            f.write("\n\n" + nuevos_modulos)
        print(f"[+] Los nuevos módulos del Bloque {batch_num} se guardaron exitosamente.")
    else:
        print("[-] Error de etiquetas. Intentando salvar crudo...")
        salvavidas = re.search(r'ID:.*?HUMAN_REVIEW:.*?$', respuesta_texto, re.DOTALL | re.MULTILINE)
        if salvavidas:
            with open(modulos_existentes_path, "a", encoding="utf-8") as f:
                f.write("\n\n" + salvavidas.group(0).strip())
            print(f"[+] Módulos salvados y añadidos al índice.")
        else:
            print("[-] No se pudieron salvar. Revisar logs.")
            with open(output_dir / f"modulos_error_b{batch_num}.txt", "w", encoding="utf-8") as f:
                f.write(respuesta_texto)
                
if __name__ == "__main__":
    main()
