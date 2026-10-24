"""
LIFEXTREME WHATSAPP OPERATOR BRIDGE
Automatización de Notificaciones, Aceptaciones y Confirmaciones
entre Turistas de Lifextreme y Operadores/Guías de Aventura en Cusco.
"""

import os
import sys
import json
import uuid
import urllib.parse
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

BASE_URL = "https://www.lifextreme.store"
DB_FILE = ROOT_DIR / "data" / "adventure_bookings.json"


def cargar_reservas() -> list:
    if DB_FILE.exists():
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def guardar_reservas(reservas: list):
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(reservas, f, indent=2, ensure_ascii=False)


def crear_solicitud_reserva(
    cliente_nombre: str,
    cliente_telefono: str,
    cliente_hotel: str,
    tour_nombre: str,
    fecha_tour: str,
    pax: int,
    pago_operador_pen: float,
    operador_nombre: str,
    operador_telefono: str
) -> dict:
    """Registra una nueva reserva y genera los enlaces de 1 toque para el operador"""
    booking_id = f"LFX-{datetime.now().strftime('%m%d')}-{uuid.uuid4().hex[:4].upper()}"
    token_seguridad = uuid.uuid4().hex[:8]

    # Enlaces de 1 toque para el Operador
    op_encoded = urllib.parse.quote(operador_nombre)
    enlace_aceptar = f"{BASE_URL}/api/booking/operator-action?action=accept&id={booking_id}&token={token_seguridad}&op={op_encoded}"
    enlace_rechazar = f"{BASE_URL}/api/booking/operator-action?action=reject&id={booking_id}&token={token_seguridad}&op={op_encoded}"

    # 1. Mensaje formateado para el Operador en Cusco (vía WhatsApp)
    mensaje_operador = f"""🏔️ *¡NUEVA ASIGNACIÓN DE EXPEDICIÓN LIFEXTREME!*

Hola *{operador_nombre}*, tienes una nueva reserva confirmada para operar en Cusco:

📍 *Tour:* {tour_nombre}
📅 *Fecha:* {fecha_tour}
👥 *Pasajeros:* {pax} pax
🏨 *Hotel de Recojo:* {cliente_hotel}
💰 *Pago directo a ti:* *S/ {pago_operador_pen:,.2f} PEN*
🆔 *Código de Orden:* `{booking_id}`

⚡ *CONFIRMA TU DISPONIBILIDAD CON 1 SOLO TAP:*
👉 [🟢 ACEPTAR Y ASIGNAR A MI CUPO]({enlace_aceptar})
👉 [🔴 NO DISPONIBLE (RECHAZAR)]({enlace_rechazar})

_🛰️ Red de Operadores Certificados • Lifextreme Adventure AI_"""

    # 2. Mensaje formateado para el Turista / Usuario (vía WhatsApp)
    mensaje_turista = f"""🎉 *¡RESERVA CONFIRMADA EN LIFEXTREME!*

Hola *{cliente_nombre}*, tu expedición de aventura está en marcha:

📍 *Experiencia:* {tour_nombre}
📅 *Fecha:* {fecha_tour}
👥 *Grupo:* {pax} persona(s)
🏨 *Punto de Encuentro:* {cliente_hotel}
🛡️ *Guía Oficial Asignado:* {operador_nombre} (Certificado MINCETUR)
🆔 *Voucher:* `{booking_id}`

⏰ *Hora de recojo:* Te contactaremos por aquí a las 8:00 PM del día previo con los detalles del briefing y clima.

¿Tienes dudas de equipo o aclimatación? Escríbenos directamente respondiendo a este chat. 🏔️"""

    registro = {
        "booking_id": booking_id,
        "token": token_seguridad,
        "timestamp": datetime.now().isoformat(),
        "cliente": {
            "nombre": cliente_nombre,
            "telefono": cliente_telefono,
            "hotel": cliente_hotel
        },
        "tour": {
            "nombre": tour_nombre,
            "fecha": fecha_tour,
            "pax": pax,
            "pago_operador_pen": pago_operador_pen
        },
        "operador": {
            "nombre": operador_nombre,
            "telefono": operador_telefono
        },
        "links": {
            "aceptar": enlace_aceptar,
            "rechazar": enlace_rechazar
        },
        "mensajes": {
            "operador_wa": mensaje_operador,
            "turista_wa": mensaje_turista
        },
        "estado": "PENDIENTE_OPERADOR"
    }

    reservas = cargar_reservas()
    reservas.append(registro)
    guardar_reservas(reservas)

    return registro


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Lifextreme WhatsApp Operator Bridge")
    parser.add_argument("--demo", action="store_true", help="Simular una orden de prueba completa")
    args = parser.parse_args()

    if args.demo:
        print("\n" + "=" * 75)
        print("🚀 SIMULACIÓN DE RESERVA CRUZADA: TURISTA ↔ OPERADOR VIA WHATSAPP")
        print("=" * 75)

        orden = crear_solicitud_reserva(
            cliente_nombre="Sarah Jenkins (USA)",
            cliente_telefono="+14155552671",
            cliente_hotel="Kokopelli Hostel (Calle San Andrés)",
            tour_nombre="Salkantay Trek 4D / 3N con Domos",
            fecha_tour="28 de Octubre 2026",
            pax=2,
            pago_operador_pen=760.00,
            operador_nombre="Juan Carlos Quispe",
            operador_telefono="+51984123456"
        )

        print("\n📲 [1. MENSAJE ENVIADO AL WHATSAPP DEL OPERADOR/GUÍA]:")
        print("-" * 70)
        print(orden["mensajes"]["operador_wa"])
        print("-" * 70)

        print("\n📲 [2. MENSAJE AUTOMÁTICO ENVIADO AL TURISTA]:")
        print("-" * 70)
        print(orden["mensajes"]["turista_wa"])
        print("-" * 70)

        print(f"\n✅ Registro guardado en {DB_FILE}")
        print(f"👉 Link de prueba para el operador:")
        print(f"   {orden['links']['aceptar']}")
