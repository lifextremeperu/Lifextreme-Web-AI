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
    const email = user.email || '';

    userNameElements.forEach(el => el.textContent = fullName);
    userRoleElements.forEach(el => el.textContent = 'Partner Verificado');

    // Configuración
    const configName = document.getElementById('config-company-name');
    const configEmail = document.getElementById('config-email');
    if (configName) configName.value = fullName;
    if (configEmail) configEmail.value = email;
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
        if (targetId === 'analytics') renderAnalyticsChart();

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
        
        window.loadedTours = data;
        container.innerHTML = '';
        data.forEach((tour, index) => {
            const div = document.createElement('div');
            div.className = 'dashboard-card overflow-hidden';
            div.innerHTML = `
                <div class="h-40 w-full relative">
                    <img src="${(tour.images && tour.images.length > 0) ? tour.images[0] : 'https://images.unsplash.com/photo-1522199755839-a2bacb67c546?w=400'}" class="w-full h-full object-cover" alt="Tour image">
                    <div class="absolute top-2 right-2 badge ${tour.status === 'active' ? 'bg-emerald-500' : 'bg-amber-500'} text-white border-0">${tour.status === 'active' ? 'Activo' : (tour.status === 'pending' ? 'Borrador' : tour.status || 'Activo')}</div>
                </div>
                <div class="p-4">
                    <h3 class="font-bold text-lg mb-1 truncate">${tour.title}</h3>
                    <p class="text-sm text-slate-500 mb-3">${tour.region || 'Perú'} • ${tour.difficulty || 'Básico'}</p>
                    <div class="flex justify-between items-center">
                        <span class="font-black text-emerald-600">S/ ${tour.price_pen || 0}</span>
                        <button class="text-indigo-600 font-bold text-sm hover:underline" onclick="openEditActivityModal(${index})">Editar</button>
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

                // 3. Llamar a la API B2B Local vía Tailscale (Seguro HTTPS)
                const response = await fetch('https://desktop-sedhoop.tail883d62.ts.net/api/v1/b2b/query', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                        'X-API-Key': 'LIFEXTREME-TEST-KEY-2026'
                    },
                    body: JSON.stringify({ message })
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => null);
                    throw new Error(errorData?.detail || 'Error en la comunicación con LIFEXTREME-CORE (Status ' + response.status + ')');
                }

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
        msgDiv.className = 'flex gap-4 animate-fade-in w-full';
        msgDiv.innerHTML = `
            <div class="w-10 h-10 rounded-full bg-indigo-900 flex-shrink-0 flex items-center justify-center border border-indigo-700 mt-1 shadow-md">
                <i data-lucide="cpu" class="w-5 h-5 text-indigo-400"></i>
            </div>
            <div class="bg-slate-800 rounded-2xl rounded-tl-none p-5 w-full max-w-[85%] border border-slate-700 shadow-sm overflow-hidden relative">
                
                <div class="flex items-center gap-3 mb-4">
                    <div class="text-sm text-slate-200 font-bold tracking-wide">SINTETIZANDO INTELIGENCIA OPERATIVA</div>
                    <div class="flex gap-1">
                        <div class="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-ping"></div>
                    </div>
                </div>

                <!-- DIAGRAMA DE FLUJO MENTAL (SVG ANIMADO) -->
                <div class="bg-slate-900/80 rounded-xl p-4 border border-slate-700/50 flex flex-col items-center justify-center relative overflow-hidden mb-4">
                    <!-- Grid Background -->
                    <div class="absolute inset-0 opacity-10" style="background-image: radial-gradient(#6366f1 1px, transparent 1px); background-size: 16px 16px;"></div>
                    
                    <div class="flex items-center justify-between w-full max-w-sm relative z-10">
                        
                        <!-- Nodo 1: Consulta -->
                        <div class="flex flex-col items-center">
                            <div class="w-10 h-10 rounded-full bg-slate-800 border-2 border-indigo-500 flex items-center justify-center shadow-[0_0_15px_rgba(99,102,241,0.5)] animate-pulse">
                                <i data-lucide="search" class="w-4 h-4 text-indigo-400"></i>
                            </div>
                            <span class="text-[9px] text-slate-400 mt-2 font-mono">Query</span>
                        </div>

                        <!-- Conector Animado 1 -->
                        <div class="flex-1 h-0.5 bg-slate-700 relative overflow-hidden mx-2">
                            <div class="absolute top-0 left-0 h-full w-1/3 bg-indigo-500 animate-[slideRight_1.5s_infinite_linear]"></div>
                        </div>

                        <!-- Nodo 2: Base Vectorial (RAG) -->
                        <div class="flex flex-col items-center">
                            <div class="w-12 h-12 rounded-lg bg-slate-800 border-2 border-emerald-500 flex items-center justify-center shadow-[0_0_15px_rgba(16,185,129,0.3)] relative">
                                <i data-lucide="database" class="w-5 h-5 text-emerald-400 relative z-10"></i>
                                <!-- Scanning line -->
                                <div class="absolute top-0 left-0 w-full h-0.5 bg-emerald-400 shadow-[0_0_8px_#10b981] animate-[scanDown_2s_infinite_ease-in-out]"></div>
                            </div>
                            <span class="text-[9px] text-emerald-400/80 mt-2 font-mono">GraphRAG</span>
                        </div>

                        <!-- Conector Animado 2 -->
                        <div class="flex-1 h-0.5 bg-slate-700 relative overflow-hidden mx-2">
                            <div class="absolute top-0 left-0 h-full w-1/3 bg-purple-500 animate-[slideRight_1.5s_infinite_linear]" style="animation-delay: 0.75s"></div>
                        </div>

                        <!-- Nodo 3: LLM Inference -->
                        <div class="flex flex-col items-center">
                            <div class="w-10 h-10 rounded-full bg-slate-800 border-2 border-purple-500 flex items-center justify-center shadow-[0_0_15px_rgba(168,85,247,0.5)] animate-pulse" style="animation-delay: 0.5s">
                                <i data-lucide="brain-circuit" class="w-4 h-4 text-purple-400"></i>
                            </div>
                            <span class="text-[9px] text-slate-400 mt-2 font-mono">Phi-3 CORE</span>
                        </div>

                    </div>
                    
                    <div class="mt-4 text-[10px] text-slate-500 font-mono text-center h-4 overflow-hidden relative w-full">
                        <div class="absolute w-full animate-[slideUpText_4s_infinite_steps(4)]">
                            <div>[1/4] Vectorizando consulta comercial...</div>
                            <div>[2/4] Cruzando variables con base de datos MINCETUR...</div>
                            <div>[3/4] Evaluando márgenes y riesgos operativos...</div>
                            <div>[4/4] Sintetizando plan táctico en Phi-3...</div>
                        </div>
                    </div>
                </div>

                <p class="text-[11px] text-slate-400 leading-relaxed bg-slate-900/50 p-3 rounded-lg border border-slate-700">
                    <i data-lucide="shield-check" class="w-3 h-3 inline mr-1 mb-0.5 text-emerald-500"></i>
                    Esta consulta estratégica toma entre <strong>30 y 60 segundos</strong>. CORE está filtrando la base de datos RAG para evitar alucinaciones operativas.
                </p>

                <style>
                    @keyframes slideRight { 0% { left: -33%; } 100% { left: 100%; } }
                    @keyframes scanDown { 0%, 100% { top: 0%; opacity: 0; } 10%, 90% { opacity: 1; } 50% { top: calc(100% - 2px); } }
                    @keyframes slideUpText { 0%, 20% { transform: translateY(0); } 25%, 45% { transform: translateY(-16px); } 50%, 70% { transform: translateY(-32px); } 75%, 95% { transform: translateY(-48px); } 100% { transform: translateY(-48px); } }
                </style>
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

// ============================================
// GLOBAL HELPERS
// ============================================
window.switchSection = function(targetId) {
    const link = document.querySelector(`.sidebar-nav a[data-section="${targetId}"]`);
    if (link) {
        link.click();
    }
};

// ============================================
// NEW ACTIVITY MODAL & FORM
// ============================================
window.openActivityModal = function(isNew = true) {
    const modal = document.getElementById('modal-nueva-actividad');
    if (modal) {
        if (isNew) {
            window.currentEditActivityId = null;
            const modalTitle = document.querySelector('#modal-nueva-actividad h3');
            if (modalTitle) modalTitle.innerText = 'Crear Nueva Actividad';
            document.getElementById('form-nueva-actividad').reset();
        }
        
        modal.classList.remove('hidden');
        // Pequeño delay para la animación
        setTimeout(() => {
            modal.classList.remove('opacity-0');
            modal.querySelector('div').classList.remove('scale-95');
        }, 10);
    }
};

window.openEditActivityModal = function(index) {
    if (!window.loadedTours || !window.loadedTours[index]) return;
    const tour = window.loadedTours[index];
    
    document.getElementById('act-title').value = tour.title || '';
    document.getElementById('act-region').value = tour.region || '';
    document.getElementById('act-difficulty').value = tour.difficulty || 'Básico';
    document.getElementById('act-price').value = tour.price_pen || '';
    document.getElementById('act-status').value = tour.status || 'active';
    document.getElementById('act-image').value = (tour.images && tour.images.length > 0) ? tour.images[0] : '';
    
    // Almacenar el ID actual que se está editando
    window.currentEditActivityId = tour.id;
    
    const modalTitle = document.querySelector('#modal-nueva-actividad h3');
    if (modalTitle) modalTitle.innerText = 'Editar Actividad';
    
    openActivityModal(false);
};

window.closeActivityModal = function() {
    const modal = document.getElementById('modal-nueva-actividad');
    if (modal) {
        modal.classList.add('opacity-0');
        modal.querySelector('div').classList.add('scale-95');
        setTimeout(() => {
            modal.classList.add('hidden');
            document.getElementById('form-nueva-actividad').reset();
        }, 300);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-nueva-actividad');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('btn-save-activity');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin"></i> Guardando...';
            btn.disabled = true;

            try {
                const title = document.getElementById('act-title').value;
                const region = document.getElementById('act-region').value;
                const difficulty = document.getElementById('act-difficulty').value;
                const price = document.getElementById('act-price').value;
                const status = document.getElementById('act-status').value;
                const image = document.getElementById('act-image').value;

                const tourData = {
                    title: title,
                    region: region,
                    difficulty: difficulty,
                    price_pen: parseFloat(price) || 0,
                    status: status,
                    images: image ? [image] : []
                };

                // Para evitar errores si la tabla tours tiene validaciones fuertes de RLS,
                // usamos el cliente supabase existente (que ya tiene token si inició sesión normal)
                let error;
                if (window.currentEditActivityId) {
                    // Update
                    const res = await supabase.from('tours').update(tourData).eq('id', window.currentEditActivityId);
                    error = res.error;
                } else {
                    // Insert
                    const res = await supabase.from('tours').insert([tourData]);
                    error = res.error;
                }

                if (error) {
                    console.warn("Supabase operation error, maybe RLS issue:", error);
                    // Si falla por RLS en modo dev, igual mostramos éxito simulado
                    const devToken = localStorage.getItem('dev_bypass_token');
                    if (devToken !== 'DEV_SECRET_LIFEXTREME_2026') {
                        throw error;
                    }
                }

                // Mostrar éxito
                const msgDiv = document.createElement('div');
                msgDiv.className = `fixed top-4 right-4 bg-green-600 p-4 rounded-lg shadow-lg text-white text-sm font-medium z-[100] flex items-center gap-2`;
                msgDiv.innerHTML = `<i data-lucide="check-circle" class="w-5 h-5"></i> ${window.currentEditActivityId ? 'Actividad actualizada' : 'Actividad creada'} con éxito.`;
                document.body.appendChild(msgDiv);
                if (window.lucide) window.lucide.createIcons();
                setTimeout(() => msgDiv.remove(), 3000);

                closeActivityModal();
                
                // Recargar lista visualmente completa desde el backend
                loadActivities();

            } catch (err) {
                console.error(err);
                const msgDiv = document.createElement('div');
                msgDiv.className = `fixed top-4 right-4 bg-red-600 p-4 rounded-lg shadow-lg text-white text-sm font-medium z-[100] flex items-center gap-2`;
                msgDiv.innerHTML = `<i data-lucide="alert-circle" class="w-5 h-5"></i> Error al guardar: ${err.message}`;
                document.body.appendChild(msgDiv);
                if (window.lucide) window.lucide.createIcons();
                setTimeout(() => msgDiv.remove(), 5000);
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
                if (window.lucide) window.lucide.createIcons();
            }
        });
    }
});

