// ========================================
// LIFEXTREME AI PERSONALIZATION ENGINE
// ========================================
// Motor de personalización que adapta toda la experiencia
// del usuario basándose en su perfil psicográfico y preferencias

class AIPersonalizationEngine {
    constructor() {
        this.userProfile = null;
        this.recommendations = [];
        this.personalizedContent = {};
        this.init();
    }

    init() {
        // Cargar perfil del usuario
        this.loadUserProfile();

        // Si existe perfil, activar personalización
        if (this.userProfile) {
            this.activatePersonalization();
        }

        // Init Floating Chatbot
        this.initChatbot();
    }

    loadUserProfile() {
        const profileData = localStorage.getItem('lifextreme_ai_profile');
        if (profileData) {
            this.userProfile = JSON.parse(profileData);
            console.log('🤖 AI Engine: Perfil de usuario cargado', this.userProfile);
        }
    }

    activatePersonalization() {
        console.log('🚀 AI Engine: Activando personalización completa...');

        // 1. Personalizar Hero Section
        this.personalizeHeroSection();

        // 2. Generar recomendaciones inteligentes
        this.generateSmartRecommendations();

        // 3. Ajustar precios dinámicos
        this.applyDynamicPricing();

        // 4. Personalizar mensajes
        this.personalizeMessaging();

        // 5. Filtrar contenido relevante
        this.filterRelevantContent();
    }

    // ==========================================
    // 1. PERSONALIZACIÓN DEL HERO SECTION
    // ==========================================
    personalizeHeroSection() {
        const { personal, adventure, preferences } = this.userProfile;
        const firstName = personal.fullName.split(' ')[0];

        // Cambiar título del hero basado en nivel de experiencia
        const heroTitle = document.querySelector('[data-i18n="hero_title_2"]');
        const heroDesc = document.querySelector('[data-i18n="hero_desc"]');

        if (heroTitle && heroDesc) {
            const experienceMessages = {
                beginner: {
                    title: `${firstName}, Inicia tu Aventura`,
                    desc: `Hemos seleccionado rutas perfectas para principiantes en ${preferences.regions.join(', ')}. Guías expertos te acompañarán en cada paso.`
                },
                intermediate: {
                    title: `${firstName}, Desafía tus Límites`,
                    desc: `Basado en tu experiencia, te recomendamos expediciones de nivel medio-alto con ${adventure.interests.join(', ')}.`
                },
                advanced: {
                    title: `${firstName}, Conquista lo Extremo`,
                    desc: `Rutas técnicas y desafiantes esperan por ti. Tu perfil indica que buscas adrenalina pura.`
                },
                expert: {
                    title: `${firstName}, Territorio Elite`,
                    desc: `Expediciones exclusivas para expertos. Accede a rutas no convencionales y experiencias únicas.`
                }
            };

            const message = experienceMessages[adventure.experienceLevel] || experienceMessages.beginner;
            heroTitle.textContent = message.title;
            heroDesc.textContent = message.desc;
        }

        // Agregar badge personalizado
        const heroTag = document.querySelector('[data-i18n="hero_tag"]');
        if (heroTag) {
            const budgetBadges = {
                budget: '💰 Aventuras Accesibles',
                moderate: '⭐ Experiencias Premium',
                premium: '💎 Lujo Aventurero',
                luxury: '👑 Elite Exclusivo'
            };
            heroTag.textContent = budgetBadges[adventure.budget] || heroTag.textContent;
        }
    }

