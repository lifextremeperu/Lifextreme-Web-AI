import os
import re
import time
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Usamos el SDK Nativo de Google GenAI que soporta forzar el JSON a nivel de servidor
from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig

def extraer_modulos(texto):
    bloque_xml = re.search(r'<modulos_generados>(.*?)</modulos_generados>', texto, re.DOTALL)
    if not bloque_xml:
        partes = texto.split("---")
        modulos = []
        for p in partes:
            if "ID:" in p and "MÓDULO:" in p:
                modulos.append(p.strip())
        return modulos
    
    contenido = bloque_xml.group(1)
    modulos_crudos = contenido.split("---")
    modulos_limpios = []
    for mod in modulos_crudos:
        mod = mod.strip()
        if len(mod) > 10 and "ID:" in mod:
            modulos_limpios.append(mod)
    return modulos_limpios

def generar_prompt_enfoque(modulo_texto, nombre_angulo, departamento, pais):
    return f"""
===============================================================
SISTEMA / ROL: AGENTE MINERO PROFUNDO (FASE 3)
===============================================================
Actúa como un Analista de Inteligencia Turística y Guía Oficial Senior hiper-especializado en {departamento}, {pais}.

Tu objetivo es extraer exactamente 10 Preguntas y Respuestas (FQSAs) sobre el siguiente destino turístico, PERO ÚNICAMENTE ENFOCADAS EN EL ÁNGULO: "{nombre_angulo}".

DESTINO Y CONTEXTO:
{modulo_texto}

INSTRUCCIONES SEO Y KEYWORDS (¡MUY IMPORTANTE!):
- Las preguntas deben reflejar EXACTAMENTE cómo un turista las buscaría en Google.
- Usa lenguaje de búsqueda natural, con palabras clave de cola larga (long-tail keywords). Incluye siempre el nombre del destino y "{departamento}".
- Ejemplos de preguntas EXCELENTES: "¿Cuánto cuesta la entrada a X en {departamento} el 2026?", "¿Es peligroso subir a Y sin guía oficial?", "¿Cómo llegar a Z desde el centro de {departamento} en transporte público?".
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
    "pregunta": "¿Cuánto cuesta la miniván desde {departamento} hasta el destino?",
    "respuesta": "El pasaje cuesta alrededor de 20 a 25 Soles y las minivanes salen desde el Terminal Terrestre de {departamento} cada 30 minutos."
  }}
]
"""

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

def main():
    load_dotenv()
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="Ejecutar el Agente Minero (Fase 2)")
    parser.add_argument("departamento", help="Nombre del departamento a minar")
    parser.add_argument("--pais", default="Perú", help="País (por defecto: Perú)")
    parser.add_argument("--test", action="store_true", help="Solo minar el primer módulo como prueba")
    args = parser.parse_args()
    
    departamento = args.departamento.lower()
    pais = args.pais
    
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'lifextreme-arequipa-agent'
    os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
    
    print(f"==================================================")
    print(f"INICIANDO MINERÍA PROFUNDA PARA {departamento.upper()}")
    print(f"==================================================")
    
    ruta_input = f"data/knowledge/{departamento}/modulos_cartografo.txt"
    ruta_output_dir = f"data/knowledge/{departamento}/fqsas_deep"
    os.makedirs(ruta_output_dir, exist_ok=True)
    
    try:
        with open(ruta_input, "r", encoding="utf-8") as f:
            texto_maestro = f.read()
    except Exception as e:
        print(f"[-] Error leyendo el archivo maestro: {e}")
        return

    modulos = extraer_modulos(texto_maestro)
    print(f"[+] Se detectaron {len(modulos)} módulos en {departamento.capitalize()} para minar.")
    
    if args.test:
        print("[!] MODO TEST ACTIVADO: Solo se minará el primer módulo.")
        modulos = modulos[:1]

    print(f"[+] Conectando a Vertex AI (gemini-2.5-flash) usando Service Account NATIVA...")
    try:
        client = genai.Client(http_options=HttpOptions(api_version='v1'))
    except Exception as e:
        print(f"[-] Error fatal de conexión con Vertex AI Nativo: {e}")
        sys.exit(1)
        
    for i, modulo in enumerate(modulos):
        id_match = re.search(r'ID:\s*([A-Z0-9\-]+)', modulo)
        modulo_id = id_match.group(1) if id_match else f"MODULO-{i+1}"
        
        nombre_match = re.search(r'MÓDULO:\s*(.+)', modulo)
        modulo_nombre = nombre_match.group(1).strip() if nombre_match else "Desconocido"
        
        archivo_salida = os.path.join(ruta_output_dir, f"{modulo_id}.json")
        if os.path.exists(archivo_salida):
            print(f"[>] Módulo {modulo_id} ({i+1}/{len(modulos)}) ya existe. Saltando...")
            continue
            
        print(f"\n[>] Minando Módulo {i+1}/{len(modulos)}: {modulo_id} - {modulo_nombre}")
        
        datos_modulo = {
            "destino_id": modulo_id,
            "modulo_contexto": modulo_nombre,
            "fqsas": {}
        }
        
        exito_modulo = True
        
        for idx, angulo in enumerate(ENFOQUES):
            print(f"    -> Extrayendo Ángulo {idx+1}/10: {angulo}...", end=" ", flush=True)
            
            prompt = generar_prompt_enfoque(modulo, angulo, departamento.capitalize(), pais)
            
            try:
                respuesta = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=GenerateContentConfig(
                        temperature=0.3, 
                        max_output_tokens=8192,
                        response_mime_type="application/json"
                    )
                )
                
                texto_json = respuesta.text.strip()
                preguntas_array = json.loads(texto_json)
                
                datos_modulo["fqsas"][angulo] = preguntas_array
                print(f"[OK] ({len(preguntas_array)} FQSAs)")
                
            except Exception as e:
                print(f"[ERROR] JSON parse error evadido o fallido: {e}")
                datos_modulo["fqsas"][angulo] = [{"pregunta": "ERROR", "respuesta": str(e)}]
                exito_modulo = False
                
            time.sleep(3.5)
            
        if exito_modulo:
            with open(archivo_salida, "w", encoding="utf-8") as f:
                json.dump(datos_modulo, f, ensure_ascii=False, indent=4)
            print(f"    [+] Guardado perfecto: {archivo_salida}")
        else:
            print(f"    [!] Se guardará con errores parciales para revisión manual.")
            with open(archivo_salida, "w", encoding="utf-8") as f:
                json.dump(datos_modulo, f, ensure_ascii=False, indent=4)

    print("\n==================================================")
    print("MINERÍA PROFUNDA COMPLETADA")

if __name__ == "__main__":
    main()
