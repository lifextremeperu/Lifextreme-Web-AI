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
    { id: 2, title: 'Salkantay Trek a Machu Picchu 4D', dept: 'Cusco', img: 'https://images.unsplash.com/photo-1590520611221-998bd104f6ed', ratings: null },
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
        hero_tag: "🔥 LA TRIBU MÁS EXTREMA DEL PERÚ • GUÍAS UIAGM • +15,000 EXPEDICIONARIOS",
        hero_title_1: "EXPLORA, VIVE,",
        hero_title_2: "VIAJA.",
        hero_desc: "¿Hasta cuándo vas a mirar la adrenalina desde una pantalla? Sal de la rutina, siente la gravedad cero y desafía tus límites con la tribu de aventureros más activa del país. 40 expediciones verificadas, 164 parques auditados y guías certificados UIAGM. Cero improvisación, 100% adrenalina pura.",
        btn_explore: "Explorar Destinos",
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
        hero_tag: "🔥 PERU'S MOST EXTREME TRIBE • UIAGM GUIDES • +15,000 EXPLORERS",
        hero_title_1: "EXPLORE, LIVE,",
        hero_title_2: "TRAVEL.",
        hero_desc: "How much longer will you watch adrenaline through a screen? Break the routine, feel zero gravity, and conquer the Andes with Peru's premier adventure tribe. 40 verified expeditions, 164 audited parks, and certified UIAGM guides. 0% guesswork, 100% pure adrenaline.",
        btn_explore: "Explore Destinations",
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
    },
    pt: {
        nav_home: "Início",
        nav_destinos: "Destinos",
        nav_eventos: "Eventos",
        nav_equipos: "Equipamentos",
        nav_guias: "Guias",
        user_status: "Sócio Elite Ativo",
        hero_tag: "🔥 A TRIBO MAIS EXTREMA DO PERU • GUIAS UIAGM • +15,000 AVENTUREIROS",
        hero_title_1: "EXPLORE, VIVA,",
        hero_title_2: "VIAJE.",
        hero_desc: "Até quando você vai assistir à adrenalina por uma tela? Saia da rotina, sinta a gravidade zero e conquiste os Andes com a maior tribo de aventura do Peru. 40 expedições verificadas, 164 parques auditados e guias certificados UIAGM. Zero improviso, 100% adrenalina pura.",
        btn_explore: "Explorar Mapa",
        btn_events: "Ver Eventos",
        quiz_prompt: "Não sabe o que escolher?",
        quiz_desc: "Faça o Teste de Aventura e ganhe -10%",
        membership_alert: "⚠️ ALERTA DE EXPIRAÇÃO",
        membership_title_1: "Seu acesso",
        membership_title_2: "Elite",
        membership_title_3: "expira em breve",
        membership_desc_1: "Você está prestes a perder um desconto de",
        membership_desc_2: "na sua mochila tática. Ative agora para garantir seus benefícios.",
        timer_hours: "Horas",
        timer_min: "Min",
        timer_sec: "Seg",
        btn_secure_discount: "Garantir meu Desconto",
        membership_action_required: "Ação necessária para manter o status",
        backpack_title: "MOCHILA TÁTICA",
        backpack_tag: "Pronta para a ação",
        backpack_empty: "Mochila Vazia",
        backpack_total: "Investimento em Aventura",
        btn_continue_exploring: "Continuar Explorando",
        btn_checkout: "PAGAR AGORA",
        section_destinos: "Exploração Nacional",
        section_eventos: "Competições & Festivais",
        section_equipos: "Catálogo Pro",
        section_guias: "Staff de Guias Elite",
        modal_duration: "Duração",
        modal_guide: "Guia",
        modal_cancel: "Cancelamento",
        modal_itinerary: "Itinerário Tático",
        modal_gear: "Equipamento Sugerido",
        modal_addons: "Serviços Adicionais",
        modal_summary: "Resumo",
        modal_date: "Selecionar Data",
        modal_pax: "Participantes",
        btn_next: "Próximo Passo",
        btn_prev: "Passo Anterior",
        btn_book: "RESERVAR AGORA",
        status_no_events: "Sem eventos para esta região em 2026",
        events_official_calendar: "Calendário Oficial 2026",
        equip_sidebar_backpacks: "Mochilas",
        equip_sidebar_footwear: "Calçados",
        equip_sidebar_accessories: "Acessórios",
        equip_sidebar_all: "Ver Tudo",
        backpack_investment: "Investimento em Aventura",
        backpack_member_discount: "-15% Desconto",
        backpack_protection: "Seus objetos estão protegidos.",
        footer_rights: "© 2026 Lifextreme Pro System. Todos os Direitos Reservados.",
        wizard_step_1: "Configurar",
        wizard_step_2: "Equipamento",
        wizard_step_3: "Pagamento",
        quiz_q1: "Qual é o seu nível de loucura?",
        quiz_a1_1: "Iniciante",
        quiz_a1_2: "Elite Pro",
        quiz_q2: "Qual é o seu terreno?",
        quiz_a2_1: "🏔️ Montanha",
        quiz_a2_2: "🌴 Selva",
        card_inscription: "Inscrição",
        card_specialty: "Especialidade",
        card_mission_docs: "Docs Missão",
        card_suggestion: "Equip. Sugerido",
        card_add: "Adicionar",
        msg_scanning: "Analisando dados táticos...",
        msg_analyzing: "Lifextreme AI está analisando o seu perfil..."
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

    // Trigger Prediction
    updatePredictionWidget(d);
}

