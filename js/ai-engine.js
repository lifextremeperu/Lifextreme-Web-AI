// ========================================
// LIFEXTREME AI PERSONALIZATION ENGINE (v7.0 - MASTER CORE INTEGRATION)
// ========================================

class AIPersonalizationEngine {
    constructor() {
        this.identity = {
            name: "MAX",
            origin: "Asesor Maestro de Aventura (Lifextreme PRO)",
            full_name: "Master AI Sales Advisor",
            traits: ["Expert", "Safe", "Closer"]
        };
        
        // Paths & Cloud Config
        this.kbPath = 'data/knowledge/lifextreme/knowledge_base.json';
        this.hubUrl = 'https://desktop-sedhoop.tail883d62.ts.net/webhook/lifextreme';
        
        // Data State
        this.knowledgeBase = null;
        this.isTyping = false;
        this.userProfile = { nivel: 'Intermedio', es_elite: false };
        
        // Evolutionary Memory
        this.chatHistory = [];
        this.init();
    }

    async init() {
        this.loadChatHistory();
        console.log(`🚀 MAX v7.0 Standby | Connected to Hub Cusco`);
    }

    async loadKnowledgeBase() {
        if (this.knowledgeBase !== null) return; // Already loaded
        try {
            const kb = await fetch(this.kbPath).then(r => r.json()).catch(() => ({ data: [] }));
            this.knowledgeBase = kb.data || [];
            console.log(`🧠 Local KB Loaded`);
        } catch (e) {
            console.error('❌ Local KB Fail');
        }
    }

    loadChatHistory() {
        const history = sessionStorage.getItem('lifextreme_chat_history');
        if (history) this.chatHistory = JSON.parse(history);
    }

    saveChatHistory() {
        sessionStorage.setItem('lifextreme_chat_history', JSON.stringify(this.chatHistory.slice(-10)));
    }

    toggleChat() {
        const windowEl = document.getElementById('life-chat-window');
        if (!windowEl) return;
        
        // Carga diferida de KB (Lazy Loading) al abrir el chat
        this.loadKnowledgeBase();

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
        this.saveChatHistory();
        const container = document.getElementById('life-messages');
        const html = `<div class="flex justify-end animate-slideUp mb-4"><div class="chat-bubble-user p-4 max-w-[85%] text-xs font-medium shadow-md break-words bg-primary text-white rounded-2xl rounded-tl-none">${text}</div></div>`;
        container.insertAdjacentHTML('beforeend', html);
        this.scrollToBottom();
    }

    async processUserMessage(msg) {
        if (this.isTyping) return;
        this.showTypingIndicator();
        
        // URL pública segura vía LocalTunnel (Conecta al puerto 8000 local)
        const apiUrl = 'https://max-lifextreme.loca.lt/webhook/lifextreme';

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Bypass-Tunnel-Reminder': 'true' // Necesario para saltar la advertencia de loca.lt
                },
                body: JSON.stringify({ 
                    message: msg,
                    history: this.chatHistory.slice(-7, -1).map(h => ({
                        role: h.role === 'bot' ? 'assistant' : 'user',
                        content: h.content
                    }))
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                let responseText = data.mensaje || data.mensaje_principal || "Lo siento, no pude procesar la respuesta.";
                
                // Mostrar datos de cotización si vienen del agente RAG
                if (data.datos_cotizacion) {
                    const c = data.datos_cotizacion;
                    responseText += `\n\n--- 📊 **COTIZACIÓN PRO** ---\n` +
                                   `🎒 **Items:** ${c.items.join(', ')}\n` +
                                   `💵 **Monto Reserva (30%):** S/ ${c.monto_reserva_hoy}\n\n` +
                                   `📍 [Paga tu reserva con YAPE aquí](${c.link_pago_niubiz})`;
                }
                
                await this.addBotMessage(responseText);
                return;
            } else {
                throw new Error("HTTP " + response.status);
            }
        } catch (e) { 
            console.warn('⚠️ Agente MAX Offline', e);
            await this.addBotMessage('⚠️ MAX está desconectado. Asegúrate de ejecutar `npx localtunnel --port 8000 --subdomain max-lifextreme` y el servidor uvicorn local.');
            return;
        }

        await this.addBotMessage("Esa es una excelente pregunta técnica. Para darte la asesoría de seguridad exacta, ¿quieres que te conecte con un guía UIAGM por WhatsApp? 🧗⚡");
    }

    searchKnowledgeBase(query) {
        if (!this.knowledgeBase) return null;
        const norm = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        const words = norm.split(/\s+/).filter(w => w.length > 2);
        let best = null, maxScore = 0;
        for (const faq of this.knowledgeBase) {
            const qNorm = faq.question.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            let score = 0;
            for (const w of words) { if (qNorm.includes(w)) score += 20; }
            if (score > maxScore) { maxScore = score; best = faq; }
        }
        return (maxScore >= 40) ? best : null;
    }

    async addBotMessage(text) {
        this.chatHistory.push({ role: 'bot', content: text, time: Date.now() });
        this.saveChatHistory();
        
        try {
            this.isTyping = true;
            this.hideTypingIndicator();
            const container = document.getElementById('life-messages');
            const msgId = 'bot-' + Date.now();
            
            const html = `
                <div class="flex gap-3 animate-slideUp mb-4">
                    <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg shrink-0">
                        <i class="ri-flashlight-fill text-white text-xl"></i>
                    </div>
                    <div class="flex flex-col gap-2 max-w-[85%]">
                        <span class="text-[9px] font-black uppercase tracking-widest text-slate-400 ml-1">${this.identity.name}</span>
                        <div id="${msgId}" class="chat-bubble-bot p-4 text-slate-700 text-xs font-medium leading-relaxed break-words shadow-sm border border-slate-100 bg-white rounded-2xl rounded-tl-none"></div>
                    </div>
                </div>`;
            container.insertAdjacentHTML('beforeend', html);
            
            const bubble = document.getElementById(msgId);
            const formatted = text.replace(/\n/g, '<br>')
                                  .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="block mt-2 p-3 bg-orange-600 text-white text-center rounded-xl font-bold shadow-lg animate-bounce">$1</a>');
            
            bubble.innerHTML = formatted;
            this.scrollToBottom();
        } finally {
            this.isTyping = false;
            this.scrollToBottom();
        }
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
