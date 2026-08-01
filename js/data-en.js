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
        img: 'assets/images/destinos/cusco/trekking.jpg',
        detail: 'El "Holy Grail" del trekking. La ruta más famosa de América hacia Machu Picchu.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Camino Inca a Machu Picchu de 4 días tiene una dificultad alta y un precio desde $2,450. Se recorren 43 km alcanzando los 4,215 msnm. Requiere reserva con 6 meses de anticipación por normas gubernamentales. La mejor temporada es de mayo a octubre (temporada seca).',
        faqs: [
            { q: '¿Con cuánta anticipación debo reservar?', a: 'Por regulaciones del gobierno peruano (solo 500 cupos diarios), se requiere reservar con al menos 6 meses de antelación.' },
            { q: '¿Qué tan difícil es el Camino Inca?', a: 'Es de dificultad alta. El Day 2 incluye un ascenso prolongado hasta los 4,215 metros sobre el nivel del mar.' },
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
            'Trekking por el original Qhapaq Ñan (Camino Inca)',
            'Exploración de ruinas intactas en el bosque nuboso',
            'Despertar en campamentos con vista a nevados',
            'Entrada triunfal a Machu Picchu por la Puerta del Sol (Inti Punku)'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: El Paso de los Incas. Inicio en el Km 82. Trekking por el valle del río Urubamba hasta llegar al campamento de Wayllabamba.' },
            { day: 2, desc: 'Day 2: El Desafío del Dead Woman\'s Pass. Ascenso letal a 4,215 msnm. El día más duro pero más gratificante. Descenso al valle de Pacaymayo.' },
            { day: 3, desc: 'Day 3: Viaje en el Tiempo. Trekking por la selva nubosa pasando por ruinas intactas (Runkurakay, Sayacmarca, Wiñay Wayna). El día visualmente más hermoso.' },
            { day: 4, desc: 'Day 4: La Puerta del Sol. Despertar a las 3:30 AM para cruzar la Puerta del Sol (Inti Punku) y ver el amanecer sobre Machu Picchu. Retorno a Cusco en tren.' }
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
        title: 'Ciclismo Downhill Abra Málaga',
        dept: 'Cusco',
        price: 180,
        duration: '1 día',
        difficulty: 'Alta',
        img: 'assets/images/destinos/cusco/ciclismo.jpg',
        detail: 'Descenso vertiginoso desde los 4,316m hasta la selva inca.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El descenso en bicicleta por el Abra Málaga cuesta $180 y dura todo el día. Bajarás desde los 4,316 msnm a lo largo de sinuosas carreteras de montaña, cruzando diferentes pisos altitudinales hasta llegar a la cálida ceja de selva.',
        faqs: [
            { q: '¿Necesito experiencia previa?', a: 'Se requiere dominio de la bicicleta y buena reacción, el descenso es veloz y en parte por carretera asfaltada y trocha.' },
            { q: '¿Se provee equipo de protección?', a: 'Sí, proveemos bicicletas profesionales de downhill, casco integral, rodilleras, coderas y guantes.' },
            { q: '¿Cuánto dura el descenso?', a: 'Aproximadamente 3 a 4 horas de puro descenso en bicicleta.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso parcial hasta 3 días antes',
            duration: '1 día (8 horas)',
            availability: 'Salidas diarias',
            guide: 'Instructor de MTB Bilingüe',
            groupSize: 'Máximo 8 ciclistas'
        },
        whatYouDo: [
            'Inicia el descenso a los pies del imponente Nevado Verónica (4,316 msnm)',
            'Siente la adrenalina bajando a alta velocidad por carreteras de montaña',
            'Atraviesa nubes y neblina andina hasta llegar al calor de la selva',
            'Disfruta de vistas espectaculares del Valle Sagrado'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: Adrenalina pura. Salida de Cusco a las 7:00 AM hacia el Abra Málaga (4,316m). Breve charla de seguridad y entrega de equipo. Descenso de más de 3 horas en bicicleta hasta Huamanmarca. Almuerzo buffet y retorno a Cusco.' }
        ],
        inc: [
            'Bicicleta de Montaña (Suspensión Completa)',
            'Equipo de protección completo (Casco integral, rodilleras)',
            'Guía instructor experto',
            'Vehículo de apoyo durante todo el descenso',
            'Almuerzo buffet'
        ],
        notSuitable: ['Personas sin dominio de bicicleta', 'Menores de 14 años'],
        meetingPoint: 'Plaza San Francisco, Cusco',
        importantInfo: 'Traer ropa deportiva cómoda y una casaca cortavientos.',
        steps: [{ n: 'G', t: 'Abra Málaga', d: 'Inicio' }, { n: 'ri-riding-line', t: 'Descenso', d: 'Bicicleta' }, { n: 'dot', t: 'Huamanmarca', d: 'Final' }],
        sensoryVariants: {
            landscape: 'Siente el cambio drástico de temperatura y paisaje, desde los gélidos glaciares andinos hasta el denso verdor amazónico.',
            comfort: 'Disfruta de la seguridad de contar con un vehículo escolta en todo momento detrás de ti.',
            action: 'Desafía la gravedad y alcanza velocidades extremas en una de las rutas de downhill más largas de Sudamérica.'
        }
    },
    {
        id: 3,
        title: 'Montaña de los 7 Colores Express',
        dept: 'Cusco',
        price: 450,
        duration: '1 día',
        difficulty: 'Media-Alta',
        img: 'assets/images/destinos/cusco/montana.jpg',
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
            'Breakfast y almuerzo buffet andino incluido'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: Conquista la Cumbre. Recojo a las 4:00 AM para ganarle a las multitudes. Breakfast buffet en Cusipata. Trekking de 1.5 horas desafiando la altitud hasta el mirador de Vinicunca (5,200m). Descenso, almuerzo y retorno a Cusco a las 5:00 PM.' }
        ],
        inc: ['Transporte turístico de primera', 'Guía profesional bilingüe', 'Balón de oxígeno de emergencia', 'Breakfast y Almuerzo Buffet andino'],
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
        img: 'assets/images/destinos/cusco/choquequirao.jpg',
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
            { day: 1, desc: 'Day 1: Descenso al Infierno Verde. Trekking desde Capuliyoc bajando en picada hacia el ardiente Cañón del Apurímac. Campamento en Playa Rosalina.' },
            { day: 2, desc: 'Day 2: La Pared Inclinada. Ascenso brutal en zigzag hacia Marampata. Llegada por la tarde al campamento base de Choquequirao.' },
            { day: 3, desc: 'Day 3: La Ciudad Perdida. Day completo para explorar a solas esta megaestructura inca. Atardecer mágico en las terrazas agrícolas.' },
            { day: 4, desc: 'Day 4: El Retorno del Guerrero. Descenso al cañón y último ascenso de regreso a la civilización (Cachora). Retorno a Cusco.' }
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
        img: 'https://images.unsplash.com/photo-1583417319070-4a69db38a482',
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
            { day: 1, desc: 'Days 1-2: Aguas Termales y Glaciares. De Tinki hacia Upis. Baño termal frente al glaciar. Cruce del primer paso (Arapa) a 4,850m.' },
            { day: 2, desc: 'Days 3-4: El Techo del Mundo. Cruce del paso Palomani (5,100 msnm), el punto más alto. Observación de vicuñas salvajes.' },
            { day: 3, desc: 'Days 5-6: Las Lagunas Turquesas. Descenso pasando por las espectaculares 7 lagunas hasta Pacchanta y retorno a Cusco.' }
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
        img: 'assets/images/destinos/huaraz/tour_6.jpg',
        detail: 'El circuito clásico más espectacular de la Cordillera Blanca.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Trekking Santa Cruz (4 días) tiene dificultad media-alta y cuesta $1,200. Cruza la Cordillera Blanca por valles glaciares, alcanzando su punto máximo en el Paso Punta Unión (4,750m). Apto para senderistas con aclimatación previa. Salidas lunes y jueves.',
        faqs: [
            { q: '¿Qué tan frío es por las noches?', a: 'Las temperaturas bajan a -5°C. Se requiere sleeping bag de plumas.' },
            { q: '¿Cuál es la altitud máxima?', a: 'Se alcanza el mítico Paso Punta Unión a 4,750 metros sobre el nivel del mar.' }
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
            'Despertar frente al Nevado Alpamayo',
            'Trekking por valles glaciares turquesas'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1 (Cashapampa a Llamacorral): 06:00 AM: Recojo en su hotel en Huaraz. 06:30 AM - 09:30 AM: Transporte privado hacia Cashapampa (2,900m). 10:00 AM: Inicio del trekking por el valle. 01:00 PM: Almuerzo campestre. 04:00 PM: Llegada al campamento Llamacorral (3,760m). 06:30 PM: Cena y pernocte.' },
            { day: 2, desc: 'Day 2 (Llamacorral a Taullipampa): 06:00 AM: Despertar con mate de coca y desayuno. 07:30 AM: Trekking pasando por las lagunas Ichiccocha y Jatuncocha. 12:30 PM: Almuerzo frente a los glaciares. 03:30 PM: Llegada al campamento Taullipampa (4,250m) con vista al Alpamayo. 06:30 PM: Cena caliente.' },
            { day: 3, desc: 'Day 3 (Taullipampa a Paria): 05:30 AM: Breakfast temprano. 06:30 AM: Inicio del duro ascenso al Paso Punta Unión (4,750m). 10:30 AM: Cumbre en el paso, fotos y descanso. 11:30 AM: Descenso abrupto. 01:30 PM: Almuerzo en ruta. 04:00 PM: Campamento Paria (3,870m).' },
            { day: 4, desc: 'Day 4 (Paria a Vaquería y Retorno): 06:30 AM: Breakfast. 08:00 AM: Trekking final hacia el pueblo de Vaquería cruzando bosques de queñuales. 11:30 AM: Llegada a Vaquería. 12:00 PM: Transporte por el paso Portachuelo (espectaculares vistas de las lagunas de Llanganuco). 04:00 PM: Retorno a Huaraz y fin del servicio.' }
        ],
        inc: [
            'Recojo desde el hotel en Huaraz (06:00 AM)',
            'Transporte privado ida y vuelta',
            'Guía Oficial de Trekking',
            'Cocinero y pensión completa',
            'Burros y arrieros (máx 5kg por persona)',
            'Carpas de alta montaña 4 estaciones'
        ],
        notSuitable: ['Menores de 10 años', 'Personas con problemas de rodilla'],
        meetingPoint: 'Su hotel en Huaraz (06:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Sleeping bag para -10°C, botas de trekking, linterna frontal. NO INCLUYE: Bolsa de dormir, desayuno del primer día ni cena del último día, ticket de ingreso al Parque Nacional (S/ 60).',
        steps: [{ n: 'G', t: 'Cashapampa', d: 'Inicio' }, { n: 'ri-mountain-fill', t: 'Punta Unión', d: '4,750m' }, { n: 'dot', t: 'Vaquería', d: 'Final' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 7,
        title: 'Expedición Nevado Huascarán 7D',
        dept: 'Huaraz',
        price: 4500,
        duration: '7 días',
        difficulty: 'Experto',
        img: 'assets/images/destinos/huaraz/alpinismo.jpg',
        detail: 'Conquista la montaña tropical más alta del mundo (6,768m).',
        last_verified: '2026-06-30',
        direct_answer_block: 'La expedición al Huascarán (7 días) cuesta $4,500. Es alta montaña (6,768m) cruzando paredes de hielo y grietas, con guías UIAGM (1x2).',
        faqs: [
            { q: '¿Puedo ir si no tengo experiencia técnica?', a: 'No. El Huascarán requiere uso avanzado de piolets, crampones y cuerdas.' }
        ],
        genInfo: {
            cancelPolicy: 'Actividad no reembolsable',
            duration: '7 días / 6 noches',
            availability: 'Temporada Seca (Junio a Agosto)',
            guide: 'Guía UIAGM',
            groupSize: 'Expedición técnica reducida'
        },
        whatYouDo: [
            'Escalada técnica en hielo puro',
            'Supervivencia en campos de altura',
            'Conquista el Huascarán (6,768m)'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 05:00 AM Recojo. 08:00 AM Llegada a Musho. 09:00 AM a 02:00 PM Ascenso al Campo Base (4,200m). Tarde de hidratación.' },
            { day: 2, desc: 'Day 2: 07:00 AM Breakfast. 08:30 AM Ascenso por la morrena (rocas) hasta el Glaciar Campo 1 (5,300m). Llegada 02:00 PM. Armado de carpas sobre el hielo.' },
            { day: 3, desc: 'Day 3: 06:00 AM Salida táctica sorteando grietas y escalando La Canaleta (zona de avalanchas). 01:00 PM Llegada al Campo 2 (La Garganta, 6,000m).' },
            { day: 4, desc: 'Day 4: ¡Day de Cumbre! 12:00 AM (Medianoche): Despertar, mate caliente. 01:00 AM: Inicio del ataque a la cumbre en oscuridad total. 08:00 AM: ¡CUMBRE SUR (6,768m)! 09:00 AM a 03:00 PM: Descenso agotador de regreso al Campo 2 para descansar.' },
            { day: 5, desc: 'Day 5: 08:00 AM Breakfast en La Garganta. Descenso técnico usando rápeles hasta el Campo 1 (5,300m).' },
            { day: 6, desc: 'Day 6: Descenso final desde Campo 1 hasta el Campo Base.' },
            { day: 7, desc: 'Day 7: 08:00 AM Trekking de retorno a Musho. 12:00 PM Vehículo de regreso. 02:00 PM Llegada a Huaraz. Celebración.' }
        ],
        inc: [
            'Recojo desde el hotel (05:00 AM)',
            'Guía Oficial de Alta Montaña UIAGM (1 por cada 2 pax)',
            'Carpas de alta montaña de expedición, comida hipercalórica',
            'Cuerdas dinámicas, estacas de nieve, tornillos de hielo',
            'Porteros de altura y arrieros hasta campo base',
            'Transporte privado ida y vuelta'
        ],
        notSuitable: ['Principiantes', 'Personas sin experiencia en crampones'],
        meetingPoint: 'Recojo en hotel en Huaraz (05:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Equipo personal completo (Botas de plástico, piolet técnico, crampones, ropa de plumas para -20°C). NO INCLUYE: Alquiler de equipo personal técnico, bolsa de dormir para -20°C, ticket Huascarán, seguro de rescate.',
        steps: [{ n: 'G', t: 'Musho', d: 'Base' }, { n: 'ri-vip-crown-fill', t: 'Cumbre Sur', d: '6,768m' }, { n: 'dot', t: 'Huaraz', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 8,
        title: 'Trekking Laguna 69 y Llanganuco',
        dept: 'Huaraz',
        price: 350,
        duration: '1 día',
        difficulty: 'Alta',
        img: 'assets/images/destinos/huaraz/trekking.jpg',
        detail: 'El desafío de aclimatación más hermoso de la Cordillera Blanca.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Trekking a Laguna 69 es de 1 día y cuesta $350. Sube hasta los 4,600 msnm para ver una espectacular laguna turquesa.',
        faqs: [
            { q: '¿Cuántas horas de caminata son?', a: 'Aproximadamente 3 horas de subida pronunciada y 2 horas de bajada.' }
        ],
        genInfo: {
            cancelPolicy: 'Cancelación gratuita hasta 24h antes',
            duration: '1 día (12 horas intensas)',
            availability: 'Salidas diarias garantizadas',
            guide: 'Guía local experto',
            groupSize: 'Máximo 15 participantes'
        },
        whatYouDo: [
            'Trekking espectacular bajo el Nevado Chacraraju',
            'Fotografía las aguas esmeraldas de Llanganuco',
            'Alcanza la Laguna 69 a 4,600m'
        ],
        fullItinerary: [
            { day: 1, desc: '05:00 AM: Recojo en su hotel en Huaraz. 07:30 AM: Parada en Yungay para tomar desayuno (no incluido). 08:30 AM: Ingreso al Parque Nacional y parada fotográfica en las lagunas de Llanganuco. 09:30 AM: Llegada a Cebollapampa (3,900m) e inicio del trekking. 12:30 PM: Llegada a la Laguna 69 (4,600m). 1 hora para comer box lunch y fotos. 01:30 PM: Inicio del descenso. 03:30 PM: Llegada al bus en Cebollapampa. 06:30 PM: Llegada a Huaraz.' }
        ],
        inc: [
            'Recojo desde su hotel céntrico (05:00 AM)',
            'Transporte turístico equipado con oxígeno y botiquín',
            'Guía Oficial de Turismo especializado en trekking',
            'Tickets de ingreso al Parque Nacional Huascarán'
        ],
        notSuitable: ['Sedentarios', 'Mala oxigenación'],
        meetingPoint: 'Recojo en hotel (05:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Agua (mínimo 2L), box lunch/snacks energéticos, casaca cortavientos, pastillas para el mal de altura. NO INCLUYE: Breakfast, almuerzo, caballos de emergencia.',
        steps: [{ n: 'G', t: 'Cebollapampa', d: 'Ascenso' }, { n: 'ri-drop-fill', t: 'Laguna 69', d: '4,600m' }, { n: 'dot', t: 'Huaraz', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 9,
        title: 'Glaciar Pastoruri y Puya Raimondi',
        dept: 'Huaraz',
        price: 280,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/huaraz/tour_9.jpg',
        detail: 'Ruta del Cambio Climático y aclimatación alpina.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El tour al Glaciar Pastoruri dura medio día y cuesta $280. Ideal como primera excursión para aclimatar el cuerpo, alcanzando 5,000m.',
        faqs: [
            { q: '¿Hay que caminar mucho?', a: 'No. El bus llega cerca del glaciar y la caminata dura solo 45 minutos.' }
        ],
        genInfo: {
            cancelPolicy: 'Cancelación gratuita hasta 12h antes',
            duration: '7 horas de recorrido',
            availability: 'Salidas diarias a las 09:00 AM',
            guide: 'Guía bilingüe',
            groupSize: 'Ideal para familias'
        },
        whatYouDo: [
            'Camina sobre un glaciar milenario en retroceso',
            'Conoce la planta andina más alta del mundo: Puya Raimondi'
        ],
        fullItinerary: [
            { day: 1, desc: '09:00 AM: Recojo en su hotel en Huaraz. 10:30 AM: Parada en el Valle de Pachacoto para degustar mate de coca. 11:30 AM: Parada en aguas gasificadas de Pumapampa y Puya Raimondi. 01:00 PM: Llegada al parqueo base del Pastoruri (4,800m). 01:00 a 02:00 PM: Trekking de ascenso hacia el glaciar (5,000m). 02:00 a 02:45 PM: Exploración de la cueva de hielo. 03:00 PM: Descenso al bus. 03:30 PM: Almuerzo en restaurante local (no incluido). 05:30 PM: Llegada a Huaraz.' }
        ],
        inc: [
            'Recojo desde el hotel (09:00 AM)',
            'Bus turístico con calefacción y botiquín de oxígeno',
            'Guía bilingüe experto en glaciología básica',
            'Ticket de ingreso a la comunidad y al Parque Huascarán'
        ],
        notSuitable: ['Bebés menores de 1 año', 'Personas con cardiopatías severas'],
        meetingPoint: 'Recojo en hotel (09:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Ropa muy abrigadora (gorro de lana, guantes), lentes polarizados. NO INCLUYE: Almuerzo, alquiler de caballos en la base (S/ 20 aprox).',
        steps: [{ n: 'G', t: 'Huaraz', d: 'Salida' }, { n: 'ri-snowy-fill', t: 'Pastoruri', d: 'Glaciar' }, { n: 'dot', t: 'Huaraz', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 10,
        title: 'Nevado Ishinca Base Camp 3D',
        dept: 'Huaraz',
        price: 1600,
        duration: '3 días',
        difficulty: 'Técnica',
        img: 'assets/images/destinos/huaraz/tour_10.jpg',
        detail: 'Tu primer "Cincomil" y entrenamiento de cuerdas en glaciar.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La expedición Ishinca Base Camp (3 días) cuesta $1,600. Es el "cincomil" (5,530m) ideal para iniciarse en montañismo con refugio andino.',
        faqs: [
            { q: '¿Necesito botas cramponables?', a: 'Sí, es obligatorio el uso de botas de alta montaña rígidas compatibles.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso del 50% hasta 5 días antes',
            duration: '3 días / 2 noches',
            availability: 'Temporada Seca (Mayo a Septiembre)',
            guide: 'Guía UIAGM',
            groupSize: 'Máximo 4 personas por guía'
        },
        whatYouDo: [
            'Alojamiento en el Refugio Andino Ishinca',
            'Escalada técnica al pico Ishinca (5,530m)',
            'Taller intensivo de cuerdas, piolets y crampones'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 08:00 AM: Recojo en hotel. 09:30 AM: Llegada a Pashpa (3,650m) e inicio de caminata de 4h. 02:00 PM: Llegada al Refugio Ishinca (4,350m). 03:00 a 05:00 PM: Clínica de nudos y uso de equipo. 06:30 PM: Cena en refugio.' },
            { day: 2, desc: 'Day 2: 02:30 AM: Despertar y desayuno. 03:00 AM: Ascenso por morrena. 05:30 AM: Llegada al glaciar y encordamiento. 08:30 AM: Cumbre Nevado Ishinca (5,530m). 09:30 AM: Descenso al refugio. 01:00 PM: Retorno al refugio y descanso.' },
            { day: 3, desc: 'Day 3: 08:00 AM: Breakfast montañero. 09:00 AM: Descenso hacia Pashpa. 01:00 PM: Encuentro con transporte. 02:30 PM: Retorno a su hotel en Huaraz.' }
        ],
        inc: [
            'Recojo y retorno en vehículo privado (08:00 AM)',
            'Estadía (2 noches) en camas del Refugio Andino Ishinca',
            'Guía de Montaña Certificado (UIAGM o AGMP)',
            'Alimentación completa (Almuerzo Day 1 hasta Breakfast Day 3)',
            'Equipo técnico colectivo',
            'Burros de carga'
        ],
        notSuitable: ['Personas sin estado físico apto', 'Falta de aclimatación a 4,500m+'],
        meetingPoint: 'Recojo en hotel (08:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Equipo personal (Botas cramponables, piolet, crampones, arnés, casco, ropa goretex). NO INCLUYE: Alquiler de equipo personal (aprox $50/día), seguro contra accidentes.',
        steps: [{ n: 'G', t: 'Pashpa', d: 'Inicio' }, { n: 'ri-vip-crown-fill', t: 'Ishinca', d: '5,530m' }, { n: 'dot', t: 'Huaraz', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    // IQUITOS (5)
    {
        id: 11,
        title: 'Expedición Pacaya Samiria 5D',
        dept: 'Iquitos',
        price: 2800,
        duration: '5 días',
        difficulty: 'Media-Alta',
        img: 'assets/images/destinos/iquitos/tour_11.jpg',
        detail: 'Inmersión profunda en la selva de los espejos. Kayak y pirañas.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La expedición a Pacaya Samiria (5 días) tiene un precio de $2,800. Te adentrarás en la Reserva Nacional navegando en kayak, pescando pirañas y buscando delfines rosados en su hábitat natural.',
        faqs: [
            { q: '¿Hay señal de celular?', a: 'No, estaremos totalmente desconectados en la selva profunda.' },
            { q: '¿Dormimos en carpas o lodge?', a: 'Dormimos en plataformas elevadas con mosquiteros y tiendas de campaña especializadas para la selva.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso del 50% hasta 15 días antes',
            duration: '5 días / 4 noches',
            availability: 'Salidas semanales (Martes)',
            guide: 'Guía nativo bilingüe',
            groupSize: 'Máximo 6 aventureros'
        },
        whatYouDo: [
            'Navega en kayak por el bosque inundado',
            'Pesca de pirañas de manera tradicional',
            'Avistamiento de delfines rosados y perezosos',
            'Trekkings de interpretación de flora medicinal'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 07:00 AM Recojo en hotel/aeropuerto en Iquitos. 08:30 AM Viaje terrestre a Nauta. 10:30 AM Abordaje de lancha rápida. 02:00 PM Ingreso a la Reserva Pacaya Samiria. Almuerzo a bordo. 04:30 PM Llegada al campamento base. 06:30 PM Cena y expedición nocturna en canoa.' },
            { day: 2, desc: 'Day 2: 05:30 AM Avistamiento de aves al amanecer. 08:00 AM Breakfast. 09:30 AM Kayak por los tributarios (búsqueda de nutrias gigantes). 01:00 PM Almuerzo estilo selva. 03:00 PM Pesca de pirañas. 07:00 PM Cena.' },
            { day: 3, desc: 'Day 3: 07:00 AM Breakfast. 08:30 AM Trekking profunda de supervivencia (orientación y agua de lianas). 12:30 PM Almuerzo. 03:30 PM Búsqueda del delfín rosado. 07:30 PM Fogata y mitos de la selva.' },
            { day: 4, desc: 'Day 4: 08:00 AM Breakfast. 09:30 AM Visita a comunidad ribereña para aprender técnicas de cerbatana y recolección. 01:00 PM Almuerzo. Tarde libre para nadar en zona segura.' },
            { day: 5, desc: 'Day 5: 07:00 AM Breakfast. 08:00 AM Desmontaje de campamento. 09:00 AM Inicio del viaje de retorno por el río Marañón. 12:30 PM Llegada a Nauta y almuerzo. 03:30 PM Drop-off en Iquitos.' }
        ],
        inc: [
            'Recojo desde el aeropuerto u hotel (07:00 AM)',
            'Transporte terrestre y lancha rápida',
            'Guía naturalista experto de la zona',
            'Chef de selva (todas las comidas incluidas)',
            'Equipo de campamento y kayaks',
            'Tickets de ingreso a la Reserva Nacional'
        ],
        notSuitable: ['Personas alérgicas severas a picaduras de insectos', 'Menores de 8 años'],
        meetingPoint: 'Aeropuerto Internacional o Hotel en Iquitos (07:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Ropa ligera de colores claros (manga larga), repelente extra fuerte con DEET, poncho para lluvia, linterna frontal, bloqueador, sombrero de ala ancha, cámara con protección contra el agua. NO INCLUYE: Propinas, bebidas alcohólicas.',
        steps: [{ n: 'G', t: 'Iquitos', d: 'Salida' }, { n: 'ri-leaf-fill', t: 'Samiria', d: 'Selva' }, { n: 'dot', t: 'Iquitos', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 12,
        title: 'Retiro Ayahuasca Pro 7D',
        dept: 'Iquitos',
        price: 3500,
        duration: '7 días',
        difficulty: 'Espiritual',
        img: 'assets/images/destinos/iquitos/tour_12.jpg',
        detail: 'Viaje místico en la Amazonía liderado por chamanes Shipibos.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Retiro de Ayahuasca (7 días) cuesta $3,500. Es una profunda experiencia de limpieza espiritual en medio de la jungla con 3 ceremonias sagradas y acompañamiento psicológico.',
        faqs: [
            { q: '¿Hay un proceso médico previo?', a: 'Sí, requerimos una evaluación médica y psicológica antes de confirmar la reserva.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso 100% hasta 30 días antes',
            duration: '7 días / 6 noches',
            availability: 'Retiros mensuales (Luna Nueva)',
            guide: 'Maestro Onaya (Shipibo-Konibo) y Facilitador',
            groupSize: 'Máximo 10 pasajeros por sesión'
        },
        whatYouDo: [
            'Participa en 3 ceremonias sagradas de Ayahuasca',
            'Integración psicológica diaria',
            'Dietas tradicionales de limpieza (sin sal, azúcar ni aceites)',
            'Baños de florecimiento con plantas aromáticas'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 09:00 AM Recojo y viaje en bote al centro holístico. 12:00 PM Llegada e instalación. 02:00 PM Charla de introducción. 04:00 PM Purga inicial con tabaco o plantas eméticas.' },
            { day: 2, desc: 'Day 2: 08:00 AM Breakfast de dieta. 10:00 AM Consultas privadas con el chamán. 06:00 PM Preparación espiritual. 08:00 PM PRIMERA CEREMONIA DE AYAHUASCA. Silencio absoluto.' },
            { day: 3, desc: 'Day 3: 09:00 AM Breakfast. 11:00 AM Círculo de integración grupal (análisis de visiones). Tarde de descanso en hamacas. Baños de florecimiento.' },
            { day: 4, desc: 'Day 4: 08:00 AM Breakfast. Trekking por el jardín botánico de plantas maestras. 08:00 PM SEGUNDA CEREMONIA DE AYAHUASCA.' },
            { day: 5, desc: 'Day 5: 10:00 AM Integración. Tarde libre para meditación y arteterapia en la selva.' },
            { day: 6, desc: 'Day 6: 08:00 PM TERCERA Y ÚLTIMA CEREMONIA (Sellado y sanación final).' },
            { day: 7, desc: 'Day 7: 08:00 AM Rompimiento de la dieta (comida normal). 10:00 AM Círculo de cierre. 12:00 PM Retorno a Iquitos.' }
        ],
        inc: [
            'Transporte fluvial Iquitos - Centro Holístico',
            'Alojamiento en tambo individual privado',
            'Alimentación estricta de dieta amazónica',
            'Maestros curanderos y facilitadores de integración',
            '3 Ceremonias de Ayahuasca y 1 Purga'
        ],
        notSuitable: ['Personas con antecedentes de esquizofrenia o psicosis', 'Personas que tomen antidepresivos (ISRS)', 'Problemas cardíacos graves'],
        meetingPoint: 'Oficina de Retiros en Iquitos (09:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Ropa blanca o clara cómoda, diario personal, botella de agua reutilizable. NO INCLUYE: Pasajes aéreos. PREPARACIÓN: Requiere dieta estricta (cero alcohol, drogas, o carnes rojas) 2 semanas antes.',
        steps: [{ n: 'G', t: 'Iquitos', d: 'Llegada' }, { n: 'ri-moon-fill', t: 'Maloca', d: 'Ceremonia' }, { n: 'dot', t: 'Iquitos', d: 'Cierre' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 13,
        title: 'Búsqueda de Caimanes Nocturna 1D',
        dept: 'Iquitos',
        price: 150,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'assets/images/destinos/iquitos/tour_13.jpg',
        detail: 'Safari nocturno por el río más caudaloso del mundo.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La Búsqueda de Caimanes Nocturna dura unas horas en la tarde-noche y cuesta $150. Experimentarás la selva en la oscuridad a bordo de una canoa de madera.',
        faqs: [
            { q: '¿Es peligroso?', a: 'No, nuestros guías tienen décadas de experiencia en el manejo y observación segura de reptiles amazónicos.' }
        ],
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '6 horas (Tarde-Night)',
            availability: 'Salidas diarias',
            guide: 'Guía rastreador de fauna',
            groupSize: 'Máximo 8 personas'
        },
        whatYouDo: [
            'Navegación al atardecer viendo la caída del sol en el Amazonas',
            'Uso de linternas potentes para buscar ojos brillantes en la orilla',
            'Escucha la ensordecedora sinfonía de insectos y ranas nocturnas',
            'Captura y liberación segura de caimanes pequeños por el guía'
        ],
        fullItinerary: [
            { day: 1, desc: '04:00 PM: Recojo en su hotel. 04:30 PM: Traslado al puerto Bellavista-Nanay. 05:00 PM: Navegación por el río Nanay hacia el Amazonas. 06:00 PM: Contemplación del Sunset amazónico desde el bote. 06:30 PM: Oscuridad total. Inicio de la exploración con linternas por los afluentes inundados (búsqueda de caimanes blancos y negros). 08:30 PM: Retorno navegando bajo las estrellas. 09:30 PM: Llegada a Iquitos y traslado al hotel.' }
        ],
        inc: [
            'Traslado hotel-puerto-hotel',
            'Bote tradicional (peque-peque) con motor silencioso',
            'Guía especialista en fauna nocturna',
            'Poncho de lluvia y linterna'
        ],
        notSuitable: ['Niños hiperactivos que no puedan mantener silencio en el bote'],
        meetingPoint: 'Recojo en su hotel en Iquitos (04:00 PM)',
        importantInfo: 'QUÉ LLEVAR: Pantalón largo, repelente, cámara con buena captación de luz. NO INCLUYE: Cena (cenar antes o llevar snacks).',
        steps: [{ n: 'G', t: 'Puerto', d: '04:00 PM' }, { n: 'ri-eye-fill', t: 'Río', d: 'Caimanes' }, { n: 'dot', t: 'Hotel', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 14,
        title: 'Amazon Canopy Walkway 1D',
        dept: 'Iquitos',
        price: 350,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/iquitos/canopy.jpg',
        detail: 'Puentes colgantes sobre la copa de los árboles a 35m de altura.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Amazon Canopy Walkway es una excursión de 1 día que cuesta $350. Caminarás por una red de puentes colgantes suspendidos a 35 metros sobre el suelo, observando aves, monos y el dosel de la selva desde arriba.',
        faqs: [
            { q: '¿Qué tan altos son los puentes?', a: 'Están a 35 metros de altura y tienen 500 metros de largo en total.' },
            { q: '¿Son seguros?', a: 'Totalmente. Son plataformas estabilizadas con cables de acero.' }
        ],
        genInfo: {
            cancelPolicy: 'Gratis 48h antes',
            duration: '8 horas',
            availability: 'Salidas diarias',
            guide: 'Guía bilingüe',
            groupSize: 'Grupos pequeños'
        },
        whatYouDo: [
            'Camina a 35 metros de altura sobre el suelo de la selva',
            'Observa bromelias, orquídeas y aves (tucanes) a nivel de la vista',
            'Aprende sobre la estratificación vertical de la Amazonía',
            'Almuerzo típico selvático incluido'
        ],
        fullItinerary: [
            { day: 1, desc: '07:30 AM: Recojo en hotel. 08:00 AM: Viaje en lancha rápida por el río Amazonas (1.5h). 09:30 AM: Llegada a la reserva privada. Trekking de 30 min por la selva primaria hasta la base del canopy. 10:00 AM: Ascenso a las plataformas. Recorrido de 1 hora por los puentes colgantes, escuchando monos aulladores y aves. 11:30 AM: Descenso. 12:30 PM: Almuerzo en el lodge ecológico. 02:00 PM: Visita a tribu Yagua cercana. 03:30 PM: Retorno a Iquitos.' }
        ],
        inc: [
            'Transporte fluvial rápido',
            'Tickets de ingreso al Canopy',
            'Guía especializado en ornitología básica',
            'Almuerzo buffet selvático (Juane, Tacacho, refresco de camu camu)'
        ],
        notSuitable: ['Personas con acrofobia severa (miedo a las alturas)'],
        meetingPoint: 'Puerto de Iquitos (07:30 AM)',
        importantInfo: 'QUÉ LLEVAR: Zapatillas cerradas con buen agarre, binoculares (indispensable para ver aves), cámara fotográfica con correa de seguridad para que no caiga. NO INCLUYE: Propinas, artesanías en la visita Yagua.',
        steps: [{ n: 'G', t: 'Iquitos', d: 'Salida' }, { n: 'ri-guide-fill', t: 'Canopy', d: '35m Altura' }, { n: 'dot', t: 'Iquitos', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 15,
        title: 'Survival Jungle Camp 3D',
        dept: 'Iquitos',
        price: 1950,
        duration: '3 días',
        difficulty: 'Extrema',
        img: 'assets/images/destinos/iquitos/selva.jpg',
        detail: 'Aprende a sobrevivir en la selva virgen con nativos comandos.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Jungle Survival Camp (3 días) cuesta $1,950 y es de dificultad extrema. Aprenderás a construir refugios, hacer fuego bajo la lluvia, buscar agua y comida, liderado por ex-militares y nativos de la zona.',
        faqs: [
            { q: '¿Vamos a dormir en un hotel?', a: 'NO. Dormirás en un refugio de hojas que tú mismo construirás en medio del lodo.' },
            { q: '¿Llevamos comida?', a: 'Muy poca (arroz y fariña). El objetivo es aprender a pescar y recolectar alimento natural.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso 50% hasta 7 días antes',
            duration: '3 días / 2 noches',
            availability: 'Salidas bajo pedido',
            guide: 'Instructor de Supervivencia',
            groupSize: 'Máximo 4 personas'
        },
        whatYouDo: [
            'Construcción de refugios temporales impermeables con hojas de palmera',
            'Técnicas de obtención de agua potable de lianas (Uña de gato)',
            'Creación de fuego por fricción en un ambiente 90% húmedo',
            'Navegación y orientación táctica sin GPS ni brújula'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 06:00 AM Salida secreta. 09:00 AM Desembarco en una zona remota del río Amazonas. Abandono de tecnología y comida extra. Marcha por la selva virgen de 4 horas abriendo trocha a machete. 01:00 PM Práctica: Identificación de agua y plantas venenosas. 03:00 PM Construcción del campamento base (armar refugio con hojas). 06:00 PM Intento de hacer fuego y pesca nocturna básica. Pernocte en el suelo/hamaca improvisada.' },
            { day: 2, desc: 'Day 2: 05:00 AM Despertar. Breakfast (lo que se haya cazado/pescado). 08:00 AM Taller de trampas para pequeños animales. 12:00 PM Pesca con arco y flecha nativa. Tarde de supervivencia de primer auxilios en selva (qué hacer ante mordedura de serpiente). Night de guardia.' },
            { day: 3, desc: 'Day 3: 06:00 AM Desarme del refugio (dejar sin huella). 08:00 AM Marcha de orientación (el participante lidera la salida al río guiándose por el sol y los árboles). 12:00 PM Extracción en bote. 03:00 PM Retorno a la civilización. Entrega de diploma de supervivencia.' }
        ],
        inc: [
            'Instrucción de supervivencia de élite',
            'Machete personal (te lo llevas de recuerdo)',
            'Hamaca de selva ligera',
            'Botiquín trauma completo llevado por el instructor',
            'Transporte fluvial de extracción'
        ],
        notSuitable: ['Cualquier persona no dispuesta a sufrir hambre, picaduras o barro'],
        meetingPoint: 'Puerto Militar Iquitos (06:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Botas pantaneras de goma altas (obligatorio), 2 mudas de ropa resistentes a rasgaduras, repelente, pastillas purificadoras, muchísima fuerza mental. NO INCLUYE: Comodidades de ningún tipo.',
        steps: [{ n: 'G', t: 'Base', d: 'Drop off' }, { n: 'ri-fire-fill', t: 'Selva', d: 'Supervivencia' }, { n: 'dot', t: 'Civilización', d: 'Pick up' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    // PIURA (5)
    {
        id: 16,
        title: 'Kitesurf Máncora Pro 3D',
        dept: 'Piura',
        price: 850,
        duration: '3 días',
        difficulty: 'Media-Alta',
        img: 'assets/images/destinos/piura/kitesurf.jpg',
        detail: 'Vuela sobre las olas del Pacífico con instructores certificados.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El curso de Kitesurf en Máncora (3 días) cuesta $850. Es dictado exclusivamente por instructores certificados IKO (International Kiteboarding Organization) asegurando estándares internacionales de seguridad.',
        faqs: [
            { q: '¿Necesito experiencia previa?', a: 'No. El curso está diseñado desde cero, comenzando con control de vela en tierra firme.' },
            { q: '¿Qué pasa si no hay viento?', a: 'Reprogramamos la clase o reembolsamos. Solo dictamos clases con viento óptimo.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso por falta de viento 100%',
            duration: '3 días (3 horas diarias)',
            availability: 'Temporada de Vientos (Mayo - Noviembre)',
            guide: 'Instructor Certificado IKO Nivel 2',
            groupSize: 'Clase Privada (1 a 1)'
        },
        whatYouDo: [
            'Control total del Kite de tracción en la arena (ventanas de viento)',
            'Práctica de rescate de tabla en mar abierto (Body drag)',
            'Primeros deslizamientos reales sobre la tabla (Waterstart)',
            'Obtención del carnet IKO válido a nivel mundial'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 09:00 AM Encuentro en la Escuela IKO Máncora. 09:30 AM Teoría de vientos y sistemas de seguridad. 10:30 AM a 12:30 PM Vuelo de kite de entrenamiento en la arena. Tarde libre.' },
            { day: 2, desc: 'Day 2: 10:00 AM Ingreso al mar sin tabla (Body Drag). Aprender a usar la tracción del kite para desplazarse en el agua y recuperar la tabla perdida. 01:00 PM Fin de la sesión.' },
            { day: 3, desc: 'Day 3: 11:00 AM ¡El Waterstart! Práctica de levantarse en la tabla y realizar los primeros metros navegando. 02:00 PM Entrega de certificación IKO internacional.' }
        ],
        inc: [
            'Kite, arnés, barra, leash y tabla profesional de última generación',
            'Casco con radio de comunicación bidireccional',
            'Instructor Certificado IKO permanente',
            'Chaleco salvavidas y seguro de equipo'
        ],
        notSuitable: ['Menores de 12 años', 'Personas que no saben nadar'],
        meetingPoint: 'Escuela de Kitesurf Máncora (09:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Ropa de baño cómoda (rashguard UV recomendado), mucho bloqueador solar resistente al agua, lentes de sol con correa. NO INCLUYE: Alojamiento, alimentación.',
        steps: [{ n: 'G', t: 'Playa', d: 'Teoría' }, { n: 'ri-windy-fill', t: 'Olas', d: 'Kitesurf' }, { n: 'dot', t: 'Máncora', d: 'Certificación' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 17,
        title: 'Buceo Profesional Los Órganos 1D',
        dept: 'Piura',
        price: 320,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/piura/buceo.jpg',
        detail: 'Explora arrecifes en el cruce de dos corrientes oceánicas.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La inmersión de Buceo en Los Órganos (1 día) cuesta $320. Operada bajo los estrictos estándares de PADI, incluye 2 inmersiones profundas en arrecifes llenos de vida.',
        faqs: [
            { q: '¿Qué certificación necesito?', a: 'Se requiere certificación PADI Open Water o equivalente. (Si no tienes, pregunta por nuestro programa Discover Scuba Diving).' },
            { q: '¿El operador es legal?', a: 'Sí. Somos un PADI Dive Center de 5 estrellas autorizado por DICAPI (Marina de Guerra del Perú).' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso 100% por oleaje peligroso',
            duration: '5 horas',
            availability: 'Salidas diarias',
            guide: 'Divemaster / Instructor PADI',
            groupSize: 'Máximo 4 buzos por guía'
        },
        whatYouDo: [
            'Inmersión en arrecifes de piedra con tortugas gigantes y meros',
            'Buceo en una plataforma petrolera inactiva cubierta de coral',
            'Navegación segura en lanchas equipadas con oxígeno de emergencia'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 08:00 AM Encuentro en el Dive Center Los Órganos. Prueba de trajes (wetsuit de 5mm a 7mm). 09:00 AM Zarpe en lancha. 09:40 AM Primera inmersión (aprox 45 min, 18 metros). 10:30 AM Intervalo de superficie con frutas y rehidratación. 11:30 AM Segunda inmersión en locación diferente. 01:00 PM Retorno al muelle y logbook.' }
        ],
        inc: [
            '2 Tanques de oxígeno y lastre',
            'Equipo scuba completo (Regulador, BCD, traje húmedo, aletas, máscara)',
            'Guía PADI Divemaster certificado',
            'Snacks y agua en la embarcación'
        ],
        notSuitable: ['Personas sin certificación de buceo', 'Mujeres embarazadas', 'Vuelos programados dentro de las próximas 18 horas'],
        meetingPoint: 'PADI Dive Center Los Órganos (08:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Toalla, ropa seca para cambiarse, carnet PADI y logbook. NO INCLUYE: Almuerzo, pastillas para el mareo.',
        steps: [{ n: 'G', t: 'Muelle', d: 'Zarpe' }, { n: 'ri-anchor-fill', t: 'Arrecife', d: 'Buceo' }, { n: 'dot', t: 'Órganos', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 18,
        title: 'Cabo Blanco Surf Quest 1D',
        dept: 'Piura',
        price: 300,
        duration: '1 día',
        difficulty: 'Alta',
        img: 'assets/images/destinos/piura/surf.jpg',
        detail: 'Surfea el legendario tubo de Cabo Blanco con instructores ISA.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Surf Quest a Cabo Blanco dura 1 día completo y cuesta $300. Es un viaje guiado por instructores certificados por la International Surfing Association (ISA) diseñado para surfistas experimentados.',
        faqs: [
            { q: '¿Puedo ir si soy principiante?', a: 'No. Cabo Blanco rompe sobre un fondo de roca (reef break) muy peligroso. Exigimos nivel intermedio-avanzado.' },
            { q: '¿El instructor entra al agua?', a: 'Sí, tu coach ISA te guiará en el "line-up" y marcará las mejores olas.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso por falta de olas (Swell Norte)',
            duration: '1 día (8 horas)',
            availability: 'Temporada de Verano (Diciembre - Marzo)',
            guide: 'Instructor de Surf ISA Nivel 2',
            groupSize: 'Máximo 3 surfistas'
        },
        whatYouDo: [
            'Surfea tubos perfectos en la histórica caleta de Hemingway',
            'Coaching táctico avanzado dentro del agua',
            'Grabación de video desde la orilla para análisis técnico',
            'Almuerzo en restaurante de pescadores ancestrales'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 05:30 AM "Dawn Patrol": Salida temprano desde tu hotel hacia Cabo Blanco. 06:30 AM Llegada, análisis de la corriente y marea con tu coach ISA. 07:00 AM Primera sesión intensa de surf (tubos). 10:00 AM Salida, desayuno en la caleta y revisión de video. 11:30 AM Segunda sesión si las condiciones lo permiten. 01:30 PM Almuerzo cevichero. 03:00 PM Retorno al hotel.' }
        ],
        inc: [
            'Transporte 4x4 privado a Cabo Blanco',
            'Coach ISA Nivel 2 en el agua',
            'Sesión de video-análisis',
            'Breakfast y almuerzo local'
        ],
        notSuitable: ['Surfistas principiantes o personas con lesiones recientes'],
        meetingPoint: 'Recojo en su hotel en Máncora/Órganos (05:30 AM)',
        importantInfo: 'QUÉ LLEVAR: Tu propia tabla (preferible shortboard), botines de reef, lycra, leash de repuesto y cera tropical. NO INCLUYE: Alquiler de tabla de surf (disponible por costo extra).',
        steps: [{ n: 'G', t: 'Hotel', d: 'Dawn Patrol' }, { n: 'ri-water-flash-fill', t: 'Cabo Blanco', d: 'Tubos' }, { n: 'dot', t: 'Hotel', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 19,
        title: 'Pesca de Altura Cabo Blanco 1D',
        dept: 'Piura',
        price: 950,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/piura/pesca_altura.jpg',
        detail: 'Atrapa a los gigantes del océano siguiendo reglas IGFA.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La Pesca de Altura cuesta $950 por embarcación. Se realiza en los mismos mares donde se grabó "El Viejo y el Mar", operada por capitanes certificados bajo normas IGFA para Catch & Release del Merlín.',
        faqs: [
            { q: '¿Qué peces buscaremos?', a: 'El objetivo principal es el Merlín Negro, Atún de Aleta Amarilla y Pez Vela.' },
            { q: '¿Puedo quedarme con el pescado?', a: 'Los Merlines y peces pico se liberan estrictamente (Catch & Release). Atunes sí se pueden conservar.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso si las autoridades cierran el puerto',
            duration: '7 horas de mar adentro',
            availability: 'Todo el año (Mejor de Nov a Abril)',
            guide: 'Capitán Certificado IGFA',
            groupSize: 'Chárter privado (Hasta 4 pescadores)'
        },
        whatYouDo: [
            'Navega millas mar adentro en un yate equipado',
            'Lucha durante horas con peces de más de 100 kilos',
            'Aprende técnicas profesionales de trolling',
            'Contribuye a la conservación liberando especies protegidas'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 06:00 AM Embarque en el muelle de Cabo Blanco. 06:30 AM Zarpe mar adentro (aprox 1.5 horas). 08:00 AM Inicio de arrastre de señuelos (Trolling). 10:00 AM a 01:00 PM Acción de pesca y luchas (Pez Vela, Merlín, Atún). 01:00 PM Box lunch abordo. 02:00 PM Retorno al muelle. 03:30 PM Desembarque.' }
        ],
        inc: [
            'Yate de pesca deportiva (Cabin cruiser, baño, fishfinder)',
            'Capitán y marinero certificados',
            'Cañas, carretes Shimano/Penn de clase mundial y carnada',
            'Bebidas frías, cervezas y box lunch completo'
        ],
        notSuitable: ['Personas propensas a mareos severos en alta mar'],
        meetingPoint: 'Muelle de Cabo Blanco (06:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Sombrero, bloqueador FPS 100, lentes polarizados (vitales para ver el agua), pastilla para el mareo tomada 1 hora antes. NO INCLUYE: Traslado desde el hotel al muelle de Cabo Blanco.',
        steps: [{ n: 'G', t: 'Muelle', d: 'Zarpe' }, { n: 'ri-ship-fill', t: 'Alta Mar', d: 'Pesca' }, { n: 'dot', t: 'Cabo Blanco', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 20,
        title: 'Sandboard y Buggies Desierto de Sechura',
        dept: 'Piura',
        price: 150,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/cusco/montana.jpg',
        detail: 'Velocidad y surf en arena en el desierto más grande.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La excursión de Buggies y Sandboard en Sechura (Médano Blanco) cuesta $150. Operado por pilotos certificados por MINCETUR con vehículos tubulares con jaula antivuelco homologada.',
        faqs: [
            { q: '¿Los buggies son seguros?', a: 'Sí, nuestros tubulares pasan revisiones técnicas periódicas y los pilotos son profesionales acreditados.' },
            { q: '¿Tengo que saber Sandboard?', a: 'No, te enseñaremos desde deslizarte acostado hasta usar botas y fijaciones como snowboarder.' }
        ],
        genInfo: {
            cancelPolicy: 'Cancelación gratuita hasta 24h antes',
            duration: '4 horas',
            availability: 'Salidas diarias 03:00 PM',
            guide: 'Piloto certificado MINCETUR',
            groupSize: 'Máximo 8 pasajeros por vehículo'
        },
        whatYouDo: [
            'Recorre dunas gigantes a alta velocidad en un V8',
            'Aprende Sandboarding con tablas profesionales (fijaciones)',
            'Disfruta del atardecer en medio de un inmenso mar de arena'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 03:00 PM Recojo en Piura o Sechura. 04:00 PM Llegada al inicio de las dunas del Médano Blanco. 04:15 PM Recorrido estilo montaña rusa en buggy por las inmensas dunas (45 min). 05:00 PM Inicio de la sesión de Sandboard. 06:00 PM Contemplación del atardecer desértico. 06:45 PM Retorno. 07:30 PM Llegada al punto de inicio.' }
        ],
        inc: [
            'Paseo en Arenero (Tubular) certificado',
            'Tablas de Sandboard (madera para principiantes, tipo snowboard para avanzados)',
            'Piloto profesional y cera para tablas'
        ],
        notSuitable: ['Mujeres embarazadas', 'Personas con problemas graves de columna'],
        meetingPoint: 'Plaza de Armas de Sechura (03:00 PM)',
        importantInfo: 'QUÉ LLEVAR: Lentes de sol cerrados, gorra, zapatillas (no sandalias), bloqueador. NO INCLUYE: Transporte desde Máncora (Sechura está al sur de Piura, a 3h de Máncora).',
        steps: [{ n: 'G', t: 'Sechura', d: 'Buggy' }, { n: 'ri-riding-fill', t: 'Dunas', d: 'Sandboard' }, { n: 'dot', t: 'Sechura', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    // ICA (5)
    {
        id: 21,
        title: 'Buggies y Sandboard Extremo',
        dept: 'Ica',
        price: 180,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/ica/tour_21.jpg',
        detail: 'Montaña rusa de arena en el Oasis de América.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La excursión de Buggies y Sandboard en Huacachina (2 horas) cuesta $180. Operado estrictamente por pilotos certificados por MINCETUR usando tubulares V8 con jaula antivuelco, ofreciendo máxima seguridad y adrenalina.',
        faqs: [
            { q: '¿Los autos son seguros?', a: 'Completamente. Solo trabajamos con operadores formales inscritos en el gremio de turismo de Ica que pasan revisiones técnicas trimestrales.' }
        ],
        genInfo: {
            cancelPolicy: 'Gratis hasta 12h antes',
            duration: '2.5 horas de recorrido',
            availability: 'Salidas diarias (Recomendado 4:00 PM para sunset)',
            guide: 'Piloto Profesional MINCETUR',
            groupSize: 'Hasta 8 pasajeros por tubular'
        },
        whatYouDo: [
            'Navega por dunas gigantes a altas velocidades en un tubular V8',
            'Deslízate en tablas de sandboard profesionales (con fijaciones)',
            'Disfruta de un atardecer dorado con vista panorámica al oasis'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 04:00 PM Punto de encuentro en Huacachina. Charla de seguridad (Briefing). 04:15 PM Inicio del recorrido en las dunas con ascensos verticales y descensos rápidos. 05:00 PM Paradas en dunas altas para instrucción y práctica de sandboarding. 06:00 PM Contemplación del Sunset en lo alto del desierto. 06:30 PM Retorno al oasis.' }
        ],
        inc: [
            'Asiento en Arenero (Tubular) certificado',
            'Tabla de Sandboard tipo snowboard (con fijaciones y botas)',
            'Piloto instructor y pago de tasa de ingreso al desierto'
        ],
        notSuitable: ['Mujeres embarazadas', 'Personas con cirugías recientes de columna'],
        meetingPoint: 'Oficina Operador Autorizado, Oasis de Huacachina (04:00 PM)',
        importantInfo: 'QUÉ LLEVAR: Lentes de sol cerrados para la arena, bloqueador solar, chaqueta cortavientos (hace frío al anochecer).',
        steps: [{ n: 'G', t: 'Oasis', d: 'Briefing' }, { n: 'ri-riding-fill', t: 'Dunas', d: 'Sandboard' }, { n: 'dot', t: 'Oasis', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 22,
        title: 'Kitesurf Bahía de Paracas',
        dept: 'Ica',
        price: 750,
        duration: '3 días',
        difficulty: 'Media-Alta',
        img: 'assets/images/destinos/ica/tour_22.jpg',
        detail: 'Domina los vientos paracas en aguas planas.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El curso de Kitesurf en Paracas cuesta $750 por 3 días. Paracas es famoso por su viento térmico asegurado casi todo el año. Todos los instructores tienen certificación internacional IKO.',
        faqs: [
            { q: '¿Por qué Paracas es ideal?', a: 'El agua es plana y poco profunda en la zona de práctica, y el viento "Paracas" sopla constante a más de 15 nudos casi a diario.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso total si no hay viento',
            duration: '9 horas prácticas totales',
            availability: 'Todo el año (Tardes)',
            guide: 'Instructor Certificado IKO Nivel 2',
            groupSize: 'Clase Semi-Privada (Max 2)'
        },
        whatYouDo: [
            'Aprende a montar el equipo, líneas y sistemas de seguridad',
            'Practica control de tracción del cometa dentro del agua',
            'Ejecuta el "Waterstart" y navega tus primeros metros'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 01:00 PM Teoría de vientos y armado de equipo. Práctica en la playa controlando el kite pequeño. 03:00 PM Fin de sesión.' },
            { day: 2, desc: 'Day 2: 01:00 PM Body drag en el mar (usar el viento para arrastrarse sin tabla). Recuperación de tabla simulada.' },
            { day: 3, desc: 'Day 3: 01:00 PM Waterstart (incorporarse sobre la tabla en el agua). Navegación guiada.' }
        ],
        inc: [
            'Equipo de Kitesurf 2026 (Cometa, barra, arnés, tabla)',
            'Casco con radio para corrección en tiempo real',
            'Instructor IKO',
            'Licencia digital IKO al aprobar'
        ],
        notSuitable: ['Personas que no saben nadar básico'],
        meetingPoint: 'Kite Beach Santo Domingo, Paracas (01:00 PM)',
        importantInfo: 'QUÉ LLEVAR: Wetsuit propio (aunque se provee, es mejor el propio), escarpines de neoprene, mucho bloqueador solar deportivo.',
        steps: [{ n: 'G', t: 'Playa', d: 'Armado' }, { n: 'ri-windy-fill', t: 'Bahía', d: 'Kitesurf' }, { n: 'dot', t: 'Paracas', d: 'IKO' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 23,
        title: 'Vuelo Geoglifos de Nazca',
        dept: 'Ica',
        price: 650,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'assets/images/destinos/ica/tour_23.jpg',
        detail: 'Sobrevuela los misterios del desierto.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El vuelo sobre las Líneas de Nazca (35 minutos) cuesta $650 y se realiza en avionetas Cessna 208 Grand Caravan. Operado bajo estrictas certificaciones DGAC (Dirección General de Aeronáutica Civil).',
        faqs: [
            { q: '¿Me voy a marear?', a: 'La avioneta realiza giros pronunciados para que ambos lados vean las figuras. Toma una pastilla contra el mareo 1 hora antes.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso por mal clima/neblina',
            duration: '35 minutos de vuelo efectivo',
            availability: 'Sujeto a clima (Normalmente de 8:00 AM a 2:00 PM)',
            guide: 'Pilotos Comerciales DGAC',
            groupSize: 'Avioneta de 12 pasajeros'
        },
        whatYouDo: [
            'Observa 13 geoglifos principales (Mono, Araña, Colibrí, etc.)',
            'Escucha la narración copiloto sobre las teorías de Maria Reiche',
            'Experimenta giros en picada ligera para la mejor toma fotográfica'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 08:00 AM Check-in en el aeródromo Maria Reiche. Pesaje y pago de tasa aeroportuaria. 09:30 AM Abordaje a la avioneta Cessna. 09:40 AM Despegue y sobrevuelo de los valles, ingresando al polígono de geoglifos. Observación de la Ballena, Triángulos, Mono, Perro, Cóndor, etc. 10:15 AM Aterrizaje suave y entrega de certificado de vuelo.' }
        ],
        inc: [
            'Vuelo panorámico certificado',
            'Auriculares de aviación para el guiado',
            'Certificado de vuelo nominal'
        ],
        notSuitable: ['Personas que sufren vértigo o problemas cardíacos graves', 'Pánico extremo a volar'],
        meetingPoint: 'Aeródromo Maria Reiche, Nazca',
        importantInfo: 'QUÉ LLEVAR: Pasaporte original o DNI (Obligatorio por ley aeronáutica), cámara lista. NO INCLUYE: Tasa aeroportuaria (aprox. 30 soles que se paga en efectivo).',
        steps: [{ n: 'G', t: 'Aeródromo', d: 'Check-in' }, { n: 'ri-flight-takeoff-fill', t: 'Nazca', d: 'Geoglifos' }, { n: 'dot', t: 'Pista', d: 'Aterrizaje' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 24,
        title: 'Parapente Acantilados de Paracas',
        dept: 'Ica',
        price: 350,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'assets/images/destinos/ica/tour_24.jpg',
        detail: 'Vuela libre sobre la Reserva Nacional.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El vuelo en Parapente Biplaza en Paracas cuesta $350. Es un vuelo tandem de 15 minutos manejado al 100% por un piloto certificado por la API (Asociación Peruana de Instructores de Parapente).',
        faqs: [
            { q: '¿Tengo que saber saltar?', a: 'No, el despegue se hace con viento dinámico desde el acantilado. Solo tienes que dar dos pasos y ya estarás volando con el piloto.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso por falta de viento ascendente',
            duration: '2 horas (Vuelo 15 min)',
            availability: 'Dependiente del viento (Tardes)',
            guide: 'Piloto Tandem API',
            groupSize: '1 persona por piloto'
        },
        whatYouDo: [
            'Vuela impulsado únicamente por las corrientes térmicas',
            'Observa la Playa Roja y el Océano Pacífico desde 200 metros de altura',
            'Siente el silencio absoluto del vuelo sin motor'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 02:00 PM Recojo en Paracas y traslado a los acantilados de la Reserva. 02:30 PM Preparación de la vela, arnés y charla técnica. 03:00 PM Despegue seguro hacia el abismo costero. Vuelo panorámico sostenido por brisa marina. 03:15 PM Aterrizaje en el mismo punto o en la playa inferior. 04:00 PM Retorno.' }
        ],
        inc: [
            'Vuelo Tandem (Piloto certificado)',
            'Video HD grabado con GoPro',
            'Traslado desde Paracas a la zona de despegue'
        ],
        notSuitable: ['Personas de más de 110 kg (por límite de carga de la vela)', 'Miedo paralizante a las alturas'],
        meetingPoint: 'Entrada a Reserva Nacional de Paracas',
        importantInfo: 'QUÉ LLEVAR: Zapatillas ajustadas (no sandalias), chaqueta rompevientos. NO INCLUYE: Ingreso SERNANP a la Reserva.',
        steps: [{ n: 'G', t: 'Acantilado', d: 'Viento' }, { n: 'ri-send-plane-fill', t: 'Cielo', d: 'Vuelo' }, { n: 'dot', t: 'Tierra', d: 'Aterrizaje' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 25,
        title: 'Expedición Cuatrimotos Reserva',
        dept: 'Ica',
        price: 220,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/ica/tour_25.jpg',
        detail: 'Ruta off-road cruzando el desierto amarillo y rojo.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El recorrido en Cuatrimotos (ATV) por Paracas cuesta $220. Liderado por guías oficiales autorizados por SERNANP para no afectar el ecosistema protegido de la Reserva Nacional.',
        faqs: [
            { q: '¿Necesito licencia de conducir?', a: 'No, pero requieres demostrar habilidad básica de manejo en la pista de prueba antes de salir a la reserva.' }
        ],
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '2.5 horas',
            availability: 'Salidas diarias (mañana y tarde)',
            guide: 'Guía Off-Road SERNANP',
            groupSize: 'Convoy de 4 a 6 cuatrimotos'
        },
        whatYouDo: [
            'Maneja tu propia cuatrimoto Honda 250cc por dunas y pampas',
            'Detente en acantilados con vistas asombrosas a la Playa Supay',
            'Siente el fuerte viento paracas en pleno desierto'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 09:00 AM Encuentro en base de cuatrimotos. 09:15 AM Instrucción de uso, acelerador, frenos y entrega de equipo de protección. 09:30 AM Ingreso a la Reserva. Recorrido por el istmo de la península (trocha y arena afirmada). 10:30 AM Parada en Mirador Playa Yumaque y Playa Roja. 11:30 AM Retorno en convoy acelerado a la base.' }
        ],
        inc: [
            'Cuatrimoto personal automática / semi-automática',
            'Casco integral y lentes contra polvo',
            'Guía líder en moto líder',
            'Asistencia mecánica en ruta'
        ],
        notSuitable: ['Menores de 16 años conduciendo (pueden ir de copiloto)'],
        meetingPoint: 'Base Off-Road entrada Paracas (09:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Ropa que se pueda ensuciar con polvo, zapatillas cerradas (obligatorio), protector solar. NO INCLUYE: Ingreso turístico a la Reserva Nacional.',
        steps: [{ n: 'G', t: 'Base', d: 'Instrucción' }, { n: 'ri-motorbike-fill', t: 'Reserva', d: 'Off-Road' }, { n: 'dot', t: 'Base', d: 'Fin Ruta' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    // PUNO (5)
    {
        id: 26,
        title: 'Kayak de Altura Titicaca',
        dept: 'Puno',
        price: 150,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/puno/tour_26.jpg',
        detail: 'Rema a 3,812 metros sobre el nivel del mar.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La travesía en Kayak por el Lago Titicaca cuesta $150. Operado por agencias especializadas (Titikayak) usando kayaks de travesía cerrados (Sea Kayak) con faldón y chalecos homologados.',
        faqs: [
            { q: '¿Hace mucho frío?', a: 'El agua está a 10°C, pero proveemos cobertores impermeables. Remar te mantendrá en calor rápidamente.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso por mal clima/viento',
            duration: '4.5 horas',
            availability: 'Salidas diarias 07:00 AM (menos viento)',
            guide: 'Guía de Kayak de Mar',
            groupSize: 'Máximo 6 kayaks'
        },
        whatYouDo: [
            'Remo de travesía desde la Península de Esteves',
            'Navegación silenciosa a través de los bosques de Totora',
            'Llegada a las Islas Flotantes de los Uros (sin motor)'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 06:45 AM Recojo del hotel en Puno. 07:15 AM Charla técnica en la orilla sobre uso de remos, timón y medidas de rescate. 08:00 AM Inicio del remado hacia la Reserva de Totoras. 09:30 AM Llegada a las islas flotantes Uros y encuentro con las familias. 10:30 AM Descanso y snack andino. 11:30 AM Retorno remando al punto de partida o bote a motor (opcional). 12:30 PM Fin del tour.' }
        ],
        inc: [
            'Kayak cerrado de expedición',
            'Remo asimétrico, faldón y salvavidas Pro',
            'Lancha a motor escolta de seguridad',
            'Snack y tickets de ingreso'
        ],
        notSuitable: ['Personas con lesiones graves de hombro/espalda'],
        meetingPoint: 'Hotel en Puno (06:45 AM)',
        importantInfo: 'QUÉ LLEVAR: Pantalones impermeables, chaqueta cortavientos térmica, guantes de neopreno o lana, lentes de sol, bloqueador FPS 50+ (la radiación es brutal).',
        steps: [{ n: 'G', t: 'Puno', d: 'Remos' }, { n: 'ri-ship-fill', t: 'Lago', d: 'Travesía' }, { n: 'dot', t: 'Uros', d: 'Isla' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 27,
        title: 'Stand Up Paddle Titicaca',
        dept: 'Puno',
        price: 180,
        duration: '1 día',
        difficulty: 'Media-Baja',
        img: 'assets/images/destinos/puno/tour_27.jpg',
        detail: 'Camina sobre las aguas sagradas del imperio Inca.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El recorrido en Stand Up Paddle (SUP) cuesta $180. Es una forma increíble de conexión con el lago operada por instructores SUP certificados. Se hace al amanecer cuando el lago es un espejo perfecto.',
        faqs: [
            { q: '¿Qué pasa si me caigo al agua?', a: 'Usarás un traje de neopreno (wetsuit) completo que te aislará del frío si caes, y el instructor te ayudará a subir de inmediato.' }
        ],
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '3.5 horas',
            availability: 'Salidas diarias 06:00 AM (Amanecer)',
            guide: 'Instructor SUP Certificado',
            groupSize: 'Máximo 5 tablas'
        },
        whatYouDo: [
            'Observa el amanecer andino reflejado perfectamente en el lago',
            'Ejercita el equilibrio y core sobre tablas rígidas largas',
            'Conecta con la naturaleza en silencio total'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 05:45 AM Recojo del hotel. 06:00 AM Llegada a bahía y colocación del wetsuit. 06:15 AM Briefing en la orilla sobre equilibrio y técnica de paleo. 06:30 AM Ingreso al agua para ver el amanecer sobre las montañas de Bolivia. Remado suave hacia formaciones de totora. 08:30 AM Retorno a tierra, cambio de ropa y desayuno caliente en la orilla. 09:30 AM Fin de la actividad.' }
        ],
        inc: [
            'Tabla rígida SUP y remo ajustable',
            'Wetsuit de 4mm y botines de neopreno',
            'Leash de seguridad y chaleco flotador',
            'Instructor guía y mate de coca caliente'
        ],
        notSuitable: ['Personas que no saben nadar'],
        meetingPoint: 'Hotel en Puno (05:45 AM)',
        importantInfo: 'QUÉ LLEVAR: Ropa de baño para poner debajo del wetsuit, toalla, ropa abrigadora para después. NO INCLUYE: Fotografía profesional (costo extra).',
        steps: [{ n: 'G', t: 'Puno', d: 'Amanecer' }, { n: 'ri-water-flash-fill', t: 'Espejo', d: 'SUP' }, { n: 'dot', t: 'Puno', d: 'Breakfast' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 28,
        title: 'Cuatrimotos Sillustani 1D',
        dept: 'Puno',
        price: 190,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/puno/tour_28.jpg',
        detail: 'Ruta Off-Road hacia las torres funerarias.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La excursión en cuatrimotos hacia Sillustani dura medio día y cuesta $190. Atraviesas caminos de trocha de la meseta del Collao operado por agencias de aventura formales de Puno con equipos revisados.',
        faqs: [
            { q: '¿Vamos por pista asfaltada?', a: 'No, el 90% del recorrido es por caminos de herradura (trocha de tierra) atravesando comunidades andinas auténticas.' }
        ],
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '4 horas',
            availability: 'Diario (Mañanas y Tardes)',
            guide: 'Guía Motociclista Profesional',
            groupSize: 'Convoy Privado (Max 6)'
        },
        whatYouDo: [
            'Conduce cuatrimotos Honda/Yamaha 250cc-350cc',
            'Atraviesa paisajes altiplánicos llenos de alpacas y vicuñas',
            'Visita la Laguna Umayo y el centro arqueológico de Sillustani'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 08:00 AM Traslado desde Puno hasta el poblado de Atuncolla (Base). 08:45 AM Charla técnica y prueba de conducción en terreno plano. 09:15 AM Inicio de la expedición cruzando pampas y bordeando la Laguna Umayo. 10:30 AM Llegada a las Chullpas de Sillustani. Visita guiada caminando por la necrópolis inca y colla. 11:30 AM Retorno en cuatrimoto a la base. 12:30 PM Regreso a Puno en van.' }
        ],
        inc: [
            'Cuatrimoto automática moderna',
            'Casco protector con visor anti-polvo',
            'Guía mecánico y escolta de seguridad',
            'Entrada al complejo arqueológico Sillustani'
        ],
        notSuitable: ['Menores de 16 años como pilotos'],
        meetingPoint: 'Hotel en Puno (08:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Guantes contra el frío, casaca abrigadora que se pueda empolvar, bloqueador solar y zapatillas cerradas de montaña.',
        steps: [{ n: 'G', t: 'Base', d: 'ATV' }, { n: 'ri-riding-fill', t: 'Altiplano', d: 'Ruta' }, { n: 'dot', t: 'Sillustani', d: 'Chullpas' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 29,
        title: 'Tirolesa Juli (Zipline) 1D',
        dept: 'Puno',
        price: 90,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'assets/images/destinos/puno/tour_29.jpg',
        detail: 'Vuelo rasante en "La pequeña Roma de América".',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Zipline en Juli cuesta $90 y es de los más altos de la región. Cuenta con un cable de acero certificado para alta tensión y arneses Petzl supervisados por operadores capacitados.',
        faqs: [
            { q: '¿Qué distancia se recorre?', a: 'Son casi 700 metros de cable con vista directa al Lago Titicaca.' }
        ],
        genInfo: {
            cancelPolicy: 'Gratis 12h antes',
            duration: 'Medio Day',
            availability: 'Diario 09:00 AM',
            guide: 'Instructor de Cuerdas',
            groupSize: 'Grupal'
        },
        whatYouDo: [
            'Lánzate al vacío sintiendo el viento helado del ande',
            'Alcanza velocidades de 80 km/h sobre el suelo andino',
            'Disfruta de una vista privilegiada del lago Titicaca'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 09:00 AM Viaje desde Puno hacia la localidad de Juli (1 hora). 10:00 AM Llegada al mirador y base de Canopy. 10:30 AM Equipamiento (arnés tipo silla, casco, mosquetones) e instrucción de posturas. 11:00 AM Salto individual o en tandem por el Zipline. 11:30 AM Descenso y caminata corta. Retorno a Puno al mediodía.' }
        ],
        inc: [
            'Transporte ida y vuelta',
            'Equipo de seguridad homologado (CE/UIAA)',
            '2 Instructores (Despegue y Frenado)'
        ],
        notSuitable: ['Personas con problemas cardíacos', 'Embarazadas'],
        meetingPoint: 'Plaza de Armas de Puno (09:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Ropa muy abrigadora, zapatillas sujetas (que no caigan durante el vuelo).',
        steps: [{ n: 'G', t: 'Juli', d: 'Ascenso' }, { n: 'ri-windy-fill', t: 'Cable', d: 'Zipline' }, { n: 'dot', t: 'Puno', d: 'Retorno' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 30,
        title: 'MTB Península de Llachón',
        dept: 'Puno',
        price: 210,
        duration: '1 día',
        difficulty: 'Alta',
        img: 'assets/images/destinos/puno/tour_30.jpg',
        detail: 'Ciclismo de montaña a 3,800 metros snm.',
        last_verified: '2026-06-30',
        direct_answer_block: 'La ruta de Ciclismo MTB (Mountain Bike) en Llachón (1 día) cuesta $210. Exige resistencia pulmonar extrema debido a la altitud y es operado con bicicletas Trek/Specialized con frenos hidráulicos.',
        faqs: [
            { q: '¿Hay vehículo de soporte?', a: 'Sí, una van de asistencia nos sigue a distancia durante todo el trayecto en caso alguien requiera descansar.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso 100% 48h antes',
            duration: '6 horas',
            availability: 'Diario',
            guide: 'Guía Biker Certificado (RCP)',
            groupSize: 'Máximo 5 ciclistas'
        },
        whatYouDo: [
            'Pedalea 45 kilómetros por la orilla del Titicaca',
            'Descensos rápidos (Downhill ligero) en terreno pedregoso',
            'Almuerzo en casa de comuneros de Llachón'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 08:00 AM Traslado a zona de inicio fuera del tráfico urbano. 09:00 AM Configuración de bicicletas (altura de asiento, presiones). 09:30 AM Inicio de pedaleo por trochas que bordean el lago. 12:00 PM Subidas fuertes hacia la península de Capachica. 01:30 PM Llegada a Llachón. Almuerzo trucha fresca. 03:00 PM Retorno a Puno en transporte (las bicis van en parrilla).' }
        ],
        inc: [
            'Mountain Bike aro 29, doble freno disco, suspensión delantera',
            'Casco, guantes y kit de pinchazos',
            'Vehículo escolta, guía de ruta y almuerzo'
        ],
        notSuitable: ['Personas sin condición cardiovascular excelente', 'Falta de aclimatación previa (Min 2 días en Puno)'],
        meetingPoint: 'Oficina MTB Puno',
        importantInfo: 'QUÉ LLEVAR: Ropa ciclista (culotte recomendado), hidratación extra (camelbak), lentes contra el sol/polvo. NO INCLUYE: Pedales con calas (traer propios si los requiere).',
        steps: [{ n: 'G', t: 'Ruta', d: 'Bici' }, { n: 'ri-riding-fill', t: 'Cerro', d: 'MTB' }, { n: 'dot', t: 'Llachón', d: 'Almuerzo' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },

    // AREQUIPA (5)
    {
        id: 31,
        title: 'Trekking Cañón del Colca 3D',
        dept: 'Arequipa',
        price: 850,
        duration: '3 días',
        difficulty: 'Alta',
        img: 'assets/images/destinos/arequipa/tour_31.jpg',
        detail: 'Incursión profunda al abismo de los cóndores.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Trekking de 3 Days al fondo del Cañón del Colca (Oasis Sangalle) cuesta $850. Operado por guías de alta montaña con permisos oficiales. Uno de los descensos más profundos del mundo.',
        faqs: [
            { q: '¿Es muy exigente?', a: 'Sí. Bajar destruye las rodillas y subir destruye los pulmones. Se requiere excelente estado físico.' }
        ],
        genInfo: {
            cancelPolicy: 'Gratis hasta 7 días antes',
            duration: '3 días / 2 noches',
            availability: 'Salidas diarias 03:00 AM',
            guide: 'Guía oficial de Trekking (AGMP)',
            groupSize: 'Expediciones reducidas (Máximo 8)'
        },
        whatYouDo: [
            'Descenso vertical de 1,200 metros por paredes de roca',
            'Observación del Cóndor Andino en vuelo termal',
            'Recuperación muscular en las piscinas del Oasis Sangalle',
            'Ataque de subida bajo las estrellas a las 04:00 AM'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 03:00 AM Salida de Arequipa. 07:00 AM Parada en la Cruz del Cóndor. 09:30 AM Llegada a Cabanaconde e inicio del trekking en picada de bajada. 01:00 PM Llegada a San Juan de Chuccho (almuerzo). Trekking hasta Cosñirhua para cenar y dormir en lodge rústico.' },
            { day: 2, desc: 'Day 2: 09:00 AM Trekking suave bajando al Oasis de Sangalle. 11:30 AM Llegada. Tarde de relajación total en las piscinas con agua de manantial rodeado de palmeras. Night de descanso temprano.' },
            { day: 3, desc: 'Day 3: 04:00 AM (Aún de noche) Inicio del ascenso vertical continuo por 3 horas. 07:30 AM Llegada al borde (Cabanaconde). Breakfast. 09:30 AM Viaje a Chivay (baños termales). 05:00 PM Llegada a Arequipa.' }
        ],
        inc: [
            'Transporte ida y vuelta turístico',
            '2 Nights de alojamiento (básico)',
            'Pensión completa (2D, 3A, 2C)',
            'Guía experto con balón de oxígeno/botiquín trauma',
            'Ticket turístico del Colca (BTC)'
        ],
        notSuitable: ['Personas sedentarias, asma severo, problemas de rodillas/articulaciones'],
        meetingPoint: 'Recojo en Hoteles Centro de Arequipa (03:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Bastones de trekking (obligatorio para cuidar rodillas), linterna frontal, bloqueador, sombrero y poco peso en la mochila.',
        steps: [{ n: 'G', t: 'Cabanaconde', d: 'Descenso' }, { n: 'ri-footprint-fill', t: 'Oasis', d: 'Cañón' }, { n: 'dot', t: 'Chivay', d: 'Termas' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 32,
        title: 'Ascenso Volcán Misti 2D',
        dept: 'Arequipa',
        price: 1100,
        duration: '2 días',
        difficulty: 'Experto',
        img: 'assets/images/destinos/arequipa/tour_32.jpg',
        detail: 'Escala el cráter activo de 5,822 metros snm.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El ascenso al Volcán Misti cuesta $1,100. Es una expedición de Alta Montaña rigurosa guiada por instructores UIAGM (Unión Internacional de Asociaciones de Guías de Montaña), garantizando estándares suizos de seguridad.',
        faqs: [
            { q: '¿Se necesita experiencia en escalada?', a: 'Técnicamente no hay escalada en hielo/roca vertical, pero físicamente es exhaustivo por la falta de oxígeno y el terreno de ceniza volcánica.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso por avalanchas / clima extremo',
            duration: '2 días (1 noche en carpa alta)',
            availability: 'Mejor temporada: Abril a Noviembre',
            guide: 'Guía UIAGM / AGMP certificado',
            groupSize: 'Expedición 2 pax por 1 guía'
        },
        whatYouDo: [
            'Camina por cenizas volcánicas hasta tocar los 5,822 metros',
            'Duerme en carpa de alta montaña a 4,500m (Nido de Águilas)',
            'Observa los humos sulfurosos del cráter activo al amanecer',
            'Descenso brutal y rápido (sandboarding en ceniza)'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 08:00 AM Salida de Arequipa en 4x4. Llegada a la base (3,300m). Inicio de caminata cargando equipo y agua (4-5 hrs). Llegada al campamento base Nido de Águilas (4,500m). Armado de carpas The North Face VE25. Cena ligera y a dormir a las 06:00 PM.' },
            { day: 2, desc: 'Day 2: 01:00 AM Despertar helado. Mate de coca. 02:00 AM Inicio del ataque a la cumbre en oscuridad, con linternas frontales, avanzando un paso a la vez sobre ceniza volcánica. 07:00 AM Llegada a la Cumbre (5,822m) al amanecer. Olor a azufre. Fotos. 08:00 AM Descenso rápido en arena volcánica (2 hrs). 11:00 AM Campamento, empacar. 02:00 PM Retorno 4x4 a Arequipa.' }
        ],
        inc: [
            'Equipo de acampada (Carpa 4 estaciones, colchoneta térmica)',
            'Guía UIAGM con radio y oxígeno',
            'Transporte 4x4 off-road especializado',
            'Piquetas/crampones si la temporada exige hielo'
        ],
        notSuitable: ['Personas sin aclimatación previa', 'Problemas cardíacos o pulmonares'],
        meetingPoint: 'Oficina Operador Arequipa (08:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Botas de montaña rígidas o semi-rígidas, ropa de pluma de alta montaña, guantes gruesos, 4 litros de agua por persona. NO INCLUYE: Bolsa de dormir (mínimo de -15°C confort).',
        steps: [{ n: 'G', t: 'Campo Base', d: 'Ascenso' }, { n: 'ri-fire-fill', t: 'Cráter', d: '5822m' }, { n: 'dot', t: 'Arequipa', d: 'Descenso' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 33,
        title: 'Canotaje Río Chili (Rafting)',
        dept: 'Arequipa',
        price: 150,
        duration: '1 día',
        difficulty: 'Media',
        img: 'assets/images/destinos/arequipa/rafting.jpg',
        detail: 'Rápidos potentes Clase III y IV a minutos de la ciudad.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El Rafting en el Río Chili dura 3 horas y cuesta $150. Está liderado por instructores de la International Rafting Federation (IRF), superando olas y hoyos de gran tamaño con botes profesionales NRS.',
        faqs: [
            { q: '¿El agua está fría?', a: 'Sí, es deshielo de volcanes, pero proveemos trajes de neopreno completos para evitar la hipotermia.' }
        ],
        genInfo: {
            cancelPolicy: 'Gratis 24h antes',
            duration: '3 horas totales (1.5h en el río)',
            availability: 'Turnos: 08:00 AM, 11:00 AM y 02:00 PM',
            guide: 'Capitán de Bote IRF Clase 4/5',
            groupSize: 'Balsa de 6 pax + Guía'
        },
        whatYouDo: [
            'Rema fuertemente para superar rápidos turbulentos clase III y IV',
            'Nada en las frías aguas cristalinas en la zona segura final',
            'Admira el cañón de Chilina resguardado por el Volcán Misti'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: Recojo de la Plaza de Armas. Viaje de 20 min hasta Charcani (Valle de Chilina). Entrega de wetsuit y equipamiento. Charla de seguridad vitalícia (cómo remar, cómo caer al agua y ser rescatado). Navegación extrema (6 km) de rápidos continuos. Llegada al puente Chilina y refrigerio de celebración. Retorno.' }
        ],
        inc: [
            'Bote inflable bailing automático, remos, casco, salvavidas clase V',
            'Traje de neopreno y cortavientos de agua',
            'Kayakista rescatista de seguridad (escolta)',
            'Guía IRF en el bote'
        ],
        notSuitable: ['Personas que no saben nadar', 'Menores de 8 años (dependiendo del caudal)'],
        meetingPoint: 'Cercado de Arequipa',
        importantInfo: 'QUÉ LLEVAR: Ropa de baño bajo la ropa, toalla grande, sandalias de sujeción (que no se salgan) o zapatillas viejas que se puedan mojar. NO INCLUYE: USB con fotos (costo extra).',
        steps: [{ n: 'G', t: 'Charcani', d: 'Rápidos' }, { n: 'ri-water-flash-fill', t: 'Río Chili', d: 'Rafting' }, { n: 'dot', t: 'Puente', d: 'Fin' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 34,
        title: 'Downhill Ciclismo Volcán Chachani',
        dept: 'Arequipa',
        price: 250,
        duration: '1 día',
        difficulty: 'Alta',
        img: 'assets/images/destinos/cusco/ciclismo.jpg',
        detail: 'Caída libre de casi 2,000 metros en bicicleta.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El descenso en Bicicleta (Downhill) del Volcán Chachani cuesta $250. Empieza a los 4,700m y desciende casi 2,000 metros verticales. Operado con bicicletas Full Suspension y equipo integral de enduro.',
        faqs: [
            { q: '¿Tengo que pedalear de subida?', a: '¡No! Un transporte te lleva hasta las faldas del volcán. Toda la ruta es puro descenso por caminos de ceniza y rocas.' }
        ],
        genInfo: {
            cancelPolicy: 'Reembolso por mal clima/nieve',
            duration: '5 horas',
            availability: 'Salidas diarias (08:00 AM)',
            guide: 'Guía Ciclista (Primeros Auxilios WFR)',
            groupSize: 'Pequeños grupos (Max 6)'
        },
        whatYouDo: [
            'Desciende velozmente zigzagueando por las faldas del volcán Chachani',
            'Lidia con caminos técnicos llenos de "calamina" (irregularidades)',
            'Disfruta de vistas espectaculares del Misti y de vicuñas salvajes'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 08:00 AM Traslado de 2 horas en van hasta el Mirador de los Andes (Pampa Cañahuas - 4,700m). 10:00 AM Entrega de protecciones tipo Robocop y bicicleta doble suspensión. 10:30 AM Inicio del descenso infernal (Off-Road puro). La van sigue detrás del grupo. Paradas fotográficas y de rehidratación. 01:30 PM Fin del descenso en las afueras de Arequipa. 02:00 PM Retorno al hotel.' }
        ],
        inc: [
            'Bicicleta de Montaña Enduro / DH doble suspensión y frenos hidráulicos',
            'Armadura de cuerpo completo (rodilleras, coderas, peto)',
            'Casco integral de Downhill y guantes',
            'Transporte y guía de ruta'
        ],
        notSuitable: ['Principiantes en bicicleta (requiere dominar frenadas en ripio/tierra suelta)'],
        meetingPoint: 'Recojo en Hotel Arequipa (08:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Lentes para el polvo, zapatillas de suela plana (para buen agarre de pedales). Cortavientos ligero.',
        steps: [{ n: 'G', t: 'Pampa', d: '4700m' }, { n: 'ri-riding-fill', t: 'Volcán', d: 'Downhill' }, { n: 'dot', t: 'Ciudad', d: 'Arequipa' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    {
        id: 35,
        title: 'Ascenso Volcán Chachani 2D',
        dept: 'Arequipa',
        price: 950,
        duration: '2 días',
        difficulty: 'Experto',
        img: 'assets/images/destinos/arequipa/volcan.jpg',
        detail: 'Supera la barrera de los 6,000 metros.',
        last_verified: '2026-06-30',
        direct_answer_block: 'El ascenso al Chachani (6,057 metros) cuesta $950 y es famoso por ser el "6 mil" más accesible del mundo. Operado por guías de alta montaña de la Asociación de Guías de Montaña del Perú (AGMP).',
        faqs: [
            { q: '¿Requiero cuerdas y piolets técnicos?', a: 'Por lo general no es vertical. En la temporada seca, se usan crampones para tramos helados simples, pero es básicamente caminata de altura.' }
        ],
        genInfo: {
            cancelPolicy: 'No reembolsable (El clima en montañas no es predecible)',
            duration: '2 días',
            availability: 'Marzo a Noviembre',
            guide: 'Guía Alta Montaña AGMP',
            groupSize: 'Pareja o Privado'
        },
        whatYouDo: [
            'Experimenta la falta de oxígeno al cruzar la cota de los 6,000 metros',
            'Camina por glaciares residuales con crampones',
            'Acampa a 5,200 metros (Campamento Azteca) en el frío más extremo',
            'Celebra el amanecer desde la cumbre nevada de Arequipa'
        ],
        fullItinerary: [
            { day: 1, desc: 'Day 1: 08:00 AM Vehículo 4x4 sube hasta los casi 5,000m (el ascenso vehicular ayuda bastante). 10:30 AM Trekking de 2 horas llevando nuestro equipo hasta el campamento base "Azteca" (5,200m). Aclimatación, cena rápida y dormir a las 05:30 PM.' },
            { day: 2, desc: 'Day 2: 01:30 AM Inicio del ataque a cumbre usando linternas. Frío que baja de los -10°C. 5 a 6 horas de caminata muy lenta ("paso de tortuga"). 07:00 AM Cumbre del Chachani (6,057m). Paisaje de las cadenas de volcanes peruanos. 08:30 AM Descenso rápido. 11:00 AM Desarme campamento. 02:00 PM Retorno Arequipa.' }
        ],
        inc: [
            'Transporte 4x4 extremo y especializado',
            'Carpas de alta montaña expedición, comida (2 comidas de campamento)',
            'Crampones, casco y piolet (si hay hielo/nieve dura)',
            'Guía AGMP experto'
        ],
        notSuitable: ['Cualquier persona que no haya aclimatado 3 días antes a más de 3,000m'],
        meetingPoint: 'Arequipa Centro (08:00 AM)',
        importantInfo: 'QUÉ LLEVAR: Todo el equipo de Alta Montaña: Casaca de pluma -15C, saco de dormir -15C (puedes alquilarlo), botas plásticas/rígidas, doble guante. NO INCLUYE: Porteador personal (lo cargas tú, o contratas porteador extra por $150).',
        steps: [{ n: 'G', t: 'Camp 5200m', d: 'Base' }, { n: 'ri-snowy-fill', t: 'Glaciar', d: 'Cumbre' }, { n: 'dot', t: 'Retorno', d: 'Arequipa' }],
        sensoryVariants: { landscape: '', comfort: '', action: '' }
    },
    // LIMA (5)
    {
        id: 36,
        title: 'Parapente Costa Verde',
        dept: 'Lima',
        price: 280,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'assets/images/destinos/lima/tour_36.jpg',
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
        img: 'assets/images/destinos/lima/tour_37.jpg',
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
        img: 'assets/images/destinos/lima/tour_38.jpg',
        detail: 'El bosque de piedras místico.',
        genInfo: {
            cancelPolicy: 'Gratis 72h antes',
            duration: '2 días / 1 noche',
            availability: 'Fines de semana o privado',
            guide: 'Guía experto en altitud',
            groupSize: 'Grupal aventurero'
        },
        whatYouDo: [
            'Trekking hacia la meseta a 4,000m de altura',
            'Observa las extrañas figuras talladas por la naturaleza (Monumento a la Humanidad)',
            'Acampa bajo uno de los cielos más limpios cerca de Lima',
            'Siente la energía mística del lugar'
        ],
        fullItinerary: [
            { day: 1, desc: 'Lima a San Pedro de Casta. Ascenso caminando o a mula hasta la meseta. Campamento Anfiteatro. Night de fogata.' },
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
        img: 'assets/images/destinos/lima/tour_39.jpg',
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
        title: 'Rápel en Cañón de Autisha',
        dept: 'Lima',
        price: 160,
        duration: '1 día',
        difficulty: 'Alta',
        img: 'assets/images/destinos/lima/tour_40.jpg',
        detail: 'Adrenalina pura en un cañón y túneles subterráneos.',
        genInfo: {
            cancelPolicy: 'Gratis 48h antes',
            duration: '12 horas',
            availability: 'Sábados y Domingos',
            guide: 'Instructor de cuerdas',
            groupSize: 'Máximo 10 personas'
        },
        whatYouDo: [
            'Descenso en rápel vertical de 30 metros en un profundo cañón',
            'Trekking por oscuros túneles abandonados',
            'Llegada a una espectacular cascada oculta subterránea',
            'Supera tus límites con un ascenso extremo por escaleras de hierro'
        ],
        fullItinerary: [
            { day: 1, desc: 'Salida de Lima hacia la cuenca de Santa Eulalia. Trekking de aproximación, paso por túneles hasta la boca del abismo. Descenso en rápel de 30m hasta la cascada subterránea de Sheque. Ascenso extremo y retorno a Lima.' }
        ],
        inc: ['Transporte turístico ida y vuelta', 'Equipo técnico (arnés, casco, mosquetones)', 'Guía instructor especializado en rescate'],
        notSuitable: ['Personas con claustrofobia', 'Acrofobia severa', 'Falta de condición física'],
        meetingPoint: 'Javier Prado / San Isidro',
        importantInfo: 'Llevar linterna frontal (obligatorio), guantes de cuero y ropa que se pueda mojar.',
        steps: [{ n: 'G', t: 'Autisha', d: 'Descenso' }, { n: 'dot', t: 'Cascada', d: 'Rápel' }]
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
    { id: 214, title: 'Sierra Andina Mountain Trail', dept: 'Huaraz', cat: 'Trail Running', date: '19', month: 'JUL', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070', price: 200, detail: 'Carrera extrema en Matara, Áncash.', whatYouDo: ['Desnivel', 'High mountain', 'Frío'], steps: [{ n: 'ri-arrow-up-line', t: 'Ascenso', d: 'Paso' }, { n: 'ri-flag-checkered-line', t: 'Meta', d: 'Pueblo' }], inc: ['Dorsal', 'Cerveza SAMT', 'Medalla'] },
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

// --- NEW PARKS DATA ---
const parks = [
    {
        "id": "INF-LIMA-001",
        "nombre_infraestructura": "Palestras Escalada Pro",
        "region": "Lima",
        "tipo": "Palestras",
        "ubicacion_lat": -12.046374,
        "ubicacion_lon": -77.042793,
        "url_foto": "https://images.unsplash.com/photo-1522163182402-834f871fd851",
        "nivel_dificultad": "Intermedio",
        "estado_actual": "Activo",
        "precio_estimado": 45.0
    },
    {
        "id": "INF-CUSCO-001",
        "nombre_infraestructura": "V\u00eda Ferrata Valle Sagrado",
        "region": "Cusco",
        "tipo": "V\u00eda Ferrata",
        "ubicacion_lat": -13.3039,
        "ubicacion_lon": -72.2274,
        "url_foto": "https://images.unsplash.com/photo-1627894483216-2138af692e32",
        "nivel_dificultad": "Avanzado",
        "estado_actual": "Activo",
        "precio_estimado": 180.0
    },
    {
        "id": "INF-SMART-001",
        "nombre_infraestructura": "Zipline Tarapoto Adrenaline",
        "region": "San Mart\u00edn",
        "tipo": "Zipline",
        "ubicacion_lat": -6.4862,
        "ubicacion_lon": -76.3683,
        "url_foto": "https://images.unsplash.com/photo-1515444744559-7be63e1600de",
        "nivel_dificultad": "Principiante",
        "estado_actual": "Activo",
        "precio_estimado": 60.0
    },
    {
        "id": "INF-ICA-001",
        "nombre_infraestructura": "Dunas Buggy Park",
        "region": "Ica",
        "tipo": "Sandboard / Buggy",
        "ubicacion_lat": -14.088,
        "ubicacion_lon": -75.762,
        "url_foto": "https://images.unsplash.com/photo-1509316785289-025f5b846b35",
        "nivel_dificultad": "Intermedio",
        "estado_actual": "Activo",
        "precio_estimado": 55.0
    }
];
window.parks = parks;

// --- NEW GUIDES DATA ---
