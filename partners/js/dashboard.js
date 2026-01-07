// ============================================
// DASHBOARD JAVASCRIPT (SUPABASE VERSION)
// ============================================

import { supabase } from '../../js/supabase-client.js';

// 🔒 PROTECCIÓN DE RUTA
// Verificar sesión antes de cargar nada
(async function protectRoute() {
    const { data: { session }, error } = await supabase.auth.getSession();

    if (!session) {
        // Si no hay sesión, redirigir al login
        console.log('No session found, redirecting to login...');
        window.location.href = 'index.html';
    } else {
        // Sesión válida
        console.log('Session active:', session.user.email);
        updateUserProfile(session.user);
    }
})();

document.addEventListener('DOMContentLoaded', () => {
    // Si llegamos aquí, asumimos que protectRoute está corriendo, 
    // pero inicializamos la UI de todos modos.
    // En una app SPA real, haríamos render condicional.

    if (window.lucide) window.lucide.createIcons();
    initSidebar();
    initMobileSidebar();
    initLogout();
    initNavigation();
    animateStats();
    loadBookings(); // Esto eventualmente debería cargar datos reales
    loadActivities();
});

// Actualizar datos del usuario en la UI
function updateUserProfile(user) {
    const userNameElements = document.querySelectorAll('.user-name-display');
    const userRoleElements = document.querySelectorAll('.user-role-display');

    // Obtener Metadata del usuario (nombre)
    const fullName = user.user_metadata?.full_name || 'Partner';

    userNameElements.forEach(el => el.textContent = fullName);
    userRoleElements.forEach(el => el.textContent = 'Partner Verificado');
}

// Navigation state
let currentSection = 'dashboard';

// ============================================
// SIDEBAR (Sin cambios mayores)
// ============================================

function initSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebar_collapsed', isCollapsed);
        });

        const savedState = localStorage.getItem('sidebar_collapsed');
        if (savedState === 'true') {
            sidebar.classList.add('collapsed');
        }
    }
}

// ============================================
// MOBILE SIDEBAR
// ============================================

function initMobileSidebar() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    if (mobileMenuBtn && sidebar && overlay) {
        function toggleMobileMenu() {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
            document.body.classList.toggle('overflow-hidden');
        }

        mobileMenuBtn.addEventListener('click', toggleMobileMenu);
        overlay.addEventListener('click', toggleMobileMenu);

        // Close details on link click
        const sidebarLinks = sidebar.querySelectorAll('a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 1024) {
                    toggleMobileMenu();
                }
            });
        });
    }
}

// ============================================
// LOGOUT (CON SUPABASE)
// ============================================

function initLogout() {
    const logoutBtn = document.getElementById('logoutBtn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();

            // Cerrar sesión en Supabase
            const { error } = await supabase.auth.signOut();

            if (error) console.error('Error signing out:', error);

            // Limpiar local storage legacy si existe
            localStorage.removeItem('lifextreme_session');

            // Redirigir al login
            window.location.href = 'index.html';
        });
    }
}

// ============================================
// NAVIGATION (SPA-like behavior)
// ============================================

function initNavigation() {
    const links = document.querySelectorAll('.sidebar-nav a');
    const sections = document.querySelectorAll('.dashboard-section');
    const pageTitle = document.getElementById('pageTitle');

    function navigateTo(targetId) {
        // Update links
        links.forEach(l => {
            l.classList.remove('active');
            if (l.dataset.target === targetId) l.classList.add('active');
        });

        // Update sections
        sections.forEach(s => {
            s.classList.add('hidden');
            if (s.id === targetId) s.classList.remove('hidden');
        });

        // Update title
        if (pageTitle) {
            const activeLink = document.querySelector(`.sidebar-nav a[data-target="${targetId}"]`);
            if (activeLink) {
                const titleText = activeLink.querySelector('span').textContent;
                pageTitle.textContent = titleText;
            }
        }

        currentSection = targetId;

        // Cargar datos específicos de la sección si es necesario
        if (targetId === 'bookings') loadBookings();
        if (targetId === 'activities') loadActivities();
    }

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.dataset.target;
            if (target) navigateTo(target);
        });
    });

    // Handle initial hash routing
    const hash = window.location.hash.substring(1);
    if (hash && document.getElementById(hash)) {
        navigateTo(hash);
    }
}

// ============================================
// STATS ANIMATION
// ============================================

function animateStats() {
    const stats = document.querySelectorAll('.stat-value');

    stats.forEach(stat => {
        const finalValue = parseInt(stat.dataset.value || stat.innerText.replace(/[^0-9]/g, ''));
        // Si no hay data-value, usamos el texto, pero para demo está bien
        if (isNaN(finalValue)) return;

        let startValue = 0;
        const duration = 2000;
        const step = finalValue / (duration / 16);

        function update() {
            startValue += step;
            if (startValue >= finalValue) {
                stat.innerText = stat.innerText.includes('S/') ?
                    'S/ ' + finalValue.toLocaleString() :
                    finalValue.toLocaleString() + (stat.innerText.includes('%') ? '%' : '');
            } else {
                stat.innerText = stat.innerText.includes('S/') ?
                    'S/ ' + Math.floor(startValue).toLocaleString() :
                    Math.floor(startValue).toLocaleString() + (stat.innerText.includes('%') ? '%' : '');
                requestAnimationFrame(update);
            }
        }

        update();
    });
}

// ============================================
// DATA LOADING (MOCK por ahora, conectar a Supabase luego)
// ============================================

function loadBookings() {
    // Aquí iría la llamada a Supabase:
    // const { data } = await supabase.from('bookings').select('*')...

    // Por ahora mantenemos los mocks para que se vea algo
    console.log('Loading bookings...');
}

function loadActivities() {
    console.log('Loading activities...');
}
