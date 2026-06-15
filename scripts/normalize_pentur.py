import os
import sys
import glob
import json
import time
import requests
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi3:latest" 

SYSTEM_PROMPT = """Actúa como el Director de Inversiones (CIO) de Lifextreme, una agencia de turismo de vanguardia.
A continuación tienes datos extraídos del PENTUR/PERTUR oficial del gobierno para una región.
Tu tarea es leer estos datos macro y extraer inteligencia puramente B2B (oportunidades de negocio, riesgos, plan del gobierno y datos macro) y responder ESTRICTAMENTE en formato JSON con la siguiente estructura, sin texto adicional ni bloques de markdown (```json):

{
  "region": "Nombre de la región",
  "oportunidades_negocio": ["Déficit de servicios", "nuevas tendencias"],
  "riesgos_inversion": ["Brechas de infraestructura", "conflictos sociales"],
  "datos_macro_clave": ["Cifras de crecimiento", "estadísticas"],
  "plan_gobierno": ["Inversión pública proyectada", "proyectos"],
  "resumen_ejecutivo": "Resumen táctico de alto nivel para el CEO"
}

Si el texto no contiene datos relevantes para alguna lista, deja el array vacío [].
Asegúrate de que la salida sea UNICAMENTE un JSON válido que pueda ser procesado por json.loads().
"""

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass
    
    print("==================================================")
    print(" >>> INICIANDO NORMALIZACIÓN ESTRATÉGICA PENTUR (B2B Local)")
    print("==================================================")
    
    pentur_files = glob.glob('data/knowledge/peru/*/modulos_pdf_error.txt')
    print(f"[+] Se encontraron {len(pentur_files)} archivos crudos de PENTUR.")
    
    for file_path in pentur_files:
        region = Path(file_path).parent.name
        output_file = Path(file_path).parent / "strategic_insights.json"
        
        if output_file.exists():
            print(f"[>] Región {region.capitalize()} ya tiene insights. Saltando...")
            continue
            
        print(f"\n[>] Analizando a nivel corporativo: {region.capitalize()}...")
        
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                texto_crudo = f.read()
                
            # Limitar a 40k caracteres para Ollama local (Phi3)
            texto_crudo = texto_crudo[:40000] 
            
            user_message = f"Analiza los siguientes datos de la región {region.capitalize()} y genera el JSON correspondiente:\n\n{texto_crudo}"
            
            print(f"    -> Conectando con {MODEL} (Ollama) para extraer Insights...")
            res = requests.post(OLLAMA_URL, json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                "stream": False,
                "format": "json"
            }, timeout=600)
            
            if res.ok:
                respuesta_json = res.json()['message']['content']
                with open(output_file, "w", encoding="utf-8") as out:
                    out.write(respuesta_json)
                print(f"    [+] Intelligence Report guardado: {output_file}")
            else:
                print(f"    [-] Error HTTP {res.status_code}: {res.text}")
            
        except Exception as e:
            print(f"    [-] Error procesando {region}: {e}")
            
        time.sleep(2)

    print("==================================================")
    print(" ✅ NORMALIZACIÓN B2B COMPLETADA.")
    print("==================================================")

if __name__ == "__main__":
    main()
