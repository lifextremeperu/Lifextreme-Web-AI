// ==============================================================================
// LIFEXTREME MAX AI — Conversational Assistant & Multiagent Orchestrator (Vercel)
// Estilo limpio, orgánico y consultivo (tipo Gemini / ChatGPT).
// ==============================================================================

export default async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    try {
        const { message = '', history = [], profile = {} } = req.body || {};
        const groqKey = (process.env.GROQ_API_KEY || '').trim();

        const hasBooking = Boolean(profile && profile.booking_code) || /\bLX-[A-Z0-9]{4,10}\b/i.test(message);
        const roleDirective = hasBooking
            ? `El usuario YA TIENE UNA RESERVA CONFIRMADA (${profile.booking_code || 'Activa'}). Atiéndelo como su Concierge Post-Venta (aclimatación médica, Duffle Bag de 7 kg, itinerario). No intentes venderle.`
            : `El usuario está explorando o consultando en la web. Atiéndelo de forma orgánica, consultiva y sin presionarlo a comprar.`;

        const systemPrompt = `Eres MAX, el asistente experto en montaña y expediciones de Lifextreme Perú (certificado UIAGM).
${roleDirective}

ESTILO DE CONVERSACIÓN (TIPO GEMINI / CHATGPT):
1. Limpio, natural, empático y directo al grano (máximo 2 párrafos breves, 60 a 90 palabras).
2. Responde SIEMPRE la duda exacta del usuario primero (ej. fechas, clima en diciembre, ruta, dificultad, aclimatación o equipaje).
3. NO lances discursos agresivos de venta, ni listes precios o enlaces de pago si el usuario no los ha pedido.
4. Al final de tu respuesta, haz una sola pregunta suave y natural para entender mejor su viaje (por ejemplo: con quién viaja, qué ritmo de caminata prefieren o qué días de ese mes les acomodan más).

INFORMACIÓN OPERATIVA VERIFICADA DE LIFEXTREME PERÚ:
- Fechas en Diciembre y Todo el Año: En Salkantay Trek (4D/3N y 5D/4N), Ausangate y Choquequirao tenemos salidas diarias garantizadas del 1 al 31 de diciembre (incluyendo Navidad y Año Nuevo) desde 2 personas, en grupo reducido (máx. 8 personas por guía) o en privado.
- Alojamiento: Domos Geodésicos Glamping en Soraypampa (3,900 msnm) con aislamiento térmico y duchas calientes.
- Desfase Horario (Offset Trekking): Salimos 90 minutos antes que los grupos masivos para cruzar el Abra Salkantay (4,630m) en silencio y sin multitudes.
- Equipaje (Duffle Bag 7 kg & Ley N° 31614): Te damos un Duffle Bag para hasta 7 kg que llevan nuestros arrieros con pesaje digital certificado; tú solo caminas con una mochila ligera de día.
- Seguridad y Aclimatación: Control de oximetría 2 veces al día, oxígeno medicinal portátil, fisioterapia en campamento (botas de compresión y pediluvios botánicos) y soporte clínico con O2 Medical Network.
- Precios de referencia (solo menciónalos si el usuario pregunta cuánto cuesta o quiere reservar): Salkantay 4D/3N S/ 1,850, Ausangate 6D S/ 2,100, Choquequirao 4D S/ 3,200, Camino Inca 4D S/ 2,450 (se separan con el 30%).`;

        const messages = [
            { role: 'system', content: systemPrompt },
            ...(Array.isArray(history) ? history.slice(-6).map(m => ({
                role: m.role === 'user' ? 'user' : 'assistant',
                content: String(m.content || '')
            })) : []),
            { role: 'user', content: String(message) }
        ];

        if (groqKey) {
            const groqRes = await fetch('https://api.groq.com/openai/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${groqKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: 'llama-3.3-70b-versatile',
                    messages,
                    temperature: 0.45,
                    max_tokens: 350
                })
            });

            if (groqRes.ok) {
                const data = await groqRes.json();
                const reply = data.choices?.[0]?.message?.content || '';
                if (reply) {
                    return res.status(200).json({ mensaje: reply, source: 'groq_lpu' });
                }
            }
        }

        // Respuesta conversacional inteligente por dominio si no hay API key en entorno cloud
        const q = String(message).toLowerCase();
        let fallbackReply = '';
        if (q.includes('fecha') || q.includes('diciembre') || q.includes('cuando') || q.includes('salid')) {
            fallbackReply = `Para **Salkantay 4 Días / 3 Noches en diciembre** tenemos salidas diarias confirmadas del **1 al 31 de diciembre** (incluyendo semanas de Navidad y Año Nuevo), tanto en grupos pequeños (máximo 8 viajeros por guía) como en formato privado.\n\nEn diciembre la montaña luce increíble y descansamos en nuestros **Domos Geodésicos en Soraypampa (3,900 msnm)** bien abrigados de la lluvia andina. ¿Tienen pensado viajar en la primera quincena o cerca de fin de año, y cuántos serían en el grupo?`;
        } else if (q.includes('altura') || q.includes('aclimat') || q.includes('soroche')) {
            fallbackReply = `Para que disfrutes el paso de montaña sin malestar, te recomendamos estar en Cusco o el Valle Sagrado al menos **2 días antes** de iniciar la caminata.\n\nDurante toda la ruta medimos tu saturación de oxígeno mañana y tarde, llevamos oxígeno medicinal y al llegar al campamento realizamos sesiones de recuperación muscular con botas de compresión y pediluvios calientes. ¿Ya has caminado antes sobre los 3,500 metros?`;
        } else if (q.includes('equipaje') || q.includes('mochila') || q.includes('llevar') || q.includes('peso') || q.includes('duffle')) {
            fallbackReply = `No tienes que cargar peso pesado en la caminata: la noche previa en Cusco te entregamos un **Duffle Bag oficial donde puedes meter hasta 7 kg** (tu ropa de abrigo y saco de dormir), el cual llevan nuestros arrieros en mulas.\n\nTú solo caminas con una mochila ligera de día (20 a 25 litros) para tu agua, cámara y casaca impermeable. ¿Ya cuentas con equipo de trekking o te gustaría ver qué implementos tenemos disponibles?`;
        } else {
            fallbackReply = `El **Salkantay 4 Días / 3 Noches** es una de las travesías más hermosas de Cusco: combina los **Domos Glamping frente al glaciar en Soraypampa**, salidas con desfase horario para caminar sin multitudes y el cierre en **Machu Picchu**.\n\nCuéntame un poco más de tu plan: ¿para qué mes están pensando viajar y cuántas personas vienen contigo?`;
        }

        return res.status(200).json({ mensaje: fallbackReply, source: 'organic_domain' });
    } catch (err) {
        return res.status(200).json({
            mensaje: `Para **Salkantay 4D/3N** contamos con salidas diarias todo diciembre y descanso en Domos Glamping en Soraypampa. ¿Para qué fechas aproximadas estás planeando tu viaje?`
        });
    }
}
