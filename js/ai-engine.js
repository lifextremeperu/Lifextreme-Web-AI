// ========================================
// LIFEXTREME AI PERSONALIZATION ENGINE (v5.0 - MASTER ADVISOR)
// ========================================

class AIPersonalizationEngine {
    constructor() {
        this.identity = {
            name: "MAX",
            origin: "Asesor Maestro de Aventura (Lifextreme PRO)",
            full_name: "Master Sales Advisor",
            traits: ["Exciting", "Expert", "Safety-oriented", "Closer"]
        };
        
        // Paths
        this.kbPath = 'data/knowledge/lifextreme/knowledge_base.json';
        this.salesDnaPath = 'data/knowledge/max_sales_dna.json';
        this.commercialPath = 'data/knowledge/max_commercial_brain.json';
        this.hubUrl = 'https://hub-cusco-2026.tail883d62.ts.net/webhook/lifextreme';
        
        // Data State
        this.knowledgeBase = null;
        this.salesDNA = null;
        this.commercialBrain = null;
        this.isTyping = false;
        this.pendingBonus = 30; 
        
        // Evolutionary Memory
        this.chatHistory = [];
        this.currentTopic = null;
        this.lastIntent = 'GENERAL_INFO';
        
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
            
            console.log(`🚀 MAX v5.0: Master Advisor Initialized | ${this.knowledgeBase.length} Expert Nodes`);
        } catch (e) {
            console.error('❌ AI Hub Load Error:', e);
        }
    }

    loadUserProfile() {
        const profileData = localStorage.getItem('lifextreme_ai_profile');
        this.userProfile = profileData ? JSON.parse(profileData) : { rewards: 0, interactions: 0 };
    }

    loadChatHistory() {
        const history = sessionStorage.getItem('lifextreme_chat_history');
        if (history) {
            this.chatHistory = JSON.parse(history);
            const lastBotMsg = this.chatHistory.filter(m => m.role === 'bot').pop();
            if (lastBotMsg) this.detectTopic(lastBotMsg.content);
        }
    }

    saveChatHistory() {
        sessionStorage.setItem('lifextreme_chat_history', JSON.stringify(this.chatHistory.slice(-10)));
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

    // --- INTENT ROUTER (LANGCHAIN INSPIRED) ---
    analyzeIntent(query) {
        const lower = query.toLowerCase();
        
        const intentFlows = {
            'ADVENTURE_BOOKING': ['reserva', 'ir a', 'tour', 'expedicion', 'vuelo', 'rafting', 'trekking', 'entrada'],
            'EQUIPMENT_RENTAL': ['alquiler', 'renta', 'equipo', 'carpa', 'gopro', 'ropas', 'bolsa', 'mochila'],
            'MEMBERSHIP_UPGRADE': ['elite', 'socio', 'membresia', 'beneficios exclusive', 'vip'],
            'GIFT_EXPERIENCE': ['regalo', 'gift card', 'sorpresa', 'comprar para alguien'],
            'LOYALTY_QUERY': ['lifecoins', 'puntos', 'ganar', 'recompensas', 'canje']
        };

        for (const [intent, keywords] of Object.entries(intentFlows)) {
            if (keywords.some(k => lower.includes(k))) {
                this.lastIntent = intent;
                return intent;
            }
        }
        return 'GENERAL_INFO';
    }

    detectTopic(msg) {
        const lower = msg.toLowerCase();
        const keywords = ['salkantay', 'choquequirao', 'machu picchu', 'incas', 'canotaje', 'escalada'];
        for (const k of keywords) {
            if (lower.includes(k)) {
                this.currentTopic = k;
                return k;
            }
        }
        return null;
    }

    // --- SALES HOOKS (CREWAI INSPIRED) ---
    getStrategicSalesHook(intent, topic) {
        if (!this.commercialBrain) return null;
        
        const units = this.commercialBrain.business_units;
        
        switch (intent) {
            case 'ADVENTURE_BOOKING':
                return `🚀 **Sugerencia Experta:** Sabías que en nuestra **Comunidad Social** para ${topic ? topic.toUpperCase() : 'esta ruta'} estamos armando grupos para compartir gastos? ¡Podrías ahorrar hasta un 25%!`;
            case 'EQUIPMENT_RENTAL':
                return `📦 **Dato Pro:** Al ser socio Elite, tu renta de GoPro y Carpas es a mitad de precio. ¿Quieres que veamos el catálogo completo?`;
            case 'LOYALTY_QUERY':
                return `🪙 **Info:** Recuerda que 1,000 LifeCoins = $10 de descuento real en cualquier expedición.`;
            case 'GIFT_EXPERIENCE':
                return `🎁 **Tip:** Las Gift Cards no vencen y son el mejor regalo para un explorador.`;
            default:
                if (topic) return `🏔️ **¿Listo para el siguiente paso?** Tenemos expediciones abiertas para ${topic.toUpperCase()} con guías certificados Lifextreme.`;
                return null;
        }
    }

    async processUserMessage(msg) {
        if (this.isTyping) return;
        this.showTypingIndicator();
        
        const intent = this.analyzeIntent(msg);
        this.detectTopic(msg);
        
        this.chatHistory.push({ role: 'user', content: msg, time: Date.now() });
        this.saveChatHistory();

        // 1. GREETING FLOW
        if (msg.toLowerCase().match(/hola|buenos|buenas|que tal/)) {
            let welcome = `¡Hola! Soy **${this.identity.name}**, tu ${this.identity.full_name}! 🏔️⚡`;
            if (this.pendingBonus) {
                welcome += `\n\n🎁 **BONO ACTIVADO:** Te he acreditado **30 LifeCoins** por iniciar nuestra charla.`;
                this.pendingBonus = 0;
            }
            welcome += `\n\n¿Buscas alguna ruta técnica, alquilar equipo de alta montaña o unirte a la Comunidad Social hoy?`;
            await this.addBotMessage(welcome);
            return;
        }

        // 2. BACKEND ROUTING (PYDANTIC AI HUB)
        try {
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 9000);
            
            const response = await fetch(this.hubUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                mode: 'cors',
                body: JSON.stringify({ 
                    message: msg, 
                    intent: intent,
                    topic: this.currentTopic,
                    history: this.chatHistory.slice(-5),
                    profile: this.userProfile
                }),
                signal: controller.signal
            });
            clearTimeout(timeout);
            
            if (response.ok) {
                const data = await response.json();
                if (data.response || data.reply) {
                    let agentResp = data.response || data.reply;
                    const hook = this.getStrategicSalesHook(intent, this.currentTopic);
                    if (hook) agentResp += `\n\n---\n${hook}`;
                    await this.addBotMessage(agentResp);
                    return;
                }
            }
        } catch (e) {
            console.warn('⚠️ HUB Offline. Saltando a RAG Local Experto.');
        }

        // 3. LOCAL EXPERT RAG
        const kbResult = this.searchKnowledgeBase(msg);
        if (kbResult) {
            let expertMsg = kbResult.answer;
            const hook = this.getStrategicSalesHook(intent, this.currentTopic);
            if (hook) expertMsg += `\n\n---\n${hook}`;
            await this.addBotMessage(expertMsg);
            return;
        }

        // 4. FINAL FALLBACK (PERSUASIVE CLOSER)
        const fallback = `Esa es una consulta de alta montaña. Como tu **${this.identity.full_name}**, te conectaré con nuestro Jefe de Logística por WhatsApp para garantizar que tu aventura a ${this.currentTopic ? this.currentTopic.toUpperCase() : 'el destino deseado'} sea perfecta. 🧗⚡`;
        await this.addBotMessage(fallback);
    }

    searchKnowledgeBase(query) {
        if (!this.knowledgeBase || this.knowledgeBase.length === 0) return null;
        let target = query;
        if (query.length < 15 && this.currentTopic) target = `${this.currentTopic} ${query}`;
        
        const norm = target.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[¿?¡!.,;:]/g, '');
        const queryWords = norm.split(/\s+/).filter(w => w.length > 2);
        
        let best = null, maxScore = 0;
        for (const faq of this.knowledgeBase) {
            const qNorm = faq.question.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            let score = 0, matches = 0;
            for (const w of queryWords) { 
                if (qNorm.includes(w)) { score += 20; matches++; }
            }
            if (qNorm.includes(norm)) score += 100;
            if (matches / (queryWords.length || 1) < 0.45) score = 0;
            if (score > maxScore) { maxScore = score; best = faq; }
        }
        return (best && maxScore >= 40) ? best : null;
    }

    async addBotMessage(text) {
        this.chatHistory.push({ role: 'bot', content: text, time: Date.now() });
        this.saveChatHistory();
        this.detectTopic(text);
        
        this.isTyping = true;
        this.hideTypingIndicator();
        const container = document.getElementById('life-messages');
        const stylized = this.personalizeResponse(text);
        const msgId = 'bot-' + Date.now();
        
        const html = `
            <div class="flex gap-3 animate-slideUp mb-4">
                <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg flex-shrink-0">
                    <i class="ri-flashlight-fill text-white text-xl"></i>
                </div>
                <div class="flex flex-col gap-1 max-w-[85%]">
                    <span class="text-[9px] font-black uppercase tracking-widest text-slate-400 ml-1">${this.identity.name}</span>
                    <div id="${msgId}" class="chat-bubble-bot p-4 text-slate-700 text-xs font-medium leading-relaxed break-words shadow-sm border border-slate-100 bg-[#f8fafc] rounded-2xl rounded-tl-none"></div>
                </div>
            </div>`;
        container.insertAdjacentHTML('beforeend', html);
        
        const bubble = document.getElementById(msgId);
        const chars = stylized.split('');
        let current = '';
        for (let i = 0; i < chars.length; i++) {
            current += chars[i];
            bubble.innerHTML = current.replace(/\n/g, '<br>');
            if (i % 8 === 0) this.scrollToBottom();
            await new Promise(r => setTimeout(r, 1)); 
        }
        this.isTyping = false;
        this.scrollToBottom();
    }

    personalizeResponse(text) {
        if (text.includes('🏔️') || text.includes('⚡')) return text;
        const suffixes = ["🏔️⚡", "🚀", "🧗", "🔥"];
        return `${text} ${suffixes[Math.floor(Math.random() * suffixes.length)]}`;
    }

    showTypingIndicator() {
        const container = document.getElementById('life-messages');
        const html = `<div id="typing-indicator" class="flex gap-3 mb-4"><div class="p-3 bg-white rounded-2xl shadow-sm border border-slate-100 flex gap-1"><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce"></span><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay:0.2s"></span><span class="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay:0.4s"></span></div></div>`;
        container.insertAdjacentHTML('beforeend', html);
        this.scrollToBottom();
    }

    hideTypingIndicator() { document.getElementById('typing-indicator')?.remove(); }
    scrollToBottom() {
        const el = document.getElementById('life-messages');
        if (el) el.scrollTop = el.scrollHeight;
    }
}

document.addEventListener('DOMContentLoaded', () => { window.AIEngine = new AIPersonalizationEngine(); });
