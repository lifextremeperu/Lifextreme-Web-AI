// ========================================
// LIFEXTREME AI PERSONALIZATION ENGINE (v3.5 - AMBASSADOR MODE)
// ========================================

class AIPersonalizationEngine {
    constructor() {
        this.identity = {
            name: "MAX",
            origin: "Asesor Maestro de Aventura (Lifextreme PRO)",
            full_name: "Asesor de Aventura en Perú",
            traits: ["Exciting", "Expert", "Safety-oriented", "Direct"]
        };
        
        this.kbPath = 'data/knowledge/lifextreme/knowledge_base.json';
        this.salesDnaPath = 'data/knowledge/max_sales_dna.json';
        this.commercialPath = 'data/knowledge/max_commercial_brain.json';
        
        this.knowledgeBase = null;
        this.salesDNA = null;
        this.commercialBrain = null;
        this.isTyping = false;
        this.pendingBonus = 30; 
        
        this.init();
    }

    async init() {
        this.loadUserProfile();
        try {
            const [kb, dna, comm] = await Promise.all([
                fetch(this.kbPath).then(r => r.json()).catch(() => ({ data: [] })),
                fetch(this.salesDnaPath).then(r => r.json()).catch(() => []),
                fetch(this.commercialPath).then(r => r.json()).catch(() => null)
            ]);
            
            this.knowledgeBase = kb.data || [];
            this.salesDNA = dna;
            this.commercialBrain = comm;
            
            console.log(`🧠 MAX: Embajador Cargado (${this.knowledgeBase.length} FAQs)`);
        } catch (e) {
            console.error('❌ Error en motores de IA:', e);
        }
    }

