// --- APPLICATION LOGIC (MODULARIZED V29) ---

// --- STATE ---
const backpack = window.useBackpack();
const membership = window.useMembership();
const draftBooking = window.useDraftBooking();

let activeTour = null;
let participants = 1;
let selectedAddons = [];
let selectedDay = null;
let activeFeedbackTour = null;
let currentRatings = { guide: 0, equipment: 0, difficulty: 0 };
let currentMonthIndex = 2; // Default starting at March (index 2)
let currentYear = 2026;
let wishlist = JSON.parse(localStorage.getItem('lifextreme_wishlist')) || [];

let completedTours = [
    { id: 1, title: 'Inca Trail 4D', ratings: { guide: 5, equipment: 4, difficulty: 5 } },
    { id: 2, title: 'Salkantay Trek 5D', dept: 'Cusco', img: 'https://images.unsplash.com/photo-1590520611221-998bd104f6ed', ratings: null },
    { id: 6, title: 'Santa Cruz Trek 4D', ratings: { guide: 5, equipment: 5, difficulty: 4 } },
    { id: 21, title: 'Sandboarding Huacachina', ratings: null }
];

const monthNames = {
    es: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    en: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
};

let currentLang = localStorage.getItem('lifextreme_lang') || 'es';

const translations = {
    es: {
        nav_home: "Inicio",
        nav_destinos: "Destinos",
        nav_eventos: "Eventos",
        nav_equipos: "Equipos",
        nav_guias: "Guías",
        user_status: "Socio Elite Active",
        hero_tag: "Aventura de Alta Gama",
        hero_title_1: "Domina el",
        hero_title_2: "Territorio",
        hero_desc: "Reserva expediciones regionales, certifica tus habilidades en talleres técnicos y obtén equipo de elite en un solo lugar.",
        btn_explore: "Explorar Mapa",
        btn_events: "Ver Eventos",
        quiz_prompt: "¿No sabes qué elegir?",
        quiz_desc: "Haz el Test de Aventura y gana -10%",
        membership_alert: "⚠️ ALERTA DE EXPIRACIÓN",
        membership_title_1: "Tu acceso",
        membership_title_2: "Elite",
        membership_title_3: "expira pronto",
        membership_desc_1: "Estás a punto de perder un ahorro de",
        membership_desc_2: "en tu mochila táctica. Activa ahora para asegurar tus beneficios.",
        timer_hours: "Horas",
        timer_min: "Min",
        timer_sec: "Seg",
        btn_secure_discount: "Asegurar mi Descuento Elite",
        membership_action_required: "Acción requerida para mantener el status de socio",
        backpack_title: "MOCHILA TÁCTICA",
        backpack_tag: "Preparada para la acción",
        backpack_empty: "Mochila Vacía",
        backpack_total: "Inversión en Aventura",
        btn_continue_exploring: "Seguir Explorando",
        btn_checkout: "PAGAR AHORA",
        section_destinos: "Exploración Nacional",
        section_eventos: "Competencias & Festivales",
        section_equipos: "Catálogo Pro",
        section_guias: "Staff de Guías Elite",
        modal_duration: "Duración",
        modal_guide: "Guía",
        modal_cancel: "Cancelación",
        modal_itinerary: "Itinerary Táctico",
        modal_gear: "Equipo Sugerido",
        modal_addons: "Servicios Adicionales",
        modal_summary: "Resumen de Despliegue",
        modal_date: "Seleccionar Fecha",
        modal_pax: "Participantes",
        btn_next: "Siguiente Paso",
        btn_prev: "Paso Anterior",
        btn_book: "RESERVAR AHORA",
        status_no_events: "Sin eventos programados para esta región en 2026",
        events_official_calendar: "Calendario Oficial 2026",
        equip_sidebar_backpacks: "Mochilas",
        equip_sidebar_footwear: "Calzado",
        equip_sidebar_accessories: "Accesorios",
        equip_sidebar_all: "Ver Todo",
        backpack_investment: "Inversión en Aventura",
        backpack_member_discount: "-15% Descuento Apl.",
        backpack_protection: "Tus objetos están protegidos y listos para el despliegue.",
        footer_rights: "© 2026 Lifextreme Pro System. All Rights Reserved.",
        wizard_step_1: "Configura",
        wizard_step_2: "Equipo",
        wizard_step_3: "Pago",
        quiz_q1: "¿Cuál es tu nivel de locura?",
        quiz_a1_1: "Principiante",
        quiz_a1_2: "Elite Pro",
        quiz_q2: "¿Cuál es tu terreno?",
        quiz_a2_1: "🏔️ Montaña",
        quiz_a2_2: "🌴 Selva",
        card_inscription: "Inscripción",
        card_specialty: "Especialidad",
        card_mission_docs: "Documentación de Misión",
        card_suggestion: "Equipo Sugerido",
        card_add: "Añadir",
        msg_scanning: "Escaneando base de datos táctica...",
        msg_analyzing: "Lifextreme AI está analizando tu perfil..."
    },
    en: {
        nav_home: "Home",
        nav_destinos: "Destinations",
        nav_eventos: "Events",
        nav_equipos: "Equipment",
        nav_guias: "Guides",
        user_status: "Elite Active Member",
        hero_tag: "Premium Adventure",
        hero_title_1: "Master the",
        hero_title_2: "Territory",
        hero_desc: "Book regional expeditions, certify your skills in technical workshops, and get elite gear in one place.",
        btn_explore: "Explore Map",
        btn_events: "View Events",
        quiz_prompt: "Not sure what to choose?",
        quiz_desc: "Take the Adventure Test and win -10%",
        membership_alert: "⚠️ EXPIRATION ALERT",
        membership_title_1: "Your",
        membership_title_2: "Elite",
        membership_title_3: "access expires soon",
        membership_desc_1: "You are about to lose a saving of",
        membership_desc_2: "in your tactical backpack. Activate now to secure your benefits.",
        timer_hours: "Hours",
        timer_min: "Min",
        timer_sec: "Sec",
        btn_secure_discount: "Secure my Elite Discount",
        membership_action_required: "Action required to maintain member status",
        backpack_title: "TACTICAL BACKPACK",
        backpack_tag: "Ready for action",
        backpack_empty: "Empty Backpack",
        backpack_total: "Adventure Investment",
        btn_continue_exploring: "Keep Exploring",
        btn_checkout: "Secure Possession",
        section_destinos: "National Exploration",
        section_eventos: "Competitions & Festivals",
        section_equipos: "Pro Catalog",
        section_guias: "Elite Guides Staff",
        modal_duration: "Duration",
        modal_guide: "Guide",
        modal_cancel: "Cancellation",
        modal_itinerary: "Tactical Itinerary",
        modal_gear: "Suggested Gear",
        modal_addons: "Additional Services",
        modal_summary: "Deployment Summary",
        modal_date: "Select Date",
        modal_pax: "Participants",
        btn_next: "Next Step",
        btn_prev: "Previous Step",
        btn_book: "BOOK NOW",
        status_no_events: "No events scheduled for this region in 2026",
        events_official_calendar: "Official Calendar 2026",
        equip_sidebar_backpacks: "Backpacks",
        equip_sidebar_footwear: "Footwear",
        equip_sidebar_accessories: "Accessories",
        equip_sidebar_all: "View All",
        backpack_investment: "Adventure Investment",
        backpack_member_discount: "-15% Discount Applied",
        backpack_protection: "Your items are protected and ready for deployment.",
        footer_rights: "© 2026 Lifextreme Pro System. All Rights Reserved.",
        wizard_step_1: "Configure",
        wizard_step_2: "Gear",
        wizard_step_3: "Payment",
        quiz_q1: "What is your madness level?",
        quiz_a1_1: "Novice",
        quiz_a1_2: "Elite Pro",
        quiz_q2: "What is your terrain?",
        quiz_a2_1: "🏔️ Mountain",
        quiz_a2_2: "🌴 Jungle",
        card_inscription: "Registration",
        card_specialty: "Specialty",
        card_mission_docs: "Mission Docs",
        card_suggestion: "Suggested Gear",
        card_add: "Add",
        msg_scanning: "Scanning tactical database...",
        msg_analyzing: "Lifextreme AI is analyzing your profile..."
    }
};

