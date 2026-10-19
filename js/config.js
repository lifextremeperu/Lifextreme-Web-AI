// ========================================
// CONFIGURACIÓN CORPORATIVA - LIFEXTREME PERÚ
// ========================================

const COMPANY_CONFIG = {
    // INFORMACIÓN BÁSICA
    name: "Lifextreme",
    legalName: "Lifextreme Perú S.A.C.",
    ruc: "20612489512",
    founded: "2024",

    // CONTACTO OFICIAL
    contact: {
        email: {
            info: "contacto@lifextreme.store",
            reservas: "contacto@lifextreme.store",
            soporte: "contacto@lifextreme.store",
            legal: "contacto@lifextreme.store",
            privacidad: "contacto@lifextreme.store"
        },
        phone: {
            main: "+51 958 050 928",
            whatsapp: "+51 958 050 928",
            emergency: "+51 958 050 928"
        },
        address: {
            street: "Cl. Chihuampata 626 - Barrio de San Blas",
            city: "Cusco",
            region: "Cusco",
            country: "Perú",
            zipCode: "08003",
            googleMapsUrl: "https://maps.google.com/?q=Cl.+Chihuampata+626+San+Blas+Cusco+Peru"
        },
        hours: {
            weekdays: "Lunes a Viernes: 8:00 AM - 8:00 PM",
            saturday: "Sábado: 8:00 AM - 6:00 PM",
            sunday: "Soporte Táctico 24/7 para Expediciones Activas",
            timezone: "America/Lima (UTC-5)"
        }
    },

    // REDES SOCIALES VERIFICADAS
    social: {
        facebook: "https://www.facebook.com/Lifextremeperu",
        instagram: "https://www.instagram.com/lifextremeperu/",
        youtube: "https://www.youtube.com/@lifextremeperu2780",
        tiktok: "https://www.tiktok.com/@lifextremeperu",
        linkedin: "https://www.linkedin.com/company/lifextreme/"
    },

    // CERTIFICACIONES Y ESTÁNDARES OPERATIVOS
    certifications: {
        tourism: {
            name: "Directorio Nacional de Prestadores de Servicios Turísticos Calificados",
            number: "MINCETUR-CUS-2024-LX",
            issuer: "MINCETUR / GERCETUR CUSCO"
        },
        guides: {
            certification: "UIAGM / IFMGA & AGMP (Asociación de Guías de Montaña del Perú)",
            verified: true
        },
        insurance: {
            provider: "Rimac / Pacífico Asistencia en Alta Montaña",
            policy: "POL-LX-ADV-2026",
            coverage: "Cobertura de Evacuación y Accidentes en Ruta"
        }
    },

    // MÉTODOS DE PAGO ACEPTADOS
    paymentMethods: {
        cards: ["Visa", "Mastercard", "American Express", "Diners Club"],
        digital: ["Yape", "Plin", "Niubiz", "Izipay"],
        bank: ["BCP", "BBVA", "Interbank", "Scotiabank"],
        international: ["PayPal", "Stripe"]
    },

    // POLÍTICAS DE CANCELACIÓN Y RESERVA FRACCIONADA (30-30-40)
    policies: {
        cancellation: {
            moreThan30Days: {
                refund: 100,
                adminFee: 5,
                description: "Reembolso del 100% menos 5% de gastos administrativos y logísticos"
            },
            between15And30Days: {
                refund: 50,
                description: "Reembolso del 50% o reprogramación libre sin penalidad"
            },
            between7And14Days: {
                refund: 25,
                description: "Reembolso del 25% o crédito Lifextreme válido por 12 meses"
            },
            lessThan7Days: {
                refund: 0,
                description: "Sin reembolso por bloqueo logístico de guías UIAGM y permisos"
            }
        },
        minimumAge: 18,
        requiresInsurance: true,
        requiresID: true
    },

    // SEO Y METADATOS
    seo: {
        title: "Lifextreme | Turismo de Aventura, Alta Montaña e IA en Perú",
        description: "Plataforma tecnológica líder de turismo de aventura, trekking, escalada y eventos outdoor en Perú, impulsada por Inteligencia Artificial (MAX RAG 336K+ vectores).",
        keywords: "aventuras perú, trekking cusco, escalada huaraz, ausangate, quellccaya, huayhuash, pacaya samiria, parques de aventura perú",
        ogImage: "https://www.lifextreme.store/LOGOS%20LIFEXTREME/LOGO%20OFICIAL.png",
        twitterHandle: "@lifextremeperu"
    },

    // INFRAESTRUCTURA IA & BACKEND
    aiEngine: {
        endpoint: "https://max.lifextreme.store",
        vectorDb: "Qdrant Vector Engine (336,869 vectores activos)",
        llmProvider: "Groq LPU (openai/gpt-oss-120b) + FastEmbed Multilingual",
        collections: ["Lifextreme_Knowledge", "Lifextreme_FQSA_Knowledge"]
    },

    // CONFIGURACIÓN DE NOTIFICACIONES TRANSACCIONALES
    email: {
        provider: "Zoho Enterprise SMTP (Serverless /api/send-email)",
        sender: "contacto@lifextreme.store"
    },

    // MONEDA E IDIOMAS
    currency: {
        code: "PEN",
        symbol: "S/",
        name: "Sol Peruano"
    },
    languages: ["es", "en", "pt"],
    defaultLanguage: "es"
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = COMPANY_CONFIG;
}

if (typeof window !== 'undefined') {
    window.COMPANY_CONFIG = COMPANY_CONFIG;
}

console.log('✅ Configuración corporativa Lifextreme cargada');

