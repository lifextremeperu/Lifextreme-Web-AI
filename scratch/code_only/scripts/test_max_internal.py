import sys
import requests
import json
import time

def test_api():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass
    print("==================================================")
    print(" 🧠 CONSULTA INTERNA DIRECTA A LIFEXTREME-CORE (MAX)")
    print("==================================================")
    
    url = "http://localhost:8000/api/v1/b2b/query"
    
    query = "Saludos MAX. Soy un operador logístico B2B. Tengo una caravana de 15 turistas lista para salir en bus turístico desde Cusco hacia Puno en 4 horas. Cruza esta información con los sensores de carreteras y dime si hay alertas críticas de SUTRAN, conflictos sociales recientes y si me das luz verde o luz roja para esta operación nocturna."
    
    print(f"[>] PREGUNTA CRÍTICA ENVIADA:\n{query}\n")
    print("[+] Activando Sensores en tiempo real (SUTRAN, GDELT) y RAG Vectorial. Esto tomará unos segundos...")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "LIFEXTREME-TEST-KEY-2026"
    }
    
    payload = {"message": query}
    
    start = time.time()
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=120)
        end = time.time()
        
        if res.ok:
            data = res.json()
            print(f"\n[TIEMPO TOTAL DE PROCESAMIENTO]: {round(end-start, 2)} segundos")
            print("==================================================")
            print(" 🤖 RESPUESTA OFICIAL DEL ANALISTA (LIFEXTREME-CORE):")
            print("==================================================")
            print(data.get('mensaje_principal', 'Sin respuesta'))
            print("\n[FUENTES INTELIGENCIA VECTORIAL B2B]:")
            for f in data.get('fuentes_utilizadas', []):
                print(f" - {f}")
        else:
            print(f"[-] Error HTTP {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[-] Error de conexión local. Asegúrate de que api/main.py está corriendo: {e}")

if __name__ == '__main__':
    test_api()
