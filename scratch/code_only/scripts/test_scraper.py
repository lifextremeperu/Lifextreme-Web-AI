import requests
import json
import time

url = "http://localhost:8000/api/v1/b2b/query"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer DEV_SECRET_LIFEXTREME_2026"
}
payload = {
    "message": "quiero saber como subir mis ventas esta es mi web : https://lunallenatravel.com/"
}

print("Iniciando prueba interna del Cerebro B2B (Web Scraper)...")
print(f"Pregunta enviada: '{payload['message']}'\n")
print("Esperando razonamiento de Qwen2.5 y extracción de BeautifulSoup... (Esto tomará entre 30 y 60 segundos)\n")

start_time = time.time()

try:
    response = requests.post(url, json=payload, headers=headers, timeout=300)
    
    elapsed = time.time() - start_time
    print(f"--- TIEMPO DE RESPUESTA: {elapsed:.2f} segundos ---\n")
    
    if response.status_code == 200:
        data = response.json()
        with open("test_output.md", "w", encoding="utf-8") as f:
            f.write("💡 CONSEJO ESTRATÉGICO (Phi-3):\n")
            f.write("--------------------------------------------------\n")
            f.write(data.get("mensaje_principal", "Sin mensaje") + "\n")
            f.write("--------------------------------------------------\n")
            f.write("\n🔍 FUENTES UTILIZADAS:\n")
            for fuente in data.get("fuentes_utilizadas", []):
                f.write(f"- {fuente}\n")
        print("¡Respuesta recibida! Revisa el archivo 'test_output.md'.")
    else:
        print(f"Error HTTP {response.status_code}: {response.text}")
except Exception as e:
    print(f"Error en la conexión: {e}")
