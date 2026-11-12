// ==============================================================================
// LIFEXTREME MAX AI — Conversational Assistant & Multiagent Orchestrator (Vercel)
// Motor Híbrido Multi-LLM (Qdrant RAG -> Groq LPU -> Gemini -> Cloud LLM -> Context Engine)
// Con memoria conversacional, anti-repetición y cobertura total de destinos del Perú.
// ==============================================================================

const SYSTEM_PROMPT_BASE = `Eres MAX 🏔️, el especialista en alta montaña, selva, costa y expediciones de Lifextreme Perú (certificado UIAGM / WFR).

REGLAS DE COHERENCIA Y ESTILO (OBLIGATORIAS):
1. RESPONDE DIRECTAMENTE A LA PREGUNTA O DESTINO EXACTO DEL USUARIO desde la primera línea (si pregunta por Gocta, habla de Gocta en Amazonas/Chachapoyas; si pregunta por Huaraz, habla de Huaraz; si pregunta por Cusco, habla de Cusco). NUNCA cambies de tema a Salkantay si el usuario pregunta por otro destino.
2. Nunca repitas una respuesta anterior del historial.
3. Mantén un tono cálido, experto, conciso y natural (máximo 2 a 3 párrafos cortos o viñetas limpias, entre 70 y 130 palabras).
4. Cierra con UNA pregunta consultiva relevante sobre el destino que el usuario está consultando.

CATÁLOGO Y GEOGRAFÍA OFICIAL VERIFICADA DE LIFEXTREME PERÚ:
• AMAZONAS / CHACHAPOYAS (Selva Alta Norte):
  - Catarata de Gocta & Fortaleza de Kuélap (3D/2N o Full Day desde Chachapoyas): Caminata escénica por bosque de neblina desde Cocachimba o San Pablo de Valera hacia la Catarata de Gocta (771 metros de caída, una de las más altas del mundo, hábitat del gallito de las rocas y colibrí cola de espátula), combinada con la ciudadela amurallada de Kuélap en teleférico y Sarcófagos de Karajía. Tarifa: Full Day Gocta S/ 190 | Expedición Amazonas & Gocta 3D/2N S/ 890.
• AMAZONÍA / SELVA BAJA (Iquitos y Madre de Dios):
  - Reserva Nacional Pacaya Samiria desde Iquitos (5D/4N o 3D/2N): Navegación por la "Selva de los Espejos", delfines rosados, caminatas nocturnas y campamento inmersivo (S/ 1,650).
  - Reserva Nacional Tambopata & Lago Sandoval en Puerto Maldonado (3D/2N): Collpa de guacamayos de Chuncho, nutrias gigantes y lodges amazónicos (S/ 950).
• CUSCO — Travesías Multidía:
  - Salkantay Trek & Domos Glamping a Machu Picchu (4D/3N): Laguna Humantay, noche en Domos Geodésicos en Soraypampa (3,900m), Abra Salkantay (4,630m) con desfase horario sin multitudes y cierre en Machu Picchu. Tarifa base: S/ 1,630 (All-Inclusive: S/ 1,850).
  - Circuito Ausangate & 7 Lagunas Glamping (6D/5N): Alta montaña pura rodeando el Apu Ausangate (6,384m), pasos sobre 5,000m (Palomani), 7 Lagunas de Pacchanta y aguas termales. Tarifa base: S/ 1,880.
  - Choquequirao Expedición Legendaria (4D/3N): Cañón del Apurímac y la ciudadela hermana de Machu Picchu (S/ 2,980).
  - Camino Inca Clásico a Machu Picchu (4D/3N): Ingreso directo por la Puerta del Sol - Inti Punku (S/ 2,230).
• CUSCO — Rutas de 1 Día:
  - Montaña de 7 Colores (Vinicunca) & Valle Rojo Pro (1D, S/ 230), Laguna Humantay (1D, S/ 230), Cuatrimotos Maras Moray y Vía Ferrata & Zipline en el Valle Sagrado.
• HUARAZ / CORDILLERA BLANCA (Áncash):
  - Trekking Santa Cruz (4D/3N, S/ 980), Laguna 69 (1D, S/ 180) y Cumbre Glaciar Nevado Mateo 5,150m (1D, S/ 380 con equipo técnico Petzl/Grivel).
• AREQUIPA, ICA Y LIMA:
  - Arequipa: Trekking Cañón del Colca 3D/2N (S/ 630) y Ascenso Volcán Misti 5,825m 2D/1N (S/ 880).
  - Ica: Tubulares & Sandboarding Pro en Dunas de Huacachina + Islas Ballestas Paracas (S/ 240).
  - Lima: Parapente Costa Verde Miraflores (S/ 260) y Rafting/Canopy en Lunahuaná (S/ 220).
• ESTÁNDARES DE OPERACIÓN LIFEXTREME:
  - En treks de montaña incluimos Duffle Bag de 7 kg porteado por arrieros (Ley N° 31614), alimentación completa, guías UIAGM/WFR con oxímetro y oxígeno medicinal, y reserva flexible con el 30%.`;