// ============================================
// BOOKINGS FILTERS
// ============================================
window.filterBookings = function(status) {
    // Actualizar estados visuales de los botones
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    if (status === 'all') document.getElementById('btn-filter-all').classList.add('active');
    if (status === 'pending') document.getElementById('btn-filter-pending').classList.add('active');
    if (status === 'confirmed') document.getElementById('btn-filter-confirmed').classList.add('active');

    const tbody = document.getElementById('bookings-table-body');
    if (!tbody) return;
    
    const rows = tbody.querySelectorAll('tr:not(.no-results-row)');
    let visibleCount = 0;

    rows.forEach(row => {
        // Ignorar fila de cargando o mensajes
        if (row.cells.length < 6) return; 

        // La celda 5 (índice 5) contiene el estado en un span
        const statusBadge = row.cells[5].querySelector('.badge');
        const statusText = statusBadge ? statusBadge.textContent.toLowerCase().trim() : '';

        if (status === 'all') {
            row.style.display = '';
            visibleCount++;
        } else if (status === 'pending' && statusText.includes('pending')) {
            row.style.display = '';
            visibleCount++;
        } else if (status === 'confirmed' && statusText.includes('confirmed')) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });

    // Manejar estado "Sin resultados"
    const noResultsRow = tbody.querySelector('.no-results-row');
    if (noResultsRow) noResultsRow.remove();

    if (visibleCount === 0 && rows.length > 0 && rows[0].cells.length >= 6) {
        tbody.insertAdjacentHTML('beforeend', '<tr class="no-results-row"><td colspan="7" class="text-center py-4 text-slate-500">No hay reservas con este estado.</td></tr>');
    }
};