    // ==========================================
    // 2. RECOMENDACIONES INTELIGENTES
    // ==========================================
    generateSmartRecommendations() {
        const { adventure, preferences } = this.userProfile;

        // Scoring algorithm para cada tour
        this.recommendations = window.tours.map(tour => {
            let score = 0;

            // +30 puntos si coincide con región de interés
            if (preferences.regions.includes(tour.dept.toLowerCase())) {
                score += 30;
            }

            // +25 puntos por nivel de dificultad apropiado
            const difficultyMatch = {
                beginner: ['Baja', 'Media'],
                intermediate: ['Media', 'Alta'],
                advanced: ['Alta', 'Extrema'],
                expert: ['Extrema']
            };
            if (difficultyMatch[adventure.experienceLevel]?.includes(tour.difficulty)) {
                score += 25;
            }

            // +20 puntos por intereses (análisis de keywords en título/detalle)
            adventure.interests.forEach(interest => {
                const keywords = {
                    trekking: ['trek', 'camino', 'caminata', 'trail'],
                    climbing: ['escalada', 'climbing', 'ascenso'],
                    jungle: ['selva', 'jungle', 'amazonas'],
                    cycling: ['bici', 'cycling', 'bike'],
                    water: ['río', 'rafting', 'kayak'],
                    camping: ['camping', 'acampar']
                };

                const searchText = (tour.title + tour.detail).toLowerCase();
                keywords[interest]?.forEach(keyword => {
                    if (searchText.includes(keyword)) score += 20;
                });
            });

            // +15 puntos por presupuesto apropiado
            const budgetRanges = {
                budget: [0, 1000],
                moderate: [1000, 2500],
                premium: [2500, 5000],
                luxury: [5000, Infinity]
            };
            const [min, max] = budgetRanges[adventure.budget] || [0, Infinity];
            if (tour.price >= min && tour.price <= max) {
                score += 15;
            }

            // +10 puntos por tipo de grupo (análisis de duración)
            if (preferences.groupType === 'family' && tour.difficulty === 'Baja') {
                score += 10;
            }
            if (preferences.groupType === 'solo' && tour.duration.includes('1 día')) {
                score += 10;
            }

            return { ...tour, aiScore: score };
        });

        // Ordenar por score
        this.recommendations.sort((a, b) => b.aiScore - a.aiScore);

        console.log('🎯 Top 5 Recomendaciones IA:', this.recommendations.slice(0, 5).map(t => ({
            title: t.title,
            score: t.aiScore
        })));

        // Mostrar recomendaciones en la UI
        this.displayRecommendations();
    }

    displayRecommendations() {
        // Crear sección de recomendaciones personalizadas
        const destinosSection = document.getElementById('section-destinos');
        if (!destinosSection) return;

        const firstName = this.userProfile.personal.fullName.split(' ')[0];

        // Insertar antes del grid de destinos
        const recommendationsHTML = `
            <div class="mb-12 bg-gradient-to-r from-primary/5 to-secondary/5 rounded-[48px] p-8 lg:p-12 border-2 border-primary/20">
                <div class="flex items-center gap-4 mb-6">
                    <div class="w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-2xl flex items-center justify-center">
                        <i class="ri-sparkling-2-fill text-white text-3xl"></i>
                    </div>
                    <div>
                        <h3 class="text-2xl font-black italic">Recomendado para ti, ${firstName}</h3>
                        <p class="text-xs font-bold text-slate-500">Basado en tu perfil de aventurero ${this.userProfile.adventure.experienceLevel}</p>
                    </div>
                </div>
                
                <div class="grid md:grid-cols-3 gap-6" id="ai-recommendations-grid">
                    ${this.recommendations.slice(0, 3).map((tour, i) => `
                        <div class="bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all cursor-pointer group relative" data-action="open-booking" data-id="${tour.id}">
                            <div class="absolute top-4 right-4 z-10 bg-accent text-slate-900 px-3 py-1 rounded-full text-[8px] font-black uppercase">
                                ${tour.aiScore}% Match
                            </div>
                            <div class="h-48 overflow-hidden relative bg-slate-100">
                                <div class="skeleton-loader absolute inset-0"></div>
                                <img src="${tour.img}?w=400" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition-all duration-700 img-reveal" onload="this.classList.add('loaded'); this.previousElementSibling.style.display='none';">
                            </div>
                            <div class="p-6">
                                <p class="text-[8px] font-black text-primary uppercase mb-2">${tour.dept}</p>
                                <h4 class="text-lg font-black italic mb-3 leading-tight">${tour.title}</h4>
                                <div class="flex justify-between items-center pt-4 border-t">
                                    <span class="text-xl font-black italic">S/ ${tour.price}</span>
                                    <i class="ri-arrow-right-line text-primary text-xl"></i>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        const container = destinosSection.querySelector('.container');
        const regionSelector = document.getElementById('region-selector');
        if (container && regionSelector) {
            regionSelector.insertAdjacentHTML('afterend', recommendationsHTML);
        }
    }

