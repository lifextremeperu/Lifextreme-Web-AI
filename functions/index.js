const {onRequest} = require("firebase-functions/v2/https");
const {defineString} = require("firebase-functions/params");
const nodemailer = require("nodemailer");
const cors = require("cors")({origin: true});

// ============================================
// CONFIGURACIÓN DE EMAIL (Cloud Function v2)
// Define estas variables en Firebase Console:
// firebase functions:secrets:set GMAIL_USER
// firebase functions:secrets:set GMAIL_PASS
// ============================================
const GMAIL_USER = defineString("GMAIL_USER");
const GMAIL_PASS = defineString("GMAIL_PASS");
const ADMIN_EMAIL = defineString("ADMIN_EMAIL");

/**
 * API de Email para Lifextreme Partners
 * Endpoint: POST /api/send-email
 *
 * Tipos soportados:
 *   - partner_registration: Email de bienvenida al partner + notificación al admin
 */
exports.sendEmail = onRequest({
  region: "us-central1",
  timeoutSeconds: 30,
}, (req, res) => {
  cors(req, res, async () => {
    // Solo aceptar POST
    if (req.method !== "POST") {
      return res.status(405).json({error: "Método no permitido"});
    }

    const {
      tipo,
      nombre,
      apellido,
      email,
      telefono,
      pais,
      empresa,
      tipo_actividad,
      ruc,
      website,
      descripcion,
      cert_uiagm,
      cert_iso,
      cert_cpr,
      cert_govt,
    } = req.body;

    // Validación básica
    if (!tipo || !email) {
      return res.status(400).json({error: "Faltan campos requeridos: tipo, email"});
    }

    // Configurar transporter de Gmail
    const transporter = nodemailer.createTransport({
      service: "gmail",
      auth: {
        user: GMAIL_USER.value(),
        pass: GMAIL_PASS.value(),
      },
    });

    // ============================================
    // EMAIL: REGISTRO DE PARTNER
    // ============================================
    if (tipo === "partner_registration") {
      const certsList = [
        cert_uiagm === "on" ? "✅ UIAGM / IFMGA" : null,
        cert_iso === "on" ? "✅ ISO 21101 (Aventura)" : null,
        cert_cpr === "on" ? "✅ Primeros Auxilios / CPR" : null,
        cert_govt === "on" ? "✅ Licencia Gubernamental" : null,
      ].filter(Boolean).join("<br>") || "Ninguna especificada";

      // 1. Email de bienvenida al partner
      const welcomeEmail = {
        from: `"Lifextreme Partners" <${GMAIL_USER.value()}>`,
        to: email,
        subject: "🏔️ ¡Bienvenido a Lifextreme Partners! Tu cuenta está en revisión",
        html: `
          <div style="font-family: 'Outfit', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a0a; color: #ffffff; border-radius: 16px; overflow: hidden;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #ff6b35, #f7c59f); padding: 40px 30px; text-align: center;">
              <h1 style="margin: 0; font-size: 28px; font-weight: 800; color: #0a0a0a;">⚡ LIFEXTREME</h1>
              <p style="margin: 8px 0 0; font-size: 14px; color: #0a0a0a; opacity: 0.8;">PARTNERS PROGRAM</p>
            </div>

            <!-- Body -->
            <div style="padding: 40px 30px;">
              <h2 style="color: #ff6b35; margin-top: 0;">¡Hola, ${nombre}!</h2>
              <p style="color: #ccc; line-height: 1.6;">Hemos recibido tu solicitud para unirte como operador de aventura en <strong style="color: #fff;">Lifextreme Partners</strong>. Aquí tienes un resumen de lo que registraste:</p>
              
              <div style="background: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 24px; margin: 24px 0;">
                <table style="width: 100%; border-collapse: collapse;">
                  <tr><td style="color: #888; padding: 8px 0; width: 40%;">Empresa</td><td style="color: #fff; font-weight: 600;">${empresa}</td></tr>
                  <tr><td style="color: #888; padding: 8px 0;">RUC / Tax ID</td><td style="color: #fff;">${ruc || "No especificado"}</td></tr>
                  <tr><td style="color: #888; padding: 8px 0;">Actividad Principal</td><td style="color: #fff;">${tipo_actividad || "No especificado"}</td></tr>
                  <tr><td style="color: #888; padding: 8px 0;">País</td><td style="color: #fff;">${pais || "No especificado"}</td></tr>
                  <tr><td style="color: #888; padding: 8px 0;">Teléfono</td><td style="color: #fff;">${telefono || "No especificado"}</td></tr>
                  <tr><td style="color: #888; padding: 8px 0;">Web</td><td style="color: #fff;">${website || "No especificado"}</td></tr>
                  <tr><td style="color: #888; padding: 8px 0; vertical-align: top;">Certificaciones</td><td style="color: #fff;">${certsList}</td></tr>
                </table>
              </div>

              <div style="background: #1a2f1a; border: 1px solid #2d5a2d; border-radius: 12px; padding: 20px; margin: 24px 0;">
                <p style="margin: 0; color: #4ade80;">⏱️ <strong>Próximos pasos:</strong> Nuestro equipo revisará tu solicitud en las próximas <strong>24 horas</strong>. Recibirás un segundo email con el acceso a tu dashboard.</p>
              </div>

              <p style="color: #888; font-size: 13px;">¿Tienes preguntas? Escríbenos a <a href="mailto:partners@lifextreme.com" style="color: #ff6b35;">partners@lifextreme.com</a></p>
            </div>

            <!-- Footer -->
            <div style="background: #111; padding: 20px 30px; text-align: center; border-top: 1px solid #222;">
              <p style="margin: 0; color: #555; font-size: 12px;">© 2026 Lifextreme. Todos los derechos reservados.</p>
            </div>
          </div>
        `,
      };

      // 2. Notificación al admin
      const adminEmail = {
        from: `"Sistema Lifextreme" <${GMAIL_USER.value()}>`,
        to: ADMIN_EMAIL.value(),
        subject: `🆕 Nuevo Partner Registrado: ${empresa} — ${tipo_actividad}`,
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #ff6b35;">🏔️ Nuevo Partner Solicitante</h2>
            <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
              <tr style="background: #f5f5f5;"><th style="padding: 12px; text-align: left;">Campo</th><th style="padding: 12px; text-align: left;">Valor</th></tr>
              <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">Nombre</td><td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>${nombre} ${apellido}</strong></td></tr>
              <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">Email</td><td style="padding: 10px; border-bottom: 1px solid #eee;">${email}</td></tr>
              <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">Empresa</td><td style="padding: 10px; border-bottom: 1px solid #eee;">${empresa}</td></tr>
              <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">RUC</td><td style="padding: 10px; border-bottom: 1px solid #eee;">${ruc}</td></tr>
              <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">Actividad</td><td style="padding: 10px; border-bottom: 1px solid #eee;">${tipo_actividad}</td></tr>
              <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">País</td><td style="padding: 10px; border-bottom: 1px solid #eee;">${pais}</td></tr>
              <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">Teléfono</td><td style="padding: 10px; border-bottom: 1px solid #eee;">${telefono}</td></tr>
              <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">Descripción</td><td style="padding: 10px; border-bottom: 1px solid #eee;">${descripcion}</td></tr>
            </table>
            <p style="margin-top: 20px;"><a href="https://supabase.com" style="background: #ff6b35; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none;">Ver en Supabase Dashboard</a></p>
          </div>
        `,
      };

      try {
        await transporter.sendMail(welcomeEmail);
        await transporter.sendMail(adminEmail);
        return res.status(200).json({success: true, message: "Emails enviados correctamente"});
      } catch (err) {
        console.error("Error enviando email:", err);
        return res.status(500).json({error: "Error al enviar email", detail: err.message});
      }
    }

    return res.status(400).json({error: `Tipo de email desconocido: ${tipo}`});
  });
});