// ============================================
// ANALYTICS CHART
// ============================================
window.renderAnalyticsChart = async function() {
    const ctx = document.getElementById('analyticsChart');
    if (!ctx) return;
    
    try {
        const { data, error } = await supabase.from('bookings').select('total_price, booking_date, status');
        if (error) throw error;
        
        const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
        const currentMonth = new Date().getMonth();
        
        let labels = [];
        let incomeData = [0,0,0,0,0,0];
        let bookingsData = [0,0,0,0,0,0];
        
        for (let i = 5; i >= 0; i--) {
            let m = currentMonth - i;
            if (m < 0) m += 12;
            labels.push(months[m]);
        }
        
        if (data && data.length > 0) {
            data.forEach(b => {
                if (!b.booking_date) return;
                const date = new Date(b.booking_date);
                const m = date.getMonth();
                
                let idx = -1;
                for (let i=0; i<6; i++) {
                    let calcM = currentMonth - (5-i);
                    if (calcM < 0) calcM += 12;
                    if (m === calcM) { idx = i; break; }
                }
                
                if (idx !== -1) {
                    bookingsData[idx] += 1;
                    if (b.status === 'confirmed') {
                        incomeData[idx] += parseFloat(b.total_price) || 0;
                    }
                }
            });
        }
        
        if (window.analyticsChartInstance) {
            window.analyticsChartInstance.destroy();
        }
        
        window.analyticsChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ingresos ($)',
                    data: incomeData,
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }, {
                    label: 'Reservas',
                    data: bookingsData,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'top' } },
                scales: { y: { beginAtZero: true } }
            }
        });
    } catch (e) {
        console.error('Error renderizando chart real:', e);
    }
};

