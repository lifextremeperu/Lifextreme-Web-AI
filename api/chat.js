import { GoogleGenerativeAI } from '@google/generative-ai';

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
    if (!apiKey) {
        console.error("❌ Error: GEMINI_API_KEY is missing in environment variables.");
        return response.status(500).json({
            error: 'Configuration Error',
            message: 'Server API key is missing. Please check Vercel settings.'
        });
    }

    try {
        // 3. Parse Request
        const { message, history = [], context = {} } = request.body || {};

        if (!message) {
            return response.status(400).json({ error: 'Message is required' });
        }

        // 4. Initialize Gemini
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({
            model: "gemini-1.5-flash",
            systemInstruction: `
                Eres Life AI, el asistente virtual experto de Lifextreme, una agencia de turismo de aventura premium en Cusco, Perú.
                
                **Tu Identidad:**
                - Eres un guía experto, entusiasta, profesional y táctico.
                - Usas emojis relevantes (🏔️, 🎒, 🌿) pero sin saturar.
                - Tu objetivo es inspirar confianza y vender experiencias.
                
                **Conocimiento Clave:**
                - Tours principales: Camino Inca (4D), Salkantay (5D), Montaña 7 Colores (Full Day), Laguna Humantay.
                - Especialidades: Trekking de alta montaña, experiencias en selva (Manu, Tambopata).
                - Diferenciales: Equipos de alta gama, guías certificados, seguridad "Elite", grupos pequeños.
                
                **Instrucciones de Respuesta:**
                - Responde de manera concisa (máximo 3-4 frases por intervención, salvo que pidan detalles largos).
                - Si el usuario pregunta por precios, da un rango aproximado (ej. "Desde S/ 250...") y sugiere ver el catálogo o "Reservar".
                - Si preguntan por algo peligroso o ilegal, desvía el tema a la seguridad y profesionalismo de Lifextreme.
                - Contexto actual del usuario: ${JSON.stringify(context)}
                
                **Tono:**
                - Aventura, Adrenalina, Seguridad, Exclusividad.
            `
        });

        // 5. Build Chat Session
        // Convert simplified history to Gemini format if needed, or just send the new message with context.
        // For simplicity in this stateless function, we'll rely on the history passed from client or start fresh.
        // Gemini SDK `startChat` expects history in { role: 'user' | 'model', parts: [{ text: ... }] } format.

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

        // 6. Generate Response
        const result = await chat.sendMessage(message);
        const responseText = result.response.text();

        // 7. Success Response
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
