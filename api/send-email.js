// ============================================
// LIFEXTREME — Vercel Serverless Email Function
// Vía: Zoho SMTP (smtp.zoho.com:465)
// Destino: contacto@lifextreme.store
// ============================================

import nodemailer from 'nodemailer';

// Configuración SMTP Zoho
const transporter = nodemailer.createTransport({
    host: 'smtp.zoho.com',
    port: 465,
    secure: true, // SSL
    auth: {
        user: process.env.ZOHO_USER, // contacto@lifextreme.store
        pass: process.env.ZOHO_PASS  // App Password de Zoho
    }
});

// ── Digital Gift Card (Para el DESTINATARIO) ─────────────────────────────────
function buildGiftCardEmail(data) {
    const giftCode = `LXG-${Math.random().toString(36).substr(2, 6).toUpperCase()}`;
    const themes = {
        bday: { bg: 'linear-gradient(135deg, #ec4899 0%, #d946ef 100%)', title: '¡Feliz Cumpleaños!' },
        love: { bg: 'linear-gradient(135deg, #ef4444 0%, #f43f5e 100%)', title: '¡Feliz Aniversario!' },
        xmas: { bg: 'linear-gradient(135deg, #059669 0%, #047857 100%)', title: '¡Feliz Navidad!' },
        surprise: { bg: 'linear-gradient(135deg, #4338ca 0%, #4f46e5 100%)', title: '¡Sorpresa Adventure!' }
    };
    const theme = themes[data.theme] || themes.surprise;

    return {
        from: `"Lifextreme Gifts" <${process.env.ZOHO_USER}>`,
        to: data.recipientEmail,
        subject: `🎁 ¡${data.buyerName} te ha enviado una Adventure Card de Lifextreme!`,
        html: `
        <!DOCTYPE html>
        <html lang="es">
        <head><meta charset="UTF-8"></head>
        <body style="margin:0;padding:40px 20px;background:#0f172a;font-family:'Outfit',Arial,sans-serif;color:#ffffff;text-align:center;">
          <div style="max-width:400px;margin:0 auto;background:#ffffff;border-radius:32px;overflow:hidden;box-shadow:0 25px 50px -12px rgba(0,0,0,0.5);">
            <!-- Card Visual -->
            <div style="background:${theme.bg};padding:48px 32px;color:#ffffff;position:relative;">
              <div style="font-size:10px;font-weight:900;letter-spacing:4px;text-transform:uppercase;opacity:0.8;margin-bottom:20px;">Adventure Card</div>
              <div style="font-size:18px;font-weight:900;font-style:italic;margin-bottom:40px;">LIFE<span style="opacity:0.7;">XTREME</span></div>
              
              <h1 style="font-size:32px;font-weight:900;margin:0 0 8px;font-style:italic;">${theme.title}</h1>
              <div style="font-size:48px;font-weight:900;margin:16px 0;">S/ ${data.amount}</div>
              
              <p style="font-size:14px;font-style:italic;opacity:0.9;line-height:1.6;margin:24px 0;">"${data.message || 'Prepárate para la aventura de tu vida.'}"</p>
              
              <div style="margin-top:40px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.2);font-size:12px;opacity:0.8;">
                De: <strong style="color:#ffffff;">${data.buyerName}</strong>
              </div>
            </div>
            
            <!-- Redención Info -->
            <div style="padding:40px 32px;background:#ffffff;color:#1e293b;">
              <div style="background:#f8fafc;border-radius:16px;padding:20px;margin-bottom:24px;border:1px dashed #cbd5e1;">
                <p style="font-size:10px;font-weight:900;color:#94a3b8;margin:0 0 8px;text-transform:uppercase;">Tu Código de Canje</p>
                <div style="font-size:24px;font-weight:900;color:#1e293b;letter-spacing:2px;font-family:monospace;">${giftCode}</div>
              </div>
              
              <h2 style="font-size:18px;font-weight:900;margin:0 0 12px;">¿Cómo usar tu regalo?</h2>
              <p style="font-size:13px;color:#64748b;line-height:1.6;margin-bottom:28px;">
                Cualquier aventura que veas en <strong>lifextreme.store</strong> puede ser tuya. Al reservar, solo presenta este código o contáctanos directamente.
              </p>
              
              <a href="https://www.lifextreme.store" style="display:inline-block;background:#1e293b;color:#ffffff;text-decoration:none;padding:14px 28px;border-radius:12px;font-weight:900;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Explorar Rutas →</a>
            </div>
          </div>
          <p style="color:#475569;font-size:11px;margin-top:32px;">© 2026 Lifextreme Adventures · El regalo de la libertad.</p>
        </body>
        </html>
        `
    };
}

