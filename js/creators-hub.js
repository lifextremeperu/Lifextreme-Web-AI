/**
 * Creators Hub Engine
 * Manages logic for Writers, Photographers, and VR Creators
 */

document.addEventListener('DOMContentLoaded', () => {
    initRoleSwitcher();
    initWriterEngine();
    initPhotographerEngine();
    initVREngine();
});

// ==========================================
// 1. Role Switcher Logic
// ==========================================
function initRoleSwitcher() {
    const tabs = document.querySelectorAll('.role-tab');
    const sections = document.querySelectorAll('.role-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Deactivate all
            tabs.forEach(t => {
                t.classList.remove('bg-slate-900', 'text-white', 'shadow-lg');
                t.classList.add('bg-white', 'text-slate-500', 'hover:bg-slate-50');
            });
            sections.forEach(s => s.classList.add('hidden'));

            // Activate current
            tab.classList.remove('bg-white', 'text-slate-500', 'hover:bg-slate-50');
            tab.classList.add('bg-slate-900', 'text-white', 'shadow-lg');

            const targetId = tab.dataset.target;
            document.getElementById(targetId).classList.remove('hidden');

            // Optional: Scroll to section slightly
            // document.getElementById('creators-hub').scrollIntoView({ behavior: 'smooth' });
        });
    });
}

// ==========================================
// 2. Writer Engine (Original AI Editor)
// ==========================================
function initWriterEngine() {
    const btnAnalyze = document.getElementById('btn-analyze-writer');
    if (!btnAnalyze) return;

    const inputTitle = document.getElementById('input-title');
    const inputBody = document.getElementById('input-body');
    const aiLoading = document.getElementById('ai-loading-writer');
    const aiStatus = document.getElementById('ai-status-writer');
    const previewContainer = document.getElementById('preview-container-writer');
    const previewActions = document.getElementById('preview-actions-writer');

    btnAnalyze.addEventListener('click', async () => {
        if (!inputBody.value.trim() || inputBody.value.length < 50) {
            alert('Por favor escribe al menos un párrafo para que la IA pueda trabajar.');
            return;
        }

        aiLoading.classList.remove('hidden');
        aiLoading.classList.add('flex');

        const steps = [
            "Analizando sentimiento...",
            "Corrigiendo gramática y ortografía...",
            "Inyectando palabras clave SEO...",
            "Estructurando párrafos...",
            "Seleccionando imágenes de stock..."
        ];

        for (const step of steps) {
            aiStatus.innerText = step;
            await new Promise(r => setTimeout(r, 800));
        }

        const rawText = inputBody.value;
        const rawTitle = inputTitle.value || "Mi Aventura Increíble";
        const optimizedContent = processContent(rawTitle, rawText);

        renderPreview(optimizedContent);

        aiLoading.classList.add('hidden');
        aiLoading.classList.remove('flex');
        previewContainer.classList.remove('opacity-50', 'blur-[1px]', 'pointer-events-none');
        previewActions.classList.remove('hidden');
    });
}

// Helper for Writer (Keep original logic)
function processContent(title, text) {
    let polished = text.replace(/\n\n/g, '</p><p class="mb-4 text-slate-600 leading-relaxed">').replace(/\n/g, ' ').trim();
    polished = `<p class="mb-4 text-slate-600 leading-relaxed first-letter:text-5xl first-letter:font-black first-letter:text-primary first-letter:float-left first-letter:mr-3">${polished}</p>`;

    // Naive H2 Injection
    if (!polished.includes('<h2')) {
        const split = polished.split('</p>');
        if (split.length > 1) {
            const mid = Math.floor(split.length / 2);
            split.splice(mid, 0, `<h2 class="text-2xl font-black italic text-slate-900 mt-8 mb-4">El Momento de la Verdad</h2>`);
            polished = split.join('');
        }
    }

    // SEO Highlights
    const seoKeywords = ['trekking', 'montaña', 'aventura', 'cusco', 'perú', 'viaje'];
    seoKeywords.forEach(kw => {
        const regex = new RegExp(`\\b(${kw})\\b`, 'gi');
        polished = polished.replace(regex, '<span class="bg-green-100 text-green-700 font-bold px-1 rounded cursor-help"> $1 </span>');
    });

    return {
        title: title,
        body: polished,
        image: "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=1200"
    };
}

function renderPreview(content) {
    const container = document.getElementById('preview-container-writer');
    container.innerHTML = `
        <div class="relative h-48 rounded-2xl overflow-hidden mb-6 group">
            <img src="${content.image}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700">
            <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
                <span class="bg-primary text-white text-[10px] font-bold px-2 py-1 rounded uppercase tracking-widest mb-2 inline-block">Historia Épica</span>
            </div>
        </div>
        <h1 class="text-3xl font-black italic text-slate-900 mb-4 leading-tight">${content.title}</h1>
        <div class="prose prose-sm text-slate-600 max-w-none">${content.body}</div>
    `;
}

