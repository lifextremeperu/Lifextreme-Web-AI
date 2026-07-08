// --- DATA (MODULARIZED V29) ---

const tours = [
    // CUSCO (5)
    {
        id: 1,
        title: 'Camino Inca a Machu Picchu 4D',
        dept: 'Cusco',
        price: 2450,
        duration: '4 días',
        difficulty: 'Alta',
        img: 'https://images.unsplash.com/photo-1587547131116-a0655a526190',
        detail: 'El "Holy Grail" del trekking. La ruta más famosa de América hacia Machu Picchu.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Camino Inca a Machu Picchu de 4 días tiene una dificultad alta y un precio desde $2,450. Se recorren 43 km alcanzando los 4,215 msnm. Requiere reserva con 6 meses de anticipación por normas gubernamentales. La mejor temporada es de mayo a octubre (temporada seca).',
        faqs: [
            { q: '¿Con cuánta anticipación debo reservar?', a: 'Por regulaciones del gobierno peruano (solo 500 cupos diarios), se requiere reservar con al menos 6 meses de antelación.' },
            { q: '¿Qué tan difícil es el Camino Inca?', a: 'Es de dificultad alta. El Día 2 incluye un ascenso prolongado hasta los 4,215 metros sobre el nivel del mar.' },
            { q: '¿Están incluidas las entradas a Machu Picchu?', a: 'Sí, el paquete incluye los permisos del Camino Inca, el ingreso a la ciudadela y el tren de retorno.' },
            { q: '¿Qué hacer con el mal de altura?', a: 'Nuestros guías llevan oxígeno portátil. Es obligatorio aclimatarse en Cusco al menos 2 días antes del inicio.' },
            { q: '¿Qué equipo de campamento proveen?', a: 'Proveemos carpas de montaña para 4 estaciones, colchonetas y todo el equipo de comedor.' }
        ],
        genInfo: {
            cancelPolicy: 'Actividad no reembolsable (Regulación de Gobierno)',
            duration: '4 días / 3 noches',
            availability: 'Requiere reserva con 6 meses de anticipación',
            guide: 'Inglés, Español',
            groupSize: 'Máximo 9 participantes'
        },
        whatYouDo: [
            'Caminata por el original Qhapaq Ñan (Camino Inca)',
            'Exploración de ruinas intactas en el bosque nuboso',
            'Despertar en campamentos con vista a nevados',
            'Entrada triunfal a Machu Picchu por la Puerta del Sol (Inti Punku)'
        ],
        fullItinerary: [
            { day: 1, desc: 'Día 1: El Paso de los Incas. Inicio en el Km 82. Caminata por el valle del río Urubamba hasta llegar al campamento de Wayllabamba.' },
            { day: 2, desc: 'Día 2: El Desafío del Dead Woman\'s Pass. Ascenso letal a 4,215 msnm. El día más duro pero más gratificante. Descenso al valle de Pacaymayo.' },
            { day: 3, desc: 'Día 3: Viaje en el Tiempo. Caminata por la selva nubosa pasando por ruinas intactas (Runkurakay, Sayacmarca, Wiñay Wayna). El día visualmente más hermoso.' },
            { day: 4, desc: 'Día 4: La Puerta del Sol. Despertar a las 3:30 AM para cruzar la Puerta del Sol (Inti Punku) y ver el amanecer sobre Machu Picchu. Retorno a Cusco en tren.' }
        ],
        inc: [
            'Ticket de ingreso oficial al Camino Inca y Machu Picchu',
            'Guía profesional bilingüe experto en historia Inca',
            'Porteros para el equipo de campamento y comida',
            '3 desayunos / 3 almuerzos / 3 cenas de alta montaña',
            'Equipos de campamento (Carpas, colchonetas)',
            'Tren de retorno a Ollantaytambo y bus a Cusco'
        ],
        notSuitable: ['Embarazadas', 'Personas con problemas de espalda', 'Personas con movilidad reducida'],
        meetingPoint: 'Plaza Mayor de Cuzco (Briefing 1 día antes)',
        importantInfo: 'Llevar pasaporte original (Obligatorio en controles del gobierno), botas impermeables y sleeping bag de plumas.',
        steps: [{ n: 'G', t: 'Km 82', d: 'Inicio' }, { n: 'ri-map-pin-2-fill', t: 'Inti Punku', d: 'Amanecer' }, { n: 'dot', t: 'Machu Picchu', d: 'Final' }],
        sensoryVariants: {
            landscape: 'Siente la energía ancestral bajo tus pies mientras la neblina se levanta y revela la ciudad sagrada ante tus ojos.',
            comfort: 'Disfruta de comida gourmet preparada por nuestros chefs en medio de las montañas más remotas de los Andes.',
            action: 'Conquista el paso de la Mujer Muerta a 4,215m y demuestra que tu cuerpo y mente no tienen límites.'
        }
    },
    {
        id: 2,
        title: 'Salkantay Trek a Machu Picchu 4D',
        dept: 'Cusco',
        price: 1850,
        duration: '4 días',
        difficulty: 'Extrema',
        img: 'https://images.unsplash.com/photo-1596395819057-033f7b2c5897',
        detail: 'Ruta de alta montaña por nevados y selva alta (Alternativa al Camino Inca).',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Salkantay Trek a Machu Picchu (4 días) tiene dificultad extrema y cuesta $1,850. Es la mejor alternativa sin reserva previa. Ascenderás hasta el Paso Salkantay (4,600m) cruzando glaciares y descendiendo a la selva tropical. Disponible todo el año, ideal de abril a noviembre.',
        faqs: [
            { q: '¿Necesito reservar con meses de anticipación?', a: 'No, a diferencia del Camino Inca, Salkantay no tiene límite estricto gubernamental. Puedes reservar con poca antelación.' },
            { q: '¿Es más difícil que el Camino Inca?', a: 'Sí, físicamente es más exigente. Se alcanza mayor altitud (4,600m) y las caminatas diarias son más largas.' },
            { q: '¿Las mulas llevan mi mochila?', a: 'Sí, incluimos caballos de carga que llevarán hasta 7kg de tu equipo personal.' },
            { q: '¿Visitamos la Laguna Humantay?', a: 'Absolutamente, el primer día incluye el ascenso a esta icónica laguna glaciar a 4,200m.' },
            { q: '¿Cómo regresamos a Cusco?', a: 'El tour incluye tren Expedition desde Aguas Calientes hasta Ollantaytambo y bus a Cusco.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso parcial hasta 7 días antes',
            duration: '4 días / 3 noches',
            availability: 'Salidas diarias confirmadas',
            guide: 'Inglés, Español, Francés',
            groupSize: 'Máximo 12 participantes'
        },
        whatYouDo: [
            'Conquistar el Abra Salkantay a 4,600 msnm',
            'Visitar la majestuosa Laguna Humantay',
            'Caminata por ceja de selva y plantaciones de café',
            'Exploración de la Ciudadela Inca al amanecer'
        ],
        fullItinerary: [
            { day: 1, desc: 'Día 1: El Desafío Comienza. Recogida a las 4:30 AM, caminata hacia Soraypampa (3,900m) y ascenso a la Laguna Humantay (4,200m). Noche en campamento.' },
            { day: 2, desc: 'Día 2: El Paso del Glaciar. Ascenso de 4 horas al Abra Salkantay (4,600m) frente al nevado. Descenso radical hacia el bosque nuboso en Chaullay.' },
            { day: 3, desc: 'Día 3: Inmersión en la Selva. Trekking rodeados de orquídeas y café hasta Lucmabamba. Caminata por el Camino Inca original hacia Llactapata y tren a Aguas Calientes.' },
            { day: 4, desc: 'Día 4: La Victoria. Exploración guiada de Machu Picchu al amanecer. Por la tarde, retorno a Cusco en tren y bus.' }
        ],
        inc: [
            'Recogida en hotel (04:30 AM)',
            'Guía profesional especializado en montaña',
            'Caballos de carga (7kg personales)',
            '3 desayunos / 3 almuerzos / 3 cenas',
            'Equipo de campamento de alta montaña',
            'Ticket de entrada a Machu Picchu y tren de retorno'
        ],
        notSuitable: ['Menores de 12 años', 'Personas con asma severa', 'Problemas de rodilla'],
        meetingPoint: 'Recepción de su hotel en Cusco',
        importantInfo: 'Llevar botas ya usadas (break-in), ropa térmica para los días 1 y 2, y ropa ligera para la selva.',
        steps: [{ n: 'G', t: 'Mollepata', d: 'Inicio' }, { n: 'ri-mountain-fill', t: 'Paso Salkantay', d: '4,600m' }, { n: 'dot', t: 'Machu Picchu', d: 'Final' }],
        sensoryVariants: {
            landscape: 'Respira la esencia de los glaciares a 4,600m y siente el poder del nevado protegiendo tu camino hacia la selva tropical.',
            comfort: 'Duerme bajo un cielo andino completamente estrellado tras superar el mayor desafío físico de tu viaje.',
            action: 'Supera el Paso Salkantay y siente la adrenalina pura del descenso extremo hacia la amazonía.'
        }
    },
    {
        id: 3,
        title: 'Montaña de los 7 Colores Express',
        dept: 'Cusco',
        price: 450,
        duration: '1 día',
        difficulty: 'Media-Alta',
        img: 'https://images.unsplash.com/photo-1547483238-2c6036746654',
        detail: 'Conquista el rey de Instagram a 5,200 metros de altitud.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El tour a la Montaña de 7 Colores (Vinicunca) dura 1 día (12 horas), tiene dificultad media-alta por la altitud y cuesta $450. Se asciende a 5,200 msnm, por lo que requiere aclimatación previa. Salidas diarias con recojo a las 4:00 AM. Incluye desayuno y almuerzo buffet.',
        faqs: [
            { q: '¿Cuánto dura la caminata?', a: 'La caminata es de aproximadamente 1.5 a 2 horas de subida y 1 hora de bajada.' },
            { q: '¿Qué pasa si no puedo caminar a esa altitud?', a: 'Puedes alquilar caballos a los comuneros locales en el punto de inicio por un costo adicional.' },
            { q: '¿Hace mucho frío en la cumbre?', a: 'Sí, debido a los 5,200m de altitud y vientos fuertes, la temperatura suele rondar los 0°C a 5°C. Llevar ropa térmica.' },
            { q: '¿El tour incluye alimentación?', a: 'Sí, incluimos desayuno andino antes del trekking y almuerzo buffet al retorno.' },
            { q: '¿Llevan oxígeno de emergencia?', a: 'Todos nuestros grupos viajan equipados con balones de oxígeno portátiles y botiquines de primeros auxilios.' }
        ],
        genInfo: {
            cancelPolicy: 'Cancelación gratuita hasta 24h antes',
            duration: '12-14 horas',
            availability: 'Salidas diarias de madrugada',
            guide: 'Español, Inglés',
            groupSize: 'Máximo 15 participantes'
        },
        whatYouDo: [
            'Conquista la cumbre a 5,200 metros sobre el nivel del mar',
            'Observa el Nevado Ausangate en todo su esplendor',
            'Interactúa con comunidades locales y alpacas',
            'Desayuno y almuerzo buffet andino incluido'
        ],
        fullItinerary: [
            { day: 1, desc: 'Día 1: Conquista la Cumbre. Recojo a las 4:00 AM para ganarle a las multitudes. Desayuno buffet en Cusipata. Caminata de 1.5 horas desafiando la altitud hasta el mirador de Vinicunca (5,200m). Descenso, almuerzo y retorno a Cusco a las 5:00 PM.' }
        ],
        inc: ['Transporte turístico de primera', 'Guía profesional bilingüe', 'Balón de oxígeno de emergencia', 'Desayuno y Almuerzo Buffet andino'],
        notSuitable: ['Personas con asma', 'Menores de 8 años', 'Hipertensos'],
        meetingPoint: 'Recepción de su hotel (Centro Histórico)',
        importantInfo: 'Llevar lentes de sol UV, cortavientos, guantes térmicos (mucho viento en cumbre) y hojas de coca.',
        steps: [{ n: 'G', t: 'Cusco', d: '04:00 AM' }, { n: 'ri-mountain-fill', t: 'Vinicunca', d: '5,200m' }, { n: 'dot', t: 'Cusco', d: 'Retorno' }]
    },
    {
        id: 4,
        title: 'Trekking Choquequirao 4D',
        dept: 'Cusco',
        price: 3200,
        duration: '4 días',
        difficulty: 'Experto',
        img: 'https://images.unsplash.com/photo-1583032353423-04fd96ef2211',
        detail: 'Turismo de Élite. Explora la última ciudad Inca sin multitudes.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Trekking a Choquequirao (4 días) tiene una dificultad experta y un costo de $3,200. Se cruza el profundo Cañón del Apurímac descendiendo y ascendiendo miles de metros. Es ideal para aventureros en excelente forma física que buscan ruinas incas sin las multitudes de Machu Picchu.',
        faqs: [
            { q: '¿Llegamos a Machu Picchu en este tour?', a: 'No, este tour de 4 días es exclusivamente a Choquequirao (la ciudad hermana de Machu Picchu). Existe una versión de 8 días que une ambas.' },
            { q: '¿Es realmente tan difícil como dicen?', a: 'Sí. El desnivel es brutal. Bajarás al fondo del cañón del río Apurímac (1,500m) y volverás a subir a 3,000m bajo un sol fuerte.' },
            { q: '¿Hay baños y duchas?', a: 'Las facilidades son muy rústicas. Hay campamentos con baños básicos de pozo ciego y lavabos fríos de agua de manantial.' },
            { q: '¿Hay señal de celular?', a: 'No. El cañón está totalmente desconectado. Nuestro guía lleva radios de emergencia.' },
            { q: '¿Quién lleva la comida y carpas?', a: 'Contamos con arrieros locales y mulas de carga que transportan todo el campamento y comida.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso del 50% hasta 15 días antes',
            duration: '4 días / 3 noches',
            availability: 'Salidas programadas semanalmente',
            guide: 'Guía especializado en historia Inca',
            groupSize: 'Máximo 8 aventureros'
        },
        whatYouDo: [
            'Cruce del colosal Cañón del río Apurímac',
            'Acampa bajo el cielo más estrellado y puro de Cusco',
            'Explora las misteriosas terrazas de las llamas',
            'Descubre la ciudadela hermana de Machu Picchu en total soledad'
        ],
        fullItinerary: [
            { day: 1, desc: 'Día 1: Descenso al Infierno Verde. Caminata desde Capuliyoc bajando en picada hacia el ardiente Cañón del Apurímac. Campamento en Playa Rosalina.' },
            { day: 2, desc: 'Día 2: La Pared Inclinada. Ascenso brutal en zigzag hacia Marampata. Llegada por la tarde al campamento base de Choquequirao.' },
            { day: 3, desc: 'Día 3: La Ciudad Perdida. Día completo para explorar a solas esta megaestructura inca. Atardecer mágico en las terrazas agrícolas.' },
            { day: 4, desc: 'Día 4: El Retorno del Guerrero. Descenso al cañón y último ascenso de regreso a la civilización (Cachora). Retorno a Cusco.' }
        ],
        inc: ['Equipo de campamento Pro', 'Arrieros y mulas de carga', 'Pensión completa con chef', 'Entradas oficiales'],
        notSuitable: ['Personas sin experiencia en trekking', 'Menores de 15 años'],
        meetingPoint: 'Plaza Regocijo, Cusco (05:00 AM)',
        importantInfo: 'Ruta físicamente devastadora. Traer bastones de trekking (vital para rodillas) y bloqueador FPS 100.',
        steps: [{ n: 'G', t: 'Capuliyoc', d: 'Inicio' }, { n: 'ri-building-4-fill', t: 'Choquequirao', d: 'Ciudadela' }, { n: 'dot', t: 'Cachora', d: 'Retorno' }]
    },
    {
        id: 5,
        title: 'Circuito Ausangate 6D',
        dept: 'Cusco',
        price: 2100,
        duration: '6 días',
        difficulty: 'Técnica',
        img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b',
        detail: 'Expedición mística de alta montaña rodeando el Apu sagrado.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Circuito Ausangate (6 días) es de dificultad técnica con un precio de $2,100. Es un trek de gran altitud permanente (siempre por encima de 4,000m, con pasos de hasta 5,100m). No recomendado sin aclimatación previa estricta. Verás glaciares, lagunas turquesas y vicuñas salvajes.',
        faqs: [
            { q: '¿Necesito experiencia técnica de escalada?', a: 'No requiere escalada en hielo ni cuerdas, pero sí excelente resistencia física y experiencia previa en trekking de altura.' },
            { q: '¿Cuál es el punto más alto?', a: 'El Paso Palomani a 5,100 metros sobre el nivel del mar.' },
            { q: '¿Qué tan frías son las noches?', a: 'Extremadamente frías. Las temperaturas pueden caer a -10°C o -15°C. Necesitas un sleeping bag de 4 estaciones.' },
            { q: '¿Veremos la Montaña de 7 Colores?', a: 'Este itinerario rodea el Ausangate; Vinicunca (7 colores) puede añadirse como extensión, pero el enfoque son las lagunas glaciares.' },
            { q: '¿Está incluido el caballo de rescate?', a: 'Sí, todas nuestras expediciones llevan caballos logísticos extra por si algún pasajero no puede continuar.' }
        ],
        genInfo: {
            cancelPolicy: 'Actividad no reembolsable',
            duration: '6 días / 5 noches',
            availability: 'Temporada de Abril a Octubre',
            guide: 'Guía de Alta Montaña (AGMP)',
            groupSize: 'Expedición privada o máx 6'
        },
        whatYouDo: [
            'Rodea el Apu más sagrado y alto de Cusco (Ausangate)',
            'Duerme a más de 4,000 metros junto a glaciares milenarios',
            'Relájate en aguas termales naturales',
            'Cruza pasos de montaña por encima de los 5,100 metros'
        ],
        fullItinerary: [
            { day: 1, desc: 'Días 1-2: Aguas Termales y Glaciares. De Tinki hacia Upis. Baño termal frente al glaciar. Cruce del primer paso (Arapa) a 4,850m.' },
            { day: 2, desc: 'Días 3-4: El Techo del Mundo. Cruce del paso Palomani (5,100 msnm), el punto más alto. Observación de vicuñas salvajes.' },
            { day: 3, desc: 'Días 5-6: Las Lagunas Turquesas. Descenso pasando por las espectaculares 7 lagunas hasta Pacchanta y retorno a Cusco.' }
        ],
        inc: ['Caballos de carga logísticos', 'Carpas térmicas 4 estaciones', 'Balón de oxígeno', 'Alimentación Pro Alta Montaña'],
        notSuitable: ['Personas no aclimatadas', 'Problemas cardíacos'],
        meetingPoint: 'Recepción de su hotel (06:00 AM)',
        importantInfo: 'Requiere aclimatación mínima de 3 días en Cusco. Necesitas un sleeping bag para -15°C.',
        steps: [{ n: 'G', t: 'Tinqui', d: 'Base' }, { n: 'ri-temp-cold-fill', t: 'Palomani', d: '5,100m' }, { n: 'dot', t: 'Tinqui', d: 'Retorno' }]
    },

    // HUARAZ (5)
    {
        id: 6,
        title: 'Trekking Santa Cruz 4D',
        dept: 'Huaraz',
        price: 1200,
        duration: '4 días',
        difficulty: 'Media-Alta',
        img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190',
        detail: 'El circuito clásico más espectacular de la Cordillera Blanca.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Trekking Santa Cruz (4 días) tiene dificultad media-alta y cuesta $1,200. Cruza la Cordillera Blanca por valles glaciares, alcanzando su punto máximo en el Paso Punta Unión (4,750m). Apto para senderistas con aclimatación previa. Salidas lunes y jueves.',
        faqs: [
            { q: '¿Qué tan frío es por las noches?', a: 'Las temperaturas bajan a -5°C. Se requiere sleeping bag de plumas.' },
            { q: '¿Cuál es la altitud máxima?', a: 'Se alcanza el mítico Paso Punta Unión a 4,750 metros sobre el nivel del mar.' },
            { q: '¿Quién carga las carpas y comida?', a: 'Nuestros arrieros y burros transportan todo el campamento y hasta 5kg de tu equipo personal.' },
            { q: '¿Veremos el nevado Alpamayo?', a: 'Sí, pasaremos por su valle e incluye unas vistas majestuosas del Alpamayo y Taulliraju.' },
            { q: '¿Se requiere oxígeno?', a: 'Es una caminata desafiante pero el guía siempre lleva oxígeno de emergencia.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso parcial hasta 7 días antes',
            duration: '4 días / 3 noches',
            availability: 'Salidas confirmadas lunes y jueves',
            guide: 'Guía oficial de Trekking (AGMP)',
            groupSize: 'Máximo 10 aventureros'
        },
        whatYouDo: [
            'Cruce del mítico Paso Punta Unión a 4,750 msnm',
            'Despertar frente al Nevado Alpamayo, "la montaña más bella del mundo"',
            'Caminata por valles glaciares de intenso color turquesa',
            'Campamentos bajo picos de hielo de más de 6,000 metros'
        ],
        fullItinerary: [
            { day: 1, desc: 'Día 1: Hacia el Valle. Salida de Huaraz a Cashapampa. Caminata inicial por el profundo valle de Santa Cruz hasta el campamento en Llamacorral.' },
            { day: 2, desc: 'Día 2: El Espejo de los Andes. Pasamos por las lagunas Ichiccocha y Jatuncocha. Llegada al Campamento base de Alpamayo (Taullipampa).' },
            { day: 3, desc: 'Día 3: El Techo de la Cordillera. Ascenso duro y gratificante al Paso Punta Unión (4,750m). Vistas espectaculares del Taulliraju. Descenso brutal a Paria.' },
            { day: 4, desc: 'Día 4: El Retorno. Caminata final hacia Vaquería atravesando queñuales andinos. Transporte panorámico de retorno a Huaraz cruzando el paso Portachuelo.' }
        ],
        inc: [
            'Transporte privado Huaraz - Cashapampa / Vaquería - Huaraz',
            'Burros de carga (hasta 5kg de equipo personal)',
            'Cocinero experto en alta montaña (Pensión completa)',
            'Tickets de ingreso al Parque Nacional Huascarán'
        ],
        notSuitable: ['Menores de 10 años', 'Personas con problemas articulares de rodilla', 'Viajeros no aclimatados'],
        meetingPoint: 'Oficina Lifextreme Huaraz (06:00 AM)',
        importantInfo: 'Traer sleeping bag de plumas para -10°C (disponible para renta) y bloqueador extremo.',
        steps: [{ n: 'G', t: 'Cashapampa', d: 'Inicio' }, { n: 'ri-mountain-fill', t: 'Punta Unión', d: '4,750m' }, { n: 'dot', t: 'Vaquería', d: 'Final' }],
        sensoryVariants: {
            landscape: 'Maravíllate ante los picos nevados más imponentes de los Andes, reflejados en lagunas cristalinas.',
            comfort: 'Duerme rodeado de glaciares colosales mientras nuestro chef andino prepara cenas calientes en medio de la nada.',
            action: 'Desafía tus pulmones en el ascenso al Paso Punta Unión y siente la recompensa de la cumbre.'
        }
    },
    {
        id: 7,
        title: 'Expedición Nevado Huascarán 7D',
        dept: 'Huaraz',
        price: 4500,
        duration: '7 días',
        difficulty: 'Experto',
        img: 'https://images.unsplash.com/photo-1522163182402-834f60b58e26',
        detail: 'Conquista la montaña tropical más alta del mundo (6,768m).',
        last_verified: '2026-06-30',
        direct_answer_block: 'La expedición al Huascarán (7 días) es para alpinistas expertos y tiene un precio de $4,500. Se escala la montaña más alta del Perú (6,768m) cruzando paredes de hielo y grietas, con guías UIAGM (1x2). Requiere aclimatación y experiencia en hielo.',
        faqs: [
            { q: '¿Puedo ir si no tengo experiencia técnica?', a: 'No. El Huascarán requiere uso avanzado de piolets, crampones y progresión en cuerda por grietas.' },
            { q: '¿Cuál es el tramo más peligroso?', a: 'El cruce de "La Canaleta" hacia La Garganta debido al riesgo de desprendimiento de seracs.' },
            { q: '¿Cuántos días de aclimatación necesito?', a: 'Mínimo 5 a 7 días en montañas de 5,000m en Huaraz antes de intentar el Huascarán.' },
            { q: '¿Están incluidos los equipos de hielo?', a: 'El costo incluye cuerdas y mosquetones. El equipo personal (botas, piolet, arnés) corre por tu cuenta.' },
            { q: '¿Es 100% segura la cumbre?', a: 'Ninguna expedición garantiza la cumbre. Depende del clima, la aclimatación y el estado del hielo.' }
        ],
        genInfo: {
            cancelPolicy: 'Actividad no reembolsable (Logística Extrema)',
            duration: '7 días / 6 noches',
            availability: 'Temporada Seca (Junio a Agosto)',
            guide: 'Guía UIAGM (1 guía por cada 2 escaladores)',
            groupSize: 'Expedición técnica súper reducida'
        },
        whatYouDo: [
            'Escalada técnica en hielo puro y grietas glaciares',
            'Supervivencia en campos de altura sobre los 5,000 y 6,000 metros',
            'Conquista el punto más alto del Perú (Cumbre Sur 6,768m)',
            'Cruza el paso extremo de "La Canaleta" y "La Garganta"'
        ],
        fullItinerary: [
            { day: 1, desc: 'Día 1: Hacia la Morrena. Salida de Huaraz a Musho. Caminata dura al Campo Base (4,200m).' },
            { day: 2, desc: 'Día 2: El Hielo. Ascenso técnico por la morrena hasta el Campo 1 (5,300m) directamente sobre el glaciar.' },
            { day: 3, desc: 'Día 3: El Abismo. Cruce táctico de "La Canaleta" evadiendo seracs y llegada al Campo 2 (La Garganta a 6,000m).' },
            { day: 4, desc: 'Día 4: Ataque a la Cumbre. Ascenso final a medianoche a los 6,768m. Retorno al Campo 2 (Día extenuante de 12 horas).' },
            { day: 5, desc: 'Día 5: Día de Seguridad. Día extra reservado por mal clima o descanso necesario.' },
            { day: 6, desc: 'Día 6: El Descenso. Descenso cuidadoso desde el Campo 2 hasta el Campo Base.' },
            { day: 7, desc: 'Día 7: La Victoria. Retorno a Musho y transporte a Huaraz.' }
        ],
        inc: [
            'Guías Oficiales UIAGM (Equipamiento de seguridad garantizado)',
            'Cuerdas dinámicas, estacas, tornillos de hielo',
            'Porteros de altura y carpas de expedición',
            'Alimentación de Alta Energía y gas propano'
        ],
        notSuitable: ['Principiantes', 'Personas sin experiencia en cramponaje', 'Mala aclimatación'],
        meetingPoint: 'Centro Base Lifextreme Huaraz (05:00 AM)',
        importantInfo: 'Requiere entrenamiento técnico y aclimatación previa en picos de 5,000m.',
        steps: [{ n: 'G', t: 'Musho', d: 'Base' }, { n: 'ri-vip-crown-fill', t: 'Cumbre Sur', d: '6,768m' }, { n: 'dot', t: 'Huaraz', d: 'Retorno' }],
        sensoryVariants: {
            landscape: 'Siente que tocas el cielo estando en el punto más cercano al sol de toda la zona tropical del planeta.',
            comfort: 'Confía en nuestro equipo técnico UIAGM mientras te refugias en carpas de 4 estaciones en la Garganta.',
            action: 'Desafía el hielo vertical y supera el agotamiento absoluto; esta es la máxima prueba de resistencia.'
        }
    },
    {
        id: 8,
        title: 'Trekking Laguna 69 y Llanganuco',
        dept: 'Huaraz',
        price: 350,
        duration: '1 día',
        difficulty: 'Alta',
        img: 'https://images.unsplash.com/photo-1527004013197-29007328905b',
        detail: 'El desafío de aclimatación más hermoso de la Cordillera Blanca.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Trekking a Laguna 69 es de 1 día (dificultad alta) y cuesta $350. Sube hasta los 4,600 msnm para ver una espectacular laguna turquesa. Son 14 km ida y vuelta. Imprescindible buena condición física y aclimatación previa.',
        faqs: [
            { q: '¿Cuántas horas de caminata son?', a: 'Aproximadamente 3 horas de subida pronunciada y 2 horas de bajada.' },
            { q: '¿Me puede dar mal de altura?', a: 'Sí, llegarás a 4,600m. Si es tu primer día en Huaraz, te recomendamos primero ir a Pastoruri.' },
            { q: '¿Se puede ir con niños?', a: 'No se recomienda para menores de 12 años ni adultos sin entrenamiento.' },
            { q: '¿Incluye almuerzo?', a: 'El tour no incluye almuerzo pero ofrecemos un box lunch opcional.' },
            { q: '¿A qué hora salimos de Huaraz?', a: 'El recojo inicia a las 5:00 AM para aprovechar el clima despejado.' }
        ],
        genInfo: {
            cancelPolicy: 'Cancelación gratuita hasta 24h antes',
            duration: '1 día (12 horas intensas)',
            availability: 'Salidas diarias garantizadas',
            guide: 'Guía local experto',
            groupSize: 'Máximo 15 participantes'
        },
        whatYouDo: [
            'Caminata espectacular bajo los picos del Nevado Chacraraju y Pisco',
            'Fotografía las aguas esmeraldas de las lagunas de Llanganuco',
            'Alcanza la impresionante Laguna 69 a 4,600 metros de altitud',
            'Supera una dura prueba de resistencia cardiovascular'
        ],
        fullItinerary: [
            { day: 1, desc: 'Día 1: Desafío a los 4,600m. Salida 5:00 AM. Parada fotográfica en Lagunas de Llanganuco. Inicio en Cebollapampa (3,900m). Ascenso pronunciado de 3 horas. Contemplación en Laguna 69. Retorno a Huaraz.' }
        ],
        inc: ['Transporte turístico compartido', 'Guía capacitado en primeros auxilios', 'Oxígeno portátil y botiquín', 'Tickets de ingreso'],
        notSuitable: ['Personas mayores de 65 años sin entrenamiento', 'Problemas respiratorios', 'Sedentarios'],
        meetingPoint: 'Plaza de Armas de Huaraz (05:00 AM)',
        importantInfo: 'Llevar impermeable, snacks, hidratación y determinación.',
        steps: [{ n: 'G', t: 'Cebollapampa', d: 'Ascenso' }, { n: 'ri-drop-fill', t: 'Laguna 69', d: '4,600m' }, { n: 'dot', t: 'Huaraz', d: 'Retorno' }],
        sensoryVariants: {
            landscape: 'Camina entre cascadas glaciales hasta descubrir una de las lagunas más turquesas prístinas de la Tierra.',
            comfort: 'Disfruta del traslado en asientos reclinables mientras te preparamos mentalmente para el ascenso.',
            action: 'Siente cómo tu corazón late más fuerte con cada zigzag; la recompensa al llegar superará tu agotamiento.'
        }
    },
    {
        id: 9,
        title: 'Glaciar Pastoruri y Puya Raimondi',
        dept: 'Huaraz',
        price: 280,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190',
        detail: 'Ruta del Cambio Climático y aclimatación familiar.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El tour al Glaciar Pastoruri dura medio día (baja dificultad física, pero altitud extrema a 5,000m) y cuesta $280. Ideal como primera excursión para aclimatar el cuerpo. Incluye parada para ver las famosas Puyas de Raimondi.',
        faqs: [
            { q: '¿Hay que caminar mucho?', a: 'No. El bus llega cerca del glaciar y la caminata dura solo 45 minutos.' },
            { q: '¿Es apto para toda la familia?', a: 'Sí, la ruta está pavimentada en partes, pero cuidado con el mal de altura (5,000m).' },
            { q: '¿Hace falta equipo técnico?', a: 'No. Solo necesitas ropa abrigadora y buenos zapatos impermeables.' },
            { q: '¿Por qué la llaman ruta del Cambio Climático?', a: 'Porque el glaciar está en franco retroceso y podrás ver evidencia directa del deshielo mundial.' },
            { q: '¿A qué hora terminamos?', a: 'Normalmente retornamos a Huaraz alrededor de las 3:00 o 4:00 PM.' }
        ],
        genInfo: {
            cancelPolicy: 'Cancelación gratuita hasta 12h antes',
            duration: '7 horas de recorrido',
            availability: 'Salidas diarias a las 09:00 AM',
            guide: 'Guía bilingüe de historia natural',
            groupSize: 'Ideal para familias'
        },
        whatYouDo: [
            'Camina sobre el hielo de un glaciar milenario en retroceso',
            'Conoce la planta andina más alta del mundo: Puya Raimondi',
            'Observa pinturas rupestres pre-incas en el valle',
            'Toca la nieve y el hielo a más de 5,000 metros sin escalar'
        ],
        fullItinerary: [
            { day: 1, desc: 'Día 1: El Glaciar. Parada en el bosque de Puya Raimondi y aguas gasificadas de Pumapampa. Llegada a la base del Pastoruri (4,800m). Caminata de 45 min al frente glaciar. Retorno a Huaraz.' }
        ],
        inc: ['Bus turístico panorámico', 'Paradas fotográficas', 'Guía bilingüe experto'],
        notSuitable: ['Personas que sufren de mal de altura severo'],
        meetingPoint: 'Recojo en hotel en Huaraz (09:00 AM)',
        importantInfo: 'Ruta con poco esfuerzo físico pero altitud extrema (5,000m).',
        steps: [{ n: 'G', t: 'Huaraz', d: 'Salida' }, { n: 'ri-snowy-fill', t: 'Pastoruri', d: 'Glaciar' }, { n: 'dot', t: 'Huaraz', d: 'Retorno' }],
        sensoryVariants: {
            landscape: 'Pisa un gigante de hielo que se desvanece; una experiencia visual única sobre nuestro planeta.',
            comfort: 'Aclimatación perfecta para tu primer día, con paradas constantes y transporte sumamente cómodo.',
            action: 'Juega con la nieve a más de 5,000 metros sin necesidad de piolets ni experiencia.'
        }
    },
    {
        id: 10,
        title: 'Nevado Ishinca Base Camp 3D',
        dept: 'Huaraz',
        price: 1600,
        duration: '3 días',
        difficulty: 'Técnica',
        img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b',
        detail: 'Tu primer "Cincomil" y entrenamiento de cuerdas en glaciar.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La expedición Ishinca Base Camp (3 días) tiene dificultad técnica básica y precio de $1,600. Es el "cincomil" (5,530m) ideal para iniciarse en montañismo, durmiendo en un cómodo refugio andino y practicando técnicas de hielo con guías certificados.',
        faqs: [
            { q: '¿Necesito botas cramponables?', a: 'Sí, es obligatorio el uso de botas de alta montaña rígidas compatibles con crampones.' },
            { q: '¿Dormiremos en carpas?', a: 'No, este tour incluye la estadía en el Refugio Andino Ishinca, brindando mayor comodidad.' },
            { q: '¿Me darán clases técnicas?', a: 'Sí. El tour incluye entrenamiento de nudos, progresión en ensamble y manejo básico de piolet.' },
            { q: '¿Quién lleva mi equipo pesado?', a: 'Contamos con arrieros (burros) que suben tu equipo desde el transporte hasta el refugio.' },
            { q: '¿Si no hago cumbre, me reembolsan?', a: 'No. Los costos operativos de refugio y guías se cubren independientemente del éxito de la cumbre.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso del 50% hasta 5 días antes',
            duration: '3 días / 2 noches',
            availability: 'Salidas programadas o bajo pedido',
            guide: 'Guía Aspirante / UIAGM',
            groupSize: 'Máximo 4 personas por guía'
        },
        whatYouDo: [
            'Alojamiento estilo europeo en Refugio Andino Ishinca',
            'Escalada técnica al pico Ishinca (5,530m)',
            'Taller intensivo de cuerdas, piolets y crampones',
            'Vistas panorámicas 360° de la Cordillera Blanca'
        ],
        fullItinerary: [
            { day: 1, desc: 'Día 1: El Refugio. Caminata al Refugio Ishinca (4,350m). Prácticas de nudos.' },
            { day: 2, desc: 'Día 2: El Ataque. Salida de madrugada hacia el Nevado Ishinca. Prácticas en glaciar, progresión en ensamble. Cumbre y retorno.' },
            { day: 3, desc: 'Día 3: El Descenso. Desayuno andino y retorno en vehículo privado a Huaraz.' }
        ],
        inc: [
            'Estadía en Refugio Ishinca',
            'Cenas calientes tipo alpinista',
            'Guía técnico (Entrenamiento)',
            'Burros de carga'
        ],
        notSuitable: ['Personas sin botas cramponables'],
        meetingPoint: 'Huaraz Basecamp Office',
        importantInfo: 'Ideal como entrenamiento antes de intentar retos como Huascarán.',
        steps: [{ n: 'G', t: 'Pashpa', d: 'Inicio' }, { n: 'ri-vip-crown-fill', t: 'Ishinca', d: '5,530m' }, { n: 'dot', t: 'Huaraz', d: 'Retorno' }],
        sensoryVariants: {
            landscape: 'Despierta rodeado de paredes de hielo vertical que quitan el aliento.',
            comfort: 'Disfruta del calor de un refugio de montaña sin necesidad de armar carpas.',
            action: 'Aprende a clavar tus crampones y manejar el piolet en tu primer ascenso técnico.'
        }
    },

    // IQUITOS (5)
    {
        id: 11,
        title: 'Pacaya Samiria Safari',
        dept: 'Iquitos',
        price: 2800,
        duration: '5 días',
        difficulty: 'Media',
        img: 'https://images.unsplash.com/photo-1516306580123-e6e52b1b7b5f',
        detail: 'Vida silvestre profunda en la selva de espejos.',
        genInfo: {
            cancelPolicy: 'Gratis hasta 15 días antes',
            duration: '5 días',
            availability: 'Todo el año (mejor en creciente)',
            guide: 'Ranger nativo certificado',
            groupSize: 'Botes privados para 4-6 pax'
        },
        whatYouDo: [
            'Búsqueda de delfines rosados y grises en el río',
            'Expediciones nocturnas para avistamiento de caimanes',
            'Pesca artesanal de pirañas en lagunas negras',
            'Contacto con comunidades Kukama y sus tradiciones'
        ],
        fullItinerary: [
            { day: 1, desc: 'Iquitos - Nauta vía terrestre. Embarque en bote rápido hacia la reserva. Primer campamento o lodge táctico.' },
            { day: 2, desc: 'Navegación por el río Yanayacu-Pucate. Observación de primates y aves tropicales.' },
            { day: 3, desc: 'Caminata por selva inundable. Búsqueda de la Victoria Regia y nutrias gigantes.' },
            { day: 4, desc: 'Exploración de la "Selva de los Espejos" para fotos de reflejos perfectos.' },
            { day: 5, desc: 'Desayuno en la selva, navegación de retorno a Nauta e Iquitos.' }
        ],
        inc: ['Bote con motor fuera de borda', 'Lodge o campamento con mosquiteros', 'Chef de selva', 'Botas de goma'],
        notSuitable: ['Personas alérgicas a picaduras de insectos severas'],
        meetingPoint: 'Aeropuerto o Hotel en Iquitos',
        importantInfo: 'Vacuna contra la fiebre amarilla altamente recomendada.',
        steps: [{ n: 'G', t: 'Iquitos', d: 'Nauta' }, { n: 'dot', t: 'Iquitos', d: 'Retorno' }]
    },
    {
        id: 12,
        title: 'Ayahuasca Retreat Pro',
        dept: 'Iquitos',
        price: 3500,
        duration: '7 días',
        difficulty: 'Espiritual',
        img: 'https://images.unsplash.com/photo-1440342359743-84fcb8c21f21',
        detail: 'Viaje espiritual guiado por maestros Shamanes.',
        genInfo: {
            cancelPolicy: 'Reembolso 100% hasta 30 días antes',
            duration: '7 días / 6 noches',
            availability: 'Retiros mensuales programados',
            guide: 'Maestro Onaya (Shipibo-Konibo)',
            groupSize: 'Máximo 10 pasajeros por sesión'
        },
        whatYouDo: [
            'Participa en 3 ceremonias sagradas de Ayahuasca',
            'Charlas de integración con psicólogos y maestros',
            'Alimentación basada en dieta tradicional de limpieza',
            'Vivir en un centro holístico en medio de la reserva'
        ],
        fullItinerary: [
            { day: 1, desc: 'Llegada y purga inicial con tabaco o plantas medicinales. Introducción.' },
            { day: 2, desc: 'Primera ceremonia nocturna. Silencio profundo.' },
            { day: 3, desc: 'Integración grupal. Caminata por el jardín botánico de plantas maestras.' },
            { day: 4, desc: 'Segunda ceremonia. Trabajo de introspección profunda.' },
            { day: 5, desc: 'Día de descanso consciente y baños de florecimiento.' },
            { day: 6, desc: 'Tercera y última ceremonia de sellado espiritual.' },
            { day: 7, desc: 'Cierre de retiro y retorno a la civilización.' }
        ],
        inc: ['Hospedaje individual rústico', 'Dieta de purificación', 'Entrevistas personales con maestro'],
        notSuitable: ['Personas con medicación psiquiátrica', 'Problemas de presión arterial'],
        meetingPoint: 'Iquitos Harbor Office',
        importantInfo: 'Requiere preparación dietética estricta 2 semanas antes del viaje.',
        steps: [{ n: 'G', t: 'Maloca', d: 'Inicio' }, { n: 'dot', t: 'Luz', d: 'Cierre' }]
    },
    {
        id: 13,
        title: 'Monkey Island Boat',
        dept: 'Iquitos',
        price: 150,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9',
        detail: 'Rescate de primates en el Amazonas.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '5 horas',
            availability: 'Diario 9:00 AM y 1:00 PM',
            guide: 'Staff del santuario',
            groupSize: 'Open tour'
        },
        whatYouDo: [
            'Conoce 9 especies de monos rescatados de la venta ilegal',
            'Aprende sobre el proceso de reintroducción a la selva',
            'Navegación por el río más caudaloso del mundo',
            'Soporte directo a un proyecto de conservación real'
        ],
        fullItinerary: [
            { day: 1, desc: 'Salida de Iquitos en bote. Navegación de 45 min. Estancia en la isla con guías de conservación. Retorno con sunset en el río.' }
        ],
        inc: ['Bote ida y vuelta', 'Donación incluida', 'Guía especialista'],
        notSuitable: ['Mascotas'],
        meetingPoint: 'Puerto de Bellavista-Nanay',
        importantInfo: 'No usar perfumes fuertes para no estresar a los animales.',
        steps: [{ n: 'G', t: 'Puerto', d: '09:00 AM' }, { n: 'dot', t: 'Isla', d: 'Visita' }]
    },
    {
        id: 14,
        title: 'Amazon Canopy Walkway',
        dept: 'Iquitos',
        price: 650,
        duration: '1 día',
        difficulty: 'Media',
        img: 'https://images.unsplash.com/photo-1542332213-9b5a5a3fad35',
        detail: 'Puentes colgantes sobre la copa de los árboles.',
        genInfo: {
            cancelPolicy: 'Gratis 48h antes',
            duration: '8 horas',
            availability: 'Diario',
            guide: 'Guía bilingüe',
            groupSize: 'Privado o grupos pequeños'
        },
        whatYouDo: [
            'Camina a 35 metros de altura sobre el suelo de la selva',
            'Observa bromelias, orquídeas y aves desde los puentes',
            'Aprende sobre la estratificación vertical de la Amazonía',
            'Almuerzo en lodge ecológico incluido'
        ],
        fullItinerary: [
            { day: 1, desc: 'Bote desde Iquitos. Caminata de aproximación. Ascenso a torres de control. Recorrido de 500 metros de puentes. Almuerzo selvático. Retorno.' }
        ],
        inc: ['Transporte fluvial', 'Tickets de ingreso', 'Arnés y seguridad', 'Almuerzo'],
        notSuitable: ['Personas con acrofobia o vértigo extremo'],
        meetingPoint: 'Iquitos Lodge Reception',
        importantInfo: 'Llevar binoculares para aprovechar las vistas.',
        steps: [{ n: 'G', t: 'Lodge', d: 'Ascenso' }, { n: 'dot', t: 'Mirador', d: 'Sunset' }]
    },
    {
        id: 15,
        title: 'Survival Jungle Camp',
        dept: 'Iquitos',
        price: 1950,
        duration: '3 días',
        difficulty: 'Alta',
        img: 'https://images.unsplash.com/photo-1516306580123-e6e52b1b7b5f',
        detail: 'Aprende a vivir de la selva virgen.',
        genInfo: {
            cancelPolicy: 'Reembolso 50% hasta 7 días antes',
            duration: '3 días / 2 noches',
            availability: 'Solo temporada seca',
            guide: 'Ex-militar o nativo comando',
            groupSize: 'Máximo 4 personas'
        },
        whatYouDo: [
            'Construcción de refugios temporales con materiales naturales',
            'Técnicas de obtención de agua y fuego en ambiente húmedo',
            'Identificación de plantas comestibles y medicinales',
            'Orientación táctica sin GPS en densa vegetación'
        ],
        fullItinerary: [
            { day: 1, desc: 'Abandono de la zona de confort. Caminata profunda. Primer refugio.' },
            { day: 2, desc: 'Técnicas de caza primitiva y recolección. Gestión del fuego bajo lluvia.' },
            { day: 3, desc: 'Señalización de rescate y extracción.' }
        ],
        inc: ['Machete personal (regalo)', 'Botiquín trauma', 'Instrucción experta'],
        notSuitable: ['Cualquier condición de salud pre-existente sin previo aviso'],
        meetingPoint: 'Iquitos Military Dock',
        importantInfo: 'No apto para personas que busquen comodidad. Es un reto psicológico duro.',
        steps: [{ n: 'G', t: 'Selva', d: 'Drop off' }, { n: 'dot', t: 'Selva', d: 'Pick up' }]
    },

    // PIURA (5)
    {
        id: 16,
        title: 'Kitesurf Máncora Pro',
        dept: 'Piura',
        price: 850,
        duration: '3 días',
        difficulty: 'Media',
        img: 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd',
        detail: 'Vuela sobre las olas del Pacífico norte.',
        genInfo: {
            cancelPolicy: 'Gratis 72h antes',
            duration: '3 días presenciales',
            availability: 'Temporada Mayo - Noviembre',
            guide: 'Instructor IKO Nivel 2',
            groupSize: 'Individual o Pareja'
        },
        whatYouDo: [
            'Control de vela en tierra (ventanas de viento)',
            'Body drag para rescate de tabla en mar abierto',
            'Primeros "rides" en las olas de Máncora',
            'Certificación internacional IKO al finalizar'
        ],
        fullItinerary: [
            { day: 1, desc: 'Teoría y vuelo de kite de entrenamiento en la arena.' },
            { day: 2, desc: 'Prácticas en el agua. Control de potencia.' },
            { day: 3, desc: 'Intento de navegación con tabla (Waterstart).' }
        ],
        inc: ['Kite, arnés y tabla profesional', 'Comunicación casco radio', 'Seguro de equipo'],
        notSuitable: ['Menores de 12 años', 'Personas que no saben nadar'],
        meetingPoint: 'Máncora Kite Zone Office',
        importantInfo: 'Máncora tiene los mejores vientos constantes del Perú.',
        steps: [{ n: 'G', t: 'Beach', d: 'Viento' }, { n: 'dot', t: 'Sunset', d: 'Bar' }]
    },
    {
        id: 17,
        title: 'Nado Polinizador Tortugas',
        dept: 'Piura',
        price: 120,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1544551763-47a0159f963f',
        detail: 'Nado respetuoso con tortugas en El Ñuro.',
        genInfo: {
            cancelPolicy: 'Gratis hasta 24h antes',
            duration: '3 horas',
            availability: 'Diario 08:00 AM a 1:00 PM',
            guide: 'Guía de mar',
            groupSize: 'Grupal'
        },
        whatYouDo: [
            'Nado con tortugas verdes gigantes en su hábitat natural',
            'Visita al centro de interpretación marina',
            'Fotos GoPro profesionales (vía Staff)',
            'Contribuye al turismo sostenible de caletas'
        ],
        fullItinerary: [
            { day: 1, desc: 'Recojo en Máncora. Traslado a El Ñuro. Instrucción de respeto animal. 1 hora de nado. Fotos. Retorno.' }
        ],
        inc: ['Transporte ida y vuelta', 'Chaleco salvavidas obligatorio', 'Snorkel'],
        notSuitable: ['Personas con bloqueador solar no biodegradable'],
        meetingPoint: 'Muelle de El Ñuro',
        importantInfo: 'PROHIBIDO tocar o alimentar a las tortugas. Lifextreme promueve el respeto total.',
        steps: [{ n: 'G', t: 'Muelle', d: 'Embarque' }, { n: 'dot', t: 'Mar', d: 'Nado' }]
    },
    {
        id: 18,
        title: 'Cabo Blanco Surf Quest',
        dept: 'Piura',
        price: 300,
        duration: '1 día',
        difficulty: 'Media',
        img: 'https://images.unsplash.com/photo-1439066615861-d1af74d74000',
        detail: 'La mejor ola izquierda del Perú.',
        genInfo: {
            cancelPolicy: 'Reembolso por mal oleaje 100%',
            duration: '1 día',
            availability: 'Diciembre - Marzo (Swell Norte)',
            guide: 'Local Pro Surfer',
            groupSize: 'Máximo 3 pax'
        },
        whatYouDo: [
            'Surfea tubos perfectos en la ola histórica de Hemingway',
            'Coaching táctico dentro del agua',
            'Almuerzo en caleta de pescadores ancestrales',
            'Grabación de video para análisis técnico'
        ],
        fullItinerary: [
            { day: 1, desc: 'Sesión de mañana (Dawn Patrol). Analisis de corriente. Surf intenso. Almuerzo de mar fresco. Sesión tarde.' }
        ],
        inc: ['Board Pro (opcional)', 'Traslado fluvial a la ola si es necesario', 'Almuerzo ceviche'],
        notSuitable: ['Surfistas nivel principiante (ola peligrosa sobre reef)'],
        meetingPoint: 'Cabo Blanco Fishing Club',
        importantInfo: 'Requiere nivel intermedio-avanzado comprobable.',
        steps: [{ n: 'G', t: 'Caleta', d: '06:00 AM' }, { n: 'dot', t: 'Pipeline', d: 'Final' }]
    },
    {
        id: 19,
        title: 'Manglares Tumbes Safari',
        dept: 'Piura',
        price: 450,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1518495973542-4542c06a5843',
        detail: 'Navegación por ecosistemas únicos.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '8 horas',
            availability: 'Diario',
            guide: 'Guía oficial de turismo',
            groupSize: 'Grupal o Familiar'
        },
        whatYouDo: [
            'Viaje en bote por el Santuario Nacional Manglares',
            'Visita al zoocriadero de cocodrilos americanos',
            'Degustación de conchas negras y cangrejo de manglar',
            'Frontera histórica entre Perú y Ecuador'
        ],
        fullItinerary: [
            { day: 1, desc: 'Salida de Máncora/Tumbes. Embarque en Puerto Pizarro. Isla de los Pájaros. Zoocriadero. Almuerzo tradicional. Compras en frontera (opcional). Retorno.' }
        ],
        inc: ['Transporte climatizado', 'Almuerzo buffet de mariscos', 'Bote motorizado'],
        notSuitable: ['Personas alérgicas a los mariscos'],
        meetingPoint: 'Oficina Tumbes Center',
        importantInfo: 'Traer repelente fuerte y gorra.',
        steps: [{ n: 'G', t: 'Zarumilla', d: 'Bote' }, { n: 'dot', t: 'Frontera', d: 'Retorno' }]
    },
    {
        id: 20,
        title: 'Whale Watching Season',
        dept: 'Piura',
        price: 250,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1454991727061-be514eae86f7',
        detail: 'Observación de ballenas jorobadas.',
        genInfo: {
            cancelPolicy: 'Garantía de avistamiento parcial',
            duration: '4 horas',
            availability: 'Agosto - Octubre únicamente',
            guide: 'Biólogo marino',
            groupSize: 'Bote de expedición (20 pax)'
        },
        whatYouDo: [
            'Avistamiento de saltos y cantos de ballenas jorobadas',
            'Uso de hidrófonos para escuchar cantos bajo el agua',
            'Observación de delfines, lobos y tortugas',
            'Charla científica sobre migración antártica'
        ],
        fullItinerary: [
            { day: 1, desc: 'Zarpe 7:30 AM. Navegación en zona de tránsito. Avistamiento de grupos de ballenas. Hidrófono táctico. Retorno al mediodía.' }
        ],
        inc: ['Bote certificado de gran tamaño', 'Chalecos Pro', 'Agua y snacks'],
        notSuitable: ['Personas que sufren de mareo fuerte (tomar medicación 1h antes)'],
        meetingPoint: 'Marina de Los Órganos',
        importantInfo: 'Tener cámara con buen zoom lista.',
        steps: [{ n: 'G', t: 'Órganos', d: 'Salida' }, { n: 'dot', t: 'Alta Mar', d: 'Retorno' }]
    },

    // ICA (5)
    {
        id: 21,
        title: 'Sandboarding Huacachina',
        dept: 'ICA',
        price: 180,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1506461883276-594a12b11cf3',
        detail: 'Adrenalina pura en las dunas más altas.',
        genInfo: {
            cancelPolicy: 'Gratis 12h antes',
            duration: '3 horas de aventura',
            availability: 'Diario (recom: 4:00 PM)',
            guide: 'Conductor Buggy certificado',
            groupSize: 'Grupal 8-10 pax por auto'
        },
        whatYouDo: [
            'Tour extremo en Tubulares (Buggies) por el desierto',
            'Descenso de dunas gigantes en tablas de sandboard',
            'Sunset épico en el Oasis de América',
            'Fotos panorámicas de las dunas vírgenes'
        ],
        fullItinerary: [
            { day: 1, desc: 'Inicio en el Oasis. Traslado a zona de dunas. Serie de descensos de menor a mayor dificultad. Sesión de fotos tácticas. Retorno al Oasis.' }
        ],
        inc: ['Sandboard Pro (velas incluidas)', 'Conductor profesional', 'Impuestos SENANP'],
        notSuitable: ['Problemas columna', 'Embarazadas'],
        meetingPoint: 'Entrada al Oasis Huacachina',
        importantInfo: 'Traer anteojos de sol (arena vuela rápido).',
        steps: [{ n: 'G', t: 'Oasis', d: 'Briefing' }, { n: 'dot', t: 'Dunas', d: 'Sunset' }]
    },
    {
        id: 22,
        title: 'Paracas Res. Satelital',
        dept: 'ICA',
        price: 350,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1610484826917-0f101a7bf7f4',
        detail: 'Expedición terrestre a la Reserva Nacional.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '6 horas',
            availability: 'Diario',
            guide: 'Naturalista',
            groupSize: 'Privado SUV'
        },
        whatYouDo: [
            'Formaciones rocosas únicas (Catedral)',
            'Visita a Playas Rojas y Lagunillas',
            'Observación de flamencos y aves de desierto',
            'Almuerzo frente al mar incluido'
        ],
        fullItinerary: [
            { day: 1, desc: 'Pickup Paracas. Ingreso a reserva. Miradores de playas. Caminata suave por senderos geológicos. Almuerzo en caleta de pescadores. Retorno.' }
        ],
        inc: ['SUV 4x4 privada', 'Almuerzo a la carta', 'Pick up hotel'],
        notSuitable: ['Personas con sensibilidad al polvo'],
        meetingPoint: 'Recepción Hotel en Paracas',
        importantInfo: 'La cámara es obligatoria para el paisaje lunar.',
        steps: [{ n: 'G', t: 'Paracas', d: 'Pickup' }, { n: 'dot', t: 'Catedral', d: 'Final' }]
    },
    {
        id: 23,
        title: 'Islas Ballestas Boat',
        dept: 'ICA',
        price: 80,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1544551763-47a0159f963f',
        detail: 'El pequeño Galápagos de Perú.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '2 horas',
            availability: '08:00 AM y 10:00 AM (fijo)',
            guide: 'Guía oficial',
            groupSize: 'Lancha compartida 20-30 pax'
        },
        whatYouDo: [
            'Navegación frente al geoglifo "El Candelabro"',
            'Miles de pingüinos de Humboldt y Lobos Marinos',
            'Aves guaneras cubriendo las islas blancas',
            'Formaciones rocosas marinas naturales'
        ],
        fullItinerary: [
            { day: 1, desc: 'Embarque en muelle turístico. Navegación costa. Parada en Candelabro. Circuito Islas Ballestas. Retorno.' }
        ],
        inc: ['Lancha con motores modernos', 'Chalecos salvavidas', 'Impuestos de reserva'],
        notSuitable: ['Miedo intenso al mar'],
        meetingPoint: 'Muelle Turístico de Paracas',
        importantInfo: 'Lanzarse al agua está estrictamente prohibido.',
        steps: [{ n: 'G', t: 'Puerto', d: 'Zarpe' }, { n: 'dot', t: 'Mar', d: 'Puerto' }]
    },
    {
        id: 24,
        title: 'Nazca Flight Experience',
        dept: 'ICA',
        price: 650,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1540304453527-62f9791029c1',
        detail: 'Vuelo sobre los misteriosos geoglifos.',
        genInfo: {
            cancelPolicy: 'Gratis 48h antes',
            duration: '35 min de vuelo',
            availability: 'Dependiente de clima (mañana)',
            guide: 'Piloto instructor',
            groupSize: 'Avioneta 4-6 pax'
        },
        whatYouDo: [
            'Observa el Colibrí, el Astronauta y el Mono desde el aire',
            'Explicación arqueológica en tiempo real vía auriculares',
            'Maniobras tácticas para fotos desde ambos lados del avión',
            'Certificado de vuelo oficial Nazca'
        ],
        fullItinerary: [
            { day: 1, desc: 'Check-in aeródromo Maria Reiche. Video introductorio. Pesaje. Despegue. Circuito de 12 geoglifos principales. Aterrizaje.' }
        ],
        inc: ['Vuelo certificado', 'Traslados hotel-aeropuerto', 'Guía de vuelo'],
        notSuitable: ['Personas con problemas de oído interno si es severo'],
        meetingPoint: 'Aeródromo Maria Reiche (Nazca)',
        importantInfo: 'Desayuno ligero recomendado (evitar lácteos antes de volar).',
        steps: [{ n: 'G', t: 'Aeródromo', d: 'Check-in' }, { n: 'dot', t: 'Nazca', d: 'Vuelo' }]
    },
    {
        id: 25,
        title: 'Viñedo Elite Tasting',
        dept: 'ICA',
        price: 220,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1506377247377-2a5b3b0ca3ef',
        detail: 'Visita técnica a bodegas de Pisco.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '4 horas',
            availability: 'Diario',
            guide: 'Sommelier',
            groupSize: 'Privado'
        },
        whatYouDo: [
            'Tour por viñedos de uvas pisqueras',
            'Visita a destilería moderna y falcas coloniales',
            'Cata dirigida de 5 variedades de Pisco Elite',
            'Aprende a preparar el Pisco Sour perfecto'
        ],
        fullItinerary: [
            { day: 1, desc: 'Entrada al viñedo. Explicación del suelo. Proceso de destilación. Cata en cava subterránea. Taller de coctelería.' }
        ],
        inc: ['Transporte privado', 'Cata de alta gama', 'Snacks de maridaje'],
        notSuitable: ['Menores de 18 años'],
        meetingPoint: 'Hotel Centro Ica',
        importantInfo: 'Ica es la cuna del Pisco, disfruta responsablemente.',
        steps: [{ n: 'G', t: 'Ica', d: 'Ingreso' }, { n: 'dot', t: 'Cata', d: 'Final' }]
    },

    // PUNO (5)
    {
        id: 26,
        title: 'Titicaca Kayak Quest',
        dept: 'Puno',
        price: 150,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1544551763-47a0159f963f',
        detail: 'Rema por el lago navegable más alto.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '4 horas',
            availability: 'Mañanas (07:00 AM)',
            guide: 'Guía de aventura certificado',
            groupSize: 'Máximo 10 kayaks'
        },
        whatYouDo: [
            'Navegación en kayak de travesía por el Lago Titicaca',
            'Visita a las islas flotantes de los Uros en horario no turístico',
            'Observación de aves endémicas en los totorales',
            'Amanecer espectacular sobre el horizonte andino'
        ],
        fullItinerary: [
            { day: 1, desc: 'Recojo en hotel. Traslado a la bahía de Puno. Charla técnica de remado. 1.5 horas de travesía hasta Uros. Desayuno local. Retorno remando o en bote de apoyo.' }
        ],
        inc: ['Kayak profesional y remo', 'Chaleco salvavidas y falda', 'Guía especialista', 'Snack andino'],
        notSuitable: ['Personas que no toleran el frío intenso matutino'],
        meetingPoint: 'Puerto de Puno (Isla Esteves)',
        importantInfo: 'Llevar guantes y ropa térmica. El agua está a 10°C.',
        steps: [{ n: 'G', t: 'Puno', d: 'Remos' }, { n: 'dot', t: 'Uros', d: 'Base' }]
    },
    {
        id: 27,
        title: 'Taquile Island Hike',
        dept: 'Puno',
        price: 120,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1516306580123-e6e52b1b7b5f',
        detail: 'Tradición textil en medio del lago.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '8 horas',
            availability: 'Diario',
            guide: 'Guía local bilingüe',
            groupSize: 'Grupal'
        },
        whatYouDo: [
            'Caminata por senderos prehispánicos con vistas al lago',
            'Demostración de tejido por los famosos tejedores Taquileños',
            'Almuerzo tradicional de trucha en la plaza del pueblo',
            'Conoce el sistema social único de la isla'
        ],
        fullItinerary: [
            { day: 1, desc: 'Bote desde Puno. Arribo a Taquile. Ascenso de 500 escalones (lento). Exploración de la isla. Almuerzo. Descenso por el otro lado de la isla. Retorno.' }
        ],
        inc: ['Transporte fluvial', 'Almuerzo tradicional', 'Guía local'],
        notSuitable: ['Personas con dificultades motoras'],
        meetingPoint: 'Muelle Principal de Puno',
        importantInfo: 'Respetar las costumbres locales y no tomar fotos sin permiso en rituales.',
        steps: [{ n: 'G', t: 'Muelle', d: 'Bote' }, { n: 'dot', t: 'Isla', d: 'Retorno' }]
    },
    {
        id: 28,
        title: 'Sillustani Necropolis',
        dept: 'Puno',
        price: 90,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1587547131116-a0655a526190',
        detail: 'Chullpas funerarias de la cultura Qolla.',
        genInfo: {
            cancelPolicy: 'Gratis 12h antes',
            duration: '3.5 horas',
            availability: 'Tardes (14:00 PM)',
            guide: 'Guía arqueológico',
            groupSize: 'Abierto'
        },
        whatYouDo: [
            'Explora las impresionantes torres funerarias de hasta 12m',
            'Vistas panorámicas de la Laguna Umayo y su isla central',
            'Conoce la ingeniería lítica de los Collas e Incas',
            'Observa la fauna local (alpacas y vizcachas)'
        ],
        fullItinerary: [
            { day: 1, desc: 'Viaje por tierra desde Puno (45 min). Recorrido guiado por el complejo arqueológico. Tiempo para meditación frente a la laguna. Regreso a Puno.' }
        ],
        inc: ['Bus turístico', 'Entrada al sitio', 'Guía'],
        notSuitable: ['-'],
        meetingPoint: 'Recojo en Plaza de Armas Puno',
        importantInfo: 'Ideal para visitar el día que llegas o te vas de Puno.',
        steps: [{ n: 'G', t: 'Puno', d: 'Check' }, { n: 'dot', t: 'Sillustani', d: 'Final' }]
    },
    {
        id: 29,
        title: 'Amantani Overnight',
        dept: 'Puno',
        price: 400,
        duration: '2 días',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1440342359743-84fcb8c21f21',
        detail: 'Duerme en la casa de una familia local.',
        genInfo: {
            cancelPolicy: 'Reembolso 50% hasta 7 días antes',
            duration: '2 días / 1 noche',
            availability: 'Salidas diarias 08:00 AM',
            guide: 'Coordinador local',
            groupSize: 'Pequeños grupos por familia'
        },
        whatYouDo: [
            'Hospeda y comparte comidas con una familia isleña',
            'Ritual de agradecimiento a la Pachamama al sunset',
            'Fiesta tradicional con trajes típicos locales',
            'Caminata a los templos Pachatata y Pachamama'
        ],
        fullItinerary: [
            { day: 1, desc: 'Bote a Uros y luego a Amantaní. Bienvenida por las familias. Almuerzo. Caminata al templo sagrado al atardecer. Cena y peña bailable.' },
            { day: 2, desc: 'Desayuno familiar. Despedida. Visita a Taquile (opcional) o retorno directo a Puno.' }
        ],
        inc: ['Transporte fluvial', 'Hospedaje rural', '3 comidas locales', 'Guía'],
        notSuitable: ['Personas que requieran servicios de lujo extremos'],
        meetingPoint: 'Muelle de Puno',
        importantInfo: 'Llevar pequeños regalos para los niños de la familia es un buen gesto.',
        steps: [{ n: 'G', t: 'Puno', d: 'Bote' }, { n: 'dot', t: 'Amantani', d: 'Noche' }]
    },
    {
        id: 30,
        title: 'Puerta Aramu Muru',
        dept: 'Puno',
        price: 110,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1583032353423-04fd96ef2211',
        detail: 'El portal interdimensional de Hayu Marca.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '5 horas',
            availability: 'Diario bajo reserva',
            guide: 'Guía místico / arqueólogo',
            groupSize: 'Máximo 8 pax'
        },
        whatYouDo: [
            'Visita la famosa "Puerta de los Dioses" tallada en roca',
            'Realiza una sesión de meditación solar guiada',
            'Explora el bosque de piedras de Hayu Marca',
            'Fotos espectaculares de formaciones rocosas rojas'
        ],
        fullItinerary: [
            { day: 1, desc: 'Viaje hacia el sur de Puno. Caminata suave entre las formaciones rocosas. Tiempo de conexión en el portal. Regreso vía Chucuito (Templo de la Fertilidad).' }
        ],
        inc: ['Transporte privado', 'Guía místico especializado', 'Entradas'],
        notSuitable: ['Escépticos extremos (es una ruta de enfoque místico)'],
        meetingPoint: 'Hotel Puno Center',
        importantInfo: 'Se recomienda llevar cristales u objetos personales para cargar energía.',
        steps: [{ n: 'G', t: 'Chucuito', d: 'Viaje' }, { n: 'dot', t: 'Portal', d: 'Final' }]
    },

    // AREQUIPA (5)
    {
        id: 31,
        title: 'Colca Canyon Trek 3D',
        dept: 'Arequipa',
        price: 850,
        duration: '3 días',
        difficulty: 'Alta',
        img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b',
        detail: 'Uno de los cañones más profundos.',
        genInfo: {
            cancelPolicy: 'Gratis hasta 7 días antes',
            duration: '3 días / 2 noches',
            availability: 'Salidas diarias 03:00 AM',
            guide: 'Guía especializado de trekking',
            groupSize: 'Máximo 10 personas'
        },
        whatYouDo: [
            'Observa el vuelo majestuoso del Cóndor Andino',
            'Desciende 1,200 metros hasta el fondo del cañón',
            'Relájate en el Oasis de Sangalle con piscinas naturales',
            'Ascenso épico de madrugada bajo las estrellas'
        ],
        fullItinerary: [
            { day: 1, desc: 'Arequipa a Chivay. Cruz del Cóndor. Descenso desde Cabanaconde hasta San Juan de Chuccho.' },
            { day: 2, desc: 'Caminata por pueblos Malata y Cosñirhua. Llegada al Oasis de Sangalle. Tarde de piscina.' },
            { day: 3, desc: 'Ascenso 4:00 AM hacia Cabanaconde. Desayuno. Baños termales en Chivay. Retorno a Arequipa.' }
        ],
        inc: ['Bus Arequipa-Chivay-Cabanaconde', 'Hospedajes rústicos', 'Pensión completa', 'Guía'],
        notSuitable: ['Personas con vértigo o problemas de rodilla'],
        meetingPoint: 'Hotel en Arequipa (03:00 AM)',
        importantInfo: 'El ascenso final es muy exigente físicamente.',
        steps: [{ n: 'G', t: 'Chivay', d: 'Inicio' }, { n: 'dot', t: 'Cabanaconde', d: 'Retorno' }]
    },
    {
        id: 32,
        title: 'Misti Volcano Ascent',
        dept: 'Arequipa',
        price: 1100,
        duration: '2 días',
        difficulty: 'Experto',
        img: 'https://images.unsplash.com/photo-1522163182402-834f60b58e26',
        detail: 'Sube al volcán guardián de la ciudad blanca.',
        genInfo: {
            cancelPolicy: 'No reembolsable',
            duration: '2 días',
            availability: 'Temporada seca (Abril-Nov)',
            guide: 'Guía UIAGM/AGMP',
            groupSize: 'Expedición privada 2 pax por guía'
        },
        whatYouDo: [
            'Alcanza la cumbre de un volcán activo de 5,822m',
            'Observa el cráter humeante y siente el olor a azufre',
            'Vistas increíbles de Arequipa iluminada por la noche',
            'Descenso rápido por arenales volcánicos'
        ],
        fullItinerary: [
            { day: 1, desc: 'Transporte 4x4 a la base. Caminata de ascenso hasta el campamento Nido de Águilas (4,500m). Cena y descanso temprano.' },
            { day: 2, desc: 'Ascenso cumbre a la 1:00 AM. Llegada a la cruz de la cima al amanecer. Fotos en el cráter. Descenso y retorno.' }
        ],
        inc: ['SUV 4x4 técnica', 'Equipo de campamento Pro', 'Guía de montaña', 'Alimentación'],
        notSuitable: ['Personas sin experiencia en altitud'],
        meetingPoint: 'Oficina Lifextreme Arequipa',
        importantInfo: 'Mucho viento y frío extremo en la noche.',
        steps: [{ n: 'G', t: 'Arequipa', d: 'Salida' }, { n: 'dot', t: 'Cumbre', d: 'Cumbre' }]
    },
    {
        id: 33,
        title: 'Rafting Río Chili',
        dept: 'Arequipa',
        price: 150,
        duration: '1 día',
        difficulty: 'Media',
        img: 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd',
        detail: 'Rápidos clase III a clase IV.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '3 horas totales',
            availability: 'Turnos 08:00 AM, 11:00 AM, 2:00 PM',
            guide: 'Instructor IRF Clase 5',
            groupSize: '6 pax por bote'
        },
        whatYouDo: [
            'Enfréntate a los rápidos del río Chili en el valle de Chilina',
            'Aprende comandos de remo táctico y rescate en río',
            'Vistas únicas de los volcanes desde el fondo del cañón',
            'Snacks y fotos de acción incluidos'
        ],
        fullItinerary: [
            { day: 1, desc: 'Recojo. Traslado a Charcani. Equipamiento. Charla de seguridad. 1.5 horas en el río. Desembarque y retorno.' }
        ],
        inc: ['Bote, remos, casco y chaleco', 'Wetsuit (opcional)', 'Guía profesional', 'Transporte'],
        notSuitable: ['Personas que no saben nadar'],
        meetingPoint: 'Plaza de Armas Arequipa',
        importantInfo: 'Traer ropa de cambio completa después del río.',
        steps: [{ n: 'G', t: 'Charcani', d: 'Brief' }, { n: 'dot', t: 'Puente', d: 'Final' }]
    },
    {
        id: 34,
        title: 'Canteras del Sillar',
        dept: 'Arequipa',
        price: 60,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1587547131116-a0655a526190',
        detail: 'La historia de la piedra volcánica.',
        genInfo: {
            cancelPolicy: 'Gratis 12h antes',
            duration: '4 horas',
            availability: 'Diario mañanas y tardes',
            guide: 'Guía local experto',
            groupSize: 'Abierto'
        },
        whatYouDo: [
            'Observa cómo los maestros cortadores trabajan el sillar',
            'Visita la fachada de la Compañía de Jesús grabada en la cantera',
            'Explora la Quebrada de Culebrillas (tallado ancestral)',
            'Ayuda a la economía circular de los cortadores tradicionales'
        ],
        fullItinerary: [
            { day: 1, desc: 'Traslado a las canteras de Añashuayco. Demostración de corte. Recorrido por las mega-estructuras. Caminata por Culebrillas. Retorno.' }
        ],
        inc: ['Bus turístico', 'Guía certificado', 'Entradas'],
        notSuitable: ['-'],
        meetingPoint: 'Hoteles céntricos Arequipa',
        importantInfo: 'Traer buen sombrero, el sol en la piedra blanca es muy fuerte.',
        steps: [{ n: 'G', t: 'Centro', d: 'Tour' }, { n: 'dot', t: 'Sillar', d: 'Fin' }]
    },
    {
        id: 35,
        title: 'Ascenso Chachani',
        dept: 'Arequipa',
        price: 950,
        duration: '2 días',
        difficulty: 'Experto',
        img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190',
        detail: 'Sencillo paso por los 6,000m.',
        genInfo: {
            cancelPolicy: 'No reembolsable',
            duration: '2 días',
            availability: 'Sujeto a clima',
            guide: 'Guía AGMP',
            groupSize: 'Pareja o Privado'
        },
        whatYouDo: [
            'Técnicamente el "6 mil" más fácil del mundo',
            'Supera la barrera de los 6,075 metros snm',
            'Uso de crampones en glaciar residual',
            'Inmortaliza tu logro en la cima helada'
        ],
        fullItinerary: [
            { day: 1, desc: 'Viaje 4x4 hasta los 5,000m. Caminata suave al campamento base. Aclimatación y cena.' },
            { day: 2, desc: 'Ataque a la cumbre 2:00 AM. 5 a 6 horas de ascenso constante. Cumbre. Descenso directo al auto.' }
        ],
        inc: ['Traslado 4x4 especializado', 'Equipo camping', 'Guía cumbre', 'Oxígeno'],
        notSuitable: ['Personas con mala aclimatación'],
        meetingPoint: 'Oficina Lifextreme Arequipa',
        importantInfo: 'Es un reto de altitud pura, no técnico.',
        steps: [{ n: 'G', t: 'Campo Base', d: 'Alta' }, { n: 'dot', t: '6075m', d: 'Top' }]
    },

    // LIMA (5)
    {
        id: 36,
        title: 'Parapente Costa Verde',
        dept: 'Lima',
        price: 280,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1534447677768-be436bb09401',
        detail: 'Vuelo sobre los acantilados de Lima.',
        genInfo: {
            cancelPolicy: 'Reembolso 100% por falta de viento',
            duration: '15 min de vuelo',
            availability: 'Sujeto a condiciones de viento',
            guide: 'Piloto instructor APVL',
            groupSize: 'Vuelo individual con piloto'
        },
        whatYouDo: [
            'Despegue desde el paracuerto de Miraflores',
            'Vistas aéreas de Larcomar, playas y ciudad',
            'Siente la libertad de volar como un ave sobre el océano',
            'Video HD de tu vuelo grabado en GoPro'
        ],
        fullItinerary: [
            { day: 1, desc: 'Check-in en el parque Raimondi. Charla técnica. Espera de ventana de viento. Vuelo panorámico. Aterrizaje suave en el mismo punto.' }
        ],
        inc: ['Equipo de vuelo certificado', 'Piloto experto', 'Seguro de accidentes', 'Tarjeta SD con Video'],
        notSuitable: ['Personas con peso superior a 100kg'],
        meetingPoint: 'Parapuerto de Miraflores',
        importantInfo: 'Llegar 15 min antes de tu turno programado.',
        steps: [{ n: 'G', t: 'Parapuerto', d: 'Briefing' }, { n: 'dot', t: 'Cielo', d: 'Landing' }]
    },
    {
        id: 37,
        title: 'Islas Palomino Swim',
        dept: 'Lima',
        price: 180,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1610484826917-0f101a7bf7f4',
        detail: 'Nada con miles de lobos marinos.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '4 horas',
            availability: 'Turno mañana (10:00 AM)',
            guide: 'Biólogo / Guía de mar',
            groupSize: 'Yate de expedición'
        },
        whatYouDo: [
            'Navegación por el puerto del Callao frente a islas históricas',
            'Nado respetuoso junto a colonia de miles de lobos marinos',
            'Observación de aves guaneras y pingüinos',
            'Snacks y fotos de recuerdo'
        ],
        fullItinerary: [
            { day: 1, desc: 'Zarpe desde el muelle Darsena. Isla San Lorenzo y El Frontón. Arribo a Islas Palomino. 20 min de nado con wetsuit. Retorno al puerto.' }
        ],
        inc: ['Yate de gran calado', 'Wetsuit y chaleco', 'Guía profesional', 'Tasa de embarque'],
        notSuitable: ['Miedo al mar abierto'],
        meetingPoint: 'Puerto de la Darsena, Callao',
        importantInfo: 'Prohibido tocar a los lobos, ellos se acercan solos por curiosidad.',
        steps: [{ n: 'G', t: 'Muelle', d: 'Check' }, { n: 'dot', t: 'Mar', d: 'Nado' }]
    },
    {
        id: 38,
        title: 'Trekking Marcahuasi',
        dept: 'Lima',
        price: 250,
        duration: '2 días',
        difficulty: 'Media',
        img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b',
        detail: 'El bosque de piedras místico.',
        genInfo: {
            cancelPolicy: 'Gratis 72h antes',
            duration: '2 días / 1 noche',
            availability: 'Fines de semana o privado',
            guide: 'Guía experto en altitud',
            groupSize: 'Grupal aventurero'
        },
        whatYouDo: [
            'Caminata hacia la meseta a 4,000m de altura',
            'Observa las extrañas figuras talladas por la naturaleza (Monumento a la Humanidad)',
            'Acampa bajo uno de los cielos más limpios cerca de Lima',
            'Siente la energía mística del lugar'
        ],
        fullItinerary: [
            { day: 1, desc: 'Lima a San Pedro de Casta. Ascenso caminando o a mula hasta la meseta. Campamento Anfiteatro. Noche de fogata.' },
            { day: 2, desc: 'Recorrido por las figuras (Cabañas, Alquimista). Descenso al pueblo. Retorno a Lima.' }
        ],
        inc: ['Bus Lima-Casta-Lima', 'Carpas y sleeping (opcional)', 'Guía', 'Derecho ingreso'],
        notSuitable: ['Personas con mala oxigenación inmediata'],
        meetingPoint: 'Calle Comercio, San Borja (Lima)',
        importantInfo: 'Llevar mucha ropa de abrigo, la temperatura baja a 0°C.',
        steps: [{ n: 'G', t: 'Chosica', d: 'Viaje' }, { n: 'dot', t: 'Meseta', d: 'Base' }]
    },
    {
        id: 39,
        title: 'Ciclismo Lomas de Lúcumo',
        dept: 'Lima',
        price: 120,
        duration: '1 día',
        difficulty: 'Media',
        img: 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd',
        detail: 'Mountain bike en el desierto verde.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '5 horas',
            availability: 'Temporada Lomas (Jun-Oct)',
            guide: 'Instructor MTB',
            groupSize: 'Máximo 8 ciclistas'
        },
        whatYouDo: [
            'Ruta técnica de MTB por senderos de lomas costeras',
            'Observación de la flor de Amancae',
            'Descensos fluidos con vistas al valle de Pachacamac',
            'Taller básico de mecánica de emergencia'
        ],
        fullItinerary: [
            { day: 1, desc: 'Punto de encuentro. Setup de bicis. Ascenso constante por 1 hora. Descensos por singletracks. Almuerzo campestre opcional. Retorno.' }
        ],
        inc: ['Bicicleta de montaña Pro', 'Casco y guantes', 'Instructor experto'],
        notSuitable: ['Personas que no dominan la bicicleta en tierra'],
        meetingPoint: 'Plaza de Armas de Pachacamac',
        importantInfo: 'Traer rodilleras si tienes poca experiencia.',
        steps: [{ n: 'G', t: 'Pachacamac', d: 'MTB' }, { n: 'dot', t: 'Lomas', d: 'Final' }]
    },
    {
        id: 40,
        title: 'Antioquía Art Village',
        dept: 'Lima',
        price: 150,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1440342359743-84fcb8c21f21',
        detail: 'El pueblo pintado de colores.',
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '10 horas',
            availability: 'Sábados y Domingos',
            guide: 'Guía bilingüe',
            groupSize: 'Grupal familiar'
        },
        whatYouDo: [
            'Visita el pueblo reconocido por el Récord Guinness como el más pintado',
            'Prueba mermeladas artesanales de manzana y membrillo',
            'Visita el santuario de la juventud y el río Lurín',
            'Almuerzo típico de camarones (en temporada)'
        ],
        fullItinerary: [
            { day: 1, desc: 'Salida de Lima. Parada en Cieneguilla. Llegada a Antioquía. Recorrido fotográfico por las casas pintadas. Almuerzo. Visita a restos arqueológicos cercanos. Retorno.' }
        ],
        inc: ['Bus turístico ida y vuelta', 'Guía de turismo', 'Degustación de productos'],
        notSuitable: ['-'],
        meetingPoint: 'Larcomar / San Borja',
        importantInfo: 'Ideal para amantes de la fotografía de arquitectura y arte.',
        steps: [{ n: 'G', t: 'Lima', d: 'Pickup' }, { n: 'dot', t: 'Antioquía', d: 'Retorno' }]
    }
];

