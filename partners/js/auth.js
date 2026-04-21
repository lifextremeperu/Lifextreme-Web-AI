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

            // Extraer todos los campos del formulario
            const nombre        = formData.get('nombre') || '';
            const apellido      = formData.get('apellido') || '';
            const email         = formData.get('email');
            const password      = formData.get('password');
            const confirmPass   = formData.get('password_confirm');
            const telefono      = formData.get('telefono') || '';
            const pais          = formData.get('pais') || '';
            const empresa       = formData.get('empresa') || '';
            const tipo_actividad = formData.get('tipo_actividad') || '';
            const ruc           = formData.get('ruc') || '';
            const website       = formData.get('website') || '';
            const descripcion   = formData.get('descripcion') || '';
            const cert_uiagm    = formData.get('cert_uiagm') || '';
            const cert_iso      = formData.get('cert_iso') || '';
            const cert_cpr      = formData.get('cert_cpr') || '';
            const cert_govt     = formData.get('cert_govt') || '';
            const terms         = formData.get('terms');

            // Validaciones
            if (password !== confirmPass) {
                showMessage('error', 'Las contraseñas no coinciden');
                return;
            }
            if (!terms) {
                showMessage('error', 'Debes aceptar los términos y condiciones');
                return;
            }
            if (!empresa) {
                showMessage('error', 'El nombre de empresa es obligatorio');
                return;
            }

            // UI Loading
            const submitBtn = registroForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Creando cuenta...';
            submitBtn.disabled = true;

            try {
                // 1. Crear usuario en Supabase Auth
                const { data: authData, error: authError } = await supabase.auth.signUp({
                    email: email,
                    password: password,
                    options: {
                        data: {
                            full_name: `${nombre} ${apellido}`.trim(),
                            company: empresa
                        }
                    }
                });

                if (authError) throw authError;

                if (authData.user) {
                    // 2. Guardar TODOS los campos en la tabla partners
                    const certsList = [
                        cert_uiagm === 'on' ? 'UIAGM/IFMGA' : null,
                        cert_iso   === 'on' ? 'ISO 21101'   : null,
                        cert_cpr   === 'on' ? 'CPR/Primeros Auxilios' : null,
                        cert_govt  === 'on' ? 'Licencia Gubernamental' : null
                    ].filter(Boolean);

                    const { error: partnerError } = await supabase
                        .from('partners')
                        .insert([{
                            user_id:          authData.user.id,
                            company_name:     empresa,           // ✅ Nombre de empresa (corregido)
                            company_email:    email,
                            contact_name:     `${nombre} ${apellido}`.trim(), // ✅ Nombre del contacto
                            phone:            telefono,          // ✅ Antes se perdía
                            country:          pais,              // ✅ Antes se perdía
                            activity_type:    tipo_actividad,    // ✅ Antes se perdía
                            tax_id:           ruc,               // ✅ Antes se perdía
                            website:          website,           // ✅ Antes se perdía
                            certifications:   certsList,         // ✅ Antes se perdía
                            description:      descripcion,       // ✅ Antes se perdía
                            status:           'pending'
                        }]);

                    if (partnerError) {
                        // Si falla el insert extra, logueamos pero no bloqueamos al usuario
                        console.warn('⚠️ Error guardando datos completos de partner:', partnerError.message);
                    }

                    // 3. Enviar emails vía /api/send-email
                    try {
                        await fetch('/api/send-email', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                tipo:          'partner_registration',
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
                                cert_govt
                            })
                        });
                    } catch (emailErr) {
                        // Email falla silenciosamente — no bloquea el flujo del usuario
                        console.warn('⚠️ Email no enviado (no bloquea registro):', emailErr.message);
                    }

                    showMessage('success', '¡Cuenta creada! Revisa tu email para confirmar y espera activación en 24 horas.');

                    setTimeout(() => {
                        window.location.href = 'index.html?registered=true';
                    }, 2500);
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
