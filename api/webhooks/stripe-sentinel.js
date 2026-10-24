// ==============================================================================
// LIFEXTREME SENTINEL VIP — Webhook Stripe Automático (Serverless Vercel)
// Control de Acceso Cero Intervención Humana a Canal VIP de Telegram
// ==============================================================================

import { createClient } from '@supabase/supabase-js';

export default async function handler(req, res) {
    // 1. CORS Preflight
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST');
    res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Stripe-Signature');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método no permitido. Solo POST para webhooks.' });
    }

    const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
    const TELEGRAM_CHANNEL_VIP_ID = process.env.TELEGRAM_CHANNEL_VIP_ID || process.env.TELEGRAM_CHAT_ID;
    const SUPABASE_URL = process.env.SUPABASE_URL;
    const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_KEY;

    // Inicializar Supabase si las credenciales están presentes
    let supabase = null;
    if (SUPABASE_URL && SUPABASE_KEY) {
        supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
    }

    try {
        const event = req.body;
        console.log(`[Stripe Webhook Sentinel] Evento recibido: ${event?.type}`);

        // ======================================================================
        // CASO 1: PAGO EXITOSO / ALTA DE NUEVO SUSCRIPTOR
        // ======================================================================
        if (event.type === 'checkout.session.completed') {
            const session = event.data.object;
            const customerEmail = session.customer_details?.email || session.customer_email || 'sin-email@agencia.com';
            const customerName = session.customer_details?.name || 'Agencia VIP';
            const stripeSubId = session.subscription || session.id;
            const stripeCustomerId = session.customer || null;

            // Extraer Telegram handle desde custom_fields o metadata
            let customerTelegram = null;
            if (Array.isArray(session.custom_fields)) {
                for (const field of session.custom_fields) {
                    if (field.key === 'telegram_user' || field.label?.name?.toLowerCase().includes('telegram')) {
                        customerTelegram = field.text?.value;
                        break;
                    }
                }
            }
            if (!customerTelegram && session.metadata?.telegram_user) {
                customerTelegram = session.metadata.telegram_user;
            }
            if (!customerTelegram) {
                customerTelegram = customerEmail.split('@')[0];
            }

            console.log(`[Stripe Webhook Sentinel] Procesando alta: ${customerName} (${customerEmail}) - Telegram: ${customerTelegram}`);

            let inviteLink = null;

            // 1. Crear enlace de invitación de 1 SOLO USO en Telegram
            if (TELEGRAM_BOT_TOKEN && TELEGRAM_CHANNEL_VIP_ID) {
                try {
                    const expireTimestamp = Math.floor(Date.now() / 1000) + (3600 * 48); // 48 horas de vigencia para el enlace
                    const tgRes = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/createChatInviteLink`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            chat_id: TELEGRAM_CHANNEL_VIP_ID,
                            name: `VIP-${customerTelegram}`.substring(0, 32),
                            member_limit: 1, // Expiración inmediata tras 1 uso
                            expire_date: expireTimestamp
                        })
                    });

                    const tgData = await tgRes.json();
                    if (tgData.ok && tgData.result?.invite_link) {
                        inviteLink = tgData.result.invite_link;
                        console.log(`[Stripe Webhook Sentinel] Enlace de 1 solo uso generado: ${inviteLink}`);
                    } else {
                        console.error('[Stripe Webhook Sentinel] Error de Telegram al crear enlace:', tgData);
                    }
                } catch (tgErr) {
                    console.error('[Stripe Webhook Sentinel] Excepción al invocar Telegram API:', tgErr.message);
                }
            }

            // 2. Guardar registro en Supabase
            if (supabase) {
                try {
                    const { error: dbError } = await supabase.from('sentinel_members').upsert({
                        telegram_user: customerTelegram,
                        email: customerEmail,
                        stripe_customer_id: stripeCustomerId,
                        stripe_sub_id: stripeSubId,
                        invite_link: inviteLink,
                        status: 'active',
                        updated_at: new Date().toISOString()
                    }, { onConflict: 'stripe_sub_id' });

                    if (dbError) {
                        console.error('[Stripe Webhook Sentinel] Error al persistir en Supabase:', dbError);
                    } else {
                        console.log(`[Stripe Webhook Sentinel] Miembro registrado con éxito en base de datos.`);
                    }
                } catch (dbEx) {
                    console.error('[Stripe Webhook Sentinel] Excepción de base de datos:', dbEx.message);
                }
            }

            // 3. Notificar al Admin / Canal de Registro
            if (TELEGRAM_BOT_TOKEN && TELEGRAM_CHANNEL_VIP_ID) {
                try {
                    const notifText = `🎉 <b>NUEVA MEMBRESÍA VIP ACTIVADA</b>\n\n` +
                        `👤 <b>Cliente:</b> ${customerName}\n` +
                        `✉️ <b>Email:</b> ${customerEmail}\n` +
                        `📱 <b>Telegram:</b> @${customerTelegram.replace('@', '')}\n` +
                        `💳 <b>Sub ID:</b> <code>${stripeSubId}</code>\n` +
                        `🔗 <b>Enlace Único:</b> ${inviteLink || 'Generación pendiente'}\n\n` +
                        `<i>🛰️ Sistema Sentinel 100% Autónomo</i>`;

                    await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            chat_id: TELEGRAM_CHANNEL_VIP_ID,
                            text: notifText,
                            parse_mode: 'HTML'
                        })
                    });
                } catch (adminErr) {
                    console.error('[Stripe Webhook Sentinel] Error notificando admin:', adminErr.message);
                }
            }

            return res.status(200).json({
                received: true,
                event: 'checkout.session.completed',
                member: customerTelegram,
                invite_link: inviteLink
            });
        }

        // ======================================================================
        // CASO 2: CANCELACIÓN O IMPAGO (EXPULSIÓN AUTOMÁTICA DEL CANAL)
        // ======================================================================
        if (event.type === 'customer.subscription.deleted' || event.type === 'invoice.payment_failed') {
            const stripeSubId = event.data.object.id || event.data.object.subscription;
            console.warn(`[Stripe Webhook Sentinel] Alerta de baja o impago para Sub ID: ${stripeSubId}`);

            if (supabase && stripeSubId) {
                const { data: member } = await supabase
                    .from('sentinel_members')
                    .select('*')
                    .eq('stripe_sub_id', stripeSubId)
                    .single();

                if (member) {
                    // Actualizar estado en Supabase
                    await supabase
                        .from('sentinel_members')
                        .update({ status: 'canceled', updated_at: new Date().toISOString() })
                        .eq('stripe_sub_id', stripeSubId);

                    // Si se tiene registrado el user_id numérico de Telegram, expulsar
                    if (member.telegram_user_id && TELEGRAM_BOT_TOKEN && TELEGRAM_CHANNEL_VIP_ID) {
                        try {
                            // Ban + Unban revoca el acceso sin bloquear permanentemente
                            await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/banChatMember`, {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    chat_id: TELEGRAM_CHANNEL_VIP_ID,
                                    user_id: member.telegram_user_id
                                })
                            });

                            await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/unbanChatMember`, {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    chat_id: TELEGRAM_CHANNEL_VIP_ID,
                                    user_id: member.telegram_user_id,
                                    only_if_banned: true
                                })
                            });

                            console.log(`[Stripe Webhook Sentinel] Usuario ${member.telegram_user} expulsado automáticamente.`);
                        } catch (kickErr) {
                            console.error('[Stripe Webhook Sentinel] Error al expulsar usuario de Telegram:', kickErr.message);
                        }
                    }
                }
            }

            return res.status(200).json({
                received: true,
                event: event.type,
                status: 'revoked'
            });
        }

        // Cualquier otro evento de Stripe
        return res.status(200).json({ received: true, unhandled_event: event.type });

    } catch (err) {
        console.error('[Stripe Webhook Sentinel Error]:', err);
        return res.status(500).json({ error: err.message });
    }
}
