import os
import sys
import re
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

def extract_prompt_from_master():
    master_path = Path("data/knowledge/prompts/pipeline_prompts_maestros.md")
    with open(master_path, 'r', encoding='utf-8') as f:
        content = f.read()
    bloque2_match = re.search(r'# BLOQUE 2 — PROMPT AGENTE CARTÓGRAFO.*?```(.*?)```', content, re.DOTALL)
    if bloque2_match:
        return bloque2_match.group(1).strip()
    return "Extrae 15 módulos TIER 2."

def main():
    load_dotenv()
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("departamento")
    parser.add_argument("--pais", default="Perú")
    args = parser.parse_args()
    
    departamento = args.departamento.lower()
    pais = args.pais
    
    output_dir = Path(f"data/knowledge/{departamento}")
    modulos_existentes_path = output_dir / "modulos_cartografo.txt"
    
    modulos_previos_texto = ""
    if modulos_existentes_path.exists():
        with open(modulos_existentes_path, 'r', encoding='utf-8') as f:
            modulos_previos_texto = f.read()
            
    # Extraer nombres para decirle a la IA qué ignorar
    nombres_previos = []
    for linea in modulos_previos_texto.split('\n'):
        if linea.startswith("MÓDULO:"):
            nombres_previos.append(linea.replace("MÓDULO:", "").strip())
            
    lista_exclusiones = "\n".join([f"- {n}" for n in nombres_previos])
    
    print(f"[+] Inicializando Agente Cartógrafo (BLOQUE 2) para {departamento.capitalize()}...")
    print(f"[+] Detectados {len(nombres_previos)} módulos previos. Excluyendo...")
    
    prompt_template = extract_prompt_from_master()
    prompt = prompt_template.replace("[DEPARTAMENTO]", departamento.capitalize()).replace("[PAÍS]", pais)
    
    instruccion_b2 = f"""
    ================================================================================================
    🚨 INSTRUCCIÓN CRÍTICA DE BLOQUE 2:
    YA HEMOS MAPEADO LOS 15 MÓDULOS PRINCIPALES DE ESTA REGIÓN.
    ESTOS SON LOS MÓDULOS QUE YA EXISTEN Y QUE ESTÁ ESTRICTAMENTE PROHIBIDO REPETIR:
    {lista_exclusiones}
    
    TU MISIÓN AHORA ES GENERAR LOS SIGUIENTES 15 MÓDULOS (TIER 2). Módulos del 16 al 30.
    Lugares secundarios, rutas alternativas, nichos específicos, pueblos alejados.
    NO MENCIONES NADA DE LA LISTA ANTERIOR.
    ================================================================================================
    """
    
    final_prompt = prompt.replace("PASO 1 — DIAGNÓSTICO DEL DESTINO", instruccion_b2 + "\nPASO 1 — DIAGNÓSTICO DEL DESTINO")
    
    print(f"[+] Conectando a Ollama Local (llama3)...")
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "prompt": final_prompt,
            "stream": False,
            "options": {"temperature": 0.4, "num_ctx": 8192}
        })
        response.raise_for_status()
        respuesta_texto = response.json().get("response", "")
    except Exception as e:
        print(f"[-] Error fatal: {e}")
        sys.exit(1)
        
    print("[+] ¡Respuesta recibida! Extrayendo nuevos módulos...")
    
    modulos_match = re.search(r'<modulos_generados>(.*?)</modulos_generados>', respuesta_texto, re.DOTALL)
    
    if modulos_match:
        nuevos_modulos = modulos_match.group(1).strip()
        # APPEND al archivo original
        with open(modulos_existentes_path, "a", encoding="utf-8") as f:
            f.write("\n\n" + nuevos_modulos)
        print(f"[+] Los 15 nuevos módulos (Bloque 2) han sido añadidos al archivo maestro.")
    else:
        print("[-] Error: No se encontraron etiquetas <modulos_generados>. Salida cruda guardada en modulos_b2_error.txt.")
        with open(output_dir / "modulos_b2_error.txt", "w", encoding="utf-8") as f:
            f.write(respuesta_texto)
            
    print("Misión Bloque 2 Completada.")

if __name__ == "__main__":
    main()