// ── Confirmación de Compra de Gift Card (Para el COMPRADOR) ─────────────────
function buildGiftBuyerConfirmationEmail(data) {
    return {
        from: `"Lifextreme Payments" <${process.env.ZOHO_USER}>`,
        to: data.buyerEmail,
        subject: `✅ Tu regalo para ${data.recipientName} ha sido enviado`,
        html: `
        <div style="font-family:sans-serif;max-width:500px;margin:0 auto;background:#f8fafc;padding:40px 20px;border-radius:24px;">
            <div style="background:#ffffff;border-radius:20px;padding:32px;border:1px solid #e2e8f0;text-align:center;">
                <div style="font-size:40px;margin-bottom:20px;">🤘</div>
                <h1 style="font-size:20px;font-weight:900;color:#1e293b;margin:0 0 12px;">¡Gracias, ${data.buyerName}!</h1>
                <p style="color:#64748b;font-size:14px;line-height:1.6;margin-bottom:24px;">
                    Has enviado un regalo increíble. La Adventure Card por <strong>S/ ${data.amount}</strong> ya está en la bandeja de entrada de <strong>${data.recipientName}</strong>.
                </p>
                <div style="background:#f1f5f9;border-radius:12px;padding:16px;margin-bottom:24px;">
                    <p style="font-size:11px;color:#94a3b8;margin:0 0 4px;text-transform:uppercase;">Destinatario:</p>
                    <p style="font-size:14px;color:#1e293b;font-weight:700;margin:0;">${data.recipientEmail}</p>
                </div>
                <p style="color:#94a3b8;font-size:11px;">Te hemos enviado una copia del recibo de esta transacción.</p>
            </div>
        </div>
        `
    };
}

// ── Email de bienvenida al PARTNER ──────────────────────────────────────────
function buildWelcomeEmail(data) {
    return {
        from: `"Lifextreme" <${process.env.ZOHO_USER}>`,
        to: data.email,
        subject: `¡Bienvenido a Lifextreme Partners, ${data.nombre}! 🏔️`,
        html: `
        <!DOCTYPE html>
        <html lang="es">
        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
        <body style="margin:0;padding:0;background:#f8fafc;font-family:'Segoe UI',Arial,sans-serif;">
          <div style="max-width:600px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
            
            <!-- Header -->
            <div style="background:linear-gradient(135deg,#1e293b 0%,#334155 100%);padding:40px 32px;text-align:center;">
              <div style="font-size:32px;font-weight:900;font-style:italic;color:#ffffff;letter-spacing:-1px;">
                LIFE<span style="color:#f59e0b;">XTREME</span>
              </div>
              <div style="color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:4px;text-transform:uppercase;margin-top:6px;">Partners Program</div>
            </div>

            <!-- Body -->
            <div style="padding:40px 32px;">
              <h1 style="font-size:24px;font-weight:900;color:#1e293b;margin:0 0 12px;">
                ¡Bienvenido, ${data.nombre}! 🎉
              </h1>
              <p style="color:#64748b;font-size:15px;line-height:1.6;margin:0 0 24px;">
                Tu registro como partner de <strong>Lifextreme</strong> ha sido recibido exitosamente. 
                Nuestro equipo revisará tu perfil en las próximas <strong>24 horas</strong>.
              </p>

              <!-- Status Box -->
              <div style="background:#fef3c7;border-left:4px solid #f59e0b;border-radius:8px;padding:16px 20px;margin:0 0 28px;">
                <div style="font-size:12px;font-weight:700;color:#92400e;text-transform:uppercase;letter-spacing:1px;">Estado de tu solicitud</div>
                <div style="font-size:20px;font-weight:900;color:#78350f;margin-top:4px;">⏳ En Revisión</div>
                <div style="font-size:13px;color:#92400e;margin-top:4px;">Activación estimada: 24 horas hábiles</div>
              </div>

              <!-- Partner Details -->
              <div style="background:#f8fafc;border-radius:12px;padding:20px 24px;margin:0 0 28px;">
                <div style="font-size:11px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:2px;margin-bottom:16px;">Datos de tu registro</div>
                <table style="width:100%;border-collapse:collapse;">
                  <tr><td style="padding:6px 0;color:#64748b;font-size:13px;width:40%;">Empresa</td><td style="padding:6px 0;color:#1e293b;font-weight:700;font-size:13px;">${data.empresa}</td></tr>
                  <tr><td style="padding:6px 0;color:#64748b;font-size:13px;">Email</td><td style="padding:6px 0;color:#1e293b;font-weight:700;font-size:13px;">${data.email}</td></tr>
                  <tr><td style="padding:6px 0;color:#64748b;font-size:13px;">Actividad</td><td style="padding:6px 0;color:#1e293b;font-weight:700;font-size:13px;">${data.tipo_actividad || 'No especificado'}</td></tr>
                  <tr><td style="padding:6px 0;color:#64748b;font-size:13px;">País</td><td style="padding:6px 0;color:#1e293b;font-weight:700;font-size:13px;">${data.pais || 'No especificado'}</td></tr>
                  <tr><td style="padding:6px 0;color:#64748b;font-size:13px;">RUC / Tax ID</td><td style="padding:6px 0;color:#1e293b;font-weight:700;font-size:13px;">${data.ruc || 'No especificado'}</td></tr>
                </table>
              </div>

              <!-- Próximos pasos -->
              <div style="margin:0 0 28px;">
                <div style="font-size:13px;font-weight:700;color:#1e293b;margin-bottom:12px;">📋 ¿Qué sigue?</div>
                <div style="display:flex;align-items:flex-start;margin-bottom:10px;">
                  <span style="background:#f59e0b;color:#fff;border-radius:50%;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;margin-right:12px;">1</span>
                  <span style="color:#475569;font-size:13px;line-height:1.5;">Nuestro equipo revisará tus certificaciones y datos empresariales.</span>
                </div>
                <div style="display:flex;align-items:flex-start;margin-bottom:10px;">
                  <span style="background:#f59e0b;color:#fff;border-radius:50%;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;margin-right:12px;">2</span>
                  <span style="color:#475569;font-size:13px;line-height:1.5;">Recibirás un email de activación con tus credenciales de acceso al dashboard.</span>
                </div>
                <div style="display:flex;align-items:flex-start;">
                  <span style="background:#f59e0b;color:#fff;border-radius:50%;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;margin-right:12px;">3</span>
                  <span style="color:#475569;font-size:13px;line-height:1.5;">Comenzarás a recibir reservas y gestionar tus tours desde el panel de partners.</span>
                </div>
              </div>

              <!-- CTA -->
              <div style="text-align:center;margin:32px 0;">
                <a href="https://www.lifextreme.store/partners/login.html" 
                   style="background:#1e293b;color:#ffffff;text-decoration:none;padding:14px 36px;border-radius:50px;font-weight:900;font-size:13px;letter-spacing:1px;text-transform:uppercase;display:inline-block;">
                  Acceder al Panel →
                </a>
              </div>

              <p style="color:#94a3b8;font-size:12px;text-align:center;margin:0;">
                ¿Tienes preguntas? Escríbenos a 
                <a href="mailto:contacto@lifextreme.store" style="color:#f59e0b;">contacto@lifextreme.store</a>
              </p>
            </div>

            <!-- Footer -->
            <div style="background:#f8fafc;padding:20px 32px;text-align:center;border-top:1px solid #e2e8f0;">
              <p style="color:#94a3b8;font-size:11px;margin:0;">© 2026 Lifextreme Adventures · Cusco, Perú</p>
              <p style="color:#cbd5e1;font-size:10px;margin:6px 0 0;">www.lifextreme.store</p>
            </div>
          </div>
        </body>
        </html>
        `
    };
}

