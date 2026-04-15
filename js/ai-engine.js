// ========================================
// LIFEXTREME AI PERSONALIZATION ENGINE (v4.0 - EVOLUTIONARY MEMORY)
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
        
        // --- EVOLUTIONARY MEMORY ---
        this.chatHistory = [];
        this.currentTopic = null;
        this.lastTopicTime = 0;
        
        this.init();
    }

    async init() {
        this.loadUserProfile();
        this.loadChatHistory();
        try {
            const [kb, dna, comm] = await Promise.all([
                fetch(this.kbPath).then(r => r.json()).catch(() => ({ data: [] })),
                fetch(this.salesDnaPath).then(r => r.json()).catch(() => []),
                fetch(this.commercialPath).then(r => r.json()).catch(() => null)
            ]);
            
            this.knowledgeBase = kb.data || [];
            this.salesDNA = dna;
            this.commercialBrain = comm;
            
            console.log(`🧠 MAX v4: Memoria Evolutiva activa (${this.knowledgeBase.length} FAQs)`);
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

    loadChatHistory() {
        const history = sessionStorage.getItem('lifextreme_chat_history');
        if (history) {
            this.chatHistory = JSON.parse(history);
            // Re-infer topic from last bot message if possible
            const lastBotMsg = this.chatHistory.filter(m => m.role === 'bot').pop();
            if (lastBotMsg) this.updateCurrentTopic(lastBotMsg.content);
        }
    }

    saveChatHistory() {
        sessionStorage.setItem('lifextreme_chat_history', JSON.stringify(this.chatHistory.slice(-10)));
    }

    updateCurrentTopic(msg) {
        const topics = {
            'salkantay': ['salkantay', 'nevado', 'trek'],
            'choquequirao': ['choquequirao', 'cuna de oro', 'hermana'],
            'machu picchu': ['machu picchu', 'ciudadela', 'llaqta'],
            'canotaje': ['rio', 'rafting', 'canotaje', 'urubamba', 'apurimac'],
            'escalada': ['roca', 'escalada', 'climbing', 'vias'],
            'precios': ['cuanto', 'precio', 'costo', '$', 's/'],
            'comunidad': ['grupo', 'comunidad', 'social', 'compartido']
        };
        
        const lower = msg.toLowerCase();
        for (const [topic, keywords] of Object.entries(topics)) {
            if (keywords.some(k => lower.includes(k))) {
                this.currentTopic = topic;
                this.lastTopicTime = Date.now();
                break;
            }
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
        this.chatHistory.push({ role: 'user', content: text, time: Date.now() });
        this.updateCurrentTopic(text);
        this.saveChatHistory();

        const container = document.getElementById('life-messages');
        const msgHtml = `<div class="flex justify-end animate-slideUp mb-4"><div class="chat-bubble-user p-4 max-w-[85%] text-xs font-medium shadow-md break-words bg-primary text-white rounded-2xl rounded-tr-none">${text}</div></div>`;
        container.insertAdjacentHTML('beforeend', msgHtml);
        this.scrollToBottom();
    }

    personalizeResponse(text) {
        if (!text) return "";
        if (text.includes('🏔️') || text.includes('🧗')) return text;

        const prefixes = ["¡Aventurero!", "Atento:", "Mi consejo experto:", "Dato PRO:"];
        const suffixes = ["🏔️⚡", "🚀", "🧗", "🔥"];
        const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
        const suffix = suffixes[Math.floor(Math.random() * suffixes.length)];
        return `${prefix} ${text} ${suffix}`;
    }

    async addBotMessage(text) {
        this.chatHistory.push({ role: 'bot', content: text, time: Date.now() });
        this.saveChatHistory();

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
            await new Promise(r => setTimeout(r, 2)); 
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
        
        let targetQuery = query;
        // CONTEXTUAL MEMORY: If query is vague, inject current topic
        if (query.length < 15 && this.currentTopic) {
            targetQuery = `${this.currentTopic} ${query}`;
        }

        const normalizedQuery = targetQuery.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[¿?¡!.,;:]/g, '');
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
                welcome += `\n\n¡Te he acreditado **30 LifeCoins** por tu interés! 🎁`;
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
                const topicText = this.currentTopic ? ` para ${this.currentTopic.toUpperCase()}` : "";
                response = `¡Gran consulta! En nuestra **Comunidad Social${topicText}** aplicamos: **"${commUnit.mantra}"**. ${commUnit.value_prop} ¿Quieres que te busque compañeros de ruta para bajar el precio? 🚀`;
            } else {
                response = commUnit.value_prop || commUnit.concept || "¡Interesante! Cuéntame más.";
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

        // 4. AGENTE HUB (Advanced RAG with History Buffer)
        const HUB_URL = 'https://hub-cusco-2026.tail883d62.ts.net/webhook/lifextreme';
        try {
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 8000);
            
            // Sending last 3 interactions for context
            const historyBuffer = this.chatHistory.slice(-4); 
            
            const response = await fetch(HUB_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                mode: 'cors',
                body: JSON.stringify({ 
                    message: msg, 
                    history: historyBuffer,
                    topic: this.currentTopic,
                    context: this.userProfile || {} 
                }),
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
            console.warn('⚠️ HUB Offline / Fallback Local Activo.');
        }

        // 5. FALLBACK SPECIALIST
        const fallbackText = this.currentTopic 
            ? `Sobre **${this.currentTopic.toUpperCase()}**, tengo datos muy técnicos. Para tu seguridad, ¿prefieres que hablemos por WhatsApp con un guía o vemos cupos en la Comunidad?`
            : "Esa consulta requiere precisión técnica. ¿Prefieres contactar a un guía experto o revisamos la comunidad social?";
        await this.addBotMessage(fallbackText);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.AIEngine = new AIPersonalizationEngine();
});
