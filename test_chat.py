import requests
import json
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_chatbot():
    # URL local directa para la prueba interna
    url = "http://localhost:8000/webhook/lifextreme"
    
    payload = {
        "message": "Hola MAX, quiero hacer parapente en el Valle Sagrado, ¿qué me recomiendas y cuánto cuesta aprox?",
        "history": []
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    print("==============================================")
    print("🤖 PRUEBA INTERNA DE CHATBOT MAX (OLLAMA)")
    print("==============================================")
    print(f"Enviando mensaje: '{payload['message']}'")
    print("Esperando respuesta de Ollama... (Esto puede tardar unos segundos dependiento de la GPU)")
    
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, headers=headers)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ ¡RESPUESTA RECIBIDA EXITOSAMENTE!")
            print(f"⏱️ Tiempo de respuesta: {elapsed:.2f} segundos\n")
            
            # FastAPI Endpoint might return `mensaje` or `mensaje_principal`
            mensaje = data.get("mensaje") or data.get("mensaje_principal") or str(data)
            print("💬 Respuesta de MAX:")
            print("-" * 50)
            print(mensaje)
            print("-" * 50)
            
            if "datos_cotizacion" in data:
                print("\n📊 Datos Estructurados de Cotización detectados:")
                print(json.dumps(data["datos_cotizacion"], indent=2, ensure_ascii=False))
                
        else:
            print(f"\n❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_chatbot()
