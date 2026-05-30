import os
import sys
import re
import argparse
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage

def extract_prompt_from_master():
    master_path = Path("data/knowledge/prompts/pipeline_prompts_maestros.md")
    if not master_path.exists():
        print(f"[-] Error: No se encontró la Directiva Maestra en {master_path}")
        sys.exit(1)
        
    with open(master_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extraer el BLOQUE 2 (Cartógrafo)
    bloque2_match = re.search(r'# BLOQUE 2 — PROMPT AGENTE CARTÓGRAFO.*?```(.*?)```', content, re.DOTALL)
    if not bloque2_match:
        print("[-] Error: No se pudo extraer el prompt del BLOQUE 2 en la Directiva Maestra.")
        sys.exit(1)
        
    return bloque2_match.group(1).strip()

def main():
    load_dotenv()
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="Ejecutar el Agente Cartógrafo (Fase 1)")
    parser.add_argument("departamento", help="Nombre del departamento a minar")
    parser.add_argument("--pais", default="Perú", help="País (por defecto: Perú)")
    args = parser.parse_args()
    
    departamento = args.departamento.lower()
    pais = args.pais
    
    print(f"[+] Inicializando Agente Cartógrafo (Fase 1) para {departamento.capitalize()}...")
    
    prompt_template = extract_prompt_from_master()
    prompt = prompt_template.replace("[DEPARTAMENTO]", departamento.capitalize()).replace("[PAÍS]", pais)
    
    print(f"[+] Conectando a Vertex AI (gemini-2.5-flash) usando Service Account...")
    
    # Configurar el LLM para usar Vertex AI seguro (sin API Keys públicas)
    llm = ChatVertexAI(
        model_name="gemini-2.5-flash",
        project=os.getenv("GOOGLE_CLOUD_PROJECT", "lifextreme-arequipa-agent"),
        location=os.getenv("GOOGLE_CLOUD_REGION", "us-central1"),
        max_output_tokens=8192,
        temperature=0.3
    )
    
    print(f"[+] Enviando misión de prospección para: {departamento.capitalize()}. Esto tomará de 1 a 2 minutos...")
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        respuesta_texto = response.content
    except Exception as e:
        print(f"[-] Error fatal de conexión con Vertex AI: {e}")
        sys.exit(1)
    
    print("[+] ¡Respuesta recibida! Extrayendo módulos...")
    
    modulos_match = re.search(r'<modulos_generados>(.*?)</modulos_generados>', respuesta_texto, re.DOTALL)
    
    output_dir = Path(f"data/knowledge/{departamento}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if modulos_match:
        modulos_brutos = modulos_match.group(1).strip()
        with open(output_dir / "modulos_cartografo.txt", "w", encoding="utf-8") as f:
            f.write(modulos_brutos)
        print(f"[+] Se guardaron los módulos extraídos en: {output_dir / 'modulos_cartografo.txt'}")
    else:
        print("[-] No se encontraron etiquetas <modulos_generados>. Guardando salida cruda entera.")
        modulos_brutos = respuesta_texto
        with open(output_dir / "modulos_cartografo.txt", "w", encoding="utf-8") as f:
            f.write(modulos_brutos)
    
    # Extraer reporte de inteligencia (todo lo que no es módulos)
    texto_sin_modulos = re.sub(r'<modulos_generados>.*?</modulos_generados>', '\n[... MÓDULOS OMITIDOS AQUÍ ...]\n', respuesta_texto, flags=re.DOTALL)
    with open(output_dir / "reporte_inteligencia.txt", "w", encoding="utf-8") as f:
        f.write(texto_sin_modulos)
    
    print(f"[+] Reporte de Inteligencia (Diagnóstico y Cierre) guardado en: {output_dir / 'reporte_inteligencia.txt'}")
    print("\n========================================================")
    print("Misión Fase 1 Completada con Éxito.")
    print(f"Revisa los archivos en data/knowledge/{departamento}/ para validar el índice.")
    print("========================================================")

if __name__ == "__main__":
    main()