    // ==========================================
    // 3. PRECIOS DINÁMICOS
    // ==========================================
    applyDynamicPricing() {
        const { adventure } = this.userProfile;

        // Descuentos basados en frecuencia de viaje
        const frequencyDiscounts = {
            monthly: 0.15,    // 15% descuento
            quarterly: 0.10,  // 10% descuento
            biannual: 0.05,   // 5% descuento
            annual: 0.03      // 3% descuento
        };

        const discount = frequencyDiscounts[adventure.travelFrequency] || 0;

        if (discount > 0) {
            // Guardar descuento personalizado
            localStorage.setItem('lifextreme_ai_discount', discount.toString());

            console.log(`💰 Descuento IA aplicado: ${discount * 100}% por frecuencia ${adventure.travelFrequency}`);
        }
    }

    // ==========================================
    // 4. MENSAJES PERSONALIZADOS
    // ==========================================
    personalizeMessaging() {
        const { personal, preferences } = this.userProfile;
        const firstName = personal.fullName.split(' ')[0];

        // Personalizar mensajes del chatbot
        if (window.sendCompactChat) {
            // Inyectar mensaje de bienvenida personalizado
            setTimeout(() => {
                const motivationKeywords = preferences.motivation?.toLowerCase() || '';
                let personalizedMessage = `¡Hola ${firstName}! 👋 `;

                if (motivationKeywords.includes('desconectar')) {
                    personalizedMessage += 'Veo que buscas desconectar. Te recomiendo nuestras rutas de bienestar en la selva.';
                } else if (motivationKeywords.includes('límites') || motivationKeywords.includes('superar')) {
                    personalizedMessage += 'Perfecto para alguien que busca superar límites. Tengo rutas extremas que te encantarán.';
                } else if (motivationKeywords.includes('naturaleza')) {
                    personalizedMessage += 'Conectar con la naturaleza es nuestra especialidad. Mira estas opciones eco-friendly.';
                } else {
                    personalizedMessage += `He preparado ${this.recommendations.length} aventuras perfectas para tu perfil.`;
                }

                console.log('💬 Mensaje personalizado:', personalizedMessage);
            }, 1000);
        }
    }

    // ==========================================
    // 5. FILTRADO DE CONTENIDO RELEVANTE
    // ==========================================
    filterRelevantContent() {
        const { adventure, preferences } = this.userProfile;

        // Auto-filtrar por región preferida al cargar "Destinos"
        if (preferences.regions.length > 0) {
            const primaryRegion = preferences.regions[0];
            console.log(`🎯 Auto-filtrando por región preferida: ${primaryRegion}`);

            // Guardar preferencia de filtro
            localStorage.setItem('lifextreme_preferred_region', primaryRegion);
        }

        // Ocultar tours no aptos según experiencia
        const unsuitableFilters = {
            beginner: ['Extrema'],
            intermediate: [],
            advanced: [],
            expert: []
        };

        const hideDifficulties = unsuitableFilters[adventure.experienceLevel] || [];
        if (hideDifficulties.length > 0) {
            console.log(`⚠️ Ocultando tours de dificultad: ${hideDifficulties.join(', ')}`);
        }
    }

    // ==========================================
    // UTILIDADES PÚBLICAS
    // ==========================================
    getUserInsights() {
        if (!this.userProfile) return null;

        return {
            persona: this.generatePersona(),
            topRecommendations: this.recommendations.slice(0, 5),
            preferredBudget: this.userProfile.adventure.budget,
            travelStyle: this.analyzeTravelStyle(),
            nextBestAction: this.suggestNextAction()
        };
    }

