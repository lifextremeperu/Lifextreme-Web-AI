import os
import json
import time
import requests

# Configuración del LLM Local (Ollama)
# Puedes cambiar "deepseek-v2:lite" por "llama3:8b", "phi3" o el modelo que tengas corriendo en Ollama
MODEL_NAME = "deepseek-v2:lite" 
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Prompt de Mapeo
prompt_mapeo = """
Actúa como un Agente de Investigación Turística y Experto en Deportes de Aventura en Perú.
Tu misión es aplicar la directiva "Open Discovery" para identificar, registrar y clasificar la infraestructura física dedicada al turismo de aventura en el departamento de {departamento}.

Busca en tu conocimiento sobre:
- Palestras (indoor/outdoor), vías ferratas.
- Parques de cuerdas altas, Canopy/Zipline, Skybikes, plataformas de Bungee Jumping, puentes colgantes extremos.
- Bike parks, skateparks, circuitos de motocross/ATV, sandboard parks.
- Wakeparks, canales de canotaje.

Genera una lista de EXACTAMENTE 3 instalaciones o infraestructuras reales y operativas en {departamento}.
Debes devolver ÚNICAMENTE un array JSON con los siguientes campos para cada instalación:
"nombre_oficial", "tipo_categoria" (ej. Skybike, Palestra), "descripcion_corta", "ubicacion" (objeto con "distrito", "direccion_exacta"), "operador_responsable", "estado_actual".

No incluyas texto fuera del JSON. Si no conoces 3 exactas, inventa aproximaciones realistas para la prueba.
"""

def ejecutar_mapeo(departamento):
    print("==================================================")
    print(f"INICIANDO AGENTE DISCOVERY - DEPARTAMENTO: {departamento.upper()}")
    print(f"Utilizando LLM Local: {MODEL_NAME} vía Ollama")
    print("==================================================")
    
    ruta_output_dir = "data/knowledge/infraestructura"
    os.makedirs(ruta_output_dir, exist_ok=True)
    
    texto_enviado = prompt_mapeo.format(departamento=departamento)
    
    try:
        print(f"[>] Investigando infraestructura en {departamento}...")
        
        payload = {
            "model": MODEL_NAME,
            "prompt": texto_enviado,
            "stream": False,
            "format": "json"
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=240)
        
        if response.status_code == 200:
            respuesta_json = response.json()
            texto_json = respuesta_json.get("response", "").strip()
            
            # Limpiar posible bloque <think>
            if "</think>" in texto_json:
                texto_json = texto_json.split("</think>")[-1].strip()
                
            texto_json = texto_json.replace('```json', '').replace('```', '').strip()
            
            try:
                datos_json = json.loads(texto_json)
                archivo_salida = os.path.join(ruta_output_dir, f"{departamento.lower().replace(' ', '_')}.json")
                with open(archivo_salida, "w", encoding="utf-8") as f:
                    json.dump(datos_json, f, ensure_ascii=False, indent=4)
                    
                print(f"    [+] Guardado exitosamente en: {archivo_salida} ({len(datos_json)} registros encontrados)")
            except json.JSONDecodeError:
                print(f"    [-] Error: El modelo no devolvió un JSON válido. Respuesta bruta:\n{texto_json[:200]}...")
        else:
            print(f"    [-] Error de conexión con Ollama. Código HTTP: {response.status_code}. Mensaje: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("    [-] ERROR: No se pudo conectar a Ollama. Asegúrate de que Ollama esté ejecutándose (localhost:11434).")
    except Exception as e:
        print(f"    [-] Error procesando el departamento {departamento}: {e}")

if __name__ == "__main__":
    # Empezamos con 3 departamentos principales para validar el pipeline
    departamentos = ["Cusco", "Lima", "Arequipa"] 
    for dep in departamentos:
        ejecutar_mapeo(dep)
        print("    [!] Pausa de seguridad (3s)...")
        time.sleep(3)
    print("\n==================================================")
    print("PROCESO DE DESCUBRIMIENTO COMPLETADO (FASE 1)")
