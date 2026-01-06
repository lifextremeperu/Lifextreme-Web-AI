// ============================================
// AUTHENTICATION JAVASCRIPT
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    initPasswordToggle();
    initLoginForm();
    initRegistroForm();
});

// ============================================
// PASSWORD TOGGLE
// ============================================

function initPasswordToggle() {
    const toggleButtons = document.querySelectorAll('.password-toggle');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const input = button.previousElementSibling;
            const icon = button.querySelector('i');

            if (input.type === 'password') {
                input.type = 'text';
                icon.setAttribute('data-lucide', 'eye-off');
            } else {
                input.type = 'password';
                icon.setAttribute('data-lucide', 'eye');
            }

            lucide.createIcons();
        });
    });
}

// ============================================
// LOGIN FORM
// ============================================

function initLoginForm() {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(loginForm);
            const email = formData.get('email');
            const password = formData.get('password');
            const remember = formData.get('remember');

            // Show loading state
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Iniciando sesión...';
            submitBtn.disabled = true;

            // Simulate API call
            await simulateLogin(email, password, remember);

            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
    }
}

async function simulateLogin(email, password, remember) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Basic validation
    if (!email || !password) {
        showMessage('error', 'Por favor completa todos los campos');
        return;
    }

    // For demo purposes, accept any credentials
    console.log('Login attempt:', { email, password, remember });

    // Store session
    const sessionData = {
        email,
        timestamp: Date.now(),
        name: 'Aventura Extrema',
        role: 'Partner Pro'
    };

    // Always store session (not just when remember is checked)
    localStorage.setItem('lifextreme_session', JSON.stringify(sessionData));

    if (remember) {
        localStorage.setItem('lifextreme_remember', 'true');
    }

    // Show success message
    showMessage('success', '¡Bienvenido! Redirigiendo al dashboard...');

    // Redirect to dashboard after 1 second
    setTimeout(() => {
        window.location.href = 'dashboard.html';
    }, 1000);
}

// ============================================
// REGISTRO FORM
// ============================================

function initRegistroForm() {
    const registroForm = document.getElementById('registroForm');

    if (registroForm) {
        registroForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(registroForm);
            const data = Object.fromEntries(formData);

            // Validate terms acceptance
            if (!data.terms) {
                showMessage('error', 'Debes aceptar los términos y condiciones');
                return;
            }

            // Show loading state
            const submitBtn = registroForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Creando cuenta...';
            submitBtn.disabled = true;

            // Simulate API call
            await simulateRegistro(data);

            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
    }
}

async function simulateRegistro(data) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    console.log('Registro attempt:', data);

    // Store session with registration data
    const sessionData = {
        email: data.email,
        timestamp: Date.now(),
        name: data.empresa || 'Partner',
        role: 'Partner Starter'
    };

    localStorage.setItem('lifextreme_session', JSON.stringify(sessionData));

    // Show success message
    showMessage('success', '¡Cuenta creada exitosamente! Redirigiendo...');

    // Redirect to dashboard after 1 second
    setTimeout(() => {
        window.location.href = 'dashboard.html';
    }, 1000);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function showMessage(type, message) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.success-message, .error-message');
    existingMessages.forEach(msg => msg.remove());

    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `${type}-message show`;
    messageDiv.textContent = message;

    // Insert at the top of the form
    const form = document.querySelector('.auth-form');
    form.insertBefore(messageDiv, form.firstChild);

    // Auto-remove after 5 seconds (except for success messages that redirect)
    if (type !== 'success') {
        setTimeout(() => {
            messageDiv.classList.remove('show');
            setTimeout(() => messageDiv.remove(), 300);
        }, 5000);
    }
}

// ============================================
// SOCIAL LOGIN (DEMO)
// ============================================

document.querySelectorAll('.btn-social').forEach(button => {
    button.addEventListener('click', () => {
        const provider = button.querySelector('span').textContent;
        console.log(`Social login with ${provider}`);
        showMessage('error', `Login con ${provider} estará disponible próximamente`);
    });
});
