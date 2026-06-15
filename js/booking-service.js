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

        // 🎫 DISPARAR TACTICAL PASSBOARD (Email Confirmation vía EmailJS)
        try {
            console.log('🚀 Generando Tactical Passboard para:', bookingData.contact.email);
            
            // TODO: REEMPLAZA ESTAS CLAVES CON LAS TUYAS DE EMAILJS.COM
            const EMAILJS_PUBLIC_KEY = "TU_PUBLIC_KEY"; // Pégala aquí
            const EMAILJS_SERVICE_ID = "TU_SERVICE_ID"; // Ej: service_123xyz
            const EMAILJS_TEMPLATE_ID = "TU_TEMPLATE_ID"; // Ej: template_456abc
            
            if(window.emailjs) {
                emailjs.init(EMAILJS_PUBLIC_KEY);
                
                emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
                    to_name: bookingData.contact.name,
                    to_email: bookingData.contact.email,
                    phone: bookingData.contact.phone,
                    tour_name: bookingData.tourName || "Expedición Lifextreme",
                    date: bookingData.date,
                    pax: bookingData.pax,
                    total_price: bookingData.price || 0,
                    reply_to: "contacto@lifextreme.store"
                }).then(function(response) {
                   console.log('✅ Correo enviado exitosamente!', response.status, response.text);
                }, function(error) {
                   console.error('❌ Error enviando el correo...', error);
                });
            } else {
                console.warn("EmailJS no está cargado en la página.");
            }
        } catch (e) {
            console.error('Error al disparar Passboard:', e);
        }
    }

    return result;
}

console.log('✅ Booking Service Initialized');
