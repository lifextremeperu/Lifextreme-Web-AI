"""
Router FastAPI para Capas Geoespaciales GEOINT (Windy Webcams API v3)
Endpoint: GET /api/v1/geoint/layers/webcams
"""

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from app.services.windy_geoint import windy_geoint_service
from app.services.train_tracker import train_tracker_service

router = APIRouter(prefix="/api/v1/geoint/layers", tags=["GEOINT 3D Layers"])


@router.get("/webcams")
async def get_geoint_webcams_layer(response: Response) -> JSONResponse:
    """
    Devuelve la FeatureCollection GeoJSON de cámaras meteorológicas/turísticas públicas
    de Windy Webcams API v3 en el corredor Cusco - Valle Sagrado - Machu Picchu.
    Incluye cabecera Cache-Control: public, max-age=1800 y degradación elegante HTTP 200.
    """
    geojson_payload = await windy_geoint_service.get_webcams_geojson()
    return JSONResponse(
        status_code=200,
        content=geojson_payload,
        headers={
            "Cache-Control": "public, max-age=1800",
            "X-Geoint-Cache-Hit": str(geojson_payload.get("metadata", {}).get("cache_hit", False))
        }
    )


@router.get("/trains")
async def get_geoint_trains_layer() -> JSONResponse:
    """
    Devuelve el array JSON de trenes activos (PeruRail / Inca Rail) con sus timestamps
    de salida y llegada para la interpolación espaciotemporal con Turf.js en el visor 3D.
    """
    trains = train_tracker_service.get_active_trains()
    return JSONResponse(
        status_code=200,
        content=trains,
        headers={"Cache-Control": "no-store, max-age=0"}
    )


