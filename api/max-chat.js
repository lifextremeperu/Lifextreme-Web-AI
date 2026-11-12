// ==============================================================================
// LIFEXTREME MAX AI — Conversational Assistant & Multiagent Orchestrator (Vercel)
// Motor Híbrido Multi-LLM (Qdrant RAG -> Groq LPU -> Gemini -> Cloud LLM -> Context Engine)
// Con memoria conversacional, anti-repetición y cobertura total de intenciones.
// ==============================================================================

const SYSTEM_PROMPT_BASE = `Eres MAX 🏔️, el especialista en alta montaña, expediciones y logística de Lifextreme Perú (certificado UIAGM / WFR), operando desde Cusco para todo el Perú.

REGLAS DE COHERENCIA Y ESTILO (OBLIGATORIAS):
1. RESPONDE DIRECTAMENTE A LA PREGUNTA EXACTA DEL USUARIO en la primera frase. Nunca repitas una respuesta anterior del historial.
2. Si el usuario pide "información de tours en Cusco" o qué rutas tienen, preséntale un panorama claro de las rutas principales en Cusco (Salkantay Glamping 4D, Ausangate 7 Lagunas 6D, Choquequirao 4D, Camino Inca 4D, Vinicunca y Laguna Humantay) con sus diferencias clave.
3. Si el usuario pregunta "¿Qué incluye la expedición y los domos?", detalla qué incluye exactamente: Domos Geodésicos Glamping en Soraypampa con aislamiento térmico y baño/ducha caliente, alimentación completa gourmet de montaña (desayuno, almuerzo, cena y snacks energéticos), Duffle Bag de 7 kg porteado por arrieros (Ley N° 31614), guía certificado UIAGM/WFR con monitoreo de oximetría 2 veces al día, oxígeno medicinal, entradas a Machu Picchu, tren de retorno y transporte completo.
4. Mantén un tono cálido, experto, conciso y natural (máximo 2 a 3 párrafos cortos o viñetas limpias, entre 70 y 130 palabras).
5. Cierra con UNA pregunta consultiva relevante que ayude a avanzar según lo que el usuario acaba de preguntar (sin repetir preguntas ya hechas en el historial).

CATÁLOGO Y DATOS OFICIALES VERIFICADOS DE LIFEXTREME PERÚ:
• CUSCO — Travesías Multidía:
  1. Salkantay Trek & Domos Glamping a Machu Picchu (4D/3N o 5D/4N): Paso Abra Salkantay (4,630 msnm), Laguna Humantay, noche en Domos Geodésicos en Soraypampa (3,900m), desfase horario (salimos 90 min antes sin multitudes) y cierre en Machu Picchu. Tarifa base: S/ 1,630 (Paquete All-Inclusive: S/ 1,850).
  2. Circuito Ausangate & 7 Lagunas Glamping (6D/5N): Alta montaña pura rodeando el Apu Ausangate (6,384m), pasos sobre 5,000m (Palomani), 7 Lagunas de Pacchanta, aguas termales y cero masificación. Tarifa base: S/ 1,880 (All-Inclusive: S/ 2,100).
  3. Choquequirao Expedición Legendaria (4D/3N): Cañón del Apurímac y la ciudadela inca hermana de Machu Picchu con menos del 1% de visitantes. Tarifa base: S/ 2,980.
  4. Camino Inca Clásico a Machu Picchu (4D/3N): Ingreso directo por Inti Punku (Puerta del Sol), cumplimiento auditado de la Ley del Porteador N° 31614. Tarifa base: S/ 2,230.
• CUSCO — Rutas de 1 Día (Aclimatación y Aventura):
  5. Montaña de 7 Colores (Vinicunca) & Valle Rojo Pro (1 Día): Salida temprana anti-multitudes (03:30 am), desayuno y almuerzo buffet, oxígeno médico a bordo. S/ 230.
  6. Laguna Humantay & Soraypampa (1 Día): Caminata escénica a 4,200 msnm al pie del glaciar Humantay. S/ 230.
  7. Valle Sagrado VIP / Maras Moray en Cuatrimotos / Vía Ferrata & Zipline: Ideales para los primeros 2 días de aclimatación en Cusco.
• OTRAS REGIONES DEL PERÚ:
  - Huaraz (Cordillera Blanca): Trekking Santa Cruz (4D/3N, S/ 980), Laguna 69 (1D) y Cumbre Glaciar Nevado Mateo 5,150m (1D, S/ 380 con crampones, piolet y casco Petzl/Grivel).
  - Arequipa: Trekking Cañón del Colca 3D/2N (S/ 630) y Ascenso Volcán Misti 5,825m 2D/1N (S/ 880).
  - Amazonía (Iquitos): Expedición Reserva Nacional Pacaya Samiria 5D/4N (S/ 1,650).
  - Lima: Parapente Costa Verde Miraflores (S/ 260) y Rafting/Canopy en Lunahuaná (S/ 220).
• QUÉ INCLUYEN NUESTRAS EXPEDICIONES:
  - Alojamiento de Montaña: Domos Geodésicos Glamping en Soraypampa y campamentos térmicos 4 estaciones (carpas comedor calefaccionadas y colchones aislantes de alta densidad).
  - Alimentación Completa: Chefs de montaña especializados (desayunos proteicos, almuerzos, cenas calientes, hora del té y opciones vegetarianas/veganas/celíacas sin costo extra).
  - Equipaje Libre de Carga (Duffle Bag 7 kg - Ley N° 31614): Entregamos un Duffle Bag la noche previa en el briefing en Cusco para hasta 7 kg (ropa y saco de dormir), transportado por nuestros arrieros y mulas con pesaje digital certificado. El viajero solo lleva su mochila de día (20-25L).
  - Protocolo Médico y Seguridad: Guías certificados UIAGM/AGMP y WFR (Wilderness First Responder), control de oximetría (SpO2) y pulso 2 veces al día, balón de oxígeno medicinal portátil, comunicación satelital y sesiones de recuperación muscular en campamento (botas de compresión y pediluvios botánicos).
  - Logística Machu Picchu: Boleto oficial Llaqta Machu Picchu, bus Consettur subida/bajada, tren turístico de retorno a Ollantaytambo y traslado privado a tu hotel en Cusco.
• FECHAS Y RESERVAS:
  - Salidas diarias confirmadas todo el año (incluyendo todo diciembre, Navidad y Año Nuevo) a partir de 2 viajeros, en grupos reducidos (máx. 8 personas por guía) o en servicio Privado.
  - Sistema de Reserva Flexible 30/70: Se bloquea el cupo y permisos hoy con el 30% y el 70% restante se abona en Cusco antes de partir.`;