// ── Alerta interna al equipo Lifextreme ─────────────────────────────────────
function buildInternalAlert(data) {
    const certs = Object.entries({
        'UIAGM/IFMGA': data.cert_uiagm,
        'ISO 21101': data.cert_iso,
        'Primeros Auxilios/CPR': data.cert_cpr,
        'Licencia Gubernamental': data.cert_govt
    }).filter(([, v]) => v === 'on').map(([k]) => k).join(', ') || 'Ninguna marcada';

    return {
        from: `"Lifextreme Web" <${process.env.ZOHO_USER}>`,
        to: process.env.ZOHO_USER, // contacto@lifextreme.store
        replyTo: data.email,
        subject: `🏔️ NUEVO PARTNER: ${data.empresa} (${data.pais}) — Revisión Pendiente`,
        html: `
        <!DOCTYPE html>
        <html lang="es">
        <head><meta charset="UTF-8"></head>
        <body style="margin:0;padding:0;background:#0f172a;font-family:'Segoe UI',Arial,sans-serif;">
          <div style="max-width:600px;margin:0 auto;background:#1e293b;border-radius:12px;overflow:hidden;">
            
            <!-- Header -->
            <div style="background:#f59e0b;padding:20px 28px;display:flex;align-items:center;">
              <div style="font-size:24px;margin-right:12px;">🏔️</div>
              <div>
                <div style="font-size:16px;font-weight:900;color:#1e293b;">NUEVO PARTNER REGISTRADO</div>
                <div style="font-size:11px;color:#78350f;font-weight:700;">${new Date().toLocaleString('es-PE', {timeZone:'America/Lima'})}</div>
              </div>
            </div>

            <!-- Datos del Partner -->
            <div style="padding:28px;">
              <table style="width:100%;border-collapse:collapse;">
                <tr style="border-bottom:1px solid #334155;">
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;width:35%;">EMPRESA</td>
                  <td style="padding:10px 0;color:#f1f5f9;font-weight:700;font-size:14px;">${data.empresa}</td>
                </tr>
                <tr style="border-bottom:1px solid #334155;">
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;">CONTACTO</td>
                  <td style="padding:10px 0;color:#f1f5f9;font-weight:700;font-size:14px;">${data.nombre} ${data.apellido || ''}</td>
                </tr>
                <tr style="border-bottom:1px solid #334155;">
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;">EMAIL</td>
                  <td style="padding:10px 0;"><a href="mailto:${data.email}" style="color:#f59e0b;font-weight:700;font-size:13px;">${data.email}</a></td>
                </tr>
                <tr style="border-bottom:1px solid #334155;">
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;">TELÉFONO</td>
                  <td style="padding:10px 0;color:#f1f5f9;font-weight:700;font-size:13px;">${data.telefono || 'No proporcionado'}</td>
                </tr>
                <tr style="border-bottom:1px solid #334155;">
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;">PAÍS</td>
                  <td style="padding:10px 0;color:#f1f5f9;font-size:13px;">${data.pais || 'No especificado'}</td>
                </tr>
                <tr style="border-bottom:1px solid #334155;">
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;">ACTIVIDAD</td>
                  <td style="padding:10px 0;color:#34d399;font-weight:700;font-size:13px;">${data.tipo_actividad || 'No especificado'}</td>
                </tr>
                <tr style="border-bottom:1px solid #334155;">
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;">RUC / TAX ID</td>
                  <td style="padding:10px 0;color:#f1f5f9;font-size:13px;">${data.ruc || 'No proporcionado'}</td>
                </tr>
                <tr style="border-bottom:1px solid #334155;">
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;">WEBSITE</td>
                  <td style="padding:10px 0;"><a href="${data.website || '#'}" style="color:#60a5fa;font-size:13px;">${data.website || 'No proporcionado'}</a></td>
                </tr>
                <tr style="border-bottom:1px solid #334155;">
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;">CERTIFICACIONES</td>
                  <td style="padding:10px 0;color:#fbbf24;font-size:13px;font-weight:700;">${certs}</td>
                </tr>
                <tr>
                  <td style="padding:10px 0;color:#94a3b8;font-size:12px;vertical-align:top;">DESCRIPCIÓN</td>
                  <td style="padding:10px 0;color:#cbd5e1;font-size:13px;line-height:1.5;">${data.descripcion || 'Sin descripción'}</td>
                </tr>
              </table>

              <!-- Acciones -->
              <div style="margin-top:24px;display:flex;gap:12px;flex-wrap:wrap;">
                <a href="mailto:${data.email}?subject=Tu registro en Lifextreme Partners - Próximos pasos"
                   style="background:#f59e0b;color:#1e293b;text-decoration:none;padding:10px 20px;border-radius:8px;font-weight:900;font-size:12px;letter-spacing:1px;text-transform:uppercase;">
                  Responder al Partner →
                </a>
              </div>
            </div>

            <div style="padding:16px 28px;border-top:1px solid #334155;text-align:center;">
              <p style="color:#475569;font-size:11px;margin:0;">Lifextreme Web System · contacto@lifextreme.store</p>
            </div>
          </div>
        </body>
        </html>
        `
    };
}

