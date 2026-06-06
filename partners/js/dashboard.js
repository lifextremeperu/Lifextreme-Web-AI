// ============================================
// DASHBOARD JAVASCRIPT (SUPABASE VERSION)
// ============================================

import { supabase } from '../../js/supabase-client.js';

// 🔒 PROTECCIÓN DE RUTA ACTIVADA
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
            if (l.dataset.section === targetId) l.classList.add('active');
        });

        // Update sections
        sections.forEach(s => {
            s.classList.add('hidden');
            if (s.id === `section-${targetId}`) s.classList.remove('hidden');
        });

        // Update title
        if (pageTitle) {
            const activeLink = document.querySelector(`.sidebar-nav a[data-section="${targetId}"]`);
            if (activeLink) {
                const titleText = activeLink.querySelector('span').textContent;
                pageTitle.innerText = titleText;
            }
        }

        currentSection = targetId;

        // Custom Loaders
        if (targetId === 'reservas') loadBookings();
        if (targetId === 'actividades') loadActivities();

        // Re-init icons for new section
        if (window.lucide) window.lucide.createIcons();
    }

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.dataset.section;
            if (target) navigateTo(target);
        });
    });

    // Handle initial hash routing
    // const hash = window.location.hash.substring(1);
    // if (hash) navigateTo(hash);
}

// ============================================
// SUSTAINABILITY TABS
// ============================================
window.switchSusTab = function (tab) {
    const btnImpact = document.getElementById('btn-tab-impact');
    const btnAcademy = document.getElementById('btn-tab-academy');
    const viewImpact = document.getElementById('tab-impact');
    const viewAcademy = document.getElementById('tab-academy');

    if (tab === 'impact') {
        // UI
        btnImpact.classList.remove('text-slate-500', 'hover:bg-slate-50');
        btnImpact.classList.add('bg-emerald-50', 'text-emerald-700');

        btnAcademy.classList.add('text-slate-500', 'hover:bg-slate-50');
        btnAcademy.classList.remove('bg-emerald-50', 'text-emerald-700');

        // Views
        viewImpact.classList.remove('hidden');
        viewAcademy.classList.add('hidden');
    } else {
        // UI
        btnAcademy.classList.remove('text-slate-500', 'hover:bg-slate-50');
        btnAcademy.classList.add('bg-emerald-50', 'text-emerald-700');

        btnImpact.classList.add('text-slate-500', 'hover:bg-slate-50');
        btnImpact.classList.remove('bg-emerald-50', 'text-emerald-700');

        // Views
        viewAcademy.classList.remove('hidden');
        viewImpact.classList.add('hidden');
    }
};

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

// ============================================
// AI INTELLIGENCE CHAT (B2B)
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('ai-chat-form');
    const chatInput = document.getElementById('ai-chat-input');
    const chatHistory = document.getElementById('ai-chat-history');

    if (chatForm && chatInput && chatHistory) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            // 1. Mostrar mensaje del usuario
            appendMessage(message, 'user');
            chatInput.value = '';

            // 2. Mostrar indicador de carga
            const loadingId = appendLoading();

            try {
                // 3. Llamar a la API B2B Local
                const response = await fetch('http://localhost:8000/api/v1/b2b/query', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'X-API-Key': 'LIFEXTREME-TEST-KEY-2026' // La clave MVP acordada
                    },
                    body: JSON.stringify({ message })
                });

                if (!response.ok) throw new Error('Error en la comunicación con LIFEXTREME-CORE');

                const data = await response.json();
                
                // 4. Quitar loading y mostrar respuesta
                removeLoading(loadingId);
                appendMessage(data.mensaje_principal, 'ai', data.fuentes_utilizadas);
                
            } catch (error) {
                console.error(error);
                removeLoading(loadingId);
                appendMessage('Error de conexión con el motor GraphRAG. Por favor, verifica que la API local esté corriendo.', 'error');
            }
        });
    }

    function appendMessage(text, sender, sources = []) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'flex gap-4 animate-fade-in';
        
        if (sender === 'user') {
            msgDiv.classList.add('flex-row-reverse');
            msgDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-slate-700 flex-shrink-0 flex items-center justify-center border border-slate-600 mt-1">
                    <i data-lucide="user" class="w-4 h-4 text-slate-300"></i>
                </div>
                <div class="bg-emerald-600 rounded-2xl rounded-tr-none p-4 max-w-[85%] border border-emerald-500 shadow-sm text-white">
                    <p>${escapeHtml(text)}</p>
                </div>
            `;
        } else if (sender === 'ai') {
            let sourcesHtml = '';
            if (sources && sources.length > 0) {
                sourcesHtml = `<div class="mt-3 pt-3 border-t border-slate-700/50 flex flex-wrap gap-2">
                    <span class="text-[10px] text-slate-500 uppercase tracking-widest font-bold w-full">Fuentes (GraphRAG):</span>
                    ${sources.map(s => `<span class="bg-slate-900 px-2 py-1 rounded text-[10px] text-emerald-500 border border-slate-700">${escapeHtml(s)}</span>`).join('')}
                </div>`;
            }

            msgDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-emerald-500/20 flex-shrink-0 flex items-center justify-center border border-emerald-500/30 mt-1">
                    <i data-lucide="cpu" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div class="bg-slate-800 rounded-2xl rounded-tl-none p-4 max-w-[85%] border border-slate-700 shadow-sm text-slate-300">
                    <div class="prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-pre:bg-slate-900 prose-pre:border prose-pre:border-slate-700">${formatMarkdown(text)}</div>
                    ${sourcesHtml}
                </div>
            `;
        } else {
            msgDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-red-500/20 flex-shrink-0 flex items-center justify-center border border-red-500/30 mt-1">
                    <i data-lucide="alert-triangle" class="w-4 h-4 text-red-400"></i>
                </div>
                <div class="bg-red-900/20 rounded-2xl rounded-tl-none p-4 max-w-[85%] border border-red-500/30 text-red-400">
                    <p>${escapeHtml(text)}</p>
                </div>
            `;
        }

        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        if (window.lucide) window.lucide.createIcons({ root: msgDiv });
    }

    function appendLoading() {
        const id = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = 'flex gap-4 animate-fade-in';
        msgDiv.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-emerald-500/20 flex-shrink-0 flex items-center justify-center border border-emerald-500/30 mt-1">
                <i data-lucide="cpu" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div class="bg-slate-800 rounded-2xl rounded-tl-none p-4 max-w-[85%] border border-slate-700 shadow-sm flex items-center gap-2">
                <div class="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
        `;
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        if (window.lucide) window.lucide.createIcons({ root: msgDiv });
        return id;
    }

    function removeLoading(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function escapeHtml(unsafe) {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    function formatMarkdown(text) {
        // Formateo muy básico para negritas y saltos de línea (idealmente usar marked.js)
        return text
            .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
            .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
            .replace(/\\n/g, '<br/>');
    }
});
