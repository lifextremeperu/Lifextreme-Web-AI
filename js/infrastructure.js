// ============================================
// LIFEXTREME INFRASTRUCTURE (LOCAL DATA)
// ============================================

let allInfrastructure = [];

function initInfrastructure() {
    const grid = document.getElementById('infra-grid');
    if (!grid) return;

    allInfrastructure = window.parks || [];
    if (allInfrastructure.length > 0) {
        renderRegionFilters(allInfrastructure);
        renderInfrastructure(allInfrastructure);
    } else {
        grid.innerHTML = `<div class="col-span-full flex justify-center"><div class="animate-spin text-primary text-4xl"><i class="ri-loader-4-line"></i></div></div>`;
        setTimeout(() => {
            allInfrastructure = window.parks || [];
            renderRegionFilters(allInfrastructure);
            renderInfrastructure(allInfrastructure);
        }, 300);
    }
}

window.initInfrastructure = initInfrastructure;
window.renderInfrastructure = renderInfrastructure;

// Inicializar directamente
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initInfrastructure);
} else {
    initInfrastructure();
}

function renderRegionFilters(items) {
    const selector = document.getElementById('infra-region-selector');
    if (!selector) return;
    
    // Extract unique regions
    const regions = ['Todos'];
    items.forEach(item => {
        if (item.region && !regions.includes(item.region)) {
            regions.push(item.region);
        }
    });
    
    // Render chips
    selector.innerHTML = regions.map((region, index) => {
        return `<div class="region-chip ${index === 0 ? 'active' : ''}" data-action="sel-infra-region" data-region="${region}">${region}</div>`;
    }).join('');
    
    // Setup listeners
    setupRegionFilters();
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
        const desc = item.descripcion || 'Parque de aventura operando con los más altos estándares de seguridad en la región.';
        
        const waMsg = encodeURIComponent(`Hola Lifextreme, deseo información y reservar en el parque de aventura: *${item.nombre_infraestructura}* (${ubigeo} - ${item.tipo}).`);
        let linkAction = `https://wa.me/51958050928?text=${waMsg}`;
        let linkIcon = 'ri-whatsapp-line';
        const safeName = (item.nombre_infraestructura || 'Parque de Aventura').replace(/'/g, "\\'");

        return `
        <div class="neuro-card bg-slate-900/85 backdrop-blur-md rounded-3xl overflow-hidden border border-white/10 hover:border-amber-400/50 shadow-xl hover:shadow-[0_20px_45px_rgba(245,158,11,0.18)] transition-all duration-300 flex flex-col group">
            <div class="relative h-48 overflow-hidden bg-slate-950">
                <img src="${bgImg}" alt="${item.nombre_infraestructura}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
                <div class="absolute inset-0 bg-gradient-to-t from-slate-900/80 via-transparent to-transparent"></div>
                <div class="absolute top-4 left-4 bg-slate-900/90 backdrop-blur px-3 py-1 rounded-full text-[9px] font-black uppercase text-amber-400 border border-white/15 shadow-sm">
                    ${item.tipo}
                </div>
                <div class="absolute bottom-4 right-4 bg-emerald-500 text-slate-950 font-black px-3 py-1 rounded-full text-[9px] uppercase shadow-sm flex items-center gap-1">
                    <i class="ri-shield-check-fill"></i> ${certs}
                </div>
            </div>
            <div class="p-6 flex-1 flex flex-col">
                <div class="flex items-start justify-between gap-4 mb-2">
                    <h3 class="text-xl font-black text-white group-hover:text-amber-300 transition-colors leading-tight">${item.nombre_infraestructura}</h3>
                </div>
                <p class="text-xs font-bold text-slate-400 mb-4 flex items-center gap-1">
                    <i class="ri-map-pin-2-fill text-amber-400"></i> ${ubigeo}
                </p>
                <p class="text-sm text-slate-300 mb-6 flex-1 line-clamp-3 leading-relaxed">${desc}</p>
                
                <div class="flex items-center justify-between border-t border-white/10 pt-4 mt-auto gap-2">
                    <div class="text-[10px] font-bold text-slate-400 uppercase">
                        Op: <span class="text-slate-200">Lifextreme Partner</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <button type="button" onclick="if(window.maxAddToCartAndPay){window.maxAddToCartAndPay('${safeName}', 180, 1);}else{window.open('${linkAction}','_blank');}" class="bg-primary text-white px-3 py-2 rounded-xl text-[10px] font-black uppercase hover:bg-indigo-700 transition-colors flex items-center gap-1 shadow-md" title="Añadir al Carrito">
                            <i class="ri-shopping-bag-3-line text-sm"></i> Pass
                        </button>
                        <a href="${linkAction}" target="_blank" rel="noopener noreferrer" class="bg-slate-900 text-white px-3 py-2 rounded-xl text-[10px] font-black uppercase hover:bg-emerald-600 transition-colors flex items-center gap-1 shadow-md">
                            <i class="${linkIcon} text-sm"></i> WhatsApp
                        </a>
                    </div>
                </div>
            </div>
        </div>
        `;
    }).join('');
    
    // Inyectar SEO dinámico para los LLMs
    injectSchema(items);
}

function injectSchema(items) {
    // Remover schemas anteriores si los hay
    document.querySelectorAll('script[data-schema="infra"]').forEach(el => el.remove());
    
    items.forEach(item => {
        const schema = {
            "@context": "https://schema.org",
            "@type": "TouristDestination",
            "name": item.nombre_infraestructura,
            "description": item.descripcion || 'Parque de aventura seguro y certificado en Perú.',
            "image": item.url_foto || 'https://images.unsplash.com/photo-1522163182402-834f871fd851?q=80&w=600',
            "address": {
                "@type": "PostalAddress",
                "addressRegion": item.region || 'Perú',
                "addressCountry": "PE"
            },
            "provider": {
                "@type": "Organization",
                "name": "Lifextreme Peru",
                "url": "https://www.lifextreme.store"
            }
        };
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.setAttribute('data-schema', 'infra');
        script.textContent = JSON.stringify(schema);
        document.head.appendChild(script);
    });
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

