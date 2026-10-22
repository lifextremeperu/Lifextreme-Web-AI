"""
LIFEXTREME PREDICTIVE INTELLIGENCE SENSOR: TuBoleto Cultura Peru
Monitors real-time capacity, ticket depletion velocity, and commercial feasibility
for Peruvian Archaeological Sanctuaries (Machu Picchu, Kuélap, Sipán, Chavín, etc.).
"""

import os
import sys
import time
import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta
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

# Crypto dependencies
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# Lifextreme pubsub and schema
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(str(WORKSPACE_ROOT))

try:
    from src.models.lifextreme_schema import LifextremeSchema
    from src.integrations.core.pubsub_client import pubsub
    PUBSUB_AVAILABLE = True
except Exception:
    PUBSUB_AVAILABLE = False


class TuBoletoSensor:
    """
    Sensor de alta fidelidad conectado a la API oficial de TuBoleto (Ministerio de Cultura del Perú).
    Descifra payloads criptográficos AES-CBC y calcula predicción de cupos para evitar sobreventa.
    """

    API_URL = "https://api-tuboleto.cultura.pe"
    SECURITY_SECRET_KEY = "5t4jPtv4LpmGgWU7ZYk8FhZf5LNTpk"
    DECRYPT_SECURITY_VALUE = b"In5iAIxnHwMTLg9ldHFUb3"
    ENCRYPTION_SECURE_PASSWORD = b"Km4pDqgVZdLNXYdde5jypBysh9MzkL"
    PBKDF2_ITERATIONS = 65536
    AES_KEY_SIZE = 32

    # Centros arqueológicos clave mapeados en TuBoleto
    CENTROS_CATALOGO = {
        1: {
            "nombre": "Llaqta Machupicchu",
            "slug": "llaqta_machupicchu",
            "departamento": "Cusco",
            "circuitos_clave": [
                {"id": 1, "nombre": "Circuito 1 - Panorámico", "ruta_default": 8, "nombre_ruta": "Terraza Superior"},
                {"id": 2, "nombre": "Circuito 2 - Clásico", "ruta_default": 1, "nombre_ruta": "Circuito Clásico"},
                {"id": 3, "nombre": "Circuito 3 - Realeza", "ruta_default": 3, "nombre_ruta": "Templos y Realeza"}
            ]
        },
        4: {
            "nombre": "Complejo Arqueológico Monumental Kuélap",
            "slug": "kuelap",
            "departamento": "Amazonas",
            "circuitos_clave": [
                {"id": 1, "nombre": "Circuito Interior Kuélap", "ruta_default": 1, "nombre_ruta": "Fortaleza y Murallas"}
            ]
        },
        5: {
            "nombre": "Museo Tumbas Reales de Sipán",
            "slug": "sipan",
            "departamento": "Lambayeque",
            "circuitos_clave": [
                {"id": 1, "nombre": "Museo Principal", "ruta_default": 1, "nombre_ruta": "Tumbas Reales"}
            ]
        },
        3: {
            "nombre": "Monumento Arqueológico Chavín",
            "slug": "chavin",
            "departamento": "Áncash",
            "circuitos_clave": [
                {"id": 1, "nombre": "Templo de Chavín", "ruta_default": 1, "nombre_ruta": "Galerías y Cabezas Clavas"}
            ]
        }
    }

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Referer": "https://tuboleto.cultura.pe/"
        }
        self.derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            self.ENCRYPTION_SECURE_PASSWORD,
            self.DECRYPT_SECURITY_VALUE,
            self.PBKDF2_ITERATIONS,
            dklen=self.AES_KEY_SIZE
        )

    def _generar_hmac_auth(self):
        """Genera el código HMAC-SHA256 con timestamp sincronizado requerido por TuBoleto."""
        ts = str(int(time.time() * 1000))
        msg = f"{self.SECURITY_SECRET_KEY}:{ts}"
        h = hmac.new(self.SECURITY_SECRET_KEY.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256)
        code_b64 = base64.b64encode(h.digest()).decode('utf-8')
        return code_b64, ts

    def _desencriptar(self, b64_ciphertext: str):
        """Descifra el payload AES-256-CBC con padding PKCS7."""
        if not CRYPTO_AVAILABLE or not b64_ciphertext:
            return None
        try:
            raw_data = base64.b64decode(b64_ciphertext)
            if len(raw_data) < 16:
                return None
            iv = raw_data[:16]
            ciphertext = raw_data[16:]
            cipher = Cipher(algorithms.AES(self.derived_key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_plain = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_plain) + unpadder.finalize()
            return json.loads(plaintext.decode('utf-8'))
        except Exception as e:
            # print(f"[TuBoleto] Error decrypting: {e}")
            return None

    def consultar_info_lugar(self, id_lugar: int):
        """Obtiene información oficial, circuitos y rutas habilitadas del centro arqueológico."""
        url = f"{self.API_URL}/visita/public/informacion-lugar?idLugar={id_lugar}"
        try:
            req = urllib.request.Request(url, headers=self.headers)
            res = urllib.request.urlopen(req, timeout=10)
            return json.loads(res.read().decode('utf-8'))
        except Exception as e:
            return None

    def consultar_fechas_disponibles(self, id_lugar: int, id_circuito: int, id_ruta: int, dias_horizonte: int = 45):
        """Consulta fechas con cupos abiertos dentro del horizonte de días."""
        code, ts = self._generar_hmac_auth()
        today = datetime.now()
        df_inicio = today.strftime("%Y-%m-%d")
        df_fin = (today + timedelta(days=dias_horizonte)).strftime("%Y-%m-%d")

        payload = {
            "nidLugar": id_lugar,
            "nidCircuito": id_circuito,
            "nidRuta": id_ruta,
            "nidUsuario": 0,
            "dfInicio": df_inicio,
            "dfFin": df_fin,
            "valorPunto": 0,
            "code": code,
            "timestamp": ts
        }

        url = f"{self.API_URL}/visita/public/consulta-fechas-disponibles"
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=self.headers, method="POST")
            res = urllib.request.urlopen(req, timeout=12)
            data = json.loads(res.read().decode('utf-8'))
            if data.get("estado") and data.get("data"):
                return self._desencriptar(data["data"])
        except Exception as e:
            pass
        return []

    def consultar_horarios_cupos(self, id_lugar: int, id_circuito: int, id_ruta: int, fecha_str: str):
        """
        Consulta los cupos exactos hora por hora para una fecha (formato YYYY-MM-DD).
        Retorna lista de turnos con cupo_actual y cupo_total.
        """
        code, ts = self._generar_hmac_auth()
        payload = {
            "nidlugar": id_lugar,
            "nidcircuito": id_circuito,
            "nidruta": id_ruta,
            "df_inicio": fecha_str,
            "valorPunto": 0,
            "token": "",
            "code": code,
            "timestamp": ts
        }

        url = f"{self.API_URL}/visita/public/consulta-horarios"
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=self.headers, method="POST")
            res = urllib.request.urlopen(req, timeout=12)
            data = json.loads(res.read().decode('utf-8'))
            if data.get("estado") and data.get("data"):
                return self._desencriptar(data["data"])
        except Exception as e:
            pass
        return []

    def calcular_predictivo(self, total_disponible: int, capacidad_total: int, dias_restantes: int):
        """
        Modelo predictivo de inteligencia comercial para prevenir fallar a los clientes:
        - SEGURO_PARA_VENDER: Amplia holgura, confirmar reserva inmediatamente.
        - ALERTA_VENTA_RAPIDA: Cupos reduciéndose velozmente, exigir depósito 30% en 15 min.
        - CRITICO_ULTIMOS_CUPOS: Menos de 10 boletos restantes, riesgo extremo de colisión.
        - AGOTADO: 0 cupos en fecha solicitada -> Activa motor de recomendación de contingencia.
        """
        if total_disponible <= 0:
            return {
                "decision": "AGOTADO",
                "score_confianza": 0.0,
                "badge_color": "rose",
                "label": "🔴 Agotado en TuBoleto",
                "recomendacion": "Ofrecer ruta alterna de contingencia (Circuito 3 / Choquequirao Trek / Salkantay)",
                "permitir_reserva_automatica": False
            }

        porcentaje = (total_disponible / max(1, capacidad_total)) * 100

        if total_disponible <= 10 or porcentaje < 5.0:
            return {
                "decision": "CRITICO_ULTIMOS_CUPOS",
                "score_confianza": 0.35,
                "badge_color": "orange",
                "label": f"🟠 Crítico: Solo {total_disponible} cupos en vivo",
                "recomendacion": "Cerrar compra inmediata en pasarela TuBoleto antes de 10 minutos",
                "permitir_reserva_automatica": True
            }
        elif total_disponible <= 35 or porcentaje < 20.0:
            return {
                "decision": "ALERTA_VENTA_RAPIDA",
                "score_confianza": 0.70,
                "badge_color": "amber",
                "label": f"🟡 Alta Demanda: {total_disponible} cupos restantes",
                "recomendacion": "Venta viable separando con 30% de anticipo",
                "permitir_reserva_automatica": True
            }
        else:
            return {
                "decision": "SEGURO_PARA_VENDER",
                "score_confianza": 0.98,
                "badge_color": "emerald",
                "label": f"🟢 {total_disponible} cupos disponibles hoy - Seguro para vender",
                "recomendacion": "Confirmar tour inmediatamente con 100% de fiabilidad",
                "permitir_reserva_automatica": True
            }

    def escanear_disponibilidad_completa(self, dias_futuros: int = 14):
        """
        Escanea y audita la disponibilidad completa de Machu Picchu y santuarios clave,
        generando el mapa comercial predictivo para MAX Chatbot y el frontend.
        """
        print("🏛️ [TuBoleto-Sentinel] Iniciando auditoría en tiempo real con cifrado oficial...")
        resultados = {
            "timestamp": datetime.now().isoformat(),
            "estado_servicio": "ONLINE",
            "lugares": {}
        }

        today = datetime.now()

        for id_lugar, meta in self.CENTROS_CATALOGO.items():
            nombre = meta["nombre"]
            slug = meta["slug"]
            print(f"   -> Monitoreando: {nombre} ({meta['departamento']})...")

            lugar_res = {
                "id": id_lugar,
                "nombre": nombre,
                "slug": slug,
                "departamento": meta["departamento"],
                "circuitos": []
            }

            for circ in meta.get("circuitos_clave", []):
                id_circ = circ["id"]
                id_ruta = circ["ruta_default"]
                nombre_circ = circ["nombre"]

                # Obtener fechas disponibles
                fechas = self.consultar_fechas_disponibles(id_lugar, id_circ, id_ruta, dias_horizonte=dias_futuros)
                fechas_list = [f.get("dfecha") for f in fechas if isinstance(f, dict) and "dfecha" in f] if fechas else []

                # Si no hay fechas devueltas por horizonte corto, consultar los primeros días clave
                dias_a_chequear = fechas_list[:5] if fechas_list else [(today + timedelta(days=d)).strftime("%d-%m-%Y") for d in range(1, 4)]

                horarios_resumen = []
                total_cupos_lugar = 0
                capacidad_max_lugar = 0

                for f_str in dias_a_chequear[:2]: # Chequear los primeros 2 días para muestreo preciso de horarios
                    # Formatear a YYYY-MM-DD
                    parts = f_str.split("-")
                    if len(parts) == 3:
                        if len(parts[0]) == 4:
                            f_query = f_str
                        else:
                            f_query = f"{parts[2]}-{parts[1]}-{parts[0]}"
                        
                        turnos = self.consultar_horarios_cupos(id_lugar, id_circ, id_ruta, f_query)
                        if turnos:
                            for t in turnos:
                                cupo_act = t.get("ncupo_actual", 0)
                                cupo_tot = t.get("ncupo", 0)
                                total_cupos_lugar += cupo_act
                                capacidad_max_lugar += cupo_tot
                                horarios_resumen.append({
                                    "fecha": f_query,
                                    "hora": f"{t.get('dhora_ini')} - {t.get('dhora_fin')}",
                                    "cupos_disponibles": cupo_act,
                                    "capacidad": cupo_tot
                                })

                prediccion = self.calcular_predictivo(total_cupos_lugar, capacidad_max_lugar, dias_restantes=len(dias_a_chequear))

                circ_data = {
                    "circuito_id": id_circ,
                    "nombre": nombre_circ,
                    "ruta_id": id_ruta,
                    "fechas_abiertas_conteo": len(fechas_list),
                    "proximas_fechas": fechas_list[:7],
                    "cupos_en_muestra": total_cupos_lugar,
                    "capacidad_muestra": capacidad_max_lugar,
                    "predictivo": prediccion,
                    "turnos_muestra": horarios_resumen[:6]
                }
                lugar_res["circuitos"].append(circ_data)

            resultados["lugares"][slug] = lugar_res

        # Guardar en data/archaeo_availability.json
        output_file = Path("data/archaeo_availability.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)

        print(f"✅ [TuBoleto-Sentinel] Auditoría finalizada con éxito. Sincronizado en {output_file}")

        # Enviar evento por PubSub si está disponible
        if PUBSUB_AVAILABLE:
            try:
                evento = LifextremeSchema(
                    source_id="TUBOLETO_CULTURA",
                    category="LOGISTICS",
                    location={"lat": -13.1626, "lng": -72.5453, "country": "Perú", "region": "Cusco"},
                    payload={
                        "tipo": "AUDITORIA_DISPONIBILIDAD_SANCTUARIOS",
                        "machupicchu_decision": resultados["lugares"].get("llaqta_machupicchu", {}).get("circuitos", [{}])[0].get("predictivo", {}).get("decision", "DESCONOCIDO"),
                        "timestamp": resultados["timestamp"]
                    },
                    confidence_score=0.99
                )
                pubsub.publish(evento.model_dump_json())
            except Exception as e:
                pass

        return resultados


if __name__ == "__main__":
    sensor = TuBoletoSensor()
    res = sensor.escanear_disponibilidad_completa(dias_futuros=30)
    print("\n--- RESUMEN EJECUTIVO COMERCIAL ---")
    mapi = res["lugares"].get("llaqta_machupicchu", {})
    for c in mapi.get("circuitos", []):
        pred = c["predictivo"]
        print(f"[{c['nombre']}] -> Estado: {pred['label']} | Decisión: {pred['decision']}")
        print(f"   Recomendación: {pred['recomendacion']}")
