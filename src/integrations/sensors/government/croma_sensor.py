"""
LIFEXTREME GOVERNMENT INTELLIGENCE SENSOR: Croma Official Registry API
Conecta Lifextreme con fuentes oficiales del Estado Peruano (SUNAT, SUTRAN, APESEG, SUNARP).
Permite verificación KYC en tiempo real de agencias, guías y transporte turístico en Cusco.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 console output on Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass


class CromaGovernmentSensor:
    """Sensor de auditoría legal y fiscal conectado a la API de Croma"""

    BASE_URL = "https://api.croma.run"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("CROMA_API_KEY", "")
        if not self.api_key:
            print("⚠️  [CromaSensor]: CROMA_API_KEY no configurado en .env.")

    def _post(self, path: str, payload: dict, timeout: int = 25) -> dict:
        if not self.api_key:
            return {"error": "API Key de Croma no configurada"}

        url = f"{self.BASE_URL}{path}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Lifextreme-AI/2.0 (Cusco Adventure Systems)"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            return {"error": f"HTTP {e.code}", "detail": err_body}
        except Exception as e:
            return {"error": str(e)}

    def consultar_ruc(self, ruc: str) -> dict:
        """Consulta RUC oficial en SUNAT (estado, condición, domicilio y razón social)"""
        clean_ruc = "".join(filter(str.isdigit, str(ruc)))
        res = self._post("/pe/sunat/ruc/v1", {"ruc": clean_ruc})
        data = res.get("data", {})
        
        is_valido = data.get("status") == "ACTIVO" and data.get("condition") == "HABIDO"
        return {
            "ruc": clean_ruc,
            "razon_social": data.get("name") or data.get("trade_name"),
            "nombre_comercial": data.get("trade_name"),
            "tipo_empresa": data.get("type"),
            "estado": data.get("status", "NO_ENCONTRADO"),
            "condicion": data.get("condition", "NO_HABIDO"),
            "direccion_fiscal": data.get("fiscal_address"),
            "actividad_economica": data.get("main_economic_activity"),
            "es_valido_para_operar": is_valido,
            "timestamp": datetime.now().isoformat(),
            "raw": data
        }

    def consultar_soat_vehiculo(self, placa: str) -> dict:
        """Verifica vigencia del SOAT obligatorio en APESEG por placa vehicular"""
        clean_placa = "".join(filter(str.isalnum, str(placa))).upper()
        res = self._post("/pe/apeseg/soat/v1", {"plate": clean_placa})
        data = res.get("data", {})
        return {
            "placa": clean_placa,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

    def consultar_infracciones_sutran(self, placa: str) -> dict:
        """Audita el récord de papeletas en SUTRAN para vehículos de turismo"""
        clean_placa = "".join(filter(str.isalnum, str(placa))).upper()
        res = self._post("/pe/sutran/infracciones/v1", {"plate": clean_placa})
        data = res.get("data", {})
        return {
            "placa": clean_placa,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

    def auditoria_completa_operador(self, ruc_o_dni: str, placa: str = None) -> dict:
        """Genera un reporte de Due Diligence gubernamental 100% automático"""
        doc = "".join(filter(str.isdigit, str(ruc_o_dni)))
        reporte = {
            "identificador": doc,
            "fecha_auditoria": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sunat": None,
            "transporte_soat": None,
            "certificacion_lifextreme": "PENDIENTE"
        }

        if len(doc) == 11:
            reporte["sunat"] = self.consultar_ruc(doc)
            if reporte["sunat"].get("es_valido_para_operar"):
                reporte["certificacion_lifextreme"] = "VERIFICADO_SUNAT_ACTIVO"
            else:
                reporte["certificacion_lifextreme"] = "OBSERVADO_IRREGULAR"
        
        if placa:
            reporte["transporte_soat"] = self.consultar_soat_vehiculo(placa)

        return reporte


if __name__ == "__main__":
    sensor = CromaGovernmentSensor()
    print("\n🔍 PROBANDO SENSOR CROMA (SUNAT PERÚ)...")
    resultado = sensor.consultar_ruc("20100070970")
    print("\nResultado SUNAT:")
    print(f"  Razón Social: {resultado.get('razon_social')}")
    print(f"  Estado: {resultado.get('estado')} | Condición: {resultado.get('condicion')}")
    print(f"  ¿Válido para operar?: {'🟢 SÍ' if resultado.get('es_valido_para_operar') else '🔴 NO'}")
    print(f"  Dirección: {resultado.get('direccion_fiscal')}")
