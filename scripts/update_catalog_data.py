import os
import json
import re

# New Equips Data
equips_js = '''const equips = [
    // CARPAS & CAMPAMENTO (Camino Inca & Salkantay)
    {
        name: 'The North Face Mountain 25 (4 Estaciones)',
        cat: 'Carpas & Campamento',
        price: 2850,
        rentPrice: 65,
        img: 'https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '4.0 kg',
            temp: 'Extremo Vientos 100 km/h',
            impermeable: '10,000 mm Nylon Ripstop',
            capacidad: '2 Personas + Vestíbulo',
            cert: 'ASTM F1933 Alpine Standard'
        },
        destinos: 'Salkantay Trek, Huayhuash, Ausangate',
        desc: 'Carpa geodésica de expedición diseñada para soportar nevadas intensas y vientos huracanados en pasos de más de 4,600 msnm.'
    },
    {
        name: 'MSR Hubba Hubba NX 2P Ultraligera',
        cat: 'Carpas & Campamento',
        price: 1950,
        rentPrice: 48,
        img: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '1.54 kg (Trail Weight)',
            temp: '3 Estaciones Andinas',
            impermeable: '3,000 mm DuraShield',
            capacidad: '2 Personas',
            cert: 'ISO 5912 Trekking'
        },
        destinos: 'Camino Inca Clásico, Choquequirao, Santa Cruz',
        desc: 'El estándar de oro para mochileros ultraligeros. Espaciosa, rápida de armar con varillas Easton Syclone indestructibles.'
    },
    {
        name: 'Ferrino Svalbard 3P Expedición',
        cat: 'Carpas & Campamento',
        price: 2400,
        rentPrice: 55,
        img: 'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '4.7 kg',
            temp: '4 Estaciones Glaciar',
            impermeable: '8,000 mm Doble Faldón',
            capacidad: '3 Personas',
            cert: 'EN 5912 Polar Testing'
        },
        destinos: 'Campamento Base Huascarán, Cordillera Blanca',
        desc: 'Carpa robusta con doble ábside para cocinar en tormentas de nieve y anclajes especiales para nieve compacta.'
    },

    // SLEEPINGS & MATRAS TÉRMICAS
    {
        name: 'Bolsa de Dormir Marmot Col -29°C (800FP)',
        cat: 'Sleepings & Matras',
        price: 3100,
        rentPrice: 50,
        img: 'https://images.unsplash.com/photo-1547847932-d3a3d538df59?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1547847932-d3a3d538df59?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1617326693439-0bd649033376?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '1.76 kg',
            temp: 'Confort -20°C / Límite -29°C',
            relleno: 'Pluma de Ganso 800+ RDS Down',
            tejido: 'Pertex Shield Impermeable',
            cert: 'EN 13537 / ISO 23537'
        },
        destinos: 'Salkantay Pass, Ausangate Circuit, Campo Alto Huascarán',
        desc: 'Bolsa momia de alta cota tratada con Down Defender anti-humedad para noches bajo cero en los Andes.'
    },
    {
        name: 'Sleeping Ferrino Nightec 800 -12°C',
        cat: 'Sleepings & Matras',
        price: 1100,
        rentPrice: 32,
        img: 'https://images.unsplash.com/photo-1617326693439-0bd649033376?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1617326693439-0bd649033376?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1547847932-d3a3d538df59?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '1.45 kg',
            temp: 'Confort -5°C / Límite -12°C',
            relleno: 'Microfibra Shingle Sintética',
            tejido: 'Ripstop 260T Transpirable',
            cert: 'EN 13537 Alpine'
        },
        destinos: 'Camino Inca Clásico, Lares Trek, Valle Sagrado',
        desc: 'Excelente aislamiento térmico de secado rápido, perfecto para campamentos con humedad matutina en ceja de selva.'
    },
    {
        name: 'Matra Therm-a-Rest NeoAir XTherm NXT',
        cat: 'Sleepings & Matras',
        price: 980,
        rentPrice: 28,
        img: 'https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1617326693439-0bd649033376?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1547847932-d3a3d538df59?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '439 g',
            aislamiento: 'R-Value 7.3 (Aislamiento Máximo)',
            grosor: '7.6 cm de amortiguación',
            valvula: 'WingLock rápida y hermética',
            cert: 'ASTM F3340-18 Thermal Resistance'
        },
        destinos: 'Nieve, Suelos Rocosos Andinos, Glaciares',
        desc: 'La colchoneta inflable más cálida y liviana del planeta, bloquea el frío que asciende del suelo congelado.'
    },

    // CASACAS & INDUMENTARIA TÉCNICA
    {
        name: 'Casaca Arc\'teryx Alpha SV Gore-Tex Pro',
        cat: 'Casacas & Ropa Técnica',
        price: 3600,
        rentPrice: 70,
        img: 'https://images.unsplash.com/photo-1548883354-7622d03aca27?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1548883354-7622d03aca27?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '485 g',
            membrana: 'Gore-Tex Pro Most Rugged 3L',
            impermeable: '28,000 mm Columna de Agua',
            seguridad: 'Reflector RECCO integrado',
            cert: 'CE Alpine Severe Weather'
        },
        destinos: 'Nevado Huascarán, Alpamayo, Salkantay, Chachani',
        desc: 'Hardshell legendaria de grado militar y alpino. Resiste tormentas de nieve, granizo y rozaduras contra roca viva.'
    },
    {
        name: 'Parka Plumas The North Face Summit L3 (800FP)',
        cat: 'Casacas & Ropa Técnica',
        price: 1850,
        rentPrice: 42,
        img: 'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1548883354-7622d03aca27?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '380 g',
            relleno: 'Pluma ProDown 800FP con repelencia al agua',
            corte: 'Active Alpine Slim Fit',
            bolsillo: 'Autoguardable en su propio bolsillo',
            cert: 'Responsible Down Standard (RDS)'
        },
        destinos: 'Paso Salkantay, Cumbre Misti, Valle Sagrado frío nocturno',
        desc: 'Aislamiento de pluma hidrorepelente ultraliviana para retener calor corporal cuando el termómetro baja de 0°C.'
    },
    {
        name: 'Pantalón Hardshell Patagonia Triolet Gore-Tex 3L',
        cat: 'Casacas & Ropa Técnica',
        price: 1450,
        rentPrice: 35,
        img: 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1548883354-7622d03aca27?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '540 g',
            membrana: 'Gore-Tex 3 Capas 100% Reciclado',
            cierres: 'Cremalleras completas de doble vía en piernas',
            polainas: 'Polaina interna elástica con ganchos',
            cert: 'Fair Trade Certified™ sewing'
        },
        destinos: 'Travesías glaciares, Trekking bajo lluvia torrencial',
        desc: 'Pantalón impermeable respirable con refuerzos de Scuff Guard contra cortes de crampones en los tobillos.'
    },

    // ESCALADA EN HIELO & ROCA
    {
        name: 'Piolets Técnicos Petzl Quark (Par Hielo/Mixto)',
        cat: 'Escalada Hielo & Roca',
        price: 2100,
        rentPrice: 55,
        img: 'https://images.unsplash.com/photo-1506377225131-41e98d9ba0d1?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1506377225131-41e98d9ba0d1?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1512990414788-d97cb4a25db3?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '550 g c/u (1.10 kg el par)',
            hoja: 'Acero Forjado ICE (afinada a 3.2 mm en punta)',
            mango: 'Curvo tipo 2 con empuñadura Trigrest',
            accesorios: '1 con Martillo + 1 con Pala desmontable',
            cert: 'CE EN 13089 / UIAA 152 Ice Axe Type 2'
        },
        destinos: 'Cascadas de Hielo, Nevado Mateo, Ishinca, Alpamayo',
        desc: 'Piolets técnicos de alpinismo polivalente para escalada en hielo vertical, goulottes y corredores de nieve dura.'
    },
    {
        name: 'Crampones Semiautomáticos Grivel G12 New-Matic',
        cat: 'Escalada Hielo & Roca',
        price: 920,
        rentPrice: 30,
        img: 'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1506377225131-41e98d9ba0d1?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1512990414788-d97cb4a25db3?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '970 g el par',
            puntas: '12 puntas de acero Chromoly forjado',
            fijacion: 'Semiautomática (talonera micrométrica + puntera correa)',
            antizueco: 'Sistema Antibott activo delantero y trasero',
            cert: 'CE EN 893 / UIAA 153 Mountaineering Crampons'
        },
        destinos: 'Glaciares de Cusco y Huaraz, Pastoruri, Pisco',
        desc: 'El crampón de 12 puntas de referencia mundial para montañismo clásico, mixto y pasos de rimaya.'
    },
    {
        name: 'Casco de Escalada Petzl Sirocco Ultraligero',
        cat: 'Escalada Hielo & Roca',
        price: 580,
        rentPrice: 18,
        img: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1506377225131-41e98d9ba0d1?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1512990414788-d97cb4a25db3?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '170 g (Ultralight)',
            construccion: 'Espuma EPP (polipropileno expandido) + corona EPS',
            ventilacion: 'Canales de flujo de aire de 360°',
            ajuste: 'Cinta textil minimalista y hebilla magnética',
            cert: 'CE EN 12492 / UIAA 106 Climbing Helmet'
        },
        destinos: 'Escalada en Roca Pachar, Balcón del Diablo, Vía Ferrata',
        desc: 'Casco con cobertura envolvente en nuca y sienes para protección máxima contra impactos de caída de piedras.'
    },
    {
        name: 'Arnés Black Diamond Solution Guide',
        cat: 'Escalada Hielo & Roca',
        price: 490,
        rentPrice: 16,
        img: 'https://images.unsplash.com/photo-1512990414788-d97cb4a25db3?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1512990414788-d97cb4a25db3?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1506377225131-41e98d9ba0d1?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '394 g',
            tecnologia: 'Fusion Comfort™ de triple tejido de reparto de carga',
            material: 'Tejido Super Fabric® hiper-resistente a abrasión',
            portamateriales: '4 anillas moldeadas a presión + quinta anilla trasera',
            cert: 'CE EN 12277 Type C / UIAA 105'
        },
        destinos: 'Escalada deportiva, tradicional y vías ferratas en Cusco',
        desc: 'Arnés de alta durabilidad pensado para escalada en granito andino y días intensos de entrenamiento en roca.'
    },

    // MOCHILAS & ACCESORIOS TREKKING
    {
        name: 'Osprey Aether 65 Pro Expedition',
        cat: 'Mochilas & Trekking',
        price: 1350,
        rentPrice: 45,
        img: 'https://images.unsplash.com/photo-1622260614153-03223fb72052?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1622260614153-03223fb72052?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1547847932-d3a3d538df59?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1590845947698-8924d7409b56?w=800&fm=webp&q=80'
        ],
        specs: {
            capacidad: '65 Litros',
            peso: '2.2 kg',
            espaldar: 'AirScape™ moldeado por inyección con espuma troquelada',
            cubierta: 'Raincover impermeable integrada',
            cert: 'Bluesign® approved materials'
        },
        destinos: 'Camino Inca 4D/3N, Salkantay 5D, Choquequirao',
        desc: 'Mochila de carga pesada con ajuste Fit-on-the-Fly que distribuye el peso directamente en las caderas.'
    },
    {
        name: 'Bastones Black Diamond Trail Pro Shock (Par)',
        cat: 'Mochilas & Trekking',
        price: 520,
        rentPrice: 18,
        img: 'https://images.unsplash.com/photo-1563857508098-b6483134604d?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1563857508098-b6483134604d?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1557262947-2cb2d4705540?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1622260614153-03223fb72052?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=800&fm=webp&q=80'
        ],
        specs: {
            peso: '590 g el par',
            material: 'Aluminio 7075 de grado aeroespacial',
            amortiguacion: 'Tecnología SmashShock de absorción en bajadas',
            bloqueo: 'Cierres rápidos FlickLock® Pro de metal',
            cert: 'TÜV Rheinland Tested'
        },
        destinos: 'Descensos empinados de escalinatas incas y pedreras',
        desc: 'Protege las rodillas reduciendo un 35% del impacto acumulado en bajadas técnicas como la de Dead Woman\'s Pass.'
    },
    {
        name: 'GPS Satelital Garmin inReach Explorer+ SOS',
        cat: 'Mochilas & Trekking',
        price: 1850,
        rentPrice: 50,
        img: 'https://images.unsplash.com/photo-1557262947-2cb2d4705540?w=800&fm=webp&q=80',
        views360: [
            'https://images.unsplash.com/photo-1557262947-2cb2d4705540?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1563857508098-b6483134604d?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1622260614153-03223fb72052?w=800&fm=webp&q=80',
            'https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=800&fm=webp&q=80'
        ],
        specs: {
            cobertura: 'Red 100% Satelital Global Iridium',
            bateria: 'Hasta 100 horas en modo rastreo 10 min',
            emergencia: 'Botón SOS interactivo con centro GEOS 24/7',
            mapas: 'Mapas topográficos precargados de los Andes',
            cert: 'IPX7 Resistente al agua'
        },
        destinos: 'Zonas remotas sin señal móvil en todo el territorio peruano',
        desc: 'Comunicador satelital de rescate que envía tu ubicación en tiempo real a familiares y rescatistas en caso de imprevisto.'
    }
];

const tourEquipmentMap = {
    'Cusco': ['The North Face Mountain 25 (4 Estaciones)', 'Bolsa de Dormir Marmot Col -29°C (800FP)', 'Osprey Aether 65 Pro Expedition', 'Bastones Black Diamond Trail Pro Shock (Par)'],
    'Huaraz': ['Ferrino Svalbard 3P Expedición', 'Casaca Arc\'teryx Alpha SV Gore-Tex Pro', 'Piolets Técnicos Petzl Quark (Par Hielo/Mixto)', 'Crampones Semiautomáticos Grivel G12 New-Matic', 'Matra Therm-a-Rest NeoAir XTherm NXT'],
    'Iquitos': ['MSR Hubba Hubba NX 2P Ultraligera', 'GPS Satelital Garmin inReach Explorer+ SOS'],
    'Piura': ['MSR Hubba Hubba NX 2P Ultraligera', 'Bastones Black Diamond Trail Pro Shock (Par)'],
    'ICA': ['Osprey Aether 65 Pro Expedition', 'GPS Satelital Garmin inReach Explorer+ SOS'],
    'Puno': ['Bolsa de Dormir Marmot Col -29°C (800FP)', 'Matra Therm-a-Rest NeoAir XTherm NXT'],
    'Arequipa': ['The North Face Mountain 25 (4 Estaciones)', 'Crampones Semiautomáticos Grivel G12 New-Matic', 'Piolets Técnicos Petzl Quark (Par Hielo/Mixto)'],
    'Lima': ['Casco de Escalada Petzl Sirocco Ultraligero', 'Arnés Black Diamond Solution Guide']
};

const kitTemplates = {
    'Alta Montaña': {
        name: 'Kit Glaciar & Cumbres 6000m',
        items: ['The North Face Mountain 25 (4 Estaciones)', 'Casaca Arc\'teryx Alpha SV Gore-Tex Pro', 'Piolets Técnicos Petzl Quark (Par Hielo/Mixto)', 'Crampones Semiautomáticos Grivel G12 New-Matic'],
        icon: 'ri-landscape-line',
        description: 'Equipamiento de expedición polar y alta cota auditado bajo normativa UIAGM.'
    },
    'Camino Inca & Salkantay': {
        name: 'Kit Expedición Inca Trail',
        items: ['MSR Hubba Hubba NX 2P Ultraligera', 'Bolsa de Dormir Marmot Col -29°C (800FP)', 'Matra Therm-a-Rest NeoAir XTherm NXT', 'Bastones Black Diamond Trail Pro Shock (Par)'],
        icon: 'ri-footprint-line',
        description: 'Combo ligero y térmico diseñado para pernoctar con confort en los pasos andinos.'
    },
    'Escalada en Roca & Vía Ferrata': {
        name: 'Kit Vertical Pro',
        items: ['Casco de Escalada Petzl Sirocco Ultraligero', 'Arnés Black Diamond Solution Guide', 'GPS Satelital Garmin inReach Explorer+ SOS'],
        icon: 'ri-focus-3-line',
        description: 'Seguridad certificada CE/UIAA para paredes andinas y cañones de aventura.'
    }
};

const guides = [
    {
        id: 1,
        name: 'Inti Quispe Mayhua',
        region: 'Cusco & Valle Sagrado',
        specialty: 'Alta Montaña & Camino Inca Maestro',
        languages: ['Quechua', 'Español', 'Inglés'],
        exp: '18 años',
        cert: 'UIAGM / AGMP Cert. #042 PE • DIRCETUR Cusco',
        img: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1887&auto=format&fit=crop',
        desc: 'Nacido en Ollantaytambo, maestro de las rutas incas y rescate en altura. Más de 200 cruces exitosos por Salkantay y Ausangate.',
        fullItinerary: [
            { day: '06:00', desc: 'Briefing técnico de aclimatación y revisión de equipo en Cusco.' },
            { day: '08:30', desc: 'Ingreso al sendero andino con interpretación botánica y cosmogonía quechua.' },
            { day: '13:00', desc: 'Almuerzo de nutrición energética andina (quinua, tarwi y trucha fresca).' },
            { day: '16:30', desc: 'Llegada a campamento base seguro con chequeo de oxímetro y carpa armada.' }
        ],
        notInc: ['Vuelos internacionales', 'Seguro médico extremo individual', 'Bebidas alcohólicas'],
        recommendations: 'Aclimatarse 48h antes en Cusco (3,400m). Llevar calzado de trekking ya amoldado al pie y gorro de lana.',
        ageRating: 'A partir de 14 años en buena condición física.'
    },
    {
        id: 2,
        name: 'Valeria Condori Salas',
        region: 'Cusco & Valle Sagrado',
        specialty: 'Escalada en Roca, Vía Ferrata & Enduro MTB',
        languages: ['Español', 'Inglés', 'Francés'],
        exp: '9 años',
        cert: 'Instructora FEPAM • WFR (Wilderness First Responder)',
        img: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=1964&auto=format&fit=crop',
        desc: 'Campeona nacional de bouldering y referente técnica en vías ferratas del Valle Sagrado. Especialista en seguridad de cuerdas.',
        fullItinerary: [
            { day: '08:00', desc: 'Punto de encuentro en Urubamba o Pachar.' },
            { day: '09:00', desc: 'Taller de progresión vertical, colocación de arnés y mosquetones de seguridad.' },
            { day: '12:30', desc: 'Ascenso a repisas panorámicas a 250m sobre el río Vilcanota.' },
            { day: '15:00', desc: 'Rápel guiado o descenso técnico y retorno.' }
        ],
        notInc: ['Calzado técnico de pies de gato (disponible para alquiler)', 'Propinas'],
        recommendations: 'Ropa elástica transpirable, bloqueador solar SPF 50+ y guantes de aproximación.',
        ageRating: 'Mayores de 12 años con peso mínimo de 40 kg.'
    },
    {
        id: 3,
        name: 'Alberto "Betomontaña" Morales',
        region: 'Áncash & Cordillera Blanca',
        specialty: 'Alpinismo Glaciar & Cumbres 6,000m (Huascarán / Alpamayo)',
        languages: ['Español', 'Inglés', 'Alemán', 'Quechua'],
        exp: '22 años',
        cert: 'Guía UIAGM Internacional • IFMGA Certified #108',
        img: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=1887&auto=format&fit=crop',
        desc: 'Leyenda viva de Huaraz. Más de 40 ascensiones al Huascarán Sur (6,768m) y apertura de rutas en la pared SO del Alpamayo.',
        fullItinerary: [
            { day: '03:00', desc: 'Ataque a cumbre desde campo alto sobre glaciar con crampones y encordamiento.' },
            { day: '07:30', desc: 'Superación de rimaya y cumbre con amanecer sobre la Cordillera Blanca.' },
            { day: '11:00', desc: 'Descenso técnico en rápeles seguros hacia campo base antes del deshielo solar.' },
            { day: '14:00', desc: 'Celebración y retorno a Huaraz con el equipo.' }
        ],
        notInc: ['Permisos SERNANP Parque Nacional Huascarán', 'Equipo personal de nieve'],
        recommendations: 'Experiencia previa comprobable en caminata con crampones y seguro de rescate en helicóptero activo.',
        ageRating: 'Adultos con examen médico de alta cota aprobado.'
    },
    {
        id: 4,
        name: 'Sofía Huamán Noriega',
        region: 'Áncash & Cordillera Blanca',
        specialty: 'Trekking Alpino Huayhuash & Orientación de Rescate',
        languages: ['Español', 'Inglés', 'Italiano'],
        exp: '12 años',
        cert: 'Guía Oficial de Montaña AGMP • Paramédico WEMT',
        img: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=1888&auto=format&fit=crop',
        desc: 'Líder del circuito completo Cordillera Huayhuash. Experta en nutrición de resistencia, telemedicina y rescate en grietas.',
        fullItinerary: [
            { day: '07:00', desc: 'Revisión meteorológica satelital y partida desde campamento laguna Carhuacocha.' },
            { day: '11:30', desc: 'Cruce del Paso Siula Grande (4,830m) con vista a las paredes de Joe Simpson.' },
            { day: '14:30', desc: 'Descenso a campamento Huayhuash junto a manantiales termales.' },
            { day: '18:00', desc: 'Cena deshidratada premium y sesión de estiramiento guiado.' }
        ],
        notInc: ['Pagos a comunidades campesinas locales de Huayhuash', 'Bolsa de dormir'],
        recommendations: 'Mochila de 60L ajustada, bastones con amortiguación y pastillas potabilizadoras.',
        ageRating: 'A partir de 16 años con capacidad de marcha de 6-8 horas diarias.'
    },
    {
        id: 5,
        name: 'Mateo Ramos Cárdenas',
        region: 'Arequipa & Cañón del Colca',
        specialty: 'Volcanes del Sur (Misti, Chachani) & Cañón del Colca',
        languages: ['Español', 'Inglés', 'Portugués'],
        exp: '14 años',
        cert: 'Guía de Montaña DIRCETUR Arequipa • Rescatista Cruz Roja',
        img: 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=1887&auto=format&fit=crop',
        desc: 'Geólogo y montañista arequipeño. Más de 150 cumbres al Volcán Misti (5,822m) y descensos de cañones profundos en Cotahuasi.',
        fullItinerary: [
            { day: '01:00', desc: 'Ascenso nocturno por arenales del Misti para ganar la arista del cráter.' },
            { day: '06:15', desc: 'Amanecer con la sombra piramidal del Misti proyectada sobre la ciudad blanca.' },
            { day: '08:00', desc: 'Visita a las fumarolas activas de azufre y descenso en patinaje sobre ceniza.' },
            { day: '12:00', desc: 'Llegada a transporte 4x4 y almuerzo en picantería tradicional.' }
        ],
        notInc: ['Bebidas hidratantes adicionales', 'Equipo de campamento individual'],
        recommendations: 'Llevar 4 litros de agua por persona, linterna frontal potente y cortavientos térmico.',
        ageRating: 'Mayores de 15 años tolerantes a la altura.'
    },
    {
        id: 6,
        name: 'Elena "Amazon" Tuanama',
        region: 'Selva & Amazonía Central',
        specialty: 'Aguas Blancas, Rafting Clase IV-V & Supervivencia en Selva',
        languages: ['Español', 'Portugués', 'Inglés', 'Shipibo'],
        exp: '15 años',
        cert: 'Rescue 3 International • IRF White Water Guide Grade 5',
        img: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1888&auto=format&fit=crop',
        desc: 'Nacida junto al río Ucayali. Capitana de rafting en los cañones del Río Apurímac y Tambopata. Experta en supervivencia selvática.',
        fullItinerary: [
            { day: '09:00', desc: 'Charla de seguridad, comando de remos y prueba de natación en rápidos clase III.' },
            { day: '10:30', desc: 'Ingreso al cañón profundo con rápidos clase IV: "La Purga del Inca" y "El Laberinto".' },
            { day: '13:30', desc: 'Almuerzo en playa fluvial de arena blanca con frutas exóticas de la Amazonía.' },
            { day: '16:00', desc: 'Desembarque, rescate de botes y retorno al lodge ecológico.' }
        ],
        notInc: ['Zapatillas de agua antideslizantes', 'Cámaras subacuáticas'],
        recommendations: 'Saber nadar, ropa que seque rápido (nylon/poliéster) y repelente orgánico sin DEET fuerte.',
        ageRating: 'Mayores de 14 años con chaleco salvavidas obligatorio provisto.'
    }
];
'''

files = ['js/data.js', 'js/data-en.js', 'js/data-pt.js']

for fpath in files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace from const equips = [ ... to const guides = [ ... ];
    pattern = r'const equips = \[.*?const guides = \[.*?\];'
    replacement = equips_js.strip()

    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count > 0:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully updated {fpath} with {count} match.")
    else:
        print(f"Pattern not found in {fpath}.")
