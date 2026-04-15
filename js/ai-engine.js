// ========================================
// LIFEXTREME AI PERSONALIZATION ENGINE (v2.0)
// ========================================
// Motor de personalización y chatbot con arquitectura de 3 capas:
// 1. Knowledge Base Local (Browser) - Siempre Activo
// 2. HUB Tailscale (Local) - RAG Profundo
// 3. Fallback WhatsApp (Humano)

class AIPersonalizationEngine {
    constructor() {
        this.userProfile = null;
        this.recommendations = [];
        this.personalizedContent = {};
        this.knowledgeBase = null;
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
        this.personalizeHeroSection();
        this.generateSmartRecommendations();
        this.applyDynamicPricing();
        this.personalizeMessaging();
        this.filterRelevantContent();
    }

    // ==========================================
    // 1. PERSONALIZACIÓN DEL HERO SECTION
    // ==========================================
    personalizeHeroSection() {
        if (!this.userProfile) return;
        const { personal, adventure, preferences } = this.userProfile;
        const firstName = personal.fullName.split(' ')[0];

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
        if (!this.userProfile || !window.tours) return;
        const { adventure, preferences } = this.userProfile;

        this.recommendations = window.tours.map(tour => {
            let score = 0;
            if (preferences.regions.includes(tour.dept.toLowerCase())) score += 30;
            
            const difficultyMatch = {
                beginner: ['Baja', 'Media'],
                intermediate: ['Media', 'Alta'],
                advanced: ['Alta', 'Extrema'],
                expert: ['Extrema']
            };
            if (difficultyMatch[adventure.experienceLevel]?.includes(tour.difficulty)) score += 25;

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

            return { ...tour, aiScore: score };
        });

        this.recommendations.sort((a, b) => b.aiScore - a.aiScore);
        this.displayRecommendations();
    }

