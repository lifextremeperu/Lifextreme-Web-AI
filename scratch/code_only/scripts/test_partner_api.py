import requests
import json

def test_lifextreme_api():
    # URL de la API B2B de Lifextreme (Ajustar IP si está desplegado, ej. http://tuservidor.com/...)
    API_URL = "http://localhost:8000/api/v1/b2b/query"
    
    # Tu clave de acceso (API Key) proporcionada por Lifextreme
    API_KEY = "LIFEXTREME-TEST-KEY-2026"
    
    # Lo que quieres consultar al Cerebro de Lifextreme (GraphRAG)
    consulta = "¿Cómo afecta el bloqueo en Puno a mi logística de transporte hacia Cusco?"
    
    print("==================================================")
    print(" L I F E X T R E M E - C O R E   A P I   T E S T")
    print("==================================================")
    print(f"-> Conectando a: {API_URL}")
    print(f"-> Autenticando con API Key: {API_KEY[:10]}...")
    print(f"-> Enviando consulta: '{consulta}'\n")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    payload = {
        "message": consulta
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("=== RESPUESTA (Inteligencia de Negocios) ===")
            print(data.get("mensaje_principal"))
            print("\n--- Fuentes Utilizadas (GraphRAG) ---")
            for fuente in data.get("fuentes_utilizadas", []):
                print(f"- {fuente}")
            print(f"\n[Nivel de Confianza: {data.get('nivel_confianza')*100}%]")
        elif response.status_code == 403:
            print("[ERROR 403] Acceso Denegado. La API Key proporcionada es incorrecta.")
        else:
            print(f"[ERROR {response.status_code}] Ocurrió un problema en el servidor.")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] No se pudo conectar al servidor. Asegúrate de que FastAPI esté corriendo en el puerto 8000.")

if __name__ == "__main__":
    test_lifextreme_api()
