// ============================================
// SUPABASE DATA LOADER
// Carga datos desde Supabase para Lifextreme
// ============================================

import { supabase } from './supabase-client.js'

// ============================================
// FUNCIONES DE CARGA DE DATOS
// ============================================

/**
 * Cargar tours desde Supabase
 */
export async function loadToursFromSupabase() {
    try {
        const { data: tours, error } = await supabase
            .from('tours')
            .select('*')
            .eq('active', true)
            .order('featured', { ascending: false })
            .order('created_at', { ascending: false })

        if (error) throw error

        // Transformar datos de Supabase al formato esperado por la app
        return tours.map(tour => ({
            id: tour.id,
            title: tour.title,
            dept: tour.region,
            duration: `${tour.duration_days} días`,
            price: parseFloat(tour.price_pen),
            img: tour.images?.[0] || 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4',
            cat: tour.category,
            difficulty: tour.difficulty,
            description: tour.description,
            featured: tour.featured,
            // Datos adicionales para el modal
            genInfo: {
                duration: `${tour.duration_days} días`,
                guide: 'Español / Inglés',
                cancelPolicy: 'Flexible'
            }
        }))
    } catch (error) {
        console.error('Error cargando tours desde Supabase:', error)
        // Retornar array vacío en caso de error
        return []
    }
}

/**
 * Obtener un tour específico por ID
 */
export async function getTourById(tourId) {
    try {
        const { data: tour, error } = await supabase
            .from('tours')
            .select('*')
            .eq('id', tourId)
            .single()

        if (error) throw error

        return {
            id: tour.id,
            title: tour.title,
            dept: tour.region,
            duration: `${tour.duration_days} días`,
            price: parseFloat(tour.price_pen),
            img: tour.images?.[0] || 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4',
            cat: tour.category,
            difficulty: tour.difficulty,
            description: tour.description
        }
    } catch (error) {
        console.error('Error obteniendo tour:', error)
        return null
    }
}

/**
 * Filtrar tours por región
 */
export async function getToursByRegion(region) {
    try {
        const { data: tours, error } = await supabase
            .from('tours')
            .select('*')
            .eq('active', true)
            .eq('region', region)
            .order('created_at', { ascending: false })

        if (error) throw error

        return tours.map(tour => ({
            id: tour.id,
            title: tour.title,
            dept: tour.region,
            duration: `${tour.duration_days} días`,
            price: parseFloat(tour.price_pen),
            img: tour.images?.[0] || 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4',
            cat: tour.category
        }))
    } catch (error) {
        console.error('Error filtrando tours:', error)
        return []
    }
}

/**
 * Obtener tours destacados
 */
export async function getFeaturedTours() {
    try {
        const { data: tours, error } = await supabase
            .from('tours')
            .select('*')
            .eq('active', true)
            .eq('featured', true)
            .limit(6)

        if (error) throw error

        return tours.map(tour => ({
            id: tour.id,
            title: tour.title,
            dept: tour.region,
            duration: `${tour.duration_days} días`,
            price: parseFloat(tour.price_pen),
            img: tour.images?.[0] || 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4',
            cat: tour.category,
            featured: true
        }))
    } catch (error) {
        console.error('Error obteniendo tours destacados:', error)
        return []
    }
}

// ============================================
// FUNCIONES DE INICIALIZACIÓN
// ============================================

/**
 * Inicializar datos de la aplicación
 * Carga tours desde Supabase y los asigna a window.tours
 */
export async function initializeAppData() {
    console.log('🔄 Cargando datos desde Supabase...')

    try {
        // Cargar tours
        const tours = await loadToursFromSupabase()

        if (tours.length > 0) {
            // Asignar a window.tours para compatibilidad con el código existente
            window.tours = tours
            console.log(`✅ ${tours.length} tours cargados desde Supabase`)
            return true
        } else {
            console.warn('⚠️ No se encontraron tours en Supabase')
            // Mantener datos mock si no hay datos en Supabase
            return false
        }
    } catch (error) {
        console.error('❌ Error inicializando datos:', error)
        return false
    }
}

// ============================================
// EXPORTAR PARA USO GLOBAL
// ============================================

export default {
    loadToursFromSupabase,
    getTourById,
    getToursByRegion,
    getFeaturedTours,
    initializeAppData
}