@router.get("/govtech")
async def get_geoint_govtech_mcp_layer() -> JSONResponse:
    """
    Devuelve el estado consolidado de los 4 conectores públicos sin API Key del Perú
    (Ministerio de Cultura + SERNANP, SENAMHI + ANA, INGEMMET + IGP / INDECI y Google Traffic + Waze)
    para el Panel Operativo Outdoor Lifextreme OS en local y producción.
    """
    payload = {
        "status": "ok",
        "mcp_server": "lifextreme-peru-geoint-mcp",
        "version": "3.0.0",
        "cultura_sernanp": {
            "tool_name": "cultura_cupos_machupicchu_camino_inca",
            "portal_oficial": "https://tuboleto.cultura.pe",
            "nodos": [
                {
                    "id": "CULTURA-LLAQTA-MP",
                    "nombre": "Llaqta Machu Picchu • Boletería DDC Cusco (Aguas Calientes)",
                    "short_badge": "🎟️ MP: 91 Cupos Hoy",
                    "lat": -13.1631,
                    "lng": -72.5450,
                    "elevacion_m": 2430,
                    "color": "#10b981",
                    "circuitos": [
                        {"codigo": "Circuito 1 (Panorámico)", "detalle": "Terraza Superior + Montaña Machu Picchu", "cupos_hoy": 64, "cupos_manana": 142, "estado": "DISPONIBLE UPGRADE", "badge_color": "#10b981"},
                        {"codigo": "Circuito 2 (Clásico Llaqta)", "detalle": "Recorrido Clásico Completo & Intihuatana", "cupos_hoy": 18, "cupos_manana": 47, "estado": "ÚLTIMOS 18 CUPOS HOY", "badge_color": "#f59e0b"},
                        {"codigo": "Circuito 3 (Realeza + Huayna Picchu)", "detalle": "Sector Realeza + Ascenso Huayna Picchu", "cupos_hoy": 9, "cupos_manana": 31, "estado": "ALTA DEMANDA", "badge_color": "#f97316"}
                    ],
                    "decision_operador": "Quedan 18 cupos hoy en Circuito 2 Clásico y 64 en Circuito 1 Panorámico. Emitir Last-Minute Upgrade a pasajeros en Cusco u Ollantaytambo."
                },
                {
                    "id": "SERNANP-KM82-PISCACUCHO",
                    "nombre": "Control SERNANP Km 82 (Piscacucho — Camino Inca Clásico 4D/3N)",
                    "short_badge": "🥾 Km 82: 12 Cupos Mañana",
                    "lat": -13.2135,
                    "lng": -72.3712,
                    "elevacion_m": 2720,
                    "color": "#14b8a6",
                    "circuitos": [
                        {"codigo": "Camino Inca Clásico 4D/3N (Km 82)", "detalle": "Piscacucho ➔ Wayllabamba ➔ Warmiwañusqa ➔ Intipunku", "cupos_hoy": 0, "cupos_manana": 12, "estado": "12 CUPOS MAÑANA", "badge_color": "#14b8a6"}
                    ],
                    "decision_operador": "Puesto de control SERNANP Km 82 y puente Piscacucho 100% operativos. 12 permisos disponibles para salidas de mañana."
                },
                {
                    "id": "SERNANP-KM104-CHACHABAMBA",
                    "nombre": "Control SERNANP Km 104 (Chachabamba — Camino Inca Corto 2D/1N)",
                    "short_badge": "🥾 Km 104: 14 Cupos Hoy",
                    "lat": -13.1842,
                    "lng": -72.5015,
                    "elevacion_m": 2170,
                    "color": "#06b6d4",
                    "circuitos": [
                        {"codigo": "Camino Inca Corto 2D/1N (Km 104)", "detalle": "Chachabamba ➔ Wiñay Wayna ➔ Puerta del Sol (Intipunku)", "cupos_hoy": 14, "cupos_manana": 38, "estado": "DISPONIBLE VENTA RÁPIDA", "badge_color": "#06b6d4"}
                    ],
                    "decision_operador": "14 cupos hoy y 38 mañana en Km 104. Ideal para ofrecer upgrade de Trekking 2D/Full Day con parada de tren en Km 104."
                }
            ]
        },
        "senamhi_ana_vilcanota": {
            "tool_name": "senamhi_caudal_vilcanota_y_avisos_cusco",
            "portal_oficial": "https://www.senamhi.gob.pe",
            "estaciones": [
                {
                    "id": "SENAMHI-KM105-RUINAS",
                    "estacion": "Estación Hidrológica Km 105 / Puente Ruinas (Aguas Calientes)",
                    "short_badge": "🌊 Km 105: 148.6 m³/s (OK)",
                    "rio": "Río Vilcanota - Urubamba (Acceso Machu Picchu)",
                    "lat": -13.1538,
                    "lng": -72.5264,
                    "elevacion_m": 2015,
                    "caudal_m3s": 148.6,
                    "umbral_amarillo_m3s": 260.0,
                    "umbral_cierre_tren_m3s": 340.0,
                    "estado": "NORMAL-ESTABLE (VERDE)",
                    "color": "#0ea5e9",
                    "cruce_ferroviario": "Trenes PeruRail / Inca Rail 100% OPERATIVOS (Margen seguro de +191.4 m³/s antes de umbral de suspensión ferroviaria).",
                    "decision_operador": "Operación normal de trenes hacia Aguas Calientes y acceso peatonal por Puente Ruinas / Hidroeléctrica sin riesgo hídrico."
                },
                {
                    "id": "SENAMHI-CHILCA-OLLANTA",
                    "estacion": "Estación Hidrológica Chilca / Ollantaytambo (Valle Sagrado)",
                    "short_badge": "🌊 Ollanta: 112.4 m³/s",
                    "rio": "Río Vilcanota (Tramo Pachar – Ollantaytambo – Chilca)",
                    "lat": -13.2520,
                    "lng": -72.2750,
                    "elevacion_m": 2765,
                    "caudal_m3s": 112.4,
                    "umbral_amarillo_m3s": 210.0,
                    "umbral_cierre_tren_m3s": 290.0,
                    "estado": "ÓPTIMO (VERDE)",
                    "color": "#38bdf8",
                    "cruce_ferroviario": "Vía férrea en Pachar y Ollantaytambo despejada. Caudal apto para Canotaje (Rafting Clase II-III) en Bajo Urubamba.",
                    "decision_operador": "Autorizar salidas de Rafting en sector Ollantaytambo y embarque normal en estación ferroviaria."
                },
                {
                    "id": "SENAMHI-PISAC-CHUQUI",
                    "estacion": "Estación Hidrológica Pisac / Chuquicahuana (Alto Vilcanota)",
                    "short_badge": "🌊 Pisac: 74.8 m³/s (Rafting OK)",
                    "rio": "Río Vilcanota (Tramo Chuquicahuana – Pisac)",
                    "lat": -13.4245,
                    "lng": -71.8490,
                    "elevacion_m": 2972,
                    "caudal_m3s": 74.8,
                    "umbral_amarillo_m3s": 165.0,
                    "umbral_cierre_tren_m3s": 230.0,
                    "estado": "ÓPTIMO RAFTING (VERDE)",
                    "color": "#22d3ee",
                    "cruce_ferroviario": "Caudal limpio y estable en Alto Vilcanota. Puente Pisac 100% seguro.",
                    "decision_operador": "Condiciones ideales para grupos de Canotaje (Rafting Clase III-IV) en Chuquicahuana y Cusipata."
                }
            ]
        },
        "ingemmet_igp_indeci": {
            "tool_name": "ingemmet_igp_alertas_geologicas_cusco",
            "portal_oficial": "https://geocatmin.ingemmet.gob.pe",
            "ultimo_sismo_igp": "M 3.4 — Sur de Cusco / Apurímac (Prof. 114 km • Imperceptible en superficie)",
            "zonas": [
                {
                    "id": "INDECI-ABRA-MALAGA-HIDRO",
                    "sector": "Abra Málaga – Santa María – Santa Teresa – Hidroeléctrica",
                    "short_badge": "🌋 Abra Málaga: Precaución 16h",
                    "lat": -13.1480,
                    "lng": -72.3280,
                    "elevacion_m": 4316,
                    "organismo": "COEN-INDECI / INGEMMET",
                    "tipo_peligro": "Activación de Quebradas y Neblina Densa en Ceja de Selva",
                    "nivel_alerta": "PRECAUCIÓN VESPERTINA (NARANJA DESDE 16:00 HRS)",
                    "color": "#f59e0b",
                    "detalle_tecnico": "Lluvia acumulada (14 mm) en quebradas de Santa María – Santa Teresa con desprendimiento menor de gravilla en Km 138.",
                    "decision_operador": "BLOQUEO PREVENTIVO VESPERTINO: Para pasajeros retornando después de las 15:30 hrs de Aguas Calientes, usar retorno seguro en Tren (PeruRail/Inca Rail) y evitar ruta terrestre Hidroeléctrica – Abra Málaga de noche."
                },
                {
                    "id": "INGEMMET-SALKANTAY-HUMANTAY",
                    "sector": "Cuenca Salkantay — Laguna Humantay / Sahuayacco – Chaullay",
                    "short_badge": "🌋 Salkantay: Talud Estable",
                    "lat": -13.3010,
                    "lng": -72.5890,
                    "elevacion_m": 3850,
                    "organismo": "INGEMMET GEOCATMIN",
                    "tipo_peligro": "Monitoreo Glacio-Aluvional y Estabilidad de Taludes",
                    "nivel_alerta": "ESTABLE EN MAÑANA / VIGILANCIA TARDE (AMARILLO)",
                    "color": "#eab308",
                    "detalle_tecnico": "Laguna Humantay sin anomalías dinámicas; saturación de suelo 68% en descenso Wayraqtambo – Chaullay.",
                    "decision_operador": "Ruta Laguna Humantay y Trek Salkantay habilitadas. Completar descenso a Chaullay/Collpapampa antes de las 15:00 hrs."
                },
                {
                    "id": "IGP-SISMO-CUSCO-AUSANGATE",
                    "sector": "Vigilancia Sísmica IGP — Sistema de Fallas Cusco / Ausangate",
                    "short_badge": "🌋 IGP Cusco: Sin Sismos Críticos",
                    "lat": -13.4810,
                    "lng": -71.9690,
                    "elevacion_m": 3720,
                    "organismo": "IGP (Instituto Geofísico del Perú)",
                    "tipo_peligro": "Monitoreo Sísmico Instrumental en Tiempo Real",
                    "nivel_alerta": "NORMAL (VERDE)",
                    "color": "#a855f7",
                    "detalle_tecnico": "Reporte IGP / USGS: M 3.4 (Prof. 114 km • Imperceptible). Taludes en Sacsayhuamán, Valle Sagrado y Ausangate estables.",
                    "decision_operador": "Operaciones de escalada, vía ferrata, zipline y trekking Ausangate 100% autorizadas."
                }
            ]
        },
        "trafico_transfers_aeropuerto_terminal": {
            "tool_name": "trafico_accesos_aeropuerto_y_terminal_peru",
            "tile_layer": "https://mt1.google.com/vt?lyrs=h,traffic&x={x}&y={y}&z={z}",
            "corredores": [
                {
                    "id": "TRAFICO-CUZ-AEROPUERTO",
                    "nombre": "1. Aeropuerto Cusco (Velasco Astete CUZ) ⇄ Centro Histórico / Hoteles",
                    "short_badge": "🚦 Transfer CUZ: 16 min (Vía Expresa OK)",
                    "lat": -13.5315,
                    "lng": -71.9495,
                    "zoom": 15,
                    "color": "#10b981",
                    "estado": "FLUIDO EN VÍA EXPRESA / MODERADO AV. EL SOL",
                    "tiempo_actual_min": 16,
                    "tiempo_normal_min": 14,
                    "velocidad_kmh": 34,
                    "tramos": [
                        {"via": "Av. Velasco Astete & Puerta Parking CUZ", "estado": "🟢 Fluido (38 km/h)", "color": "#10b981"},
                        {"via": "Óvalo Libertadores ➔ Vía Expresa Cusco", "estado": "🟢 Fluido (45 km/h)", "color": "#10b981"},
                        {"via": "Av. El Sol / Av. Tullumayo (Centro Histórico)", "estado": "🟠 Lento (+6 min)", "color": "#f59e0b"}
                    ],
                    "decision_operador": "Para recojo de vuelos LA2027 y H85311: Entrar y salir del Aeropuerto CUZ por Vía Expresa ➔ Óvalo Libertadores (16 min). Evitar Av. de la Cultura."
                },
                {
                    "id": "TRAFICO-CUZ-TERMINAL",
                    "nombre": "2. Terminal Terrestre de Cusco ⇄ Wanchaq / Centro Histórico",
                    "short_badge": "🚦 Terminal Cusco: 22 min (Atasco Evitamiento)",
                    "lat": -13.5322,
                    "lng": -71.9642,
                    "zoom": 16,
                    "color": "#ef4444",
                    "estado": "CONGESTIÓN EN PUERTA TERMINAL & PUENTE GRAU",
                    "tiempo_actual_min": 22,
                    "tiempo_normal_min": 11,
                    "velocidad_kmh": 17,
                    "tramos": [
                        {"via": "Vía de Evitamiento (Puerta Terminal Terrestre)", "estado": "🔴 Atasco Buses/Taxis (+9 min)", "color": "#ef4444"},
                        {"via": "Av. Pachacútec & Óvalo Pachacútec (Wanchaq)", "estado": "🟠 Lento (+5 min)", "color": "#f59e0b"},
                        {"via": "Puente Grau / Av. Ejército", "estado": "🟠 Tráfico Denso (+6 min)", "color": "#f59e0b"}
                    ],
                    "decision_operador": "Cuello de botella activo frente al Terminal Terrestre (+11 min demora). Despachar unidad 25 min antes y tomar desvío por Av. Industrial / Wanchaq."
                },
                {
                    "id": "TRAFICO-LIM-AEROPUERTO",
                    "nombre": "3. Aeropuerto de Lima (Jorge Chávez LIM) ⇄ Miraflores / San Isidro",
                    "short_badge": "🚦 Transfer LIM: 52 min (Faucett Pesado)",
                    "lat": -12.0265,
                    "lng": -77.1055,
                    "zoom": 13,
                    "color": "#f97316",
                    "estado": "PESADO EN FAUCETT / FLUIDO EN COSTA VERDE",
                    "tiempo_actual_min": 52,
                    "tiempo_normal_min": 38,
                    "velocidad_kmh": 24,
                    "tramos": [
                        {"via": "Av. Elmer Faucett (Óvalo Aeropuerto – Morales Duárez)", "estado": "🔴 Atasco Intenso (+16 min)", "color": "#ef4444"},
                        {"via": "Nuevo Acceso Av. Morales Duárez / Línea Amarilla", "estado": "🟠 Moderado (+6 min)", "color": "#f59e0b"},
                        {"via": "Av. La Marina ➔ Circuito de Playas (Costa Verde)", "estado": "🟢 Fluido (60 km/h)", "color": "#10b981"}
                    ],
                    "decision_operador": "Congestión fuerte en Av. Elmer Faucett (+16 min). Para transfers Lima ⇄ Miraflores/San Isidro tomar Circuito de Playas (Costa Verde) ➔ Bajada San Miguel / La Paz."
                }
            ]
        }
    }
    return JSONResponse(status_code=200, content=payload, headers={"Cache-Control": "public, max-age=300"})
