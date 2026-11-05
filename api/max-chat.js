// ==============================================================================
// LIFEXTREME MAX AI — Serverless Conversational & Multiagent Endpoint (Vercel)
// Responde preguntas reales (fechas, Salkantay, aclimatación, Duffle Bag 7kg, VIP)
// y diferencia entre Visitante Web (Ventas) y Pasajero Confirmado (Post-Venta).
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
        const bookingBanner = hasBooking
            ? `ESTADO DEL CLIENTE: PASAJERO CON RESERVA CONFIRMADA (${profile.booking_code || 'Código verificado'}). Atiéndelo como Concierge Post-Venta activando el Agente 1 (Médico/Aclimatación), Agente 2 (Duffle Bag 7kg & Ley 31614) y Agente 5 (Calidad). NO le vendas de nuevo.`
            : `ESTADO DEL CLIENTE: VISITANTE EN LA WEB. Responde directamente a su pregunta específica (fechas, salidas, clima, precios, ruta) con calidez y precisión de operador UIAGM.`;

        const systemPrompt = `Eres MAX, Director Comercial y Operador UIAGM de Lifextreme Perú.
${bookingBanner}

REGLAS DE ORO:
1. RESPONDE SIEMPRE LA PREGUNTA EXACTA DEL USUARIO PRIMERO (en 2 párrafos cortos y claros). NUNCA cambies de destino (si pregunta por Salkantay, habla de Salkantay 4D/3N o 5D/4N, jamás lo cambies por Choquequirao).
2. FECHAS Y SALIDAS EN DICIEMBRE / TODO EL AÑO:
   - Salkantay Trek & Domos Glamping (4D/3N y 5D/4N): Tenemos salidas garantizadas TODOS LOS DÍAS en diciembre (del 1 al 31 de diciembre, incluyendo salidas especiales de Navidad y Año Nuevo en Machu Picchu) a partir de 2 pasajeros, tanto en grupo reducido (ratio máx. 1:8) como en modalidad Privada VIP.
   - En diciembre (inicio de temporada verde andina), nuestros Domos Geodésicos en Soraypampa (3,900m) ofrecen aislamiento térmico total, camas confort y duchas calientes, además de salidas con desfase horario (Offset Trekking +/- 90 min) para caminar sin multitudes.
3. ESTÁNDARES EXCLUSIVOS LIFEXTREME PERÚ (MALLA DE 5 AGENTES):
   - Agente 1 (Médico & Aclimatación): Escalera de 2 días previos en Cusco/Valle Sagrado, control de SpO2/Tensión 2 veces al día, oxígeno medicinal 3m³, fisioterapia en campamento con botas de compresión neumática solar y pediluvios botánicos andinos, y corredor clínico con O2 Medical Network.
   - Agente 2 (Duffle Bag 7 kg & Ley 31614): Entregamos Duffle Bag para hasta 7 kg llevado por arrieros/mulas, con pesaje digital certificado visible ante el cliente y Pasaporte Ético Animal.
   - Agente 3 (Tailor-Made VIP): Expediciones privadas con camioneta 4x4 de respaldo, guía UIAGM exclusivo y gastronomía funcional hiperlocal.
4. PRECIOS OFICIALES REFERENCIALES:
   - Salkantay Trek a Machu Picchu 4D/3N (Glamping & Tren): S/ 1,850 por persona (Reserva con 30%: S/ 555).
   - Choquequirao Expedición Legendaria 4D/3N: S/ 3,200 por persona.
   - Circuito Ausangate & 7 Lagunas 6D: S/ 2,100 por persona.
   - Camino Inca Clásico 4D: S/ 2,450 por persona (cerrado solo en febrero por mantenimiento; abierto todo diciembre con reserva anticipada).`;

        const messages = [
            { role: 'system', content: systemPrompt },
            ...(Array.isArray(history) ? history.slice(-6).map(m => ({
                role: m.role === 'user' ? 'user' : 'assistant',
                content: String(m.content || '')
            })) : []),
            { role: 'user', content: String(message) }
        ];

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
                max_tokens: 450
            })
        });

        if (groqRes.ok) {
            const data = await groqRes.json();
            const reply = data.choices?.[0]?.message?.content || '';
            if (reply) {
                return res.status(200).json({ mensaje: reply, source: 'groq_lpu' });
            }
        }

        return res.status(200).json({
            mensaje: `¡Hola! Para el **Salkantay Trek 4 Días / 3 Noches en diciembre**, contamos con **salidas diarias garantizadas todo el mes (del 1 al 31 de diciembre)** a partir de 2 personas, incluyendo fechas especiales de Navidad y Año Nuevo.\n\nNuestra expedición incluye pernocta en **Domos Geodésicos Glamping en Soraypampa (3,900 msnm)**, **Duffle Bag de 7 kg** porteado por arrieros bajo la Ley N° 31614, monitoreo biométrico de oxígeno dos veces al día y desfase horario (*Offset Trekking*) para cruzar el Abra Salkantay (4,630m) sin multitudes. ¿Para qué día exacto de diciembre y para cuántas personas deseas bloquear tus cupos con el 30%?`,
            source: 'fallback_domain'
        });
    } catch (err) {
        return res.status(200).json({
            mensaje: `¡Hola! Tenemos salidas diarias confirmadas todo diciembre para **Salkantay 4D/3N** con Domos Glamping, Duffle Bag de 7 kg y guía certificado UIAGM/WFR. Cuéntame para qué fecha exacta de diciembre y cuántos viajeros son para bloquearte los cupos.`,
            error: String(err)
        });
    }
}
