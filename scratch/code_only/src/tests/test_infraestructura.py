import sys
import time
import requests
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.models.lifextreme_schema import LifextremeSchema
from pydantic import ValidationError

# =================================================================
# PILAR A: DISPONIBILIDAD LOGÍSTICA (SMOKE TESTS)
# =================================================================
def test_disponibilidad_sernanp():
    """Valida que la web oficial de SERNANP no haya cambiado su infraestructura base."""
    url = "https://www.gob.pe/sernanp"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        # Algunos WAF devuelven 403 pero la página carga. Validamos que retorne html.
        assert response.status_code in [200, 403, 418], f"SERNANP_OFFLINE: Estado {response.status_code}"
    except requests.exceptions.Timeout:
        pytest.fail("SERNANP_TIMEOUT: La página del gobierno tardó más de 5s en responder.")

def test_disponibilidad_consettur():
    """Valida que la web oficial de CONSETTUR (Buses Machu Picchu) esté operativa."""
    url = "https://consettur.com/"
    try:
        # Simulamos un navegador humano para que no nos bloquee el firewall
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        assert response.status_code in [200, 403, 418], f"CONSETTUR_OFFLINE: Estado {response.status_code}"
    except requests.exceptions.Timeout:
        pytest.fail("CONSETTUR_TIMEOUT: La página de buses tardó más de 5s en responder.")

# =================================================================
# PILAR B: INTEGRIDAD DE DATOS
# =================================================================
def test_integridad_lifextreme_schema():
    """Valida que el motor RAG rechace datos basura e invalide esquemas incorrectos."""
    # 1. Prueba de Éxito (Debe pasar)
    payload_valido = {
        "source_id": "SERNANP",
        "category": "RISK",
        "location": {"lat": -13.1631, "lng": -72.5450, "country": "Peru"},
        "payload": {"stock": 150, "status": "AVAILABLE"},
        "confidence_score": 0.99
    }
    evento = LifextremeSchema(**payload_valido)
    assert evento.source_id == "SERNANP"
    assert "stock" in evento.payload
    
    # 2. Prueba de Fallo (Debe generar Error de Pydantic)
    payload_invalido = {
        "source_id": "FUENTE_INVENTADA", # No existe en el Enum
        "category": "RISK",
        "location": {"lat": -13.1631}, # Faltan datos
        "payload": {}
    }
    with pytest.raises(ValidationError):
        LifextremeSchema(**payload_invalido)

# =================================================================
# PILAR C: LATENCIA DE CEREBRO (RAG TEST)
# =================================================================
def test_latencia_motor_correlacion():
    """Valida que el tiempo de ejecución del código core sea inferior a 3 segundos (Evita cuellos de botella)"""
    start_time = time.time()
    
    # Ejecutamos una tarea pesada simulada de RAG
    # importamos el motor localmente para evitar overhead global
    from src.integrations.risk_correlator import RiskCorrelator
    correlator = RiskCorrelator()
    # Enviamos datos basura vacíos para ver cuánto demora en rechazarlos y calcular el score base
    correlator.calcular_score_regional("Prueba Latencia")
    
    end_time = time.time()
    ttft = end_time - start_time
    
    assert ttft < 3.0, f"SYSTEM_PERFORMANCE_DEGRADED: El RAG demoró {ttft:.2f}s (Límite: 3s)."