    loadUserProfile() {
        const profileData = localStorage.getItem('lifextreme_ai_profile');
        if (profileData) {
            this.userProfile = JSON.parse(profileData);
        } else {
            this.userProfile = { rewards: 0, interactions: 0 };
        }
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

    sendChatFromInput() {
        const input = document.getElementById('life-input');
        const msg = input.value.trim();
        if (!msg || this.isTyping) return;
        
        this.addUserMessage(msg);
        input.value = '';
        this.processUserMessage(msg);
    }

    addUserMessage(text) {
        const container = document.getElementById('life-messages');
        const msgHtml = `<div class="flex justify-end animate-slideUp mb-4"><div class="chat-bubble-user p-4 max-w-[85%] text-xs font-medium shadow-md break-words bg-primary text-white rounded-2xl rounded-tr-none">${text}</div></div>`;
        container.insertAdjacentHTML('beforeend', msgHtml);
        this.scrollToBottom();
    }

    personalizeResponse(text) {
        if (!text) return "";
        // Don't double-wrap if already processed
        if (text.includes('🏔️') || text.includes('🧗') || text.includes('⚡')) return text;

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
        this.isTyping = true;
        this.hideTypingIndicator();
        
        const container = document.getElementById('life-messages');
        const botName = this.identity.name;
        const stylizedText = this.personalizeResponse(text);
        
        const msgId = 'bot-' + Date.now();
        const msgHtml = `
            <div class="flex gap-3 animate-slideUp mb-4">
                <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg flex-shrink-0">
                    <i class="ri-flashlight-fill text-white text-xl"></i>
                </div>
                <div class="flex flex-col gap-1 max-w-[85%]">
                    <span class="text-[9px] font-black uppercase tracking-widest text-slate-400 ml-1">${botName}</span>
                    <div id="${msgId}" class="chat-bubble-bot p-4 text-slate-700 text-xs font-medium leading-relaxed break-words shadow-sm border border-slate-100 bg-[#f8fafc] rounded-2xl rounded-tl-none"></div>
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
            await new Promise(r => setTimeout(r, Math.random() * 5 + 2)); 
        }
        
        this.isTyping = false;
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const container = document.getElementById('life-messages');
        const typingHtml = `<div id="typing-indicator" class="flex gap-3 animate-slideUp mb-4"><div class="p-3 bg-white rounded-2xl shadow-sm border border-slate-100 flex gap-1"><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce"></span><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.2s"></span><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.4s"></span></div></div>`;
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

    searchCommercialTriggers(query) {
        if (!this.commercialBrain) return null;
        const normalized = query.toLowerCase();
        
        const triggers = {
            community: ["barato", "descuento", "precio", "cuanto cuesta", "economico", "grupo"],
            rewards: ["ganar", "puntos", "lifecoins", "beneficio", "gratis"],
            gifts: ["regalo", "cumpleaños", "sorpresa", "gift card"],
            partners: ["socio", "agencia", "negocio", "invertir", "trabajar"]
        };

        for (const [key, patterns] of Object.entries(triggers)) {
            if (patterns.some(p => normalized.includes(p))) {
                return { key, ...this.commercialBrain.business_units[key] };
            }
        }
        return null;
    }

    searchKnowledgeBase(query) {
        if (!this.knowledgeBase || this.knowledgeBase.length === 0) return null;
        
        const normalizedQuery = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[¿?¡!.,;:]/g, '');
        const queryWords = normalizedQuery.split(/\s+/).filter(w => w.length > 2);
        
        let bestMatch = null; 
        let maxScore = 0;

        for (const faq of this.knowledgeBase) {
            const questionNorm = faq.question.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            
            let score = 0;
            let matches = 0;

            for (const word of queryWords) {
                if (questionNorm.includes(word)) {
                    score += 20;
                    matches++;
                }
            }

            // Exatc match bonus
            if (questionNorm.includes(normalizedQuery)) score += 100;

            const hitRatio = matches / (queryWords.length || 1);
            if (hitRatio < 0.45) score = 0;

            if (score > maxScore) {
                maxScore = score;
                bestMatch = faq;
            }
        }

        return (bestMatch && maxScore >= 40) ? bestMatch : null;
    }

    async processUserMessage(msg) {
        if (this.isTyping) return;
        this.showTypingIndicator();
        
        const lowerMsg = msg.toLowerCase();

        // 1. GREETING
        if (lowerMsg.match(/hola|buenos|buenas|que tal/)) {
            let welcome = `¡Hola! Soy **${this.identity.name}**, tu ${this.identity.full_name}! 🏔️⚡`;
            if (this.pendingBonus) {
                welcome += `\n\n¡Es tu día de suerte! Te he acreditado **30 LifeCoins** de regalo por tu interés en Lifextreme! 🎁`;
                this.pendingBonus = 0;
            }
            welcome += `\n\n¿Qué ruta o actividad extrema te gustaría conquistar hoy?`;
            await this.addBotMessage(welcome);
            return;
        }

        // 2. COMMERCIAL AMBASSADOR
        const commUnit = this.searchCommercialTriggers(msg);
        if (commUnit) {
            let response = "";
            if (commUnit.key === 'community') {
                response = `¡Buena pregunta! En Lifextreme aplicamos el mantra: **"${commUnit.mantra}"**. ${commUnit.value_prop} En lugar de un precio fijo alto, ¿te gustaría que te busque un grupo social para esta ruta y dividimos los gastos? 🚀`;
            } else if (commUnit.key === 'gifts') {
                response = `¡Qué gran detalle! ${commUnit.concept}. Con nuestra Lifextreme Gift Card tú diseñas la adrenalina y ellos eligen la fecha. ¿Quieres que te ayude a configurar una ahora? 🎁`;
            } else if (commUnit.key === 'rewards') {
                response = `¡Así se habla! El sistema de LifeCoins premia tu lealtad. 1,000 LC equivalen a $10 de descuento real. ¿Quieres saber cómo ganar más hoy mismo? 🪙`;
            } else if (commUnit.key === 'partners') {
                response = `¡Amo esa mentalidad! Buscamos socios, no solo clientes. Tenemos planes desde comisiones del 22%. ¿Prefieres que te pase el contacto del WhatsApp VIP de Inversiones? 🤝`;
            }
            
            if (response) {
                await this.addBotMessage(response);
                return;
            }
        }

        // 3. KNOWLEDGE BASE (Expert)
        const kbResult = this.searchKnowledgeBase(msg);
        if (kbResult) {
            await this.addBotMessage(kbResult.answer);
            return;
        }

        // 4. AGENTE HUB (Advanced RAG)
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
            console.warn('⚠️ HUB Offline / Fallback Local.');
        }

        // 5. FALLBACK SPECIALIST
        await this.addBotMessage("Esa es una consulta muy técnica sobre seguridad y logística. Como Asesor, mi prioridad es que vuelvas a casa con una gran historia. ¿Prefieres que te conecte con nuestro Jefe de Expediciones por WhatsApp para darte el dato exacto? 🧗⚡");
    }

    scrollToBottom() {
        const container = document.getElementById('life-messages');
        if (container) container.scrollTop = container.scrollHeight;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.AIEngine = new AIPersonalizationEngine();
});