const events = [
    // JUNIO
    { id: 201, title: 'Mi Primer Trail', dept: 'Lima', cat: 'Trail Running', date: '13', month: 'JUN', img: 'https://images.unsplash.com/photo-1551632811-561732d1e306?q=80&w=2070', price: 80, detail: 'Parque Ecológico de La Molina. Ideal para iniciantes.', whatYouDo: ['Senderos cortos', 'Acompañamiento', 'Naturaleza'], steps: [{ n: 'ri-flag-2-line', t: 'Inicio', d: 'La Molina' }, { n: 'ri-medal-line', t: 'Meta', d: 'Parque' }], inc: ['Dorsal', 'Hidratación', 'Medalla'] },
    { id: 202, title: 'Ruta de la Chirimoya', dept: 'Lima', cat: 'Trail Running', date: '14', month: 'JUN', img: 'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?q=80&w=2070', price: 90, detail: 'Carrera en Callahuanca, Huarochirí. Disfruta de paisajes y fruta fresca.', whatYouDo: ['Ascensos', 'Senderos rurales', 'Degustación'], steps: [{ n: 'ri-flag-2-line', t: 'Inicio', d: 'Callahuanca' }, { n: 'ri-medal-line', t: 'Meta', d: 'Plaza' }], inc: ['Dorsal', 'Hidratación', 'Chirimoyas'] },
    { id: 203, title: 'Cajatambo Raid', dept: 'Lima', cat: 'Expedición', date: '14', month: 'JUN', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070', price: 150, detail: 'Raid de aventura en la sierra de Lima.', whatYouDo: ['Trek', 'Orientación', 'Clima andino'], steps: [{ n: 'ri-compass-line', t: 'Ruta', d: 'Navegación' }, { n: 'ri-medal-line', t: 'Cierre', d: 'Cajatambo' }], inc: ['Mapa', 'Asistencia', 'Medalla'] },
    { id: 204, title: 'Geoconsciencia Quelccaya', dept: 'Cusco', cat: 'Expedición', date: '14', month: 'JUN', img: 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=2070', price: 120, detail: 'Salida al Sistema Glaciar Quelccaya y Suyuparina.', whatYouDo: ['Trek Glaciar', 'Observación', 'Consciencia'], steps: [{ n: 'ri-snowflake-line', t: 'Glaciar', d: 'Ascenso' }, { n: 'ri-eye-line', t: 'Observación', d: 'Estudio' }], inc: ['Guía', 'Transporte', 'Snack'] },
    { id: 205, title: 'Tatoo Terra Challenge', dept: 'Lima', cat: 'Trail & Enduro', date: '20', month: 'JUN', img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190?q=80&w=2070', price: 180, detail: 'Morro Edition en Chorrillos. Incluye Trail Running y MTB Enduro.', whatYouDo: ['Rutas técnicas', 'Descensos Enduro', 'Medalla Finisher'], steps: [{ n: 'ri-riding-line', t: 'Morro', d: 'Desafío' }, { n: 'ri-medal-line', t: 'Meta', d: 'Playa' }], inc: ['Dorsal', 'Hidratación', 'Seguro'] },
    { id: 206, title: 'Carrera Sauce', dept: 'San Martín', cat: 'Trail Running', date: '20', month: 'JUN', img: 'https://images.unsplash.com/photo-1522163182402-834f60b58e26?q=80&w=2070', price: 100, detail: 'Corre bordeando la famosa Laguna Azul en Tarapoto.', whatYouDo: ['Selva', 'Humedad', 'Barro'], steps: [{ n: 'ri-drop-line', t: 'Laguna', d: 'Ruta' }, { n: 'ri-medal-line', t: 'Meta', d: 'Pueblo' }], inc: ['Dorsal', 'Hidratación', 'Medalla'] },
    { id: 207, title: 'Marcahuasi Ultra SkyRunning', dept: 'Lima', cat: 'Ultra Trail', date: '26', month: 'JUN', img: 'https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=2070', price: 250, detail: 'El MUT. Ascenso brutal hasta el bosque de piedras de Marcahuasi.', whatYouDo: ['SkyRunning', 'Altura extrema', 'Desnivel'], steps: [{ n: 'ri-arrow-up-line', t: 'Ascenso', d: 'San Pedro' }, { n: 'ri-landscape-line', t: 'Meseta', d: 'Marcahuasi' }], inc: ['Dorsal tracker', 'Puntos abasto', 'Polo Finisher'] },
    { id: 208, title: 'Picha Trail Fest', dept: 'Junín', cat: 'Trail Running', date: '28', month: 'JUN', img: 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?q=80&w=2070', price: 120, detail: 'Festival de Trail en la sierra central del Perú.', whatYouDo: ['Valles', 'Río', 'Naturaleza'], steps: [{ n: 'ri-flag-2-line', t: 'Inicio', d: 'Valle' }, { n: 'ri-medal-line', t: 'Meta', d: 'Centro' }], inc: ['Dorsal', 'Hidratación', 'Fiesta'] },
    { id: 209, title: 'Ranking Nac. DH 2da Válida', dept: 'Apurímac', cat: 'MTB DH', date: '13', month: 'JUN', img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190?q=80&w=2070', price: 150, detail: 'Campeonato Nacional de Downhill en Andahuaylas.', whatYouDo: ['Descenso extremo', 'Saltos', 'Velocidad'], steps: [{ n: 'ri-arrow-down-line', t: 'Partida', d: 'Cima' }, { n: 'ri-flag-checkered-line', t: 'Llegada', d: 'Valle' }], inc: ['Remonte', 'Cronometraje', 'Seguro'] },
    { id: 210, title: 'Andes Pacific MTB Cup', dept: 'Lima', cat: 'MTB Enduro', date: '20', month: 'JUN', img: 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?q=80&w=2070', price: 160, detail: 'Copa Internacional de Enduro en Huachupampa.', whatYouDo: ['Enduro', 'Zonas técnicas', 'Roca'], steps: [{ n: 'ri-riding-line', t: 'Especial 1', d: 'Sierra' }, { n: 'ri-flag-checkered-line', t: 'Liaison', d: 'Plaza' }], inc: ['Chip', 'Abastecimiento', 'Medalla'] },
    { id: 211, title: 'Ranking Nac. XCO 4ta Válida', dept: 'Arequipa', cat: 'MTB XCO', date: '21', month: 'JUN', img: 'https://images.unsplash.com/photo-1517604931442-7105376f7c04?q=80&w=2070', price: 140, detail: 'Cross Country Olímpico en Arequipa.', whatYouDo: ['Circuitos técnicos', 'Explosividad', 'Altitud'], steps: [{ n: 'ri-riding-line', t: 'Circuito', d: 'Vueltas' }, { n: 'ri-trophy-line', t: 'Podio', d: 'Premiación' }], inc: ['Dorsal', 'Cronometraje', 'Jueces UCI'] },

    // JULIO
    { id: 212, title: 'Ultra Trail Cordillera Blanca', dept: 'Huaraz', cat: 'Ultra Trail', date: '02', month: 'JUL', img: 'https://images.unsplash.com/photo-1551632811-561732d1e306?q=80&w=2070', price: 350, detail: 'UTCB. Corre bajo los glaciares tropicales más altos del mundo.', whatYouDo: ['Rutas 12K a 50K', 'Vistas Glaciares', 'Altitud extrema'], steps: [{ n: 'ri-flag-2-line', t: 'Huaraz', d: 'Partida' }, { n: 'ri-trophy-line', t: 'Meta', d: 'Llegada' }], inc: ['Kit UTCB', 'Puntos de Abasto', 'Medalla'] },
    { id: 213, title: 'Ai Apaec Trail', dept: 'La Libertad', cat: 'Trail Running', date: '12', month: 'JUL', img: 'https://images.unsplash.com/photo-1440342359743-84fcb8c21f21?q=80&w=2070', price: 90, detail: 'Ruta moche en Trujillo. Corriendo entre dunas y ruinas.', whatYouDo: ['Arena', 'Calor', 'Ruinas'], steps: [{ n: 'ri-sun-line', t: 'Desierto', d: 'Ruta' }, { n: 'ri-medal-line', t: 'Moche', d: 'Meta' }], inc: ['Dorsal', 'Hidratación', 'Medalla'] },
    { id: 214, title: 'Sierra Andina Mountain Trail', dept: 'Huaraz', cat: 'Trail Running', date: '19', month: 'JUL', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070', price: 200, detail: 'Carrera extrema en Matara, Áncash.', whatYouDo: ['Desnivel', 'Alta montaña', 'Frío'], steps: [{ n: 'ri-arrow-up-line', t: 'Ascenso', d: 'Paso' }, { n: 'ri-flag-checkered-line', t: 'Meta', d: 'Pueblo' }], inc: ['Dorsal', 'Cerveza SAMT', 'Medalla'] },
    { id: 215, title: 'Desafío Manchay', dept: 'Lima', cat: 'Trail Running', date: '19', month: 'JUL', img: 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?q=80&w=2070', price: 80, detail: 'Carrera local de cerros y arenales en Lima.', whatYouDo: ['Lomas', 'Arena', 'Ascensos cortos'], steps: [{ n: 'ri-flag-2-line', t: 'Inicio', d: 'Manchay' }, { n: 'ri-medal-line', t: 'Meta', d: 'Plaza' }], inc: ['Dorsal', 'Agua', 'Medalla'] },
    { id: 216, title: 'Tingo María Trail', dept: 'Huánuco', cat: 'Trail Running', date: '25', month: 'JUL', img: 'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?q=80&w=2070', price: 150, detail: 'Corre en la selva alta, cerca de la Bella Durmiente.', whatYouDo: ['Humedad', 'Barro', 'Vegetación'], steps: [{ n: 'ri-leaf-line', t: 'Selva', d: 'Ruta' }, { n: 'ri-medal-line', t: 'Meta', d: 'Cueva' }], inc: ['Dorsal', 'Kit supervivencia', 'Fiesta Finisher'] },
    { id: 217, title: 'Valley Camp', dept: 'Cusco', cat: 'Expedición', date: '27', month: 'JUL', img: 'https://images.unsplash.com/photo-1522163182402-834f60b58e26?q=80&w=2070', price: 850, detail: 'Campamento de Exploradores en Urubamba.', whatYouDo: ['Supervivencia', 'Trek', 'Cultura'], steps: [{ n: 'ri-tent-line', t: 'Base', d: 'Valle' }, { n: 'ri-compass-line', t: 'Explorar', d: 'Montañas' }], inc: ['Carpas', 'Alimentación', 'Guías'] },
    { id: 218, title: 'Ranking Nac. DH 3ra Válida', dept: 'Cusco', cat: 'MTB DH', date: '11', month: 'JUL', img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190?q=80&w=2070', price: 150, detail: 'Downhill Nacional en los senderos sagrados del Cusco.', whatYouDo: ['Descenso extremo', 'Piedra inca', 'Drops'], steps: [{ n: 'ri-arrow-down-line', t: 'Partida', d: 'Cima' }, { n: 'ri-flag-checkered-line', t: 'Llegada', d: 'Valle' }], inc: ['Remonte', 'Cronometraje', 'Seguro'] },

    // AGOSTO
    { id: 219, title: 'adidas Andes Race', dept: 'Cusco', cat: 'Ultra Maratón', date: '14', month: 'AGO', img: 'https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=2070', price: 480, detail: 'Una de las ultra maratones más exigentes del calendario andino.', whatYouDo: ['Running 100k', 'Pasos a 4500m', 'Vistas del Valle'], steps: [{ n: 'ri-flag-2-line', t: 'Partida', d: 'Valle' }, { n: 'ri-trophy-line', t: 'Meta', d: 'Ollantaytambo' }], inc: ['Kit Corredor', 'Medalla Inka', 'Seguro'] },
    { id: 220, title: 'Ranking Nac. DH 4ta Válida', dept: 'Cajamarca', cat: 'MTB DH', date: '14', month: 'AGO', img: 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?q=80&w=2070', price: 150, detail: 'Downhill Nacional en Cajamarca.', whatYouDo: ['Descenso extremo', 'Tierra suelta', 'Curvas'], steps: [{ n: 'ri-arrow-down-line', t: 'Partida', d: 'Cima' }, { n: 'ri-flag-checkered-line', t: 'Llegada', d: 'Base' }], inc: ['Remonte', 'Cronometraje', 'Seguro'] },
    { id: 221, title: 'Ranking Nac. XCO 5ta Válida', dept: 'Cusco', cat: 'MTB XCO', date: '23', month: 'AGO', img: 'https://images.unsplash.com/photo-1517604931442-7105376f7c04?q=80&w=2070', price: 140, detail: 'Penúltima fecha del circuito XCO.', whatYouDo: ['Circuito', 'Rock gardens', 'Altitud'], steps: [{ n: 'ri-riding-line', t: 'Circuito', d: 'Vueltas' }, { n: 'ri-trophy-line', t: 'Podio', d: 'Premiación' }], inc: ['Dorsal', 'Cronometraje', 'Jueces UCI'] },

    // SEPTIEMBRE
    { id: 222, title: 'Sudamericano BMX Racing', dept: 'Lima', cat: 'BMX', date: '19', month: 'SEP', img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190?q=80&w=2070', price: 200, detail: 'Campeonato Sudamericano y Latinoamericano BMX en la Costa Verde.', whatYouDo: ['BMX Racing', 'Saltos triples', 'Competición intl'], steps: [{ n: 'ri-riding-line', t: 'Pista', d: 'Clasificación' }, { n: 'ri-trophy-line', t: 'Finales', d: 'Podio' }], inc: ['Acceso a pista', 'Seguro', 'Placa UCI'] },
    { id: 223, title: 'Ranking Nac. DH 5ta Válida', dept: 'Lima', cat: 'MTB DH', date: '26', month: 'SEP', img: 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?q=80&w=2070', price: 150, detail: 'Circuito DH en Amancay.', whatYouDo: ['Roca', 'Polvo', 'Inclinación'], steps: [{ n: 'ri-arrow-down-line', t: 'Partida', d: 'Cima' }, { n: 'ri-flag-checkered-line', t: 'Meta', d: 'Pachacamac' }], inc: ['Remonte', 'Cronometraje', 'Seguro'] },
    { id: 224, title: 'Peru Outdoor Expo', dept: 'Amazonas', cat: 'Feria B2B', date: '30', month: 'SEP', img: 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=2070', price: 0, detail: 'Evento top y rueda de negocios para operadores de aventura.', whatYouDo: ['Networking', 'Equipos', 'Innovación'], steps: [{ n: 'ri-store-line', t: 'Feria', d: 'Expo' }, { n: 'ri-hand-coin-line', t: 'Negocios', d: 'B2B' }], inc: ['Credencial', 'Charlas', 'Catálogos'] },

    // OCTUBRE
    { id: 225, title: 'MTB Pongo de Maenique', dept: 'Cusco', cat: 'MTB Extremo', date: '07', month: 'OCT', img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190?q=80&w=2070', price: 1200, detail: 'La Película. Expedición MTB de resistencia en la selva de Cusco.', whatYouDo: ['MTB Selva', 'Supervivencia', 'Grabación'], steps: [{ n: 'ri-film-line', t: 'Shooting', d: 'Selva' }, { n: 'ri-riding-line', t: 'Travesía', d: 'Pongo' }], inc: ['Logística completa', 'Aparición en film', 'Campamentos'] },

    // NOVIEMBRE
    { id: 226, title: 'Triatlón Paracas', dept: 'Ica', cat: 'Triatlón', date: '21', month: 'NOV', img: 'https://images.unsplash.com/photo-1522163182402-834f60b58e26?q=80&w=2070', price: 650, detail: 'Distancia Medio Ironman en la Reserva de Paracas.', whatYouDo: ['Nado 1.9k', 'Bici 90k', 'Trote 21k'], steps: [{ n: 'ri-water-flash-line', t: 'Océano', d: 'Nado' }, { n: 'ri-medal-line', t: 'Meta', d: 'Finish' }], inc: ['Gorro natación', 'Dorsal', 'Cena carbohidratos'] },
    { id: 227, title: 'Huacho Half Marathon', dept: 'Lima', cat: 'Running', date: '22', month: 'NOV', img: 'https://images.unsplash.com/photo-1551632811-561732d1e306?q=80&w=2070', price: 90, detail: 'Media maratón de asfalto en el norte chico.', whatYouDo: ['Asfalto', 'Velocidad', 'Brisas'], steps: [{ n: 'ri-flag-2-line', t: 'Inicio', d: 'Plaza' }, { n: 'ri-medal-line', t: 'Meta', d: 'Malecón' }], inc: ['Polo oficial', 'Medalla', 'Hidratación'] },

    // DICIEMBRE
    { id: 228, title: 'Clausura Trail Cierre Temporada', dept: 'Arequipa', cat: 'Trail Running', date: '05', month: 'DIC', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070', price: 120, detail: 'Expedición final sin carácter competitivo. Aclimatación y confraternidad.', whatYouDo: ['Trek relajado', 'Confraternidad', 'Fogata'], steps: [{ n: 'ri-group-line', t: 'Comunidad', d: 'Ruta' }, { n: 'ri-fire-line', t: 'Fogata', d: 'Cierre' }], inc: ['Comida', 'Sorteos', 'Polo recuerdo'] }
];

const equips = [
    // MOCHILAS (5)
    { name: 'Osprey Aether 65 Elite', cat: 'Mochilas', price: 1250, rentPrice: 45, img: 'https://images.unsplash.com/photo-1622260614153-03223fb72052' }, // Dark Tactical/Hiking
    { name: 'Mammal Pro 45L Tactical', cat: 'Mochilas', price: 850, rentPrice: 35, img: 'https://images.unsplash.com/photo-1590845947698-8924d7409b56' }, // Camo/Green
    { name: 'Arc teryx Bora 75', cat: 'Mochilas', price: 1800, rentPrice: 60, img: 'https://images.unsplash.com/photo-1581605405669-fcdf81165afa' }, // Orange/Mountain
    { name: 'Gregory Baltoro 85 Pro', cat: 'Mochilas', price: 1100, rentPrice: 40, img: 'https://images.unsplash.com/photo-1547847932-d3a3d538df59' }, // Camping vibes
    { name: 'Black Diamond Speed 30', cat: 'Mochilas', price: 650, rentPrice: 25, img: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62' }, // General Rucksack

    // CALZADO (5)
    { name: 'La Sportiva Nepal Cube', cat: 'Calzado', price: 2150, rentPrice: 80, img: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff' }, // Red Nike style but sturdy
    { name: 'Scarpa Phantom 6000', cat: 'Calzado', price: 3200, rentPrice: 120, img: 'https://images.unsplash.com/photo-1520639888713-7851133b1ed0' }, // Boot in snow
    { name: 'Salomon Quest 4 GTX', cat: 'Calzado', price: 950, rentPrice: 35, img: 'https://images.unsplash.com/photo-1512990414788-d97cb4a25db3' }, // Classic hiking boots
    { name: 'Zamberlan Vioz Lux', cat: 'Calzado', price: 1300, rentPrice: 50, img: 'https://images.unsplash.com/photo-1603808033192-082d6919d3e1' }, // Brown leather boots
    { name: 'Merrell Moab 3 Tactical', cat: 'Calzado', price: 750, rentPrice: 30, img: 'https://images.unsplash.com/photo-1595341888016-a392ef81b7de' }, // Tactical shoe

    // ACCESORIOS (5)
    { name: 'Black Diamond Spot 400', cat: 'Accesorios', price: 220, rentPrice: 15, img: 'https://images.unsplash.com/photo-1563857508098-b6483134604d' }, // Headlamp style
    { name: 'Garmin InReach Mini 2', cat: 'Accesorios', price: 1650, rentPrice: 65, img: 'https://images.unsplash.com/photo-1557262947-2cb2d4705540' }, // Watch/GPS vibe
    { name: 'Petzl Summit Evo Axe', cat: 'Accesorios', price: 780, rentPrice: 35, img: 'https://images.unsplash.com/photo-1506377225131-41e98d9ba0d1' }, // Ice axe/Pick
    { name: 'BioLite SolarPanel 5+', cat: 'Accesorios', price: 420, rentPrice: 20, img: 'https://images.unsplash.com/photo-1545209355-66795f5539d8' }, // Solar/Tech
    { name: 'Therma-Rest NeoAir XTherm', cat: 'Accesorios', price: 950, rentPrice: 40, img: 'https://images.unsplash.com/photo-1617326693439-0bd649033376' } // Camping mat/gear
];

// Equipment recommendation mapping by tour type
const tourEquipmentMap = {
    'Cusco': ['Osprey Aether 65 Elite', 'La Sportiva Nepal Cube', 'Black Diamond Spot 400'],
    'Huaraz': ['Arc teryx Bora 75', 'Scarpa Phantom 6000', 'Petzl Summit Evo Axe', 'Therma-Rest NeoAir XTherm'],
    'Iquitos': ['Mammal Pro 45L Tactical', 'Merrell Moab 3 Tactical', 'Garmin InReach Mini 2'],
    'Piura': ['Black Diamond Speed 30', 'Salomon Quest 4 GTX', 'BioLite SolarPanel 5+'],
    'ICA': ['Gregory Baltoro 85 Pro', 'Zamberlan Vioz Lux', 'Black Diamond Spot 400'],
    'Puno': ['Osprey Aether 65 Elite', 'Salomon Quest 4 GTX', 'Therma-Rest NeoAir XTherm'],
    'Arequipa': ['Arc teryx Bora 75', 'La Sportiva Nepal Cube', 'Petzl Summit Evo Axe'],
    'Lima': ['Black Diamond Speed 30', 'Merrell Moab 3 Tactical', 'Garmin InReach Mini 2']
};

// Kit templates for complete packages
const kitTemplates = {
    'Alta Montaña': {
        name: 'Kit Montaña Elite',
        items: ['Arc teryx Bora 75', 'Scarpa Phantom 6000', 'Petzl Summit Evo Axe', 'Therma-Rest NeoAir XTherm'],
        icon: 'ri-landscape-line',
        description: 'Todo lo que necesitas para conquistar los picos más altos'
    },
    'Selva': {
        name: 'Kit Jungle Pro',
        items: ['Mammal Pro 45L Tactical', 'Merrell Moab 3 Tactical', 'Garmin InReach Mini 2', 'BioLite SolarPanel 5+'],
        icon: 'ri-cactus-line',
        description: 'Equipo especializado para expediciones en la Amazonía'
    },
    'Costa & Desierto': {
        name: 'Kit Coastal Adventure',
        items: ['Black Diamond Speed 30', 'Salomon Quest 4 GTX', 'BioLite SolarPanel 5+', 'Black Diamond Spot 400'],
        icon: 'ri-temp-hot-line',
        description: 'Perfecto para dunas, playas y aventuras costeras'
    },
    'Trekking General': {
        name: 'Kit Explorer',
        items: ['Osprey Aether 65 Elite', 'La Sportiva Nepal Cube', 'Black Diamond Spot 400', 'Garmin InReach Mini 2'],
        icon: 'ri-footprint-line',
        description: 'El kit versátil para cualquier tipo de trekking'
    }
};

const guides = [
    {
        id: 1,
        name: 'Carlos "El Puma" Mamani',
        specialty: 'Alta Montaña',
        languages: ['Español', 'Quechua', 'Inglés'],
        exp: '15 años',
        img: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1887&auto=format&fit=crop',
        desc: 'Especialista en rutas de más de 5000msnm. Certificado UIAGM.'
    },
    {
        id: 2,
        name: 'Sarah "La Lince" Jenkins',
        specialty: 'Trekking & Flora',
        languages: ['Inglés', 'Español', 'Francés'],
        exp: '8 años',
        img: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=2070&auto=format&fit=crop',
        desc: 'Bióloga experta en la biodiversidad de los Andes y Amazonía.'
    },
    {
        id: 3,
        name: 'Marco "Condor" Quispe',
        specialty: 'Cultura Inca',
        languages: ['Español', 'Quechua'],
        exp: '20 años',
        img: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=2070&auto=format&fit=crop',
        desc: 'Historiador local con acceso a rutas sagradas exclusivas.'
    },
    {
        id: 4,
        name: 'Elena "River" Tuanama',
        specialty: 'Selva & Kayak',
        languages: ['Español', 'Portugués'],
        exp: '12 años',
        img: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1888&auto=format&fit=crop',
        desc: 'Nacida en el Amazonas, experta en supervivencia y navegación.'
    }
];

// Exportar para uso global
window.tours = tours;
window.events = events;
window.equips = equips;
window.guides = guides;
window.tourEquipmentMap = tourEquipmentMap;
window.kitTemplates = kitTemplates;