async function fetchWithTimeout(url, options, timeoutMs = 5000) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
        const res = await fetch(url, { ...options, signal: controller.signal });
        clearTimeout(timer);
        return res;
    } catch (err) {
        clearTimeout(timer);
        throw err;
    }
}

function detectActiveRoute(message, history) {
    const combined = [
        String(message || ''),
        ...(Array.isArray(history) ? history.slice(-6).map(m => String(m.content || '')) : [])
    ].join(' ').toLowerCase();

    if (combined.includes('gocta') || combined.includes('chachapoyas') || combined.includes('kuelap') || combined.includes('amazonas') || combined.includes('cocachimba')) {
        return {
            name: 'Expedición Catarata de Gocta & Kuélap - Amazonas (3D/2N)',
            shortName: 'Catarata de Gocta & Kuélap (Amazonas)',
            region: 'Amazonas (Chachapoyas)',
            maxAltitude: '2,400 msnm (Bosque de Neblina)',
            priceBase: 'S/ 890 (3D/2N) o S/ 190 (Full Day Gocta)',
            priceAllInc: 'S/ 1,050',
            reserva30: 'S/ 267',
            campType: 'Eco-Lodges con vista a la caída de agua de 771m en Cocachimba'
        };
    }
    if (combined.includes('tambopata') || combined.includes('madre de dios') || combined.includes('puerto maldonado') || combined.includes('sandoval')) {
        return {
            name: 'Expedición Reserva Nacional Tambopata & Collpa Chuncho (3D/2N)',
            shortName: 'Reserva Tambopata (3D/2N)',
            region: 'Madre de Dios',
            maxAltitude: '200 msnm (Selva Baja Amazónica)',
            priceBase: 'S/ 950',
            priceAllInc: 'S/ 1,150',
            reserva30: 'S/ 285',
            campType: 'Amazon Eco-Lodge a orillas del río Tambopata'
        };
    }
    if (combined.includes('iquitos') || combined.includes('pacaya') || (combined.includes('selva') && !combined.includes('gocta'))) {
        return {
            name: 'Expedición Pacaya Samiria Amazonía (5D/4N)',
            shortName: 'Pacaya Samiria (Iquitos)',
            region: 'Loreto (Iquitos)',
            maxAltitude: '120 msnm (Selva de los Espejos)',
            priceBase: 'S/ 1,650',
            priceAllInc: 'S/ 1,850',
            reserva30: 'S/ 495',
            campType: 'Refugios amazónicos y campamentos inmersivos con guías nativos'
        };
    }
    if (combined.includes('ausangate') || combined.includes('7 lagunas') || combined.includes('siete lagunas')) {
        return {
            name: 'Circuito Ausangate & 7 Lagunas Glamping (6D/5N)',
            shortName: 'Ausangate 7 Lagunas (6D/5N)',
            region: 'Cusco',
            maxAltitude: '5,100 msnm (Paso Palomani)',
            priceBase: 'S/ 1,880',
            priceAllInc: 'S/ 2,100',
            reserva30: 'S/ 630',
            campType: 'Campamentos Glamping 4 estaciones y Aguas Termales de Pacchanta'
        };
    }
    if (combined.includes('choquequirao')) {
        return {
            name: 'Choquequirao Expedición Legendaria (4D/3N)',
            shortName: 'Choquequirao (4D/3N)',
            region: 'Cusco',
            maxAltitude: '3,050 msnm (Ciudadela Choquequirao)',
            priceBase: 'S/ 2,980',
            priceAllInc: 'S/ 3,200',
            reserva30: 'S/ 960',
            campType: 'Campamentos privados en el Cañón del Apurímac'
        };
    }
    if (combined.includes('camino inca') || combined.includes('inca trail')) {
        return {
            name: 'Camino Inca Clásico a Machu Picchu (4D/3N)',
            shortName: 'Camino Inca Clásico (4D/3N)',
            region: 'Cusco',
            maxAltitude: '4,215 msnm (Abra Warmiwañusqa)',
            priceBase: 'S/ 2,230',
            priceAllInc: 'S/ 2,450',
            reserva30: 'S/ 735',
            campType: 'Campamentos oficiales SERNANP con carpas térmicas 4 estaciones'
        };
    }
    if (combined.includes('vinicunca') || combined.includes('7 colores') || combined.includes('siete colores') || combined.includes('valle rojo')) {
        return {
            name: 'Montaña de los 7 Colores (Vinicunca) & Valle Rojo Pro (1 Día)',
            shortName: 'Vinicunca & Valle Rojo (1 Día)',
            region: 'Cusco',
            maxAltitude: '5,036 msnm (Mirador Vinicunca)',
            priceBase: 'S/ 230',
            priceAllInc: 'S/ 450',
            reserva30: 'S/ 135',
            campType: 'Full Day con salida temprana anti-multitudes (03:30 am) y restaurante buffet'
        };
    }
    if (combined.includes('huaraz') || combined.includes('santa cruz') || combined.includes('laguna 69') || combined.includes('mateo')) {
        return {
            name: 'Trekking Santa Cruz & Laguna 69 - Cordillera Blanca (4D/3N)',
            shortName: 'Santa Cruz & Laguna 69 (Huaraz)',
            region: 'Huaraz',
            maxAltitude: '4,750 msnm (Punta Unión)',
            priceBase: 'S/ 980',
            priceAllInc: 'S/ 1,200',
            reserva30: 'S/ 360',
            campType: 'Campamentos de alta montaña en el Parque Nacional Huascarán'
        };
    }
    if (combined.includes('arequipa') || combined.includes('colca') || combined.includes('misti')) {
        return {
            name: 'Trekking Cañón del Colca & Ascenso Volcán Misti (Arequipa)',
            shortName: 'Colca & Volcán Misti (Arequipa)',
            region: 'Arequipa',
            maxAltitude: '5,825 msnm (Cumbre Misti)',
            priceBase: 'S/ 630 (Colca 3D) / S/ 880 (Misti 2D)',
            priceAllInc: 'S/ 1,050',
            reserva30: 'S/ 264',
            campType: 'Oasis de Sangalle en el Colca y Campamento Nido de Águilas (4,600m) en el Misti'
        };
    }
    return {
        name: 'Salkantay Trek & Domos Glamping a Machu Picchu (4D/3N)',
        shortName: 'Salkantay Trek & Domos (4D/3N)',
        region: 'Cusco',
        maxAltitude: '4,630 msnm (Abra Salkantay)',
        priceBase: 'S/ 1,630',
        priceAllInc: 'S/ 1,850',
        reserva30: 'S/ 555',
        campType: 'Domos Geodésicos Glamping frente al glaciar en Soraypampa (3,900m) y Ecolodges en ceja de selva'
    };
}

