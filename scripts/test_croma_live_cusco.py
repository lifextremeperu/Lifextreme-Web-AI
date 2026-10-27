"""
LIFEXTREME & CROMA: PRUEBA EN VIVO DE INTELIGENCIA GUBERNAMENTAL (SUNAT PERÚ)
Consulta registros oficiales en vivo de SUNAT con la API Key activa de Croma.
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

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass

API_KEY = os.getenv("CROMA_API_KEY", "croma_live_NPNKH7BCQQZF5AQT9ZS4B5WJ0N385T91")
BASE_URL = "https://api.croma.run"


def consultar_sunat_croma(ruc: str = "20100070970"):
    print("=" * 75)
    print("🏛️  LIFEXTREME + CROMA: VERIFICACIÓN OFICIAL SUNAT EN TIEMPO REAL")
    print(f"    Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}")
    print(f"    API Server:   {BASE_URL}/pe/sunat/ruc/v1")
    print(f"    API Key:      {API_KEY[:14]}...{API_KEY[-4:]} (Autenticado)")
    print("=" * 75)

    print(f"\n📡 Consultando a SUNAT vía Croma para el RUC: {ruc}...")

    url = f"{BASE_URL}/pe/sunat/ruc/v1"
    payload = json.dumps({"ruc": ruc}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "LifextremeAI/2.0 (Cusco Operator Due Diligence)"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=35) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("data", {}).get("found"):
                info = data["data"]
                print("\n✅ [RESPUESTA 200 OK RECIBIDA DESDE SUNAT]:")
                print("-" * 75)
                print(f"  🏢 Razón Social:      {info.get('name')}")
                print(f"  🏷️  Nombre Comercial:  {info.get('trade_name') or 'N/A'}")
                print(f"  🆔 RUC Oficial:       {info.get('ruc')}")
                print(f"  🏛️  Tipo de Entidad:   {info.get('type')}")
                print(f"  🟢 Estado Tributario: {info.get('status')}")
                print(f"  ✅ Condición Fiscal:  {info.get('condition')}")
                print(f"  📍 Domicilio Fiscal:  {info.get('fiscal_address')}")
                print(f"  💼 Sistema Emisión:   {info.get('emission_system')}")
                print(f"  📅 Inicio de Activ.:  {info.get('activities_start_date')}")
                print("-" * 75)

                es_apto = info.get("status") == "ACTIVO" and info.get("condition") == "HABIDO"
                print(f"  🏆 EVALUACIÓN LIFEXTREME: {'🟢 PROVEEDOR VERIFICADO Y APTO' if es_apto else '🔴 OBSERVADO'}")
                print("-" * 75)
                return True
            else:
                print("⚠️  Entidad no encontrada en SUNAT:", data)
                return False
    except Exception as e:
        print(f"❌ Error en consulta: {e}")
        return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ruc", type=str, default="20100070970", help="RUC a auditar")
    args = parser.parse_args()
    consultar_sunat_croma(args.ruc)