// --- UTILS ---
function saveWishlist() { localStorage.setItem('lifextreme_wishlist', JSON.stringify(wishlist)); }

// --- CALENDAR & DATE SELECTOR ---
function renderMonths() {
    const selector = document.getElementById('month-selector');
    if (!selector) return;

    let monthsHtml = '';
    for (let i = 2; i < 12; i++) {
        monthsHtml += `<div class="month-chip ${currentMonthIndex === i ? 'active' : ''}" onclick="selMonth(${i})">${monthNames[currentLang][i]}</div>`;
    }
    selector.innerHTML = monthsHtml;
}

function selMonth(index) {
    currentMonthIndex = index;
    selectedDay = null;
    const display = document.getElementById('month-display');
    if (display) display.innerText = `${monthNames[currentLang][index]} ${currentYear}`;
    renderMonths();
    renderCalendar();
}

function renderCalendar() {
    const grid = document.getElementById('calendar-grid');
    if (!grid) return;

    const daysInMonth = new Date(currentYear, currentMonthIndex + 1, 0).getDate();
    let daysHtml = '';
    for (let i = 1; i <= daysInMonth; i++) {
        daysHtml += `<div class="day-box ${selectedDay === i ? 'selected' : ''}" onclick="selDay(${i})">${i}</div>`;
    }
    grid.innerHTML = daysHtml;
}

function selDay(d) {
    selectedDay = d;
    document.querySelectorAll('.day-box').forEach(b => b.classList.remove('selected'));
    event.target.classList.add('selected');
}

// --- WISHLIST ---
function toggleWishlist(id) {
    event.stopPropagation();
    const index = wishlist.indexOf(id);
    let msg = '';
    if (index > -1) {
        wishlist.splice(index, 1);
        msg = currentLang === 'es' ? 'Eliminado de tus favoritos' : 'Removed from wishlist';
        showToast('Info', msg, 'ri-heart-line');
    } else {
        wishlist.push(id);
        msg = currentLang === 'es' ? '¡Añadido a tus favoritos!' : 'Added to wishlist!';
        showToast('Favoritos', msg, 'ri-heart-fill');
    }
    saveWishlist();
    renderAll();
    updateWishlistDashboard();
}

function updateWishlistDashboard() {
    const container = document.getElementById('wishlist-container');
    if (!container) return;

    if (wishlist.length === 0) {
        container.innerHTML = `<p class="text-[10px] font-bold text-slate-400 italic">No tienes desafíos guardados aún. Explora destinos y añade los que te inspiren.</p>`;
        return;
    }

    container.innerHTML = wishlist.map(id => {
        const tour = tours.find(t => t.id === id);
        return `
            <div class="flex items-center gap-4 bg-slate-50 p-4 rounded-3xl border border-slate-100 group hover:border-primary transition-all">
                <img src="${tour.img}?w=100" class="w-12 h-12 rounded-xl object-cover">
                <div class="flex-1">
                    <p class="text-[9px] font-black text-primary uppercase">${tour.dept}</p>
                    <p class="text-[11px] font-black italic text-slate-800">${tour.title}</p>
                </div>
                <button data-action="toggle-wishlist" data-id="${id}" class="text-slate-300 hover:text-secondary p-2"><i class="ri-delete-bin-line"></i></button>
            </div>
        `;
    }).join('');
}

// --- BOOKING WIZARD MOTOR ---
function openBooking(tourId) {
    const allEvents = window.events || [];
    activeTour = tours.find(t => t.id === tourId) || allEvents.find(e => e.id === tourId);
    if (!activeTour) return;

    // Reset State
    participants = 1;
    selectedAddons = [];
    selectedDay = null;

    // Init Draft
    draftBooking.updateDraft({ step: 1, tourId, completed: false });
    renderWizardStep(1);

    // Initial Data Fill
    document.getElementById('b-title').innerText = activeTour.title;
    document.getElementById('b-dept').innerText = activeTour.dept || activeTour.cat;
    document.getElementById('b-duration').innerText = activeTour.genInfo?.duration || activeTour.duration || 'Flexible';
    document.getElementById('b-guide-lang').innerText = activeTour.genInfo?.guide || activeTour.guide || 'Español / Inglés';
    document.getElementById('b-cancel-policy').innerText = activeTour.genInfo?.cancelPolicy || activeTour.cancelPolicy || 'Estándar';

    // Itinerary Flow (Adaptive for Tours & Events)
    const flow = document.getElementById('itinerary-flow');
    let itineraryData = [];

    if (activeTour.fullItinerary) {
        itineraryData = activeTour.fullItinerary;
    } else if (activeTour.whatYouDo) {
        // Adapt Events 'whatYouDo' to allow itinerary display
        itineraryData = activeTour.whatYouDo.map((item, i) => ({ day: `Paso ${i + 1}`, desc: item }));
    }

    flow.innerHTML = itineraryData.map((item, idx) => `
        <div class="mb-6 relative border-l-2 border-slate-100 pl-6 pb-2">
            <div class="absolute -left-1.5 top-0 w-3 h-3 bg-primary rounded-full border-2 border-white"></div>
            <h6 class="text-[10px] font-black uppercase mb-1">${item.day || 'Fase ' + (idx + 1)}</h6>
            <p class="text-xs font-bold text-slate-500">${item.desc || item}</p>
        </div>
    `).join('') || '<div class="p-4 bg-slate-50 rounded-2xl text-[10px] italic text-slate-400">Detalles de misión clasificados. Ver en el punto de encuentro.</div>';

    // Tools for Step 2
    renderStep2Tools();

    document.getElementById('booking-modal').classList.remove('hidden');

    // Cargar imagen para el Moto Sensorial
    const bImg = document.getElementById('b-img');
    if (bImg && activeTour) bImg.src = activeTour.img;

    updateTotalPrice();
    renderMonths();
    renderCalendar();

    // Re-init Sensory Observers for Modal Content
    if (window.SensoryEngine) {
        SensoryEngine.activeTour = activeTour; // Pasar referencia al motor
        SensoryEngine.init();
    }
}

