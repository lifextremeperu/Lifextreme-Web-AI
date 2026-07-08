/**
 * PriceEngine - Utilidad Táctica de Precisión
 * Maneja los cálculos de descuentos y anclaje de precios de forma determinista.
 */
const PriceEngine = {
    /**
     * Calcula un descuento con precisión de centavos para evitar errores de punto flotante.
     * @param {number} amount - Precio base en S/
     * @param {number} discountPercent - Porcentaje (ej. 20 para 20%)
     * @returns {Object} { original, discounted, savings }
     */
    calculateKitDiscount(amount, discountPercent = 20) {
        // Trabajamos en céntimos para precisión absoluta
        const originalCents = Math.round(amount * 100);
        const discountFactor = (100 - discountPercent) / 100;
        const discountedCents = Math.round(originalCents * discountFactor);
        const savingsCents = originalCents - discountedCents;

        return {
            original: (originalCents / 100).toFixed(2),
            discounted: (discountedCents / 100).toFixed(2),
            savings: (savingsCents / 100).toFixed(2),
            percent: discountPercent
        };
    },

    /**
     * Formatea un precio para el sistema de anclaje visual.
     * @param {number|string} price 
     * @returns {string} Formato monetario Lifextreme
     */
    format(price) {
        return `S/ ${parseFloat(price).toLocaleString('es-PE', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    }
};

window.PriceEngine = PriceEngine;
