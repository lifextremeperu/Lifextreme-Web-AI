// ========================================
// LIFEXTREME AI PERSONALIZATION ENGINE (v2.0)
// ========================================
// Motor de personalización y chatbot con arquitectura de 3 capas:
// 1. Knowledge Base Local (Browser) - Siempre Activo
// 2. HUB Tailscale (Local) - RAG Profundo
// 3. Fallback WhatsApp (Humano)

class AIPersonalizationEngine {
    constructor() {
        this.identity = {
            name: "MAX",
            origin: "Asesor Maestro de Aventura (Lifextreme PRO)",
            traits: ["Exciting", "Expert", "Safety-oriented", "Direct"]
        };
        this.commercialBrain = null;
        this.knowledgeBase = null;
        this.salesDNA = null;
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
        
        // Cargar Inteligencia Comercial
        this.loadCommercialBrain();
        this.loadSalesDNA();
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
        this.checkWelcomeBonus();
        setTimeout(() => { if (!this.chatOpen) this.showChatNotification(); }, 8000);
    }

    async loadCommercialBrain() {
        try {
            const response = await fetch('data/knowledge/max_commercial_brain.json');
            this.commercialBrain = await response.json();
            console.log('🧠 MAX: Cerebro comercial cargado', this.commercialBrain.identity.full_name);
        } catch (e) {
            console.warn('⚠️ MAX: No se pudo cargar el cerebro comercial', e);
        }
    }

    async loadSalesDNA() {
        try {
            const response = await fetch('data/knowledge/max_sales_dna.json');
            this.salesDNA = await response.json();
            console.log(`🧬 MAX: ADN de ventas cargado (${this.salesDNA.length} patrones)`);
        } catch (e) {
            console.warn('⚠️ MAX: No se pudo cargar el ADN de ventas', e);
        }
    }

    checkWelcomeBonus() {
        if (!localStorage.getItem('max_welcome_bonus_granted')) {
            this.pendingBonus = 30;
        }
    }

