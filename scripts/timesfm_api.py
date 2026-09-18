import os
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import torch
import timesfm

# Configurar el cache en el disco D para que los archivos pesados NO se guarden en C:
os.environ["HF_HOME"] = r"D:\HuggingFaceCache"

# =====================================================================
# SOLUCION PARA EL ERROR DE PAGINACION DE WINDOWS (OS Error 1455)
# Desactivamos el uso de la tarjeta grafica (CUDA) temporalmente.
# Al usar solo la CPU, Windows no intenta hacer un "memory mapping" 
# tan agresivo entre la RAM y la VRAM, lo que suele evitar que pida 
# tanta memoria virtual al disco C:
# =====================================================================
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = FastAPI(title="Lifextreme TimesFM API", description="Microservicio de Prediccion B2B/B2C")

print("Inicializando arquitectura TimesFM 2.5 (Modo CPU puro)...")
try:
    # Usamos map_location='cpu' forzando a cargar los pesos solo en RAM (no VRAM)
    tfm = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
        "google/timesfm-2.5-200m-pytorch",
        torch_compile=False
    )
    
    tfm.compile(
        timesfm.ForecastConfig(
            max_context=1024,
            max_horizon=256,
            normalize_inputs=True,
            use_continuous_quantile_head=True,
        )
    )
    print("TimesFM 2.5 cargado exitosamente usando solo CPU/RAM.")
except Exception as e:
    print(f"Error critico al cargar TimesFM: {e}")
    raise e

class ForecastRequest(BaseModel):
    history: List[float]
    horizon: int = 10

@app.post("/forecast")
def forecast(request: ForecastRequest):
    if len(request.history) < 16:
        print("Advertencia: Para mejores predicciones, envia al menos 16 puntos historicos.")
    
    inputs = [np.array(request.history)]
    
    try:
        point_forecast, _ = tfm.forecast(
            horizon=request.horizon,
            inputs=inputs
        )
        forecast_result = point_forecast[0].tolist()
        return {"status": "success", "forecast": forecast_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la prediccion: {str(e)}")

if __name__ == "__main__":
    print("Iniciando servidor en puerto 8080...")
    uvicorn.run(app, host="0.0.0.0", port=8080)