async function fetchWithTimeout(url, options, timeoutMs = 4500) {
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
            campType: 'Campamentos privados en el Cañón del Apurímac (Chiquisca y Marampata)'
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
            campType: 'Full Day con salida temprana anti-multitudes (03:30 am) y restaurante andino buffet'
        };
    }
    if (combined.includes('humantay') && !combined.includes('salkantay') && !combined.includes('4d') && !combined.includes('4 días')) {
        return {
            name: 'Laguna Humantay & Soraypampa Pro (1 Día)',
            shortName: 'Laguna Humantay (1 Día)',
            region: 'Cusco',
            maxAltitude: '4,200 msnm (Laguna Humantay)',
            priceBase: 'S/ 230',
            priceAllInc: 'S/ 450',
            reserva30: 'S/ 135',
            campType: 'Full Day con desayuno y almuerzo en Soraypampa'
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
    // Por defecto Salkantay
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

    // 1. ¿QUÉ INCLUYE LA EXPEDICIÓN Y LOS DOMOS? (¡Crucial para el chip "✨ ¿Qué incluye?"!)
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
        return `En **${route.shortName}** incluimos toda la logística de principio a fin para que solo te concentres en disfrutar la montaña:\n\n` +
            `• **Alojamiento & Domos:** ${route.campType}, con camas térmicas y duchas calientes.\n` +
            `• **Alimentación Completa:** Chefs de montaña (desayunos energéticos, almuerzos, cenas calientes, hora del té y opciones vegetarianas/veganas).\n` +
            `• **Equipaje Libre (Duffle Bag 7 kg):** Nuestros arrieros llevan hasta 7 kg de tu equipaje (Ley N° 31614); tú solo caminas con una mochila ligera.\n` +
            `• **Entradas, Tren y Seguridad:** Boleto a Machu Picchu (en rutas hacia la Llaqta), tren de retorno, transporte completo y guía UIAGM/WFR con control de oxígeno 2 veces al día.\n\n` +
            `¿Te gustaría conocer cómo manejamos la **aclimatación a la altura** o prefieres ver los **precios y cómo separar tu cupo**?`;
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
        return `Para **${route.name}** manejamos dos modalidades transparentes:\n\n` +
            `• **Tarifa Expedición Base (${route.priceBase} por persona):** Incluye guía UIAGM/WFR, domos/campamentos, alimentación completa, Duffle Bag de 7 kg con arrieros, entradas y transporte.\n` +
            `• **Paquete All-Inclusive Pro (${route.priceAllInc} por persona):** Suma todo el equipo técnico (botas Gore-Tex, bastones de carbono, casaca térmica), asistencia médica de altura y seguro extremo.\n\n` +
            `Puedes bloquear tu cupo y permisos oficiales hoy mismo con solo el **30% (${route.reserva30})** y pagar el 70% restante al llegar a Cusco. ¿Para cuántas personas te gustaría cotizar?`;
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
        return `Para **${route.shortName}** tenemos **salidas diarias confirmadas durante todo el año** (incluyendo feriados, Navidad y Año Nuevo) a partir de 2 viajeros, tanto en **grupo reducido (máx. 8 personas por guía)** como en formato **Privado VIP**.\n\n` +
            `*Nota importante:* La única ruta que cierra en febrero por mantenimiento anual de SERNANP es el Camino Inca Clásico; **Salkantay, Ausangate y Humantay operan los 12 meses**. ¿En qué mes o quincena tienen pensado viajar?`;
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
        return `En **${route.shortName}** (altitud máxima: ${route.maxAltitude}) cuidamos tu adaptación con nuestro protocolo de medicina de montaña:\n\n` +
            `1. **Antes del trek:** Te recomendamos pasar **2 días previos en Cusco o el Valle Sagrado** haciendo caminatas suaves.\n` +
            `2. **Durante la ruta:** Nuestros guías WFR miden tu **saturación de oxígeno (SpO₂) y pulso 2 veces al día**, llevamos balón de oxígeno medicinal portátil y caballos de emergencia.\n` +
            `3. **En campamento:** Realizamos sesiones de descarga muscular con botas de compresión y pediluvios calientes.\n\n` +
            `¿Ya has estado antes sobre los 3,400 metros de altitud o sería tu primera experiencia en los Andes?`;
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
        return `Caminarás súper ligero gracias a nuestro sistema **Duffle Bag 7 kg (Ley N° 31614)**:\n\n` +
            `• En el briefing la noche previa en Cusco te entregamos una maleta **Duffle Bag donde guardas hasta 7 kg** (tu ropa de cambio, abrigo y saco de dormir). Nuestros arrieros la llevan de campamento en campamento.\n` +
            `• Tú solo caminas con una **mochila pequeña de 20-25L** (agua, bloqueador, cámara y casaca cortaviento).\n` +
            `• Si te falta algún implemento (botas Gore-Tex, bastones de carbono o saco de pluma -15°C), contamos con **alquiler Pro higienizado en Cusco**.\n\n` +
            `¿Ya cuentas con tu propio calzado de trekking o prefieres incluir nuestro Kit de Equipo Pro?`;
    }

    // 7. CLIMA / MEJOR ÉPOCA / LLUVIA / FRÍO
    if (
        q.includes('clima') ||
        q.includes('lluvia') ||
        q.includes('frio') ||
        q.includes('temperatura') ||
        q.includes('epoca') ||
        q.includes('temporada') ||
        q.includes('tiempo')
    ) {
        return `En los Andes de Cusco tenemos dos temporadas bien marcadas:\n\n` +
            `• **Temporada Seca (Abril a Octubre):** Días soleados y cielos despejados azules, con noches frías en altura (-5°C a 0°C).\n` +
            `• **Temporada Verde / Lluvias (Noviembre a Marzo):** Montañas intensamente verdes, temperaturas nocturnas más templadas y menos viajeros en ruta. Como en **Salkantay dormimos en Domos Geodésicos cerrados e impermeables**, estás 100% protegido.\n\n` +
            `¿En qué época del año te gustaría vivir la experiencia?`;
    }

    // 8. RUTAS ESPECÍFICAS
    if (q.includes('ausangate')) {
        return `El **Circuito Ausangate & 7 Lagunas Glamping (6D/5N)** es la joya de alta montaña en Cusco: rodeamos el nevado sagrado Ausangate (6,384m), cruzamos pasos como Palomani (5,100m) y nos relajamos en las **aguas termales de Pacchanta** frente a los glaciares.\n\nIncluye campamentos térmicos 4 estaciones, alimentación completa, **Duffle Bag de 7 kg** porteado por arrieros y monitoreo de oximetría diario. ¿Para qué mes estás planeando Ausangate y cuántos viajeros serían?`;
    }
    if (q.includes('choquequirao')) {
        return `**Choquequirao Expedición Legendaria (4D/3N)** te lleva a la "Cuna de Oro" de los Incas sobre el Cañón del Apurímac, una ciudadela monumental donde aún el 70% permanece oculto en la vegetación y sin turismo masivo.\n\nOperamos con arrieros y mulas para tu **Duffle Bag de 7 kg**, campamentos privados y guías certificados. ¿Qué fechas tienes en mente para esta expedición?`;
    }
    if (q.includes('camino inca') || q.includes('inca trail')) {
        return `El **Camino Inca Clásico (4D/3N)** es la ruta imperial histórica que entra a Machu Picchu directamente por la **Puerta del Sol (Inti Punku)** al amanecer del cuarto día.\n\nGestionamos tu permiso oficial del Ministerio de Cultura y operamos bajo la **Ley del Porteador N° 31614**. Como los cupos estatales se agotan con meses de anticipación, ¿para qué mes te gustaría verificar espacios disponibles?`;
    }
    if (q.includes('vinicunca') || q.includes('7 colores') || q.includes('siete colores') || q.includes('humantay')) {
        return `Nuestras rutas de **1 Día en Cusco (Montaña de 7 Colores + Valle Rojo y Laguna Humantay)** operan bajo modalidad **Offset Trekking**: salimos a las 03:30 am para que llegues al mirador antes que los buses masivos.\n\nIncluyen transporte turístico, desayuno y almuerzo buffet andino, bastones de apoyo, oxígeno médico a bordo y guía oficial (S/ 230 por persona). ¿Te gustaría usarlas como aclimatación antes de un trek más largo o como excursiones principales?`;
    }
    if (q.includes('huaraz') || q.includes('santa cruz') || q.includes('laguna 69') || q.includes('mateo')) {
        return `En la **Cordillera Blanca (Huaraz)** operamos el **Trekking Santa Cruz (4D/3N)** cruzando Punta Unión (4,750m), el full day a **Laguna 69** y el ascenso glaciar al **Nevado Mateo (5,150m)** con todo el equipo técnico de alpinismo incluido.\n\n¿Te atrae más una caminata escénica entre lagunas turquesas o coronar tu primera cumbre glaciar?`;
    }

    // 9. ANTI-REPETICIÓN INTELIGENTE SI EL USUARIO ESCRIBE ALGO CORTO (ej. "hola", "más info", "2 personas", un mes, etc.)
    if (/\b(1|2|3|4|5|6|7|8|dos|tres|cuatro|solo|pareja|familia|amigos)\b/.test(q)) {
        return `¡Excelente! Para un grupo de ese tamaño en **${route.shortName}**, garantizamos atención personalizada (máximo 8 viajeros por guía UIAGM/WFR) o podemos armarlo en formato **100% Privado**.\n\nLa tarifa base es de **${route.priceBase}** por persona (o **${route.priceAllInc}** en el paquete All-Inclusive con equipo técnico completo), y pueden separar sus cupos hoy con el **30% (${route.reserva30})**. ¿Quieres que te muestre el desglose completo para reservar o tienes alguna duda sobre el itinerario día por día?`;
    }

    // Si la última respuesta ya fue la presentación de Salkantay, no repetirla jamás; dar el itinerario día por día
    if (lastBotMsg.includes('Salkantay 4 Días / 3 Noches') || lastBotMsg.includes('travesías más hermosas')) {
        return `Aquí tienes el resumen día por día de nuestra ruta estrella **${route.shortName}**:\n\n` +
            `• **Día 1:** Cusco → Challacancha → ascenso a la **Laguna Humantay (4,200m)** y noche en **Domos Glamping en Soraypampa**.\n` +
            `• **Día 2:** Salida temprana sin multitudes hacia el **Abra Salkantay (4,630m)** y descenso a la ceja de selva en Collpapampa.\n` +
            `• **Día 3:** Sendero tropical por Lucmabamba, cafetales orgánicos y llegada a **Aguas Calientes** (hotel incluido).\n` +
            `• **Día 4:** Visita guiada en **Machu Picchu**, tren panorámico a Ollantaytambo y retorno privado a Cusco.\n\n` +
            `¿Te gustaría revisar qué incluye el paquete o consultar las tarifas y opciones de reserva?`;
    }

    // Presentación inicial consultiva
    return `En **Cusco** nuestra ruta favorita es el **Salkantay Trek & Domos Glamping a Machu Picchu (4D/3N)**: duermes en Domos Geodésicos frente al glaciar en Soraypampa, visitas la Laguna Humantay y llegas a Machu Picchu sin multitudes. También operamos **Ausangate 7 Lagunas (6D)**, **Choquequirao (4D)** y rutas de 1 día como **Vinicunca & Valle Rojo**.\n\n¿Buscas una expedición de varios días hacia Machu Picchu o prefieres rutas cortas de 1 día desde Cusco?`;
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
                }, 4000);
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
            ? `El usuario YA TIENE UNA RESERVA CONFIRMADA (${profile.booking_code || 'Activa'}). Atiéndelo como su Concierge Post-Venta (aclimatación médica, Duffle Bag de 7 kg, itinerario).`
            : `Ruta actualmente en contexto: ${activeRoute.name}. El usuario está consultando en la web. Responde exactamente su pregunta de forma consultiva y coherente con el historial.`;

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

        // 2. PRIORIDAD 2: Groq LPU (llama-3.3-70b-versatile)
        if (groqKey) {
            try {
                const groqRes = await fetchWithTimeout('https://api.groq.com/openai/v1/chat/completions', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${groqKey}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        model: 'llama-3.3-70b-versatile',
                        messages,
                        temperature: 0.4,
                        max_tokens: 400
                    })
                }, 7000);

                if (groqRes.ok) {
                    const data = await groqRes.json();
                    const reply = data.choices?.[0]?.message?.content?.trim() || '';
                    if (reply) {
                        return res.status(200).json({ mensaje: reply, source: 'groq_lpu' });
                    }
                }
            } catch (_) {}
        }

        // 3. PRIORIDAD 3: Google Gemini API (gemini-2.0-flash)
        if (geminiKey) {
            try {
                const geminiContents = [
                    { role: 'user', parts: [{ text: `INSTRUCCIONES DEL SISTEMA:\n${systemPrompt}` }] },
                    { role: 'model', parts: [{ text: 'Entendido. Responderé como MAX de Lifextreme Perú de forma directa, coherente y sin repetir respuestas.' }] },
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
                            generationConfig: { temperature: 0.4, maxOutputTokens: 400 }
                        })
                    },
                    7000
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
                    temperature: 0.4
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

        // 5. PRIORIDAD 5: Motor Conversacional Contextual y Anti-Repetición de Dominio
        const fallbackReply = buildSmartContextFallback(message, history, profile);
        return res.status(200).json({ mensaje: fallbackReply, source: 'context_domain_v2' });

    } catch (err) {
        const safeReply = buildSmartContextFallback(req.body?.message || '', req.body?.history || [], {});
        return res.status(200).json({ mensaje: safeReply, source: 'emergency_fallback' });
    }
}
