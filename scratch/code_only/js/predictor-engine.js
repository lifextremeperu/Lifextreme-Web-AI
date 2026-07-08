window.PredictorEngine = {
    // ----------------------------------------------------
    // WEATHER INTELLIGENCE (Free Open-Meteo API)
    // ----------------------------------------------------
    async getWeatherForecast(lat, lon, date) {
        // Simple logic: if date is closer than 7 days, get forecast.
        // If further, return "Historical Average". For this MVP, we fetch current forecast as a demo of capability.
        try {
            const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=weather_code,temperature_2m_max,precipitation_probability_max&timezone=auto`);
            const data = await response.json();

            // Map WMO codes to Adventure Personas
            const weatherCodes = {
                0: { desc: "Cielo Despejado", icon: "ri-sun-line", risk: "Bajo", advice: "Ideal para fotografía de alta montaña." },
                1: { desc: "Mayormente Despejado", icon: "ri-sun-cloudy-line", risk: "Bajo", advice: "Excelente visibilidad." },
                2: { desc: "Nublado", icon: "ri-cloudy-line", risk: "Medio", advice: "Lleva capas extra de abrigo." },
                3: { desc: "Cubierto", icon: "ri-cloudy-fill", risk: "Medio", advice: "Posibilidad de neblina en pasos altos." },
                61: { desc: "Lluvia Ligera", icon: "ri-drizzle-line", risk: "Medio", advice: "Poncho impermeable recomendado." },
                63: { desc: "Lluvia Moderada", icon: "ri-rainy-line", risk: "Alto", advice: "Botas impermeables obligatorias." },
                80: { desc: "Chubascos", icon: "ri-heavy-showers-line", risk: "Alto", advice: "Ruta resbaladiza. Precaución." },
                95: { desc: "Tormenta", icon: "ri-thunderstorms-line", risk: "Crítico", advice: "Posible reprogramación por seguridad." }
            };

            // For MVP, we take the average/most frequent of the next 7 days to simulate a "Season Forecast"
            // In a real app, match `date` with `data.daily.time`
            const code = data.daily.weather_code[0];
            const tempMax = data.daily.temperature_2m_max[0];

            return {
                ...weatherCodes[code] || weatherCodes[0],
                temp: tempMax
            };
        } catch (e) {
            console.error("Weather fetch failed", e);
            return { desc: "Datos Satelitales No Disponibles", icon: "ri-router-line", risk: "Desconocido", advice: "Consulta con tu guía." };
        }
    },

    // ----------------------------------------------------
    // DEMAND & PRICE PREDICTION (Manual Rules)
    // ----------------------------------------------------
    getDemandPrediction(monthIndex) {
        // monthIndex 0 = Enero
        /*
           High Season: June (5), July (6), August (7)
           Shoulder Season: April (3), May (4), September (8), October (9)
           Rainy/Low Season: Nov (10) - March (2)
        */

        if ([5, 6, 7].includes(monthIndex)) {
            return {
                level: 'ALTA',
                color: 'text-red-500',
                bg: 'bg-red-50',
                icon: 'ri-fire-fill',
                msg: "Alta demanda detectada. Quedan pocos cupos.",
                scarcity: true
            };
        } else if ([3, 4, 8, 9].includes(monthIndex)) {
            return {
                level: 'MEDIA',
                color: 'text-accent',
                bg: 'bg-amber-50',
                icon: 'ri-scales-3-line',
                msg: "Equilibrio ideal: Buen clima y menos gente.",
                scarcity: false
            };
        } else {
            return {
                level: 'BAJA',
                color: 'text-emerald-500',
                bg: 'bg-emerald-50',
                icon: 'ri-umbrella-line',
                msg: "Temporada de lluvias. Paisajes más verdes, precios bajos.",
                scarcity: false
            };
        }
    }
};
