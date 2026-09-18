import requests
import numpy as np

# Datos simulados de ventas diarias de tours (ej: "Montana de Colores") en los ultimos 45 dias
mock_historical_sales = [
    12.0, 14.0, 15.0, 13.0, 19.0, 25.0, 28.0,  # Semana 1 (Sube en fines de semana)
    11.0, 13.0, 14.0, 12.0, 20.0, 26.0, 30.0,  # Semana 2
    10.0, 15.0, 16.0, 14.0, 22.0, 28.0, 35.0,  # Semana 3
    14.0, 16.0, 17.0, 15.0, 25.0, 30.0, 40.0,  # Semana 4 (Crecimiento de temporada)
    18.0, 20.0, 22.0, 19.0, 30.0, 35.0, 45.0,  # Semana 5
    25.0, 28.0, 30.0, 25.0, 40.0, 50.0, 60.0,  # Semana 6 (Pico de temporada)
    30.0, 32.0, 35.0                           # Ultimos 3 dias
]

API_URL = "http://localhost:8080/forecast"

def calculate_dynamic_pricing(base_price: float, forecast_demand: list) -> float:
    avg_demand = sum(forecast_demand) / len(forecast_demand)
    
    if avg_demand >= 45:
        multiplier = 1.30 # +30% Surge Pricing (Demanda Extrema)
    elif avg_demand >= 30:
        multiplier = 1.15 # +15% Peak Pricing (Alta Demanda)
    elif avg_demand < 15:
        multiplier = 0.90 # -10% Discount (Baja Demanda)
    else:
        multiplier = 1.0  # Normal
        
    return base_price * multiplier

def test_timesfm_prediction():
    print("Iniciando prueba de prediccion B2B con TimesFM (Mock Data)...")
    
    payload = {
        "history": mock_historical_sales,
        "horizon": 7 # Predecir la proxima semana (7 dias)
    }
    
    try:
        print(f"Conectando a {API_URL}...")
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        
        forecast = data["forecast"]
        print(f"\nDemanda historica (Ultimos 7 dias): {mock_historical_sales[-7:]}")
        print(f"Prediccion TimesFM (Proximos 7 dias): {[round(x, 1) for x in forecast]}")
        
        avg_future = sum(forecast) / len(forecast)
        print(f"Promedio Predicho: {avg_future:.1f} reservas por dia.")
        
        base_price_usd = 50.0
        new_price = calculate_dynamic_pricing(base_price_usd, forecast)
        
        print("\nRESULTADOS DEL DYNAMIC PRICING:")
        print(f"Precio Base Original: ${base_price_usd:.2f}")
        print(f"Precio Sugerido (Basado en Prediccion de TimesFM): ${new_price:.2f}")
        
        if new_price > base_price_usd:
            print("Insight B2B: Se recomienda subir el precio. La IA proyecta una fuerte tendencia al alza.")
        elif new_price < base_price_usd:
            print("Insight B2B: Se recomienda lanzar una promocion flash. La IA proyecta baja demanda.")
        
    except Exception as e:
        print(f"Error al conectar con TimesFM API. El servidor no esta respondiendo. Error: {e}")

if __name__ == "__main__":
    test_timesfm_prediction()