    displayRecommendations() {
        const destinosSection = document.getElementById('section-destinos');
        if (!destinosSection || !this.userProfile) return;

        const firstName = this.userProfile.personal.fullName.split(' ')[0];
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
                <div class="grid md:grid-cols-3 gap-6">
                    ${this.recommendations.slice(0, 3).map(tour => `
                        <div class="bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all cursor-pointer group relative" data-action="open-booking" data-id="${tour.id}">
                            <div class="absolute top-4 right-4 z-10 bg-accent text-slate-900 px-3 py-1 rounded-full text-[8px] font-black uppercase">${tour.aiScore}% Match</div>
                            <div class="h-48 overflow-hidden relative bg-slate-100">
                                <img src="${tour.img}?w=400" loading="lazy" class="w-full h-full object-cover group-hover:scale-110 transition-all duration-700">
                            </div>
                            <div class="p-6">
                                <p class="text-[8px] font-black text-primary uppercase mb-2">${tour.dept}</p>
                                <h4 class="text-lg font-black italic mb-3 leading-tight">${tour.title}</h4>
                                <div class="flex justify-between items-center pt-4 border-t">
                                    <span class="text-xl font-black italic">S/ ${tour.price}</span>
                                    <i class="ri-arrow-right-line text-primary text-xl"></i>
                                </div>
                            </div>
                        </div>`).join('')}
                </div>
            </div>`;

        const container = destinosSection.querySelector('.container');
        const regionSelector = document.getElementById('region-selector');
        if (container && regionSelector) regionSelector.insertAdjacentHTML('afterend', recommendationsHTML);
    }

    applyDynamicPricing() {}
    personalizeMessaging() {}
    filterRelevantContent() {}

    getUserInsights() {
        if (!this.userProfile) return null;
        return {
            persona: this.generatePersona(),
            topRecommendations: this.recommendations.slice(0, 5),
            nextBestAction: this.suggestNextAction()
        };
    }

    generatePersona() {
        const { adventure, preferences } = this.userProfile;
        const key = `${adventure.experienceLevel}-${preferences.groupType}`;
        const personas = { 'beginner-family': '👨‍👩‍👧 Familia Exploradora' };
        return personas[key] || '🌟 Aventurero Único';
    }

    // ==========================================
    // LIFE AI CHATBOT CONTROLLER (FLOATING)
    // ==========================================

    initChatbot() {
        this.chatOpen = false;
        setTimeout(() => { if (!this.chatOpen) this.showChatNotification(); }, 8000);
    }

    toggleChat() {
        const windowEl = document.getElementById('life-chat-window');
        if (!windowEl) return;

        if (windowEl.classList.contains('hidden')) {
            windowEl.classList.remove('hidden');
            setTimeout(() => {
                windowEl.classList.remove('opacity-0', 'scale-75', 'translate-y-4');
                windowEl.classList.add('opacity-100', 'scale-100', 'translate-y-0');
            }, 10);
            const input = document.getElementById('life-input');
            if (input) input.focus();
        } else {
            windowEl.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
            windowEl.classList.add('opacity-0', 'scale-75', 'translate-y-4');
            setTimeout(() => { windowEl.classList.add('hidden'); }, 300);
        }
    }

    showChatNotification() {
        const badge = document.getElementById('life-badge');
        if (badge) { badge.classList.remove('hidden'); badge.classList.add('animate-bounce'); }
    }

    sendChatFromInput() {
        const input = document.getElementById('life-input');
        const msg = input.value.trim();
        if (!msg) return;
        this.addUserMessage(msg);
        input.value = '';
        this.processUserMessage(msg);
    }

    addUserMessage(text) {
        const container = document.getElementById('life-messages');
        const msgHtml = `<div class="flex justify-end animate-slideUp"><div class="chat-bubble-user p-4 max-w-[85%] text-xs font-medium shadow-md break-words">${text}</div></div>`;
        container.insertAdjacentHTML('beforeend', msgHtml);
        this.scrollToBottom();
    }

    addBotMessage(text, actions = []) {
        this.hideTypingIndicator();
        const container = document.getElementById('life-messages');
        let actionsHtml = '';
        if (actions.length > 0) {
            actionsHtml = `<div class="flex flex-wrap gap-2 mt-2">${actions.map(act => `<button onclick="window.AIEngine.handleAction('${act.val}')" class="bg-primary/10 text-primary hover:bg-primary hover:text-white px-4 py-2 rounded-xl text-[10px] font-black transition-all border border-primary/20">${act.label}</button>`).join('')}</div>`;
        }
        const msgHtml = `<div class="flex gap-3 animate-slideUp"><div class="w-10 h-10 rounded-2xl bg-white flex items-center justify-center border border-slate-100 shadow-sm flex-shrink-0"><i class="ri-flashlight-fill text-primary text-xl"></i></div><div class="flex flex-col gap-2 max-w-[85%]"><div class="chat-bubble-bot p-4 text-slate-700 text-xs font-medium leading-relaxed break-words">${text.replace(/\n/g, '<br>')}</div>${actionsHtml}</div></div>`;
        container.insertAdjacentHTML('beforeend', msgHtml);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const container = document.getElementById('life-messages');
        const typingHtml = `<div id="typing-indicator" class="flex gap-3 animate-slideUp"><div class="p-3 bg-white rounded-2xl shadow-sm border border-slate-100 flex gap-1"><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce"></span><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.2s"></span><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.4s"></span></div></div>`;
        container.insertAdjacentHTML('beforeend', typingHtml);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    scrollToBottom() {
        const container = document.getElementById('life-messages');
        if (container) container.scrollTop = container.scrollHeight;
    }

    // ==========================================
    // INTELIGENCIA LOCAL & CASCADA
    // ==========================================

    async loadKnowledgeBase() {
        if (this.knowledgeBase) return;
        try {
            const response = await fetch('js/knowledge_base.json');
            if (!response.ok) throw new Error('KB not found');
            const data = await response.json();
            this.knowledgeBase = data.data || [];
            console.log(`📚 Knowledge Base cargada: ${this.knowledgeBase.length} FAQs`);
        } catch (e) {
            console.warn('⚠️ Fallo carga KB:', e);
            this.knowledgeBase = [];
        }
    }

    searchKnowledgeBase(query) {
        if (!this.knowledgeBase || this.knowledgeBase.length === 0) return null;
        const normalizedQuery = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[¿?¡!.,;:]/g, '');
        const queryWords = normalizedQuery.split(/\s+/).filter(w => w.length > 2);
        if (queryWords.length === 0) return null;

        const stopwords = new Set(['que', 'como', 'para', 'por', 'con', 'del', 'los', 'las', 'una', 'uno']);
        const meaningfulWords = queryWords.filter(w => !stopwords.has(w));
        if (meaningfulWords.length === 0) return null;

        let bestMatch = null; let bestScore = 0;
        for (const faq of this.knowledgeBase) {
            const faqText = (faq.question + ' ' + faq.answer).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            let score = 0; let matchedWords = 0;
            for (const word of meaningfulWords) {
                if (faqText.includes(word)) {
                    matchedWords++;
                    if (faq.question.toLowerCase().includes(word)) score += 3; else score += 1;
                }
            }
            const matchRatio = matchedWords / meaningfulWords.length;
            if (matchRatio >= 0.4 && score > bestScore) { bestScore = score; bestMatch = faq; }
        }
        return (bestMatch && bestScore >= 2) ? bestMatch : null;
    }

