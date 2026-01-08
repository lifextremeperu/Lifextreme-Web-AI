import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config({ path: '.env.local' });

// ─── CONFIGURACIÓN SUPABASE (AUDITOR CONFIDENTIAL) ───
const supabaseUrl = 'https://zobpkmiqrvhbepqnjshr.supabase.co';
const supabaseKey = 'sb_secret_7d_j2u37-hVXO_2VkvCc8A_tEaP_LDS'; // Service Role Key for Admin Access

const supabase = createClient(supabaseUrl, supabaseKey);

// ─── 1. COLA DE CONTENIDO (AUDIT SECTION 4.3 & 7) ───
const contentQueue = {
    // 🇺🇸 Mercado USA (40%)
    us: [
        {
            title: "Rainy Season Peru: Complete Waterproof Gear Guide",
            slug: "rainy-season-peru-gear-guide",
            keywords: ["rain gear peru trekking", "what to pack peru january"],
            type: "Guide",
            excerpt: "Don't let the rain stop you. The ultimate tested gear list for trekking Cusco in January.",
            market: "us",
            lang: "en"
        }
    ],
    // 🇪🇺 Mercado Europa (30%)
    eu: [
        {
            title: "Sustainable Trekking: How to Leave No Trace in the Andes",
            slug: "sustainable-trekking-peru-guide",
            keywords: ["sustainable travel peru", "eco friendly trekking cusco"],
            type: "Culture",
            excerpt: "Explore the Sacred Valley while protecting its ancient heritage.",
            market: "eu",
            lang: "en"
        }
    ],
    // 🇵🇪 Mercado Perú (30%)
    pe: [
        {
            title: "Machu Picchu en Temporada de Lluvias: Guía Completa 2026",
            slug: "machu-picchu-temporada-lluvias-2026",
            keywords: ["machu picchu enero lluvia", "viajar cusco enero"],
            type: "Guía",
            excerpt: "¿Miedo a la lluvia? La verdad sobre viajar en enero y los precios bajos.",
            market: "pe",
            lang: "es"
        },
        {
            title: "Ofertas Última Hora: Tours Cusco Enero desde S/ 899",
            slug: "ofertas-cusco-enero-2026",
            keywords: ["paquetes cusco baratos"],
            type: "Oferta",
            excerpt: "Paquetes todo incluido para nacionales con DNI.",
            market: "pe",
            lang: "es"
        }
    ]
};

// ─── 2. GENERADOR DE PROMPTS ───
function generateContent(templateItem) {
    const market = templateItem.market;
    let contentBody = "";

    // Contenido Simulado basado en Auditoria
    if (market === 'us') {
        contentBody = `
            <p class="lead"><strong>So, you're planning to hit Cusco in ${new Date().toLocaleString('default', { month: 'long' })}? Good choice. While the crowds are fighting for tickets in July, you'll have the misty Andes all to yourself. But there is a catch: The Rain.</strong></p>
            <h2>The Reality of wet Season (It's not that bad)</h2>
            <p>Data shows that it only rains about 2-3 hours a day, usually in the afternoon. This means your mornings are crisp, green, and empty.</p>
            <h2>Quick Gear Checklist</h2>
            <ul class="list-disc pl-5 mb-4">
                <li><strong>Gore-Tex Shell:</strong> Don't bring a poncho. Bring a real shell.</li>
                <li><strong>Waterproof Boots:</strong> Mud is real. Converses are a bad idea.</li>
            </ul>
        `;
    } else if (market === 'pe') {
        contentBody = `
            <p class="lead"><strong>¡Causita! ¿Pensando en mandarte a Cusco este finde? No dejes que te metan miedo con la lluvia. Enero es el mes secreto de los que saben viajar.</strong></p>
            <h2>¿Por qué viajar ahora?</h2>
            <p>Mira, la cosa es simple: <strong>Precios al suelo</strong>. Hoteles, vuelos y tours bajan hasta un 40%. Con tu DNI, la experiencia te sale regalada comparada con julio.</p>
            <h2>El Pack Salvador</h2>
            <ul>
                <li>Una buena casaca (nada de chompas que absorben agua).</li>
                <li>Zapatillas con cocada (para no patinar en las piedras).</li>
            </ul>
            <div class="bg-yellow-50 p-4 border-l-4 border-yellow-500 rounded my-4">
                <h3 class="font-bold">💰 Dato Caleta</h3>
                <p>Reserva con 2 semanas de anticipación y ahorras un 15% extra.</p>
            </div>
        `;
    }

    // JSON-LD Schema
    const schema = `
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [{
        "@type": "Question",
        "name": "${templateItem.keywords[0]}?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Best time depends on priority. For low crowds and low prices, January is ideal despite the rain."
        }
      }]
    }
    </script>`;

    return contentBody + schema;
}

// ─── 3. SCHEDULER ───
async function runAuditorEngine() {
    console.log("🦾 Iniciando Motor SEO (Compliance: Auditoria Enero 2026)...");

    // Temporada Baja: Prioridad PE > US
    const primeMarket = 'pe';
    const secondaryMarket = 'us';

    // Tomamos 1 de PE y 1 de US
    const tasks = [
        contentQueue[primeMarket][0],
        contentQueue[secondaryMarket][0]
    ];

    for (const task of tasks) {
        if (!task) continue;
        console.log(`\n🚀 Procesando para Mercado [${task.market.toUpperCase()}]: ${task.title}`);

        const content = generateContent(task);

        const { data, error } = await supabase
            .from('blog_posts')
            .upsert([
                {
                    slug: task.slug,
                    title: task.title,
                    content: content,
                    excerpt: task.excerpt,
                    category: task.type,
                    cover_image: `https://source.unsplash.com/800x600/?${task.keywords[0].replace(/ /g, ',')}`,
                    published: true
                }
            ], { onConflict: 'slug' })
            .select();

        if (error) {
            console.error("❌ Error Supabase:", error.message);
        } else {
            console.log("✅ Publicado Exitosamente.");
        }
    }
}

runAuditorEngine();
