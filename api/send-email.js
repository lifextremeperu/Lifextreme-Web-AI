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

        // Validación flexible: el email puede estar en la raíz o en data.personal.email (Elite)
        const userEmail = data.email || (data.personal && data.personal.email);

        if (!data || !userEmail || !data.tipo) {
            return res.status(400).json({ error: 'Faltan campos requeridos: email, tipo' });
        }

        // Verificar credenciales SMTP configuradas
        if (!process.env.ZOHO_USER || !process.env.ZOHO_PASS) {
            console.error('❌ ZOHO_USER o ZOHO_PASS no configurados en env vars');
            return res.status(500).json({ error: 'Configuración de email incompleta' });
        }

        const results = { welcome: null, internal: null };

        if (data.tipo === 'partner_registration') {
            // ... (código existente para partners)
            // 1. Email de bienvenida al partner
            try {
                await transporter.sendMail(buildWelcomeEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; }

            // 2. Alerta interna al equipo
            try {
                await transporter.sendMail(buildInternalAlert(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; }
        } 
        
        else if (data.tipo === 'socio_update') {
            // ... (código para socios)
            try {
                await transporter.sendMail(buildSocioConfirmationEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; }

            try {
                await transporter.sendMail(buildSocioUpdateAlert(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; }
        }

        else if (data.tipo === 'elite_welcome') {
            // 1. Email de bienvenida ELITE al usuario
            try {
                await transporter.sendMail(buildEliteWelcomeEmail(data));
                results.welcome = 'sent';
            } catch (err) { results.welcome = 'failed'; }

            // 2. Alerta interna al equipo
            try {
                await transporter.sendMail(buildEliteInternalAlert(data));
                results.internal = 'sent';
            } catch (err) { results.internal = 'failed'; }
        }

        return res.status(200).json({ 
            success: true, 
            results,
            message: 'Emails procesados'
        });

    } catch (error) {
        console.error('❌ Email handler error:', error);
        return res.status(500).json({ error: 'Error interno del servidor' });
    }
}
