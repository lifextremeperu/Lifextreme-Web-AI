/**
 * PriceEngine - Utilidad Táctica de Precisión
 * Maneja los cálculos de descuentos, anclaje de precios y MULTI-MONEDA (PEN, USD, BRL).
 */
const PriceEngine = {
    currentCurrency: localStorage.getItem('lifextreme_currency') || 'PEN',
    rates: { PEN: 1, USD: 0.27, BRL: 1.35 }, // Tasas de respaldo

    async init() {
        try {
            // Obtener tasas de cambio en vivo desde API pública gratuita
            const res = await fetch('https://open.er-api.com/v6/latest/PEN');
            const data = await res.json();
            if (data && data.rates) {
                this.rates.USD = data.rates.USD;
                this.rates.BRL = data.rates.BRL;
                this.rates.PEN = 1;
            }
        } catch(e) {
            console.log('[PriceEngine] Usando tasas de cambio de respaldo por fallo de red.');
        }
    },

    setCurrency(curr) {
        this.currentCurrency = curr;
        localStorage.setItem('lifextreme_currency', curr);
    },

    convert(amountInPen) {
        return amountInPen * this.rates[this.currentCurrency];
    },

    calculateKitDiscount(amount, discountPercent = 20) {
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

    format(priceInPen) {
        const converted = this.convert(parseFloat(priceInPen));
        
        let prefix = 'S/';
        if (this.currentCurrency === 'USD') prefix = '$';
        if (this.currentCurrency === 'BRL') prefix = 'R$';

        return `${prefix} ${converted.toLocaleString('es-PE', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    }
};

window.PriceEngine = PriceEngine;
// Inicializar tasas en tiempo real
PriceEngine.init();
