// --- SENSORY ENGINE (Embodied Cognition Tracking) ---

const SensoryEngine = {
    observers: [],

    /**
     * Inicializa el rastreo de intencionalidad sensorial.
     */
    init() {
        this.setupObservers();
    },

    /**
     * Configura Intersection Observers para detectar el foco del usuario.
     */
    setupObservers() {
        const options = {
            threshold: [0.5], // Umbral más sensible para dispositivos con scroll
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Iniciamos el temporizador de Dwell Time
                    entry.target.dataset.dwellStart = Date.now();
                    this.trackDwell(entry.target);
                } else {
                    delete entry.target.dataset.dwellStart;
                }
            });
        }, options);

        // Observar elementos con data-sensory (imágenes o secciones clave)
        document.querySelectorAll('[data-sensory]').forEach(el => observer.observe(el));
        this.observers.push(observer);
    },

    /**
     * Monitorea si el usuario se queda mirando el elemento suficiente tiempo.
     */
    trackDwell(el) {
        const check = setInterval(() => {
            if (!el.dataset.dwellStart) {
                clearInterval(check);
                return;
            }

            const elapsed = Date.now() - parseInt(el.dataset.dwellStart);
            if (elapsed >= 2500) { // 2.5 segundos de "interés profundo"
                this.triggerTransformation(el.dataset.sensoryType, el.dataset.sensoryTarget);
                clearInterval(check);
                delete el.dataset.dwellStart; // Evitar disparos repetidos
            }
        }, 100);
    },

    /**
     * Realiza la transformación narrativa (Embodied Cognition).
     */
    triggerTransformation(type, targetId) {
        const targetEl = document.getElementById(targetId);
        if (!targetEl || !this.activeTour || !this.activeTour.sensoryVariants) return;

        const variant = this.activeTour.sensoryVariants[type];
        if (!variant) return;

        // Transición suave
        targetEl.classList.add('sensory-hidden');

        setTimeout(() => {
            targetEl.innerText = variant;
            targetEl.classList.remove('sensory-hidden');
            targetEl.classList.add('sensory-active', 'text-primary', 'italic');

            // Log de conversión sensorial (Simulado)
            console.log(`[SensoryEngine] Contexto activado: ${type} -> Reduciendo fricción racional.`);
        }, 600);
    }
};

window.SensoryEngine = SensoryEngine;