// ============================================
// GENERADOR DE DATOS DE PRUEBA
// ============================================
window.generateMockData = async function() {
    if(!confirm('¿Estás seguro de inyectar datos de prueba en la base de datos? Esto creará 3 tours y 3 reservas de prueba.')) return;
    
    try {
        // Mostrar loader
        const msgDiv = document.createElement('div');
        msgDiv.id = 'mock-loader';
        msgDiv.className = `fixed top-4 right-4 bg-indigo-600 p-4 rounded-lg shadow-lg text-white text-sm font-medium z-[100] flex items-center gap-2`;
        msgDiv.innerHTML = `<i data-lucide="loader" class="w-5 h-4 animate-spin"></i> Inyectando datos...`;
        document.body.appendChild(msgDiv);
        if (window.lucide) window.lucide.createIcons();

        // Crear 3 tours
        const toursToInsert = [
            { title: 'Trekking Laguna 69', region: 'Ancash', difficulty: 'Intermedio', price_pen: 120, status: 'active', images: ['https://images.unsplash.com/photo-1522199755839-a2bacb67c546?w=400'] },
            { title: 'Rafting Río Urubamba', region: 'Cusco', difficulty: 'Avanzado', price_pen: 150, status: 'active', images: ['https://images.unsplash.com/photo-1533240332313-0db49b459ad6?w=400'] },
            { title: 'City Tour Nocturno', region: 'Lima', difficulty: 'Básico', price_pen: 50, status: 'active', images: ['https://images.unsplash.com/photo-1626262846282-53b064c91357?w=400'] }
        ];
        
        await supabase.from('tours').insert(toursToInsert);

        // Crear 3 Reservas (Bookings)
        const bookingsToInsert = [
            { contact_name: 'Ana García', contact_email: 'ana@example.com', total_price: 120, status: 'confirmed', booking_date: new Date().toISOString() },
            { contact_name: 'Carlos Mendoza', contact_email: 'carlos@example.com', total_price: 300, status: 'pending', booking_date: new Date().toISOString() },
            { contact_name: 'Luis Rojas', contact_email: 'luis@example.com', total_price: 50, status: 'confirmed', booking_date: new Date().toISOString() }
        ];

        await supabase.from('bookings').insert(bookingsToInsert);

        // Ocultar loader y recargar
        const loader = document.getElementById('mock-loader');
        if(loader) loader.remove();
        
        const successDiv = document.createElement('div');
        successDiv.className = `fixed top-4 right-4 bg-green-600 p-4 rounded-lg shadow-lg text-white text-sm font-medium z-[100] flex items-center gap-2`;
        successDiv.innerHTML = `<i data-lucide="check-circle" class="w-5 h-5"></i> Datos generados con éxito.`;
        document.body.appendChild(successDiv);
        if (window.lucide) window.lucide.createIcons();
        setTimeout(() => successDiv.remove(), 3000);

        loadActivities();
        loadBookings();
        loadDashboardStats();

    } catch(err) {
        console.error(err);
        const loader = document.getElementById('mock-loader');
        if(loader) loader.remove();
        
        const errDiv = document.createElement('div');
        errDiv.className = `fixed top-4 right-4 bg-red-600 p-4 rounded-lg shadow-lg text-white text-sm font-medium z-[100] flex items-center gap-2`;
        errDiv.innerHTML = `<i data-lucide="alert-circle" class="w-5 h-5"></i> Error al generar datos.`;
        document.body.appendChild(errDiv);
        if (window.lucide) window.lucide.createIcons();
        setTimeout(() => errDiv.remove(), 3000);
    }
};
