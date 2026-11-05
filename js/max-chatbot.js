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
  const STREAM_ENDPOINT = `${BACKEND_URL}/webhook/lifextreme/stream`;

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
  const INITIAL_MSG = '¡Hola! Soy MAX 🏔️, Director Comercial de Expediciones de Lifextreme.\n\n'
    + 'No soy un simple chatbot de información: **armo y cierro tu paquete todo incluido al instante** con todo lo que necesitas para tu seguridad y confort:\n\n'
    + '🎒 **Tour oficial** + 🧗 **Equipo técnico** + 🕶️ **Accesorios** + 🩺 **Asistencia médica y oxígeno** + 🛡️ **Seguro extremo**.\n\n'
    + '¿Qué cumbre o aventura deseas conquistar hoy? Elige una opción o dime tu destino:';

  const QUICK_REPLIES = [
    '🏔️ Paquete Machu Picchu Pro',
    '⚡ Nevado Mateo con Todo Incluido',
    '🧗 Choquequirao Expedición Completa',
    '💳 Quiero Cotizar y Reservar con 30%'
  ];

  // ── SALES CLOSER ENGINE (TOUR + EQUIPO + ACCESORIOS + ASISTENCIA + SEGURO) ──
  let lastSelectedBundle = null;

  function formatMd(str) {
    return String(str || '')
      .replace(/\[CARR[^\]]*\]?/gi, '')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }

  function buildSalesBundle(query) {
    const q = (query || '').toLowerCase();
    let tourTitle = lastSelectedBundle ? lastSelectedBundle.title : 'Salkantay Trek & Domos Glamping a Machu Picchu (4D/3N)';
    let tourDept = lastSelectedBundle ? lastSelectedBundle.dept : 'Cusco';
    let basePrice = lastSelectedBundle ? lastSelectedBundle.basePrice : 1630;

    if (q.includes('salkantay')) {
      tourTitle = 'Salkantay Trek & Domos Glamping a Machu Picchu (4D/3N)';
      tourDept = 'Cusco';
      basePrice = 1630;
    } else if (q.includes('choquequirao')) {
      tourTitle = 'Choquequirao Expedición Legendaria (4D/3N)';
      tourDept = 'Cusco';
      basePrice = 790;
    } else if (q.includes('camino inca') || q.includes('inca trail')) {
      tourTitle = 'Camino Inca Clásico a Machu Picchu (4D/3N)';
      tourDept = 'Cusco';
      basePrice = 2230;
    } else if (q.includes('ausangate')) {
      tourTitle = 'Circuito Ausangate & 7 Lagunas Glamping (6D/5N)';
      tourDept = 'Cusco';
      basePrice = 1880;
    } else if (q.includes('vinicunca') || q.includes('colores')) {
      tourTitle = 'Montaña de los 7 Colores & Valle Rojo Pro';
      tourDept = 'Cusco';
      basePrice = 230;
    } else if (q.includes('humantay')) {
      tourTitle = 'Laguna Humantay & Soraypampa Glamping';
      tourDept = 'Cusco';
      basePrice = 230;
    } else if (q.includes('mateo') || q.includes('pastoruri')) {
      tourTitle = 'Nevado Mateo 5,150m (Cumbre Glaciar)';
      tourDept = 'Huaraz';
      basePrice = 380;
    } else if (q.includes('santa cruz') || q.includes('huaraz') || q.includes('laguna 69')) {
      tourTitle = 'Trekking Santa Cruz & Laguna 69 Cordillera Blanca (4D/3N)';
      tourDept = 'Huaraz';
      basePrice = 980;
    } else if (q.includes('colca') || q.includes('arequipa')) {
      tourTitle = 'Trekking Cañón del Colca (3D/2N)';
      tourDept = 'Arequipa';
      basePrice = 630;
    } else if (q.includes('misti')) {
      tourTitle = 'Ascenso Volcán Misti 5,825m (2D/1N)';
      tourDept = 'Arequipa';
      basePrice = 880;
    } else if (q.includes('parapente') || q.includes('miraflores') || q.includes('costa')) {
      tourTitle = 'Parapente Táctico Costa Verde Miraflores';
      tourDept = 'Lima';
      basePrice = 260;
    } else if (q.includes('rafting') || q.includes('lunahuana') || q.includes('canete')) {
      tourTitle = 'Rafting Extremo & Canopy Lunahuaná';
      tourDept = 'Lima';
      basePrice = 220;
    } else if (q.includes('machu picchu')) {
      tourTitle = 'Expedición Machu Picchu & Tren Panorámico';
      tourDept = 'Cusco';
      basePrice = 620;
    } else if (window.tours && Array.isArray(window.tours) && window.tours.length > 0) {
      const words = q.split(/\s+/).filter(w => w.length >= 4);
      const found = window.tours.find(t =>
        words.some(w => t.title.toLowerCase().includes(w))
      );
      if (found) {
        tourTitle = found.title;
        tourDept = found.dept;
        basePrice = Number(found.price) || 450;
      }
    }

    const gearPrice = 140; // Botas Gore-Tex, bastones carbono, arnes, casco
    const accPrice = 50;   // Lentes UV400 cat 4, frontal 450lm, guantes termicos
    const medPrice = 45;   // Monitoreo oximetria + O2 medicinal 99.5%
    const insPrice = 35;   // Seguro de rescate y accidentes personales
    const subtotal = basePrice + gearPrice + accPrice + medPrice + insPrice;
    const discount = 50;   // Bono de bienvenida Lifecoins
    const totalBundle = subtotal - discount;
    const reserva30 = Math.round(totalBundle * 0.30);
    const saldo70 = totalBundle - reserva30;

    const bundle = {
      title: tourTitle,
      dept: tourDept,
      basePrice,
      gearPrice,
      accPrice,
      medPrice,
      insPrice,
      subtotal,
      discount,
      totalBundle,
      reserva30,
      saldo70
    };
    lastSelectedBundle = bundle;
    return bundle;
  }

  function buildIntelligentLocalReply(query, bundle, hasActiveBooking, clientProfile) {
    const q = (query || '').toLowerCase();
    if (hasActiveBooking && clientProfile) {
      return `¡Hola <strong>${clientProfile.passenger_name || 'Explorador'}</strong>! 🏔️ Veo tu reserva confirmada <strong>${clientProfile.booking_code}</strong> para <strong>${clientProfile.tour_name}</strong>.<br><br>` +
        `• <strong>Escudo Médico & Aclimatación (Agente 1):</strong> Recuerda llegar a Cusco al menos 48h antes; en campamento mediremos tu saturación (SpO₂) a las 07:00 y 19:00 hrs e incluimos botas de compresión neumática y pediluvios botánicos.<br>` +
        `• <strong>Duffle Bag 7 kg (Agente 2):</strong> Te entregaremos tu duffle bag en el briefing la noche previa; los arrieros llevarán hasta 7 kg con pesaje digital certificado bajo la Ley N° 31614.`;
    }
    if (q.includes('fecha') || q.includes('diciembre') || q.includes('cuando') || q.includes('salid') || q.includes('disponib') || q.includes('mes')) {
      const monthMention = q.includes('diciembre') ? 'todo el mes de <strong>diciembre (del 1 al 31 de diciembre, incluyendo salidas especiales de Navidad y Año Nuevo)</strong>' : '<strong>todos los días de la semana</strong> con salidas confirmadas a partir de 2 pasajeros';
      return `¡Hola! 🏔️ Para <strong>${bundle.title}</strong> tenemos <strong>salidas diarias garantizadas durante ${monthMention}</strong>, tanto en grupo reducido (ratio máx. 1:8 con guía UIAGM/WFR) como en modalidad Privada VIP.<br><br>` +
        `Nuestra ruta de 4 Días / 3 Noches incluye pernocta en <strong>Domos Geodésicos Glamping en Soraypampa (3,900 msnm)</strong>, <strong>Duffle Bag de 7 kg</strong> porteado por arrieros (Ley N° 31614), desfase horario (<em>Offset Trekking</em> sin multitudes en el Abra Salkantay a 4,630m) y monitoreo de oxígeno dos veces al día.<br><br>` +
        `¿Para qué día exacto deseas programar tu salida y cuántas personas viajan contigo?`;
    }
    if (q.includes('altura') || q.includes('soroche') || q.includes('aclimat') || q.includes('oxigeno')) {
      return `En <strong>${bundle.title}</strong> aplicamos el protocolo de nuestro <strong>Agente Médico & Aclimatación</strong>:<br><br>` +
        `1️⃣ Recomendamos 2 días previos en Cusco/Valle Sagrado (2,870m - 3,399m).<br>` +
        `2️⃣ Controlamos tu oximetría (SpO₂) y pulso 2 veces al día en campamento, contamos con balón de oxígeno medicinal de 3 m³, fisioterapia con botas de compresión solar y evacuación clínica garantizada con O2 Medical Network.`;
    }
    if (q.includes('equipaje') || q.includes('duffle') || q.includes('peso') || q.includes('7 kg') || q.includes('mochila') || q.includes('mula') || q.includes('porteador')) {
      return `Con nuestro <strong>Agente Duffle Bag Optimizer (Regla 7 kg & Ley N° 31614)</strong>:<br><br>` +
        `• Te entregamos en Cusco un <strong>Duffle Bag oficial para hasta 7.0 kg</strong> (allí va tu saco de dormir, ropa térmica y calzado de campamento), que llevan nuestros arrieros y mulas con pesaje digital visible.<br>` +
        `• Tú solo caminas con una <strong>mochila ligera de día (20-30L)</strong> con tu agua, cámara y casaca impermeable.`;
    }
    return `¡Excelente elección con <strong>${bundle.title}</strong>! 🏔️ Contamos con salidas diarias confirmadas, Domos Glamping, Duffle Bag de 7 kg porteado (Ley N° 31614), guía certificado UIAGM/WFR y monitoreo biométrico de altura.<br><br>Aquí tienes el detalle de tu paquete todo incluido para bloquear tu fecha con el 30%:`;
  }

  function createSalesCardHtml(bundle) {
    const safeTourName = bundle.title.replace(/'/g, "\\'");
    let sentinelBadge = '';
    if (bundle.title.toLowerCase().includes('machu picchu')) {
      sentinelBadge = `
        <div style="background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:6px 10px; margin-bottom:8px; font-size:10px; display:flex; justify-content:space-between; align-items:center;">
          <span style="color:#6ee7b7; font-weight:700; display:flex; align-items:center; gap:5px;">
            <span style="width:6px; height:6px; border-radius:50%; background:#10b981; box-shadow:0 0 6px #10b981; display:inline-block;"></span>
            TuBoleto Cultura: 284 cupos confirmados
          </span>
          <span style="color:#94a3b8; font-size:9px;">Tren: Asientos OK</span>
        </div>
      `;
    }
    return `
      <div style="background: linear-gradient(145deg, #0b0f19, #131d31); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 16px; padding: 14px; margin-top: 10px; color: #fff; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span style="font-size:9px; font-weight:900; color:#f59e0b; text-transform:uppercase; letter-spacing:0.12em; background:rgba(245,158,11,0.15); padding:2px 8px; border-radius:20px; border:1px solid rgba(245,158,11,0.3);">
            🔥 Paquete Oficial All-Inclusive
          </span>
          <span style="font-size:9px; font-weight:bold; background:rgba(34,197,94,0.15); color:#4ade80; padding:2px 6px; border-radius:6px; border:1px solid rgba(34,197,94,0.3);">
            UIAGM Verificado
          </span>
        </div>
        <h4 style="font-weight:900; font-size:14px; margin:0 0 8px; color:#fff; line-height:1.3;">
          ${bundle.title} (${bundle.dept})
        </h4>
        ${sentinelBadge}

        <div style="font-size:11px; line-height:1.55; color:#cbd5e1; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:8px; margin-bottom:8px;">
          <div>✅ <strong style="color:#fff;">1. Tour & Tickets:</strong> Ruta guiada oficial con Guía UIAGM/AGMP + Permisos</div>
          <div>✅ <strong style="color:#fff;">2. Equipo Técnico Pro:</strong> Botas Gore-Tex, bastones carbono, casco y arnés Petzl</div>
          <div>✅ <strong style="color:#fff;">3. Accesorios de Altura:</strong> Lentes UV400 cat. 4, linterna 450lm y guantes térmicos</div>
          <div>✅ <strong style="color:#fff;">4. Asistencia Médica:</strong> Monitoreo oximetría + Balón de oxígeno medicinal 99.5%</div>
          <div>✅ <strong style="color:#fff;">5. Seguro Extremo:</strong> Cobertura médica y rescate integral hasta S/ 50,000</div>
        </div>

        <div style="background:rgba(255,255,255,0.04); padding:10px; border-radius:12px; margin-bottom:10px; border:1px solid rgba(255,255,255,0.06);">
          <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8;">
            <span>Valor Total del Paquete:</span>
            <span style="text-decoration:line-through;">S/ ${bundle.subtotal}</span>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:11px; color:#4ade80; font-weight:bold;">
            <span>Bono Lifecoins Aplicado:</span>
            <span>- S/ ${bundle.discount}.00</span>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:900; color:#fff; margin-top:5px; border-top:1px solid rgba(255,255,255,0.1); padding-top:5px;">
            <span>Inversión Todo Incluido:</span>
            <span style="color:#f59e0b; font-size:15px;">S/ ${bundle.totalBundle}.00</span>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:900; color:#38bdf8; margin-top:3px;">
            <span>🚀 Bloquea tu Cupo Hoy (30%):</span>
            <span style="font-size:15px; color:#38bdf8;">S/ ${bundle.reserva30}.00</span>
          </div>
          <div style="font-size:9px; color:#94a3b8; text-align:right; margin-top:3px;">
            *El 70% restante (S/ ${bundle.saldo70}.00) se cancela antes de partir.
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:6px;">
          <button type="button" onclick="window.maxAddToCartAndPay('${safeTourName}', ${bundle.totalBundle}, 1, true)" style="background:linear-gradient(135deg, #f59e0b, #ea580c); color:#0f172a; border:none; border-radius:12px; padding:11px; font-weight:900; font-size:11px; text-transform:uppercase; letter-spacing:0.06em; cursor:pointer; box-shadow:0 6px 18px rgba(245,158,11,0.35); transition:transform 0.2s;">
            💳 Reservar Cupo con 30% (S/ ${bundle.reserva30})
          </button>
          <a href="https://wa.me/51958050928?text=${encodeURIComponent('Hola MAX! Deseo cerrar la reserva de mi Paquete Todo Incluido: ' + bundle.title + ' (Total S/ ' + bundle.totalBundle + ' | 30% S/ ' + bundle.reserva30 + '). ¿Tienen cupos disponibles para esta fecha?')}" target="_blank" rel="noopener noreferrer" style="background:#22c55e; color:#0f172a; text-decoration:none; text-align:center; border-radius:12px; padding:9px; font-weight:900; font-size:11px; text-transform:uppercase; letter-spacing:0.05em; display:flex; align-items:center; justify-content:center; gap:6px;">
            📲 Cerrar y Coordinar con Guía en WhatsApp
          </a>
        </div>
      </div>
    `;
  }

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
            <h4>MAX — Closer Comercial Pro</h4>
            <span>● En línea · Cierre de Reservas 24/7</span>
          </div>
        </div>

        <div id="max-quick-replies">
          ${QUICK_REPLIES.map(q => `<button class="max-quick-reply">${q}</button>`).join('')}
        </div>

        <div id="max-messages">
          <div class="max-msg bot">${formatMd(INITIAL_MSG)}</div>
        </div>

        <div id="max-action-bar"></div>

        <div id="max-input-area">
          <input id="max-input" type="text" placeholder="Escribe tu destino (ej: Machu Picchu, Mateo...)" maxlength="500" autocomplete="off" />
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
    appendMessage('user', text, false);
    showTyping();
    isLoading = true;

    // Generar la cotización de venta completa de 5 componentes
    const salesBundle = buildSalesBundle(text);

    let streamSucceeded = false;
    let fullText = '';

    // Detectar si el cliente ya tiene una reserva confirmada en este navegador
    let clientProfile = {};
    let hasActiveBooking = false;
    try {
      const savedOrder = JSON.parse(localStorage.getItem('lifextreme_last_order') || 'null');
      if (savedOrder && savedOrder.bookingCode) {
        hasActiveBooking = true;
        clientProfile = {
          booking_code: savedOrder.bookingCode,
          passenger_name: localStorage.getItem('lifextreme_user_name') || 'Explorador Lifextreme',
          email: localStorage.getItem('lifextreme_user_email') || '',
          tour_name: (savedOrder.items || []).map(i => i.name).join(' + ') || 'Expedición Lifextreme',
          tour_date: savedOrder.tourDate || '',
          paid_today: savedOrder.paidToday || 0,
          lifecycle_stage: 'RESERVA_CONFIRMADA_PRE_VIAJE'
        };
      }
    } catch (e) {}

    // 1. Intentar con el motor conversacional Serverless (/api/max-chat) o Backend Local (localhost:8000)
    const isLocalHost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const primaryUrl = isLocalHost ? 'http://localhost:8000/webhook/lifextreme' : '/api/max-chat';
    const secondaryUrl = isLocalHost ? '/api/max-chat' : STREAM_ENDPOINT;

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 7000);
      const response = await fetch(primaryUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history, profile: clientProfile }),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (response.ok) {
        const data = await response.json();
        const replyMsg = data.mensaje || data.reply || '';
        if (replyMsg) {
          hideTyping();
          fullText = replyMsg;
          const cardHtml = !hasActiveBooking ? createSalesCardHtml(salesBundle) : '';
          appendMessage('bot', `${formatMd(replyMsg)}${cardHtml}`, true);
          streamSucceeded = true;
        }
      }
    } catch (err) {
      // Intentar endpoint secundario si el primario no respondió
      try {
        const controller2 = new AbortController();
        const timeoutId2 = setTimeout(() => controller2.abort(), 5000);
        const res2 = await fetch(secondaryUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text, history, profile: clientProfile }),
          signal: controller2.signal
        });
        clearTimeout(timeoutId2);
        if (res2.ok) {
          const data2 = await res2.json();
          const replyMsg2 = data2.mensaje || data2.reply || '';
          if (replyMsg2) {
            hideTyping();
            fullText = replyMsg2;
            const cardHtml = !hasActiveBooking ? createSalesCardHtml(salesBundle) : '';
            appendMessage('bot', `${formatMd(replyMsg2)}${cardHtml}`, true);
            streamSucceeded = true;
          }
        }
      } catch (e2) {}
    }

    if (!streamSucceeded) {
      hideTyping();
      const smartAnswer = buildIntelligentLocalReply(text, salesBundle, hasActiveBooking, clientProfile);
      fullText = smartAnswer.replace(/<[^>]+>/g, '');
      const cardHtml = !hasActiveBooking ? createSalesCardHtml(salesBundle) : '';
      appendMessage('bot', `${smartAnswer}${cardHtml}`, true);
    }

    // Actualizar historial
    history.push({ role: 'user', content: text });
    history.push({ role: 'assistant', content: fullText || `Información enviada sobre ${salesBundle.title}` });
    if (history.length > 20) history = history.slice(-20);

    isLoading = false;
  }

  function appendMessage(role, text, isHtml = false) {
    const msgs = document.getElementById('max-messages');
    const div  = document.createElement('div');
    div.className = `max-msg ${role}`;
    if (isHtml) {
      div.innerHTML = text;
    } else {
      div.textContent = text;
    }
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
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

  // Funcion global para llevar al usuario del chat al Carrito / Pasarela de Pago
  window.maxAddToCartAndPay = function (tourName, totalPrice, pax, openCheckoutNow) {
    try {
      if (window.useBackpack) {
        const bp = window.useBackpack();
        bp.addItem({
          id: Date.now(),
          name: `${tourName} (${pax} Pax)`,
          price: Number(totalPrice) || 450,
          img: 'assets/images/destinos/cusco/trekking.jpg',
          detail: `${pax} Participante(s) | Asesoría MAX AI`,
          date: new Date().getDate(),
          pax: pax
        });
      }
      if (typeof window.updateCart === 'function') {
        window.updateCart();
      }
      // Cerrar panel de chat MAX para que vea su carrito / pasarela
      isOpen = false;
      document.getElementById('max-chat-panel')?.classList.remove('open');

      // Abrir el drawer del carrito (Mochila Tactica)
      const drawer = document.getElementById('cart-drawer');
      if (drawer) {
        drawer.classList.remove('translate-x-full');
      }

      // Si eligio pagar directo, abrir modal de checkout con plan 30/30/40
      if (openCheckoutNow && typeof window.openStripeCheckout === 'function') {
        setTimeout(() => window.openStripeCheckout(), 350);
      }
    } catch (e) {
      console.error('[MAX Cart] Error agregando al carrito:', e);
    }
  };

  function showPaymentAction(cotizacion) {
    const bar = document.getElementById('max-action-bar');
    if (!bar) return;
    const safeTour = (cotizacion.tour || 'Expedición Lifextreme').replace(/'/g, "\\'");
    const total = Number(cotizacion.precio_total) || 450;
    const pax = Number(cotizacion.pax) || 1;
    const reservaHoy = cotizacion.monto_reserva_hoy || Math.round(total * 0.30);

    bar.style.display = 'flex';
    bar.innerHTML = `
      <button class="max-action-btn payment" onclick="window.maxAddToCartAndPay('${safeTour}', ${total}, ${pax}, true)">
        🛒 Ir a Pagar S/ ${reservaHoy} (30% hoy)
      </button>
      <button class="max-action-btn" onclick="window.maxAddToCartAndPay('${safeTour}', ${total}, ${pax}, false)">
        🎒 Ver en Carrito (S/ ${total})
      </button>
    `;
  }

  // Función global para abrir MAX con un prompt predefinido desde cualquier botón o card
  window.openMaxChatWithPrompt = function (promptText) {
    const btn = document.getElementById('max-chat-btn');
    const panel = document.getElementById('max-chat-panel');
    const input = document.getElementById('max-input');
    if (!isOpen) {
      isOpen = true;
      panel?.classList.add('open');
      btn?.classList.add('active');
    }
    if (promptText && input) {
      input.value = promptText;
      setTimeout(() => {
        sendMessage();
      }, 200);
    }
  };

  // Arrancar cuando el DOM esté listo
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