async function updatePredictionWidget(day) {
    const widget = document.getElementById('prediction-widget');
    if (!widget) return;

    // Show loading state
    widget.classList.remove('hidden');
    widget.innerHTML = `<div class="flex items-center gap-3 text-slate-400"><i class="ri-loader-4-line animate-spin"></i> <span class="text-xs font-bold">Analizando condiciones satelitales...</span></div>`;

    // 1. Get Demand Prediction (Instant)
    const demand = PredictorEngine.getDemandPrediction(currentMonthIndex);

    // 2. Get Weather Forecast (Async) - Cusco Coordinates default
    // In a real app, use activeTour.lat/lon
    const weather = await PredictorEngine.getWeatherForecast(-13.5319, -71.9675, null);

    // Render Widget
    widget.innerHTML = `
        <div class="flex items-start gap-4">
            <div class="bg-white p-3 rounded-xl shadow-sm text-center min-w-[60px]">
                <i class="${weather.icon} text-2xl text-slate-700 mb-1 block"></i>
                <span class="text-[10px] font-black block">${weather.temp}°C</span>
            </div>
            <div class="flex-1">
                <div class="flex justify-between items-start mb-1">
                    <h6 class="text-[10px] font-black uppercase text-slate-500 tracking-widest">Pronóstico de Misión</h6>
                    ${demand.scarcity ? `<span class="bg-red-100 text-red-600 px-2 py-0.5 rounded text-[9px] font-bold animate-pulse">🔥 Alta Demanda</span>` : ''}
                </div>
                <p class="text-xs font-bold text-slate-800 leading-tight mb-2">"${weather.desc}. ${weather.advice}"</p>
                
                <div class="flex gap-2 text-[9px] font-bold text-slate-500 bg-white/50 p-2 rounded-lg">
                    <i class="ri-radar-line"></i>
                    <span>Riesgo Clima: <b class="${weather.risk === 'Alto' ? 'text-red-500' : 'text-emerald-500'}">${weather.risk}</b></span>
                    <span class="mx-1">|</span>
                    <span>Ocupación: <b class="${demand.color}">${demand.level}</b></span>
                </div>
            </div>
        </div>
    `;
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

    // 📊 GA4 Tracking: View Item
    if (window.LifextremeAnalytics) {
        window.LifextremeAnalytics.trackViewItem(activeTour);
    }

    // Reset State
    participants = 1;
    selectedAddons = [];
    selectedDay = null;

    // Init Draft
    draftBooking.updateDraft({ step: 1, tourId, completed: false });
    renderWizardStep(1);

    // Initial Data Fill
    document.getElementById('b-title').innerText = activeTour.title;
    
    // Dynamic Freshness Badge
    const today = new Date();
    today.setDate(today.getDate() - 1); // "Ayer"
    const dateStr = today.toISOString().split('T')[0];
    const freshnessEl = document.getElementById('seo-freshness-badge');
    if (freshnessEl) {
        freshnessEl.innerHTML = `<span class="inline-flex items-center gap-1.5 py-1 px-2.5 rounded-full text-[10px] font-black bg-emerald-500/10 text-emerald-600 border border-emerald-500/20"><i class="ri-radar-line"></i> Estado de Ruta: Abierta | Última actualización: ${dateStr}</span>`;
    }
    document.getElementById('b-dept').innerText = activeTour.dept || activeTour.cat;
    document.getElementById('b-duration').innerText = activeTour.genInfo?.duration || activeTour.duration || 'Flexible';
    document.getElementById('b-guide-lang').innerText = activeTour.genInfo?.guide || activeTour.guide || 'Español / Inglés';
    document.getElementById('b-cancel-policy').innerText = activeTour.genInfo?.cancelPolicy || activeTour.cancelPolicy || 'Estándar';

    // 1. Qué harás (whatYouDo)
    const sQueHaras = document.getElementById('section-que-haras');
    const bWhatYouDo = document.getElementById('b-what-you-do');
    if (activeTour.whatYouDo && activeTour.whatYouDo.length > 0) {
        sQueHaras.classList.remove('hidden');
        bWhatYouDo.innerHTML = activeTour.whatYouDo.map(item => `<li>${item}</li>`).join('');
    } else {
        sQueHaras.classList.add('hidden');
    }

    // 2. En detalle (direct_answer_block or detail)
    const sEnDetalle = document.getElementById('section-en-detalle');
    const bEnDetalle = document.getElementById('b-en-detalle');
    const detailText = activeTour.direct_answer_block || activeTour.detail;
    if (detailText) {
        sEnDetalle.classList.remove('hidden');
        bEnDetalle.innerText = detailText;
    } else {
        sEnDetalle.classList.add('hidden');
    }

    // 3. Itinerario Vertical Timeline (steps + fullItinerary)
    const sItinerario = document.getElementById('section-itinerario');
    const bTimeline = document.getElementById('b-timeline');
    if ((activeTour.steps && activeTour.steps.length > 0) || (activeTour.fullItinerary && activeTour.fullItinerary.length > 0)) {
        sItinerario.classList.remove('hidden');
        let htmlStr = "";
        
        if (activeTour.steps && activeTour.steps.length > 0) {
            htmlStr += activeTour.steps.map((step, idx) => {
                let bgColor = "bg-[#4267b2]";
                let textColor = "text-white";
                let borderColor = "";
                let innerContent = `<i class="${step.n}"></i>`;
                
                // Render specific styles based on icon types (like G for origin, dot for intermediate, etc.)
                if(step.n === 'G') {
                    bgColor = "bg-[#ff5533]";
                    innerContent = `<span class="font-bold font-sans">G</span>`;
                } else if (step.n === 'dot' && idx === activeTour.steps.length - 1) {
                    bgColor = "bg-[#ff5533]";
                    innerContent = ``; // Final dot
                } else if (step.n === 'dot') {
                    bgColor = "bg-white";
                    borderColor = "border-2 border-slate-300";
                    innerContent = ``;
                } else {
                    bgColor = "bg-[#112240]";
                }

                return `
                <div class="relative flex gap-4 items-start z-10">
                    <div class="w-7 h-7 shrink-0 rounded-full ${bgColor} ${borderColor} flex items-center justify-center ${textColor} text-xs shadow-md mt-1 relative z-20">
                        ${innerContent}
                    </div>
                    <div class="pt-1">
                        <span class="inline-block bg-[#4267b2] text-white text-[11px] font-bold px-2 py-0.5 rounded shadow-sm">${step.t}</span>
                        <p class="text-xs font-bold text-[#4267b2] mt-1">${step.d}</p>
                    </div>
                </div>`;
            }).join('');
        }
        
        if (activeTour.fullItinerary && activeTour.fullItinerary.length > 0) {
            if (activeTour.steps && activeTour.steps.length > 0) {
                htmlStr += `<div class="mt-6 mb-4 border-t border-slate-100 pt-6"></div>`;
            }
            htmlStr += activeTour.fullItinerary.map((item, idx) => `
                <div class="relative flex gap-4 items-start z-10 mb-2">
                    <div class="w-4 h-4 shrink-0 rounded-full bg-slate-300 border-2 border-white flex items-center justify-center mt-1 relative z-20"></div>
                    <div class="pt-0">
                        <span class="inline-block bg-[#ff5533] text-white text-[11px] font-bold px-2 py-0.5 rounded shadow-sm">${item.day}</span>
                        <p class="text-xs text-slate-600 mt-1">${item.desc}</p>
                    </div>
                </div>
            `).join('');
        }
        bTimeline.innerHTML = htmlStr;
    } else {
        sItinerario.classList.add('hidden');
    }

    // 4. Qué incluye (inc)
    const sQueIncluye = document.getElementById('section-que-incluye');
    const bQueIncluye = document.getElementById('b-que-incluye');
    if (activeTour.inc && activeTour.inc.length > 0) {
        sQueIncluye.classList.remove('hidden');
        bQueIncluye.innerHTML = activeTour.inc.map(item => `<li class="flex items-start gap-2"><i class="ri-check-line text-green-500 mt-0.5"></i> <span>${item}</span></li>`).join('');
    } else {
        sQueIncluye.classList.add('hidden');
    }

    // 4b. Qué no incluye (notInc)
    const sQueNoIncluye = document.getElementById('section-que-no-incluye');
    const bQueNoIncluye = document.getElementById('b-que-no-incluye');
    if (sQueNoIncluye && bQueNoIncluye) {
        if (activeTour.notInc && activeTour.notInc.length > 0) {
            sQueNoIncluye.classList.remove('hidden');
            bQueNoIncluye.innerHTML = activeTour.notInc.map(item => `<li class="flex items-start gap-2"><i class="ri-close-line text-red-500 mt-0.5 font-bold"></i> <span>${item}</span></li>`).join('');
        } else {
            sQueNoIncluye.classList.add('hidden');
        }
    }

    // 5. Punto de encuentro
    const sPuntoEncuentro = document.getElementById('section-punto-encuentro');
    const bPuntoEncuentro = document.getElementById('b-punto-encuentro');
    const bMapLink = document.getElementById('b-map-link');
    if (activeTour.meetingPoint) {
        sPuntoEncuentro.classList.remove('hidden');
        bPuntoEncuentro.innerText = activeTour.meetingPoint;
        bMapLink.href = `https://maps.google.com/?q=${encodeURIComponent(activeTour.meetingPoint)}`;
    } else {
        sPuntoEncuentro.classList.add('hidden');
    }

    // 6. Información importante
    const sInfoImportante = document.getElementById('section-info-importante');
    const sQueLlevar = document.getElementById('section-que-llevar');
    const bQueLlevar = document.getElementById('b-que-llevar');
    const sRecomendaciones = document.getElementById('section-recomendaciones');
    const bRecomendaciones = document.getElementById('b-recomendaciones');
    const sAntesViajar = document.getElementById('section-antes-viajar');
    const bAntesViajar = document.getElementById('b-antes-viajar');
    const sAptoPara = document.getElementById('section-apto-para');
    const bAptoPara = document.getElementById('b-apto-para');
    
    let hasInfo = false;

    // Qué llevar
    if (activeTour.whatToBring || activeTour.importantInfo) {
        if(bQueLlevar) bQueLlevar.innerText = activeTour.whatToBring || activeTour.importantInfo;
        if(sQueLlevar) sQueLlevar.classList.remove('hidden');
        hasInfo = true;
    } else {
        if(sQueLlevar) sQueLlevar.classList.add('hidden');
    }

    // Recomendaciones
    if (activeTour.recommendations) {
        if(bRecomendaciones) bRecomendaciones.innerText = activeTour.recommendations;
        if(sRecomendaciones) sRecomendaciones.classList.remove('hidden');
        hasInfo = true;
    } else {
        if(sRecomendaciones) sRecomendaciones.classList.add('hidden');
    }

    // Antes de viajar / No apto
    if (activeTour.notSuitable && activeTour.notSuitable.length > 0) {
        if(bAntesViajar) bAntesViajar.innerHTML = activeTour.notSuitable.map(item => `<li>No apto para: ${item}</li>`).join('');
        if(sAntesViajar) sAntesViajar.classList.remove('hidden');
        hasInfo = true;
    } else {
        if(sAntesViajar) sAntesViajar.classList.add('hidden');
    }

    // Apto para (Age Rating)
    if (activeTour.ageRating) {
        if(bAptoPara) bAptoPara.innerText = activeTour.ageRating;
        if(sAptoPara) sAptoPara.classList.remove('hidden');
        hasInfo = true;
    } else {
        if(sAptoPara) sAptoPara.classList.add('hidden');
    }

    if (hasInfo) {
        if(sInfoImportante) sInfoImportante.classList.remove('hidden');
    } else {
        if(sInfoImportante) sInfoImportante.classList.add('hidden');
    }

    // AI FAQS Block
    const aeoBlock = document.getElementById('ai-aeo-block');
    const faqsContainer = document.getElementById('faqs-container');
    const faqsList = document.getElementById('b-faqs');
    
    if (activeTour.faqs && activeTour.faqs.length > 0) {
        if(aeoBlock) aeoBlock.classList.remove('hidden');
        if(faqsContainer) faqsContainer.classList.remove('hidden');
        if(faqsList) faqsList.innerHTML = activeTour.faqs.map(faq => `
            <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                <h3 class="text-xs font-black text-slate-800 mb-1">Q: ${faq.q}</h3>
                <p class="text-[11px] font-medium text-slate-600 faq-answer">${faq.a}</p>
            </div>
        `).join('');
    } else {
        if(aeoBlock) aeoBlock.classList.add('hidden');
    }

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
        if (!selectedDay) {
            showToast('Fecha requerida', 'Selecciona una fecha en el calendario para continuar.', 'ri-calendar-event-line');
            return;
        }
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
    const liabilityContainer = document.getElementById('wiz-liability-container');

    nextBtn.classList.toggle('hidden', step === 3);
    prevBtn.classList.toggle('hidden', step === 1);
    finalBtn.classList.toggle('hidden', step !== 3);
    if(liabilityContainer) liabilityContainer.classList.toggle('hidden', step !== 3);
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
        // Renderizar Formulario de Contacto + Botón Final
        const finalBtnContainer = document.getElementById('step-3-actions'); // Necesitamos un contenedor específico o inyectarlo

        // Vamos a inyectar el formulario DENTRO del contenido del paso 3, con DNI y Firma Digital
        const step3Content = document.getElementById('booking-step-3');
        if (step3Content) {
            step3Content.innerHTML = `
                <div class="space-y-4 mb-5 text-left">
                    <h5 class="font-black text-sm uppercase text-slate-700 flex items-center gap-1.5">
                        <i class="ri-user-star-fill text-amber-500"></i> Tus Datos de Comandante
                    </h5>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div class="space-y-1">
                            <label class="text-[9px] font-black uppercase text-slate-400">Nombre Completo *</label>
                            <input type="text" id="contact-name" placeholder="Ej: Carlos Mendoza" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:border-primary outline-none">
                        </div>
                        <div class="space-y-1">
                            <label class="text-[9px] font-black uppercase text-slate-400">DNI / Pasaporte *</label>
                            <input type="text" id="contact-dni" placeholder="Ej: 72849102" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:border-primary outline-none">
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div class="space-y-1">
                            <label class="text-[9px] font-black uppercase text-slate-400">Email *</label>
                            <input type="email" id="contact-email" placeholder="tu@email.com" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:border-primary outline-none">
                        </div>
                        <div class="space-y-1">
                            <label class="text-[9px] font-black uppercase text-slate-400">WhatsApp Celular *</label>
                            <input type="tel" id="contact-phone" placeholder="+51 987 654 321" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:border-primary outline-none">
                        </div>
                    </div>
                </div>
                
                <div class="bg-primary/5 p-4 rounded-2xl border border-primary/10 mb-5 text-left">
                    <div id="review-tour-title" class="font-black italic text-base text-slate-800 mb-1">...</div>
                    <div class="flex justify-between text-xs font-bold text-slate-500">
                        <span id="review-date">...</span>
                        <span id="review-pax">...</span>
                    </div>
                </div>

                <!-- LEGAL LIABILITY WAIVER & DIGITAL SIGNATURE BOX -->
                <div class="bg-red-50/70 border-2 border-red-200/80 rounded-2xl p-4 text-left space-y-3 mb-4 shadow-sm">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-red-200/60 pb-2.5">
                        <div class="flex items-center gap-2">
                            <div class="w-7 h-7 rounded-lg bg-red-500 text-white flex items-center justify-center shrink-0">
                                <i class="ri-shield-check-fill text-base"></i>
                            </div>
                            <div>
                                <span class="text-[8px] font-black uppercase text-red-600 tracking-wider block">Normativa MINCETUR • D.S. N° 005-2016</span>
                                <h6 class="font-black text-xs text-slate-900 leading-tight">Carta de Asunción de Riesgos</h6>
                            </div>
                        </div>
                        <button type="button" onclick="window.openWaiverModal()"
                            class="bg-white hover:bg-red-100 text-red-700 border border-red-300 text-[9px] font-black uppercase px-3 py-1.5 rounded-lg transition-colors cursor-pointer flex items-center gap-1 w-fit">
                            <i class="ri-book-open-line"></i>
                            <span>Leer Documento Completo</span>
                        </button>
                    </div>

                    <!-- Digital Canvas Signature Pad -->
                    <div class="bg-white rounded-xl border border-slate-300 p-2.5 shadow-inner">
                        <div class="flex items-center justify-between mb-1.5 px-1">
                            <span class="text-[9px] font-black uppercase text-slate-500 flex items-center gap-1">
                                <i class="ri-edit-2-line text-red-500"></i> Firma Digital Obligatoria (Táctil o Mouse)
                            </span>
                            <button type="button" onclick="window.clearSignaturePad()" class="text-[9px] font-bold text-slate-400 hover:text-red-600 cursor-pointer flex items-center gap-0.5">
                                <i class="ri-refresh-line"></i> Borrar Firma
                            </button>
                        </div>
                        <div class="relative bg-slate-50 rounded-lg overflow-hidden border border-slate-200">
                            <canvas id="signature-canvas" width="400" height="100" class="w-full h-24 touch-none cursor-crosshair block"></canvas>
                            <div id="signature-hint" class="absolute inset-0 flex items-center justify-center pointer-events-none text-slate-400 text-[10px] font-bold italic">
                                ✍️ Traza tu firma aquí con tu dedo o mouse
                            </div>
                        </div>
                    </div>

                    <div class="flex items-start gap-2 pt-0.5">
                        <input type="checkbox" id="tour-liability-waiver" required
                            class="mt-0.5 w-4 h-4 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500 cursor-pointer">
                        <label for="tour-liability-waiver" class="text-[10px] text-slate-700 font-semibold cursor-pointer select-none leading-tight">
                            Declaro bajo juramento haber leído y aceptado la <strong class="text-red-700 underline" onclick="window.openWaiverModal()">Carta de Asunción de Riesgos</strong>. Mi firma digital y DNI quedan registrados como prueba legal vinculante.
                        </label>
                    </div>
                </div>
            `;

            // Inicializar el canvas de firma digital
            setTimeout(() => window.initSignaturePad(), 50);
        }

        finalBtn.innerHTML = '<span>CONFIRMAR & PAGAR</span><i class="ri-whatsapp-line text-xl pl-2"></i>';
        finalBtn.className = 'w-full bg-emerald-500 text-white py-6 rounded-3xl font-black uppercase tracking-widest shadow-xl shadow-emerald-500/20 hover:bg-emerald-600 transition-all flex items-center justify-center gap-3 animate-pulse';
        finalBtn.setAttribute('onclick', 'validateAndBook()');

        renderStep3Summary();
    }
}

