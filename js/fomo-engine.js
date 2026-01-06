// --- FOMO ENGINE (Real-time Pub/Sub Simulation) ---

const FOMOEngine = {
    userCity: 'Perú',
    queue: [],
    names: ['Lucho', 'Ana', 'Carlos', 'Sofía', 'Mateo', 'Valentina', 'Diego', 'Camila'],
    cities: ['Cusco', 'Lima', 'Arequipa', 'Trujillo', 'Puno', 'Iquitos'],

    /**
     * Inicializa el motor detectando la ubicación del usuario.
     */
    async init() {
        try {
            const resp = await fetch('http://ip-api.com/json/?fields=status,city,country');
            const data = await resp.json();
            if (data.status === 'success') {
                this.userCity = data.city;
            }
        } catch (e) {
            console.warn('Geo-IP Error, usando ubicación genérica');
        }

        this.startLoop();
    },

    /**
     * Añade un evento a la cola de mensajes (Simulación de Pub/Sub).
     */
    emitEvent(tourName, city = null) {
        const event = {
            id: Date.now(),
            user: this.names[Math.floor(Math.random() * this.names.length)],
            city: city || (Math.random() > 0.4 ? this.userCity : this.cities[Math.floor(Math.random() * this.cities.length)]),
            tour: tourName,
            time: 'hace unos segundos'
        };
        this.queue.push(event);
        this.showPopup(event);
    },

    /**
     * Inicia el ciclo de avisos sociales.
     */
    startLoop() {
        setInterval(() => {
            if (Math.random() > 0.7) { // 30% de probabilidad de nuevo evento aleatorio
                const randomTour = window.tours[Math.floor(Math.random() * window.tours.length)].title;
                this.emitEvent(randomTour);
            }
        }, 15000); // Cada 15 segundos chequea
    },

    /**
     * Renderiza el popup dinámico con lógica de "tribu".
     */
    showPopup(event) {
        const container = document.getElementById('fomo-container');
        if (!container) return;

        const isLocal = event.city === this.userCity;
        const html = `
            <div id="fomo-${event.id}" class="fomo-popup bg-white/95 backdrop-blur-md p-4 rounded-3xl shadow-2xl border border-slate-100 flex items-center gap-4 mb-4 transition-all duration-500 transform translate-x-full">
                <div class="w-10 h-10 rounded-full bg-slate-900 text-white flex items-center justify-center font-black text-xs">
                    ${event.user[0]}
                </div>
                <div class="flex-1">
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">
                        ${isLocal ? '<span class="text-primary">● CERCA DE TI</span>' : 'RESERVA RECIENTE'}
                    </p>
                    <p class="text-[11px] font-black leading-tight text-slate-800">
                        <span class="text-primary">${event.user}</span> de ${event.city}
                    </p>
                    <p class="text-[10px] font-bold text-slate-500">Reservó: <span class="italic">${event.tour}</span></p>
                </div>
                <p class="text-[8px] font-black text-slate-300 uppercase">${event.time}</p>
            </div>
        `;

        container.insertAdjacentHTML('beforeend', html);
        const el = document.getElementById(`fomo-${event.id}`);

        // Animación de entrada
        setTimeout(() => el.classList.remove('translate-x-full'), 100);

        // Auto-destrucción
        setTimeout(() => {
            el.classList.add('opacity-0', 'translate-y-4');
            setTimeout(() => el.remove(), 500);
        }, 6000);
    }
};

window.FOMOEngine = FOMOEngine;
