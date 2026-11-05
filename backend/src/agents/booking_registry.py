import os
import re
import json
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from pydantic import BaseModel

LEDGER_PATH = Path(__file__).resolve().parents[3] / "data" / "bookings_ledger.json"
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://zobpkmiqrvhbepqnjshr.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "sb_publishable_pBMaD6Mm-6Pi5cwwp3UUsw_Pndjw-mo")


class BookingRecord(BaseModel):
    booking_code: str
    passenger_name: str
    email: str = "contacto@lifextreme.store"
    phone: str = "+51 958 050 928"
    tour_name: str
    tour_date: str
    pax_count: int = 1
    total_amount_pen: float = 0.0
    paid_amount_pen: float = 0.0
    payment_plan: str = "split_30_30_40"
    lifecycle_stage: str = "RESERVA_CONFIRMADA_PRE_VIAJE"  # VISITANTE | RESERVA_CONFIRMADA_PRE_VIAJE | EN_RUTA | FINALIZADO_POST_VIAJE
    medical_cleared: bool = False
    duffle_verified: bool = False
    feedback_completed: bool = False
    created_at: str = ""


class BookingRegistry:
    """
     fuente de verdad (Single Source of Truth) para que MAX y los 5 Agentes sepan:
    1. Si quien escribe es un VISITANTE curioso o un CLIENTE CON RESERVA CONFIRMADA.
    2. En qué etapa exacta está su viaje (PRE_VIAJE, EN_RUTA o POST_VIAJE).
    3. Qué agentes tienen permiso de activarse para ese pasajero.
    """

    def __init__(self):
        self._ensure_ledger()

    def _ensure_ledger(self):
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not LEDGER_PATH.exists():
            # Semilla inicial con reserva de demostración verificable
            seed = {
                "LX-DEMO99": {
                    "booking_code": "LX-DEMO99",
                    "passenger_name": "Dra. Elena Vance",
                    "email": "elena.vance@miamihealth.org",
                    "phone": "+13055550199",
                    "tour_name": "Salkantay Trek & Glamping 5D",
                    "tour_date": "2026-11-20",
                    "pax_count": 2,
                    "total_amount_pen": 3700.0,
                    "paid_amount_pen": 1110.0,
                    "payment_plan": "split_30_30_40",
                    "lifecycle_stage": "RESERVA_CONFIRMADA_PRE_VIAJE",
                    "medical_cleared": False,
                    "duffle_verified": False,
                    "feedback_completed": False,
                    "created_at": datetime.now().isoformat()
                }
            }
            LEDGER_PATH.write_text(json.dumps(seed, indent=2, ensure_ascii=False), encoding="utf-8")

    def _load(self) -> Dict[str, dict]:
        try:
            return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save(self, data: Dict[str, dict]):
        LEDGER_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def register_booking(self, req: BookingRecord) -> dict:
        data = self._load()
        code = req.booking_code.strip().upper()
        record = req.model_dump()
        record["booking_code"] = code
        if not record.get("created_at"):
            record["created_at"] = datetime.now().isoformat()
        data[code] = record
        self._save(data)
        self._notify_telegram(record)
        return record

    def _notify_telegram(self, record: dict):
        try:
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "8795186534:AAFv8qT_yW-n2L_9rB0A2m_6zH5j8K9v0L1").strip()
            # Leer de .env si no está en os.environ
            env_path = Path(__file__).resolve().parents[3] / ".env"
            if env_path.exists():
                for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                    if line.startswith("TELEGRAM_BOT_TOKEN="):
                        bot_token = line.split("=", 1)[1].strip().strip('"').strip("'")
            chat_id = "2094843795"
            msg = (
                f"🎉 *NUEVA RESERVA CONFIRMADA EN LIFEXTREME WEB*\n\n"
                f"🔖 *Código:* `{record.get('booking_code')}`\n"
                f"👤 *Pasajero:* {record.get('passenger_name')}\n"
                f"🏔️ *Expedición:* {record.get('tour_name')}\n"
                f"📅 *Fecha:* {record.get('tour_date')}\n"
                f"👥 *Participantes:* {record.get('pax_count')} Pax\n"
                f"💳 *Abonado hoy:* S/ {record.get('paid_amount_pen')} (Total S/ {record.get('total_amount_pen')})\n\n"
                f"✅ *Agente 1 (Médico & Aclimatación)* y *Agente 2 (Duffle Bag 7 kg)* activados automáticamente para este pasajero."
            )
            payload = json.dumps({
                "chat_id": chat_id,
                "text": msg,
                "parse_mode": "Markdown"
            }).encode("utf-8")
            req_tg = urllib.request.Request(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            urllib.request.urlopen(req_tg, timeout=5)
        except Exception:
            pass

    def find_booking(
        self,
        booking_code: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        text_message: Optional[str] = None
    ) -> Optional[dict]:
        """
        Busca la reserva por:
        1) Código explícito enviado por el navegador (localStorage -> profile.booking_code)
        2) Código escrito en el mensaje del chat (ej. 'Mi reserva es LX-8A92B1')
        3) Teléfono o correo electrónico del pasajero.
        """
        data = self._load()

        # 1. Extraer código LX-XXXXXX si viene dentro del texto del chat
        if not booking_code and text_message:
            match = re.search(r"\b(LX-[A-Z0-9]{4,10})\b", text_message.upper())
            if match:
                booking_code = match.group(1)

        if booking_code:
            code = booking_code.strip().upper()
            if code in data:
                return data[code]

        if email:
            clean_email = email.strip().lower()
            for rec in data.values():
                if rec.get("email", "").lower() == clean_email:
                    return rec

        if phone:
            clean_phone = re.sub(r"\D", "", phone)
            if len(clean_phone) >= 7:
                for rec in data.values():
                    rec_phone = re.sub(r"\D", "", rec.get("phone", ""))
                    if clean_phone in rec_phone or rec_phone in clean_phone:
                        return rec

        return None

    def update_stage(
        self,
        booking_code: str,
        new_stage: str,
        medical_cleared: Optional[bool] = None,
        duffle_verified: Optional[bool] = None,
        feedback_completed: Optional[bool] = None
    ) -> Optional[dict]:
        data = self._load()
        code = booking_code.strip().upper()
        if code not in data:
            return None
        data[code]["lifecycle_stage"] = new_stage
        if medical_cleared is not None:
            data[code]["medical_cleared"] = medical_cleared
        if duffle_verified is not None:
            data[code]["duffle_verified"] = duffle_verified
        if feedback_completed is not None:
            data[code]["feedback_completed"] = feedback_completed
        self._save(data)
        return data[code]
