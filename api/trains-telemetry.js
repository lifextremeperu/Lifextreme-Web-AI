/**
 * LIFEXTREME GEOINT 3D — SERVICIO DE TELEMETRÍA FERROVIARIA SIMULADA (PERURAIL / INCA RAIL)
 * Endpoint público: GET /api/v1/geoint/layers/trains (vía rewrite en vercel.json)
 * Sincronizado con app/services/train_tracker.py para interpolación espaciotemporal con Turf.js.
 */

const DAILY_TRAIN_SCHEDULES = [
    {
        train_id: "PR-84P-Expedition",
        operator: "PeruRail",
        service: "Expedition 84",
        route_segment: "Ollantaytambo_AguasCalientes",
        departure_station: "Ollantaytambo",
        arrival_station: "Aguas Calientes",
        duration_minutes: 90,
        phase_offset_minutes: 18,
        speed_kmh: 42,
        wagons: 6,
        occupancy_pct: 94
    },
    {
        train_id: "IR-43-Voyager",
        operator: "Inca Rail",
        service: "The Voyager 43",
        route_segment: "Ollantaytambo_AguasCalientes",
        departure_station: "Ollantaytambo",
        arrival_station: "Aguas Calientes",
        duration_minutes: 95,
        phase_offset_minutes: 52,
        speed_kmh: 40,
        wagons: 5,
        occupancy_pct: 88
    },
    {
        train_id: "PR-304-Vistadome",
        operator: "PeruRail",
        service: "Vistadome Observatory 304",
        route_segment: "AguasCalientes_Ollantaytambo",
        departure_station: "Aguas Calientes",
        arrival_station: "Ollantaytambo",
        duration_minutes: 92,
        phase_offset_minutes: 34,
        speed_kmh: 41,
        wagons: 6,
        occupancy_pct: 96
    },
    {
        train_id: "IR-62-The360",
        operator: "Inca Rail",
        service: "The 360° Machu Picchu Train",
        route_segment: "AguasCalientes_Ollantaytambo",
        departure_station: "Aguas Calientes",
        arrival_station: "Ollantaytambo",
        duration_minutes: 95,
        phase_offset_minutes: 68,
        speed_kmh: 39,
        wagons: 4,
        occupancy_pct: 91
    },
    {
        train_id: "PR-11-HiramBingham",
        operator: "PeruRail",
        service: "Belmond Hiram Bingham",
        route_segment: "Poroy_AguasCalientes",
        departure_station: "Poroy (Cusco)",
        arrival_station: "Aguas Calientes",
        duration_minutes: 195,
        phase_offset_minutes: 85,
        speed_kmh: 38,
        wagons: 4,
        occupancy_pct: 100
    },
    {
        train_id: "PR-71-SanPedro",
        operator: "PeruRail",
        service: "Expedition 71 San Pedro",
        route_segment: "SanPedro_Ollantaytambo",
        departure_station: "San Pedro (Cusco)",
        arrival_station: "Ollantaytambo",
        duration_minutes: 115,
        phase_offset_minutes: 44,
        speed_kmh: 36,
        wagons: 5,
        occupancy_pct: 89
    },
    {
        train_id: "PR-51-Hidroelectrica",
        operator: "PeruRail",
        service: "Autovagón Local Hidroeléctrica",
        route_segment: "AguasCalientes_Hidroelectrica",
        departure_station: "Aguas Calientes",
        arrival_station: "Hidroeléctrica",
        duration_minutes: 32,
        phase_offset_minutes: 11,
        speed_kmh: 30,
        wagons: 2,
        occupancy_pct: 82
    }
];

module.exports = async function handler(req, res) {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("Cache-Control", "no-store, max-age=0");

    if (req.method === "OPTIONS") {
        return res.status(200).end();
    }

    const nowMs = Date.now();
    const activeTrains = DAILY_TRAIN_SCHEDULES.map((sched) => {
        const durationMs = sched.duration_minutes * 60 * 1000;
        const offsetMs = sched.phase_offset_minutes * 60 * 1000;

        // Ventana de tránsito determinista sincronizada con el reloj del servidor
        const cycleIndex = Math.floor((nowMs + offsetMs) / durationMs);
        const departureMs = (cycleIndex * durationMs) - offsetMs;
        const arrivalMs = departureMs + durationMs;

        return {
            train_id: sched.train_id,
            operator: sched.operator,
            service: sched.service,
            status: "en_ruta",
            route_segment: sched.route_segment,
            speed_kmh: sched.speed_kmh,
            wagons: sched.wagons,
            occupancy_pct: sched.occupancy_pct,
            departure: {
                station: sched.departure_station,
                timestamp_ms: departureMs
            },
            arrival: {
                station: sched.arrival_station,
                timestamp_ms: arrivalMs
            }
        };
    });

    return res.status(200).json(activeTrains);
};
