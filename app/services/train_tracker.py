"""
Servicio de Itinerarios y Telemetría Ferroviaria Simulada (PeruRail / Inca Rail)
Corredor San Pedro (Cusco) -> Poroy -> Ollantaytambo -> Aguas Calientes -> Hidroeléctrica
"""

import time
from typing import List, Dict, Any

# Catálogo oficial de frecuencias diarias de PeruRail (Expedition, Vistadome, Hiram Bingham)
# e Inca Rail (The Voyager, The 360°, The First Class) con ventanas de tránsito continuo.
DAILY_TRAIN_SCHEDULES: List[Dict[str, Any]] = [
    {
        "train_id": "PR-84P-Expedition",
        "operator": "PeruRail",
        "service": "Expedition 84",
        "route_segment": "Ollantaytambo_AguasCalientes",
        "departure_station": "Ollantaytambo",
        "arrival_station": "Aguas Calientes",
        "duration_minutes": 90,
        "phase_offset_minutes": 18,
        "speed_kmh": 42,
        "wagons": 6,
        "occupancy_pct": 94
    },
    {
        "train_id": "IR-43-Voyager",
        "operator": "Inca Rail",
        "service": "The Voyager 43",
        "route_segment": "Ollantaytambo_AguasCalientes",
        "departure_station": "Ollantaytambo",
        "arrival_station": "Aguas Calientes",
        "duration_minutes": 95,
        "phase_offset_minutes": 52,
        "speed_kmh": 40,
        "wagons": 5,
        "occupancy_pct": 88
    },
    {
        "train_id": "PR-304-Vistadome",
        "operator": "PeruRail",
        "service": "Vistadome Observatory 304",
        "route_segment": "AguasCalientes_Ollantaytambo",
        "departure_station": "Aguas Calientes",
        "arrival_station": "Ollantaytambo",
        "duration_minutes": 92,
        "phase_offset_minutes": 34,
        "speed_kmh": 41,
        "wagons": 6,
        "occupancy_pct": 96
    },
    {
        "train_id": "IR-62-The360",
        "operator": "Inca Rail",
        "service": "The 360° Machu Picchu Train",
        "route_segment": "AguasCalientes_Ollantaytambo",
        "departure_station": "Aguas Calientes",
        "arrival_station": "Ollantaytambo",
        "duration_minutes": 95,
        "phase_offset_minutes": 68,
        "speed_kmh": 39,
        "wagons": 4,
        "occupancy_pct": 91
    },
    {
        "train_id": "PR-11-HiramBingham",
        "operator": "PeruRail",
        "service": "Belmond Hiram Bingham",
        "route_segment": "Poroy_AguasCalientes",
        "departure_station": "Poroy (Cusco)",
        "arrival_station": "Aguas Calientes",
        "duration_minutes": 195,
        "phase_offset_minutes": 85,
        "speed_kmh": 38,
        "wagons": 4,
        "occupancy_pct": 100
    },
    {
        "train_id": "PR-71-SanPedro",
        "operator": "PeruRail",
        "service": "Expedition 71 San Pedro",
        "route_segment": "SanPedro_Ollantaytambo",
        "departure_station": "San Pedro (Cusco)",
        "arrival_station": "Ollantaytambo",
        "duration_minutes": 115,
        "phase_offset_minutes": 44,
        "speed_kmh": 36,
        "wagons": 5,
        "occupancy_pct": 89
    },
    {
        "train_id": "PR-51-Hidroelectrica",
        "operator": "PeruRail",
        "service": "Autovagón Local Hidroeléctrica",
        "route_segment": "AguasCalientes_Hidroelectrica",
        "departure_station": "Aguas Calientes",
        "arrival_station": "Hidroeléctrica",
        "duration_minutes": 32,
        "phase_offset_minutes": 11,
        "speed_kmh": 30,
        "wagons": 2,
        "occupancy_pct": 82
    }
]


class TrainTrackerService:
    """
    Motor de evaluación horaria y cálculo de ventanas espaciotemporales activas
    para la flota ferroviaria de PeruRail e Inca Rail.
    """

    def get_active_trains(self, now_ms: int | None = None) -> List[Dict[str, Any]]:
        if now_ms is None:
            now_ms = int(time.time() * 1000)

        active_trains: List[Dict[str, Any]] = []

        for sched in DAILY_TRAIN_SCHEDULES:
            duration_ms = int(sched["duration_minutes"] * 60 * 1000)
            offset_ms = int(sched["phase_offset_minutes"] * 60 * 1000)

            # Alinear de forma determinista con el reloj UTC para que todos los clientes
            # vean exactamente la misma posición interpolada en tiempo real
            cycle_index = (now_ms + offset_ms) // duration_ms
            departure_ms = (cycle_index * duration_ms) - offset_ms
            arrival_ms = departure_ms + duration_ms

            active_trains.append({
                "train_id": sched["train_id"],
                "operator": sched["operator"],
                "service": sched["service"],
                "status": "en_ruta",
                "route_segment": sched["route_segment"],
                "speed_kmh": sched["speed_kmh"],
                "wagons": sched["wagons"],
                "occupancy_pct": sched["occupancy_pct"],
                "departure": {
                    "station": sched["departure_station"],
                    "timestamp_ms": departure_ms
                },
                "arrival": {
                    "station": sched["arrival_station"],
                    "timestamp_ms": arrival_ms
                }
            })

        return active_trains


train_tracker_service = TrainTrackerService()
