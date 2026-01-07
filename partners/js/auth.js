// ============================================
// AUTHENTICATION JAVASCRIPT (SUPABASE VERSION)
// ============================================

// Importar cliente Supabase
import { supabase } from '../../js/supabase-client.js';

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar iconos de Lucide si están disponibles
    if (window.lucide) {
        window.lucide.createIcons();
    }

    initPasswordToggle();
    initLoginForm();
    initRegistroForm();
    checkSession(); // Verificar sesión existente
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

            if (window.lucide) window.lucide.createIcons();
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

            // UI Loading
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Iniciando sesión...';
            submitBtn.disabled = true;

            try {
                // 1. Autenticación con Supabase
                const { data, error } = await supabase.auth.signInWithPassword({
                    email: email,
                    password: password
                });

                if (error) throw error;

                // 2. Verificar perfil de Partner
                const { data: partnerData, error: partnerError } = await supabase
                    .from('partners')
                    .select('*')
                    .eq('user_id', data.user.id)
                    .single();

                // Si no existe perfil de partner, redirigir a registro partner o mostrar aviso
                // (Por simplicidad en este paso, asumimos que si loguea es partner o usuario)

                // 3. Guardar sesión local (opcional, Supabase ya maneja esto, pero para compatibilidad con código viejo)
                const sessionData = {
                    email: data.user.email,
                    id: data.user.id,
                    timestamp: Date.now(),
                    role: partnerData ? 'partner' : 'user',
                    partnerInfo: partnerData || null
                };
                localStorage.setItem('lifextreme_session', JSON.stringify(sessionData));

                showMessage('success', '¡Bienvenido! Redirigiendo al dashboard...');

                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);

            } catch (error) {
                console.error('Login error:', error);
                showMessage('error', error.message || 'Error al iniciar sesión. Verifica tus credenciales.');
            } finally {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        });
    }
}

// ============================================
// REGISTRATION FORM
// ============================================

function initRegistroForm() {
    const registroForm = document.getElementById('registroForm');

    if (registroForm) {
        registroForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(registroForm);
            const nombre = formData.get('nombre'); // Nombre de la empresa o persona
            const email = formData.get('email');
            const password = formData.get('password');
            const confirmPassword = formData.get('confirm_password');
            const terms = formData.get('terms');

            // Validaciones básicas
            if (password !== confirmPassword) {
                showMessage('error', 'Las contraseñas no coinciden');
                return;
            }

            if (!terms) {
                showMessage('error', 'Debes aceptar los términos y condiciones');
                return;
            }

            // UI Loading
            const submitBtn = registroForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Creando cuenta...';
            submitBtn.disabled = true;

            try {
                // 1. Crear usuario en Auth de Supabase
                const { data: authData, error: authError } = await supabase.auth.signUp({
                    email: email,
                    password: password,
                    options: {
                        data: {
                            full_name: nombre // Metadata en Auth
                        }
                    }
                });

                if (authError) throw authError;

                if (authData.user) {
                    // 2. Crear entrada en tabla 'partners'
                    // Nota: Asegúrate de que las políticas RLS permitan insertar aquí o usa una función RPC segura
                    const { error: partnerError } = await supabase
                        .from('partners')
                        .insert([
                            {
                                user_id: authData.user.id, // ID generado por Auth
                                company_name: nombre,
                                company_email: email,
                                status: 'pending' // Estado inicial
                            }
                        ]);

                    if (partnerError) {
                        // Si falla crear el partner pero el usuario se creó, podríamos querer borrar el usuario o manejarlo
                        console.error('Error creando perfil de partner:', partnerError);
                        // Continuamos aunque falle esto para no bloquear al usuario, pero mostramos advertencia
                    }

                    showMessage('success', '¡Cuenta creada con éxito! Por favor verifica tu correo para confirmar.');

                    // Opcional: Auto-login o redirigir a login
                    setTimeout(() => {
                        window.location.href = 'index.html?registered=true';
                    }, 2000);
                }

            } catch (error) {
                console.error('Registration error:', error);
                showMessage('error', error.message || 'Error al registrarse. Intenta nuevamente.');
            } finally {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        });
    }
}

// ============================================
// UTILS
// ============================================

function showMessage(type, message) {
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg text-white text-sm font-medium z-50 transform transition-all duration-300 translate-y-[-20px] opacity-0 flex items-center gap-2`;

    // Set colors based on type
    if (type === 'success') {
        messageDiv.classList.add('bg-green-600');
        messageDiv.innerHTML = `<i data-lucide="check-circle" class="w-5 h-5"></i> ${message}`;
    } else {
        messageDiv.classList.add('bg-red-600');
        messageDiv.innerHTML = `<i data-lucide="alert-circle" class="w-5 h-5"></i> ${message}`;
    }

    document.body.appendChild(messageDiv);

    // Initialize icons
    if (window.lucide) window.lucide.createIcons();

    // Animate in
    setTimeout(() => {
        messageDiv.classList.remove('translate-y-[-20px]', 'opacity-0');
    }, 10);

    // Remove after 3 seconds
    setTimeout(() => {
        messageDiv.classList.add('translate-y-[-20px]', 'opacity-0');
        setTimeout(() => messageDiv.remove(), 300);
    }, 5000);
}

// Check session on load (for login pages, usually we redirect IF logged in)
async function checkSession() {
    const { data: { session } } = await supabase.auth.getSession();

    // Si estamos en login/registro y ya hay sesión, redirigir al dashboard
    const isAuthPage = window.location.pathname.includes('index.html') || window.location.pathname.endsWith('/partners/');

    if (session && isAuthPage) {
        // Opcional: Verificar validez o redirigir
        // window.location.href = 'dashboard.html'; 
    }
}
