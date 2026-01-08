
import { createClient } from '@supabase/supabase-js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// ==========================================
// CONFIGURACIÓN (Rellena esto si ejecutas local con node)
// ==========================================
const SUPABASE_URL = 'https://zobpkmiqrvhbepqnjshr.supabase.co';
// INTENTA USAR SERVICE ROLE KEY SI ESTÁ DISPONIBLE EN ENV, SINO ANON (Anon no puede escribir en ciertas tablas protegidas sin login)
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || 'sb_publishable_pBMaD6Mm-6Pi5cwwp3UUsw_Pndjw-mo';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// ==========================================
// MOTOR DE CONTENIDO SIMULADO (AI MOCK)
// ==========================================

const TOPICS = [
    { title: "Guía Definitiva para el Camino Inca", keyword: "camino inca", category: "Guías" },
    { title: "5 Maravillas Ocultas de Cusco", keyword: "cusco secreto", category: "Descubrimiento" },
    { title: "Cómo Aclimatarse a la Altura Fácilmente", keyword: "mal de altura", category: "Consejos" },
    { title: "Gastronomía Andina: Qué Comer", keyword: "comida cusco", category: "Gastronomía" },
    { title: "Mejor Época para Viajar a Machupicchu", keyword: "clima cusco", category: "Planificación" }
];

const TEMPLATES = [
    "Descubre los secretos mejor guardados de {keyword}. En este artículo exploraremos todo lo que necesitas saber...",
    "¿Planeando tu viaje? No puedes perderte estos consejos sobre {keyword} que transformarán tu experiencia...",
    "Muchos viajeros se preguntan sobre {keyword}. Aquí te contamos la verdad basada en años de experiencia..."
];

function generateContent(topic) {
    const template = TEMPLATES[Math.floor(Math.random() * TEMPLATES.length)];
    const content = `
    <article>
        <h2>${topic.title}</h2>
        <p><strong>Por Equipo Lifextreme</strong></p>
        <p>${template.replace('{keyword}', topic.keyword)}</p>
        <h3>Lo que necesitas saber</h3>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        <h3>Consejos de Expertos</h3>
        <ul>
            <li>Reserva con anticipacion.</li>
            <li>Lleva ropa adecuada.</li>
            <li>Disfruta cada momento.</li>
        </ul>
        <p>¿Listo para la aventura? <a href="/tours">Reserva tu tour ahora</a>.</p>
    </article>
    `;

    return {
        title: topic.title,
        slug: topic.title.toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g, ''),
        content: content,
        excerpt: template.replace('{keyword}', topic.keyword).substring(0, 150) + "...",
        category: topic.category,
        published: true,
        cover_image: "https://source.unsplash.com/random/800x600/?travel,mountain"
    };
}

// ==========================================
// FUNCIÓN PRINCIPAL
// ==========================================

async function runAutoBlog() {
    console.log("🤖 Iniciando Motor de Blog Automático...");

    // 1. Seleccionar tema
    const topic = TOPICS[Math.floor(Math.random() * TOPICS.length)];
    console.log(`💡 Tema seleccionado: ${topic.title}`);

    // 2. Generar contenido
    const post = generateContent(topic);
    console.log("📝 Contenido generado.");

    try {
        // 3. Publicar en Supabase
        const { data, error } = await supabase
            .from('blog_posts')
            .upsert([post], { onConflict: 'slug' }) // Si ya existe, actualiza
            .select();

        if (error) throw error;

        console.log("✅ Artículo publicado exitosamente en base de datos!");
        console.log("🔗 Slug:", post.slug);
    } catch (error) {
        console.error("❌ Error publicando artículo:", error.message);
        console.log("⚠️ SUGERENCIA: ¿Corriste el script de SQL actualizado (V3.0) en Supabase?");
    }
}

// Ejecutar
runAutoBlog();