// ==========================================
// 3. Photographer Engine
// ==========================================
function initPhotographerEngine() {
    const dropzone = document.getElementById('photo-dropzone');
    const analyzeBtn = document.getElementById('btn-analyze-photo');
    const galleryGrid = document.getElementById('photo-gallery-preview');
    const aiStatus = document.getElementById('ai-status-photo');
    const loadingOverlay = document.getElementById('ai-loading-photo');

    if (!dropzone) return;

    // Simulate Drag & Drop
    dropzone.addEventListener('click', () => {
        // Trigger generic timeout to simulate file selection
        dropzone.innerHTML = `<div class="text-center"><i class="ri-loader-4-line text-4xl animate-spin text-primary"></i><p class="mt-2 font-bold text-slate-500">Cargando 4 imágenes...</p></div>`;
        setTimeout(() => {
            dropzone.innerHTML = `
                <div class="grid grid-cols-2 gap-4 w-full">
                    <img src="https://images.unsplash.com/photo-1587595431973-160d0d94add1" class="rounded-lg h-32 object-cover w-full">
                    <img src="https://images.unsplash.com/photo-1526392060635-9d6019884377" class="rounded-lg h-32 object-cover w-full">
                    <img src="https://images.unsplash.com/photo-1533130061792-649d44e7855e" class="rounded-lg h-32 object-cover w-full">
                    <img src="https://images.unsplash.com/photo-1501555088652-021faa106b9b" class="rounded-lg h-32 object-cover w-full">
                </div>
            `;
            // Enable button
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }, 1500);
    });

    analyzeBtn.addEventListener('click', async () => {
        loadingOverlay.classList.remove('hidden');
        loadingOverlay.classList.add('flex');

        const steps = ["Escaneando EXIF...", "Comprobando resolución...", "Evaluando composición...", "Generando etiquetas IA..."];

        for (const step of steps) {
            aiStatus.innerText = step;
            await new Promise(r => setTimeout(r, 700));
        }

        // Show result
        loadingOverlay.classList.add('hidden');
        loadingOverlay.classList.remove('flex');

        galleryGrid.innerHTML = `
            <div class="col-span-2 bg-green-50 p-4 rounded-xl border border-green-100 flex items-center justify-between mb-4">
                <div class="flex items-center gap-3">
                    <i class="ri-checkbox-circle-fill text-green-500 text-2xl"></i>
                    <div>
                        <h4 class="font-bold text-slate-900">4 Fotos Aprobadas</h4>
                        <p class="text-xs text-slate-500">Listas para el Marketplace</p>
                    </div>
                </div>
                <span class="font-black text-xl text-green-600">$20.00 <span class="text-xs text-slate-400 font-normal">estimado</span></span>
            </div>
            <div class="space-y-3">
                 ${generatePhotoRow("Machu Picchu Amanecer", "Alta Demanda", 98)}
                 ${generatePhotoRow("Llamas en Cusco", "Tendencia", 92)}
                 ${generatePhotoRow("Montaña 7 Colores", "Popular", 89)}
                 ${generatePhotoRow("Laguna Humantay", "Nuevo", 95)}
            </div>
        `;
        galleryGrid.parentElement.classList.remove('opacity-50', 'blur-[1px]', 'pointer-events-none');
    });
}

function generatePhotoRow(name, tag, score) {
    return `
        <div class="flex items-center justify-between bg-white p-3 rounded-lg border border-slate-100 shadow-sm">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-slate-200 rounded-lg overflow-hidden">
                   <img src="https://source.unsplash.com/random/100x100/?mountains" class="w-full h-full object-cover">
                </div>
                <div>
                    <h5 class="font-bold text-xs text-slate-900">${name}</h5>
                    <span class="text-[10px] bg-indigo-50 text-indigo-600 px-1.5 py-0.5 rounded font-bold uppercase">${tag}</span>
                </div>
            </div>
            <div class="text-right">
                <div class="text-xs font-black text-green-500">Score: ${score}/100</div>
                <div class="text-[10px] text-slate-400">Metadata OK</div>
            </div>
        </div>
    `;
}

// ==========================================
// 4. VR Engine
// ==========================================
function initVREngine() {
    const vrZone = document.getElementById('vr-upload-zone');
    const analyzeBtn = document.getElementById('btn-analyze-vr');
    const resultBox = document.getElementById('vr-result-preview');
    const loadingOverlay = document.getElementById('ai-loading-vr');
    const statusText = document.getElementById('ai-status-vr');

    if (!vrZone) return;

    // Simulate input interaction
    const input = vrZone.querySelector('input');
    input.addEventListener('change', () => {
        if (input.value) {
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    });

    analyzeBtn.addEventListener('click', async () => {
        loadingOverlay.classList.remove('hidden');
        loadingOverlay.classList.add('flex');

        const steps = ["Conectando con Servidor de Render...", "Analizando bitrate...", "Verificando metadata 360...", "Comprobando audio espacial..."];

        for (const step of steps) {
            statusText.innerText = step;
            await new Promise(r => setTimeout(r, 1000));
        }

        loadingOverlay.classList.add('hidden');
        loadingOverlay.classList.remove('flex');

        // Results
        resultBox.parentElement.classList.remove('opacity-50', 'blur-[1px]', 'pointer-events-none');
        resultBox.innerHTML = `
            <div class="relative rounded-2xl overflow-hidden bg-black aspect-video mb-4 group cursor-pointer">
                <img src="https://images.unsplash.com/photo-1551632811-561732d1e306?q=80" class="w-full h-full object-cover opacity-60">
                <div class="absolute inset-0 flex items-center justify-center">
                    <div class="w-16 h-16 bg-white/20 backdrop-blur rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
                        <i class="ri-goggles-line text-3xl text-white"></i>
                    </div>
                </div>
                <div class="absolute bottom-4 left-4">
                    <span class="bg-red-600 text-white text-[10px] font-black px-2 py-1 rounded uppercase">4K 60FPS</span>
                    <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-1 rounded uppercase ml-2">Spatial Audio</span>
                </div>
            </div>
            <div class="bg-green-50 p-4 rounded-xl border border-green-100 mb-4">
                <h4 class="font-bold text-green-800 text-sm mb-1"><i class="ri-check-double-line"></i> Calidad: Masterpiece</h4>
                <p class="text-green-700 text-xs">Tu video cumple con los estándares para visualización en Meta Quest 3 y Apple Vision Pro.</p>
            </div>
         `;

        document.getElementById('vr-publish-actions').classList.remove('hidden');
    });

}