    generatePersona() {
        const { adventure, preferences } = this.userProfile;

        const personas = {
            'beginner-family': '👨‍👩‍👧 Familia Exploradora',
            'beginner-solo': '🎒 Aventurero Novato',
            'intermediate-friends': '🤝 Grupo de Amigos Activos',
            'advanced-solo': '⛰️ Montañista Solitario',
            'expert-solo': '🏔️ Alpinista Elite',
            'expert-couple': '💑 Pareja Extrema'
        };

        const key = `${adventure.experienceLevel}-${preferences.groupType}`;
        return personas[key] || '🌟 Aventurero Único';
    }

    analyzeTravelStyle() {
        const { adventure } = this.userProfile;

        if (adventure.interests.includes('camping') && adventure.budget === 'budget') {
            return 'Mochilero Económico';
        }
        if (adventure.interests.length >= 4 && adventure.travelFrequency === 'monthly') {
            return 'Aventurero Full-Time';
        }
        if (adventure.budget === 'luxury' && adventure.experienceLevel === 'expert') {
            return 'Elite Expedicionario';
        }

        return 'Explorador Versátil';
    }

    // ==========================================
    // 6. LIFE AI CHATBOT CONTROLLER (FLOATING)
    // ==========================================

    initChatbot() {
        this.chatOpen = false;
        this.chatInitialized = false;

        // Timeout para invitar a la interacción si no hya actividad
        setTimeout(() => {
            if (!this.chatOpen) {
                this.showChatNotification();
            }
        }, 8000);
    }

    toggleChat() {
        this.chatOpen = !this.chatOpen;
        const windowEl = document.getElementById('life-window');
        const badge = document.getElementById('life-badge');

        if (this.chatOpen) {
            // OPEN
            windowEl.classList.remove('hidden');
            // Small delay to allow display:block to apply before opacity transition
            setTimeout(() => {
                windowEl.classList.remove('opacity-0', 'scale-75', 'translate-y-4');
            }, 10);

            // Hide badge
            if (badge) badge.style.transform = 'scale(0)';

            // Init conversation if empty
            if (!this.chatInitialized) {
                this.addBotMessage(`¡Hola! Soy Life, tu asesor de aventuras. 🏔️\n¿Buscas algo extremo o relajante para hoy?`);
                this.chatInitialized = true;
            }
        } else {
            // CLOSE
            windowEl.classList.add('opacity-0', 'scale-75', 'translate-y-4');
            setTimeout(() => {
                windowEl.classList.add('hidden');
            }, 500); // Wait for transition
        }
    }

    showChatNotification() {
        const badge = document.getElementById('life-badge');
        if (badge) {
            badge.style.transform = 'scale(1)';
            badge.classList.add('animate-bounce');
            // Optional: sound effect could go here
        }
    }

    sendChatFromInput() {
        const input = document.getElementById('life-input');
        const msg = input.value.trim();
        if (!msg) return;

        // User Message
        this.addUserMessage(msg);
        input.value = '';

        // Simulate thinking and reply
        this.showTypingIndicator();

        setTimeout(() => {
            this.processUserMessage(msg);
        }, 1500);
    }

