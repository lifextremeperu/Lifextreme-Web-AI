"""
LIFEXTREME SENTINEL VIP: DEMONIO SENSOR 24/7 (CONTINUOUS RADAR WORKER)
Monitorea la plataforma oficial TuBoleto (Ministerio de Cultura del Perú).
Detecta boletos liberados por cancelaciones en tiempo real y dispara alertas
instantáneas al canal privado de Telegram de agencias y guías VIP.
"""

import os
import sys
import time
import json
import argparse
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

# Ensure UTF-8 console output on Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass

from src.integrations.sensors.culture.tuboleto_sensor import TuBoletoSensor

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL_VIP = os.getenv("TELEGRAM_CHANNEL_VIP_ID") or os.getenv("TELEGRAM_CHAT_ID")


def enviar_alerta_telegram(circuito: str, fecha: str, cupos_liberados: int, total_actual: int = None, canal_id: str = None) -> bool:
    """Dispara mensaje de alerta urgente de alta prioridad al canal VIP"""
    target_chat = canal_id or CANAL_VIP
    if not BOT_TOKEN or not target_chat:
        print(f"⚠️  [Alerta Omitida]: TELEGRAM_BOT_TOKEN o CANAL_VIP no configurado.")
        return False

    hora_actual = datetime.now().strftime("%I:%M:%S %p")
    total_str = f" (Total disponible ahora: {total_actual})" if total_actual is not None else ""

    mensaje = f"""🚨 <b>¡ALERTA URGENTE: CUPOS LIBERADOS EN MACHU PICCHU!</b>

📍 <b>Circuito:</b> <code>{circuito}</code>
📅 <b>Fecha:</b> <b>{fecha}</b>
🎫 <b>Boletos detectados en vivo:</b> <b>+{cupos_liberados} cupos</b>{total_str}
⚡ <b>Estado:</b> Disponibles para compra inmediata en TuBoleto
🕒 <b>Hora detección:</b> {hora_actual}

👉 <a href="https://tuboleto.cultura.pe/"><b>COMPRAR DIRECTO EN TUBOLETO AHORA ➔</b></a>

<i>🛰️ Sentinel Lifextreme IA • Sensor Criptográfico 24/7</i>"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": target_chat,
        "text": mensaje,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            res_data = json.loads(resp.read().decode('utf-8'))
            if res_data.get("ok"):
                print(f"🔔 [ALERTA TELEGRAM DISPARADA]: {circuito} | {fecha} | +{cupos_liberados} cupos")
                return True
            else:
                print(f"❌ Error en respuesta Telegram: {res_data}")
                return False
    except Exception as e:
        print(f"⚠️  Excepción al enviar alerta a Telegram: {e}")
        return False


def ejecutar_demonio_sentinel(intervalo_segundos: int = 60, dias_escanear: int = 30, test_mode: bool = False):
    """Bucle continuo de vigilancia 24/7"""
    print("\n" + "=" * 75)
    print(f"🛰️  LIFEXTREME SENTINEL VIP: DEMONIO SENSOR EN VIVO")
    print(f"    Canal Destino: {CANAL_VIP}")
    print(f"    Intervalo de barrido: {intervalo_segundos}s | Días futuros: {dias_escanear}")
    print("=" * 75)

    if test_mode:
        print("\n🧪 [MODO SIMULACIÓN / TEST ACTIVADO]")
        print("Disparando alerta de prueba inmediata para validar recepción y sonido...")
        fecha_test = (datetime.now() + sys.modules['datetime'].timedelta(days=7)).strftime("%Y-%m-%d")
        ok = enviar_alerta_telegram(
            circuito="Circuito 2 - Clásico (Ruta Tradicional)",
            fecha=fecha_test,
            cupos_liberados=4,
            total_actual=4
        )
        if ok:
            print("✅ Prueba de alerta Telegram completada con éxito.")
        else:
            print("❌ La prueba falló. Revisa token y permisos del canal.")
        return

    sensor = TuBoletoSensor()
    estado_memoria = {} # Memoria volátil: key="fecha_circuito" -> value=cupos
    ciclo = 0

    while True:
        ciclo += 1
        hora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{hora_str}] [Ciclo #{ciclo}] Escaneando disponibilidad en TuBoleto...")

        try:
            # 1. Obtener escaneo criptográfico de TuBoleto
            data = sensor.escanear_disponibilidad_completa(dias_futuros=dias_escanear)
            lugares = data.get("lugares", {})
            mapi = lugares.get("llaqta_machupicchu", {})
            circuitos = mapi.get("circuitos", [])

            # Si el sensor retorna estructura por fechas o por circuitos:
            for circ in circuitos:
                nombre_c = circ.get("nombre", "Machu Picchu")
                predictivo = circ.get("predictivo", {})
                cupos_ahora = predictivo.get("cupos_hoy", 0)
                clave = f"HOY_{nombre_c}"

                cupos_antes = estado_memoria.get(clave, None)

                # Si no es la primera vuelta y los cupos aumentaron:
                if cupos_antes is not None and cupos_ahora > cupos_antes:
                    delta = cupos_ahora - cupos_antes
                    print(f"\n🚨 [¡BOLETOS LIBERADOS DETECTADOS!]: {nombre_c} (+{delta} cupos)")
                    enviar_alerta_telegram(
                        circuito=nombre_c,
                        fecha=datetime.now().strftime("%Y-%m-%d"),
                        cupos_liberados=delta,
                        total_actual=cupos_ahora
                    )

                estado_memoria[clave] = cupos_ahora

            print(f"    ✔ Barrido completado. Próximo escaneo en {intervalo_segundos}s.")

        except Exception as e:
            print(f"⚠️  [Error Ciclo #{ciclo}]: {e}")
            time.sleep(5)

        time.sleep(intervalo_segundos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lifextreme TuBoleto Sentinel Alert Daemon")
    parser.add_argument("--test", action="store_true", help="Enviar alerta de prueba simulada a Telegram")
    parser.add_argument("--interval", type=int, default=60, help="Segundos entre cada barrido (default: 60)")
    parser.add_argument("--days", type=int, default=30, help="Días futuros a auditar (default: 30)")
    parser.add_argument("--channel", type=str, help="Canal de Telegram a sobreescribir")
    args = parser.parse_args()

    if args.channel:
        CANAL_VIP = args.channel

    ejecutar_demonio_sentinel(
        intervalo_segundos=args.interval,
        dias_escanear=args.days,
        test_mode=args.test
    )
