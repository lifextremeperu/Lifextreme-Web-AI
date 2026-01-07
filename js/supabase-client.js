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

// Ver archivo completo en: js/supabase-client.js
// Este archivo contiene todas las funciones de:
// - Autenticación
// - Perfiles de usuario
// - Tours
// - Reservas
// - Recomendaciones IA
// - Reseñas
// - Analytics
// - Storage

export default supabase
