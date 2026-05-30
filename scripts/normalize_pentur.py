import os
import sys
import glob
import json
import time
from pathlib import Path
from dotenv import load_dotenv

from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig

# Agregar src al path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.models.corporate_schema import StrategicInsightSchema

def main():
    load_dotenv()
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================")
    print(" >>> INICIANDO NORMALIZACIÓN ESTRATÉGICA PENTUR (B2B)")
    print("==================================================")
    
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'lifextreme-arequipa-agent'
    os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
    
    try:
        client = genai.Client(http_options=HttpOptions(api_version='v1'))
    except Exception as e:
        print(f"[-] Error conectando a Vertex AI: {e}")
        sys.exit(1)
        
    pentur_files = glob.glob('data/knowledge/*/modulos_pdf_error.txt')
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
                
            # Limitar a 150k caracteres para agilizar y mantener el foco
            texto_crudo = texto_crudo[:150000] 
            
            prompt = f"""
            Actúa como el Director de Inversiones (CIO) de Lifextreme, una agencia de turismo de vanguardia.
            A continuación tienes datos extraídos del PENTUR/PERTUR oficial del gobierno para la región {region.capitalize()}.
            Tu tarea es leer estos datos macro y extraer inteligencia puramente B2B (oportunidades de negocio, riesgos, plan del gobierno y datos macro) usando estrictamente el esquema JSON proporcionado.
            
            Si el texto no contiene datos relevantes para alguna lista, deja el array vacío.
            
            DATOS CRUDOS DEL GOBIERNO:
            {texto_crudo}
            """
            
            print(f"    -> Conectando con Gemini 2.5 Flash para extraer Insights...")
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                    response_schema=StrategicInsightSchema
                )
            )
            
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(response.text)
                
            print(f"    [+] Intelligence Report guardado: {output_file}")
            
        except Exception as e:
            print(f"    [-] Error procesando {region}: {e}")
            
        time.sleep(3) # Anti-spam

    print("==================================================")
    print(" ✅ NORMALIZACIÓN B2B COMPLETADA.")
    print("==================================================")

if __name__ == "__main__":
    main()
