// ============================================
// BOOKING SERVICE
// Puente entre App y Supabase para Reservas
// ============================================

import { createBooking } from './supabase-client.js'

/**
 * Función expuesta globalmente para procesar reservas
 */
window.processBookingCusco = async function (bookingData) {
    console.log('🔄 Procesando reserva vía Supabase Service...', bookingData);

    // Validar datos mínimos
    if (!bookingData.tourId || !bookingData.date) {
        console.error('Datos incompletos para reserva');
        return { success: false, message: 'Datos incompletos' };
    }

    // Llamar a Supabase
    const result = await createBooking({
        tourId: bookingData.tourId,
        date: bookingData.date, // Formato esperado: YYYY-MM-DD
        pax: bookingData.pax || 1,
        totalPrice: bookingData.price || 0,
        contact: {
            name: "Invitado Web", // Por ahora hardcodeado o tomar de inputs si existieran
            email: "invitado@web.com",
            phone: "000000000"
        }
    });

    if (result.success) {
        // Notificación visual extra si se desea
        if (window.showToast) window.showToast('Sistema Central', 'Reserva sincronizada con la nube', 'ri-cloud-check-fill');
    }

    return result;
}

console.log('✅ Booking Service Initialized');
