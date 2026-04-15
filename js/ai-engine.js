// ========================================
// LIFEXTREME AI PERSONALIZATION ENGINE (v5.5 - SUPER ADVISOR)
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
            
            console.log(`🚀 MAX v5.5: Super Advisor | Knowledge Nodes: ${this.knowledgeBase.length}`);
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
        this.chatHistory.push({ role: 'user', content: text, time: Date.now() });
        this.detectTopic(text);
        this.saveChatHistory();

        const container = document.getElementById('life-messages');
        const msgHtml = `<div class="flex justify-end animate-slideUp mb-4"><div class="chat-bubble-user p-4 max-w-[85%] text-xs font-medium shadow-md break-words bg-primary text-white rounded-2xl rounded-tr-none">${text}</div></div>`;
        container.insertAdjacentHTML('beforeend', msgHtml);
        this.scrollToBottom();
    }

    // --- INTENT ROUTER & TOPIC DETECTION ---
    analyzeIntent(query) {
        const lower = query.toLowerCase();
        
        // Priority Mapping
        const mapping = [
            { id: 'ADVENTURE_BOOKING', keywords: ['reserva', 'ir a', 'salkantay', 'choquequirao', 'tour', 'machu picchu', 'caminata'] },
            { id: 'EQUIPMENT_RENTAL', keywords: ['equipo', 'alquilar', 'renta', 'gopro', 'carpa', 'mochila', 'bolsa'] },
            { id: 'GIFT_EXPERIENCE', keywords: ['regalo', 'gift card', 'sorpresa', 'dar', 'obsequio'] },
            { id: 'MEMBERSHIP_UPGRADE', keywords: ['elite', 'socio', 'membresia', 'club', 'exclusive'] },
            { id: 'LOYALTY_QUERY', keywords: ['puntos', 'lifecoins', 'ganar', 'canje'] }
        ];

        for (const m of mapping) {
            if (m.keywords.some(k => lower.includes(k))) return m.id;
        }
        return 'GENERAL_INFO';
    }

    detectTopic(msg) {
        const lower = msg.toLowerCase();
        const mainRoutes = ['salkantay', 'choquequirao', 'machu picchu', 'vinicunca', 'laguna humantay', 'ausangate'];
        for (const r of mainRoutes) {
            if (lower.includes(r)) { 
                this.currentTopic = r; 
                return r; 
            }
        }
        return null;
    }

    // --- STRATEGIC ENGINE (THE AMBASSADOR'S VOICE) ---
    async processUserMessage(msg) {
        if (this.isTyping) return;
        this.showTypingIndicator();
        
        const intent = this.analyzeIntent(msg);
        const topic = this.detectTopic(msg);
        this.lastIntent = intent;

        // 1. GREETING FLOW
        if (msg.toLowerCase().match(/hola|buenos|buenas|que tal/)) {
            let welcome = `¡Hola! Soy **${this.identity.name}**, tu ${this.identity.full_name}! 🏔️⚡`;
            if (this.pendingBonus) {
                welcome += `\n\n🎁 **30 LifeCoins** otorgados de bofetada por tu curiosidad!`;
                this.pendingBonus = 0;
            }
            welcome += `\n\n¿Buscas conquistar el **Salkantay**, alquilar equipo **Pro** o comprar una **Gift Card** de aventura hoy?`;
            await this.addBotMessage(welcome);
            return;
        }

        // 2. COMMERCIAL OVERRIDE (COMMERCIAL BRAIN FIRST)
        const commResult = this.getCommercialResponse(intent, topic, msg);
        if (commResult) {
            await this.addBotMessage(commResult);
            return;
        }

        // 3. AGENTE HUB (Advanced RAG)
        try {
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 8000);
            const response = await fetch(this.hubUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                mode: 'cors',
                body: JSON.stringify({ 
                    message: msg, 
                    intent: intent,
                    topic: topic || this.currentTopic,
                    history: this.chatHistory.slice(-4),
                    context: "Lifextreme Sales Ambassador"
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
        } catch (e) { console.warn('⚠️ HUB offline'); }

        // 4. KNOWLEDGE BASE EXPERT
        const kbResult = this.searchKnowledgeBase(msg);
        if (kbResult) {
            await this.addBotMessage(kbResult.answer);
            return;
        }

        // 5. SMART FALLBACK
        const fallback = topic 
            ? `Sobre **${topic.toUpperCase()}**, soy un experto pero para darte la logística exacta prefiero conectarte con nuestro búnker por WhatsApp. ¿Quieres el link directo? 🧗⚡`
            : "¿Quieres que revisemos el inventario de equipos o prefieres ver la disponibilidad de la Comunidad Social para bajar costos? 🚀";
        await this.addBotMessage(fallback);
    }

    getCommercialResponse(intent, topic, msg) {
        if (!this.commercialBrain) return null;
        const units = this.commercialBrain.business_units;

        if (intent === 'GIFT_EXPERIENCE') {
            return `¡Qué gran detalle! ${units.gifts.concept}. Nuestras **Gift Cards de Aventura** son el regalo perfecto: tú eliges el monto y ellos eligen entre trekking, rafting o escalada. ¡No vencen nunca! 🎁`;
        }

        if (intent === 'ADVENTURE_BOOKING' && (topic === 'salkantay' || topic === 'choquequirao')) {
            return `¡Esa es una ruta ÉPICA! Como tu Master Advisor te digo: En la **Comunidad Social** para ${topic.toUpperCase()} estamos armando el grupo para este fin de semana. Si te unes, compartimos los costos de guía y equipo y ahorras hasta un 25%. ¿Te reservo un cupo preventivo? 🏔️⚡`;
        }

        if (intent === 'EQUIPMENT_RENTAL') {
            return `¡Inteligente decisión! ${units.equipment.value_prop}. Tenemos cámaras GoPro, carpas térmicas y carpas de alta montaña listas. Al ser Socio Elite, tienes un **15% de descuento** en renta. ¿Deseas ver el catálogo? 📦`;
        }

        if (intent === 'MEMBERSHIP_UPGRADE') {
            return `¡Bienvenido al Club! Ser **Socio Elite** es la única forma de viajar al costo en Perú. Recuperas tu inversión en tu primer tour. ¿Quieres los detalles del Pase Anual Exclusive? 🏆`;
        }

        return null;
    }

    searchKnowledgeBase(query) {
        if (!this.knowledgeBase || this.knowledgeBase.length === 0) return null;
        let target = query;
        if (query.length < 15 && this.currentTopic) target = `${this.currentTopic} ${query}`;
        
        const norm = target.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[¿?¡!.,;:]/g, '');
        const words = norm.split(/\s+/).filter(w => w.length > 2 && !['para', 'donde', 'como', 'quiero'].includes(w));
        
        let best = null, maxScore = 0;
        for (const faq of this.knowledgeBase) {
            const qNorm = faq.question.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            let score = 0, matches = 0;
            for (const w of words) { if (qNorm.includes(w)) { score += 20; matches++; } }
            if (qNorm.includes(norm)) score += 80;
            if (matches / (words.length || 1) < 0.6) score = 0; // Strict matching
            if (score > maxScore) { maxScore = score; best = faq; }
        }
        return (best && maxScore >= 40) ? best : null;
    }

    async addBotMessage(text) {
        this.chatHistory.push({ role: 'bot', content: text, time: Date.now() });
        this.saveChatHistory();
        
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
        if (text.includes('🏔️')) return text;
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
