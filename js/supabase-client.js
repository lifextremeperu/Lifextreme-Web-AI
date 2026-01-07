// ============================================
// LIFEXTREME SUPABASE CLIENT
// Cliente de Supabase para el Frontend
// ============================================

import { createClient } from '@supabase/supabase-js'

// ✅ Configuración de Supabase - Lifextreme Backend
const supabaseUrl = 'https://zobpkmiqrvhbepqnjshr.supabase.co'
const supabaseAnonKey = 'sb_publishable_pBMaD6Mm-6Pi5cwwp3UUsw_Pndjw-mo'

// Crear cliente de Supabase
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: true
    }
})

// ============================================
// 🛒 GESTIÓN DE RESERVAS
// ============================================

/**
 * Crear una nueva reserva
 * @param {Object} bookingData - Datos de la reserva
 */
export async function createBooking(bookingData) {
    try {
        console.log('📝 Creando reserva en Supabase...', bookingData);

        const { data, error } = await supabase
            .from('bookings')
            .insert([
                {
                    tour_id: bookingData.tourId,
                    booking_date: bookingData.date,
                    num_people: bookingData.pax,
                    total_price: bookingData.totalPrice,
                    status: 'pending', // Estado inicial
                    contact_name: bookingData.contact.name || 'Invitado',
                    contact_email: bookingData.contact.email || 'no-email',
                    contact_phone: bookingData.contact.phone || 'no-phone',
                    // Si el usuario está autenticado, agregamos su ID
                    user_id: (await supabase.auth.getUser()).data.user?.id || null
                }
            ])
            .select()

        if (error) throw error

        console.log('✅ Reserva creada exitosamente:', data);
        return { success: true, booking: data[0] }
    } catch (error) {
        console.error('❌ Error creando reserva:', error)
        return { success: false, error }
    }
}

/**
 * Obtener reservas de un usuario
 */
export async function getUserBookings() {
    try {
        const { data: { user } } = await supabase.auth.getUser()
        if (!user) return []

        const { data, error } = await supabase
            .from('bookings')
            .select(`
                *,
                tours (
                    title,
                    images,
                    region
                )
            `)
            .eq('user_id', user.id)
            .order('created_at', { ascending: false })

        if (error) throw error
        return data
    } catch (error) {
        console.error('Error obteniendo reservas:', error)
        return []
    }
}

// ============================================
// 👤 PERFILES DE USUARIO
// ============================================

export async function getUserProfile() {
    try {
        const { data: { user } } = await supabase.auth.getUser()
        if (!user) return null

        const { data, error } = await supabase
            .from('users_profiles')
            .select('*')
            .eq('id', user.id)
            .single()

        if (error && error.code !== 'PGRST116') throw error // Ignorar error si no existe perfil
        return data
    } catch (error) {
        console.error('Error perfil:', error)
        return null
    }
}

export default supabase
