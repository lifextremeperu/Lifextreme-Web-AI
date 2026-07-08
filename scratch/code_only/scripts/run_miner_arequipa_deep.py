import os
import re
import time
import json
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig

# 1. Cargar el entorno y forzar Vertex AI
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[-] ERROR: No se encontró una GEMINI_API_KEY en el .env.")
    exit(1)

os.environ['GOOGLE_CLOUD_PROJECT'] = 'lifextreme-arequipa-agent'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

# 2. Configurar el cliente nativo
client = genai.Client(http_options=HttpOptions(api_version='v1'))

# 3. Lista de los 10 Enfoques
ENFOQUES = [
    "1_Precios_Presupuestos_Moneda",
    "2_Logistica_Transporte_Como_Llegar",
    "3_Seguridad_Riesgos_Salud",
    "4_Clima_Temporadas_Horarios",
    "5_Historia_Cultura_Curiosidades",
    "6_Tips_Locales_Secretos",
    "7_Gastronomia_Alimentos_Supervivencia",
    "8_Accesibilidad_Infraestructura",
    "9_Reglas_Prohibiciones_Tramites",
    "10_Alternativas_Plan_B"
]

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

def generar_prompt_enfoque(modulo_texto, nombre_angulo):
    return f"""
===============================================================
SISTEMA / ROL: AGENTE MINERO PROFUNDO (FASE 3)
===============================================================
Actúa como un Analista de Inteligencia Turística y Guía Oficial Senior hiper-especializado en Arequipa.

Tu objetivo es extraer exactamente 10 Preguntas y Respuestas (FQSAs) sobre el siguiente destino turístico, PERO ÚNICAMENTE ENFOCADAS EN EL ÁNGULO: "{nombre_angulo}".

DESTINO Y CONTEXTO:
{modulo_texto}

INSTRUCCIONES SEO Y KEYWORDS (¡MUY IMPORTANTE!):
- Las preguntas deben reflejar EXACTAMENTE cómo un turista las buscaría en Google.
- Usa lenguaje de búsqueda natural, con palabras clave de cola larga (long-tail keywords). Incluye siempre el nombre del destino y "Arequipa".
- Ejemplos de preguntas EXCELENTES: "¿Cuánto cuesta la entrada al Monasterio de Santa Catalina en Arequipa el 2026?", "¿Es peligroso subir al Volcán Misti sin guía oficial?", "¿Cómo llegar a la Laguna de Salinas desde el centro de Arequipa en transporte público?".
- Ejemplos de preguntas PÉSIMAS (Robóticas): "¿Cuál es el precio?", "¿Es seguro el lugar?", "¿Cómo llego al destino?".

INSTRUCCIONES CRÍTICAS DE CALIDAD:
1. Genera EXACTAMENTE 10 FQSAs (Preguntas y Respuestas) exclusivas sobre el enfoque "{nombre_angulo}".
2. NO des respuestas genéricas. Incluye precios reales, nombres de calles, empresas de transporte, meses exactos, o reglas específicas. Si el destino es remoto, explica la cruda realidad logística.

REGLA TÉCNICA OBLIGATORIA PARA EL FORMATO JSON:
- NO uses saltos de línea ni retornos de carro dentro de los textos. Escribe cada respuesta como un solo bloque de texto continuo.
- PROHIBIDO USAR COMILLAS DOBLES (") dentro del texto de la pregunta o de la respuesta. Si necesitas enfatizar o citar, usa exclusivamente comillas simples ('). El incumplimiento de esto romperá la base de datos.
- Formato de salida: Devuelve ÚNICAMENTE un array JSON válido con objetos que tengan "pregunta" y "respuesta". No uses markdown extra fuera del JSON.

Ejemplo del array JSON esperado:
[
  {{
    "pregunta": "¿Cuánto cuesta la miniván desde Arequipa hasta Chivay?",
    "respuesta": "El pasaje cuesta alrededor de 20 a 25 Soles y las minivanes salen desde el Terminal Terrestre de Arequipa cada 30 minutos."
  }}
]
"""

def ejecutar_mineria_profunda():
    print("==================================================")
    print("INICIANDO MINERÍA PROFUNDA (FASE 3) - 10 ÁNGULOS")
    print("==================================================")
    
    ruta_input = "data/knowledge/arequipa/modulos_cartografo.txt"
    ruta_output_dir = "data/knowledge/arequipa/fqsas_deep"
    os.makedirs(ruta_output_dir, exist_ok=True)
    
    try:
        with open(ruta_input, "r", encoding="utf-8") as f:
            texto_maestro = f.read()
    except Exception as e:
        print(f"[-] Error leyendo el archivo maestro: {e}")
        return

    modulos = extraer_modulos(texto_maestro)
    print(f"[+] Se detectaron {len(modulos)} módulos para minar profundamente.")
    
    for i, modulo in enumerate(modulos):
        id_match = re.search(r'ID:\s*([A-Z0-9\-]+)', modulo)
        modulo_id = id_match.group(1) if id_match else f"MODULO-{i+1}"
        
        # Saltamos si ya existe (para poder reanudar si se corta la conexión)
        archivo_salida = os.path.join(ruta_output_dir, f"{modulo_id}.json")
        if os.path.exists(archivo_salida):
            print(f"[>] Módulo {modulo_id} ({i+1}/{len(modulos)}) ya existe. Saltando...")
            continue
            
        print(f"\n[>] Minando Módulo {i+1}/{len(modulos)}: {modulo_id} (10 Ángulos)")
        
        datos_modulo = {
            "destino_id": modulo_id,
            "modulo_contexto": modulo[:150].replace('\n', ' ') + "...", 
            "fqsas": {}
        }
        
        exito_modulo = True
        
        # Bucle de los 10 ángulos
        for idx, angulo in enumerate(ENFOQUES):
            print(f"    -> Extrayendo Ángulo {idx+1}/10: {angulo}...", end=" ", flush=True)
            
            prompt = generar_prompt_enfoque(modulo, angulo)
            
            try:
                respuesta = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=GenerateContentConfig(
                        temperature=0.3, 
                        max_output_tokens=4096,
                        response_mime_type="application/json"
                    )
                )
                
                texto_json = respuesta.text.strip()
                if texto_json.startswith("```json"):
                    texto_json = texto_json[7:]
                if texto_json.endswith("```"):
                    texto_json = texto_json[:-3]
                    
                preguntas_array = json.loads(texto_json)
                
                datos_modulo["fqsas"][angulo] = preguntas_array
                print(f"[OK] ({len(preguntas_array)} FQSAs)")
                
            except Exception as e:
                print(f"[ERROR] {e}")
                datos_modulo["fqsas"][angulo] = [{"pregunta": "ERROR", "respuesta": str(e)}]
                exito_modulo = False
                
            # Pausa obligatoria para no saturar Vertex AI
            time.sleep(2.5)
            
        # Guardar el JSON maestro del módulo
        if exito_modulo:
            with open(archivo_salida, "w", encoding="utf-8") as f:
                json.dump(datos_modulo, f, ensure_ascii=False, indent=4)
            print(f"    [+] Guardado perfecto: {archivo_salida} (100 FQSAs integradas)")
        else:
            print(f"    [!] Se guardará con errores parciales para revisión manual.")
            with open(archivo_salida, "w", encoding="utf-8") as f:
                json.dump(datos_modulo, f, ensure_ascii=False, indent=4)

    print("\n==================================================")
    print("MINERÍA PROFUNDA COMPLETADA")

if __name__ == "__main__":
    ejecutar_mineria_profunda()
