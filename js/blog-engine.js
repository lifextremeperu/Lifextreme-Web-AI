/**
 * Motor de Blog Frontend (Browser-Compatible)
 * "Pro SEO" Content Generator
 */

const postsDB = [
    {
        id: 'rainy-season-gear',
        title: "Rainy Season Peru: Complete Waterproof Gear Guide",
        category: "Guías",
        cover_image: "https://images.unsplash.com/photo-1517999588663-150277524953?q=80&w=1200&auto=format&fit=crop",
        author: "Sarah 'La Lince' Jenkins",
        date: "8 de Enero, 2026",
        readTime: "8 min",
        intro: `
            <p><strong>So, you're planning to hit Cusco in January? Good choice.</strong> While the crowds are fighting for tickets in July, you'll have the misty Andes all to yourself. But there is a catch: The Rain.</p>
            <p>Don't let the weather forecast scare you. With the right gear, the rainy season is arguably the most photogenic time to visit. The mountains are lush green, the clouds add drama to every shot, and the trails are empty.</p>
            <h3>The Reality of Wet Season</h3>
            <p>Data shows that it only rains about 2-3 hours a day, usually in the afternoon. This means your mornings are crisp, green, and perfect for hiking.</p>
        `,
        content: `
            <h2>1. The Non-Negotiables (Base Layer)</h2>
            <p>Cotton is your enemy. Repeat after me: <em>Cotton kills</em>. When wet, it loses all insulating properties.</p>
            <ul class="list-disc pl-5 mb-6">
                <li><strong>Merino Wool Base:</strong> It doesn't stink after 4 days and keeps you warm even when wet.</li>
                <li><strong>Synthetic Mid-layer:</strong> A fleece or light puffer that dries fast.</li>
            </ul>

            <h2>2. The Outer Shell (Your Shield)</h2>
            <p>Forget the $5 plastic ponchos sold at the corner store. If you are serious about the Inca Trail in January, you need a <strong>Gore-Tex (or equivalent) hard shell</strong>.</p>
            <div class="bg-blue-50 p-6 rounded-2xl border-l-4 border-primary my-6">
                <h4 class="text-primary font-bold mb-2">Pro Tip: Pit Zips</h4>
                <p class="text-sm">Ensure your jacket has underarm vents (pit zips). You will sweat hiking uphill, and if that moisture can't escape, you'll get wet from the inside out.</p>
            </div>

            <h2>3. Footwear: The Mud Struggle</h2>
            <p>The trails will be muddy. Low-cut trail runners might result in wet socks if you step deep. Mid-cut waterproof boots with good lugs (Vibram equivalent) are your best bet.</p>
        `,
        faqs: [
            { q: "Is the Inca Trail open in January?", a: "Yes, it is open all of January. It only closes in February for maintenance." },
            { q: "Do I need gaiters?", a: "Highly recommended for January. They keep mud and water out of your boots." },
            { q: "Is it cold?", a: "Not freezing, but damp. Temperatures range from 10°C to 20°C during the day, dropping to 5°C at night." }
        ]
    },
    {
        id: 'machu-picchu-rain',
        title: "Machu Picchu en Temporada de Lluvias: Guía Completa 2026",
        category: "Guías",
        cover_image: "https://images.unsplash.com/photo-1587595431973-160d0d94add1?q=80&w=1200&auto=format&fit=crop",
        author: "Marco 'Condor' Quispe",
        date: "8 de Enero, 2026",
        readTime: "10 min",
        intro: `
            <p class="lead text-xl text-slate-600 mb-6"><strong>¿Miedo a mojarte? Te estás perdiendo el secreto mejor guardado de los Andes.</strong></p>
            <p>Enero en Machu Picchu es sinónimo de misticismo. Las nubes bajas abrazando el Huayna Picchu crean una atmósfera que ningún día soleado de julio puede igualar. Y lo mejor: tendrás la ciudadela (casi) para ti solo.</p>
        `,
        content: `
            <h2>¿Por qué viajar en Enero?</h2>
            <p>Aparte de las fotos espectaculares, hay una razón de peso: <strong>El Presupuesto</strong>. Hoteles de lujo como el Sanctuary Lodge o Inkaterra suelen tener tarifas especiales, y los vuelos a Cusco bajan considerablemente.</p>
            
            <img src="https://images.unsplash.com/photo-1526392060635-9d6019884377?w=800" class="w-full rounded-2xl my-8 shadow-lg" alt="Llamas in Machu Picchu">

            <h2>La Estrategia del Horario</h2>
            <p>En temporada de lluvias, el clima sigue un patrón predecible:</p>
            <ul class="list-disc pl-5 mb-6">
                <li><strong>6:00 AM - 11:00 AM:</strong> Probabilidad de neblina matutina que se despeja espectacularmente.</li>
                <li><strong>11:00 AM - 2:00 PM:</strong> Generalmente soleado o nublado parcial.</li>
                <li><strong>2:00 PM en adelante:</strong> Probabilidad alta de lluvias fuertes.</li>
            </ul>
            <p><strong>Conclusión:</strong> Reserva el turno de la mañana sin falta.</p>
        `,
        faqs: [
            { q: "¿Se cierran los trenes por lluvia?", a: "Rara vez. PeruRail y IncaRail operan con normalidad, aunque pueden haber retrasos menores por seguridad." },
            { q: "¿Se ve Machu Picchu si llueve?", a: "Sí, y las nubes suelen moverse rápido. Es raro tener niebla cerrada todo el día." }
        ]
    },
    {
        id: 'best-time-machu-picchu',
        title: "Mejor Época para Viajar a Machupicchu",
        category: "Planificación",
        cover_image: "https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=1200&auto=format&fit=crop",
        author: "Elena 'River' Tuanama",
        date: "8 de Enero, 2026",
        readTime: "6 min",
        intro: `
            <p>La eterna pregunta de todo viajero. La respuesta corta es: <strong>Depende de qué buscas.</strong> ¿Cielos azules perfectos para Instagram? ¿O soledad y conexión espiritual?</p>
        `,
        content: `
            <h2>Temporada Seca (Mayo - Octubre)</h2>
            <p>Es la temporada alta. Cielos azules garantizados casi todos los días. Noches frías, días soleados.</p>
            <ul class="list-disc pl-5 mb-6">
                <li><strong>Pros:</strong> Vistas perfectas, cero lluvia.</li>
                <li><strong>Contras:</strong> Multitudes, precios altos, difícil conseguir entradas (reservar 6 meses antes).</li>
            </ul>

            <h2>Temporada de Lluvias (Noviembre - Abril)</h2>
            <p>Todo es verde. Orquídeas en flor. Arcoíris frecuentes.</p>
            <ul class="list-disc pl-5 mb-6">
                <li><strong>Pros:</strong> Paisajes verdes, menos gente, mejores precios.</li>
                <li><strong>Contras:</strong> Lluvia, caminos con barro.</li>
            </ul>

            <div class="bg-emerald-50 p-6 rounded-2xl my-6">
                <h4 class="text-emerald-700 font-bold mb-2">Recomendación del Experto</h4>
                <p class="text-sm text-emerald-800">Si puedes elegir, ven en <strong>Abril u Octubre</strong>. Son los meses "hombro" (shoulder season). Tienes lo mejor de los dos mundos: poco riesgo de lluvia y menos multitudes que en Julio.</p>
            </div>
        `,
        faqs: [
            { q: "¿Cuándo se agotan las entradas?", a: "Para Junio-Agosto, debes comprar en Enero o Febrero. Para otros meses, 2 meses antes es suficiente." },
            { q: "¿Hace mucho frío?", a: "En Machu Picchu (Selva Alta) es templado. En Cusco ciudad sí hace frío de noche." }
        ]
    },
    {
        id: 'default',
        title: "Artículo no encontrado",
        category: "Error",
        cover_image: "https://images.unsplash.com/photo-1594322436404-5a0526db4d13?w=1200",
        author: "Sistema",
        date: "--",
        readTime: "--",
        intro: "<p>Lo sentimos, no pudimos encontrar el artículo que buscas.</p>",
        content: "",
        faqs: []
    }
];

