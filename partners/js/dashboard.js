// ============================================
// DASHBOARD JAVASCRIPT
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    initSidebar();
    initMobileSidebar();
    initLogout();
    initNavigation();
    animateStats();
    loadBookings();
    loadActivities();
});

// Navigation state
let currentSection = 'dashboard';

// ============================================
// SIDEBAR
// ============================================

function initSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');

            // Save state to localStorage
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebar_collapsed', isCollapsed);
        });

        // Restore state from localStorage
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

    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 1024) {
                if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                    sidebar.classList.remove('active');
                }
            }
        });

        // Close sidebar when clicking on a nav item on mobile
        const navItems = sidebar.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                if (window.innerWidth <= 1024) {
                    sidebar.classList.remove('active');
                }
            });
        });
    }
}

// ============================================
// NAVIGATION
// ============================================

function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item[data-section]');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const section = item.getAttribute('data-section');
            if (section) {
                switchSection(section);
            }
        });
    });

    // Check URL for initial section
    const hash = window.location.hash.substring(1);
    if (hash && ['dashboard', 'reservas', 'actividades', 'finanzas', 'clientes', 'analytics', 'mensajes', 'configuracion'].includes(hash)) {
        switchSection(hash);
    }
}

function switchSection(sectionId) {
    console.log(`Switching to section: ${sectionId}`);

    // Update active state in sidebar
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-section') === sectionId) {
            item.classList.add('active');
        }
    });

    // Toggle sections
    const sections = document.querySelectorAll('.dashboard-section');
    sections.forEach(section => {
        section.classList.remove('active');
        if (section.id === `section-${sectionId}`) {
            section.classList.add('active');
        }
    });

    // Update current section
    currentSection = sectionId;
    window.location.hash = sectionId;

    // Refresh icons
    lucide.createIcons();

    // Trigger section-specific logic
    if (sectionId === 'reservas') {
        loadBookings();
    } else if (sectionId === 'actividades') {
        loadActivities();
    }
}

window.switchSection = switchSection;

// ============================================
// DATA LOADING (MOCK)
// ============================================

const MOCK_BOOKINGS = [
    { id: 'LX-4902', cliente: 'Carlos Mendoza', actividad: 'Paracaidismo Tándem', fecha: '2026-01-06 10:00', monto: '$250.00', estado: 'confirmed' },
    { id: 'LX-4903', cliente: 'Ana García', actividad: 'Escalada en Roca', fecha: '2026-01-07 08:30', monto: '$120.00', estado: 'pending' },
    { id: 'LX-4904', cliente: 'Grupo Aventura (6)', actividad: 'Rafting Nivel 4', fecha: '2026-01-10 14:00', monto: '$540.00', estado: 'confirmed' },
    { id: 'LX-4905', cliente: 'Luis Torres', actividad: 'MTB Extremo', fecha: '2026-01-12 09:00', monto: '$85.00', estado: 'confirmed' },
    { id: 'LX-4906', cliente: 'Maria Rojas', actividad: 'Bungee Jumping', fecha: '2026-01-15 11:00', monto: '$150.00', estado: 'pending' },
];

const MOCK_ACTIVITIES = [
    { name: 'Paracaidismo Tándem', category: 'Aéreo', img: 'https://images.unsplash.com/photo-1521336575822-6da63fb45455?w=400&q=80', active: true, price: '$250', bookings: 124 },
    { name: 'Rafting Nivel 4', category: 'Acuático', img: 'https://images.unsplash.com/photo-1530866495547-15bcdc58421a?w=400&q=80', active: true, price: '$90', bookings: 86 },
    { name: 'Escalada en Roca', category: 'Montaña', img: 'https://images.unsplash.com/photo-1522163182402-834f871fd851?w=400&q=80', active: true, price: '$120', bookings: 42 },
    { name: 'Bungee Jumping', category: 'Extremo', img: 'https://images.unsplash.com/photo-1563299796-17596ed6b017?w=400&q=80', active: false, price: '$150', bookings: 31 }
];

function loadBookings() {
    const tableBody = document.getElementById('bookings-table-body');
    if (!tableBody) return;

    tableBody.innerHTML = MOCK_BOOKINGS.map(booking => `
        <tr>
            <td><span class="font-bold">#${booking.id}</span></td>
            <td>${booking.cliente}</td>
            <td>${booking.actividad}</td>
            <td>${booking.fecha}</td>
            <td><span class="font-bold">${booking.monto}</span></td>
            <td><span class="booking-status ${booking.estado}">${booking.estado === 'confirmed' ? 'Confirmada' : 'Pendiente'}</span></td>
            <td>
                <div class="flex gap-2">
                    <button class="icon-btn sm" title="Ver Detalles"><i data-lucide="eye"></i></button>
                    ${booking.estado === 'pending' ? `<button class="icon-btn sm text-secondary" title="Confirmar"><i data-lucide="check"></i></button>` : ''}
                </div>
            </td>
        </tr>
    `).join('');

    lucide.createIcons();
}

function loadActivities() {
    const container = document.getElementById('activities-container');
    if (!container) return;

    container.innerHTML = MOCK_ACTIVITIES.map(activity => `
        <div class="activity-card">
            <div class="activity-image" style="background-image: url('${activity.img}')">
                <span class="activity-badge">${activity.active ? 'Activa' : 'Pausada'}</span>
            </div>
            <div class="activity-info">
                <div class="activity-category">${activity.category}</div>
                <h3 class="activity-name">${activity.name}</h3>
                <div class="activity-footer">
                    <div class="activity-stats">
                        <span><i data-lucide="calendar"></i> ${activity.bookings}</span>
                        <span><i data-lucide="tag"></i> ${activity.price}</span>
                    </div>
                    <div class="flex gap-2">
                        <button class="icon-btn sm"><i data-lucide="edit-3"></i></button>
                        <button class="icon-btn sm"><i data-lucide="bar-chart-2"></i></button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');

    lucide.createIcons();
}

// ============================================
// LOGOUT
// ============================================

function initLogout() {
    const logoutBtn = document.querySelector('.logout-btn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
                localStorage.removeItem('lifextreme_session');
                window.location.href = 'login.html';
            }
        });
    }
}

// ============================================
// ANIMATE STATS
// ============================================

function animateStats() {
    const statValues = document.querySelectorAll('.stat-value');

    statValues.forEach(stat => {
        const text = stat.textContent;
        const match = text.match(/[\d,.]+/);
        if (match) {
            const number = parseFloat(match[0].replace(/,/g, ''));
            const prefix = text.substring(0, text.indexOf(match[0]));
            const suffix = text.substring(text.indexOf(match[0]) + match[0].length);

            animateValue(stat, 0, number, 1500, prefix, suffix);
        }
    });
}

function animateValue(element, start, end, duration, prefix = '', suffix = '') {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }

        const formatted = Math.floor(current).toLocaleString();
        element.textContent = prefix + formatted + suffix;
    }, 16);
}

// ============================================
// REAL-TIME UPDATES (DEMO)
// ============================================

setInterval(() => {
    const notificationDot = document.querySelector('.notification-dot');
    if (notificationDot && Math.random() > 0.7) {
        notificationDot.style.animation = 'pulse 1s ease-in-out';
        setTimeout(() => {
            notificationDot.style.animation = '';
        }, 1000);
    }
}, 10000);

const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.5); opacity: 0.7; }
    }
`;
document.head.appendChild(style);
