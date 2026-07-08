import pytest

# Aquí se configurarán las fixtures globales para las pruebas sintéticas
# (Ej. tokens de prueba, configuraciones de navegador, etc.)

@pytest.fixture
def base_headers():
    return {
        "User-Agent": "Lifextreme-Synthetic-Auditor/1.0",
        "Accept": "application/json"
    }