function buildSmartContextFallback(message, history, profile) {
    const q = String(message || '')
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '');

    const route = detectActiveRoute(message, history);
    const lastBotMsg = Array.isArray(history)
        ? [...history].reverse().find(m => m.role === 'assistant')?.content || ''
        : '';

    // 0. GOCTA / CHACHAPOYAS / AMAZONAS / SELVA
    if (q.includes('gocta') || q.includes('chachapoyas') || q.includes('kuelap') || q.includes('amazonas') || q.includes('cocachimba')) {
        return `¡La **Catarata de Gocta (771 metros)** en **Chachapoyas (Amazonas)** es una de las joyas de selva alta y bosque de neblina más espectaculares del Perú!\n\n` +
            `Operamos dos formatos en la zona:\n` +
            `• **Trekking Catarata de Gocta Full Day (S/ 190):** Caminata de 5.5 horas (ida y vuelta) desde Cocachimba o ruta integral desde San Pablo de Valera atravesando cañaverales y bosque nuboso (hábitat del gallito de las rocas y el colibrí cola de espátula), almuerzo regional y guía local.\n` +
            `• **Expedición Amazonas, Gocta & Kuélap (3D/2N - S/ 890):** Incluye Gocta con alojamiento en Eco-Lodge frente a la catarata, teleférico a la fortaleza preínca de **Kuélap** y los **Sarcófagos de Karajía**.\n\n` +
            `¿Te gustaría hacer solo el trekking de 1 día a la catarata de Gocta o el paquete completo de 3 días por Chachapoyas?`;
    }

    if (q.includes('selva') || q.includes('iquitos') || q.includes('pacaya') || q.includes('tambopata') || q.includes('puerto maldonado')) {
        return `En la **Selva del Perú** operamos tres grandes expediciones según el tipo de aventura que busques:\n\n` +
            `• **Selva Alta (Chachapoyas - Amazonas):** Trekking a la **Catarata de Gocta (771m)** y fortaleza de **Kuélap** (3D/2N, S/ 890).\n` +
            `• **Selva Baja Norte (Iquitos):** **Reserva Nacional Pacaya Samiria (5D/4N, S/ 1,650)** navegando entre delfines rosados y caimanes.\n` +
            `• **Selva Sur (Puerto Maldonado - conexión directa desde Cusco):** **Reserva Tambopata & Lago Sandoval (3D/2N, S/ 950)** con la collpa de guacamayos más grande del mundo.\n\n` +
            `¿Cuál de estas tres zonas de selva te llama más la atención explorar?`;
    }

    // 1. ¿QUÉ INCLUYE LA EXPEDICIÓN?
    if (
        q.includes('incluye') ||
        q.includes('domo') ||
        q.includes('glamping') ||
        q.includes('servicio') ||
        q.includes('alojamiento') ||
        q.includes('comida') ||
        q.includes('alimentacion') ||
        q.includes('beneficio')
    ) {
        return `En **${route.shortName}** (${route.region}) incluimos toda la logística de principio a fin:\n\n` +
            `• **Alojamiento:** ${route.campType}.\n` +
            `• **Alimentación Completa:** Desayunos energéticos, almuerzos, cenas calientes y snacks de ruta (con opciones vegetarianas/veganas).\n` +
            `• **Logística y Entradas:** Todos los boletos de ingreso oficiales, transporte turístico privado y guía especializado certificado.\n` +
            `• **Seguridad:** Botiquín WFR de primeros auxilios, comunicación de ruta y acompañamiento permanente.\n\n` +
            `¿Te gustaría revisar las **fechas disponibles** o ver las **tarifas y opciones de reserva** para ${route.shortName}?`;
    }

    // 2. INFORMACIÓN DE TOURS EN CUSCO / CATÁLOGO DE RUTAS
    if (
        q.includes('tours en cusco') ||
        q.includes('tour en cusco') ||
        q.includes('informacion de tour') ||
        q.includes('que tours') ||
        q.includes('que rutas') ||
        q.includes('cuales son') ||
        q.includes('catalogo') ||
        q.includes('opciones de tour') ||
        q.includes('otra ruta') ||
        q.includes('otras rutas') ||
        q.includes('alternativa') ||
        (q.includes('cusco') && (q.includes('tour') || q.includes('ruta') || q.includes('informacion') || q.includes('aventura') || q.includes('hacer')))
    ) {
        return `En **Cusco** operamos dos categorías de experiencias según los días que tengas disponibles:\n\n` +
            `**🏔️ Expediciones Multidía (Alta Montaña & Glamping):**\n` +
            `• **Salkantay Trek & Domos Glamping (4D/3N):** Laguna Humantay, noche en Domos frente al glaciar, paso de 4,630m sin multitudes y cierre en **Machu Picchu**.\n` +
            `• **Ausangate & 7 Lagunas (6D/5N):** Paisajes alpinos puros a 5,000m, aguas termales de Pacchanta y comunidades alpaqueras.\n` +
            `• **Choquequirao Legendario (4D/3N)** y **Camino Inca Clásico (4D/3N)**.\n\n` +
            `**⚡ Rutas de 1 Día (Ideales para aclimatación):**\n` +
            `• **Montaña de 7 Colores & Valle Rojo Pro** (salida temprana sin multitudes) y **Laguna Humantay**.\n\n` +
            `¿Buscas una travesía de varios días que llegue a Machu Picchu o prefieres excursiones de 1 día desde la ciudad de Cusco?`;
    }

    // 3. PRECIOS / TARIFAS / CUÁNTO CUESTA / RESERVA
    if (
        q.includes('precio') ||
        q.includes('cuanto cuesta') ||
        q.includes('costo') ||
        q.includes('tarifa') ||
        q.includes('valor') ||
        q.includes('cotiza') ||
        q.includes('presupuesto') ||
        q.includes('pagar') ||
        q.includes('reservar')
    ) {
        return `Para **${route.name}** manejamos tarifas todo incluido transparentes:\n\n` +
            `• **Tarifa Expedición Base:** **${route.priceBase}** por persona (incluye guía oficial, alojamiento en ruta, alimentación, entradas y transporte).\n` +
            `• **Paquete All-Inclusive Pro:** **${route.priceAllInc}** por persona (suma equipamiento técnico completo y seguro de aventura).\n\n` +
            `Puedes bloquear tu cupo hoy mismo con solo el **30% (${route.reserva30})** y cancelar el 70% restante antes de iniciar la ruta. ¿Para cuántas personas te gustaría cotizar?`;
    }

    // 4. FECHAS / DISPONIBILIDAD / MESES / CUÁNDO SALEN
    if (
        q.includes('fecha') ||
        q.includes('disponib') ||
        q.includes('cuando') ||
        q.includes('salid') ||
        q.includes('diciembre') ||
        q.includes('enero') ||
        q.includes('febrero') ||
        q.includes('marzo') ||
        q.includes('abril') ||
        q.includes('mayo') ||
        q.includes('junio') ||
        q.includes('julio') ||
        q.includes('agosto') ||
        q.includes('septiembre') ||
        q.includes('octubre') ||
        q.includes('noviembre') ||
        q.includes('calendario')
    ) {
        return `Para **${route.shortName}** tenemos **salidas diarias confirmadas durante todo el año** a partir de 2 viajeros, tanto en **grupo reducido (máx. 8 personas por guía)** como en formato **Privado VIP**.\n\n` +
            `¿En qué mes o fechas aproximadas tienen pensado viajar y cuántos integrantes serían?`;
    }

    // 5. ACLIMATACIÓN / ALTURA / SOROCHE / SEGURIDAD MÉDICA / DIFICULTAD
    if (
        q.includes('altura') ||
        q.includes('aclimat') ||
        q.includes('soroche') ||
        q.includes('oxigeno') ||
        q.includes('medico') ||
        q.includes('seguridad') ||
        q.includes('dificultad') ||
        q.includes('fisico') ||
        q.includes('principiante')
    ) {
        return `En **${route.shortName}** (altitud máxima: ${route.maxAltitude}) cuidamos tu experiencia con guías certificados WFR (Wilderness First Responder), monitoreo de signos vitales en ruta y ritmo adaptado a tu grupo.\n\n` +
            `Si vienes a rutas sobre los 3,500 metros (como Cusco o Huaraz), te recomendamos 2 días previos de aclimatación suave. ¿Qué nivel de caminata suelen hacer o con quiénes viajas?`;
    }

    // 6. EQUIPAJE / MOCHILA / DUFFLE BAG 7 KG / EQUIPO / ALQUILER
    if (
        q.includes('equipaje') ||
        q.includes('mochila') ||
        q.includes('llevar') ||
        q.includes('peso') ||
        q.includes('duffle') ||
        q.includes('ropa') ||
        q.includes('alquiler') ||
        q.includes('equipo') ||
        q.includes('bota') ||
        q.includes('saco')
    ) {
        return `Para **${route.shortName}** solo necesitas caminar con una **mochila ligera de día (20-25L)** con agua, bloqueador, impermeable y cámara.\n\n` +
            `En nuestras travesías de varios días te entregamos un **Duffle Bag para hasta 7 kg** que trasladamos por ti entre campamentos. Además, contamos con alquiler de calzado Gore-Tex, bastones de carbono y casacas térmicas. ¿Ya cuentas con tus implementos de trekking?`;
    }

    // 7. RUTAS ESPECÍFICAS ADICIONALES
    if (q.includes('ausangate')) {
        return `El **Circuito Ausangate & 7 Lagunas Glamping (6D/5N)** es la joya de alta montaña en Cusco: rodeamos el nevado sagrado Ausangate (6,384m), cruzamos pasos como Palomani (5,100m) y nos relajamos en las **aguas termales de Pacchanta** frente a los glaciares.\n\n¿Para qué mes estás planeando Ausangate y cuántos viajeros serían?`;
    }
    if (q.includes('choquequirao')) {
        return `**Choquequirao Expedición Legendaria (4D/3N)** te lleva a la "Cuna de Oro" de los Incas sobre el Cañón del Apurímac, una ciudadela monumental sin turismo masivo.\n\nOperamos con arrieros y mulas para tu **Duffle Bag de 7 kg**, campamentos privados y guías certificados. ¿Qué fechas tienes en mente para esta expedición?`;
    }
    if (q.includes('huaraz') || q.includes('santa cruz') || q.includes('laguna 69') || q.includes('mateo')) {
        return `En la **Cordillera Blanca (Huaraz)** operamos el **Trekking Santa Cruz (4D/3N)** cruzando Punta Unión (4,750m), el full day a **Laguna 69** y el ascenso glaciar al **Nevado Mateo (5,150m)** con todo el equipo técnico de alpinismo incluido.\n\n¿Te atrae más una caminata escénica entre lagunas turquesas o coronar tu primera cumbre glaciar?`;
    }
    if (q.includes('arequipa') || q.includes('colca') || q.includes('misti')) {
        return `En **Arequipa** operamos el **Trekking al Cañón del Colca (3D/2N, S/ 630)** descendiendo hasta el Oasis de Sangalle y el **Ascenso al Volcán Misti (5,825m en 2D/1N, S/ 880)** con guías de alta montaña UIAGM.\n\n¿Prefieres caminata por cañón y aguas termales o cumbre volcánica?`;
    }

    // 8. ANTI-REPETICIÓN
    if (lastBotMsg.includes('Salkantay') || lastBotMsg.includes('ruta favorita')) {
        return `En **Lifextreme Perú** operamos expediciones en **Cusco** (Salkantay, Ausangate, Choquequirao, Camino Inca), **Huaraz** (Santa Cruz, Laguna 69, Nevado Mateo), **Amazonas** (Catarata de Gocta y Kuélap), **Iquitos / Tambopata** (Selva Amazónica) y **Arequipa** (Colca y Volcán Misti).\n\n¿Qué región del Perú o qué tipo de aventura (montaña, selva o costa) te gustaría explorar?`;
    }

    return `En **Lifextreme Perú** diseñamos expediciones en **Cusco** (Salkantay Glamping, Ausangate 7 Lagunas, Choquequirao), **Amazonas / Selva** (Catarata de Gocta, Pacaya Samiria, Tambopata), **Huaraz** (Santa Cruz, Nevado Mateo) y **Arequipa** (Colca y Misti).\n\nCuéntame: ¿qué destino del Perú te gustaría conocer y cuántos días tienes planeados para tu viaje?`;
}

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
        const groqModel = (process.env.GROQ_MODEL || 'openai/gpt-oss-120b').trim();
        const geminiKey = (process.env.GEMINI_API_KEY || '').trim();
        const qdrantTunnelUrl = (process.env.QDRANT_TUNNEL_URL || '').replace(/\/$/, '');

        // 0. REGISTRO DIRECTO DE RESERVAS EN BACKEND QDRANT
        if (action === 'register_booking' && booking) {
            if (qdrantTunnelUrl) {
                try {
                    const regRes = await fetchWithTimeout(`${qdrantTunnelUrl}/api/v1/agents/bookings/register`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(booking)
                    }, 4000);
                    if (regRes.ok) {
                        const regData = await regRes.json();
                        return res.status(200).json({ ok: true, booking: regData });
                    }
                } catch (_) {}
            }
            return res.status(200).json({ ok: true, booking });
        }

        // 1. PRIORIDAD 1: Puente directo a Cerebro Vectorial Qdrant (si QDRANT_TUNNEL_URL está configurado y activo)
        if (qdrantTunnelUrl) {
            try {
                const qdrantRes = await fetchWithTimeout(`${qdrantTunnelUrl}/webhook/lifextreme`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message, history, profile })
                }, 3500);
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
            } catch (_) {}
        }

        const hasBooking = Boolean(profile && profile.booking_code) || /\bLX-[A-Z0-9]{4,10}\b/i.test(message);
        const activeRoute = detectActiveRoute(message, history);
        const roleDirective = hasBooking
            ? `El usuario YA TIENE UNA RESERVA CONFIRMADA (${profile.booking_code || 'Activa'}). Atiéndelo como su Concierge Post-Venta.`
            : `Destino/ruta detectado en la consulta actual: ${activeRoute.name} (${activeRoute.region}). Responde directamente sobre el destino que consulta el usuario sin desviarte a otra ruta.`;

        const systemPrompt = `${SYSTEM_PROMPT_BASE}\n\nCONTEXTO ACTUAL DE LA SESIÓN:\n${roleDirective}`;

        const cleanHistory = Array.isArray(history)
            ? history.slice(-8).map(m => ({
                role: m.role === 'user' ? 'user' : 'assistant',
                content: String(m.content || '').slice(0, 800)
            }))
            : [];

        const messages = [
            { role: 'system', content: systemPrompt },
            ...cleanHistory,
            { role: 'user', content: String(message) }
        ];

        // 2. PRIORIDAD 2: Groq Cloud LPU (modelos actuales 2026: openai/gpt-oss-120b, qwen/qwen3.8-27b, openai/gpt-oss-20b)
        if (groqKey) {
            const candidateGroqModels = [groqModel, 'openai/gpt-oss-120b', 'qwen/qwen3.8-27b', 'openai/gpt-oss-20b'];
            const uniqueModels = [...new Set(candidateGroqModels)];
            for (const mdl of uniqueModels) {
                try {
                    const groqRes = await fetchWithTimeout('https://api.groq.com/openai/v1/chat/completions', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${groqKey}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            model: mdl,
                            messages,
                            temperature: 0.35,
                            max_tokens: 400
                        })
                    }, 6500);

                    if (groqRes.ok) {
                        const data = await groqRes.json();
                        const reply = data.choices?.[0]?.message?.content?.trim() || '';
                        if (reply) {
                            return res.status(200).json({ mensaje: reply, source: `groq_${mdl}` });
                        }
                    }
                } catch (_) {}
            }
        }

        // 3. PRIORIDAD 3: Google Gemini API (si GEMINI_API_KEY es válida)
        if (geminiKey) {
            try {
                const geminiContents = [
                    { role: 'user', parts: [{ text: `INSTRUCCIONES DEL SISTEMA:\n${systemPrompt}` }] },
                    { role: 'model', parts: [{ text: 'Entendido. Responderé como MAX de Lifextreme Perú sobre el destino exacto consultado.' }] },
                    ...cleanHistory.map(m => ({
                        role: m.role === 'user' ? 'user' : 'model',
                        parts: [{ text: m.content }]
                    })),
                    { role: 'user', parts: [{ text: String(message) }] }
                ];

                const gemRes = await fetchWithTimeout(
                    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${geminiKey}`,
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            contents: geminiContents,
                            generationConfig: { temperature: 0.35, maxOutputTokens: 400 }
                        })
                    },
                    6000
                );

                if (gemRes.ok) {
                    const gemData = await gemRes.json();
                    const reply = gemData.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || '';
                    if (reply) {
                        return res.status(200).json({ mensaje: reply, source: 'gemini_flash' });
                    }
                }
            } catch (_) {}
        }

        // 4. PRIORIDAD 4: Cloud OpenAI-Compatible Inference (Keyless Cloud LLM Fallback)
        try {
            const cloudRes = await fetchWithTimeout('https://text.pollinations.ai/openai', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: 'openai',
                    messages,
                    temperature: 0.35
                })
            }, 6500);

            if (cloudRes.ok) {
                const cloudData = await cloudRes.json();
                const reply = cloudData.choices?.[0]?.message?.content?.trim() || '';
                if (reply && reply.length > 25 && !reply.toLowerCase().includes('rate limit')) {
                    return res.status(200).json({ mensaje: reply, source: 'cloud_llm' });
                }
            }
        } catch (_) {}

        // 5. PRIORIDAD 5: Motor Conversacional Contextual Multi-Destino
        const fallbackReply = buildSmartContextFallback(message, history, profile);
        return res.status(200).json({ mensaje: fallbackReply, source: 'context_domain_v3' });

    } catch (err) {
        const safeReply = buildSmartContextFallback(req.body?.message || '', req.body?.history || [], {});
        return res.status(200).json({ mensaje: safeReply, source: 'emergency_fallback' });
    }
}
