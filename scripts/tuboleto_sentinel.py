"""
LIFEXTREME SENTINEL & BUSINESS INTELLIGENCE AUTOMATION
Real-time synchronized monitoring for:
1. TuBoleto Cultura Peru (Machu Picchu, Kuélap, Sipán, Chavín)
2. Train Logistics (PeruRail & Inca Rail)
3. Combined Commercial Feasibility (Previene sobreventa y calcula alternativas)
"""

import sys
import os
import time
import json
import argparse
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

from src.integrations.sensors.culture.tuboleto_sensor import TuBoletoSensor
from src.integrations.sensors.transport.train_sensor import TrainSensor


def ejecutar_ciclo_sentinela():
    print("\n" + "=" * 70)
    print(f"🛰️  LIFEXTREME SENTINEL: AUDITORÍA EN TIEMPO REAL [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    print("=" * 70)

    # 1. Ejecutar TuBoleto Sensor
    tuboleto = TuBoletoSensor()
    res_cultura = tuboleto.escanear_disponibilidad_completa(dias_futuros=30)

    # 2. Ejecutar Train Sensor
    tren = TrainSensor()
    res_tren = tren.auditar_disponibilidad_trenes()

    # 3. Matriz de Viabilidad Comercial Cruzada
    mapi_circs = res_cultura.get("lugares", {}).get("llaqta_machupicchu", {}).get("circuitos", [])
    c1_pred = mapi_circs[0]["predictivo"] if len(mapi_circs) > 0 else {}
    c2_pred = mapi_circs[1]["predictivo"] if len(mapi_circs) > 1 else {}
    
    tren_viable = res_tren.get("viable_para_paquete", False)

    # Diagnóstico comercial
    puede_vender_c1 = (c1_pred.get("decision") in ["SEGURO_PARA_VENDER", "ALERTA_VENTA_RAPIDA"]) and tren_viable
    puede_vender_c2 = (c2_pred.get("decision") in ["SEGURO_PARA_VENDER", "ALERTA_VENTA_RAPIDA"]) and tren_viable

    matriz_comercial = {
        "timestamp": datetime.now().isoformat(),
        "machupicchu": {
            "circuito_1_panoramico": {
                "puede_vender": puede_vender_c1,
                "estado_ticket": c1_pred.get("label", "Desconocido"),
                "decision": c1_pred.get("decision", "DESCONOCIDO"),
                "asientos_tren": res_tren.get("total_asientos_ida", 0),
                "accion_comercial": "Venta 100% habilitada en MAX Chatbot y Web con depósito del 30%" if puede_vender_c1 else "Ofrecer Circuito Alterno o Trekking",
                "alternativa_sugerida": None if puede_vender_c1 else "Choquequirao Trek 4D / Salkantay Trek"
            },
            "circuito_2_clasico": {
                "puede_vender": puede_vender_c2,
                "estado_ticket": c2_pred.get("label", "Desconocido"),
                "decision": c2_pred.get("decision", "DESCONOCIDO"),
                "asientos_tren": res_tren.get("total_asientos_ida", 0),
                "accion_comercial": "Venta habilitada" if puede_vender_c2 else "Redirigir a Circuito 1 Panorámico o Circuito 3 Realeza",
                "alternativa_sugerida": "Circuito 1 Panorámico (Terraza Superior) - 285 cupos en vivo"
            }
        },
        "otros_centros": {
            "kuelap": res_cultura.get("lugares", {}).get("kuelap", {}).get("circuitos", [{}])[0].get("predictivo", {}),
            "sipan": res_cultura.get("lugares", {}).get("sipan", {}).get("circuitos", [{}])[0].get("predictivo", {}),
            "chavin": res_cultura.get("lugares", {}).get("chavin", {}).get("circuitos", [{}])[0].get("predictivo", {})
        },
        "logistica_tren": {
            "estado": res_tren.get("estado_general"),
            "asientos_ida": res_tren.get("total_asientos_ida"),
            "asientos_retorno": res_tren.get("total_asientos_retorno")
        }
    }

    # Guardar matriz consolidada
    consolidado_path = ROOT_DIR / "data" / "commercial_feasibility.json"
    consolidado_path.parent.mkdir(parents=True, exist_ok=True)
    with open(consolidado_path, "w", encoding="utf-8") as f:
        json.dump(matriz_comercial, f, indent=2, ensure_ascii=False)

    print("\n" + "-" * 70)
    print("📊 MATRIZ PREDICTIVA DE FEASIBILITY COMERCIAL:")
    print(f"   [Machu Picchu Circuito 1] => {'🟢 SEGURO VENDER' if puede_vender_c1 else '🔴 RIESGO/AGOTADO'}")
    print(f"      Acción: {matriz_comercial['machupicchu']['circuito_1_panoramico']['accion_comercial']}")
    print(f"   [Machu Picchu Circuito 2] => {'🟢 SEGURO VENDER' if puede_vender_c2 else '🔴 AGOTADO EN CULTURA'}")
    print(f"      Acción: {matriz_comercial['machupicchu']['circuito_2_clasico']['accion_comercial']}")
    print(f"      Alternativa automática: {matriz_comercial['machupicchu']['circuito_2_clasico']['alternativa_sugerida']}")
    print(f"   [Logística Tren] => {res_tren.get('label')}")
    print("-" * 70)
    print(f"💾 Base de conocimiento actualizada en {consolidado_path}")
    print("=" * 70 + "\n")

    return matriz_comercial


def main():
    parser = argparse.ArgumentParser(description="Lifextreme TuBoleto & Train Availability Sentinel")
    parser.add_argument("--daemon", action="store_true", help="Ejecutar en modo daemon continuo con intervalo")
    parser.add_argument("--interval", type=int, default=300, help="Intervalo en segundos para modo daemon (default 300s)")
    args = parser.parse_args()

    if args.daemon:
        print(f"🚀 Iniciando Lifextreme Sentinel en modo DAEMON (Intervalo: {args.interval}s)...")
        while True:
            try:
                ejecutar_ciclo_sentinela()
            except Exception as e:
                print(f"⚠️ Error en ciclo sentinela: {e}")
            time.sleep(args.interval)
    else:
        ejecutar_ciclo_sentinela()


if __name__ == "__main__":
    main()