    grantWelcomeBonus() {
        if (this.pendingBonus) {
            localStorage.setItem('max_welcome_bonus_granted', 'true');
            // Simular actualización de LifeCoins en el perfil local si existe
            if (this.userProfile) {
                this.userProfile.rewards = (this.userProfile.rewards || 0) + 30;
                localStorage.setItem('lifextreme_ai_profile', JSON.stringify(this.userProfile));
            }
            this.pendingBonus = 0;
            return true;
        }
        return false;
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

    personalizeResponse(text) {
        if (!text) return "";
        // No personalizar si es una respuesta estructurada (JSON) o ya tiene emojis de aventura
        if (text.startsWith('{') || text.includes('🏔️') || text.includes('🧗')) return text;

        const prefixes = [
            "¡Escucha esto, aventurero! ",
            "Desde las rutas más extremas del Cusco: ",
            "¡Esa es la actitud! Mi consejo es: ",
            "Como tu asesor en Lifextreme, te digo: "
        ];
        const suffixes = [
            " ¡La adrenalina te espera! 🏔️⚡",
            " ¿Listo para el siguiente nivel? 🚀",
            " ¡Nos vemos en la cima! 🧗",
            " ¡Vive la experiencia real! 🔥"
        ];
        
        const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
        const suffix = suffixes[Math.floor(Math.random() * suffixes.length)];
        
        return `${prefix}${text}${suffix}`;
    }

    addBotMessage(text, actions = []) {
        this.hideTypingIndicator();
        const container = document.getElementById('life-messages');
        const botName = this.identity.name;
        
        // Aplicar la personalidad de MAX
        const stylizedText = this.personalizeResponse(text);

        let actionsHtml = '';
        if (actions.length > 0) {
            actionsHtml = `<div class="flex flex-wrap gap-2 mt-2">${actions.map(act => `<button onclick="window.AIEngine.handleAction('${act.val}')" class="bg-primary/10 text-primary hover:bg-primary hover:text-white px-4 py-2 rounded-xl text-[10px] font-black transition-all border border-primary/20">${act.label}</button>`).join('')}</div>`;
        }
        const msgHtml = `
            <div class="flex gap-3 animate-slideUp">
                <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg flex-shrink-0">
                    <i class="ri-flashlight-fill text-white text-xl"></i>
                </div>
                <div class="flex flex-col gap-1 max-w-[85%]">
                    <span class="text-[9px] font-black uppercase tracking-widest text-slate-400 ml-1">${botName}</span>
                    <div class="chat-bubble-bot p-4 text-slate-700 text-xs font-medium leading-relaxed break-words shadow-sm border border-slate-100">${stylizedText.replace(/\n/g, '<br>')}</div>
                    ${actionsHtml}
                </div>
            </div>`;
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

    searchSalesDNA(query) {
        if (!this.salesDNA || this.salesDNA.length === 0) return null;
        const normalizedQuery = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        
        let bestMatch = null; let bestScore = 0;
        for (const pattern of this.salesDNA) {
            const contextText = pattern.context.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            if (!contextText) continue;

            // Búsqueda por similitud básica (palabras clave compartidas)
            const queryWords = normalizedQuery.split(/\s+/).filter(w => w.length > 3);
            let matched = 0;
            for (const word of queryWords) {
                if (contextText.includes(word)) matched++;
            }
            
            const score = matched / (queryWords.length || 1);
            if (score > 0.6 && score > bestScore) {
                bestScore = score;
                bestMatch = pattern;
            }
        }
        return bestMatch;
    }

    async processUserMessage(msg) {
        if (!document.getElementById('typing-indicator')) this.showTypingIndicator();
        
        // Carga diferida de conocimientos si no existen
        await Promise.all([this.loadKnowledgeBase(), this.loadSalesDNA()]);

        const lowerMsg = msg.toLowerCase();

        // FILTRO DE PERSONALIDAD: Evitar respuestas puramente académicas
        const academicKeywords = ['libro', 'historia', 'arqueologia', 'enciclopedia', 'articulo'];
        if (academicKeywords.some(word => lowerMsg.includes(word)) && !lowerMsg.includes('tour') && !lowerMsg.includes('ruta')) {
            const redirectMsg = "¡Interesante dato! Pero en Lifextreme preferimos vivir la historia en lugar de solo leerla. Lugares como Tipón son brutales para una caminata de aclimatación. ¿Quieres que te muestre rutas extremas por esa zona? 🧗🏔️";
            setTimeout(() => {
                this.addBotMessage(redirectMsg, [{ label: '🏔️ Ver Rutas', val: 'Cusco' }]);
            }, 600);
            return;
        }

        // CAPA 1.1: FAQ Local
        const kbResult = this.searchKnowledgeBase(msg);
        if (kbResult) {
            setTimeout(() => {
                const actions = [{ label: '📋 Ver Tours', val: 'quiero ver tours disponibles' }, { label: '💬 WhatsApp', val: 'contactar whatsapp' }];
                this.addBotMessage(kbResult.answer, actions);
            }, 600);
            return;
        }

        // CAPA 1.2: ADN Comercial (Paolo Sales Style)
        const dnaResult = this.searchSalesDNA(msg);
        if (dnaResult) {
            setTimeout(() => {
                this.addBotMessage(dnaResult.response, [{ label: '📱 Más info por WhatsApp', val: 'OPEN_WHATSAPP' }]);
            }, 800);
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
        
        // GESTIÓN DE TRIGGERS COMERCIALES (Cerebro MAX)
        if (this.commercialBrain) {
            const units = this.commercialBrain.business_units;
            
            // 1. Inversionistas (VIP)
            if (units.partners.triggers.some(t => lower.includes(t)) && (lower.includes('invertir') || lower.includes('dinero'))) {
                const reply = `¡Excelente! Para temas de inversión y alianzas estratégicas, Paolo atiende estas consultas personalmente. ¿Te gustaría que te conecte a su WhatsApp personal ahora mismo?`;
                const actions = [{ label: '📞 Contactar a Paolo', val: 'CONNECT_PAOLO_INVESTOR' }, { label: '🏢 Ver Portal Partners', val: 'ver portal partners' }];
                this.addBotMessage(reply, actions);
                return;
            }

            // 2. Comunidad (Pagos/Ahorro)
            if (units.community.triggers.some(t => lower.includes(t))) {
                const reply = `En Lifextreme creemos en democratizar la aventura. Con nuestra "Comunidad Social", puedes unirte a expediciones existentes y dividir gastos. ¡Viaja más, paga menos! 🏔️`;
                const actions = [{ label: '👥 Ver Expediciones Sociales', val: 'quiero ver expediciones sociales' }];
                this.addBotMessage(reply, actions);
                return;
            }

            // 3. Recompensas (LifeCoins)
            if (units.rewards.triggers.some(t => lower.includes(t))) {
                const reply = `Nuestro sistema de LifeCoins premia tu fidelidad. ¡Recuerda que 1,000 LC equivalen a un descuento de $10! Puedes ganarlos refiriendo amigos o con check-ins diarios. 🚀`;
                const actions = [{ label: '💰 Ver mis Recompensas', val: 'recompensas' }];
                this.addBotMessage(reply, actions);
                return;
            }

            // 4. Regalos (Gift Cards)
            if (units.gifts.triggers.some(t => lower.includes(t))) {
                const reply = `¡Qué gran detalle! Nuestras Gift Cards digitales son perfectas para cumpleaños o aniversarios. Tú eliges el monto y el cumpleañero elige el destino. 🎁`;
                const actions = [{ label: '🎨 Diseñar Regalo', val: 'openGiftModal()' }];
                this.addBotMessage(reply, actions);
                return;
            }
        }

        let reply = 'Esa es una buena pregunta. He aprendido mucho de Paolo sobre el terreno, pero para detalles muy específicos, lo mejor es que hablemos por WhatsApp. ¿Te conecto?';
        let actions = [{ label: '📱 WhatsApp', val: 'OPEN_WHATSAPP' }, { label: '🏔️ Ver Tours', val: 'qué tours tienen' }];
        
        if (lower.match(/hola|buenos|buenas/)) {
            let welcome = `Hola! Soy **${this.identity.name}**, tu Asesor de Aventuras! 🏔️⚡`;
            if (this.pendingBonus) {
                welcome += `\n\n¡Por ser tu primera vez, te he acreditado **30 LifeCoins** de regalo! 🎁`;
                this.grantWelcomeBonus();
            }
            welcome += `\n\n¿Qué destino quieres explorar hoy?`;
            
            reply = welcome;
            actions = [{ label: '🏔️ Tours', val: 'tours disponibles' }, { label: '👥 Comunidad', val: 'qué es la comunidad' }, { label: '🎁 Regalar', val: 'quiero hacer un regalo' }];
        }
        
        if (msg === 'OPEN_WHATSAPP') {
            window.open('https://wa.me/51958050928?text=Hola%20Lifextreme!%20Vengo%20del%20chat%20con%20MAX', '_blank');
            reply = '¡Listo! WhatsApp abierto. 🚀';
            actions = [];
        }

        if (msg === 'CONNECT_PAOLO_INVESTOR') {
            window.open('https://wa.me/51958050928?text=Hola%20Paolo,%20vengo%20del%20chat%20con%20MAX.%20Me%20interesa%20invertir%20en%20Lifextreme.', '_blank');
            reply = 'Te he conectado con el canal VIP de Paolo. 💼';
            actions = [];
        }

        this.addBotMessage(reply, actions);
    }

    handleAction(val) {
        if (val === 'OPEN_WHATSAPP') {
            window.open('https://wa.me/51958050928?text=Hola%20Lifextreme!', '_blank');
            return;
        }
        if (val === 'CONNECT_PAOLO_INVESTOR') {
            window.open('https://wa.me/51958050928?text=Hola%20Paolo,%20quiero%20invertir%20en%20Lifextreme', '_blank');
            return;
        }
        if (val.includes('()')) {
            try { eval(val); } catch(e) { console.error('Error executing action:', val); }
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
    console.log('🤖 MAX: Asesor Maestro de Lifextreme (v3.0) Cargado');
});
