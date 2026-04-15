// ========================================
// LIFEXTREME AI PERSONALIZATION ENGINE (v3.0)
// ========================================

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
        this.isTyping = false;
        this.init();
    }

    init() {
        this.loadUserProfile();
        this.initChatbot();
        this.loadCommercialBrain();
        this.loadSalesDNA();
        this.loadKnowledgeBase();
    }

    loadUserProfile() {
        const profileData = localStorage.getItem('lifextreme_ai_profile');
        if (profileData) {
            this.userProfile = JSON.parse(profileData);
        }
    }

    initChatbot() {
        this.chatOpen = false;
        this.checkWelcomeBonus();
    }

    async loadCommercialBrain() {
        try {
            const response = await fetch('data/knowledge/max_commercial_brain.json');
            this.commercialBrain = await response.json();
        } catch (e) {
            console.warn('⚠️ MAX: Error loading commercial brain');
        }
    }

    async loadSalesDNA() {
        try {
            const response = await fetch('data/knowledge/max_sales_dna.json');
            this.salesDNA = await response.json();
        } catch (e) {
            console.warn('⚠️ MAX: Error loading sales DNA');
        }
    }

    async loadKnowledgeBase() {
        try {
            const response = await fetch('js/knowledge_base.json');
            const data = await response.json();
            this.knowledgeBase = data.data || [];
        } catch (e) {
            console.warn('⚠️ MAX: Error loading knowledge base');
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
            document.getElementById('life-input')?.focus();
        } else {
            windowEl.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
            windowEl.classList.add('opacity-0', 'scale-75', 'translate-y-4');
            setTimeout(() => { windowEl.classList.add('hidden'); }, 300);
        }
    }

    addUserMessage(text) {
        const container = document.getElementById('life-messages');
        const msgHtml = `<div class="flex justify-end animate-slideUp"><div class="chat-bubble-user p-4 max-w-[85%] text-xs font-medium shadow-md break-words">${text}</div></div>`;
        container.insertAdjacentHTML('beforeend', msgHtml);
        this.scrollToBottom();
    }

    personalizeResponse(text) {
        if (!text) return "";
        if (text.startsWith('{') || text.includes('🏔️') || text.includes('🧗')) return text;

        const prefixes = [
            "¡Escucha esto, aventurero! ",
            "Como especialista en las rutas del Cusco, te cuento: ",
            "¡Esa es la actitud de un explorador! Mi consejo experto es: ",
            "Desde mi experiencia técnica en Lifextreme: "
        ];
        const suffixes = [
            " ¡La montaña nos espera! 🏔️⚡",
            " ¿Listo para subir de nivel con Lifextreme? 🚀",
            " ¡Nos vemos en la ruta! 🧗",
            " ¡Adrenalina segura garantizada! 🔥"
        ];
        
        const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
        const suffix = suffixes[Math.floor(Math.random() * suffixes.length)];
        return `${prefix}${text}${suffix}`;
    }

    async addBotMessage(text) {
        if (this.isTyping) return;
        this.isTyping = true;
        this.hideTypingIndicator();
        
        const container = document.getElementById('life-messages');
        const botName = this.identity.name;
        const stylizedText = this.personalizeResponse(text);
        
        const msgId = 'bot-' + Date.now();
        const msgHtml = `
            <div class="flex gap-3 animate-slideUp">
                <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg flex-shrink-0">
                    <i class="ri-flashlight-fill text-white text-xl"></i>
                </div>
                <div class="flex flex-col gap-1 max-w-[85%]">
                    <span class="text-[9px] font-black uppercase tracking-widest text-slate-400 ml-1">${botName}</span>
                    <div id="${msgId}" class="chat-bubble-bot p-4 text-slate-700 text-xs font-medium leading-relaxed break-words shadow-sm border border-slate-100"></div>
                </div>
            </div>`;
        container.insertAdjacentHTML('beforeend', msgHtml);
        
        const bubble = document.getElementById(msgId);
        const chars = stylizedText.split('');
        let currentText = '';
        
        for (let i = 0; i < chars.length; i++) {
            currentText += chars[i];
            bubble.innerHTML = currentText.replace(/\n/g, '<br>');
            if (i % 5 === 0) this.scrollToBottom();
            await new Promise(r => setTimeout(r, Math.random() * 15 + 5));
        }
        
        this.isTyping = false;
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const container = document.getElementById('life-messages');
        const typingHtml = `<div id="typing-indicator" class="flex gap-3 animate-slideUp"><div class="p-3 bg-white rounded-2xl shadow-sm border border-slate-100 flex gap-1"><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce"></span><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.2s"></span><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.4s"></span></div></div>`;
        container.insertAdjacentHTML('beforeend', typingHtml);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        document.getElementById('typing-indicator')?.remove();
    }

    scrollToBottom() {
        const container = document.getElementById('life-messages');
        if (container) container.scrollTop = container.scrollHeight;
    }

    searchKnowledgeBase(query) {
        if (!this.knowledgeBase) return null;
        const normalizedQuery = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[¿?¡!.,;:]/g, '');
        const queryWords = normalizedQuery.split(/\s+/).filter(w => w.length > 2);
        if (queryWords.length === 0) return null;

        const stopwords = new Set(['que', 'como', 'para', 'por', 'con', 'del', 'los', 'las', 'una', 'uno', 'quisiera', 'quiero', 'informacion']);
        const meaningfulWords = queryWords.filter(w => !stopwords.has(w));
        
        let bestMatch = null; 
        let maxScore = 0;

        for (const faq of this.knowledgeBase) {
            const questionNormalized = faq.question.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            const answerNormalized = faq.answer.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            
            let score = 0;
            let matches = 0;

            for (const word of meaningfulWords) {
                if (questionNormalized.includes(word)) {
                    score += 15; // Mayor peso a la pregunta
                    matches++;
                }
                if (answerNormalized.includes(word)) {
                    score += 2;
                }
            }

            // Bono por frase exacta
            if (questionNormalized.includes(normalizedQuery)) score += 50;

            const hitRatio = matches / (meaningfulWords.length || 1);
            if (hitRatio < 0.5) score = 0; // Umbral de rigurosidad

            if (score > maxScore) {
                maxScore = score;
                bestMatch = faq;
            }
        }

        return (bestMatch && maxScore >= 20) ? bestMatch : null;
    }

    searchSalesDNA(query) {
        if (!this.salesDNA) return null;
        const normalizedQuery = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        let bestMatch = null;
        let bestScore = 0;

        for (const pattern of this.salesDNA) {
            const contextText = pattern.context.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            const queryWords = normalizedQuery.split(/\s+/).filter(w => w.length > 3);
            let matched = 0;
            for (const word of queryWords) {
                if (contextText.includes(word)) matched++;
            }
            const score = matched / (queryWords.length || 1);
            if (score > 0.7 && score > bestScore) {
                bestScore = score;
                bestMatch = pattern;
            }
        }
        return bestMatch;
    }

    async processUserMessage(msg) {
        if (this.isTyping) return;
        this.showTypingIndicator();
        
        const lowerMsg = msg.toLowerCase();

        // 1. ESPECIALISTA HARDCODED (Filtros de ADRENALINA)
        if (lowerMsg.includes('libro') || lowerMsg.includes('arqueologia')) {
            await this.addBotMessage("¡Interesante! Pero mi especialidad es la acción. Tipón es sublime para un trekking de aclimatación. ¡Olvida la teoría y vamos a la práctica! 🧗🏔️");
            return;
        }

        if (lowerMsg.includes('trekking') || lowerMsg.includes('caminata')) {
            await this.addBotMessage("Como experto en rutas de Cusco, te digo que el trekking es nuestra religión. Tenemos desde rutas clásicas hasta expediciones nivel PRO. ¿Buscas un reto de un día o una expedición total? 🏔️⚡");
            return;
        }

        // 2. KNOWLEDGE BASE
        const kbResult = this.searchKnowledgeBase(msg);
        if (kbResult) {
            await this.addBotMessage(kbResult.answer);
            return;
        }

        // 3. AGENTE HUB (Remote RAG) - Con control de CORS
        const HUB_URL = 'https://hub-cusco-2026.tail883d62.ts.net/webhook/lifextreme';
        try {
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 8000);
            const response = await fetch(HUB_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                mode: 'cors',
                body: JSON.stringify({ message: msg, context: this.userProfile || {} }),
                signal: controller.signal
            });
            clearTimeout(timeout);
            if (response.ok) {
                const data = await response.json();
                if (data.response || data.reply) {
                    await this.addBotMessage(data.response || data.reply);
                    return;
                }
            }
        } catch (e) {
            console.warn('⚠️ HUB Offline / CORS Blocked. Falling back to DNA.');
        }

        // 4. SALES DNA
        const dnaResult = this.searchSalesDNA(msg);
        if (dnaResult) {
            await this.addBotMessage(dnaResult.response);
            return;
        }

        // 5. FALLBACK
        await this.processContextualFallback(msg);
    }

    async processContextualFallback(msg) {
        const lower = msg.toLowerCase();
        if (lower.match(/hola|buenos|buenas/)) {
            let welcome = `Hola! Soy **${this.identity.name}**, tu Asesor de Aventuras! 🏔️⚡`;
            if (this.pendingBonus) {
                welcome += `\n\n¡Te he acreditado **30 LifeCoins** de regalo por tu interés en Lifextreme! 🎁`;
                this.grantWelcomeBonus();
            }
            welcome += `\n\n¿Qué ruta o actividad extrema te gustaría conquistar hoy?`;
            await this.addBotMessage(welcome);
            return;
        }

        await this.addBotMessage("Esa es una excelente consulta. He recorrido muchas rutas con el equipo, pero para darte la asesoría técnica exacta que garantice tu seguridad, lo mejor es hablar por WhatsApp con un guía humano. ¿Pasamos a WhatsApp? 🚀");
    }

    handleAction(val) {
        if (val.includes('WHATSAPP') || val.includes('PAOLO')) {
            window.open('https://wa.me/51958050928?text=Hola%20Lifextreme!%20Vengo%20del%20chat%20con%20MAX', '_blank');
        } else {
            this.processUserMessage(val);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.AIEngine = new AIPersonalizationEngine();
});
