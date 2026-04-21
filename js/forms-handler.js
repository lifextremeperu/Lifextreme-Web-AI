/**
 * LIFEXTREME — Universal Forms Handler
 * Maneja el envío de formularios hacia la API de Notificaciones
 */

document.addEventListener('DOMContentLoaded', () => {
    initSocioUpdateForm();
    // Aquí agregaremos otros handlers (guías, contacto, etc.)
});

/**
 * Handler para Actualizar Datos de Socio en index.html
 */
function initSocioUpdateForm() {
    const socioForm = document.getElementById('form-socio-update');
    if (!socioForm) return;

    socioForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = socioForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        // Bloquear botón y mostrar loading
        submitBtn.disabled = true;
        submitBtn.textContent = 'PROCESANDO...';

        const formData = new FormData(socioForm);
        const data = {
            tipo: 'socio_update',
            name: formData.get('name'),
            email: formData.get('email'),
            interest: formData.get('interest')
        };

        try {
            const response = await fetch('/api/send-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                showToast('✅ ¡Datos actualizados! Gracias socio.', 'success');
                socioForm.reset();
            } else {
                throw new Error(result.error || 'Error en el servidor');
            }
        } catch (error) {
            console.error('Error enviando datos de socio:', error);
            showToast('❌ Error al enviar. Intenta por WhatsApp.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
}

/**
 * Utilidad para mostrar notificaciones rápidas
 */
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-8 left-1/2 -translate-x-1/2 px-6 py-3 rounded-2xl font-black text-[10px] tracking-widest uppercase z-[3000] shadow-2xl transition-all duration-500 opacity-0 translate-y-4 ${
        type === 'success' ? 'bg-secondary text-white' : 'bg-red-600 text-white'
    }`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.classList.remove('opacity-0', 'translate-y-4');
    }, 10);

    // Remove after 4s
    setTimeout(() => {
        toast.classList.add('opacity-0', 'translate-y-4');
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}