// Inicializar Canvas de Firma Digital
window.hasDrawnSignature = false;

window.initSignaturePad = function() {
    const canvas = document.getElementById('signature-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const hint = document.getElementById('signature-hint');

    // Configurar estilo del trazo
    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    function getPos(e) {
        const rect = canvas.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {
            x: (clientX - rect.left) * scaleX,
            y: (clientY - rect.top) * scaleY
        };
    }

    function start(e) {
        e.preventDefault();
        isDrawing = true;
        const pos = getPos(e);
        lastX = pos.x;
        lastY = pos.y;
        if (hint) hint.classList.add('hidden');
        window.hasDrawnSignature = true;
        const cb = document.getElementById('tour-liability-waiver');
        if (cb) cb.checked = true;
    }

    function draw(e) {
        if (!isDrawing) return;
        e.preventDefault();
        const pos = getPos(e);
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
        lastX = pos.x;
        lastY = pos.y;
    }

    function stop() {
        isDrawing = false;
    }

    canvas.addEventListener('mousedown', start);
    canvas.addEventListener('mousemove', draw);
    window.addEventListener('mouseup', stop);

    canvas.addEventListener('touchstart', start, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    window.addEventListener('touchend', stop);
};

window.clearSignaturePad = function() {
    const canvas = document.getElementById('signature-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const hint = document.getElementById('signature-hint');
    if (hint) hint.classList.remove('hidden');
    window.hasDrawnSignature = false;
};

// Nueva función intermedia para validar antes de enviar
window.validateAndBook = function () {
    const name = document.getElementById('contact-name')?.value.trim();
    const dni = document.getElementById('contact-dni')?.value.trim();
    const email = document.getElementById('contact-email')?.value.trim();
    const phone = document.getElementById('contact-phone')?.value.trim();
    const waiverCb = document.getElementById('tour-liability-waiver');

    if (!name || !dni || !email || !phone) {
        showToast('Datos requeridos', 'Completa tu nombre, DNI, email y WhatsApp para continuar.', 'ri-user-follow-line');
        return;
    }

    if (!waiverCb || !waiverCb.checked) {
        showToast('Compromiso Legal Requerido', 'Debes leer y aceptar la Carta de Asunción de Riesgos.', 'ri-shield-flash-line');
        return;
    }

    if (!window.hasDrawnSignature) {
        showToast('Firma Requerida', 'Por favor traza tu firma digital en el recuadro para validar el deslinde legal.', 'ri-edit-2-line');
        return;
    }

    const legalHash = 'LFX-WAIVER-2026-' + Date.now().toString(36).toUpperCase();
    const waiverRecord = {
        name, dni, email, phone,
        tour: activeTour?.title || 'Expedición Lifextreme',
        timestamp: new Date().toISOString(),
        hash: legalHash
    };

    localStorage.setItem('lifextreme_user_name', name);
    localStorage.setItem('lifextreme_user_dni', dni);
    localStorage.setItem('lifextreme_user_email', email);
    localStorage.setItem('lifextreme_user_phone', phone);
    localStorage.setItem('lifextreme_active_waiver', JSON.stringify(waiverRecord));

    window.currentContact = { name, dni, email, phone };
    window.currentWaiver = waiverRecord;
    addToCartFinal();
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
    // Check Liability Waiver
    const waiverCb = document.getElementById('tour-liability-waiver');
    if (waiverCb && !waiverCb.checked) {
        showToast('Atención', 'Debes aceptar la Carta de Asunción de Riesgos para continuar.', 'ri-error-warning-line');
        return;
    }

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

    // 📊 GA4 Tracking: Add to Cart
    if (window.LifextremeAnalytics) {
        window.LifextremeAnalytics.trackAddToCart(item);
    }

    // 2. ☁️ Sincronizar con Supabase
    if (window.processBookingCusco) {
        window.processBookingCusco({
            tourId: activeTour.id,
            tourName: activeTour.title,
            date: fullDate,
            pax: participants,
            price: item.price,
            contact: window.currentContact || {
                name: "Usuario Web",
                email: "pendiente@checkout.com",
                phone: "000000000"
            }
        });
    }

    closeModal();
    updateCart();

    // 3. 📲 REDIRECCIÓN A WHATSAPP (CIERRE DE VENTA CON PRUEBA LEGAL)
    const contact = window.currentContact || { name: 'Viajero' };
    const waiver = window.currentWaiver || JSON.parse(localStorage.getItem('lifextreme_active_waiver') || '{}');
    const legalText = waiver.hash
        ? `\n\n📜 *Compromiso Legal MINCETUR (Ley 29408):* Firmado Digitalmente\n🆔 *DNI / Pasaporte:* ${contact.dni || waiver.dni || 'Validado'}\n🔐 *Hash Legal:* ${waiver.hash}`
        : `\n\n✅ *He leído y acepto los Términos y la Carta de Asunción de Riesgos.*`;

    const activeVariant = (window.SensoryEngine && window.SensoryEngine.lastTriggeredVariant) ? window.SensoryEngine.lastTriggeredVariant : 'none';
    const waMessage = `Hola Lifextreme! 🏔️ Soy *${contact.name}*.\nQuiero confirmar mi reserva:\n\n📍 *Tour:* ${activeTour.title}\n📅 *Fecha:* ${fullDate}\n👥 *Pax:* ${participants}\n💰 *Total:* S/ ${item.price}${legalText}\n\nQuedo atento para coordinar el pago. 🚀`;
    const waUrl = `https://wa.me/51958050928?text=${encodeURIComponent(waMessage)}&utm_source=web&utm_medium=whatsapp&utm_campaign=sensory_booking&utm_content=${activeVariant}`;

    // Abrir WhatsApp en nueva pestaña
    window.open(waUrl, '_blank');

    // Toast Feedback
    const msg = currentLang === 'es' ? `¡Solicitud enviada! Finaliza en WhatsApp` : `Request sent! Finish on WhatsApp`;
    showToast('Mochila Táctica', msg, 'ri-whatsapp-fill');


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
        const totalEl = document.getElementById('cart-total');
        if (totalEl) totalEl.innerText = window.PriceEngine ? window.PriceEngine.format(0) : "S/ 0";
        return;
    }

    list.innerHTML = items.map((item, idx) => {
        const itemPriceFormatted = window.PriceEngine ? window.PriceEngine.format(item.price) : `S/ ${item.price}`;
        return `
        <div class="flex items-center gap-4 bg-slate-50 p-4 rounded-3xl border border-slate-100">
            <img src="${item.img}?w=100" class="w-12 h-12 rounded-xl object-cover">
            <div class="flex-1">
                <h4 class="font-black text-[10px] uppercase">${item.name}</h4>
                <p class="text-[8px] font-bold text-slate-400">${item.detail}</p>
            </div>
            <p class="font-black text-xs">${itemPriceFormatted}</p>
            <button data-action="remove-item" data-idx="${idx}" class="text-slate-300 hover:text-red-500 cursor-pointer"><i class="ri-delete-bin-line"></i></button>
        </div>
        `;
    }).join('');

    const totalEl = document.getElementById('cart-total');
    if (totalEl) {
        const discountedTotal = total * 0.85; // Elite Discount
        totalEl.innerText = window.PriceEngine ? window.PriceEngine.format(discountedTotal) : `S/ ${Math.round(discountedTotal).toLocaleString()}`;
    }
}

// 360 Angle Switcher & Delivery State for Equipment
window.selectedEquipDeliveries = {};

window.switchAngle360 = function(imgId, newUrl, btnEl) {
    const img = document.getElementById(imgId);
    if (!img) return;
    img.style.opacity = '0.3';
    setTimeout(() => {
        img.src = newUrl;
        img.style.opacity = '1';
    }, 150);
    if (btnEl && btnEl.parentElement) {
        btnEl.parentElement.querySelectorAll('button').forEach(b => {
            b.classList.remove('bg-amber-400', 'text-slate-950');
            b.classList.add('bg-white/80', 'text-slate-700');
        });
        btnEl.classList.remove('bg-white/80', 'text-slate-700');
        btnEl.classList.add('bg-amber-400', 'text-slate-950');
    }
};

window.toggleEquipDelivery = function(idx, checked) {
    window.selectedEquipDeliveries[idx] = checked;
    const toastMsg = checked ? 'Delivery express activado (+S/ 25.00 a hotel/agencia)' : 'Recojo en Basecamp seleccionado';
    showToast('Logística de Entrega', toastMsg, 'ri-truck-fill');
};

window.toggleHeroAudio = function() {
    const video = document.getElementById('hero-bg-video');
    const audioText = document.getElementById('audio-text');
    const btn = document.getElementById('audio-toggle');
    if (!video) return;

    const icon = btn ? btn.querySelector('i') : null;
    if (video.muted) {
        video.muted = false;
        video.volume = 0.8;
        if (audioText) audioText.textContent = 'Silenciar';
        if (icon) {
            icon.classList.remove('ri-volume-mute-line');
            icon.classList.add('ri-volume-up-line');
        }
        if (window.showToast) window.showToast('Audio Inmersivo', 'Disfruta el sonido de la expedición peruana.', 'ri-volume-up-line');
    } else {
        video.muted = true;
        if (audioText) audioText.textContent = 'Activar Sonido';
        if (icon) {
            icon.classList.remove('ri-volume-up-line');
            icon.classList.add('ri-volume-mute-line');
        }
    }
};

async function renderGuides() {
    const grid = document.getElementById('guides-grid');
    if (!grid) return;

    const guides = window.guides || [];
    grid.innerHTML = guides.map((guide) => `
        <div class="neuro-card bg-slate-900/85 backdrop-blur-md text-white rounded-[44px] overflow-hidden border border-white/10 hover:border-amber-400/50 group hover:shadow-[0_20px_45px_rgba(245,158,11,0.18)] transition-all duration-500 flex flex-col h-full shadow-xl">
            <div class="h-72 overflow-hidden relative bg-slate-900">
                <div class="skeleton-loader absolute inset-0"></div>
                <img src="${guide.img}?w=600" loading="lazy" class="h-full w-full object-cover group-hover:scale-105 transition-all duration-700 img-reveal" onload="this.classList.add('loaded'); if(this.previousElementSibling) this.previousElementSibling.style.display='none';">
                
                <!-- Region & Verification Badges -->
                <div class="absolute top-4 left-4 flex flex-col gap-1.5 z-10">
                    <span class="bg-slate-950/85 backdrop-blur-md text-amber-400 border border-amber-400/30 px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-wider shadow-md">
                        📍 ${guide.region || 'Perú'}
                    </span>
                    <span class="bg-primary/90 backdrop-blur-md text-white px-3 py-1 rounded-full text-[8px] font-black uppercase tracking-widest shadow-md">
                        ${guide.cert ? '🛡️ ' + guide.cert.split('•')[0] : 'Guía Oficial'}
                    </span>
                </div>

                <div class="absolute bottom-4 left-4 right-4 p-3.5 bg-slate-950/85 backdrop-blur-md rounded-2xl border border-white/10 text-white">
                    <p class="text-[8px] font-black uppercase text-amber-400 tracking-widest">Especialidad</p>
                    <p class="text-xs font-black italic">${guide.specialty}</p>
                </div>
            </div>

            <div class="p-6 sm:p-8 flex-1 flex flex-col justify-between space-y-6">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <h4 class="font-black italic text-2xl text-white group-hover:text-amber-300 transition-colors leading-tight">${guide.name}</h4>
                        <span class="text-[10px] font-black bg-amber-400/15 text-amber-300 border border-amber-400/30 px-2.5 py-1 rounded-full shrink-0">
                            ⭐ ${guide.exp}
                        </span>
                    </div>
                    <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-4">
                        🗣️ Idiomas: ${(guide.languages || []).join(' • ')}
                    </p>
                    
                    <p class="text-xs font-medium text-slate-300 leading-relaxed mb-4">
                        ${guide.desc || ''}
                    </p>
                    
                    ${guide.cert ? `
                    <div class="bg-white/5 p-3 rounded-2xl border border-white/10 mb-4 flex items-center gap-2.5">
                        <i class="ri-verified-badge-fill text-amber-400 text-lg shrink-0"></i>
                        <span class="text-[10px] font-black text-slate-200 leading-tight">${guide.cert}</span>
                    </div>` : ''}
                </div>
                
                <div class="space-y-2 pt-4 border-t border-white/10 mt-auto">
                    <button onclick="window.openGuideHireModal('${guide.name.replace(/'/g, "\\'")}', ${guide.id});" 
                        class="w-full py-3.5 bg-amber-400 hover:bg-amber-300 text-slate-950 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all shadow-md flex items-center justify-center gap-2 cursor-pointer">
                        <i class="ri-file-list-3-line"></i> Ver Itinerario & Recomendaciones
                    </button>
                    <a href="https://wa.me/51958050928?text=${encodeURIComponent('Hola Lifextreme! Deseo consultar disponibilidad para contratar al guía certificado ' + guide.name + ' en ' + (guide.region || 'Perú') + '.')}" 
                        target="_blank" rel="noopener"
                        class="w-full py-3 bg-emerald-500/15 hover:bg-emerald-500 text-emerald-300 hover:text-slate-950 border border-emerald-500/30 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all flex items-center justify-center gap-2">
                        <i class="ri-whatsapp-fill text-base"></i> Consultar Disponibilidad
                    </a>
                </div>
            </div>
        </div>
    `).join('');
}

// --- RENDER MAIN GRIDS ---
function renderAll(region = 'Todos', category = 'Todos') {
    const grid = document.getElementById('destinos-grid');
    if (!grid) return;

    const allTours = (typeof tours !== 'undefined') ? tours : (window.tours || []);
    const filtered = (region === 'Todos') ? allTours : allTours.filter(t => t.dept === region);
    grid.innerHTML = filtered.map((t, i) => {
        const tourPrice = window.PriceEngine ? window.PriceEngine.format(t.price) : `S/ ${t.price}`;
        const isMapi = t.title.toLowerCase().includes('machu picchu');
        const isKuelap = t.title.toLowerCase().includes('kuélap') || t.title.toLowerCase().includes('kuelap');
        let liveTelemetryBadge = '';
        if (isMapi) {
            liveTelemetryBadge = `
            <div class="mb-3 px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/25 flex items-center justify-between text-[10px]">
                <span class="flex items-center gap-1.5 text-emerald-400 font-bold">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    TuBoleto Cultura: 284 cupos en vivo
                </span>
                <span class="text-slate-400 text-[9px] font-medium">Tren: Asientos OK</span>
            </div>`;
        } else if (isKuelap) {
            liveTelemetryBadge = `
            <div class="mb-3 px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/25 flex items-center justify-between text-[10px]">
                <span class="flex items-center gap-1.5 text-amber-400 font-bold">
                    <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
                    Telecabinas Kuélap: Operativas
                </span>
                <span class="text-slate-400 text-[9px] font-medium">Monitoreo Oficial</span>
            </div>`;
        }

        return `
        <div class="neuro-card bg-slate-900/85 backdrop-blur-md text-white rounded-[40px] overflow-hidden group cursor-pointer shadow-xl hover:shadow-[0_20px_45px_rgba(245,158,11,0.18)] transition-all animate-card-entry relative border border-white/10 hover:border-amber-400/50" 
             style="animation-delay: ${i * 40}ms; animation-fill-mode: both;"
             data-action="open-booking" data-id="${t.id}">
            <!-- Share Button Overlay -->
            <div class="card-share-overlay">
                <button 
                    class="share-btn-compact" 
                    onclick="event.stopPropagation(); window.ShareEngine.shareViaWhatsApp({id: ${t.id}, title: '${t.title.replace(/'/g, "\\'")}', dept: '${t.dept}', duration: '${t.duration}', price: ${t.price}}, 'tour');"
                    title="Invitar a un amigo">
                    <i class="ri-whatsapp-line text-emerald-400"></i>
                </button>
            </div>
            <div class="h-64 overflow-hidden relative bg-slate-950">
                <div class="skeleton-loader absolute inset-0"></div>
                <img src="${t.img}?w=500" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition-all duration-700 img-reveal" onload="this.classList.add('loaded'); if(this.previousElementSibling) this.previousElementSibling.style.display='none';">
                <div class="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-transparent to-transparent"></div>
            </div>
            <div class="p-8">
                <div class="flex justify-between items-center mb-2">
                    <p class="text-[9px] font-black text-amber-400 uppercase tracking-widest">${t.dept}</p>
                    <div class="flex items-center gap-2">
                        <button 
                            onclick="event.stopPropagation(); window.ShareEngine.copyLinkToClipboard('tour', ${t.id});" 
                            class="text-slate-400 hover:text-amber-400 transition-colors z-10 relative" 
                            title="Copiar link">
                            <i class="ri-link text-sm"></i>
                        </button>
                        <button data-action="toggle-wishlist" data-id="${t.id}" class="${wishlist.includes(t.id) ? 'text-secondary' : 'text-slate-500 hover:text-rose-400'} z-10 relative"><i class="ri-heart-pulse-fill"></i></button>
                    </div>
                </div>
                ${liveTelemetryBadge}
                <h3 class="text-xl font-black italic mb-6 text-white group-hover:text-amber-300 transition-colors">${t.title}</h3>
                <div class="flex justify-between items-center pt-6 border-t border-white/10 font-black">
                    <span class="text-2xl italic text-amber-400">${tourPrice}</span>
                    <i class="ri-arrow-right-line text-amber-400 text-xl group-hover:translate-x-1.5 transition-transform"></i>
                </div>
            </div>
        </div>
        `;
    }).join('');
    
    // SEO: Inyectar Schema de Producto para Expediciones
    if (typeof injectTourSchema === 'function') {
        injectTourSchema(filtered);
    }

    // Handle Equipment grid if it exists
    const equipGrid = document.getElementById('equip-grid');
    if (equipGrid) {
        let equipsData = (typeof equips !== 'undefined') ? equips : (window.equips || []);
        if (category !== 'Todos') {
            equipsData = equipsData.filter(e => e.cat === category);
        }

        equipGrid.innerHTML = equipsData.map((e, i) => {
            const buyPrice = window.PriceEngine ? window.PriceEngine.format(e.price) : `S/ ${e.price}`;
            const rentPrice = window.PriceEngine ? window.PriceEngine.format(e.rentPrice) : `S/ ${e.rentPrice}`;
            const views = e.views360 || [e.img];
            const imgId = `equip-img-${i}`;

            return `
            <div class="neuro-card bg-slate-900/85 backdrop-blur-md rounded-[36px] border border-white/10 hover:border-amber-400/50 shadow-xl hover:shadow-[0_20px_45px_rgba(245,158,11,0.18)] transition-all p-6 sm:p-7 flex flex-col justify-between animate-card-entry text-white" style="animation-delay: ${i * 40}ms; animation-fill-mode: both;">
                <div>
                    <!-- Top Category & Recommend Destinos -->
                    <div class="flex items-center justify-between gap-2 mb-3">
                        <span class="bg-amber-400/15 text-amber-300 border border-amber-400/30 text-[9px] font-black uppercase px-3 py-1 rounded-full tracking-wider">
                            ${e.cat}
                        </span>
                        ${e.destinos ? `
                        <span class="text-[9px] font-bold text-slate-400 truncate max-w-[180px]" title="${e.destinos}">
                            📍 ${e.destinos}
                        </span>` : ''}
                    </div>

                    <!-- Main Image with 360 Spin Preview Controls -->
                    <div class="h-60 rounded-3xl relative overflow-hidden bg-slate-950 mb-4 group/img">
                        <img id="${imgId}" src="${e.img}?w=600" loading="lazy" class="w-full h-full object-cover transition-opacity duration-300" alt="${e.name}">
                        
                        <!-- 360 Spin Angle Bar -->
                        <div class="absolute bottom-3 left-3 right-3 bg-slate-950/80 backdrop-blur-md rounded-xl p-1.5 flex items-center justify-between gap-1 z-10 border border-white/10">
                            <span class="text-[8px] font-black uppercase text-amber-400 tracking-wider flex items-center gap-1 pl-1">
                                <i class="ri-360-line text-xs"></i> 360°
                            </span>
                            <div class="flex items-center gap-1">
                                ${views.map((v, vIdx) => `
                                    <button type="button" onclick="window.switchAngle360('${imgId}', '${v}?w=600', this)" 
                                        class="${vIdx === 0 ? 'bg-amber-400 text-slate-950' : 'bg-white/80 text-slate-700 hover:bg-white'} text-[8px] font-black px-2 py-0.5 rounded-lg transition-all cursor-pointer">
                                        ${vIdx === 0 ? 'Frente' : vIdx === 1 ? 'Lateral' : vIdx === 2 ? 'Interior' : 'Detalle'}
                                    </button>
                                `).join('')}
                            </div>
                        </div>
                    </div>

                    <h4 class="font-black italic text-lg sm:text-xl text-white group-hover:text-amber-300 transition-colors leading-snug mb-2">${e.name}</h4>
                    <p class="text-xs text-slate-300 mb-4 leading-relaxed">${e.desc || ''}</p>

                    <!-- Technical Specs Grid -->
                    ${e.specs ? `
                    <div class="grid grid-cols-2 gap-2 bg-white/5 p-3 rounded-2xl border border-white/10 text-[10px] font-bold text-slate-300 mb-4">
                        ${e.specs.peso ? `<div><strong class="text-white block text-[9px] uppercase text-slate-400">Peso</strong> ${e.specs.peso}</div>` : ''}
                        ${e.specs.temp ? `<div><strong class="text-white block text-[9px] uppercase text-slate-400">Rango Temp / Viento</strong> ${e.specs.temp}</div>` : ''}
                        ${e.specs.impermeable ? `<div><strong class="text-white block text-[9px] uppercase text-slate-400">Impermeabilidad</strong> ${e.specs.impermeable}</div>` : ''}
                        ${e.specs.cert ? `<div><strong class="text-white block text-[9px] uppercase text-slate-400">Norma / Cert.</strong> ${e.specs.cert}</div>` : ''}
                    </div>` : ''}

                    <!-- Express Delivery Option -->
                    <div class="mb-4">
                        <label class="flex items-center gap-2 text-[10px] font-bold text-slate-200 bg-white/5 hover:bg-white/10 p-3 rounded-2xl border border-white/10 cursor-pointer transition-all">
                            <input type="checkbox" class="accent-amber-500 w-4 h-4 rounded cursor-pointer" onchange="window.toggleEquipDelivery(${i}, this.checked)">
                            <span>🚚 <strong>Delivery Express</strong> a mi Hotel/Agencia en Cusco o Huaraz (+S/ 25.00)</span>
                        </label>
                    </div>
                </div>

                <!-- Price & Action Buttons -->
                <div class="grid grid-cols-2 gap-2 pt-3 border-t border-white/10">
                    <button type="button" onclick="const del = window.selectedEquipDeliveries[${i}]; const p = ${e.price} + (del ? 25 : 0); const n = '${e.name.replace(/'/g, "\\'")}' + (del ? ' (+ Delivery Express)' : ''); addToCartShort(n, p, 'sale', '${e.img}');"
                        class="flex flex-col items-center justify-center bg-amber-400 hover:bg-amber-300 text-slate-950 p-3 rounded-2xl transition-all cursor-pointer shadow-sm group">
                        <span class="text-[9px] font-black uppercase mb-0.5">Comprar</span>
                        <span class="text-sm font-black italic">${buyPrice}</span>
                    </button>
                    
                    <button type="button" onclick="const del = window.selectedEquipDeliveries[${i}]; const p = ${e.rentPrice} + (del ? 25 : 0); const n = '${e.name.replace(/'/g, "\\'")}' + (del ? ' (+ Delivery Express)' : ''); addToCartShort(n, p, 'rent', '${e.img}');"
                        class="flex flex-col items-center justify-center bg-indigo-50 hover:bg-primary hover:text-white text-primary p-3 rounded-2xl transition-all cursor-pointer border border-indigo-100 group">
                        <span class="text-[9px] font-bold text-indigo-400 uppercase mb-0.5 group-hover:text-indigo-100">Alquilar / Día</span>
                        <span class="text-sm font-black italic">${rentPrice}</span>
                    </button>
                </div>
            </div>
            `;
        }).join('');
    }

    renderGuides();
    renderEvents();
}

// Expose function globally for onclick event
window.openGuideHireModal = function (name, id) {
    const modal = document.getElementById('guide-hire-modal');
    if (modal) {
        modal.classList.remove('hidden');
        document.getElementById('guide-modal-name').innerText = name;
        document.getElementById('guide-id-input').value = id;
    }
}

function renderEvents(region = 'Todos') {
    const grid = document.getElementById('events-grid');
    if (!grid) return;

    const allEvents = (typeof events !== 'undefined') ? events : (window.events || []);
    const filtered = (region === 'Todos') ? allEvents : allEvents.filter(e => e.dept === region);

    if (filtered.length === 0) {
        grid.innerHTML = `<div class="col-span-full py-20 text-center opacity-40"><i class="ri-calendar-event-line text-5xl mb-4 block"></i><p class="font-black italic">${translations[currentLang].status_no_events}</p></div>`;
        return;
    }

    grid.innerHTML = filtered.map(e => {
        const eventPrice = window.PriceEngine ? window.PriceEngine.format(e.price) : `S/ ${e.price}`;
        return `
        <div class="neuro-card bg-slate-900/85 backdrop-blur-md text-white rounded-[44px] overflow-hidden group shadow-xl hover:shadow-[0_20px_45px_rgba(244,63,94,0.18)] transition-all duration-500 border border-white/10 hover:border-rose-400/50 flex flex-col h-full relative" data-action="open-booking" data-id="${e.id}">
            <!-- Share Button Overlay -->
            <div class="card-share-overlay">
                <button 
                    class="share-btn-compact" 
                    onclick="event.stopPropagation(); window.ShareEngine.shareViaWhatsApp({id: ${e.id}, title: '${e.title.replace(/'/g, "\\'")}'', dept: '${e.dept}', date: '${e.date} ${e.month}', price: ${e.price}}, 'event');"
                    title="Invitar a un amigo">
                    <i class="ri-whatsapp-line text-emerald-400"></i>
                </button>
            </div>
            <div class="h-64 overflow-hidden relative bg-slate-950">
                <div class="skeleton-loader absolute inset-0"></div>
                <img src="${e.img}?w=500" loading="lazy" class="h-full w-full object-cover group-hover:scale-110 transition-all duration-700 img-reveal" onload="this.classList.add('loaded'); if(this.previousElementSibling) this.previousElementSibling.style.display='none';">
                <div class="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-transparent to-transparent"></div>
                <div class="absolute top-6 left-6 bg-slate-900/90 backdrop-blur-md px-4 py-3 rounded-2xl shadow-sm text-center min-w-[60px] border border-white/15">
                    <p class="text-xs font-black text-amber-400 leading-none">${e.date}</p>
                    <p class="text-[8px] font-black text-slate-300 uppercase tracking-widest mt-1">${e.month}</p>
                </div>
                <div class="absolute bottom-6 right-6 bg-gradient-to-r from-rose-600 to-orange-500 backdrop-blur-md px-4 py-2 rounded-xl text-white text-[9px] font-black uppercase tracking-widest shadow-lg">
                    ${e.cat}
                </div>
            </div>
            <div class="p-8 sm:p-10 flex-1 flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-start mb-3">
                        <p class="text-[9px] font-black text-amber-400 uppercase tracking-[0.3em]">${e.dept}</p>
                        <button 
                            onclick="event.stopPropagation(); window.ShareEngine.copyLinkToClipboard('event', ${e.id});" 
                            class="text-slate-400 hover:text-amber-400 transition-colors" 
                            title="Copiar link">
                            <i class="ri-link text-sm"></i>
                        </button>
                    </div>
                    <h4 class="text-2xl font-black italic text-white mb-4 leading-tight group-hover:text-amber-300 transition-colors">${e.title}</h4>
                    <p class="text-xs font-medium text-slate-300 mb-6 leading-relaxed">${e.detail}</p>
                    
                    <div class="flex flex-wrap gap-2 mb-6">
                        ${e.whatYouDo.map(tag => `<span class="bg-white/5 text-slate-300 px-3 py-1.5 rounded-lg text-[8px] font-black uppercase tracking-wider border border-white/10">${tag}</span>`).join('')}
                    </div>
                </div>
                
                <div class="flex items-center justify-between pt-6 border-t border-white/10">
                    <div>
                        <p class="text-[8px] font-black text-slate-400 uppercase tracking-widest mb-1">${translations[currentLang].card_inscription}</p>
                        <p class="text-2xl font-black italic text-amber-400">${eventPrice}</p>
                    </div>
                    <button class="w-12 h-12 bg-white/10 hover:bg-amber-400 hover:text-slate-950 rounded-2xl flex items-center justify-center text-white transition-all shadow-sm">
                        <i class="ri-arrow-right-up-line text-xl"></i>
                    </button>
                </div>
            </div>
        </div>
        `;
    }).join('');
}

// Global Currency Change Handler linked to Language
window.handleCurrencyChange = function(curr) {
    if (window.PriceEngine) {
        window.PriceEngine.setCurrency(curr);
    }
    const sel = document.getElementById('currency-selector');
    if (sel && sel.value !== curr) sel.value = curr;

    // Automatic Language Sync according to Currency
    if (curr === 'PEN' && currentLang !== 'es') {
        setLanguage('es');
        return;
    } else if (curr === 'USD' && currentLang !== 'en') {
        setLanguage('en');
        return;
    } else if (curr === 'BRL' && currentLang !== 'pt') {
        setLanguage('pt');
        return;
    }

    renderAll();
    updateCart();
    if (typeof updateTotalPrice === 'function') updateTotalPrice();
    showToast('Moneda Sincronizada', `Precios actualizados en ${curr}`, 'ri-exchange-dollar-line');
};

// --- EVENT DELEGATION SYSTEM (CORE UPDATE) ---
function setupEventListeners() {
    // Click Handler Central
    document.body.addEventListener('click', (e) => {
        const target = e.target.closest('[data-action]');
        if (!target) return;

        const action = target.dataset.action;
        const data = target.dataset;

        // Evitar comportamiento default si es un enlace de navegacion o enlace hash
        if (target.tagName === 'A' && (action === 'navigate' || action === 'mobile-navigate' || target.getAttribute('href')?.startsWith('#'))) {
            e.preventDefault();
        }

        // Router de Acciones
        switch (action) {
            case 'navigate': navigateTo(data.target); break;
            case 'mobile-navigate': mobileNavigate(data.target); break;
            case 'set-lang': setLanguage(data.lang); break;
            case 'set-currency': 
                window.handleCurrencyChange(data.currency);
                break;
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

            // Payment & Modals
            case 'open-checkout': openStripeCheckout(); break;
            case 'close-checkout': closeStripeCheckout(); break;
            case 'switch-payment': switchPaymentMethod(data.method); break;
            case 'select-payment-plan':
                if (data.plan === 'split') {
                    document.getElementById('payment-plan-split')?.click();
                } else {
                    document.getElementById('payment-plan-full')?.click();
                }
                break;
            case 'confirm-payment': confirmManualPayment(); break;
            case 'continue-exploring': toggleCart(); break;
            case 'close-guide-modal':
                if (typeof window.closeGuideContactModal === 'function') {
                    window.closeGuideContactModal();
                } else {
                    document.getElementById('guide-contact-modal')?.classList.add('hidden');
                }
                break;
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
    if (typeof renderEvents === 'function') renderEvents();
    if (typeof renderGuides === 'function') renderGuides();
    if (typeof window.initInfrastructure === 'function') window.initInfrastructure();
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
    if (!email) {
        showToast('Email requerido', 'Ingresa tu correo para recibir tu recomendación y cupón.', 'ri-mail-send-line');
        return;
    }

    const resultTour = tours[Math.floor(Math.random() * tours.length)];
    document.getElementById('recommended-tour').innerText = resultTour.title;

    document.querySelectorAll('.quiz-step').forEach(s => s.classList.add('hidden'));
    document.getElementById('quiz-step-result').classList.remove('hidden');
}

// Accordion toggle helper for Club Socio collapsible modules
window.toggleSocioAccordion = function(panelId, btnEl) {
    const panel = document.getElementById(panelId);
    if (!panel) return;
    const isHidden = panel.classList.contains('hidden');
    // Close sibling accordions in the same container for clean UX
    const parent = panel.closest('.socio-accordion-group');
    if (parent) {
        parent.querySelectorAll('.socio-accordion-panel').forEach(p => {
            if (p.id !== panelId) p.classList.add('hidden');
        });
        parent.querySelectorAll('.socio-accordion-icon').forEach(ic => {
            ic.style.transform = 'rotate(0deg)';
        });
    }
    panel.classList.toggle('hidden', !isHidden);
    const icon = btnEl ? btnEl.querySelector('.socio-accordion-icon') : null;
    if (icon) {
        icon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
    }
};

// SPA Navigation
function navigateTo(id) {
    const selectedNav = id;
    document.querySelectorAll('.nav-link').forEach(link => {
        const isMatch = (link.id === 'nav-' + selectedNav) || (link.dataset && link.dataset.target === selectedNav);
        link.classList.toggle('active', isMatch);
    });

    if (id === 'destinos') {
        id = 'home';
        document.querySelectorAll('.section-view').forEach(s => s.classList.remove('active'));
        document.getElementById('section-' + id)?.classList.add('active');
        if (typeof renderAll === 'function') renderAll();
        setTimeout(() => {
            const destContainer = document.getElementById('home-destinos-container');
            if (destContainer) destContainer.scrollIntoView({ behavior: 'smooth' });
        }, 50);
        return;
    }

    document.querySelectorAll('.section-view').forEach(s => s.classList.remove('active'));
    const targetSection = document.getElementById('section-' + id);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // Explicitly re-render module grids so contents are never blank
    if (id === 'socio') {
        if (typeof updateWishlistDashboard === 'function') updateWishlistDashboard();
    } else if (id === 'eventos') {
        if (typeof renderEvents === 'function') renderEvents();
    } else if (id === 'guias') {
        if (typeof renderGuides === 'function') renderGuides();
    } else if (id === 'equipos') {
        if (typeof renderAll === 'function') renderAll('Todos', 'Todos');
    } else if (id === 'infraestructura') {
        if (typeof window.initInfrastructure === 'function') {
            window.initInfrastructure();
        } else if (typeof renderInfrastructure === 'function' && window.parks) {
            renderInfrastructure(window.parks);
        }
    } else if (id === 'home') {
        if (typeof renderAll === 'function') renderAll();
    }

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

// --- LANGUAGE DROPDOWN & I18N LOGIC ---
window.toggleLangDropdown = function(e) {
    if (e) e.stopPropagation();
    const menu = document.getElementById('lang-dropdown-menu');
    if (menu) menu.classList.toggle('hidden');
};

document.addEventListener('click', (e) => {
    const wrapper = document.getElementById('lang-dropdown-wrapper');
    const menu = document.getElementById('lang-dropdown-menu');
    if (menu && !menu.classList.contains('hidden')) {
        if (!wrapper || !wrapper.contains(e.target)) {
            menu.classList.add('hidden');
        }
    }
});

// Global fallback for any broken external image
window.addEventListener('error', (e) => {
    if (e.target && e.target.tagName === 'IMG' && !e.target.dataset.fallbackApplied) {
        e.target.dataset.fallbackApplied = 'true';
        e.target.src = 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&fm=webp&q=80';
    }
}, true);

function setLanguage(lang) {
    const menu = document.getElementById('lang-dropdown-menu');
    if (menu) menu.classList.add('hidden');

    // Sincronizar moneda de acuerdo al idioma
    const langToCurrency = { es: 'PEN', en: 'USD', pt: 'BRL' };
    const targetCurrency = langToCurrency[lang] || 'PEN';
    if (window.PriceEngine) {
        window.PriceEngine.setCurrency(targetCurrency);
    }
    const currSel = document.getElementById('currency-selector');
    if (currSel) currSel.value = targetCurrency;

    if (currentLang === lang) {
        updateLanguageUI();
        renderAll();
        updateCart();
        return;
    }
    localStorage.setItem('lifextreme_lang', lang);
    
    const currentPath = window.location.pathname;
    let isEn = currentPath.includes('/en/') || currentPath.endsWith('/en');
    let isPt = currentPath.includes('/pt/') || currentPath.endsWith('/pt');
    
    if (lang === 'en' && !isEn) {
        if (isPt) {
            window.location.href = window.location.href.replace('/pt/', '/en/');
        } else {
            window.location.href = 'en/index.html' + window.location.hash;
        }
    } else if (lang === 'pt' && !isPt) {
        if (isEn) {
            window.location.href = window.location.href.replace('/en/', '/pt/');
        } else {
            window.location.href = 'pt/index.html' + window.location.hash;
        }
    } else if (lang === 'es' && (isEn || isPt)) {
        window.location.href = '../index.html' + window.location.hash;
    } else {
        currentLang = lang;
        updateLanguageUI();
        renderAll();
        updateCart();
        const msgs = {
            es: 'Idioma cambiado a Español (Moneda: S/ PEN)',
            en: 'Language switched to English (Currency: $ USD)',
            pt: 'Idioma alterado para Português (Moeda: R$ BRL)'
        };
        showToast('Success', msgs[lang], 'ri-translate-2');
    }
}

function updateLanguageUI() {
    const langLabels = {
        es: '🇪🇸 ES',
        en: '🇬🇧 EN',
        pt: '🇧🇷 PT'
    };
    const currentLabel = document.getElementById('current-lang-label');
    if (currentLabel) {
        currentLabel.innerText = langLabels[currentLang] || '🇪🇸 ES';
    }

    ['es', 'en', 'pt'].forEach(code => {
        const btn = document.getElementById('lang-' + code);
        if (btn) {
            const isActive = currentLang === code;
            btn.classList.toggle('text-primary', isActive);
            btn.classList.toggle('bg-indigo-50/70', isActive);
            btn.classList.toggle('text-slate-600', !isActive);
        }
    });

    // Initialize Currency Selector
    const currSelect = document.getElementById('currency-selector');
    if(currSelect && window.PriceEngine) {
        currSelect.value = window.PriceEngine.currentCurrency;
    }

    // Update static elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[currentLang] && translations[currentLang][key]) {
            el.innerText = translations[currentLang][key];
        }
    });
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
    if (items.length === 0) {
        showToast('Mochila vacía', 'Agrega primero una expedición o equipo a tu mochila.', 'ri-shopping-bag-3-line');
        return;
    }

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

async function confirmManualPayment() {
    const btn = document.getElementById('confirm-payment-btn');
    btn.disabled = true;
    btn.innerHTML = '<i class="ri-loader-4-line animate-spin text-xl"></i> Validando Operación...';

    const { items, total } = backpack.getState();
    const finalTotal = Math.round(total * 0.85);
    const amountToday = currentPaymentPlan === 'split' ? Math.round(finalTotal * 0.30) : finalTotal;
    const bookingCode = 'LX-' + Math.random().toString(36).substring(2, 8).toUpperCase();
    const tourNames = items.map(i => i.name).join(' + ') || 'Expedición Lifextreme';
    const tourDateStr = selectedTourDate ? formatDate(selectedTourDate) : formatDate(new Date(Date.now() + 86400000 * 15));

    // Sincronizar con Supabase & API Serverless en segundo plano sin bloquear UX
    try {
        if (typeof window.processBookingCusco === 'function') {
            window.processBookingCusco({
                tourId: String(items[0]?.id || 'LX-WEB'),
                tourName: tourNames,
                date: selectedTourDate ? selectedTourDate.toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
                pax: items.length || 1,
                price: amountToday,
                contact: {
                    name: localStorage.getItem('lifextreme_user_name') || 'Explorador Web',
                    email: localStorage.getItem('lifextreme_user_email') || 'contacto@lifextreme.store',
                    phone: '+51 958 050 928'
                }
            }).catch(() => {});
        }
        fetch('/api/send-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tipo: 'booking_confirmation',
                fullName: localStorage.getItem('lifextreme_user_name') || `Reserva Web (${bookingCode})`,
                email: localStorage.getItem('lifextreme_user_email') || 'contacto@lifextreme.store',
                phone: '+51 958 050 928',
                tourName: `${tourNames} [${currentPaymentPlan === 'split' ? 'Plan 30-30-40' : 'Pago 100%'}]`,
                date: tourDateStr,
                pax: items.length || 1
            })
        }).catch(() => {});
    } catch (err) {
        console.warn('Sync notice:', err);
    }

    setTimeout(() => {
        btn.innerHTML = `<i class="ri-checkbox-circle-fill text-xl"></i> ORDEN ${bookingCode} REGISTRADA`;

        const orderSummary = {
            bookingCode,
            plan: currentPaymentPlan,
            totalAmount: finalTotal,
            paidToday: amountToday,
            firstPaymentDate: new Date().toISOString(),
            tourDate: tourDateStr,
            items: items
        };
        localStorage.setItem('lifextreme_payment_plan', JSON.stringify(orderSummary));
        localStorage.setItem('lifextreme_last_order', JSON.stringify(orderSummary));

        if (currentPaymentPlan === 'split') {
            showToast(`Reserva ${bookingCode} Activa (30%)`, `Abono inicial S/ ${amountToday} registrado. Enviando voucher...`, 'ri-verified-badge-fill');
        } else {
            showToast(`Expedición ${bookingCode} Confirmada`, `Pago total S/ ${amountToday} registrado exitosamente.`, 'ri-verified-badge-fill');
        }

        const waMsg = encodeURIComponent(
            `¡Hola Lifextreme! Acabo de registrar mi reserva web.\n` +
            `• Código: *${bookingCode}*\n` +
            `• Expedición/Items: *${tourNames}*\n` +
            `• Fecha estimada: *${tourDateStr}*\n` +
            `• Modalidad: *${currentPaymentPlan === 'split' ? 'Reserva Fraccionada 30/30/40 (30% hoy)' : 'Pago Total 100%'}*\n` +
            `• Monto abonado hoy: *S/ ${amountToday}*\n` +
            `Adjunto mi constancia de operación para validación inmediata.`
        );

        setTimeout(() => {
            closeStripeCheckout();
            backpack.setState(state => ({ ...state, items: [], total: 0 }));
            localStorage.removeItem('lifextreme_backpack');
            updateCart();

            // Reset button state for next time
            btn.disabled = false;
            btn.innerHTML = 'Confirmar Pago Enviado';
            currentPaymentPlan = 'full';

            // Abrir confirmación directa con el centro de operaciones en WhatsApp
            window.open(`https://wa.me/51958050928?text=${waMsg}`, '_blank');
        }, 1200);
    }, 1200);
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

// --- MEMBERSHIP COUNTDOWN LOGIC ---
function startMembershipCountdown() {
    // 1. Set End Time (36 Hours from now or stored)
    const STORAGE_KEY = 'lifextreme_offer_end_time';
    let endTime = localStorage.getItem(STORAGE_KEY);

    if (!endTime) {
        const now = new Date();
        now.setHours(now.getHours() + 36);
        endTime = now.getTime();
        localStorage.setItem(STORAGE_KEY, endTime);
    }

    // 2. Timer Interval
    const timerInterval = setInterval(() => {
        const now = new Date().getTime();
        const distance = endTime - now;

        if (distance < 0) {
            clearInterval(timerInterval);
            document.getElementById('m-hours').innerText = "00";
            document.getElementById('m-minutes').innerText = "00";
            document.getElementById('m-seconds').innerText = "00";
            // Optional: Disable button or show "Expired"
            return;
        }

        const hours = Math.floor((distance % (1000 * 60 * 60 * 48)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        const hElem = document.getElementById('m-hours');
        if (hElem) hElem.innerText = hours < 10 ? "0" + hours : hours;

        const mElem = document.getElementById('m-minutes');
        if (mElem) mElem.innerText = minutes < 10 ? "0" + minutes : minutes;

        const sElem = document.getElementById('m-seconds');
        if (sElem) sElem.innerText = seconds < 10 ? "0" + seconds : seconds;

    }, 1000);


    // 3. Spots Counter (Simulate drops)
    // Decrement spots occasionally to create urgency
    let spots = 70;
    const spotsElem = document.getElementById('spots-counter');
    const spotsBar = document.getElementById('spots-bar');

    if (!spotsElem) return;

    // Retrieve stored spots if needed, but for visual effect lets restart or keep simple
    // A simple logic: drop 1 spot every X seconds randomly

    function updateSpots() {
        if (spots <= 12) return; // Stop at 12 to maintain scarcity but not 0

        spots--;
        spotsElem.innerText = spots;
        if (spotsBar) spotsBar.style.width = `${spots}%`;

        // Random next update between 10s and 40s
        setTimeout(updateSpots, Math.random() * 30000 + 10000);
    }

    setTimeout(updateSpots, 5000);
}

// Start everything
document.addEventListener('DOMContentLoaded', () => {
    startMembershipCountdown();
});
// --- FILTER & URL HANDLING ---
function filterDestinations(region) {
    renderAll(region);
    const destSection = document.getElementById('destinos');
    if (destSection) {
        destSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// Check URL params on load
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const region = params.get('region');
    // If region exists, capitalize first letter to match data (Cusco, Huaraz, etc if needed, or update renderAll to be case-insensitive)
    if (region) {
        // Simple capitalization
        const formattedRegion = region.charAt(0).toUpperCase() + region.slice(1).toLowerCase();
        // Wait a bit for data to load if needed, or call immediately if data is static
        // Assuming 'tours' data is available globally from data.js
        setTimeout(() => {
            filterDestinations(formattedRegion);
        }, 300); // Small delay to ensure renderAll is ready and DOM is parsed
    }
});

// --- V10 SEO DIRECTIVE: JSON-LD GENERATION ---
function injectStructuredData() {
    if (typeof tours === 'undefined') return;
    
    // Generate an ItemList of Tours
    const itemList = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": tours.map((tour, index) => {
            const item = {
                "@type": "TouristTrip",
                "name": tour.title,
                "description": tour.direct_answer_block || tour.detail,
                "touristType": [
                    "Adventure",
                    "Mountain"
                ],
                "offers": {
                    "@type": "Offer",
                    "price": tour.price,
                    "priceCurrency": "USD"
                }
            };
            if (tour.faqs && tour.faqs.length > 0) {
                item.subjectOf = {
                    "@type": "FAQPage",
                    "mainEntity": tour.faqs.map(faq => ({
                        "@type": "Question",
                        "name": faq.q,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": faq.a
                        }
                    }))
                };
            }
            return {
                "@type": "ListItem",
                "position": index + 1,
                "item": item
            };
        })
    };

    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(itemList);
    document.head.appendChild(script);
}

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(injectStructuredData, 1000); // Give it a slight delay to ensure tours are loaded
});