// ── Pase de Abordaje TÁCTICO (Confirmación de Reserva) ─────────────────────
function buildBookingConfirmationEmail(data) {
    const bookingId = Math.random().toString(36).substr(2, 9).toUpperCase();
    return {
        from: `"Lifextreme Command" <${process.env.ZOHO_USER}>`,
        to: data.email,
        subject: `🎫 BOARDING PASS: ${data.tourName} - ${data.date}`,
        html: `
        <div style="font-family:'Courier New', Courier, monospace;max-width:600px;margin:0 auto;background:#000000;color:#00ff00;border:2px solid #00ff00;padding:0;overflow:hidden;">
            <div style="background:#00ff00;color:#000000;padding:15px;text-align:center;font-weight:900;letter-spacing:5px;">
                CONFIRMED EXPEDITION
            </div>
            
            <div style="padding:30px;">
                <div style="border-bottom:1px dashed #00ff00;padding-bottom:20px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-size:10px;text-transform:uppercase;">Explorador Principal</div>
                        <div style="font-size:18px;font-weight:bold;">${data.fullName}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px;text-transform:uppercase;">ID de Misión</div>
                        <div style="font-size:18px;font-weight:bold;">${bookingId}</div>
                    </div>
                </div>

                <div style="display:grid;margin-bottom:30px;">
                    <div style="margin-bottom:15px;">
                        <div style="font-size:10px;text-transform:uppercase;">Objetivo / Tour</div>
                        <div style="font-size:22px;font-weight:900;font-style:italic;">${data.tourName}</div>
                    </div>
                    
                    <div style="background:rgba(0,255,0,0.1);padding:15px;border-left:4px solid #00ff00;">
                        <div style="font-size:14px;margin-bottom:5px;">📅 DEPLOYMENT: <b>${data.date}</b></div>
                        <div style="font-size:14px;margin-bottom:5px;">👥 EXPLORADORES: <b>${data.pax}</b></div>
                        <div style="font-size:14px;">📍 STATUS: <b>PRE-ALPHA ACTIVATED</b></div>
                    </div>
                </div>

                <!-- QR MOCK -->
                <div style="text-align:center;margin:30px 0;">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=${bookingId}&color=00ff00&bgcolor=000000" style="border:1px solid #00ff00;padding:10px;" alt="Tactical QR">
                    <div style="font-size:10px;margin-top:10px;letter-spacing:2px;">SECURE CHECK-IN CODE</div>
                </div>

                <div style="font-size:12px;line-height:1.4;border-top:1px dashed #00ff00;padding-top:20px;">
                    <p><b>NOTAS DE CAMPO:</b> Presenta este pase digital a tu guía asignado. Asegúrate de llevar equipo táctico recomendado y estar en el punto de extracción 15 min antes.</p>
                </div>
            </div>
            
            <div style="background:#111;padding:10px;text-align:center;font-size:9px;color:#008800;letter-spacing:1px;">
                SYSTEM GENERATED · NO SIGNATURE REQUIRED · ENCRYPTED DATA
            </div>
        </div>`
    };
}

function buildBookingInternalAlert(data) {
    return {
        from: `"Command Center" <${process.env.ZOHO_USER}>`,
        to: process.env.ZOHO_USER,
        subject: `🚀 NUEVA OPERACIÓN ACTIVADA: ${data.tourName}`,
        html: `
        <div style="font-family:sans-serif;padding:20px;background:#000;">
            <div style="background:#111;color:#fff;padding:24px;border:1px solid #333;border-radius:12px;">
                <h2 style="color:#0f0;">Nueva Reserva de Tour</h2>
                <hr style="border-color:#333;">
                <p><b>Cliente:</b> ${data.fullName}</p>
                <p><b>Email:</b> ${data.email}</p>
                <p><b>Tour:</b> ${data.tourName}</p>
                <p><b>Fecha:</b> ${data.date}</p>
                <p><b>Pax:</b> ${data.pax}</p>
                <p><b>WhatsApp:</b> ${data.phone}</p>
            </div>
        </div>`
    };
}

