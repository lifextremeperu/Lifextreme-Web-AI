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
        const { action = '', booking = null, message = '', history = [], profile = {} } = req.body || {};
        const groqKey = (process.env.GROQ_API_KEY || '').trim();
        const qdrantTunnelUrl = (process.env.QDRANT_TUNNEL_URL || 'https://expression-writings-boxing-mitsubishi.trycloudflare.com').replace(/\/$/, '');

        // 0. REGISTRO DIRECTO DE RESERVAS EN BACKEND QDRANT + NOTIFICACIÓN TELEGRAM
        if (action === 'register_booking' && booking) {
            try {
                const regRes = await fetch(`${qdrantTunnelUrl}/api/v1/agents/bookings/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(booking)
                });
                if (regRes.ok) {
                    const regData = await regRes.json();
                    return res.status(200).json({ ok: true, booking: regData });
                }
            } catch (e) {}
            return res.status(200).json({ ok: true, booking });
        }

        // 1. PRIORIDAD 1: Puente directo a nuestro Cerebro Vectorial Qdrant (337,000+ vectores + 5 Agentes + Ollama local)
        try {
            const qdrantRes = await fetch(`${qdrantTunnelUrl}/webhook/lifextreme`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, history, profile })
            });
            if (qdrantRes.ok) {
                const qdrantData = await qdrantRes.json();
                const qdrantReply = qdrantData.mensaje || qdrantData.reply || '';
                if (qdrantReply && !qdrantReply.includes('Disculpa, estoy teniendo un problema')) {
                    return res.status(200).json({
                        mensaje: qdrantReply,
                        source: 'qdrant_337k_rag'
                    });
                }
            }
        } catch (tunnelErr) {
            // Si el túnel local está cerrado temporalmente, continúa al motor conversacional
        }

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
        if (q.includes('otra') || q.includes('otrra') || q.includes('opcion') || q.includes('ppcion') || q.includes('alternativa') || q.includes('rutas') || q.includes('cuales')) {
            fallbackReply = `En Cusco y el Perú operamos varias travesías de clase mundial para que elijas según tu estilo:\n\n• **Salkantay Trek & Glamping (4D/3N):** Domos Geodésicos frente al glaciar en Soraypampa (3,900m), desfase horario sin multitudes y cierre en Machu Picchu.\n• **Circuito Ausangate & 7 Lagunas (6D/5N):** Alta montaña pura rodeando el Apu Ausangate (pasos de 5,000m), aguas termales de Pacchanta y cero masificación.\n• **Choquequirao Expedición Legendaria (4D/3N):** El cañón del Apurímac y la ciudadela hermana de Machu Picchu en exclusividad.\n• **Cordillera Blanca en Huaraz:** Trekking Santa Cruz (4D) y Laguna 69.\n\n¿Buscas una ruta que termine en Machu Picchu o prefieres una expedición de alta montaña y lagunas como Ausangate?`;
        } else if (q.includes('ausangate')) {
            fallbackReply = `El **Circuito Ausangate & 7 Lagunas Glamping (6D/5N)** es nuestra ruta más espectacular de alta montaña en Cusco: rodeamos el nevado sagrado Ausangate pasando por pasos como Palomani (5,100 msnm), las **7 Lagunas turquesas de Pacchanta** con aguas termales y comunidades alpaqueras.\n\nIncluimos **Duffle Bag de 7 kg** porteado por arrieros (Ley N° 31614), carpas térmicas 4 estaciones / domos, monitoreo de oxígeno dos veces al día y fisioterapia de recuperación en campamento. ¿Para qué mes estás planeando hacer Ausangate y cuántas personas viajan contigo?`;
        } else if (q.includes('choquequirao')) {
            fallbackReply = `**Choquequirao Expedición Legendaria (4D/3N)** te lleva a la ciudadela inca hermana de Machu Picchu, suspendida sobre el imponente Cañón del Apurímac y visitada por menos del 1% de los viajeros que llegan a Cusco.\n\nOperamos con mulas y arrieros certificados (llevan tu **Duffle Bag de 7 kg**), campamentos privados y guías UIAGM/WFR. ¿Qué mes tienes en mente para esta travesía?`;
        } else if (q.includes('camino inca') || q.includes('inca trail')) {
            fallbackReply = `El **Camino Inca Clásico a Machu Picchu (4D/3N)** recorre la red vial imperial entrando directamente por la Puerta del Sol (Inti Punku), con cumplimiento estricto de la **Ley del Porteador N° 31614** (pesaje digital auditado).\n\nRecuerda que los permisos del Ministerio de Cultura son limitados por día (y en febrero cierra por mantenimiento anual). ¿Para qué mes te gustaría verificar disponibilidad de permisos?`;
        } else if (q.includes('huaraz') || q.includes('santa cruz') || q.includes('laguna 69') || q.includes('mateo')) {
            fallbackReply = `En la **Cordillera Blanca (Huaraz)** operamos el famoso **Trekking Santa Cruz (4D/3N)** cruzando el paso Punta Unión (4,750m), la aclimatación en **Laguna 69** y tu primer glaciar de alta montaña en el **Nevado Mateo (5,150m)** con equipo técnico Petzl/Grivel incluido.\n\n¿Buscas trekking escénico entre lagunas o te gustaría coronar cumbre en glaciar?`;
        } else if (q.includes('arequipa') || q.includes('colca') || q.includes('misti')) {
            fallbackReply = `En **Arequipa** operamos el **Trekking al Cañón del Colca (3D/2N)** descendiendo hasta el Oasis de Sangalle y el **Ascenso al Volcán Misti (5,825m en 2D/1N)** con guías de alta montaña UIAGM y equipo completo.\n\n¿Prefieres caminata por cañón y aguas termales o cumbre volcánica sobre los 5,800 metros?`;
        } else if (q.includes('iquitos') || q.includes('selva') || q.includes('amazon') || q.includes('pacaya')) {
            fallbackReply = `En la Amazonía operamos la **Expedición Pacaya Samiria (5D/4N)** desde Iquitos, navegando por la selva de los espejos con avistamiento de delfines rosados, caminatas nocturnas y campamentos inmersivos con guías nativos.\n\n¿Para qué fecha te gustaría explorar la selva y cuántos integrantes serían?`;
        } else if (q.includes('fecha') || q.includes('diciembre') || q.includes('cuando') || q.includes('salid')) {
            fallbackReply = `Tenemos **salidas diarias confirmadas del 1 al 31 de diciembre** (incluyendo semanas de Navidad y Año Nuevo) y durante todo el año, tanto en grupos pequeños (máximo 8 viajeros por guía) como en formato privado.\n\nIncluimos **Domos Geodésicos / Campamentos Pro**, **Duffle Bag de 7 kg** porteado por arrieros (Ley N° 31614) y monitoreo de oxígeno dos veces al día. ¿Tienen pensado viajar en la primera quincena o cerca de fin de año, y cuántos serían en el grupo?`;
        } else if (q.includes('altura') || q.includes('aclimat') || q.includes('soroche')) {
            fallbackReply = `Para que disfrutes el paso de montaña sin malestar, te recomendamos estar en Cusco o el Valle Sagrado al menos **2 días antes** de iniciar la caminata.\n\nDurante toda la ruta medimos tu saturación de oxígeno mañana y tarde, llevamos oxígeno medicinal y al llegar al campamento realizamos sesiones de recuperación muscular con botas de compresión y pediluvios calientes. ¿Ya has caminado antes sobre los 3,500 metros?`;
        } else if (q.includes('equipaje') || q.includes('mochila') || q.includes('llevar') || q.includes('peso') || q.includes('duffle')) {
            fallbackReply = `No tienes que cargar peso pesado en la caminata: la noche previa en Cusco te entregamos un **Duffle Bag oficial donde puedes meter hasta 7 kg** (tu ropa de abrigo y saco de dormir), el cual llevan nuestros arrieros en mulas.\n\nTú solo caminas con una mochila ligera de día (20 a 25 litros) para tu agua, cámara y casaca impermeable. ¿Ya cuentas con equipo de trekking o te gustaría ver qué implementos tenemos disponibles?`;
        } else {
            fallbackReply = `El **Salkantay 4 Días / 3 Noches** es una de las travesías más hermosas de Cusco: combina los **Domos Glamping frente al glaciar en Soraypampa**, salidas con desfase horario para caminar sin multitudes y el cierre en **Machu Picchu**. También operamos **Ausangate 7 Lagunas (6D)**, **Choquequirao (4D)** y **Cordillera Blanca en Huaraz**.\n\nCuéntame un poco más de tu plan: ¿qué ruta te llama más la atención y para qué mes están pensando viajar?`;
        }

        return res.status(200).json({ mensaje: fallbackReply, source: 'organic_domain' });
    } catch (err) {
        return res.status(200).json({
            mensaje: `Para **Salkantay 4D/3N** contamos con salidas diarias todo diciembre y descanso en Domos Glamping en Soraypampa. ¿Para qué fechas aproximadas estás planeando tu viaje?`
        });
    }
}