function renderStep2Tools() {
    if (!activeTour) return;
    const recommended = (window.equips || []).slice(0, 3); // Dynamic logic later
    document.getElementById('recommended-equipment-list').innerHTML = recommended.map(e => `
        <div class="flex items-center justify-between bg-white p-4 rounded-2xl border border-slate-100">
            <div class="flex items-center gap-4">
                <img src="${e.img}?w=80" class="w-12 h-12 rounded-xl object-cover">
                <div>
                    <p class="text-[9px] font-black text-slate-400 uppercase">${e.cat}</p>
                    <p class="text-[11px] font-black italic">${e.name}</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <p class="text-xs font-black text-primary">S/ ${e.price}</p>
                <button data-action="add-cart-short" data-name="${e.name}" data-price="${e.price}" data-img="${e.img}" class="bg-slate-50 p-2 rounded-lg hover:bg-slate-200">
                     <i class="ri-add-line"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function nextBookingStep() {
    const { draftBooking: draft } = draftBooking.getState();
    const currentStep = draft.step;

    if (currentStep === 1) {
        if (!selectedDay) { alert('Selecciona una fecha de despliegue.'); return; }
    }

    if (currentStep < 3) {
        const nextStep = currentStep + 1;
        draftBooking.updateDraft({ step: nextStep });
        renderWizardStep(nextStep);
    }
}

function prevBookingStep() {
    const { draftBooking: draft } = draftBooking.getState();
    const currentStep = draft.step;
    if (currentStep > 1) {
        const prevStep = currentStep - 1;
        draftBooking.updateDraft({ step: prevStep });
        renderWizardStep(prevStep);
    }
}

function renderWizardStep(step) {
    const progress = (step / 3) * 100;
    document.getElementById('wizard-progress-bar').style.width = `${progress}%`;

    document.querySelectorAll('.booking-wizard-step').forEach(el => el.classList.add('hidden'));
    document.getElementById(`booking-step-${step}`).classList.remove('hidden');

    // Sphere indicators
    for (let i = 1; i <= 3; i++) {
        const sphere = document.getElementById(`wiz-step-${i}`);
        const label = sphere.nextElementSibling;
        if (i < step) {
            sphere.className = 'w-8 h-8 rounded-full bg-emerald-500 text-white flex items-center justify-center text-[10px] font-black';
            sphere.innerHTML = '<i class="ri-check-line"></i>';
            label.className = 'text-[8px] font-black uppercase tracking-tighter mt-1 text-emerald-500';
        } else if (i === step) {
            sphere.className = 'w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center text-[10px] font-black shadow-lg';
            sphere.innerText = i;
            label.className = 'text-[8px] font-black uppercase tracking-tighter mt-1 text-primary';
        } else {
            sphere.className = 'w-8 h-8 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center text-[10px] font-black';
            sphere.innerText = i;
            label.className = 'text-[8px] font-black uppercase tracking-tighter mt-1 text-slate-400';
        }
    }

    const nextBtn = document.getElementById('wiz-next-btn');
    const prevBtn = document.getElementById('wiz-prev-btn');
    const finalBtn = document.getElementById('add-btn');
    const controls = document.getElementById('wiz-date-picker-container');

    nextBtn.classList.toggle('hidden', step === 3);
    prevBtn.classList.toggle('hidden', step === 1);
    finalBtn.classList.toggle('hidden', step !== 3);
    controls.classList.toggle('hidden', step !== 1);

    // STICKY MOBILE FOOTER CONTROL
    const stickyFooter = document.getElementById('sticky-booking-footer');
    const stickyNextBtn = document.getElementById('sticky-next-btn');
    const stickyBookBtn = document.getElementById('sticky-book-btn');

    if (stickyFooter) {
        // Show sticky footer on mobile
        stickyFooter.classList.remove('translate-y-full');

        // Toggle buttons based on step
        if (step === 3) {
            stickyNextBtn.classList.add('hidden');
            stickyBookBtn.classList.remove('hidden');
        } else {
            stickyNextBtn.classList.remove('hidden');
            stickyBookBtn.classList.add('hidden');
        }
    }

    if (step === 3) {
        finalBtn.innerHTML = '<span>RESERVAR AHORA</span><i class="ri-shopping-cart-2-line border-l border-white/20 pl-2"></i>';
        finalBtn.className = 'w-full bg-emerald-500 text-white py-6 rounded-3xl font-black uppercase tracking-widest shadow-xl shadow-emerald-500/20 hover:bg-emerald-600 transition-all flex items-center justify-center gap-3';
        renderStep3Summary();
    }
}

function renderStep3Summary() {
    if (!activeTour) return;
    document.getElementById('review-tour-title').innerText = activeTour.title;
    document.getElementById('review-date').innerText = `${selectedDay} ${monthNames[currentLang][currentMonthIndex]}`;
    document.getElementById('review-pax').innerText = `${participants} ${currentLang === 'es' ? 'EXPLORADORES' : 'EXPLORERS'}`;
    document.getElementById('review-addons-count').innerText = `${selectedAddons.length} ${currentLang === 'es' ? 'ACTIVOS' : 'ACTIVE'}`;
}

function updateTotalPrice() {
    const basePrice = (activeTour?.price || 0) * participants;
    const addonsPrice = selectedAddons.reduce((sum, a) => sum + a.price, 0);
    const total = basePrice + addonsPrice;
    const formattedTotal = `S/ ${Math.round(total)}`;

    // Update desktop price
    document.getElementById('b-total-price').innerText = formattedTotal;

    // Update sticky mobile price
    const stickyPrice = document.getElementById('sticky-total-price');
    if (stickyPrice) stickyPrice.innerText = formattedTotal;
}

function toggleAddon(id, price, name) {
    const idx = selectedAddons.findIndex(a => a.id === id);
    if (idx > -1) selectedAddons.splice(idx, 1);
    else selectedAddons.push({ id, price, name });
    updateTotalPrice();
}

function changePax(delta) {
    participants = Math.max(1, Math.min(10, participants + delta));
    document.getElementById('pax-count').innerText = participants.toString().padStart(2, '0');
    updateTotalPrice();
}

function addToCartFinal() {
    // Construir fecha real
    const year = currentYear || 2026;
    const month = (currentMonthIndex + 1).toString().padStart(2, '0');
    const day = selectedDay.toString().padStart(2, '0');
    const fullDate = `${year}-${month}-${day}`;

    const item = {
        id: activeTour.id,
        name: activeTour.title,
        price: parseFloat(document.getElementById('b-total-price').innerText.replace('S/ ', '')),
        img: activeTour.img,
        detail: `${selectedDay} ${monthNames[currentLang][currentMonthIndex]} | ${participants} Pax | ${selectedAddons.map(a => a.name).join(', ')}`,
        date: selectedDay,
        pax: participants
    };

    // 1. Añadir a UI Mochila (Local)
    backpack.addItem(item);

    // 2. ☁️ Sincronizar con Supabase (Fire & Forget por ahora para no bloquear UI)
    if (window.processBookingCusco) {
        window.processBookingCusco({
            tourId: activeTour.id,
            date: fullDate,
            pax: participants,
            price: item.price,
            contact: {
                name: "Usuario Web", // Idealmente vendría de un form de checkout
                email: "pendiente@checkout.com"
            }
        });
    }

    closeModal();
    updateCart();

    // Toast Feedback
    const msg = currentLang === 'es' ? `${activeTour.title} añadido a la mochila` : `${activeTour.title} added to backpack`;
    showToast('Mochila Táctica', msg, 'ri-shopping-bag-3-fill');

    // FOMO Real-time Emission
    if (window.FOMOEngine) FOMOEngine.emitEvent(activeTour.title);

    // Trigger Kit Builder for High-Value Tours
    if (activeTour.price > 1800) {
        setTimeout(() => openKitBuilder(), 800);
    } else {
        toggleCart();
    }
}

// --- KIT BUILDER LOGIC (Price Anchoring) ---
let currentKit = [];

function openKitBuilder() {
    const equipsList = window.equips || [];
    currentKit = equipsList.slice(0, 3); // Featured Survival Pack

    const basePrice = currentKit.reduce((sum, e) => sum + e.price, 0);
    const pricing = PriceEngine.calculateKitDiscount(basePrice, 25); // 25% aggressive discount for anchoring

    document.getElementById('kit-original-price').innerText = PriceEngine.format(pricing.original);
    document.getElementById('kit-final-price').innerText = PriceEngine.format(pricing.discounted);
    document.getElementById('kit-savings-amount').innerText = PriceEngine.format(pricing.savings);

    document.getElementById('kit-items-preview').innerHTML = currentKit.map(e => `
        <div class="relative group">
            <img src="${e.img}?w=150" class="w-20 h-20 rounded-2xl object-cover border-2 border-slate-100 group-hover:border-primary transition-all">
            <div class="absolute -top-2 -right-2 bg-primary text-white w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-black"><i class="ri-check-line"></i></div>
        </div>
    `).join('');

    document.getElementById('kit-builder-modal').classList.remove('hidden');
    // Actualizar botones del modal para usar data-action
    const addBtn = document.querySelector('#kit-builder-modal button[onclick="addKitToCart()"]');
    if (addBtn) { addBtn.removeAttribute('onclick'); addBtn.setAttribute('data-action', 'add-kit'); }

    const closeBtn = document.querySelector('#kit-builder-modal button[onclick="closeKitBuilder()"]');
    if (closeBtn) { closeBtn.removeAttribute('onclick'); closeBtn.setAttribute('data-action', 'close-kit'); }
}

function closeKitBuilder() {
    document.getElementById('kit-builder-modal').classList.add('hidden');
    toggleCart();
}

function addKitToCart() {
    const basePrice = currentKit.reduce((sum, e) => sum + e.price, 0);
    const pricing = PriceEngine.calculateKitDiscount(basePrice, 25);

    const item = {
        id: 'kit-survival-' + Date.now(),
        name: 'Pack Supervivencia Elite',
        price: parseFloat(pricing.discounted),
        img: 'https://images.unsplash.com/photo-1510672981848-a1c4f1cb5ccf',
        detail: currentKit.map(e => e.name).join(', ')
    };

    backpack.addItem(item);
    updateCart();
    closeKitBuilder();
}

function closeModal() {
    document.getElementById('booking-modal').classList.add('hidden');

    // Hide sticky footer when modal closes
    const stickyFooter = document.getElementById('sticky-booking-footer');
    if (stickyFooter) stickyFooter.classList.add('translate-y-full');
}
function toggleCart() { document.getElementById('cart-drawer')?.classList.toggle('translate-x-full'); }

// --- BACKPACK UI SYNC ---
function updateCart() {
    const { items, total } = backpack.getState();
    const list = document.getElementById('cart-list');
    const count = document.getElementById('cart-count');
    if (count) count.innerText = items.length;

    if (!list) return;

    if (items.length === 0) {
        list.innerHTML = `<div class="py-20 text-center opacity-30"><i class="ri-ghost-line text-4xl"></i><p class="font-black italic mt-2">${translations[currentLang].backpack_empty}</p></div>`;
        document.getElementById('cart-total').innerText = "S/ 0";
        return;
    }

    list.innerHTML = items.map((item, idx) => `
        <div class="flex items-center gap-4 bg-slate-50 p-4 rounded-3xl border border-slate-100">
            <img src="${item.img}?w=100" class="w-12 h-12 rounded-xl object-cover">
            <div class="flex-1">
                <h4 class="font-black text-[10px] uppercase">${item.name}</h4>
                <p class="text-[8px] font-bold text-slate-400">${item.detail}</p>
            </div>
            <p class="font-black text-xs">S/ ${item.price}</p>
            <button data-action="remove-item" data-idx="${idx}" class="text-slate-300 hover:text-red-500"><i class="ri-delete-bin-line"></i></button>
        </div>
    `).join('');

    document.getElementById('cart-total').innerText = "S/ " + (total * 0.85).toLocaleString(); // Elite Discount
}

async function renderGuides() {
    const grid = document.getElementById('guides-grid');
    if (!grid) return;

    const guides = await CMSService.getGuides();
    grid.innerHTML = guides.map(guide => `
        <div class="bg-white rounded-[48px] overflow-hidden border border-slate-50 group hover:shadow-2xl transition-all duration-500 flex flex-col h-full">
            <div class="h-64 overflow-hidden relative bg-slate-100">
                <div class="skeleton-loader absolute inset-0"></div>
                <img src="${guide.img}?w=500" loading="lazy" class="h-full w-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700 group-hover:scale-110 img-reveal" onload="this.classList.add('loaded'); this.previousElementSibling.style.display='none';">
                <div class="absolute bottom-6 left-6 right-6 p-4 bg-white/90 backdrop-blur-md rounded-2xl shadow-sm transform translate-y-4 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-500">
                    <p class="text-[9px] font-black uppercase text-primary mb-1">${translations[currentLang].card_specialty}</p>
                    <p class="text-xs font-black italic text-slate-900">${guide.specialty}</p>
                </div>
            </div>
            <div class="p-8 flex-1 flex flex-col justify-between">
                <div>
                    <h4 class="font-black italic text-2xl text-slate-900 mb-1">${guide.name}</h4>
                    <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-6">Staff Certified UIAGM</p>
                    
                    <div class="space-y-3 mb-8">
                        ${guide.achievements.map(ach => `
                            <div class="flex items-start gap-3">
                                <i class="ri-shield-check-fill text-emerald-500 text-sm"></i>
                                <span class="text-[10px] font-bold text-slate-600 leading-tight">${ach}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="pt-6 border-t border-slate-50">
                    <p class="text-[10px] font-medium text-slate-400 italic leading-relaxed mb-6">"${guide.bio}"</p>
                    <button class="w-full py-4 border-2 border-slate-100 rounded-2xl text-[10px] font-black uppercase text-slate-500 hover:border-primary hover:text-primary transition-all tracking-widest">
                        ${translations[currentLang].card_mission_docs}
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// --- RENDER MAIN GRIDS ---
function renderAll(region = 'Todos', category = 'Todos') {
    const grid = document.getElementById('destinos-grid');
    if (!grid) return;

    const filtered = (region === 'Todos') ? tours : tours.filter(t => t.dept === region);
    grid.innerHTML = filtered.map((t, i) => `
        <div class="bg-white rounded-[40px] overflow-hidden group cursor-pointer shadow-sm hover:shadow-xl transition-all animate-card-entry relative" 
             style="animation-delay: ${i * 40}ms; animation-fill-mode: both;"
             data-action="open-booking" data-id="${t.id}">
            <!-- Share Button Overlay -->
            <div class="card-share-overlay">
                <button 
                    class="share-btn-compact" 
                    onclick="event.stopPropagation(); window.ShareEngine.shareViaWhatsApp({id: ${t.id}, title: '${t.title.replace(/'/g, "\\'")}'', dept: '${t.dept}', duration: '${t.duration}', price: ${t.price}}, 'tour');"
                    title="Invitar a un amigo">
                    <i class="ri-whatsapp-line"></i>
                </button>
            </div>
            <div class="h-64 overflow-hidden relative bg-slate-100">
                <div class="skeleton-loader absolute inset-0"></div>
                <img src="${t.img}?w=500" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition-all duration-700 img-reveal" onload="this.classList.add('loaded'); this.previousElementSibling.style.display='none';">
            </div>
            <div class="p-8">
                <div class="flex justify-between mb-2">
                    <p class="text-[9px] font-black text-primary uppercase">${t.dept}</p>
                    <div class="flex items-center gap-2">
                        <button 
                            onclick="event.stopPropagation(); window.ShareEngine.copyLinkToClipboard('tour', ${t.id});" 
                            class="text-slate-300 hover:text-primary transition-colors z-10 relative" 
                            title="Copiar link">
                            <i class="ri-link text-sm"></i>
                        </button>
                        <button data-action="toggle-wishlist" data-id="${t.id}" class="${wishlist.includes(t.id) ? 'text-secondary' : 'text-slate-200'} z-10 relative"><i class="ri-heart-pulse-fill"></i></button>
                    </div>
                </div>
                <h3 class="text-xl font-black italic mb-6">${t.title}</h3>
                <div class="flex justify-between items-center pt-6 border-t font-black">
                    <span class="text-2xl italic">S/ ${t.price}</span>
                    <i class="ri-arrow-right-line text-primary"></i>
                </div>
            </div>
        </div>
    `).join('');

    // Handle Equipment grid if it exists
    const equipGrid = document.getElementById('equip-grid');
    if (equipGrid) {
        let equipsData = window.equips || [];
        if (category !== 'Todos') {
            equipsData = equipsData.filter(e => e.cat === category);
        }

        equipGrid.innerHTML = equipsData.map((e, i) => `
            <div class="bg-white p-8 rounded-[40px] border border-slate-50 flex items-center gap-8 shadow-sm hover:shadow-xl transition-all animate-card-entry" style="animation-delay: ${i * 40}ms; animation-fill-mode: both;">
                <div class="w-24 h-24 rounded-2xl relative bg-slate-50 overflow-hidden">
                    <div class="skeleton-loader absolute inset-0"></div>
                    <img src="${e.img}?w=200" loading="lazy" class="w-full h-full object-cover img-reveal" onload="this.classList.add('loaded'); this.previousElementSibling.style.display='none';">
                </div>
                <div class="flex-1">
                    <p class="text-[8px] font-black text-slate-400 uppercase tracking-widest mb-1">${e.cat}</p>
                    <h4 class="font-black italic text-md mb-2 leading-tight">${e.name}</h4>
                    <p class="text-xl font-black text-primary italic">S/ ${e.price}</p>
                </div>
                <button data-action="add-cart-short" data-name="${e.name}" data-price="${e.price}" data-img="${e.img}" class="bg-slate-900 text-white w-12 h-12 rounded-xl flex items-center justify-center hover:bg-primary transition-all shadow-lg"><i class="ri-add-line text-xl"></i></button>
            </div>
        `).join('');
    }

    renderGuides();
    renderEvents();
}

function renderEvents(region = 'Todos') {
    const grid = document.getElementById('events-grid');
    if (!grid) return;

    const filtered = (region === 'Todos') ? events : events.filter(e => e.dept === region);

    if (filtered.length === 0) {
        grid.innerHTML = `<div class="col-span-full py-20 text-center opacity-40"><i class="ri-calendar-event-line text-5xl mb-4 block"></i><p class="font-black italic">${translations[currentLang].status_no_events}</p></div>`;
        return;
    }

    grid.innerHTML = filtered.map(e => `
        <div class="bg-white rounded-[48px] overflow-hidden group shadow-sm hover:shadow-2xl transition-all duration-500 border border-slate-50 flex flex-col h-full relative" data-action="open-booking" data-id="${e.id}">
            <!-- Share Button Overlay -->
            <div class="card-share-overlay">
                <button 
                    class="share-btn-compact" 
                    onclick="event.stopPropagation(); window.ShareEngine.shareViaWhatsApp({id: ${e.id}, title: '${e.title.replace(/'/g, "\\'")}'', dept: '${e.dept}', date: '${e.date} ${e.month}', price: ${e.price}}, 'event');"
                    title="Invitar a un amigo">
                    <i class="ri-whatsapp-line"></i>
                </button>
            </div>
            <div class="h-64 overflow-hidden relative bg-slate-100">
                <div class="skeleton-loader absolute inset-0"></div>
                <img src="${e.img}?w=500" loading="lazy" class="h-full w-full object-cover group-hover:scale-110 transition-all duration-700 img-reveal" onload="this.classList.add('loaded'); this.previousElementSibling.style.display='none';">
                <div class="absolute top-6 left-6 bg-white/90 backdrop-blur-md px-4 py-3 rounded-2xl shadow-sm text-center min-w-[60px]">
                    <p class="text-xs font-black text-primary leading-none">${e.date}</p>
                    <p class="text-[8px] font-black text-slate-400 uppercase tracking-widest mt-1">${e.month}</p>
                </div>
                <div class="absolute bottom-6 right-6 bg-primary/90 backdrop-blur-md px-4 py-2 rounded-xl text-white text-[9px] font-black uppercase tracking-widest shadow-lg">
                    ${e.cat}
                </div>
            </div>
            <div class="p-10 flex-1 flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-start mb-3">
                        <p class="text-[9px] font-black text-primary uppercase tracking-[0.3em]">${e.dept}</p>
                        <button 
                            onclick="event.stopPropagation(); window.ShareEngine.copyLinkToClipboard('event', ${e.id});" 
                            class="text-slate-300 hover:text-primary transition-colors" 
                            title="Copiar link">
                            <i class="ri-link text-sm"></i>
                        </button>
                    </div>
                    <h4 class="text-2xl font-black italic text-slate-900 mb-4 leading-tight">${e.title}</h4>
                    <p class="text-xs font-bold text-slate-500 mb-8">${e.detail}</p>
                    
                    <div class="flex flex-wrap gap-2 mb-8">
                        ${e.whatYouDo.map(tag => `<span class="bg-slate-50 text-slate-400 px-3 py-1.5 rounded-lg text-[8px] font-black uppercase tracking-wider border border-slate-100">${tag}</span>`).join('')}
                    </div>
                </div>
                
                <div class="flex items-center justify-between pt-8 border-t border-slate-50">
                    <div>
                        <p class="text-[8px] font-black text-slate-400 uppercase tracking-widest mb-1">${translations[currentLang].card_inscription}</p>
                        <p class="text-2xl font-black italic text-slate-900">S/ ${e.price}</p>
                    </div>
                    <button class="w-12 h-12 bg-slate-50 rounded-2xl flex items-center justify-center text-primary hover:bg-primary hover:text-white transition-all shadow-sm">
                        <i class="ri-arrow-right-up-line text-xl"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// --- EVENT DELEGATION SYSTEM (CORE UPDATE) ---
function setupEventListeners() {
    // Click Handler Central
    document.body.addEventListener('click', (e) => {
        const target = e.target.closest('[data-action]');
        if (!target) return;

        // Evitar comportamiento default si es un link vacio
        if (target.tagName === 'A' && target.getAttribute('href') === '#') e.preventDefault();

        const action = target.dataset.action;
        const data = target.dataset;

        // Router de Acciones
        switch (action) {
            case 'navigate': navigateTo(data.target); break;
            case 'mobile-navigate': mobileNavigate(data.target); break;
            case 'set-lang': setLanguage(data.lang); break;
            case 'toggle-cart': toggleCart(); break;
            case 'toggle-mobile-menu': toggleMobileMenu(); break;

            // Booking & Modals
            case 'open-booking': openBooking(parseInt(data.id)); break;
            case 'close-modal': closeModal(); break;
            case 'next-step': nextBookingStep(); break;
            case 'prev-step': prevBookingStep(); break;
            case 'add-booking-cart': addToCartFinal(); break;
            case 'change-pax': changePax(parseInt(data.delta)); break;

            // Cart & Store
            case 'toggle-wishlist': toggleWishlist(parseInt(data.id)); break;
            case 'add-cart-short': addToCartShort(data.name, parseFloat(data.price), data.img); break;
            case 'remove-item': backpack.removeItem(parseInt(data.idx)); updateCart(); break;
            case 'add-kit': addKitToCart(); break;
            case 'close-kit': closeKitBuilder(); break;

            // Features
            case 'open-quiz': openQuiz(); break;
            case 'close-quiz': closeQuiz(); break;
            case 'quiz-next': nextQuizStep(parseInt(data.step), data.val); break;
            case 'quiz-finish': finishQuiz(); break;
            case 'activate-membership': openAIPersonalizationModal(); break;
            case 'close-ai-modal': closeAIPersonalizationModal(); break;
            case 'send-chat': sendCompactChat(data.msg); break;
            case 'send-chat-input': sendCompactChatFromInput(); break;

            // Share Actions
            case 'share-whatsapp':
                if (window.ShareEngine) {
                    const activityData = JSON.parse(data.activity || '{}');
                    window.ShareEngine.shareViaWhatsApp(activityData, data.type);
                }
                break;
            case 'copy-link':
                if (window.ShareEngine) {
                    window.ShareEngine.copyLinkToClipboard(data.type, parseInt(data.id));
                }
                break;

            // Filters
            case 'sel-region': selRegion(data.region); break;
            case 'sel-event-region': selEventRegion(data.region); break;
            case 'filter-equip':
                // Actualizar UI de radio buttons si es necesario
                const radio = target.querySelector('input[type="radio"]');
                if (radio) radio.checked = true;
                renderAll('Todos', data.category);
                break;

            // Payment
            case 'open-checkout': openStripeCheckout(); break;
            case 'close-checkout': closeStripeCheckout(); break;
            case 'switch-payment': switchPaymentMethod(data.method); break;
            case 'confirm-payment': confirmManualPayment(); break;
            case 'continue-exploring': toggleCart(); break;
        }
    });

    // Change Handler (Inputs/Selects)
    document.body.addEventListener('change', (e) => {
        const target = e.target.closest('[data-action]');
        if (!target) return;

        const action = target.dataset.action;
        const data = target.dataset;

        if (action === 'toggle-addon') {
            toggleAddon(data.id, parseInt(data.price), data.name);
        }
    });

    // Input Handler (Search Live)
    document.body.addEventListener('input', (e) => {
        const target = e.target.closest('[data-action="search-live"]');
        if (target) {
            handleLiveSearch(target.value);
        }
    });
}

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    updateLanguageUI();
    setupEventListeners(); // NEW: Hook up global event delegation
    renderAll();
    updateCart();
    if (window.FOMOEngine) FOMOEngine.init();
    if (window.SensoryEngine) SensoryEngine.init();
    // Urgency Loop
    setInterval(() => {
        const remaining = membership.getRemainingTime();
        const lost = membership.calculateLostSavings();
        const hours = Math.floor(remaining / 3600000);
        const mins = Math.floor((remaining % 3600000) / 60000);
        const secs = Math.floor((remaining % 60000) / 1000);

        const hEl = document.getElementById('m-hours');
        const mEl = document.getElementById('m-minutes');
        const sEl = document.getElementById('m-seconds');
        if (hEl) hEl.innerText = hours.toString().padStart(2, '0');
        if (mEl) mEl.innerText = mins.toString().padStart(2, '0');
        if (sEl) sEl.innerText = secs.toString().padStart(2, '0');

        const savingsEl = document.getElementById('lost-savings-amount');
        if (savingsEl) savingsEl.innerText = `S/ ${lost}`;
    }, 1000);
});

// --- MISSING SYSTEM FUNCTIONS ---
// --- MISSING SYSTEM FUNCTIONS ---
function selRegion(region) {
    document.querySelectorAll('#region-selector .region-chip').forEach(c => {
        c.classList.toggle('active', c.innerText === region);
    });

    // Smooth container exit sequence
    const grid = document.getElementById('destinos-grid');
    if (grid) {
        grid.classList.add('grid-transition-fade', 'grid-hidden');
        setTimeout(() => {
            renderAll(region);
            grid.classList.remove('grid-hidden');
        }, 200);
    } else {
        renderAll(region);
    }
}

function selEventRegion(region) {
    document.querySelectorAll('#event-region-selector .region-chip').forEach(c => {
        c.classList.toggle('active', c.innerText === region);
    });

    // Smooth container exit sequence for events
    const grid = document.getElementById('events-grid');
    if (grid) {
        grid.classList.add('grid-transition-fade', 'grid-hidden');
        setTimeout(() => {
            renderEvents(region);
            grid.classList.remove('grid-hidden');
        }, 200);
    } else {
        renderEvents(region);
    }
}

function activateMembership() {
    membership.initMembership();
    // Animación visual de confirmación
    const btn = document.querySelector('button[onclick="activateMembership()"]');
    if (btn) {
        btn.innerHTML = 'ESTATUS ELITE ACTIVADO <i class="ri-checkbox-circle-fill ml-2"></i>';
        btn.className = 'bg-emerald-500 text-white px-12 py-6 rounded-3xl font-black uppercase text-[13px] tracking-widest shadow-2xl transition-all';
    }
}

function addToCartShort(name, price, img) {
    backpack.addItem({
        id: 'eq-' + Date.now(),
        name: name,
        price: price,
        img: img,
        detail: 'Accesorios Pro'
    });
    updateCart();

    // Toast Feedback
    const msg = currentLang === 'es' ? `${name} añadido a la mochila` : `${name} added to backpack`;
    showToast('Equipo Añadido', msg, 'ri-check-double-line');

    // Optional: open cart or just notify? Let's just notify for smooth flow
    // toggleCart(); 
}

// --- QUIZ LOGIC ---
function openQuiz() { document.getElementById('quiz-modal').classList.remove('hidden'); }
function closeQuiz() { document.getElementById('quiz-modal').classList.add('hidden'); }

function nextQuizStep(step, value) {
    document.querySelectorAll('.quiz-step').forEach(s => s.classList.add('hidden'));
    document.getElementById(`quiz-step-${step}`).classList.remove('hidden');
    console.log(`Quiz Progress: Step ${step - 1} = ${value}`);
}

function finishQuiz() {
    const email = document.getElementById('quiz-email').value;
    if (!email) return alert('Ingresa tu email para recibir el cupón.');

    const resultTour = tours[Math.floor(Math.random() * tours.length)];
    document.getElementById('recommended-tour').innerText = resultTour.title;

    document.querySelectorAll('.quiz-step').forEach(s => s.classList.add('hidden'));
    document.getElementById('quiz-step-result').classList.remove('hidden');
}

// SPA Navigation
function navigateTo(id) {
    document.querySelectorAll('.section-view').forEach(s => s.classList.remove('active'));
    document.getElementById('section-' + id)?.classList.add('active');
    if (id === 'socio') { updateWishlistDashboard(); }
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// --- MOBILE MENU LOGIC ---
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('translate-x-full');
}

function mobileNavigate(id) {
    toggleMobileMenu();
    navigateTo(id);
}

// --- TOAST NOTIFICATION SYSTEM ---
function showToast(title, message, icon = 'ri-check-line') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container); // Append to body, not inside a section
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
        <div class="toast-icon"><i class="${icon}"></i></div>
        <div class="toast-content">
            <h4>${title}</h4>
            <p>${message}</p>
        </div>
    `;

    container.appendChild(toast);

    // Auto remove
    setTimeout(() => {
        toast.classList.add('toast-hide');
        setTimeout(() => toast.remove(), 400); // Wait for CSS transition
    }, 3000);
}

// --- LANGUAGE LOGIC ---
function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('lifextreme_lang', lang);
    updateLanguageUI();
    renderAll(); // Re-render to update dynamic labels if any
    updateCart();

    // Toast Feedback
    const msg = lang === 'es' ? 'Idioma cambiado a Español' : 'Language switched to English';
    showToast('Success', msg, 'ri-translate-2');
}

function updateLanguageUI() {
    // Update active button state
    document.getElementById('lang-es').classList.toggle('bg-white', currentLang === 'es');
    document.getElementById('lang-es').classList.toggle('shadow-sm', currentLang === 'es');
    document.getElementById('lang-en').classList.toggle('bg-white', currentLang === 'en');
    document.getElementById('lang-en').classList.toggle('shadow-sm', currentLang === 'en');
    // Update static elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[currentLang][key]) {
            el.innerText = translations[currentLang][key];
        }
    });

    // Update section titles (they don't have data-i18n in current HTML, let's fix that)
    const titles = {
        'destinos': translations[currentLang].section_destinos,
        'eventos': translations[currentLang].section_eventos,
        'equipos': translations[currentLang].section_equipos,
        'guias': translations[currentLang].section_guias
    };

    // This is a bit manual, ideally add data-i18n to titles in HTML too.
}
// --- COMPACT CHAT LOGIC ---
function sendCompactChat(msg) {
    const container = document.getElementById('compact-messages');
    if (!container) return;

    // User message
    container.innerHTML += `
        <div class="flex gap-3 items-start justify-end">
            <div class="bg-primary text-white rounded-2xl p-4 shadow-sm border border-primary/20 max-w-[80%]">
                <p class="text-xs font-semibold">${msg}</p>
            </div>
            <div class="w-8 h-8 bg-slate-100 rounded-xl flex items-center justify-center text-slate-400 flex-shrink-0">
                <i class="ri-user-smile-line text-sm"></i>
            </div>
        </div>
    `;

    container.scrollTop = container.scrollHeight;

    // AI thinking
    const thinkingId = 'thinking-' + Date.now();
    setTimeout(() => {
        container.innerHTML += `
            <div id="${thinkingId}" class="flex gap-3 items-start">
                <div class="w-8 h-8 bg-black rounded-xl flex items-center justify-center text-white flex-shrink-0">
                    <i class="ri-sparkling-fill text-sm"></i>
                </div>
                <div class="flex-1 bg-white rounded-2xl p-4 shadow-sm border border-slate-100 italic text-slate-400 text-[10px]">
                    ${translations[currentLang].msg_scanning}
                </div>
            </div>
        `;
        container.scrollTop = container.scrollHeight;

        // AI Response Logic
        setTimeout(() => {
            const el = document.getElementById(thinkingId);
            if (el) el.remove();

            let responseText = "";
            let recommendedTour = null;

            const input = msg.toLowerCase();
            if (input.includes('montaña') || input.includes('trekking')) {
                recommendedTour = tours.find(t => t.difficulty === 'Alta' || t.difficulty === 'Extrema');
                responseText = "Para un perfil táctico como el tuyo, recomiendo una ruta de alta exigencia. Mira esta opción:";
            } else if (input.includes('selva')) {
                recommendedTour = tours.find(t => t.dept === 'Iquitos' || t.title.toLowerCase().includes('selva'));
                responseText = "La selva requiere equipo especializado y guías certificados. Esta es nuestra mejor expedición actual:";
            } else if (input.includes('equipo')) {
                responseText = "Nuestra mochila táctica tiene un 15% de descuento para socios Elite. ¿Deseas ver el catálogo?";
                responseText += `<br><button onclick="navigateTo('equipos')" class="mt-3 bg-slate-900 text-white px-4 py-2 rounded-xl text-[9px] font-black uppercase">Ver Catálogo Pro</button>`;
            } else if (input.includes('sorpréndeme') || input.includes('sorpresa')) {
                recommendedTour = tours[Math.floor(Math.random() * tours.length)];
                responseText = "Basado en las tendencias de la comunidad Lifextreme, esta es la aventura del momento:";
            } else {
                responseText = "Entendido. Busco aventuras que desafíen tus límites. ¿Prefieres alta montaña, selva densa o equipo técnico?";
            }

            let htmlResponse = `
                <div class="flex gap-3 items-start">
                    <div class="w-8 h-8 bg-black rounded-xl flex items-center justify-center text-white flex-shrink-0">
                        <i class="ri-sparkling-fill text-sm"></i>
                    </div>
                    <div class="flex-1 space-y-3">
                        <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-100">
                            <p class="text-slate-800 text-xs font-semibold">${responseText}</p>
                        </div>
            `;

            if (recommendedTour) {
                htmlResponse += `
                    <div class="bg-white rounded-3xl overflow-hidden shadow-xl border border-slate-100 group cursor-pointer" onclick="openBooking(${recommendedTour.id})">
                        <div class="h-32 overflow-hidden relative">
                            <img src="${recommendedTour.img}?w=400" class="w-full h-full object-cover">
                            <div class="absolute top-2 right-2 bg-primary text-white text-[8px] font-black px-2 py-1 rounded-lg uppercase italic">Recomendado</div>
                        </div>
                        <div class="p-4">
                            <p class="text-[8px] font-black text-primary uppercase mb-1">${recommendedTour.dept}</p>
                            <h5 class="text-sm font-black italic mb-2">${recommendedTour.title}</h5>
                            <div class="flex justify-between items-center border-t pt-3">
                                <span class="text-xs font-black">S/ ${recommendedTour.price}</span>
                                <i class="ri-arrow-right-line text-primary"></i>
                            </div>
                        </div>
                    </div>
                `;
            }

            htmlResponse += `</div></div>`;
            container.innerHTML += htmlResponse;
            container.scrollTop = container.scrollHeight;
        }, 1500);
    }, 400);
}

function sendCompactChatFromInput() {
    const input = document.getElementById('compact-input');
    if (input && input.value.trim()) {
        sendCompactChat(input.value);
        input.value = '';
    }
}

// --- STRIPE MOCKUP & PAYMENT ---
function openStripeCheckout() {
    const { items, total } = backpack.getState();
    if (items.length === 0) return alert('Tu mochila está vacía.');

    const orderItems = document.getElementById('stripe-order-items');
    orderItems.innerHTML = items.map(item => `
        <div class="flex justify-between items-center text-xs border-b border-slate-50 pb-4">
            <span class="font-bold">${item.name}</span>
            <span class="font-black italic">S/ ${item.price}</span>
        </div>
    `).join('');

    const finalTotal = Math.round(total * 0.85); // Applying Elite Discount
    document.getElementById('stripe-total-amount').innerText = `S/ ${finalTotal}`;

    // Initialize default view
    switchPaymentMethod('qr');

    // Initialize payment plan system
    initializePaymentPlan(finalTotal);

    document.getElementById('stripe-checkout-modal').classList.remove('hidden');
}

// --- PAYMENT PLAN SYSTEM (ELITE MEMBERS) ---
let currentPaymentPlan = 'full'; // 'full' or 'split'
let selectedTourDate = null; // Will be set from booking

function initializePaymentPlan(totalAmount) {
    // Get the selected tour date from booking state
    const bookingDateElement = document.getElementById('review-date');
    if (bookingDateElement && bookingDateElement.innerText) {
        selectedTourDate = parseTourDate(bookingDateElement.innerText);
    } else {
        // Default to 30 days from now if no date selected
        selectedTourDate = new Date();
        selectedTourDate.setDate(selectedTourDate.getDate() + 30);
    }

    // Calculate payment dates
    const today = new Date();
    const oneDayBefore = new Date(selectedTourDate);
    oneDayBefore.setDate(oneDayBefore.getDate() - 1);
    const tourDay = new Date(selectedTourDate);

    // Calculate amounts (30%-30%-40%)
    const payment1 = Math.round(totalAmount * 0.30);
    const payment2 = Math.round(totalAmount * 0.30);
    const payment3 = totalAmount - payment1 - payment2; // Remaining to ensure exact total

    // Update UI with dates and amounts
    document.getElementById('payment-date-1').innerText = formatDate(today);
    document.getElementById('payment-date-2').innerText = formatDate(oneDayBefore);
    document.getElementById('payment-date-3').innerText = formatDate(tourDay);

    document.getElementById('payment-amount-1').innerText = `S/ ${payment1}`;
    document.getElementById('payment-amount-2').innerText = `S/ ${payment2}`;
    document.getElementById('payment-amount-3').innerText = `S/ ${payment3}`;

    // Set current payment amount (default to full)
    document.getElementById('current-payment-amount').innerText = `S/ ${totalAmount}`;

    // Setup payment plan toggle listeners
    setupPaymentPlanListeners(totalAmount, payment1);
}

function setupPaymentPlanListeners(totalAmount, firstPayment) {
    const btnFull = document.getElementById('payment-plan-full');
    const btnSplit = document.getElementById('payment-plan-split');
    const splitDetails = document.getElementById('split-payment-details');
    const currentPaymentDisplay = document.getElementById('current-payment-amount');

    // Remove existing listeners
    const newBtnFull = btnFull.cloneNode(true);
    const newBtnSplit = btnSplit.cloneNode(true);
    btnFull.parentNode.replaceChild(newBtnFull, btnFull);
    btnSplit.parentNode.replaceChild(newBtnSplit, btnSplit);

    // Add new listeners
    newBtnFull.addEventListener('click', () => {
        currentPaymentPlan = 'full';

        // Update button states
        newBtnFull.classList.add('bg-primary', 'text-white');
        newBtnFull.classList.remove('text-slate-400');
        newBtnSplit.classList.remove('bg-primary', 'text-white');
        newBtnSplit.classList.add('text-slate-400');

        // Hide split details
        splitDetails.classList.add('hidden');

        // Update current payment amount
        currentPaymentDisplay.innerText = `S/ ${totalAmount}`;
    });

    newBtnSplit.addEventListener('click', () => {
        currentPaymentPlan = 'split';

        // Update button states
        newBtnSplit.classList.add('bg-primary', 'text-white');
        newBtnSplit.classList.remove('text-slate-400');
        newBtnFull.classList.remove('bg-primary', 'text-white');
        newBtnFull.classList.add('text-slate-400');

        // Show split details
        splitDetails.classList.remove('hidden');

        // Update current payment amount (first installment)
        currentPaymentDisplay.innerText = `S/ ${firstPayment}`;

        // Add animation
        splitDetails.style.opacity = '0';
        splitDetails.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            splitDetails.style.transition = 'all 0.3s ease';
            splitDetails.style.opacity = '1';
            splitDetails.style.transform = 'translateY(0)';
        }, 10);
    });
}

function parseTourDate(dateString) {
    // Parse date from format like "10 Mar 2026"
    const months = {
        'Ene': 0, 'Feb': 1, 'Mar': 2, 'Abr': 3, 'May': 4, 'Jun': 5,
        'Jul': 6, 'Ago': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dic': 11
    };

    const parts = dateString.split(' ');
    if (parts.length === 3) {
        const day = parseInt(parts[0]);
        const month = months[parts[1]];
        const year = parseInt(parts[2]);
        return new Date(year, month, day);
    }

    // Default to 30 days from now
    const defaultDate = new Date();
    defaultDate.setDate(defaultDate.getDate() + 30);
    return defaultDate;
}

function formatDate(date) {
    const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    const day = date.getDate().toString().padStart(2, '0');
    const month = months[date.getMonth()];
    const year = date.getFullYear();
    return `${day} ${month} ${year}`;
}

function closeStripeCheckout() {
    document.getElementById('stripe-checkout-modal').classList.add('hidden');
}

// --- MANUAL PAYMENT LOGIC ---
function switchPaymentMethod(method) {
    const qrView = document.getElementById('view-pay-qr');
    const bankView = document.getElementById('view-pay-bank');
    const btnQr = document.getElementById('btn-pay-qr');
    const btnBank = document.getElementById('btn-pay-bank');

    if (method === 'qr') {
        qrView.classList.remove('hidden');
        bankView.classList.add('hidden');

        btnQr.classList.add('border-primary', 'text-primary', 'shadow-md');
        btnQr.classList.remove('border-transparent', 'text-slate-400');

        btnBank.classList.add('border-transparent', 'text-slate-400');
        btnBank.classList.remove('border-primary', 'text-primary', 'shadow-md');
    } else {
        qrView.classList.add('hidden');
        bankView.classList.remove('hidden');

        btnBank.classList.add('border-primary', 'text-primary', 'shadow-md');
        btnBank.classList.remove('border-transparent', 'text-slate-400');

        btnQr.classList.add('border-transparent', 'text-slate-400');
        btnQr.classList.remove('border-primary', 'text-primary', 'shadow-md');
    }
}

function confirmManualPayment() {
    const btn = document.getElementById('confirm-payment-btn');
    btn.disabled = true;
    btn.innerHTML = '<i class="ri-loader-4-line animate-spin text-xl"></i> Validando...';

    setTimeout(() => {
        btn.innerHTML = '<i class="ri-checkbox-circle-fill text-xl"></i> PAGO REGISTRADO';

        // Different messages based on payment plan
        if (currentPaymentPlan === 'split') {
            showToast('Primer Pago Confirmado', 'Recibirás recordatorios para los siguientes pagos', 'ri-verified-badge-fill');

            // Save payment plan info to localStorage for future reference
            const paymentInfo = {
                plan: 'split',
                firstPaymentDate: new Date().toISOString(),
                tourDate: selectedTourDate ? selectedTourDate.toISOString() : null,
                items: backpack.getState().items
            };
            localStorage.setItem('lifextreme_payment_plan', JSON.stringify(paymentInfo));
        } else {
            showToast('Pago Exitoso', 'Tu expedición está confirmada', 'ri-verified-badge-fill');
        }

        setTimeout(() => {
            closeStripeCheckout();
            backpack.setState(state => ({ ...state, items: [], total: 0 }));
            localStorage.removeItem('lifextreme_backpack');
            updateCart();
            navigateTo('home');

            // Reset button state for next time
            btn.disabled = false;
            btn.innerHTML = 'Confirmar Pago Enviado';

            // Reset payment plan to default
            currentPaymentPlan = 'full';
        }, 1500);
    }, 2000);
}

// --- LIVE SEARCH SYSTEM ---
function handleLiveSearch(query) {
    const dropdown = document.getElementById('search-results-dropdown');
    if (!query) {
        dropdown.classList.add('hidden', 'opacity-0', 'translate-y-2');
        return;
    }

    const term = query.toLowerCase();

    // Search in Tours
    const matchedTours = tours.filter(t =>
        t.title.toLowerCase().includes(term) ||
        t.dept.toLowerCase().includes(term) ||
        (t.difficulty && t.difficulty.toLowerCase().includes(term))
    ).slice(0, 3);

    // Search in Events (Optional)
    const matchedEvents = (window.events || []).filter(e =>
        e.title.toLowerCase().includes(term) ||
        e.cat.toLowerCase().includes(term)
    ).slice(0, 2);

    const hasResults = matchedTours.length > 0 || matchedEvents.length > 0;

    if (!hasResults) {
        dropdown.innerHTML = `
            <div class="p-6 text-center text-slate-400">
                <i class="ri-ghost-line text-2xl mb-2"></i>
                <p class="text-[10px] font-bold">Sin resultados tácticos</p>
            </div>
        `;
    } else {
        let html = '';

        if (matchedTours.length > 0) {
            html += `<div class="p-4"><p class="text-[9px] font-black uppercase text-slate-400 mb-2 pl-2">Expediciones</p>`;
            html += matchedTours.map(t => `
                <div class="flex items-center gap-3 p-2 hover:bg-slate-50 rounded-xl cursor-pointer transition-colors" onclick="openBooking(${t.id}); document.getElementById('search-results-dropdown').classList.add('hidden')">
                    <img src="${t.img}?w=80" class="w-10 h-10 rounded-lg object-cover">
                    <div class="flex-1">
                        <p class="text-[10px] font-black text-slate-800 leading-tight">${t.title}</p>
                        <p class="text-[8px] font-bold text-slate-400 uppercase">${t.dept}</p>
                    </div>
                    <span class="text-[10px] font-black text-primary">S/ ${t.price}</span>
                </div>
            `).join('');
            html += `</div>`;
        }

        if (matchedEvents.length > 0) {
            html += `<div class="bg-slate-50 p-4 border-t border-slate-100"><p class="text-[9px] font-black uppercase text-slate-400 mb-2 pl-2">Eventos</p>`;
            html += matchedEvents.map(e => `
                <div class="flex items-center gap-3 p-2 hover:bg-white rounded-xl cursor-pointer transition-colors" onclick="openBooking(${e.id}); document.getElementById('search-results-dropdown').classList.add('hidden')">
                    <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center text-accent shadow-sm border border-slate-100 font-black text-xs">
                        ${e.date.split(' ')[0]}
                    </div>
                    <div class="flex-1">
                        <p class="text-[10px] font-black text-slate-800 leading-tight">${e.title}</p>
                        <p class="text-[8px] font-bold text-slate-400 uppercase">${e.cat}</p>
                    </div>
                </div>
            `).join('');
            html += `</div>`;
        }

        dropdown.innerHTML = html;
    }

    dropdown.classList.remove('hidden');
    // Small delay to allow display block to apply before opacity transition
    requestAnimationFrame(() => {
        dropdown.classList.remove('opacity-0', 'translate-y-2');
    });
}