// ── Bienvenida INVERSIONISTA (Preventa Lifecoins) ───────────────────────────
function buildPresaleWelcomeEmail(data) {
    return {
        from: `"Lifextreme Finance" <${process.env.ZOHO_USER}>`,
        to: data.email,
        subject: `📀 CERTIFICADO DE FUNDADOR: ${data.full_name}`,
        html: `
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;background:#0f172a;border-radius:24px;overflow:hidden;color:#ffffff;border:1px solid #f59e0b;">
            <div style="padding:48px 32px;text-align:center;background:linear-gradient(135deg, #f59e0b 0%, #d97706 100%);color:#0f172a;">
                <div style="font-size:12px;font-weight:900;letter-spacing:4px;margin-bottom:16px;text-transform:uppercase;">Intención de Inversión Registrada</div>
                <h1 style="font-size:32px;font-weight:900;font-style:italic;margin:0;line-height:1.2;">BIENVENIDO,<br>FUNDADOR</h1>
            </div>
            <div style="padding:40px 32px;background:#0f172a;color:#ffffff;">
                <p style="font-size:16px;line-height:1.6;margin-bottom:24px;">
                    ¡Felicidades <b>${data.full_name}</b>!<br><br>
                    Has tomado una posición estratégica en el futuro de la aventura en los Andes. Hemos registrado tu intención de inversión para el paquete <b>${data.package_name.toUpperCase()}</b>.
                </p>
                
                <div style="background:rgba(245,158,11,0.1);border-radius:16px;padding:24px;margin-bottom:32px;border:1px solid rgba(245,158,11,0.3);">
                    <h3 style="margin-top:0;font-size:14px;text-transform:uppercase;color:#f59e0b;">Detalles del Paquete</h3>
                    <div style="font-size:14px;margin-top:10px;">
                        • <b>Créditos:</b> ${data.lifecoins} Lifecoins<br>
                        • <b>Inversión:</b> $${data.amount_usd} USD<br>
                        • <b>Método:</b> ${data.payment_method.toUpperCase()}
                    </div>
                </div>

                <div style="background:#1e293b;border-radius:12px;padding:20px;text-align:center;margin-bottom:32px;">
                    <p style="margin:0;font-size:14px;color:#cbd5e1;"><b>¿Qué sigue?</b> Una vez validado tu pago, tus Lifecoins serán cargados a tu cuenta y recibirás tu <b>Badge de Fundador</b> digital.</p>
                </div>

                <div style="text-align:center;">
                    <p style="font-size:12px;color:#94a3b8;margin-bottom:16px;">Si aún no completaste el pago vía ${data.payment_method}, puedes contactar a soporte:</p>
                    <a href="https://wa.me/51999999999" style="display:inline-block;background:#22c55e;color:#ffffff;padding:14px 28px;border-radius:12px;font-weight:900;text-decoration:none;text-transform:uppercase;font-size:12px;">Hablar con un Asesor</a>
                </div>
            </div>
            <div style="padding:32px;text-align:center;color:#475569;font-size:11px;">
                © 2026 Lifextreme Founders Program · Safe and Bold
            </div>
        </div>`
    };
}

function buildPresaleInternalAlert(data) {
    return {
        from: `"Lifextreme Sales" <${process.env.ZOHO_USER}>`,
        to: process.env.ZOHO_USER,
        subject: `💰 NUEVA INTENCIÓN DE COMPRA: $${data.amount_usd} USD`,
        html: `
        <div style="font-family:sans-serif;padding:24px;background:#f8fafc;">
            <div style="background:#fff;padding:24px;border-radius:12px;border:1px solid #e2e8f0;">
                <h2 style="color:#1e293b;margin-top:0;">Nueva Intención de Inversión</h2>
                <hr style="border:0;border-top:1px solid #e2e8f0;margin:20px 0;">
                <p><b>Inversor:</b> ${data.full_name}</p>
                <p><b>Email:</b> ${data.email}</p>
                <p><b>WhatsApp:</b> ${data.phone}</p>
                <p><b>País:</b> ${data.country}</p>
                <p><b>Paquete:</b> ${data.package_name}</p>
                <p><b>Monto:</b> $${data.amount_usd} USD</p>
                <p><b>Método:</b> ${data.payment_method}</p>
            </div>
        </div>`
    };
}

// ── Bienvenida GUÍA (Welcome to the Crew) ───────────────────────────
function buildGuideWelcomeEmail(data) {
    return {
        from: `"Lifextreme Operations" <${process.env.ZOHO_USER}>`,
        to: data.email,
        subject: `🏔️ BIENVENIDO AL EQUIPO: ${data.fullName}`,
        html: `
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #e2e8f0;">
            <div style="background:#4338ca;padding:40px;text-align:center;color:#ffffff;">
                <h1 style="font-size:24px;font-weight:900;margin:0;text-transform:uppercase;letter-spacing:2px;">Welcome to the Crew</h1>
            </div>
            <div style="padding:40px 32px;">
                <h2 style="color:#1e293b;font-size:20px;margin:0 0 16px;">¡Hola, ${data.fullName}!</h2>
                <p style="color:#64748b;line-height:1.6;font-size:15px;margin:0 0 24px;">
                    Gracias por postular al equipo de guías de <b>Lifextreme</b>. Hemos recibido tu ficha técnica y estamos muy emocionados por la posibilidad de colaborar contigo.
                </p>
                <div style="background:#f1f5f9;border-radius:12px;padding:20px;margin-bottom:24px;">
                    <p style="margin:0;font-size:13px;color:#1e293b;"><b>Próximo Paso:</b> Nuestro equipo de operaciones revisará tus certificaciones (<b>${data.certs.join(', ')}</b>) y especialidades. Te contactaremos vía WhatsApp para una breve entrevista técnica.</p>
                </div>
                <p style="color:#64748b;font-size:14px;margin:0;">Atentamente,<br><b>Equipo de Operaciones de Lifextreme</b></p>
            </div>
        </div>`
    };
}

