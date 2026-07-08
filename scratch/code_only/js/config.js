// ========================================
// CONFIGURACIÓN DE EMPRESA - LIFEXTREME
// ========================================
// IMPORTANTE: Actualiza estos datos con tu información real antes de lanzar

const COMPANY_CONFIG = {
    // INFORMACIÓN BÁSICA
    name: "Lifextreme",
    legalName: "Lifextreme Perú S.A.C.",
    ruc: "XXXXXXXXXXX", // ⚠️ ACTUALIZAR CON RUC REAL
    founded: "2024",

    // CONTACTO
    contact: {
        email: {
            info: "info@lifextreme.com",
            reservas: "reservas@lifextreme.com",
            soporte: "soporte@lifextreme.com",
            legal: "legal@lifextreme.com",
            privacidad: "privacidad@lifextreme.com"
        },
        phone: {
            main: "+51 XXX XXX XXX", // ⚠️ ACTUALIZAR CON NÚMERO REAL
            whatsapp: "+51 XXX XXX XXX", // ⚠️ ACTUALIZAR CON WHATSAPP BUSINESS
            emergency: "+51 XXX XXX XXX" // ⚠️ ACTUALIZAR CON NÚMERO DE EMERGENCIAS
        },
        address: {
            street: "Av. El Sol 123", // ⚠️ ACTUALIZAR CON DIRECCIÓN REAL
            city: "Cusco",
            region: "Cusco",
            country: "Perú",
            zipCode: "08000",
            googleMapsUrl: "https://maps.google.com/?q=Cusco+Peru" // ⚠️ ACTUALIZAR CON URL REAL
        },
        hours: {
            weekdays: "Lunes a Viernes: 8:00 AM - 8:00 PM",
            saturday: "Sábado: 9:00 AM - 6:00 PM",
            sunday: "Domingo: Cerrado",
            timezone: "America/Lima (UTC-5)"
        }
    },

    // REDES SOCIALES
    social: {
        facebook: "https://facebook.com/lifextreme", // ⚠️ ACTUALIZAR
        instagram: "https://instagram.com/lifextreme", // ⚠️ ACTUALIZAR
        youtube: "https://youtube.com/@lifextreme", // ⚠️ ACTUALIZAR
        tiktok: "https://tiktok.com/@lifextreme", // ⚠️ ACTUALIZAR
        twitter: "https://twitter.com/lifextreme", // ⚠️ ACTUALIZAR
        linkedin: "https://linkedin.com/company/lifextreme" // ⚠️ ACTUALIZAR
    },

    // CERTIFICACIONES Y LICENCIAS
    certifications: {
        tourism: {
            name: "Registro Nacional de Prestadores de Servicios Turísticos",
            number: "XXXXXXXXX", // ⚠️ ACTUALIZAR
            issuer: "MINCETUR"
        },
        guides: {
            certification: "UIAGM (Union Internationale des Associations de Guides de Montagnes)",
            verified: true
        },
        insurance: {
            provider: "Seguros SURA", // ⚠️ ACTUALIZAR CON ASEGURADORA REAL
            policy: "XXXXXXXXX", // ⚠️ ACTUALIZAR CON NÚMERO DE PÓLIZA
            coverage: "Hasta USD $100,000 por persona"
        }
    },

    // MÉTODOS DE PAGO ACEPTADOS
    paymentMethods: {
        cards: ["Visa", "Mastercard", "American Express", "Diners Club"],
        digital: ["Mercado Pago", "Yape", "Plin", "Culqi"],
        bank: ["BCP", "BBVA", "Interbank", "Scotiabank"],
        international: ["PayPal", "Stripe", "Western Union"]
    },

    // POLÍTICAS
    policies: {
        cancellation: {
            moreThan30Days: {
                refund: 100,
                adminFee: 5,
                description: "Reembolso del 100% menos 5% de gastos administrativos"
            },
            between15And30Days: {
                refund: 50,
                description: "Reembolso del 50%"
            },
            between7And14Days: {
                refund: 25,
                description: "Reembolso del 25%"
            },
            lessThan7Days: {
                refund: 0,
                description: "Sin reembolso"
            }
        },
        minimumAge: 18,
        requiresInsurance: true,
        requiresID: true
    },

    // SEO Y MARKETING
    seo: {
        title: "Lifextreme - Aventuras Extremas en Perú | Tours de Trekking y Montaña",
        description: "Descubre las mejores aventuras extremas en Perú con Lifextreme. Tours de trekking, escalada, selva y más. Personalización con IA. Reserva ahora.",
        keywords: "aventuras perú, trekking cusco, inca trail, salkantay trek, tours extremos, escalada huaraz, selva iquitos",
        ogImage: "https://lifextreme.com/og-image.jpg", // ⚠️ ACTUALIZAR
        twitterHandle: "@lifextreme"
    },

    // ANALYTICS Y TRACKING
    analytics: {
        googleAnalytics: "G-XXXXXXXXXX", // ⚠️ ACTUALIZAR CON GA4 ID
        facebookPixel: "XXXXXXXXXXXXXXX", // ⚠️ ACTUALIZAR
        googleTagManager: "GTM-XXXXXXX", // ⚠️ ACTUALIZAR
        hotjar: "XXXXXXX" // ⚠️ ACTUALIZAR (opcional)
    },

    // API KEYS (NUNCA EXPONGAS KEYS SECRETAS AQUÍ)
    // Solo keys públicas del frontend
    publicKeys: {
        mercadoPago: "APP_USR-XXXXXXXX-XXXXXX", // ⚠️ ACTUALIZAR CON PUBLIC KEY
        stripe: "pk_test_XXXXXXXXXXXXXXXXXXXXXXXX", // ⚠️ ACTUALIZAR
        googleMaps: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" // ⚠️ ACTUALIZAR
    },

    // CONFIGURACIÓN DE EMAILS
    email: {
        provider: "SendGrid", // o "EmailJS", "Mailgun", etc.
        templates: {
            bookingConfirmation: "d-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            paymentConfirmation: "d-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            reminder24h: "d-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            welcome: "d-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        }
    },

    // MONEDA Y PRECIOS
    currency: {
        code: "PEN",
        symbol: "S/",
        name: "Sol Peruano"
    },

    // IDIOMAS SOPORTADOS
    languages: ["es", "en"],
    defaultLanguage: "es"
};

// Exportar configuración
if (typeof module !== 'undefined' && module.exports) {
    module.exports = COMPANY_CONFIG;
}

// Hacer disponible globalmente en el navegador
if (typeof window !== 'undefined') {
    window.COMPANY_CONFIG = COMPANY_CONFIG;
}

console.log('✅ Configuración de empresa cargada');
