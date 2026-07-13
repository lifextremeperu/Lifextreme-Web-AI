import requests
import json
import time

print("Esperando a que el servidor MAX inicie...")
time.sleep(5)

url = "http://127.0.0.1:8000/chat"
payload = {
    "message": "Hola MAX, ¿qué incluye exactamente el tour de la Montaña de Colores y es seguro ir en época de lluvias?"
}

print(f"Enviando consulta de prueba a {url}...")
try:
    response = requests.post(url, json=payload, timeout=90)
    print("=======================================")
    print("RESPUESTA DE MAX (Recibida con exito)")
    print("=======================================")
    data = response.json()
    print(f"Mensaje: {data.get('mensaje_principal')}")
    print(f"Fuentes: {data.get('fuentes_utilizadas')}")
    print("=======================================")
    print("Revisa tu panel en cloud.langfuse.com. El rastreo ya debe estar ahi!")
except Exception as e:
    print(f"[-] Error: {e}")
