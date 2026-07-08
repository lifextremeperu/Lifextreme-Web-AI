// ============================================
// ANALYTICS SERVICE (GA4)
// Servicio para rastreo de eventos E-commerce
// ============================================

/**
 * Helper para enviar eventos a GA4
 */
const logEvent = (eventName, params) => {
    if (window.gtag) {
        window.gtag('event', eventName, params);
        console.log(`📊 GA4 Event: ${eventName}`, params);
    } else {
        console.warn('⚠️ Google Analytics no está inicializado');
    }
}

// Objeto global de Analytics expuesto para la app
window.LifextremeAnalytics = {

    /**
     * Rastrea cuando un usuario ve el detalle de un tour
     * Evento: view_item
     */
    trackViewItem: (tour) => {
        logEvent('view_item', {
            currency: 'PEN',
            value: tour.price,
            items: [{
                item_id: tour.id,
                item_name: tour.title,
                item_category: tour.dept || 'General',
                price: tour.price,
                quantity: 1
            }]
        });
    },

    /**
     * Rastrea cuando un usuario añade algo a la mochila
     * Evento: add_to_cart
     */
    trackAddToCart: (item) => {
        logEvent('add_to_cart', {
            currency: 'PEN',
            value: item.price,
            items: [{
                item_id: item.id,
                item_name: item.name,
                item_category: 'Tour',
                price: item.price,
                quantity: item.pax || 1
            }]
        });
    },

    /**
     * Rastrea el inicio del checkout
     * Evento: begin_checkout
     */
    trackBeginCheckout: (totalValue, items) => {
        logEvent('begin_checkout', {
            currency: 'PEN',
            value: totalValue,
            items: items.map(i => ({
                item_id: i.id,
                item_name: i.name,
                price: i.price
            }))
        });
    },

    /**
     * Rastrea búsqueda interna
     * Evento: search
     */
    trackSearch: (searchTerm) => {
        logEvent('search', {
            search_term: searchTerm
        });
    },

    /**
     * Rastrea leads (ej: contacto partner)
     * Evento: generate_lead
     */
    trackLead: (details) => {
        logEvent('generate_lead', {
            ...details
        });
    }
};

console.log('✅ Analytics Service Initialized');
