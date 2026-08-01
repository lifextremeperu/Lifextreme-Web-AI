// ============================================
// LIFEXTREME INFRASTRUCTURE (LOCAL DATA)
// ============================================

// Inicializar directamente
initInfrastructure();

let allInfrastructure = [];

function initInfrastructure() {
    const grid = document.getElementById('infra-grid');
    if (!grid) return;

    // Simulate small network delay for effect
    grid.innerHTML = `<div class="col-span-full flex justify-center"><div class="animate-spin text-primary text-4xl"><i class="ri-loader-4-line"></i></div></div>`;

    setTimeout(() => {
        allInfrastructure = window.parks || [];
        renderInfrastructure(allInfrastructure);
        setupRegionFilters();
    }, 500);
}

function renderInfrastructure(items) {
    const grid = document.getElementById('infra-grid');
    if (!grid) return;

    if (items.length === 0) {
        grid.innerHTML = `<div class="col-span-full text-center text-slate-400 font-bold">No se encontraron parques en esta región.</div>`;
        return;
    }

    grid.innerHTML = items.map(item => {
        const bgImg = item.url_foto || 'https://images.unsplash.com/photo-1522163182402-834f871fd851?q=80&w=600';
        const certs = 'Estándar';
        const ubigeo = item.region || 'Perú';
        
        let linkAction = 'https://wa.me/51999999999';
        let linkIcon = 'ri-whatsapp-line';

        return `
        <div class="group bg-white rounded-3xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-2xl transition-all duration-300 flex flex-col">
            <div class="relative h-48 overflow-hidden">
                <img src="${bgImg}" alt="${item.nombre_infraestructura}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
                <div class="absolute top-4 left-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-[9px] font-black uppercase text-slate-800 shadow-sm">
                    ${item.tipo}
                </div>
                <div class="absolute bottom-4 right-4 bg-emerald-500 text-white px-3 py-1 rounded-full text-[9px] font-black uppercase shadow-sm flex items-center gap-1">
                    <i class="ri-shield-check-fill"></i> ${certs}
                </div>
            </div>
            <div class="p-6 flex-1 flex flex-col">
                <div class="flex items-start justify-between gap-4 mb-2">
                    <h3 class="text-xl font-black text-slate-900 leading-tight">${item.nombre_infraestructura}</h3>
                </div>
                <p class="text-xs font-bold text-slate-400 mb-4 flex items-center gap-1">
                    <i class="ri-map-pin-2-fill text-primary"></i> ${ubigeo}
                </p>
                <p class="text-sm text-slate-600 mb-6 flex-1 line-clamp-3">Parque de aventura operando con los más altos estándares de seguridad en la región.</p>
                
                <div class="flex items-center justify-between border-t border-slate-100 pt-4 mt-auto">
                    <div class="text-[10px] font-bold text-slate-400 uppercase">
                        Op: <span class="text-slate-700">Lifextreme Partner</span>
                    </div>
                    <a href="${linkAction}" target="_blank" rel="noopener noreferrer" class="bg-slate-900 text-white px-4 py-2 rounded-xl text-[10px] font-black uppercase hover:bg-emerald-600 transition-colors flex items-center gap-2 shadow-md">
                        <i class="${linkIcon} text-sm"></i> Reservar
                    </a>
                </div>
            </div>
        </div>
        `;
    }).join('');
}

function setupRegionFilters() {
    const chips = document.querySelectorAll('#infra-region-selector .region-chip');
    chips.forEach(chip => {
        chip.addEventListener('click', (e) => {
            chips.forEach(c => c.classList.remove('active'));
            e.target.classList.add('active');

            const region = e.target.dataset.region;
            
            if (region === 'Todos') {
                renderInfrastructure(allInfrastructure);
            } else {
                const filtered = allInfrastructure.filter(item => 
                    item.region && item.region.toLowerCase() === region.toLowerCase()
                );
                renderInfrastructure(filtered);
            }
        });
    });
}

