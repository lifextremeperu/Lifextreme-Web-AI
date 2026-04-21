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
            name: bookingData.contact?.name || "Invitado Web",
            email: bookingData.contact?.email || "invitado@web.com",
            phone: bookingData.contact?.phone || "000000000"
        }
    });

    if (result.success) {
        // Notificación visual extra
        if (window.showToast) window.showToast('Sistema Central', 'Reserva sincronizada con la nube', 'ri-cloud-check-fill');

        // 🎫 DISPARAR TACTICAL PASSBOARD (Email Confirmation)
        try {
            console.log('🚀 Generando Tactical Passboard para:', bookingData.contact.email);
            fetch('/api/send-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tipo: 'booking_confirmation',
                    fullName: bookingData.contact.name,
                    email: bookingData.contact.email,
                    phone: bookingData.contact.phone,
                    tourName: bookingData.tourName || "Expedición Lifextreme",
                    date: bookingData.date,
                    pax: bookingData.pax
                })
            });
            // Nota: No esperamos el await del email para no bloquear el UI del cliente
        } catch (e) {
            console.error('Error al disparar Passboard:', e);
        }
    }

    return result;
}

console.log('✅ Booking Service Initialized');