function buildGuideInternalAlert(data) {
    return {
        from: `"Lifextreme Ops" <${process.env.ZOHO_USER}>`,
        to: process.env.ZOHO_USER,
        subject: `🚩 NUEVA POSTULACIÓN DE GUÍA: ${data.fullName}`,
        html: `
        <div style="font-family:sans-serif;padding:24px;background:#fefce8;">
            <div style="background:#fff;padding:24px;border-radius:12px;border:1px solid #fef08a;">
                <h2 style="color:#854d0e;margin-top:0;">Ficha Técnica de Guía</h2>
                <hr style="border:0;border-top:1px solid #fef08a;margin:20px 0;">
                <table style="width:100%;font-size:14px;">
                    <tr><td style="color:#a1a1aa;padding:5px 0;">GUÍA</td><td style="font-weight:700;">${data.fullName}</td></tr>
                    <tr><td style="color:#a1a1aa;padding:5px 0;">DNI/PASS</td><td style="font-weight:700;">${data.dni}</td></tr>
                    <tr><td style="color:#a1a1aa;padding:5px 0;">EXP</td><td style="font-weight:700;">${data.experience}</td></tr>
                    <tr><td style="color:#a1a1aa;padding:5px 0;">CERTIFICADOS</td><td style="font-weight:700;color:#4338ca;">${data.certs.join(', ')}</td></tr>
                    <tr><td style="color:#a1a1aa;padding:5px 0;">ESPECIALIDADES</td><td style="font-weight:700;">${data.specialties.join(', ')}</td></tr>
                    <tr><td style="color:#a1a1aa;padding:5px 0;">WHATSAPP</td><td style="font-weight:700;">${data.phone}</td></tr>
                </table>
            </div>
        </div>`
    };
}

// ── Bienvenida ELITE (Activación de Cuenta Socio) ───────────────────────────
function buildEliteWelcomeEmail(data) {
    return {
        from: `"Lifextreme Elite" <${process.env.ZOHO_USER}>`,
        to: data.personal.email,
        subject: `🚀 BIENVENIDO AL CLUB ELITE: ${data.personal.fullName}`,
        html: `
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;background:#0f172a;border-radius:24px;overflow:hidden;color:#ffffff;">
            <div style="padding:48px 32px;text-align:center;background:linear-gradient(135deg, #1e293b 0%, #0f172a 100%);">
                <div style="font-size:12px;font-weight:900;letter-spacing:4px;color:#f59e0b;margin-bottom:16px;text-transform:uppercase;">Membership Activated</div>
                <h1 style="font-size:32px;font-weight:900;font-style:italic;margin:0;line-height:1.2;">BIENVENIDO A<br><span style="color:#f59e0b;">LIFE</span>XTREME ELITE</h1>
            </div>
            <div style="padding:40px 32px;background:#ffffff;color:#1e293b;">
                <p style="font-size:16px;line-height:1.6;margin-bottom:24px;">
                    ¡Hola <b>${data.personal.fullName}</b>!<br><br>
                    Has dado el paso definitivo. Tu cuenta ha sido elevada al estatus <b>Elite</b>. Nuestra Inteligencia Artificial ya está analizando tus preferencias de <b>${data.adventure.experienceLevel}</b> para diseñar tu próxima gran expedición.
                </p>
                
                <div style="background:#f8fafc;border-radius:16px;padding:24px;margin-bottom:32px;border:1px solid #e2e8f0;">
                    <h3 style="margin-top:0;font-size:14px;text-transform:uppercase;color:#64748b;">Tu Perfil de Aventurero</h3>
                    <div style="font-size:14px;color:#1e293b;margin-top:10px;">
                        • <b>Nivel:</b> ${data.adventure.experienceLevel}<br>
                        • <b>Intereses:</b> ${data.adventure.interests.join(', ')}<br>
                        • <b>Motivación:</b> ${data.preferences.motivation}
                    </div>
                </div>

                <div style="text-align:center;">
                    <a href="https://www.lifextreme.store" style="display:inline-block;background:#f59e0b;color:#ffffff;padding:18px 36px;border-radius:12px;font-weight:900;text-decoration:none;text-transform:uppercase;letter-spacing:1px;font-size:14px;">Explorar Beneficios Elite</a>
                </div>
            </div>
            <div style="padding:32px;text-align:center;color:#64748b;font-size:12px;">
                Cusco, Perú · Safe and Bold Adventures
            </div>
        </div>`
    };
}

