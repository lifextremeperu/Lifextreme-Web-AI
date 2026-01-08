/**
 * AI Editor Engine
 * Simulates an LLM optimization process purely on client-side
 */

document.addEventListener('DOMContentLoaded', () => {
    const btnAnalyze = document.getElementById('btn-analyze');
    const inputTitle = document.getElementById('input-title');
    const inputBody = document.getElementById('input-body');
    const aiLoading = document.getElementById('ai-loading');
    const aiStatus = document.getElementById('ai-status');
    const previewContainer = document.getElementById('preview-container');
    const previewActions = document.getElementById('preview-actions');

    btnAnalyze.addEventListener('click', async () => {
        // Validation
        if (!inputBody.value.trim() || inputBody.value.length < 50) {
            alert('Por favor escribe al menos un párrafo para que la IA pueda trabajar.');
            return;
        }

        // 1. Activate Loading State
        aiLoading.classList.remove('hidden');
        aiLoading.classList.add('flex');

        // 2. Simulation Steps
        const steps = [
            "Analizando sentimiento...",
            "Corrigiendo gramática y ortografía...",
            "Inyectando palabras clave SEO...",
            "Estructurando párrafos...",
            "Seleccionando imágenes de stock..."
        ];

        for (const step of steps) {
            aiStatus.innerText = step;
            await new Promise(r => setTimeout(r, 800)); // Delay between steps
        }

        // 3. Process Content (The "AI" Magic)
        const rawText = inputBody.value;
        const rawTitle = inputTitle.value || "Mi Aventura Increíble";

        const optimizedContent = processContent(rawTitle, rawText);

        // 4. Render Result
        renderPreview(optimizedContent);

        // 5. Hide Loading & Unlock
        aiLoading.classList.add('hidden');
        aiLoading.classList.remove('flex');

        previewContainer.classList.remove('opacity-50', 'blur-[1px]', 'pointer-events-none');
        previewActions.classList.remove('hidden');
    });
});

function processContent(title, text) {
    // A. Clean up
    let polished = text
        .replace(/\n\n/g, '</p><p class="mb-4 text-slate-600 leading-relaxed">') // Paragraphs
        .replace(/\n/g, ' ') // Remove single breaks
        .trim();

    // Wrap in first p
    polished = `<p class="mb-4 text-slate-600 leading-relaxed first-letter:text-5xl first-letter:font-black first-letter:text-primary first-letter:float-left first-letter:mr-3">${polished}</p>`;

    // B. Inject Subheadings (Naïve approach: insert H2 every 300 chars approx)
    // For a demo, let's just insert a "Highlights" section if not present
    if (!polished.includes('<h2')) {
        const split = polished.split('</p>');
        if (split.length > 1) {
            // Insert H2 in the middle
            const mid = Math.floor(split.length / 2);
            split.splice(mid, 0, `<h2 class="text-2xl font-black italic text-slate-900 mt-8 mb-4">El Momento de la Verdad</h2>`);
            polished = split.join('');
        }
    }

    // C. Inject "Pro Tip" Box based on keywords
    const keywords = [
        { word: 'lluvia', tip: 'Lleva siempre un poncho de plástico ligero, incluso si hay sol.', title: 'Clima Impredecible' },
        { word: 'altura', tip: 'Toma mate de coca y evita el alcohol el primer día.', title: 'Soroche Hacks' },
        { word: 'comida', tip: 'El mercado central tiene opciones desde 10 soles.', title: 'Ahorro Gourmet' },
        { word: 'taxi', tip: 'Usa Uber o Indriver en ciudad para evitar sobreprecios.', title: 'Transporte Seguro' }
    ];

    let tipInserted = false;
    for (const kw of keywords) {
        if (polished.toLowerCase().includes(kw.word) && !tipInserted) {
            const tipBox = `
                <div class="bg-indigo-50 border-l-4 border-primary p-6 my-8 rounded-r-xl">
                    <h4 class="font-bold text-primary uppercase text-xs tracking-widest mb-1 flex items-center gap-2">
                        <i class="ri-lightbulb-flash-fill"></i> Lifextreme Pro Tip: ${kw.title}
                    </h4>
                    <p class="text-sm font-medium text-slate-700 italic">"${kw.tip}"</p>
                </div>
            `;
            // Append after first paragraph
            polished = polished.replace('</p>', `</p>${tipBox}`);
            tipInserted = true;
        }
    }

    // D. Return Object
    return {
        title: title,
        body: polished,
        image: "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=1200&auto=format&fit=crop" // Generic travel image
    };
}

function renderPreview(content) {
    const container = document.getElementById('preview-container');

    container.innerHTML = `
        <div class="relative h-48 rounded-2xl overflow-hidden mb-6 group">
            <img src="${content.image}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700">
            <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
                <span class="bg-primary text-white text-[10px] font-bold px-2 py-1 rounded uppercase tracking-widest mb-2 inline-block">Historia Épica</span>
            </div>
        </div>
        
        <h1 class="text-3xl font-black italic text-slate-900 mb-4 leading-tight">${content.title}</h1>
        
        <div class="flex items-center gap-2 mb-6 border-b border-slate-100 pb-4">
            <img src="https://ui-avatars.com/api/?name=Tu+Nombre&background=random" class="w-8 h-8 rounded-full">
            <div class="text-xs">
                <p class="font-bold text-slate-900">Por [Tu Nombre]</p>
                <p class="text-slate-400">Hace un momento</p>
            </div>
            <div class="ml-auto text-xs font-bold text-accent flex items-center gap-1">
                <i class="ri-fire-fill"></i> Trending
            </div>
        </div>

        <div class="prose prose-sm text-slate-600 max-w-none">
            ${content.body}
        </div>
    `;
}