// ==========================================
// SEO DYNAMIC SCHEMA: @graph + Speakable + AEO
// ==========================================
window.injectTourSchema = function(toursList) {
    document.querySelectorAll('script[data-schema="tour"]').forEach(el => el.remove());
    
    toursList.forEach(t => {
        // Build FAQPage schema for this tour
        let faqSchema = [];
        if (t.faqs && t.faqs.length > 0) {
            faqSchema = t.faqs.map(faq => ({
                "@type": "Question",
                "name": faq.q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq.a
                }
            }));
        }

        const schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Organization",
                    "@id": "https://www.lifextreme.store/#organization",
                    "name": "Lifextreme Peru",
                    "url": "https://www.lifextreme.store",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "Cl. Chihuampata 626 - Barrio de San Blas",
                        "addressLocality": "Cusco",
                        "addressCountry": "PE"
                    },
                    "sameAs": [
                        "https://www.linkedin.com/company/lifextreme/",
                        "https://www.facebook.com/Lifextremeperu",
                        "https://www.instagram.com/lifextremeperu/",
                        "https://www.youtube.com/@lifextremeperu2780",
                        "https://tiktok.com/@lifextremeperu"
                    ]
                },
                {
                    "@type": "WebSite",
                    "@id": "https://www.lifextreme.store/#website",
                    "url": "https://www.lifextreme.store",
                    "name": "Lifextreme",
                    "dateModified": new Date(Date.now() - 86400000).toISOString().split('T')[0],
                    "publisher": { "@id": "https://www.lifextreme.store/#organization" },
                    "speakable": {
                        "@type": "SpeakableSpecification",
                        "cssSelector": [".faq-answer", "h3"]
                    }
                },
                {
                    "@type": ["TouristTrip", "Product"],
                    "@id": `https://www.lifextreme.store/#tour-${t.id}`,
                    "name": t.title,
                    "image": t.img,
                    "description": t.description || `Expedición de aventura en ${t.dept} por Lifextreme.`,
                    "dateModified": new Date(Date.now() - 86400000).toISOString().split('T')[0],
                    "brand": { "@id": "https://www.lifextreme.store/#organization" },
                    "offers": {
                        "@type": "Offer",
                        "price": t.price,
                        "priceCurrency": "PEN",
                        "availability": "https://schema.org/InStock",
                        "seller": { "@id": "https://www.lifextreme.store/#organization" }
                    }
                }
            ]
        };

        if (faqSchema.length > 0) {
            schema["@graph"].push({
                "@type": "FAQPage",
                "@id": `https://www.lifextreme.store/#faq-${t.id}`,
                "mainEntity": faqSchema,
                "isPartOf": { "@id": "https://www.lifextreme.store/#website" }
            });
        }

        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.setAttribute('data-schema', 'tour');
        script.textContent = JSON.stringify(schema);
        document.head.appendChild(script);
    });
};
