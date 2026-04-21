/**
 * LIFEXTREME — Universal Forms Handler
 * Maneja el envío de formularios hacia la API de Notificaciones
 */

document.addEventListener('DOMContentLoaded', () => {
    initSocioUpdateForm();
    initGuideRegisterForm();
    // Aquí agregaremos otros handlers (contacto, etc.)
});

/**
 * Handler para Registro de Guía Profesional
 */
function initGuideRegisterForm() {
    const guideForm = document.getElementById('guide-register-form');
    if (!guideForm) return;

    guideForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = guideForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="ri-loader-4-line animate-spin text-xl"></i> PROCESANDO...';

        const formData = new FormData(guideForm);
        const data = {
            tipo: 'guide_registration',
            fullName: formData.get('fullName'),
            dni: formData.get('dni'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            experience: formData.get('experience'),
            certs: formData.getAll('certs'),
            specialties: formData.getAll('specialties')
        };

        try {
            const response = await fetch('/api/send-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                // Redirigir a una página de éxito o mostrar mensaje
                showToast('✅ Solicitud enviada. Revisaremos tu perfil.', 'success');
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 2000);
            } else {
                throw new Error(result.error || 'Error en el servidor');
            }
        } catch (error) {
            console.error('Error en el registro de guía:', error);
            showToast('❌ Error al enviar. Intenta por WhatsApp.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}


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
