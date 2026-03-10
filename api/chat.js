
// Helper: Fetch Real-time Weather from Open-Meteo
async function getWeatherContext() {
    try {
        // Cusco Coordinates
        const lat = -13.5319;
        const lon = -71.9675;
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,precipitation,weather_code,wind_speed_10m&daily=precipitation_sum,weather_code&timezone=America%2FLima&forecast_days=1`;

        const response = await fetch(url);
        const data = await response.json();

        const current = data.current;
        const daily = data.daily;

        // WMO Weather Code Interpretation
        const wmo = {
            0: "Cielo Despejado ☀️",
            1: "Mayormente Despejado 🌤️",
            2: "Nublado Parcialmente ⛅",
            3: "Nublado ☁️",
            45: "Niebla 🌫️",
            51: "Llovizna Ligera 🌦️",
            61: "Lluvia Moderada 🌧️",
            63: "Lluvia Fuerte 🌧️",
            80: "Lluvia Torrencial ⛈️",
            95: "Tormenta Eléctrica ⚡"
        };

        const weatherDesc = wmo[current.weather_code] || "Clima Variable";

        // Disaster/Risk Analysis
        let alertLevel = "VERDE";
        let alertMessage = "";

        if (current.precipitation > 5 || current.wind_speed_10m > 40 || current.weather_code >= 60) {
            alertLevel = "AMARILLA";
            alertMessage = "Precaución: Lluvias activas.";
        }
        if (current.precipitation > 15 || current.wind_speed_10m > 70 || current.weather_code >= 80) {
            alertLevel = "ROJA";
            alertMessage = "ALERTA: Condiciones climáticas adversas. Posibles cancelaciones.";
        }

        return `
            DATOS CLIMÁTICOS EN TIEMPO REAL (Cusco):
            - Condición: ${weatherDesc}
            - Temperatura: ${current.temperature_2m}°C
            - Lluvia Actual: ${current.precipitation} mm
            - Viento: ${current.wind_speed_10m} km/h
            - NIVEL DE ALERTA: ${alertLevel} ${alertMessage ? `(${alertMessage})` : ''}
            
            SEASONAL INTELLIGENCE (Para contestar "¿Cuándo ir?"):
            - Temporada Seca (Alta): Mayo a Octubre (Mejor para fotos, cielos azules, noches frías).
            - Temporada Lluvias (Baja): Noviembre a Abril (Paisajes verdes, menos gente, lluvias tardes/noches).
            - Mes Secreto: Abril u Octubre (Hombro de temporada, equilibrio perfecto).
        `;
    } catch (e) {
        console.error("Weather API Error:", e);
        return "Datos climáticos no disponibles temporalmente.";
    }
}

export default async function handler(request, response) {
    // 1. CORS Configuration
    response.setHeader('Access-Control-Allow-Credentials', true)
    response.setHeader('Access-Control-Allow-Origin', '*')
    response.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT')
    response.setHeader(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    )

    // Handle Preflight
    if (request.method === 'OPTIONS') {
        return response.status(200).end();
    }

    // 2. Auth Check (Server-side)
    const difyApiKey = process.env.DIFY_API_KEY || 'app-WXQvLfYuqOFNGEh7q4V8dtak';
    const difyBaseUrl = process.env.DIFY_BASE_URL || 'https://api.dify.ai/v1';

    try {
        // 3. Parse Request
        const { message, context = {} } = request.body || {};

        if (!message) {
            return response.status(400).json({ error: 'Message is required' });
        }

        // 4. Fetch Weather Data (Intelligence)
        const weatherContext = await getWeatherContext();

        // 5. Call Dify API
        const difyResponse = await fetch(`${difyBaseUrl}/chat-messages`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${difyApiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: message,
                inputs: {
                    weather_context: weatherContext,
                    user_profile: JSON.stringify(context)
                },
                response_mode: "blocking",
                user: context.personal?.fullName || "anonymous-web-user"
            })
        });

        if (!difyResponse.ok) {
            const errorData = await difyResponse.json().catch(() => ({}));
            throw new Error(errorData.message || `Dify API error: ${difyResponse.status}`);
        }

        const data = await difyResponse.json();

        // 6. Success Response
        return response.status(200).json({
            reply: data.answer || 'Lo siento, no pude procesar tu solicitud en este momento.',
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('❌ Dify API Error:', error);
        return response.status(500).json({
            error: 'AI Engine Error',
            message: 'Life AI is currently rebooting systems. Please try again.',
            details: error.message
        });
    }
}
