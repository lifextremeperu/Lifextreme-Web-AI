import { GoogleGenerativeAI } from '@google/generative-ai';

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
    const apiKey = process.env.GEMINI_API_KEY;

    // Fallback for demo if no key (remove in production)
    if (!apiKey) {
        console.warn("⚠️ GEMINI_API_KEY missing. Returning mock response for testing.");
        const { message } = request.body || {};
        // Mock simple response if no API key
        return response.status(200).json({
            reply: `(Modo Demo - Sin API Key) He recibido tu mensaje: "${message}". En producción, aquí te respondería Alex con datos reales del clima en Cusco.`,
            timestamp: new Date().toISOString()
        });
    }

    try {
        // 3. Parse Request
        const { message, history = [], context = {} } = request.body || {};

        if (!message) {
            return response.status(400).json({ error: 'Message is required' });
        }

        // 4. Fetch Weather Data (Intelligence)
        const weatherContext = await getWeatherContext();

        // 5. Initialize Gemini
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({
            model: "gemini-1.5-flash",
            systemInstruction: `
                Actúa como "Alex", el Guía Principal de Lifextreme y Analista de Aventuras.
                
                *** INFO DE INTELIGENCIA DE NEGOCIOS (CLIMA REAL) ***
                ${weatherContext}
                *****************************************************

                **Tu Misión:**
                1. Recomendar tours basados en el clima ACTUAL y la temporada. Si llueve mucho hoy, sugiere museos o tours gastronómicos, no montaña.
                2. Si el usuario pregunta por fechas futuras, usa la "Seasonal Intelligence".
                3. Proteger al usuario: Si hay ALERTA ROJA, advierte sobre seguridad.

                **Tu Personalidad:**
                - **Experto pero Cool:** Sabes de meteorología andina pero lo explicas fácil.
                - **Vendedor Sutil:** "Viendo que hace sol, es el día perfecto para cuatrimotos. ¿Te reservo?"
                - **Breve y Directo.**

                **Reglas:**
                - NUNCA menciones "API" o "Open-Meteo". Di "mis reportes dicen..." o "veo en el radar...".
                - Si el clima es malo, ofrece alternativas (Plan B).
                
                **Contexto del Viajero:** ${JSON.stringify(context)}
            `
        });

        // 6. Build Chat Session
        let validHistory = [];
        if (Array.isArray(history)) {
            validHistory = history.map(h => ({
                role: h.role === 'ai' ? 'model' : 'user',
                parts: [{ text: h.text }]
            }));
        }

        const chat = model.startChat({
            history: validHistory,
            generationConfig: {
                maxOutputTokens: 600,
                temperature: 0.7,
            },
        });

        // 7. Generate Response
        const result = await chat.sendMessage(message);
        const responseText = result.response.text();

        // 8. Success Response
        return response.status(200).json({
            reply: responseText,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('❌ Gemini API Error:', error);
        return response.status(500).json({
            error: 'AI Engine Error',
            message: 'Life AI is currently rebooting systems. Please try again.',
            details: error.message
        });
    }
}
