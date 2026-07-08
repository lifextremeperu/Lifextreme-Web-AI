import os
import re
import time
import json
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig

# 1. Cargar el entorno
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[-] ERROR: No se encontró una GEMINI_API_KEY en el .env.")
    exit(1)

# Variables necesarias para Vertex AI con la nueva llave
os.environ['GOOGLE_CLOUD_PROJECT'] = 'lifextreme-arequipa-agent'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

# 2. Configurar el cliente nativo
client = genai.Client(http_options=HttpOptions(api_version='v1'))

# 3. Prompt Minero (Fase 2)
prompt_minero = """
===============================================================
SISTEMA / ROL: AGENTE MINERO DE DATOS (FASE 2)
===============================================================
Actúa como un Analista de Inteligencia Turística y Guía Oficial Senior especializado en Arequipa.

Tu objetivo es expandir UN (1) Módulo Turístico específico en una lista de Preguntas Frecuentes (FQSA - Frequently Questioned Specific Answers) de alta densidad y valor.

===============================================================
CONTEXTO DEL MÓDULO A EXPANDIR:
{modulo_texto}
===============================================================

INSTRUCCIONES CRÍTICAS:
1. Genera exactamente 10 FQSAs (Preguntas y Respuestas) hiper-específicas basadas en este módulo. (Idealmente deberían ser 100, pero empezamos con 10 por módulo para validar la estructura).
2. NO des respuestas genéricas. Incluye nombres de calles, precios estimados (en Soles/USD), distancias en horas, rutas, riesgos reales, y nombres locales.
3. Formato de salida: Devuelve ÚNICAMENTE un JSON válido que contenga un array de objetos con "pregunta" y "respuesta". No uses markdown extra fuera del JSON.
"""

def extraer_modulos(texto):
    bloque_xml = re.search(r'<modulos_generados>(.*?)</modulos_generados>', texto, re.DOTALL)
    if not bloque_xml:
        return []
    contenido = bloque_xml.group(1)
    modulos_crudos = contenido.split("ID:")
    modulos_limpios = []
    for mod in modulos_crudos:
        mod = mod.strip()
        if len(mod) > 10:
            modulos_limpios.append("ID: " + mod)
    return modulos_limpios

def ejecutar_mineria():
    print("==================================================")
    print("INICIANDO AGENTE MINERO (FASE 2) - EXPANSIÓN FQSA")
    print("==================================================")
    
    ruta_input = "data/knowledge/arequipa/modulos_cartografo.txt"
    ruta_output_dir = "data/knowledge/arequipa/fqsas"
    os.makedirs(ruta_output_dir, exist_ok=True)
    
    try:
        with open(ruta_input, "r", encoding="utf-8") as f:
            texto_maestro = f.read()
    except Exception as e:
        print(f"[-] Error leyendo el archivo {ruta_input}: {e}")
        return

    modulos = extraer_modulos(texto_maestro)
    print(f"[+] Se encontraron {len(modulos)} módulos para minar.")
    if len(modulos) == 0:
        return

    for i, modulo in enumerate(modulos):
        print(f"\n[>] Minando Módulo {i+1}/{len(modulos)}...")
        id_match = re.search(r'ID:\s*([A-Z0-9\-]+)', modulo)
        modulo_id = id_match.group(1) if id_match else f"MODULO-{i+1}"
        print(f"    ID detectado: {modulo_id}")
        
        texto_enviado = prompt_minero.format(modulo_texto=modulo)
        
        try:
            respuesta = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=texto_enviado,
                config=GenerateContentConfig(temperature=0.3, max_output_tokens=8192)
            )
            
            texto_json = respuesta.text.replace('```json', '').replace('```', '').strip()
            datos_json = json.loads(texto_json)
            
            archivo_salida = os.path.join(ruta_output_dir, f"{modulo_id}.json")
            with open(archivo_salida, "w", encoding="utf-8") as f:
                json.dump(datos_json, f, ensure_ascii=False, indent=4)
                
            print(f"    [+] Guardado exitosamente en: {archivo_salida} ({len(datos_json)} preguntas)")
        except Exception as e:
            print(f"    [-] Error procesando el módulo {modulo_id}: {e}")
        
        if i < len(modulos) - 1:
            print("    [!] Pausa de seguridad (3s)...")
            time.sleep(3)

    print("\n==================================================")
    print("PROCESO COMPLETADO")

if __name__ == "__main__":
    ejecutar_mineria()
