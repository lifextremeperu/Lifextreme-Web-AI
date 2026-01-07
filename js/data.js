// --- DATA (MODULARIZED V29) ---

const tours = [
    // CUSCO (5)
    {
        id: 1,
        title: 'Inca Trail 4D',
        dept: 'Cusco',
        price: 2450,
        duration: '4 días',
        difficulty: 'Alta',
        img: 'https://images.unsplash.com/photo-1587547131116-a0655a526190',
        detail: 'La ruta más icónica del mundo hacia Machu Picchu.',
        genInfo: {
            cancelPolicy: 'Esta actividad no es reembolsable',
            duration: '4 días',
            availability: 'Comprueba la disponibilidad para ver los horarios de inicio',
            guide: 'Inglés, Español',
            groupSize: 'Máximo 9 participantes'
        },
        whatYouDo: [
            'Bicicleta en Abra Málaga a 4,316 metros',
            'Aprende y participa en el tostado de café artesanal',
            'Relájate en las relajantes aguas termales de Cocalmayo',
            'Explora la ciudadela de Machu Picchu con guía experto'
        ],
        fullItinerary: [
            {
                day: 1,
                desc: 'El Día 1 comienza con un servicio de recogida a las 6:00 AM en la Plaza Mayor de Cuzco. Viaja a través del Valle Sagrado hasta el paso de Abra Málaga (4,316m). Se inicia un descenso en bicicleta de unas 3 horas (50 km) por zonas de puna y bosque nuboso hasta las ruinas de Huaman Marq\'a. Pasaremos la noche en una casa ecológica en Pispitayoc con cena incluida.'
            },
            {
                day: 2,
                desc: 'El segundo día comienza con un desayuno y clases de tostado de café. Caminaremos por parte del Camino Inca (Qhapaq Ñan) con vistas de aves y plantaciones frutales. Llegaremos al mirador de Huancarcasa (1,750m) para vistas panorámicas. El descenso nos lleva a Qellomayo para almorzar y finalmente a las termas de Cocalmayo antes de dormir en Santa Teresa.'
            },
            {
                day: 3,
                desc: 'Caminata de 3 horas por plantaciones de café y coca hasta llegar a Hidroeléctrica (1,900m). Después del almuerzo, seguimos 3 horas más por la vía del tren hasta Aguas Calientes (1,950m). Tarde libre para ocio y preparación para la ascensión final a Machu Picchu.'
            },
            {
                day: 4,
                desc: 'Subida temprana a las 4:00 AM hacia Machu Picchu (2,400m). Tour guiado de 2 horas por los sectores más significativos de la ciudadela. Tiempo libre de exploración antes de retornar a Aguas Calientes para el tren a Ollantaytambo y bus de retorno a Cusco.'
            }
        ],
        inc: [
            'Briefing el día anterior',
            'Recogida en el centro de Cusco (Plaza de Armas)',
            'Transporte Cusco - Abra Málaga - Santa María',
            'Bicicleta Kona, coderas, rodilleras, guantes, casco',
            '3 desayunos / 3 almuerzos / 3 cenas',
            'Tickets de entrada a Machu Picchu',
            'Guía profesional bilingüe (inglés-español)',
            'Bus de retorno Ollantaytambo - Cusco'
        ],
        notSuitable: ['Embarazadas', 'Personas con problemas de espalda', 'Personas en silla de ruedas'],
        meetingPoint: 'Plaza Mayor de Cuzco (El guía tendrá la chaqueta oficial Lifextreme)',
        importantInfo: 'Llevar pasaporte o documento de identidad original (se acepta copia)',
        steps: [{ n: 'G', t: 'Cusco Hotel', d: '06:00 AM' }, { n: 'ri-map-pin-2-fill', t: 'Abra Málaga', d: 'Descenso Bici' }, { n: 'dot', t: 'Machu Picchu', d: 'Final' }],
        sensoryVariants: {
            landscape: 'Siente la inmensidad de los Andes bajo tus pies mientras el aire puro de la montaña renueva cada célula de tu cuerpo.',
            comfort: 'Sumérgete en la calidez de un refugio ecológico, donde el aroma del café recién tostado te abraza después de la jornada.',
            action: 'Siente la adrenalina pura en el descenso de Abra Málaga, donde el viento ruge y la libertad se vuelve absoluta.'
        }
    },
    {
        id: 2,
        title: 'Salkantay Trek Elite',
        dept: 'Cusco',
        price: 1850,
        duration: '5 días',
        difficulty: 'Extrema',
        img: 'https://images.unsplash.com/photo-1596395819057-033f7b2c5897',
        detail: 'Ruta alternativa de alta montaña por nevados y selva alta.',
        genInfo: {
            cancelPolicy: 'Reembolso parcial hasta 7 días antes',
            duration: '5 días',
            availability: 'Salidas diarias confirmadas',
            guide: 'Inglés, Español, Francés',
            groupSize: 'Máximo 12 participantes'
        },
        whatYouDo: [
            'Ascenso al paso Salkantay a 4,630 metros',
            'Visita a la Laguna Humantay turquesa',
            'Caminata por ceja de selva y plantaciones',
            'Llegada triunfal a Machu Picchu'
        ],
        fullItinerary: [
            { day: 1, desc: 'Recogida en Cusco y viaje a Mollepata. Caminata de ascenso hacia Soraypampa con vistas del nevado Humantay. Visita a la laguna Humantay por la tarde.' },
            { day: 2, desc: 'El día más difícil: ascenso al Paso Salkantay (4,630m). Vistas espectaculares de la cordillera Vilcabamba antes de descender hacia Chaullay.' },
            { day: 3, desc: 'Caminata por la selva alta (ceja de selva). Veremos cascadas, aves y plantaciones de café y frutas tropicales. Noche en La Playa o Lucmabamba.' },
            { day: 4, desc: 'Ascenso hacia Llactapata para una vista única de Machu Picchu desde la distancia. Descenso a Hidroeléctrica y caminata final a Aguas Calientes.' },
            { day: 5, desc: 'Exploración completa de Machu Picchu al amanecer. Retorno a Cusco por la tarde en tren y bus.' }
        ],
        inc: [
            'Recogida en hotel',
            'Guía profesional especializado en montaña',
            'Cocinero y asistentes especializados',
            'Caballos para equipo y 7kg personales',
            '4 desayunos / 4 almuerzos / 4 cenas',
            'Equipo de campamento de alta montaña',
            'Ticket de entrada a Machu Picchu',
            'Tren de retorno y bus a Cusco'
        ],
        notSuitable: ['Menores de 12 años', 'Personas con asma severa', 'Problemas de rodilla'],
        meetingPoint: 'Recepción de su hotel en Cusco (04:30 AM)',
        importantInfo: 'Llevar ropa térmica, bloqueador solar y calzado de trekking ya usado (break-in).',
        steps: [{ n: 'G', t: 'Mollepata', d: 'Inicio' }, { n: 'dot', t: 'Machu Picchu', d: 'Final' }],
        sensoryVariants: {
            landscape: 'Respira la esencia de los glaciares y deja que el silencio de la alta montaña calme tu mente y despierte tus sentidos.',
            comfort: 'Déjate envolver por el calor de las aguas termales de Cocalmayo, un bálsamo turquesa en medio de la selva alta.',
            action: 'Conquista el paso Salkantay a 4,630m y siente el poder de las nubes al alcance de tu mano.'
        }
    },
    {
        id: 3,
        title: 'Vinicunca Speed Run',
        dept: 'Cusco',
        price: 450,
        duration: '1 día',
        difficulty: 'Media-Alta',
        img: 'https://images.unsplash.com/photo-1547483238-2c6036746654',
        detail: 'Ascenso táctico a la Montaña de 7 Colores.',
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
            'Interactúa con comunidades locales de pastores de alpacas',
            'Desayuno y almuerzo buffet en valle andino'
        ],
        fullItinerary: [
            { day: 1, desc: 'Recojo 4:00 AM. 3 horas de viaje hasta Cusipata. Desayuno buffet. Inicio de caminata de 1.5 horas hasta la cima de Vinicunca. Tiempo para fotos y vistas. Descenso, almuerzo buffet y retorno a Cusco a las 17:00.' }
        ],
        inc: ['Transporte turístico', 'Guía profesional', 'Oxígeno de emergencia', 'Desayuno y Almuerzo Buffet'],
        notSuitable: ['Personas con asma', 'Menores de 8 años', 'Hipertensos'],
        meetingPoint: 'Recepción de su hotel (Centro Histórico)',
        importantInfo: 'Llevar ropa de abrigo extrema, bloqueador y mucha agua.',
        steps: [{ n: 'G', t: 'Cusco', d: '04:00 AM' }, { n: 'ri-mountain-fill', t: 'Cumbre', d: '5,200m' }, { n: 'dot', t: 'Cusco', d: 'Retorno' }]
    },
    {
        id: 4,
        title: 'Choquequirao Expedition',
        dept: 'Cusco',
        price: 3200,
        duration: '4 días',
        difficulty: 'Experto',
        img: 'https://images.unsplash.com/photo-1583032353423-04fd96ef2211',
        detail: 'La verdadera ciudad perdida de los Incas.',
        genInfo: {
            cancelPolicy: 'Reembolso del 50% hasta 15 días antes',
            duration: '4 días / 3 noches',
            availability: 'Salidas programadas semanalmente',
            guide: 'Guía especializado en historia Inca',
            groupSize: 'Máximo 8 aventureros'
        },
        whatYouDo: [
            'Cruce del cañón del río Apurímac bajo el sol andino',
            'Campamento bajo el cielo más estrellado de Cusco',
            'Explora terrazas agrícolas con decoraciones de llamas',
            'Visita la ciudadela de Choquequirao sin multitudes'
        ],
        fullItinerary: [
            { day: 1, desc: 'Cusco a Capuliyoc. Descenso épico al cañón del Apurímac. Campamento en Chiquisca.' },
            { day: 2, desc: 'Ascenso duro desde el río hasta Marampata. Llegada a las cercanías de Choquequirao.' },
            { day: 3, desc: 'Día completo de exploración en Choquequirao. Atardecer en las terrazas de las llamas.' },
            { day: 4, desc: 'Retorno por la misma ruta. Almuerzo final en Capuliyoc y regreso a Cusco.' }
        ],
        inc: ['Equipo de campamento Pro', 'Arrieros y mulas', 'Pensión completa', 'Entradas a Choquequirao'],
        notSuitable: ['Personas sin experiencia en trekking', 'Menores de 15 años'],
        meetingPoint: 'Plaza Regocijo, Cusco (05:00 AM)',
        importantInfo: 'Entrenamiento previo requerido. Ruta físicamente devastadora pero gratificante.',
        steps: [{ n: 'G', t: 'Capuliyoc', d: 'Inicio' }, { n: 'dot', t: 'Cachora', d: 'Retorno' }]
    },
    {
        id: 5,
        title: 'Ausangate Glaciar Challenge',
        dept: 'Cusco',
        price: 2100,
        duration: '6 días',
        difficulty: 'Técnica',
        img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b',
        detail: 'Alta ruta alrededor del Apu Ausangate.',
        genInfo: {
            cancelPolicy: 'Actividad no reembolsable',
            duration: '6 días',
            availability: 'Temporada de Abril a Octubre',
            guide: 'Guía AGMP (Asoc. Guías Montaña)',
            groupSize: 'Expedición privada o máx 6'
        },
        whatYouDo: [
            'Circuito completo al Apu más sagrado de Cusco',
            'Noches a más de 4,000 metros en lodges o carpas térmicas',
            'Baños termales naturales en medio de glaciares',
            'Cruce de pasos de montaña a 5,100 metros'
        ],
        fullItinerary: [
            { day: 1, desc: 'Cusco a Tinki. Inicio de expedición hacia Upis. Termas naturales.' },
            { day: 2, desc: 'Paso Arapa y Laguna Jatun Pucacocha con vistas del glaciar.' },
            { day: 3, desc: 'Paso Palomani (5,100m) el punto más alto del circuito tradicional.' },
            { day: 4, desc: 'Valle de Chilca y avistamiento de manadas de vicuñas silvestres.' },
            { day: 5, desc: 'Laguna Comercocha y descenso hacia Pacchanta.' },
            { day: 6, desc: 'Retorno a Tinki y bus de vuelta a la ciudad del Cusco.' }
        ],
        inc: ['Caballos de carga', 'Carpas de alta montaña', 'Oxígeno y Botiquín', 'Alimentación Pro'],
        notSuitable: ['Personas no aclimatadas', 'Problemas de corazón'],
        meetingPoint: 'Hotel en Cusco (06:00 AM)',
        importantInfo: 'Se requiere aclimatación mínima de 3 días en Cusco antes de iniciar.',
        steps: [{ n: 'G', t: 'Tinqui', d: 'Base' }, { n: 'dot', t: 'Tinqui', d: 'Retorno' }]
    },

    // HUARAZ (5)
    {
        id: 6,
        title: 'Santa Cruz Trek 4D',
        dept: 'Huaraz',
        price: 1200,
        duration: '4 días',
        difficulty: 'Media',
        img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190',
        detail: 'El circuito clásico de la Cordillera Blanca.',
        genInfo: {
            cancelPolicy: 'Gratis hasta 7 días antes',
            duration: '4 días',
            availability: 'Salidas confirmadas lunes y jueves',
            guide: 'Guía certificado UIAGM',
            groupSize: '10 personas máx'
        },
        whatYouDo: [
            'Vista panorámica del Alpamayo (la montaña más bella)',
            'Cruce del Paso Punta Unión a 4,750m',
            'Caminata por valles glaciares de color turquesa',
            'Campamentos bajo picos de más de 6,000m'
        ],
        fullItinerary: [
            { day: 1, desc: 'Huaraz a Cashapampa. Caminata inicial por el valle de Santa Cruz hasta Llamacorral.' },
            { day: 2, desc: 'Laguna Ichiccocha y Jatuncocha. Campamento base de Alpamayo en Taullipampa.' },
            { day: 3, desc: 'El día clave: Paso Punta Unión (4,750m). Vistas del Taulliraju. Descenso a Paria.' },
            { day: 4, desc: 'Caminata final hacia Vaquería. Transporte de retorno a Huaraz vía Portachuelo.' }
        ],
        inc: ['Transporte privado', 'Burros de carga', 'Cocinero de montaña', 'Entrada al PNAS'],
        notSuitable: ['Menores de 10 años', 'Problemas severos de rodilla'],
        meetingPoint: 'Oficina Lifextreme Huaraz (06:00 AM)',
        importantInfo: 'Traer saco de dormir de pluma (disponible para renta).',
        steps: [{ n: 'G', t: 'Cashapampa', d: 'Inicio' }, { n: 'dot', t: 'Vaqueria', d: 'Final' }]
    },
    {
        id: 7,
        title: 'Huascarán Summit View',
        dept: 'Huaraz',
        price: 4500,
        duration: '7 días',
        difficulty: 'Experto',
        img: 'https://images.unsplash.com/photo-1522163182402-834f60b58e26',
        detail: 'Ascenso técnico por el glaciar más alto.',
        genInfo: {
            cancelPolicy: 'No reembolsable',
            duration: '7 días',
            availability: 'Solo Junio y Julio',
            guide: 'Guía UIAGM (1 guía por 2 pax)',
            groupSize: 'Expedición técnica reducida'
        },
        whatYouDo: [
            'Escalada técnica en hielo y grietas glaciares',
            'Noches en campos de altura sobre los 5,000m',
            'Conquista el punto más alto del Perú (Cumbre Sur)',
            'Uso de equipo de rescate y seguridad Pro'
        ],
        fullItinerary: [
            { day: 1, desc: 'Huaraz - Musho. Caminata al Campo Base (4,200m).' },
            { day: 2, desc: 'Acenso por la morrena hasta el Campo 1 (5,300m) sobre el glaciar.' },
            { day: 3, desc: 'Cruce de "La Canaleta" y llegada al Campo 2 (Garganta - 6,000m).' },
            { day: 4, desc: 'Día de Cumbre. Ascenso final a los 6,768m. Retorno a La Garganta.' },
            { day: 5, desc: 'Día extra por mal tiempo o descanso.' },
            { day: 6, desc: 'Descenso al Campo Base.' },
            { day: 7, desc: 'Retorno a Musho y transporte a Huaraz.' }
        ],
        inc: ['Guías UIAGM', 'Cuerdas y equipo técnico de grupo', 'Porteros de altura', 'Alimentación Alta Energía'],
        notSuitable: ['Principiantes', 'Personas sin experiencia en cramponaje'],
        meetingPoint: 'Huaraz Center (05:00 AM)',
        importantInfo: 'Requiere aclimatación previa en picos de 5,000m (e.g. Ishinca).',
        steps: [{ n: 'G', t: 'Musho', d: 'Base' }, { n: 'dot', t: 'Cumbre', d: 'Cumbre' }]
    },
    {
        id: 8,
        title: 'Laguna 69 Ultra',
        dept: 'Huaraz',
        price: 350,
        duration: '1 día',
        difficulty: 'Alta',
        img: 'https://images.unsplash.com/photo-1527004013197-29007328905b',
        detail: 'Aclimatación extrema a 4,600m.',
        genInfo: {
            cancelPolicy: 'Gratis hasta 24h antes',
            duration: '1 día (12 horas)',
            availability: 'Salidas diarias',
            guide: 'Guía local experto',
            groupSize: 'Máximo 18 personas'
        },
        whatYouDo: [
            'Caminata bajo el Nevado Huascarán y Huandoy',
            'Visita a las lagunas de Llanganuco (Chinancocha)',
            'Alcanza una de las lagunas más azules del mundo a 4,600m',
            'Prueba de resistencia física y aclimatación'
        ],
        fullItinerary: [
            { day: 1, desc: 'Salida de Huaraz 5:00 AM. Desayuno en Yungay. Parada en Lagunas de Llanganuco. Inicio de caminata en Cebollapampa. 3 horas de ascenso. 1 hora en la laguna. Descenso y retorno a Huaraz.' }
        ],
        inc: ['Transporte compartido', 'Guía de grupo', 'Oxígeno portátil'],
        notSuitable: ['Personas mayores de 65 años sin entrenamiento', 'Problemas respiratorios'],
        meetingPoint: 'Plaza de Armas de Huaraz',
        importantInfo: 'Traer impermeable, snacks y mucha determinación.',
        steps: [{ n: 'G', t: 'Cebollapampa', d: 'Ascenso' }, { n: 'dot', t: 'Huaraz', d: 'Descanso' }]
    },
    {
        id: 9,
        title: 'Pastoruri Ice Wall',
        dept: 'Huaraz',
        price: 280,
        duration: '1 día',
        difficulty: 'Baja',
        img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190',
        detail: 'Ruta del Cambio Climático y Puya Raimondi.',
        genInfo: {
            cancelPolicy: 'Gratis hasta 12h antes',
            duration: '7 horas',
            availability: 'Salidas diarias 09:00 AM',
            guide: 'Guía bilingüe',
            groupSize: 'Grupo familiar o pro'
        },
        whatYouDo: [
            'Camina sobre un glaciar de fácil acceso a 5,000m',
            'Conoce la planta milenaria Puya Raimondi',
            'Observa pinturas rupestres pre-incas',
            'Ideal para primer día de aclimatación en Huaraz'
        ],
        fullItinerary: [
            { day: 1, desc: 'Viaje hacia el sur de Huaraz. Parada en Puya Raimondi. Llegada al estacionamiento del glaciar. Caminata suave de 30 min. Tiempo de exploración en el hielo y la laguna congelada. Retorno.' }
        ],
        inc: ['Bus turístico', 'Certificado de altitud', 'Guía bilingüe'],
        notSuitable: ['Personas con mala oxigenación inmediata'],
        meetingPoint: 'Recojo en hotel (09:00 AM)',
        importantInfo: 'Ruta con poco esfuerzo físico pero alta altitud.',
        steps: [{ n: 'G', t: 'Huaraz', d: 'Salida' }, { n: 'dot', t: 'Pastoruri', d: 'Final' }]
    },
    {
        id: 10,
        title: 'Ishinca Base Camp',
        dept: 'Huaraz',
        price: 1600,
        duration: '3 días',
        difficulty: 'Técnica',
        img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b',
        detail: 'Entrenamiento técnico para 6ks.',
        genInfo: {
            cancelPolicy: 'Reembolso 30% hasta 5 días antes',
            duration: '3 días / 2 noches',
            availability: 'Bajo pedido o fechas fijas',
            guide: 'Guía aspirante AGMP',
            groupSize: 'Máximo 4 personas por guía'
        },
        whatYouDo: [
            'Alojamiento en refugio andino de alta montaña',
            'Escalada técnica básica en los picos Ishinca o Urus',
            'Taller de uso de cuerdas y crampones en glaciar real',
            'Vistas de 360 grados de la Cordillera Blanca'
        ],
        fullItinerary: [
            { day: 1, desc: 'Transporte a Pashpa. Caminata al Refugio Ishinca (4,350m).' },
            { day: 2, desc: 'Día de cumbre Ishinca (5,530m) o prácticas técnicas en glaciar. Retorno al refugio.' },
            { day: 3, desc: 'Descenso a Pashpa y retorno a Huaraz.' }
        ],
        inc: ['Estadía en Refugio Ishinca', 'Cenas calientes', 'Guía técnico', 'Burros'],
        notSuitable: ['Personas sin calzado de montaña profesional'],
        meetingPoint: 'Huaraz Basecamp Office',
        importantInfo: 'Es el mejor entrenamiento antes de intentar el Huascarán.',
        steps: [{ n: 'G', t: 'Pashpa', d: 'Caminata' }, { n: 'dot', t: 'Refugio', d: 'Base' }]
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
    { id: 101, title: 'Ultra Trail Cordillera Blanca', dept: 'Huaraz', cat: 'Competencia', date: '15', month: 'MAY', img: 'https://images.unsplash.com/photo-1544198365-f5d60b6d8190', price: 450, detail: 'La carrera de trail running más exigente del Callejón de Huaylas.', whatYouDo: ['Running 42k', 'Pasos de altura', 'Vistas glaciares'], steps: [{ n: 'G', t: 'Huaraz', d: '05:00 AM' }, { n: 'ri-map-pin-2-fill', t: 'Punta Unión', d: 'Checkpoint' }, { n: 'dot', t: 'Meta', d: 'Final' }], inc: ['Kit Competidor', 'Seguro', 'Medalla'] },
    { id: 102, title: 'Andean Adventure Film Fest', dept: 'Cusco', cat: 'Festival', date: '22', month: 'JUN', img: 'https://images.unsplash.com/photo-1478720568477-152d9b164e26', price: 80, detail: 'El mejor cine de aventura del mundo en pantalla gigante.', whatYouDo: ['Documentales', 'Charlas Pro', 'Networking'], steps: [{ n: 'G', t: 'Teatro', d: 'Opening' }, { n: 'dot', t: 'Cierre', d: 'Premiación' }], inc: ['Entrada VIP', 'Bebida'] },
    { id: 103, title: 'Taller de Autorrescate VIP', dept: 'Huaraz', cat: 'Taller', date: '05', month: 'JUL', img: 'https://images.unsplash.com/photo-1522163182402-834f60b58e26', price: 950, detail: 'Capacitación técnica avanzada para montañistas.', whatYouDo: ['Sistemas poleas', 'Maniobras pared', 'Primeros auxilios'], steps: [{ n: 'G', t: 'Base', d: 'Teoría' }, { n: 'dot', t: 'Pared', d: 'Práctica' }], inc: ['Certificación', 'Equipo'] },
    { id: 104, title: 'Inca Challenge MTB 100K', dept: 'Cusco', cat: 'Competencia', date: '18', month: 'AGO', img: 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd', price: 320, detail: 'Maratón de MTB por senderos incas originales.', whatYouDo: ['Descensos técnicos', 'Cruces de ríos'], steps: [{ n: 'G', t: 'Plaza', d: 'Partida' }, { n: 'dot', t: 'Valle', d: 'Meta' }], inc: ['Jersey', 'Hidratación'] },
    { id: 105, title: 'Summit Photography Workshop', dept: 'Cusco', cat: 'Taller', date: '12', month: 'SEP', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b', price: 1200, detail: 'Inmortaliza la montaña con guías pro y fotógrafos.', whatYouDo: ['Astrofotografía', 'Landscape Pro'], steps: [{ n: 'G', t: 'Lodge', d: 'Setup' }, { n: 'dot', t: 'Cumbre', d: 'Captura' }], inc: ['Transporte', 'Edición'] },
    { id: 106, title: 'Paracas Sand Festival', dept: 'ICA', cat: 'Festival', date: '30', month: 'OCT', img: 'https://images.unsplash.com/photo-1506461883276-594a12b11cf3', price: 150, detail: 'Música, deporte y arte en las dunas de Paracas.', whatYouDo: ['DJs en vivo', 'Sandboard Jam'], steps: [{ n: 'G', t: 'Camp', d: 'Inicio' }, { n: 'dot', t: 'Dunas', d: 'Party' }], inc: ['Acceso Free'] },
    { id: 107, title: 'Amazonas Kayak Marathon', dept: 'Iquitos', cat: 'Competencia', date: '10', month: 'NOV', img: 'https://images.unsplash.com/photo-1516306580123-e6e52b1b7b5f', price: 550, detail: 'Rema contra la corriente en el río más largo.', whatYouDo: ['Resistencia río', 'Navegación'], steps: [{ n: 'G', t: 'Iquitos', d: 'Salida' }, { n: 'dot', t: 'Lodge', d: 'Final' }], inc: ['Kayak Pro', 'Chef'] },
    { id: 108, title: 'Clinica de Escalada en Hielo', dept: 'Huaraz', cat: 'Taller', date: '15', month: 'DIC', img: 'https://images.unsplash.com/photo-1527004013197-29007328905b', price: 1800, detail: 'Domina los glaciares con herramientas técnicas.', whatYouDo: ['Uso crampones', 'Tornillos hielo'], steps: [{ n: 'G', t: 'Morrena', d: 'Ascenso' }, { n: 'dot', t: 'Muro', d: 'Escalada' }], inc: ['Botas', 'Piolets'] },
    { id: 109, title: 'Kitesurf Masters Piura', dept: 'Piura', cat: 'Competencia', date: '10', month: 'SEP', img: 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd', price: 380, detail: 'Competencia internacional de Kitesurf en Máncora.', whatYouDo: ['Freestyle', 'Big Air'], steps: [{ n: 'G', t: 'Máncora', d: '09:00 AM' }, { n: 'dot', t: 'Playa', d: 'Meta' }], inc: ['Lycra Oficial', 'Hidratación'] },
    { id: 110, title: 'Misti Vertical Race', dept: 'Arequipa', cat: 'Competencia', date: '05', month: 'AGO', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b', price: 290, detail: 'Ascenso vertical cronometrado al volcán Misti.', whatYouDo: ['Kilómetro Vertical', 'Ascenso rápido'], steps: [{ n: 'G', t: 'Base', d: 'Salida' }, { n: 'dot', t: 'Cumbre', d: 'Meta' }], inc: ['Medalla', 'Seguro'] },
    { id: 111, title: 'Puno Lake Kayak Exp', dept: 'Puno', cat: 'Taller', date: '12', month: 'OCT', img: 'https://images.unsplash.com/photo-1516306580123-e6e52b1b7b5f', price: 420, detail: 'Taller de kayak de larga distancia en el Titicaca.', whatYouDo: ['Navegación GPS', 'Técnicas remo'], steps: [{ n: 'G', t: 'Puno', d: 'Briefing' }, { n: 'dot', t: 'Isla', d: 'Cierre' }], inc: ['Kayak Pro', 'Certificación'] },
    { id: 112, title: 'Colca Canyon Trail 50K', dept: 'Arequipa', cat: 'Competencia', date: '20', month: 'NOV', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b', price: 480, detail: 'Trail running extremo por el cañón más profundo.', whatYouDo: ['Descenso técnico', 'Ascenso vertical'], steps: [{ n: 'G', t: 'Cabanaconde', d: 'Partida' }, { n: 'dot', t: 'Pinchocha', d: 'Meta' }], inc: ['Kit Trail', 'Almuerzo'] }
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
