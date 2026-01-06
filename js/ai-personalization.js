// --- AI PERSONALIZATION SYSTEM ---
function openAIPersonalizationModal() {
    document.getElementById('ai-personalization-modal').classList.remove('hidden');
}

function closeAIPersonalizationModal() {
    document.getElementById('ai-personalization-modal').classList.add('hidden');
}

function submitAIProfile(formData) {
    // Store user profile in localStorage for AI personalization
    const userProfile = {
        personal: {
            fullName: formData.get('fullName'),
            email: formData.get('email'),
            age: formData.get('age'),
            phone: formData.get('phone')
        },
        adventure: {
            experienceLevel: formData.get('experienceLevel'),
            interests: formData.getAll('interests'),
            budget: formData.get('budget'),
            travelFrequency: formData.get('travelFrequency')
        },
        preferences: {
            groupType: formData.get('groupType'),
            regions: formData.getAll('regions'),
            motivation: formData.get('motivation')
        },
        createdAt: new Date().toISOString(),
        membershipActivated: true
    };

    // Save to localStorage
    localStorage.setItem('lifextreme_ai_profile', JSON.stringify(userProfile));

    // Save to Supabase (cloud backup)
    if (typeof saveAIProfile === 'function') {
        saveAIProfile(userProfile).catch(err => {
            console.warn('No se pudo guardar en Supabase (continuando con localStorage):', err);
        });
    }

    // Activate membership
    membership.initMembership();

    // Close modal
    closeAIPersonalizationModal();

    // Show success toast with personalized message
    const firstName = userProfile.personal.fullName.split(' ')[0];
    showToast(
        `¡Bienvenido ${firstName}!`,
        'Tu perfil Elite IA ha sido activado. Preparando recomendaciones personalizadas...',
        'ri-sparkling-2-fill'
    );

    // Simulate AI processing
    setTimeout(() => {
        showToast(
            'IA Personalizada Activa',
            `Hemos identificado ${userProfile.adventure.interests.length} intereses. Ajustando ofertas...`,
            'ri-robot-2-line'
        );
    }, 2000);

    // Log for analytics/AI backend integration
    console.log('AI Profile Created:', userProfile);

    // TODO: Send to backend API for AI processing
    // fetch('/api/ai-profile', { method: 'POST', body: JSON.stringify(userProfile) });
}

// Initialize AI Profile Form Handler
document.addEventListener('DOMContentLoaded', () => {
    const aiForm = document.getElementById('ai-profile-form');
    if (aiForm) {
        aiForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            submitAIProfile(formData);
        });
    }
});