function buildEliteInternalAlert(data) {
    return {
        from: `"Lifextreme Elite" <${process.env.ZOHO_USER}>`,
        to: process.env.ZOHO_USER,
        subject: `💎 NUEVO SOCIO ELITE: ${data.personal.fullName}`,
        html: `
        <div style="font-family:sans-serif;padding:24px;background:#f8fafc;">
            <div style="background:#fff;padding:24px;border-radius:12px;border:1px solid #e2e8f0;">
                <h2 style="color:#1e293b;margin-top:0;">Nuevo Socio Elite Activado</h2>
                <hr style="border:0;border-top:1px solid #e2e8f0;margin:20px 0;">
                <p><b>Nombre:</b> ${data.personal.fullName}</p>
                <p><b>Email:</b> ${data.personal.email}</p>
                <p><b>Teléfono:</b> ${data.personal.phone}</p>
                <p><b>Intereses:</b> ${data.adventure.interests.join(', ')}</p>
                <p><b>Motivación:</b> ${data.preferences.motivation}</p>
                <p><b>Regiones:</b> ${data.preferences.regions.join(', ')}</p>
            </div>
        </div>`
    };
}

// ── Confirmación PARA el SOCIO (Confirmación de cambios) ────────────────────
function buildSocioConfirmationEmail(data) {
    return {
        from: `"Lifextreme" <${process.env.ZOHO_USER}>`,
        to: data.email,
        subject: `✅ Perfil Actualizado - Lifextreme Member`,
        html: `
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.05);border:1px solid #e2e8f0;">
            <div style="background:#1e293b;padding:32px;text-align:center;">
                <div style="font-size:24px;font-weight:900;font-style:italic;color:#ffffff;">LIFE<span style="color:#f59e0b;">XTREME</span></div>
            </div>
            <div style="padding:40px 32px;text-align:center;">
                <div style="font-size:48px;margin-bottom:16px;">👤</div>
                <h1 style="font-size:20px;font-weight:900;color:#1e293b;margin:0 0 16px;">¡Hola, ${data.name}!</h1>
                <p style="color:#64748b;font-size:15px;line-height:1.6;margin:0 0 24px;">
                    Te confirmamos que hemos actualizado tus datos de socio correctamente en nuestra plataforma. 
                    Ahora tu perfil está al día para recibir beneficios exclusivos.
                </p>
                <div style="background:#f8fafc;border-radius:12px;padding:20px;display:inline-block;margin-bottom:24px;text-align:left;">
                    <div style="font-size:11px;color:#94a3b8;font-weight:700;margin-bottom:4px;">INTERÉS PRINCIPAL ACTUALIZADO:</div>
                    <div style="color:#1e293b;font-weight:900;text-transform:uppercase;">🏔️ ${data.interest}</div>
                </div>
                <p style="color:#94a3b8;font-size:12px;">Si no realizaste este cambio, por favor contáctanos de inmediato.</p>
            </div>
            <div style="background:#f1f5f9;padding:20px;text-align:center;font-size:11px;color:#94a3b8;">
                © 2026 Lifextreme Adventures · Cusco, Perú
            </div>
        </div>`
    };
}

// ── Alerta interna: Actualización de datos de SOCIO ─────────────────────────
function buildSocioUpdateAlert(data) {
    return {
        from: `"Lifextreme Web" <${process.env.ZOHO_USER}>`,
        to: process.env.ZOHO_USER,
        replyTo: data.email,
        subject: `👤 ACTUALIZACIÓN DE SOCIO: ${data.name}`,
        html: `
        <div style="font-family:sans-serif;padding:24px;background:#f8fafc;">
            <div style="background:#fff;padding:24px;border-radius:12px;border:1px solid #e2e8f0;">
                <h2 style="color:#1e293b;margin-top:0;">Actualización de Perfil de Socio</h2>
                <p style="color:#64748b;">Un socio ha actualizado sus datos desde el sitio web:</p>
                <hr style="border:0;border-top:1px solid #e2e8f0;margin:20px 0;">
                <table style="width:100%;">
                    <tr><td style="color:#94a3b8;font-size:12px;">NOMBRE</td><td style="font-weight:700;">${data.name}</td></tr>
                    <tr><td style="color:#94a3b8;font-size:12px;padding-top:10px;">EMAIL</td><td style="font-weight:700;padding-top:10px;">${data.email}</td></tr>
                    <tr><td style="color:#94a3b8;font-size:12px;padding-top:10px;">INTERESES</td><td style="font-weight:700;padding-top:10px;text-transform:uppercase;">${data.interest}</td></tr>
                </table>
            </div>
        </div>`
    };
}

// ── Reclutamiento (Trabaja con Nosotros) ──────────────────────────────────
function buildJobApplicationEmail(data) {
    return {
        from: `"Lifextreme Careers" <${process.env.ZOHO_USER}>`,
        to: data.email,
        subject: `🚀 Tu aplicación a Lifextreme: ${data.position}`,
        html: `
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;background:#f8fafc;border-radius:24px;overflow:hidden;border:1px solid #e2e8f0;">
            <div style="background:#0f172a;padding:48px 32px;text-align:center;">
                <h1 style="color:#ffffff;font-size:24px;font-weight:900;margin:0;letter-spacing:2px;text-transform:uppercase;">Join the Elite Squad</h1>
            </div>
            <div style="padding:40px 32px;background:#ffffff;">
                <h2 style="color:#1e293b;font-size:20px;margin:0 0 16px;">¡Hola, ${data.fullName}!</h2>
                <p style="color:#64748b;line-height:1.6;font-size:15px;margin:0 0 24px;">
                    Hemos recibido tu aplicación para la posición de <b>${data.position}</b>. En Lifextreme no buscamos empleados, buscamos pioneros dispuestos a redefinir los límites de la aventura.
                </p>
                <div style="background:#f1f5f9;border-radius:12px;padding:20px;margin-bottom:24px;border-left:4px solid #4338ca;">
                    <p style="margin:0;font-size:13px;color:#1e293b;"><b>Estado de Aplicación:</b> Recibida y en revisión por el equipo de operaciones.</p>
                </div>
                <p style="color:#64748b;font-size:14px;margin-bottom:32px;">Si tu perfil encaja con nuestro ADN, nos pondremos en contacto contigo para una entrevista táctica en los próximos días.</p>
                <div style="text-align:center;">
                    <span style="font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:2px;">Safe and Bold · Since 2024</span>
                </div>
            </div>
        </div>`
    };
}

