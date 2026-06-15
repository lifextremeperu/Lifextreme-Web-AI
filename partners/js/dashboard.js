// ============================================
// DASHBOARD JAVASCRIPT (SUPABASE VERSION)
// ============================================

import { supabase } from '../../js/supabase-client.js';

// 🔒 PROTECCIÓN DE RUTA ACTIVADA
(async function protectRoute() {
    const devToken = localStorage.getItem('dev_bypass_token');
    if (devToken === 'DEV_SECRET_LIFEXTREME_2026') {
        console.warn('DEV BYPASS: Saltando verificación de Supabase.');
        updateUserProfile({ user_metadata: { full_name: "Admin Lifextreme" }, email: "admin@lifextreme.local" });
        return;
    }

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
    loadDashboardStats(); // Cargar estadísticas del resumen principal
    loadBookings(); 
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
            s.classList.remove('active');
            s.classList.add('hidden');
            if (s.id === `section-${targetId}`) {
                s.classList.remove('hidden');
                s.classList.add('active');
            }
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
        if (targetId === 'clientes') loadClients();

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
// DATA LOADING (Conectado a Supabase)
// ============================================

async function loadBookings() {
    const tbody = document.getElementById('bookings-table-body');
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4">Cargando reservas reales...</td></tr>';
    
    try {
        const { data, error } = await supabase.from('bookings').select('*').limit(5);
        if (error) throw error;
        
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-slate-500">No hay reservas activas en tu cuenta.</td></tr>';
            return;
        }
        
        tbody.innerHTML = '';
        data.forEach(booking => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="font-bold text-slate-700">#${booking.id.substring(0,8)}</td>
                <td>
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs">
                            ${(booking.contact_name || 'U').charAt(0).toUpperCase()}
                        </div>
                        <div>
                            <p class="font-bold text-sm text-slate-800">${booking.contact_name || 'Sin Nombre'}</p>
                            <p class="text-xs text-slate-500">${booking.contact_email || 'Sin Email'}</p>
                        </div>
                    </div>
                </td>
                <td class="text-sm">Tour #${booking.tour_id ? booking.tour_id.substring(0,6) : 'N/A'}</td>
                <td class="text-sm">${booking.booking_date || 'N/A'}</td>
                <td class="font-bold text-slate-700">$${booking.total_price || 0}</td>
                <td><span class="badge ${booking.status === 'confirmed' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}">${booking.status || 'pending'}</span></td>
                <td><button class="btn btn-secondary text-xs py-1 px-2">Ver Detalles</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error('Error cargando reservas:', e);
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-red-500">Error conectando con la base de datos.</td></tr>';
    }
}

async function loadActivities() {
    const container = document.getElementById('activities-container');
    if (!container) return;
    
    container.innerHTML = '<div class="text-center py-4 text-slate-500 w-full">Cargando tus tours desde el catálogo...</div>';
    
    try {
        const { data, error } = await supabase.from('tours').select('*').limit(3);
        if (error) throw error;
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div class="text-center py-4 text-slate-500 w-full">No tienes actividades creadas. ¡Empieza creando tu primer tour!</div>';
            return;
        }
        
        container.innerHTML = '';
        data.forEach(tour => {
            const div = document.createElement('div');
            div.className = 'dashboard-card overflow-hidden';
            div.innerHTML = `
                <div class="h-40 w-full relative">
                    <img src="${(tour.images && tour.images.length > 0) ? tour.images[0] : 'https://images.unsplash.com/photo-1522199755839-a2bacb67c546?w=400'}" class="w-full h-full object-cover" alt="Tour image">
                    <div class="absolute top-2 right-2 badge bg-emerald-500 text-white border-0">Activo</div>
                </div>
                <div class="p-4">
                    <h3 class="font-bold text-lg mb-1 truncate">${tour.title}</h3>
                    <p class="text-sm text-slate-500 mb-3">${tour.region || 'Perú'} • ${tour.difficulty || 'Básico'}</p>
                    <div class="flex justify-between items-center">
                        <span class="font-black text-emerald-600">S/ ${tour.price_pen || 0}</span>
                        <button class="text-indigo-600 font-bold text-sm hover:underline">Editar</button>
                    </div>
                </div>
            `;
            container.appendChild(div);
        });
    } catch (e) {
        console.error('Error cargando actividades:', e);
        container.innerHTML = '<div class="text-center py-4 text-red-500 w-full">Error conectando con la base de datos.</div>';
    }
}

async function loadDashboardStats() {
    const elIngresos = document.getElementById('stat-ingresos');
    const elReservas = document.getElementById('stat-reservas');
    const elClientes = document.getElementById('stat-clientes');
    
    if (!elIngresos || !elReservas || !elClientes) return;

    try {
        const { data: bookings, error } = await supabase.from('bookings').select('total_price, status, contact_email');
        if (error) throw error;

        if (!bookings || bookings.length === 0) {
            elIngresos.textContent = '$0.00';
            elReservas.textContent = '0';
            elClientes.textContent = '0';
            return;
        }

        // Calcular ingresos totales (reservas confirmadas)
        const totalIncome = bookings
            .filter(b => b.status === 'confirmed')
            .reduce((sum, b) => sum + (parseFloat(b.total_price) || 0), 0);

        // Contar reservas activas
        const activeBookings = bookings.length;

        // Contar clientes únicos
        const uniqueClients = new Set(bookings.map(b => b.contact_email).filter(Boolean)).size;

        // Actualizar UI
        elIngresos.textContent = '$' + totalIncome.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        elReservas.textContent = activeBookings.toString();
        elClientes.textContent = uniqueClients.toString();

    } catch (e) {
        console.error('Error cargando estadísticas globales:', e);
        elIngresos.textContent = 'Error';
        elReservas.textContent = 'Error';
        elClientes.textContent = 'Error';
    }
}

async function loadClients() {
    const tbody = document.getElementById('clients-table-body');
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-slate-500">Extrayendo datos de clientes...</td></tr>';
    
    try {
        const { data: bookings, error } = await supabase.from('bookings').select('contact_name, contact_email, total_price');
        if (error) throw error;
        
        if (!bookings || bookings.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-slate-500">Aún no tienes clientes registrados.</td></tr>';
            return;
        }
        
        // Agrupar por email
        const clientsMap = {};
        bookings.forEach(b => {
            if (!b.contact_email) return;
            if (!clientsMap[b.contact_email]) {
                clientsMap[b.contact_email] = {
                    name: b.contact_name || 'Sin Nombre',
                    email: b.contact_email,
                    tours: 0,
                    totalSpent: 0
                };
            }
            clientsMap[b.contact_email].tours += 1;
            clientsMap[b.contact_email].totalSpent += parseFloat(b.total_price) || 0;
        });
        
        const clients = Object.values(clientsMap).sort((a, b) => b.totalSpent - a.totalSpent);
        
        tbody.innerHTML = '';
        clients.forEach(client => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="font-bold text-slate-800">${client.name}</td>
                <td class="text-slate-500 text-sm">${client.email}</td>
                <td><span class="badge bg-slate-100 text-slate-700">${client.tours}</span></td>
                <td class="font-black text-emerald-600">$${client.totalSpent.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error('Error cargando clientes:', e);
        tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-red-500">Error al conectar con la base de datos.</td></tr>';
    }
}

// ============================================
// AI INTELLIGENCE CHAT (B2B)
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('ai-chat-form');
    const chatInput = document.getElementById('ai-chat-input');
    const chatHistory = document.getElementById('ai-chat-history');

    // Función global para sugerencias
    window.sendSuggestion = function(text) {
        if (chatInput && chatForm) {
            chatInput.value = text;
            chatForm.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        }
    };

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
                // Obtener token JWT de Supabase o Token Dev
                const devToken = localStorage.getItem('dev_bypass_token');
                let token = '';
                
                if (devToken === 'DEV_SECRET_LIFEXTREME_2026') {
                    token = 'DEV_SECRET_LIFEXTREME_2026';
                } else {
                    const { data: { session } } = await supabase.auth.getSession();
                    token = session ? session.access_token : '';
                }

                // 3. Llamar a la API B2B Local (Modelo 1 - JWT)
                const response = await fetch('/api/v1/b2b/query', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
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
                <div class="w-10 h-10 rounded-full bg-slate-700 flex-shrink-0 flex items-center justify-center border border-slate-600 shadow-md">
                    <i data-lucide="user" class="w-5 h-5 text-slate-300"></i>
                </div>
                <div class="bg-indigo-600 rounded-2xl rounded-tr-none p-4 max-w-[85%] border border-indigo-500 shadow-sm text-white">
                    <p class="text-sm">${escapeHtml(text)}</p>
                </div>
            `;
        } else if (sender === 'ai') {
            let sourcesHtml = '';
            if (sources && sources.length > 0) {
                sourcesHtml = `<div class="mt-4 pt-3 border-t border-slate-700/50 flex flex-wrap gap-2">
                    <span class="text-[10px] text-slate-500 uppercase tracking-widest font-bold w-full flex items-center gap-1"><i data-lucide="database" class="w-3 h-3"></i> Fuentes (GraphRAG):</span>
                    ${sources.map(s => `<span class="bg-slate-900 px-2 py-1 rounded text-[10px] text-indigo-400 border border-slate-700">${escapeHtml(s)}</span>`).join('')}
                </div>`;
            }

            msgDiv.innerHTML = `
                <div class="w-10 h-10 rounded-full bg-indigo-900 flex-shrink-0 flex items-center justify-center border border-indigo-700 mt-1 shadow-md">
                    <i data-lucide="cpu" class="w-5 h-5 text-indigo-400"></i>
                </div>
                <div class="bg-slate-800 rounded-2xl rounded-tl-none p-5 max-w-[85%] border border-slate-700 shadow-sm text-slate-200">
                    <div class="prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-pre:bg-slate-900 prose-pre:border prose-pre:border-slate-700">${formatMarkdown(text)}</div>
                    ${sourcesHtml}
                </div>
            `;
        } else {
            msgDiv.innerHTML = `
                <div class="w-10 h-10 rounded-full bg-red-900/50 flex-shrink-0 flex items-center justify-center border border-red-700 mt-1">
                    <i data-lucide="alert-triangle" class="w-5 h-5 text-red-400"></i>
                </div>
                <div class="bg-red-900/20 rounded-2xl rounded-tl-none p-4 max-w-[85%] border border-red-500/30 text-red-400 text-sm">
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
            <div class="w-10 h-10 rounded-full bg-indigo-900 flex-shrink-0 flex items-center justify-center border border-indigo-700 mt-1 shadow-md">
                <i data-lucide="cpu" class="w-5 h-5 text-indigo-400"></i>
            </div>
            <div class="bg-slate-800 rounded-2xl rounded-tl-none p-4 max-w-[85%] border border-slate-700 shadow-sm">
                <div class="flex items-center gap-2 mb-2">
                    <div class="text-sm text-slate-200 font-bold">Analizando Inteligencia Operativa...</div>
                    <div class="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    <div class="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
                <p class="text-[11px] text-amber-400/90 leading-tight bg-amber-900/20 p-2 rounded-lg border border-amber-700/30">
                    <i data-lucide="info" class="w-3 h-3 inline mr-1 mb-0.5"></i>
                    Esta consulta profunda toma entre <strong>60 y 120 segundos</strong>. La Inteligencia Artificial Local (Phi-3) está cruzando datos de GraphRAG para garantizar precisión estratégica corporativa. Por favor, espera sin cerrar la ventana.
                </p>
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
        if (!text) return "";
        // Formateo básico para negritas y saltos de línea
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br/>');
    }
});
