// SUPABASE CLIENT - MODO DEMO/LOCAL
// Este archivo funciona SIN configuración para desarrollo
// Cambia a modo PRODUCCIÓN cuando tengas credenciales reales

const SUPABASE_MODE = 'DEMO'; // Cambiar a 'PRODUCTION' cuando tengas credenciales

// Credenciales (actualizar cuando crees tu proyecto Supabase)
const SUPABASE_URL = 'https://XXXXXXXX.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';

// Cliente Supabase
let supabase = null;

// Inicializar según modo
if (SUPABASE_MODE === 'PRODUCTION' && window.supabase) {
    try {
        supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        console.log('✅ Supabase conectado (PRODUCCIÓN)');
    } catch (error) {
        console.warn('⚠️ Error conectando Supabase, usando modo DEMO');
    }
}

if (!supabase || SUPABASE_MODE === 'DEMO') {
    console.log('🔧 Supabase en modo DEMO (guardando solo en localStorage)');
}

// ==========================================
// FUNCIONES DE BASE DE DATOS
// ==========================================

// Guardar reserva
async function saveBooking(bookingData) {
    if (supabase && SUPABASE_MODE === 'PRODUCTION') {
        try {
            const { data, error } = await supabase
                .from('bookings')
                .insert([{
                    user_name: bookingData.userName,
                    user_email: bookingData.userEmail,
                    user_phone: bookingData.userPhone || '',
                    tour_id: bookingData.tourId,
                    tour_name: bookingData.tourName,
                    tour_date: bookingData.tourDate,
                    participants: bookingData.participants,
                    total_price: bookingData.totalPrice,
                    payment_status: 'pending'
                }])
                .select();

            if (error) throw error;
            console.log('✅ Reserva guardada en Supabase:', data[0]);
            return data[0];
        } catch (error) {
            console.error('❌ Error guardando reserva en Supabase:', error);
            return saveDemoBooking(bookingData);
        }
    } else {
        return saveDemoBooking(bookingData);
    }
}

// Guardar perfil IA
async function saveAIProfile(profileData) {
    if (supabase && SUPABASE_MODE === 'PRODUCTION') {
        try {
            const { data, error } = await supabase
                .from('ai_profiles')
                .upsert([{
                    user_email: profileData.personal.email,
                    profile_data: profileData
                }])
                .select();

            if (error) throw error;
            console.log('✅ Perfil IA guardado en Supabase:', data[0]);
            return data[0];
        } catch (error) {
            console.error('❌ Error guardando perfil IA en Supabase:', error);
            return saveDemoAIProfile(profileData);
        }
    } else {
        return saveDemoAIProfile(profileData);
    }
}

// Actualizar estado de pago
async function updatePaymentStatus(bookingId, status, paymentId) {
    if (supabase && SUPABASE_MODE === 'PRODUCTION') {
        try {
            const { data, error } = await supabase
                .from('bookings')
                .update({
                    payment_status: status,
                    payment_id: paymentId
                })
                .eq('id', bookingId)
                .select();

            if (error) throw error;
            console.log('✅ Estado de pago actualizado:', data[0]);
            return data[0];
        } catch (error) {
            console.error('❌ Error actualizando pago:', error);
            return null;
        }
    } else {
        console.log('🔧 DEMO: Estado de pago actualizado localmente');
        return { id: bookingId, payment_status: status, payment_id: paymentId };
    }
}

// ==========================================
// FUNCIONES DEMO (localStorage)
// ==========================================

function saveDemoBooking(bookingData) {
    const bookings = JSON.parse(localStorage.getItem('demo_bookings') || '[]');
    const newBooking = {
        id: 'demo_' + Date.now(),
        ...bookingData,
        payment_status: 'pending',
        created_at: new Date().toISOString()
    };
    bookings.push(newBooking);
    localStorage.setItem('demo_bookings', JSON.stringify(bookings));
    console.log('🔧 DEMO: Reserva guardada en localStorage:', newBooking);
    return Promise.resolve(newBooking);
}

function saveDemoAIProfile(profileData) {
    const profiles = JSON.parse(localStorage.getItem('demo_ai_profiles') || '[]');
    const newProfile = {
        id: 'demo_' + Date.now(),
        user_email: profileData.personal.email,
        profile_data: profileData,
        created_at: new Date().toISOString()
    };

    // Actualizar si ya existe
    const existingIndex = profiles.findIndex(p => p.user_email === profileData.personal.email);
    if (existingIndex >= 0) {
        profiles[existingIndex] = newProfile;
    } else {
        profiles.push(newProfile);
    }

    localStorage.setItem('demo_ai_profiles', JSON.stringify(profiles));
    console.log('🔧 DEMO: Perfil IA guardado en localStorage:', newProfile);
    return Promise.resolve(newProfile);
}

// ==========================================
// FUNCIONES DE UTILIDAD
// ==========================================

// Ver todas las reservas (DEMO)
function viewDemoBookings() {
    const bookings = JSON.parse(localStorage.getItem('demo_bookings') || '[]');
    console.table(bookings);
    return bookings;
}

// Ver todos los perfiles IA (DEMO)
function viewDemoProfiles() {
    const profiles = JSON.parse(localStorage.getItem('demo_ai_profiles') || '[]');
    console.table(profiles.map(p => ({
        email: p.user_email,
        name: p.profile_data.personal.fullName,
        experience: p.profile_data.adventure.experienceLevel,
        created: p.created_at
    })));
    return profiles;
}

// Exportar funciones globalmente
window.saveBooking = saveBooking;
window.saveAIProfile = saveAIProfile;
window.updatePaymentStatus = updatePaymentStatus;
window.viewDemoBookings = viewDemoBookings;
window.viewDemoProfiles = viewDemoProfiles;

console.log(`
╔════════════════════════════════════════════════════════════╗
║  SUPABASE CLIENT - MODO ${SUPABASE_MODE.padEnd(10)}                        ║
╠════════════════════════════════════════════════════════════╣
║  ${SUPABASE_MODE === 'DEMO' ? '🔧 Guardando en localStorage (sin configuración)' : '✅ Conectado a Supabase en la nube'}        ║
║                                                            ║
║  Funciones disponibles:                                    ║
║  • saveBooking(data)         - Guardar reserva            ║
║  • saveAIProfile(data)        - Guardar perfil IA         ║
║  • updatePaymentStatus(...)   - Actualizar pago           ║
║  • viewDemoBookings()         - Ver reservas (DEMO)       ║
║  • viewDemoProfiles()         - Ver perfiles (DEMO)       ║
╚════════════════════════════════════════════════════════════╝
`);