function buildJobInternalAlert(data) {
    return {
        from: `"Lifextreme Careers" <${process.env.ZOHO_USER}>`,
        to: process.env.ZOHO_USER,
        replyTo: data.email,
        subject: `👤 NUEVO TALENTO: ${data.fullName} (${data.position})`,
        html: `
        <div style="font-family:sans-serif;padding:24px;background:#f8fafc;">
            <div style="background:#fff;padding:24px;border-radius:12px;border:1px solid #e2e8f0;">
                <h2 style="color:#4338ca;margin-top:0;">Ficha de Postulante</h2>
                <hr style="border:0;border-top:1px solid #e2e8f0;margin:20px 0;">
                <p><b>Candidato:</b> ${data.fullName}</p>
                <p><b>Email:</b> ${data.email}</p>
                <p><b>Posición:</b> ${data.position}</p>
                <p><b>Pitch:</b> ${data.pitch}</p>
                <p style="font-size:11px;color:#94a3b8;margin-top:20px;">Revisar CV adjunto en el sistema o contactar vía email.</p>
            </div>
        </div>`
    };
}

// ── Handler Principal ────────────────────────────────────────────────────────
export default async function handler(req, res) {
    // Solo POST
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // CORS — permitir desde cualquier subdominio de lifextreme si es necesario
    const origin = req.headers.origin;
    if (origin && (origin.includes('lifextreme.store') || origin.includes('vercel.app'))) {
        res.setHeader('Access-Control-Allow-Origin', origin);
    }
    res.setHeader('Access-Control-Allow-Methods', 'POST');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    try {
        const data = req.body;
        // Limpieza atómica: solo letras y guiones bajos, en minúsculas.
        const tipoRecibido = (data.tipo || '').toLowerCase().replace(/[^a-z_]/g, '').trim();

        // Validación flexible: el email puede estar en la raíz o en data.personal.email (Elite)
        const userEmail = data.email || (data.personal && data.personal.email);

        if (!data || !userEmail || !tipoRecibido) {
            return res.status(400).json({ error: 'Faltan campos requeridos: email, tipo' });
        }

        const results = { welcome: null, internal: null };

        // ── PRIORIDAD 1: RECLUTAMIENTO ──
        if (tipoRecibido.includes('job_application')) {
            try {
                await transporter.sendMail(buildJobApplicationEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; results.errorW = err.message; }

            try {
                await transporter.sendMail(buildJobInternalAlert(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; results.errorI = err.message; }
        }

        // ── PRIORIDAD 3: GIFT CARDS ──
        else if (tipoRecibido.includes('gift_card_confirmation')) {
            try {
                // Al Destinatario
                await transporter.sendMail(buildGiftCardEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; results.errorW = err.message; }

            try {
                // Al Comprador (Confirmación)
                await transporter.sendMail(buildGiftBuyerConfirmationEmail(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; results.errorI = err.message; }
        }

        // ── PRIORIDAD 4: PARTNERS Y OTROS ──
            // ... (código existente)
            try {
                await transporter.sendMail(buildWelcomeEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; }
            try {
                await transporter.sendMail(buildInternalAlert(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; }
        }

        else if (tipoRecibido === 'socio_update') {
            // ...
            try {
                await transporter.sendMail(buildSocioConfirmationEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; }
            try {
                await transporter.sendMail(buildSocioUpdateAlert(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; }
        }

        else if (tipoRecibido === 'elite_welcome') {
            try {
                await transporter.sendMail(buildEliteWelcomeEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; }
            try {
                await transporter.sendMail(buildEliteInternalAlert(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; }
        }

        else if (tipoRecibido === 'presale_welcome') {
            try {
                await transporter.sendMail(buildPresaleWelcomeEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; }
            try {
                await transporter.sendMail(buildPresaleInternalAlert(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; }
        }

        else if (tipoRecibido === 'guide_registration') {
            try {
                await transporter.sendMail(buildGuideWelcomeEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; }
            try {
                await transporter.sendMail(buildGuideInternalAlert(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; }
        }

        return res.status(200).json({ 
            success: true, 
            results,
            debug: { tipoRecibido, version: "2026-04-21-Táctico-Final" },
            message: 'SISTEMA DE MISIÓN ALPHA-1 ACTIVADO'
        });
    } catch (error) {
        console.error('❌ Email handler error:', error);
        return res.status(500).json({ error: 'Error interno del servidor [DEBUG V1]' });
    }
}

// Last Update: 2026-04-21 18:43 (Forced Deploy)
