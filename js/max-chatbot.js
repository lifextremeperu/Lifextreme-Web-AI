/**
 * max-chatbot.js — Widget de chat MAX para Lifextreme
 * Conecta al backend FastAPI local via tunnel público
 * 
 * Configuración: define window.LIFEXTREME_BACKEND_URL antes de cargar este script
 * o usa el endpoint por defecto de Cloudflare tunnel.
 */

(function () {
  'use strict';

  // ── CONFIGURACION ─────────────────────────────────────────
  // Esta URL se actualiza automaticamente cuando el tunnel esta activo
  // El usuario puede sobreescribirla en el HTML: window.LIFEXTREME_BACKEND_URL = "https://..."
  const BACKEND_URL = (window.LIFEXTREME_BACKEND_URL || 'http://localhost:8000').replace(/\/$/, '');
  const ENDPOINT    = `${BACKEND_URL}/webhook/lifextreme`;

  // ── ESTILOS ───────────────────────────────────────────────
  const CSS = `
    #max-chat-widget {
      position: fixed;
      bottom: 28px;
      right: 28px;
      z-index: 9999;
      font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }

    #max-chat-btn {
      width: 62px;
      height: 62px;
      border-radius: 50%;
      background: linear-gradient(135deg, #1a1a2e 0%, #e63946 100%);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 20px rgba(230, 57, 70, 0.45);
      transition: transform 0.2s, box-shadow 0.2s;
      position: relative;
    }
    #max-chat-btn:hover { transform: scale(1.08); box-shadow: 0 6px 28px rgba(230,57,70,0.6); }
    #max-chat-btn svg { width: 28px; height: 28px; fill: white; }

    #max-chat-badge {
      position: absolute;
      top: -3px;
      right: -3px;
      background: #22c55e;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      border: 2px solid white;
      animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
      0%,100% { box-shadow: 0 0 0 0 rgba(34,197,94,0.5); }
      50% { box-shadow: 0 0 0 6px rgba(34,197,94,0); }
    }

    #max-chat-panel {
      position: absolute;
      bottom: 78px;
      right: 0;
      width: 370px;
      max-height: 540px;
      background: #0f0f1a;
      border: 1px solid rgba(230,57,70,0.25);
      border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.6);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transform-origin: bottom right;
      transform: scale(0.85);
      opacity: 0;
      pointer-events: none;
      transition: transform 0.25s cubic-bezier(.175,.885,.32,1.275), opacity 0.2s;
    }
    #max-chat-panel.open {
      transform: scale(1);
      opacity: 1;
      pointer-events: all;
    }

    #max-chat-header {
      background: linear-gradient(90deg, #1a1a2e, #2d0a0f);
      padding: 16px 18px;
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 1px solid rgba(230,57,70,0.2);
    }
    #max-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: linear-gradient(135deg, #e63946, #c1121f);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      color: white;
      font-size: 16px;
    }
    #max-header-info h4 { margin: 0; color: #fff; font-size: 15px; font-weight: 700; }
    #max-header-info span { font-size: 12px; color: #22c55e; }

    #max-messages {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      max-height: 340px;
      scrollbar-width: thin;
      scrollbar-color: rgba(230,57,70,0.3) transparent;
    }

    .max-msg {
      max-width: 88%;
      padding: 10px 14px;
      border-radius: 16px;
      font-size: 13.5px;
      line-height: 1.5;
      animation: fadeUp 0.2s ease;
    }
    @keyframes fadeUp { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }

    .max-msg.bot {
      background: rgba(255,255,255,0.07);
      color: #e2e8f0;
      border-bottom-left-radius: 4px;
      align-self: flex-start;
    }
    .max-msg.user {
      background: linear-gradient(135deg, #e63946, #c1121f);
      color: white;
      border-bottom-right-radius: 4px;
      align-self: flex-end;
    }

    .max-typing {
      display: flex;
      gap: 5px;
      align-items: center;
      padding: 12px 14px;
      background: rgba(255,255,255,0.07);
      border-radius: 16px;
      border-bottom-left-radius: 4px;
      align-self: flex-start;
    }
    .max-typing span {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #e63946;
      animation: bounce 1.2s infinite;
    }
    .max-typing span:nth-child(2) { animation-delay: 0.2s; }
    .max-typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce { 0%,80%,100% { transform:scale(0.7); opacity:0.5; } 40% { transform:scale(1); opacity:1; } }

    #max-action-bar {
      padding: 0 16px 8px;
      display: none;
      gap: 8px;
      flex-wrap: wrap;
    }
    .max-action-btn {
      background: rgba(230,57,70,0.15);
      border: 1px solid rgba(230,57,70,0.4);
      color: #e63946;
      padding: 6px 14px;
      border-radius: 20px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
      transition: background 0.2s;
    }
    .max-action-btn:hover { background: rgba(230,57,70,0.3); }
    .max-action-btn.payment {
      background: linear-gradient(90deg, #e63946, #c1121f);
      color: white;
      border-color: transparent;
    }

    #max-input-area {
      padding: 12px 16px;
      display: flex;
      gap: 10px;
      border-top: 1px solid rgba(255,255,255,0.08);
      background: rgba(255,255,255,0.03);
    }
    #max-input {
      flex: 1;
      background: rgba(255,255,255,0.07);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 24px;
      padding: 10px 16px;
      color: white;
      font-size: 13px;
      outline: none;
      transition: border-color 0.2s;
    }
    #max-input:focus { border-color: rgba(230,57,70,0.6); }
    #max-input::placeholder { color: rgba(255,255,255,0.35); }

    #max-send-btn {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: linear-gradient(135deg, #e63946, #c1121f);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s;
      flex-shrink: 0;
    }
    #max-send-btn:hover { transform: scale(1.1); }
    #max-send-btn svg { width: 16px; height: 16px; fill: white; }

    #max-quick-replies {
      padding: 8px 16px 0;
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .max-quick-reply {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.12);
      color: #94a3b8;
      padding: 5px 12px;
      border-radius: 16px;
      cursor: pointer;
      font-size: 12px;
      transition: all 0.2s;
      white-space: nowrap;
    }
    .max-quick-reply:hover { background: rgba(230,57,70,0.15); border-color: #e63946; color: #e63946; }

    @media (max-width: 480px) {
      #max-chat-panel { width: calc(100vw - 32px); right: -4px; }
    }
  `;

  // ── TEMPLATE HTML ─────────────────────────────────────────
  const INITIAL_MSG = '¡Hola! Soy MAX 🏔️ el asesor de aventura de Lifextreme. '
    + 'Tengo acceso a más de 100 mil datos sobre tours, rutas y precios en los Andes. '
    + '¿Qué aventura estás buscando?';

  const QUICK_REPLIES = [
    '¿Tours al Ausangate?',
    'Precios Machu Picchu',
    '¿Qué incluye?',
    'Quiero reservar'
  ];

  // ── ESTADO ────────────────────────────────────────────────
  let isOpen    = false;
  let isLoading = false;
  let history   = [];

  // ── INIT ──────────────────────────────────────────────────
  function init() {
    injectStyles();
    buildWidget();
    bindEvents();
  }

  function injectStyles() {
    const style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);
  }

  function buildWidget() {
    const widget = document.createElement('div');
    widget.id = 'max-chat-widget';
    widget.innerHTML = `
      <button id="max-chat-btn" aria-label="Abrir chat MAX">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/></svg>
        <div id="max-chat-badge"></div>
      </button>

      <div id="max-chat-panel" role="dialog" aria-label="Chat MAX">
        <div id="max-chat-header">
          <div id="max-avatar">M</div>
          <div id="max-header-info">
            <h4>MAX — Asesor de Aventura</h4>
            <span>● En línea · Lifextreme Peru</span>
          </div>
        </div>

        <div id="max-quick-replies">
          ${QUICK_REPLIES.map(q => `<button class="max-quick-reply">${q}</button>`).join('')}
        </div>

        <div id="max-messages">
          <div class="max-msg bot">${INITIAL_MSG}</div>
        </div>

        <div id="max-action-bar"></div>

        <div id="max-input-area">
          <input id="max-input" type="text" placeholder="Escribe tu pregunta..." maxlength="500" autocomplete="off" />
          <button id="max-send-btn" aria-label="Enviar">
            <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(widget);
  }

  function bindEvents() {
    document.getElementById('max-chat-btn').addEventListener('click', togglePanel);
    document.getElementById('max-send-btn').addEventListener('click', handleSend);
    document.getElementById('max-input').addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
    });
    document.querySelectorAll('.max-quick-reply').forEach(btn => {
      btn.addEventListener('click', () => {
        document.getElementById('max-input').value = btn.textContent;
        handleSend();
        btn.closest('#max-quick-replies').style.display = 'none';
      });
    });
  }

  function togglePanel() {
    isOpen = !isOpen;
    document.getElementById('max-chat-panel').classList.toggle('open', isOpen);
  }

  async function handleSend() {
    if (isLoading) return;
    const input = document.getElementById('max-input');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    appendMessage('user', text);
    showTyping();
    isLoading = true;

    try {
      const response = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history, profile: {} })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();
      hideTyping();

      const msg = data.mensaje || data.message || 'No pude procesar tu consulta. Intenta de nuevo.';
      appendMessage('bot', msg);

      // Acciones especiales del agente
      if (data.action_required === 'SHOW_PAYMENT' && data.datos_cotizacion) {
        showPaymentAction(data.datos_cotizacion);
      }

      // Actualizar historial para contexto multi-turno
      history.push({ role: 'user', content: text });
      history.push({ role: 'assistant', content: msg });
      if (history.length > 20) history = history.slice(-20);

    } catch (err) {
      hideTyping();
      appendMessage('bot', `Lo siento, el backend no responde ahora. Escríbenos por WhatsApp: +51 984 123 456`);
      console.error('[MAX] Error:', err);
    } finally {
      isLoading = false;
    }
  }

  function appendMessage(role, text) {
    const msgs = document.getElementById('max-messages');
    const div  = document.createElement('div');
    div.className = `max-msg ${role}`;
    div.textContent = text;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  let typingEl = null;
  function showTyping() {
    const msgs = document.getElementById('max-messages');
    typingEl = document.createElement('div');
    typingEl.className = 'max-typing';
    typingEl.innerHTML = '<span></span><span></span><span></span>';
    msgs.appendChild(typingEl);
    msgs.scrollTop = msgs.scrollHeight;
  }
  function hideTyping() {
    if (typingEl) { typingEl.remove(); typingEl = null; }
  }

  function showPaymentAction(cotizacion) {
    const bar = document.getElementById('max-action-bar');
    bar.style.display = 'flex';
    bar.innerHTML = `
      <button class="max-action-btn payment" onclick="window.open('${cotizacion.link_pago_niubiz || '#'}','_blank')">
        Pagar S/ ${cotizacion.monto_reserva_hoy} (Reservar ahora)
      </button>
      <button class="max-action-btn" onclick="document.getElementById('max-action-bar').style.display='none'">
        Más info
      </button>
    `;
  }

  // Arrancar cuando el DOM esté listo
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