    addUserMessage(text) {
        const container = document.getElementById('life-messages');
        const msgHtml = `
            <div class="flex justify-end animate-slideUp">
                <div class="bg-slate-900 text-white p-3 rounded-2xl rounded-tr-sm max-w-[85%] text-xs font-medium shadow-md">
                    ${text}
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', msgHtml);
        this.scrollToBottom();
    }

    addBotMessage(text, actions = []) {
        this.hideTypingIndicator();
        const container = document.getElementById('life-messages');

        let actionsHtml = '';
        if (actions.length > 0) {
            actionsHtml = `<div class="flex flex-wrap gap-2 mt-2">
                ${actions.map(act => `<button onclick="window.AIEngine.handleAction('${act.val}')" class="bg-indigo-50 text-indigo-700 hover:bg-indigo-100 px-3 py-2 rounded-xl text-[10px] font-bold transition-colors">${act.label}</button>`).join('')}
            </div>`;
        }

        const msgHtml = `
            <div class="flex gap-3 animate-slideUp">
                <div class="w-8 h-8 rounded-xl bg-white flex items-center justify-center border border-slate-100 shadow-sm flex-shrink-0">
                    <i class="ri-flashlight-fill text-primary text-sm"></i>
                </div>
                <div class="flex flex-col gap-1 max-w-[85%]">
                    <div class="bg-white p-3 rounded-2xl rounded-tl-sm text-slate-700 text-xs font-medium shadow-sm border border-slate-100">
                        ${text.replace(/\n/g, '<br>')}
                    </div>
                    ${actionsHtml}
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', msgHtml);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const container = document.getElementById('life-messages');
        const typingHtml = `
            <div id="typing-indicator" class="flex gap-3 animate-slideUp">
                <div class="w-8 h-8 rounded-xl bg-white flex items-center justify-center border border-slate-100 shadow-sm flex-shrink-0">
                    <i class="ri-flashlight-fill text-primary text-sm"></i>
                </div>
                <div class="bg-white p-3 rounded-2xl rounded-tl-sm text-slate-400 text-xs font-medium shadow-sm border border-slate-100 flex gap-1 items-center">
                    <span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce"></span>
                    <span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
                    <span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', typingHtml);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    scrollToBottom() {
        const container = document.getElementById('life-messages');
        container.scrollTop = container.scrollHeight;
    }

    // Logic to process intent (Mock NLP)
    processUserMessage(msg) {
        msg = msg.toLowerCase();

        let reply = "Interesante... Cuéntame más sobre qué tipo de experiencia buscas.";
        let actions = [];

        if (msg.includes('hola') || msg.includes('buen')) {
            reply = "¡Hola viajero! 👋 Estoy analizando las condiciones actuales en Cusco. ¿Te interesa montaña 🏔️, selva 🌴 o cultura 🏺?";
            actions = [
                { label: 'Montaña', val: 'montaña' },
                { label: 'Selva', val: 'selva' },
                { label: 'Cultura', val: 'cultura' }
            ];
        } else if (msg.includes('precio') || msg.includes('costo')) {
            reply = "Los precios varían según la complejidad de la expedición. Tengo opciones desde S/ 150 para fulldays hasta expediciones premium de varios días. ¿Cuál es tu presupuesto aproximado?";
        } else if (msg.includes('montaña') || msg.includes('trek')) {
            reply = "¡Excelente elección! 🏔️ Para montaña, el Salkantay Trek y la Montaña de 7 Colores están en condiciones óptimas esta semana. ¿Prefieres un reto físico alto o algo más moderado?";
            actions = [
                { label: 'Alto (Reto)', val: 'alto' },
                { label: 'Moderado (Disfrute)', val: 'moderado' }
            ];
        } else if (msg.includes('selva')) {
            reply = "La selva es mágica. 🌴 Te recomiendo Manu o Tambopata. Manu es más salvaje y biodiversa, Tambopata es más accesible. ¿Cuál te suena mejor?";
        } else {
            reply = "Entiendo. Puedo ayudarte a armar un itinerario a medida. ¿Cuántos días planeas quedarte en Cusco?";
        }

        this.addBotMessage(reply, actions);
    }

    handleAction(val) {
        this.addUserMessage(val); // Treat button click as user message
        this.showTypingIndicator();
        setTimeout(() => this.processUserMessage(val), 1000);
    }

    suggestNextAction() {
        const topTour = this.recommendations[0];
        return {
            action: 'open-booking',
            tourId: topTour.id,
            message: `Te recomendamos reservar "${topTour.title}" - ${topTour.aiScore}% compatible con tu perfil`,
            urgency: topTour.aiScore > 80 ? 'high' : 'medium'
        };
    }
}

// ==========================================
// INICIALIZACIÓN GLOBAL
// ==========================================
window.AIEngine = new AIPersonalizationEngine();

// Exponer insights para debugging
window.getAIInsights = () => window.AIEngine.getUserInsights();

console.log('🤖 Lifextreme AI Personalization Engine v1.0 Cargado');
