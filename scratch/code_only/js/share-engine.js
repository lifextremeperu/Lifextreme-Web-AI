// --- SHARE ENGINE (INVITE A FRIEND FUNCTIONALITY) ---

/**
 * Share Engine Module
 * Permite a los usuarios compartir actividades específicas por WhatsApp
 * con links directos a la página de reserva
 */

const ShareEngine = (function () {
    'use strict';

    // Configuración base
    const config = {
        baseUrl: window.location.origin + window.location.pathname,
        whatsappApiUrl: 'https://wa.me/',
        defaultCountryCode: '51', // Perú
    };

    /**
     * Genera un link directo a una actividad específica
     * @param {string} type - Tipo de actividad ('tour' o 'event')
     * @param {number} id - ID de la actividad
     * @returns {string} URL completa con parámetros
     */
    function generateActivityLink(type, id) {
        const params = new URLSearchParams({
            activity: type,
            id: id,
            ref: 'share'
        });
        return `${config.baseUrl}?${params.toString()}`;
    }

    /**
     * Genera el mensaje de WhatsApp personalizado
     * @param {Object} activity - Objeto con datos de la actividad
     * @param {string} type - Tipo de actividad
     * @returns {string} Mensaje formateado para WhatsApp
     */
    function generateWhatsAppMessage(activity, type) {
        const activityLink = generateActivityLink(type, activity.id);

        const emoji = type === 'tour' ? '🏔️' : '🎯';
        const typeLabel = type === 'tour' ? 'expedición' : 'evento';

        let message = `${emoji} *¡Mira esta increíble ${typeLabel}!*\n\n`;
        message += `📍 *${activity.title}*\n`;
        message += `🌎 ${activity.dept || activity.location}\n`;

        if (activity.duration) {
            message += `⏱️ Duración: ${activity.duration}\n`;
        }

        if (activity.price) {
            message += `💰 Desde S/ ${activity.price}\n`;
        }

        if (activity.date) {
            message += `📅 Fecha: ${activity.date}\n`;
        }

        message += `\n✨ *¿Te animas a esta aventura conmigo?*\n\n`;
        message += `👉 Reserva aquí: ${activityLink}\n\n`;
        message += `_Compartido desde Lifextreme - Tu plataforma de aventuras extremas_`;

        return encodeURIComponent(message);
    }

    /**
     * Abre WhatsApp con el mensaje pre-cargado
     * @param {Object} activity - Datos de la actividad
     * @param {string} type - Tipo de actividad
     * @param {string} phoneNumber - Número de teléfono (opcional)
     */
    function shareViaWhatsApp(activity, type, phoneNumber = '') {
        const message = generateWhatsAppMessage(activity, type);
        let whatsappUrl = config.whatsappApiUrl;

        // Si hay número de teléfono, agregarlo
        if (phoneNumber) {
            // Limpiar el número de caracteres no numéricos
            const cleanNumber = phoneNumber.replace(/\D/g, '');
            whatsappUrl += cleanNumber;
        }

        whatsappUrl += `?text=${message}`;

        // Abrir WhatsApp en nueva ventana
        window.open(whatsappUrl, '_blank');

        // Tracking analytics (opcional)
        trackShareEvent(activity, type);
    }

    /**
     * Copia el link directo al portapapeles
     * @param {string} type - Tipo de actividad
     * @param {number} id - ID de la actividad
     * @returns {Promise<boolean>} True si se copió exitosamente
     */
    async function copyLinkToClipboard(type, id) {
        const link = generateActivityLink(type, id);

        try {
            await navigator.clipboard.writeText(link);
            showNotification('✅ Link copiado al portapapeles', 'success');
            return true;
        } catch (err) {
            // Fallback para navegadores antiguos
            const textArea = document.createElement('textarea');
            textArea.value = link;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            document.body.appendChild(textArea);
            textArea.select();

            try {
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showNotification('✅ Link copiado al portapapeles', 'success');
                return true;
            } catch (err) {
                document.body.removeChild(textArea);
                showNotification('❌ Error al copiar el link', 'error');
                return false;
            }
        }
    }

    /**
     * Muestra una notificación temporal
     * @param {string} message - Mensaje a mostrar
     * @param {string} type - Tipo de notificación ('success', 'error', 'info')
     */
    function showNotification(message, type = 'info') {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `share-notification share-notification-${type}`;
        notification.innerHTML = `
            <div class="share-notification-content">
                <p class="text-xs font-bold">${message}</p>
            </div>
        `;

        // Agregar estilos inline si no existen
        if (!document.getElementById('share-notification-styles')) {
            const style = document.createElement('style');
            style.id = 'share-notification-styles';
            style.textContent = `
                .share-notification {
                    position: fixed;
                    bottom: 24px;
                    right: 24px;
                    background: white;
                    padding: 16px 24px;
                    border-radius: 16px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                    z-index: 9999;
                    animation: slideInUp 0.3s ease-out;
                    border-left: 4px solid #4338ca;
                }
                .share-notification-success {
                    border-left-color: #10b981;
                }
                .share-notification-error {
                    border-left-color: #ef4444;
                }
                @keyframes slideInUp {
                    from {
                        transform: translateY(100px);
                        opacity: 0;
                    }
                    to {
                        transform: translateY(0);
                        opacity: 1;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(notification);

        // Remover después de 3 segundos
        setTimeout(() => {
            notification.style.animation = 'slideInUp 0.3s ease-out reverse';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    /**
     * Tracking de eventos de compartir (para analytics)
     * @param {Object} activity - Datos de la actividad
     * @param {string} type - Tipo de actividad
     */
    function trackShareEvent(activity, type) {
        // Aquí puedes integrar con Google Analytics, Mixpanel, etc.
        if (window.gtag) {
            window.gtag('event', 'share', {
                event_category: 'engagement',
                event_label: `${type}_${activity.id}`,
                value: activity.title
            });
        }

        console.log('📊 Share Event Tracked:', {
            type,
            id: activity.id,
            title: activity.title
        });
    }

    /**
     * Procesa parámetros URL al cargar la página
     * Si hay un parámetro de actividad compartida, abre automáticamente
     */
    function handleIncomingShare() {
        const urlParams = new URLSearchParams(window.location.search);
        const activityType = urlParams.get('activity');
        const activityId = urlParams.get('id');
        const ref = urlParams.get('ref');

        if (activityType && activityId && ref === 'share') {
            // Esperar a que el DOM esté listo
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => {
                    openSharedActivity(activityType, parseInt(activityId));
                });
            } else {
                openSharedActivity(activityType, parseInt(activityId));
            }
        }
    }

    /**
     * Abre la actividad compartida automáticamente
     * @param {string} type - Tipo de actividad
     * @param {number} id - ID de la actividad
     */
    function openSharedActivity(type, id) {
        setTimeout(() => {
            if (type === 'tour') {
                // Navegar a destinos y abrir el modal de booking
                if (typeof navigateTo === 'function') {
                    navigateTo('destinos');
                }
                setTimeout(() => {
                    if (typeof openBooking === 'function') {
                        openBooking(id);
                        showNotification('🎉 ¡Tu amigo te invitó a esta aventura!', 'success');
                    }
                }, 500);
            } else if (type === 'event') {
                // Navegar a eventos y abrir el modal correspondiente
                if (typeof navigateTo === 'function') {
                    navigateTo('eventos');
                }
                setTimeout(() => {
                    if (typeof openEventBooking === 'function') {
                        openEventBooking(id);
                        showNotification('🎉 ¡Tu amigo te invitó a este evento!', 'success');
                    }
                }, 500);
            }
        }, 1000);
    }

    // Inicializar al cargar la página
    handleIncomingShare();

    // API Pública
    return {
        shareViaWhatsApp,
        copyLinkToClipboard,
        generateActivityLink,
        showNotification
    };
})();

// Exponer globalmente
window.ShareEngine = ShareEngine;