// Main Logic to Populate Article Page
function initArticlePage() {
    // 1. Get ID from URL
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');

    // 2. Find Post
    const post = postsDB.find(p => p.id === id) || postsDB.find(p => p.id === 'default');

    // 3. Populate DOM Elements
    document.title = `${post.title} | Lifextreme Blog`;

    // Header
    const heroImg = document.getElementById('article-hero-img');
    const titleEl = document.getElementById('article-title');
    const catEl = document.getElementById('article-category');

    if (heroImg) heroImg.src = post.cover_image;
    if (titleEl) titleEl.innerText = post.title;
    if (catEl) catEl.innerText = `Blog / ${post.category}`;

    // Body
    const introEl = document.getElementById('article-intro');
    if (introEl) {
        introEl.innerHTML = `
            ${post.intro}
            ${post.content || ''}
        `;
    }

    // FAQs
    const faqsEl = document.getElementById('article-faqs');
    if (faqsEl && post.faqs.length > 0) {
        faqsEl.innerHTML = post.faqs.map(faq => `
            <div class="border border-gray-200 rounded-xl p-4 hover:border-primary transition-colors cursor-pointer bg-white">
                <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                    <i class="ri-question-line text-primary"></i> ${faq.q}
                </h4>
                <p class="text-sm text-gray-500">${faq.a}</p>
            </div>
        `).join('');
    } else if (faqsEl) {
        // Hide FAQ section if empty
        faqsEl.parentElement.style.display = 'none';
    }

    // JSON-LD Update (Advanced SEO)
    const schemaScript = document.getElementById('json-ld-faq');
    if (schemaScript) {
        const schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": post.title,
            "image": [post.cover_image],
            "author": {
                "@type": "Person",
                "name": post.author
            },
            "publisher": {
                "@type": "Organization",
                "name": "Lifextreme",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://www.lifextreme.store/logo.png"
                }
            },
            "datePublished": "2026-01-08"
        };
        schemaScript.text = JSON.stringify(schema);
    }
}

// Auto-run if on article page
if (document.getElementById('article-title')) {
    document.addEventListener('DOMContentLoaded', initArticlePage);
}
