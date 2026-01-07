// ============================================
// LIFEXTREME SUPABASE CLIENT
// Cliente de Supabase para el Frontend
// ============================================

import { createClient } from '@supabase/supabase-js'

// Configuración de Supabase
// IMPORTANTE: Reemplaza estos valores con tus credenciales reales
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://tu-proyecto.supabase.co'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'tu-anon-key-aqui'

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