    async processUserMessage(msg) {
        if (!document.getElementById('typing-indicator')) this.showTypingIndicator();
        await this.loadKnowledgeBase();

        // CAPA 1: Local KB
        const kbResult = this.searchKnowledgeBase(msg);
        if (kbResult) {
            setTimeout(() => {
                const actions = [{ label: '📋 Ver Tours', val: 'quiero ver tours disponibles' }, { label: '💬 WhatsApp', val: 'contactar whatsapp' }];
                this.addBotMessage(kbResult.answer, actions);
            }, 600);
            return;
        }

        // CAPA 2: HUB Local (Tailscale)
        const HUB_URL = 'https://hub-cusco-2026.tail883d62.ts.net/webhook/lifextreme';
        try {
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 5000);
            const response = await fetch(HUB_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg, context: this.userProfile || {} }),
                signal: controller.signal
            });
            clearTimeout(timeout);
            if (!response.ok) throw new Error('HUB Offline');
            const data = await response.json();
            this.addBotMessage(data.response || data.reply);
            return;
        } catch (error) {
            console.warn('⚠️ HUB Offline, usando Fallback.');
        }

        // CAPA 3: Fallback Contextual
        setTimeout(() => this.processContextualFallback(msg), 800);
    }

    processContextualFallback(msg) {
        const lower = msg.toLowerCase();
        let reply = 'Esa es una buena pregunta. Para darte la mejor respuesta, te recomiendo contactar a nuestro equipo directamente por WhatsApp. ¿Deseas que te conecte ahora?';
        let actions = [{ label: '📱 WhatsApp', val: 'OPEN_WHATSAPP' }, { label: '🏔️ Ver Tours', val: 'qué tours tienen' }];
        
        if (lower.match(/hola|buenos|buenas/)) {
            reply = '¡Hola! 👋 Soy Life, tu asistente de Lifextreme. ¿En qué aventura puedo ayudarte hoy?';
            actions = [{ label: '🏔️ Tours', val: 'tours disponibles' }, { label: '💰 Precios', val: 'cuánto cuestan' }];
        }
        
        if (msg === 'OPEN_WHATSAPP') {
            window.open('https://wa.me/51958050928?text=Hola%20Lifextreme!%20Quisiera%20información', '_blank');
            reply = '¡Listo! WhatsApp abierto. 🚀';
            actions = [];
        }
        this.addBotMessage(reply, actions);
    }

    handleAction(val) {
        if (val === 'OPEN_WHATSAPP') {
            window.open('https://wa.me/51958050928?text=Hola%20Lifextreme!', '_blank');
            return;
        }
        this.addUserMessage(val);
        this.processUserMessage(val);
    }

    suggestNextAction() { return null; }
}

// INICIALIZACIÓN
document.addEventListener('DOMContentLoaded', () => {
    window.AIEngine = new AIPersonalizationEngine();
    console.log('🤖 Lifextreme AI Engine v2.0 (Always Active) Cargado');
});
