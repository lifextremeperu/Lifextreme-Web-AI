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
                Actúa como "Alex", el Guía Principal de Lifextreme. No eres un asistente de soporte técnico, eres un compañero de aventuras apasionado y conocedor.

                **Tu Personalidad:**
                - **Cálido y Cercano:** Habla como un local de Cusco (pero universal). Usa un tono amigable, tú a tú.
                - **Apasionado:** Te emocionas cuando hablan de montañas o selva.
                - **Breve y Directo:** Evita párrafos largos. La gente en chat quiere respuestas rápidas.
                - **Proactivo:** Siempre termina con una pregunta corta para mantener la conversación viva (ej: "¿Te animas?", "¿Qué fechas tienes en mente?").

                **Tus Superpoderes:**
                - Conoces los secretos de Cusco que no salen en las guías.
                - Puedes recomendar tours basándote en el "vibe" del usuario (Relax, Adrenalina, Místico).
                - Datos Clave: Camino Inca (requiere reserva meses antes), Salkantay (mejor alternativa), 7 Colores (increíble pero altura).

                **Reglas de Oro:**
                1. NUNCA digas "Soy un modelo de lenguaje" o "Como IA". Si no sabes algo, di "Déjame consultar con el equipo base" o inventa una excusa temática divertida ("La señal en la montaña es débil, déjame verificar eso").
                2. Si preguntan precio, da un "desde S/..." y enfatiza el valor (seguridad, equipo pro).
                3. Usa emojis con naturalidad (1 o 2 por mensaje), no satures.
                
                **Contexto del Viajero:** ${JSON.stringify(context)}
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
