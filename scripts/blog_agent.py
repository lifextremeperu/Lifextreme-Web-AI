"""
============================================================
LIFEXTREME - Blog Agent con Pydantic AI + Gemini
Genera artículos SEO diarios usando el Dataset CIXTUR
============================================================
"""

import os
import json
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel

# ── Cargar variables de entorno ──────────────────────────
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
CIXTUR_PATH = os.getenv("CIXTUR_JSONL_PATH", "data/cixtur_knowledge.jsonl")
OUTPUT_DIR = os.getenv("BLOG_OUTPUT_DIR", "blog/articulos")
BASE_URL = os.getenv("BLOG_BASE_URL", "https://www.lifextreme.store/blog")

# ── Modelo de Datos del Artículo (Pydantic) ───────────────
class FAQItem(BaseModel):
    pregunta: str = Field(description="Pregunta en lenguaje natural que hace un viajero")
    respuesta: str = Field(description="Respuesta directa, max 100 palabras, optimizada para LLMs")

class BlogArticle(BaseModel):
    titulo: str = Field(description="Título SEO atractivo con keyword principal, max 65 chars")
    slug: str = Field(description="URL slug sin tildes ni espacios, ej: trek-ausangate-guia")
    meta_description: str = Field(description="Descripción SEO max 155 caracteres con llamada a acción")
    region: str = Field(description="Ciudad/región del Perú: Cusco, Huaraz, Iquitos, etc.")
    dificultad: str = Field(description="Nivel: Principiante, Intermedio, Avanzado, Extremo")
    palabras_clave: list[str] = Field(description="5-8 keywords long-tail del artículo")
    contenido_html: str = Field(description="Artículo completo en HTML semántico con H2, H3, párrafos y listas")
    faqs: list[FAQItem] = Field(description="3-5 preguntas frecuentes optimizadas para IA y voz")
    fuente_datos: str = Field(description="Resumen del dato CIXTUR usado como base del artículo")

# ── Cargar Dataset CIXTUR ─────────────────────────────────
def cargar_cixtur(ruta: str, n_samples: int = 15) -> str:
    """Carga registros aleatorios del dataset CIXTUR como contexto RAG."""
    registros = []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                try:
                    registros.append(json.loads(linea.strip()))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"⚠️  CIXTUR no encontrado en: {ruta}")
        print("   Ejecuta primero: python scripts/convert_cixtur.py")
        return "Dataset CIXTUR no disponible. Usa conocimiento general de turismo peruano."

    # Selección aleatoria para variedad diaria
    muestra = random.sample(registros, min(n_samples, len(registros)))
    
    contexto = "=== DATOS REALES DEL DATASET CIXTUR (Turismo Perú) ===\n\n"
    for r in muestra:
        contexto += f"Tema: {r.get('source', 'General')}\n"
        contexto += f"P: {r.get('prompt', '')}\n"
        contexto += f"R: {r.get('completion', '')}\n\n"
    
    return contexto

# ── Temas Estratégicos por día ────────────────────────────
TEMAS_BLOG = [
    "Guía completa para trekking en Ausangate Cusco: qué necesitas saber antes de ir",
    "Cuánto cuesta contratar una agencia de turismo de aventura en Cusco en 2026",
    "Mal de altura en Cusco: síntomas, prevención y qué hacer si te afecta",
    "Los 5 treks menos conocidos de la región Cusco que valen la pena",
    "Mejor época para trekking en Perú: mes a mes, región por región",
    "Equipo obligatorio para expediciones extremas sobre 5000 msnm en Perú",
    "Guías certificados en Cusco: qué certificaciones debe tener el tuyo",
    "Rafting en el río Urubamba: niveles, temporadas y precios reales",
    "Cómo planificar una expedición al Nevado Salkantay desde cero",
    "Turismo de aventura seguro en Perú: protocolos de emergencia que debes conocer",
    "Diferencia entre tour privado y tour grupal en agencias de aventura Cusco",
    "Montañismo en Huaraz: rutas para principiantes y avanzados en 2026",
    "Por qué el barrio de San Blas en Cusco es la base perfecta para tus aventuras",
    "Turismo extremo en la Amazonía peruana: qué esperar y cómo prepararse",
]

# ── Generador de JSON-LD para el Artículo ─────────────────
def generar_json_ld(articulo: BlogArticle) -> str:
    """Genera el structured data Schema.org para Article + FAQPage."""
    url = f"{BASE_URL}/{articulo.slug}"
    fecha = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    faq_items = [
        {"@type": "Question",
         "name": faq.pregunta,
         "acceptedAnswer": {"@type": "Answer", "text": faq.respuesta}}
        for faq in articulo.faqs
    ]
    
    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": articulo.titulo,
            "description": articulo.meta_description,
            "keywords": ", ".join(articulo.palabras_clave),
            "url": url,
            "datePublished": fecha,
            "dateModified": fecha,
            "author": {
                "@type": "Organization",
                "name": "Lifextreme Peru",
                "url": "https://www.lifextreme.store"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Lifextreme Peru",
                "logo": {"@type": "ImageObject", "url": "https://www.lifextreme.store/logo.png"}
            },
            "about": {
                "@type": "TouristDestination",
                "name": articulo.region,
                "touristType": articulo.dificultad
            }
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_items
        }
    ]
    
    return "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(s, ensure_ascii=False, indent=2)}\n</script>'
        for s in schemas
    )

# ── Generador de HTML del Artículo ───────────────────────
def generar_html_pagina(articulo: BlogArticle) -> str:
    """Envuelve el artículo en la plantilla HTML de Lifextreme."""
    json_ld = generar_json_ld(articulo)
    fecha_display = datetime.now().strftime("%d de %B de %Y")
    
    faq_html = "".join(
        f"""<div class="faq-item">
            <h3>{faq.pregunta}</h3>
            <p>{faq.respuesta}</p>
        </div>"""
        for faq in articulo.faqs
    )
    
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{articulo.titulo} | Lifextreme</title>
    <meta name="description" content="{articulo.meta_description}">
    <meta name="keywords" content="{', '.join(articulo.palabras_clave)}">
    <link rel="canonical" href="{BASE_URL}/{articulo.slug}">
    <meta property="og:title" content="{articulo.titulo}">
    <meta property="og:description" content="{articulo.meta_description}">
    <meta property="og:url" content="{BASE_URL}/{articulo.slug}">
    <meta name="geo.region" content="PE-CUS">
    <meta name="geo.placename" content="{articulo.region}, Perú">
    {json_ld}
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/remixicon@4.5.0/fonts/remixicon.css" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Outfit', sans-serif; background: #fcfdff; color: #1e293b; }}
        .nav {{ background: #0f172a; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }}
        .nav a {{ color: white; text-decoration: none; font-weight: 900; font-style: italic; font-size: 1.2rem; }}
        .nav .back {{ color: #94a3b8; font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; font-style: normal; }}
        .hero {{ background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%); color: white; padding: 4rem 2rem; }}
        .hero-inner {{ max-width: 800px; margin: 0 auto; }}
        .badge {{ background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.2); padding: .4rem 1rem; border-radius: 999px; font-size: .65rem; font-weight: 900; text-transform: uppercase; letter-spacing: .2em; display: inline-block; margin-bottom: 1.5rem; }}
        h1 {{ font-size: clamp(1.8rem, 4vw, 3rem); font-weight: 900; font-style: italic; line-height: 1.1; margin-bottom: 1rem; }}
        .meta {{ color: rgba(255,255,255,.6); font-size: .8rem; font-weight: 700; display: flex; gap: 1.5rem; flex-wrap: wrap; }}
        .content {{ max-width: 800px; margin: 3rem auto; padding: 0 2rem; }}
        .content h2 {{ font-size: 1.6rem; font-weight: 900; font-style: italic; margin: 2.5rem 0 1rem; color: #312e81; }}
        .content h3 {{ font-size: 1.2rem; font-weight: 700; margin: 1.5rem 0 .75rem; }}
        .content p {{ line-height: 1.8; color: #475569; margin-bottom: 1rem; }}
        .content ul, .content ol {{ padding-left: 1.5rem; margin-bottom: 1rem; color: #475569; line-height: 1.8; }}
        .faq-section {{ background: #f8fafc; border-radius: 1.5rem; padding: 2.5rem; margin: 3rem 0; border: 1px solid #e2e8f0; }}
        .faq-section h2 {{ color: #1e293b; margin-top: 0; }}
        .faq-item {{ border-bottom: 1px solid #e2e8f0; padding: 1.5rem 0; }}
        .faq-item:last-child {{ border-bottom: none; }}
        .faq-item h3 {{ color: #4338ca; font-size: 1rem; margin-bottom: .5rem; }}
        .faq-item p {{ margin: 0; font-size: .9rem; }}
        .cta {{ background: #0f172a; color: white; border-radius: 2rem; padding: 3rem; text-align: center; margin: 3rem 0; }}
        .cta h3 {{ font-size: 1.8rem; font-weight: 900; font-style: italic; margin-bottom: 1rem; }}
        .cta a {{ background: #f43f5e; color: white; padding: .9rem 2rem; border-radius: 999px; text-decoration: none; font-weight: 900; font-size: .8rem; text-transform: uppercase; letter-spacing: .1em; }}
        footer {{ background: #0f172a; color: #64748b; text-align: center; padding: 2rem; font-size: .75rem; margin-top: 4rem; }}
    </style>
</head>
<body>
    <nav class="nav">
        <a href="https://www.lifextreme.store">⚡ LIFEXTREME</a>
        <a href="https://www.lifextreme.store/blog" class="back">← Volver al Blog</a>
    </nav>
    
    <header class="hero">
        <div class="hero-inner">
            <span class="badge">📍 {articulo.region} · {articulo.dificultad}</span>
            <h1>{articulo.titulo}</h1>
            <div class="meta">
                <span><i class="ri-calendar-line"></i> {fecha_display}</span>
                <span><i class="ri-team-line"></i> Por Lifextreme Peru</span>
                <span><i class="ri-map-pin-line"></i> {articulo.region}</span>
            </div>
        </div>
    </header>
    
    <article class="content">
        {articulo.contenido_html}
        
        <section class="faq-section">
            <h2>❓ Preguntas Frecuentes</h2>
            {faq_html}
        </section>
        
        <div class="cta">
            <h3>¿Listo para tu próxima aventura?</h3>
            <p style="color:#94a3b8;margin-bottom:1.5rem;">Reserva con guías certificados y equipo homologado.</p>
            <a href="https://www.lifextreme.store/#destinos">Ver Tours Disponibles →</a>
        </div>
        
        <p style="font-size:.75rem;color:#94a3b8;margin-top:2rem;padding-top:1rem;border-top:1px solid #e2e8f0;">
            <strong>Fuente de datos:</strong> {articulo.fuente_datos}
        </p>
    </article>
    
    <footer>
        <p>© 2026 Lifextreme Peru · 
        <a href="https://www.lifextreme.store/privacidad.html" style="color:#64748b">Privacidad</a> · 
        <a href="https://www.lifextreme.store/reclamaciones.html" style="color:#64748b">Reclamaciones</a> ·
        Calle Chihuampata N° 626 - Barrio de San Blas - Cusco, Perú
        </p>
    </footer>
</body>
</html>"""

# ── Agente Principal ──────────────────────────────────────
async def generar_articulo(tema: Optional[str] = None) -> BlogArticle:
    """Genera un artículo de blog usando Pydantic AI + Gemini + CIXTUR."""
    
    if not GEMINI_KEY:
        raise ValueError("❌ GEMINI_API_KEY no encontrado en .env")
    
    # Cargar contexto del dataset real
    contexto_cixtur = cargar_cixtur(CIXTUR_PATH)
    
    # Seleccionar tema del día
    tema_del_dia = tema or random.choice(TEMAS_BLOG)
    print(f"\n📝 Generando artículo sobre: {tema_del_dia}")
    
    # Configurar API key via variable de entorno (requerido por GoogleModel)
    os.environ["GEMINI_API_KEY"] = GEMINI_KEY
    
    # Inicializar modelo Google (nueva API de pydantic-ai)
    model = GoogleModel('gemini-2.0-flash')
    
    # Crear agente con instrucciones SEO-IA
    agent = Agent(
        model=model,
        result_type=BlogArticle,
        system_prompt=f"""Eres el experto en turismo de aventura de Lifextreme Peru.
Tu misión es generar artículos de blog que:
1. Respondan preguntas REALES de viajeros (long-tail keywords)
2. Usen datos del Dataset CIXTUR cuando sea posible
3. Incluyan FAQs optimizadas para ser citadas por ChatGPT, Perplexity y Google AI Overviews
4. El HTML sea semántico con H2, H3, listas <ul> y párrafos <p>
5. El meta_description incluya una llamada a la acción y la keyword principal
6. El slug sea en minúsculas, sin tildes ni espacios

Contexto de datos reales del turismo peruano (Dataset CIXTUR):
{contexto_cixtur}

IMPORTANTE: Cita en fuente_datos de dónde tomaste el dato CIXTUR que usaste."""
    )
    
    result = await agent.run(f"Escribe un artículo SEO completo sobre: {tema_del_dia}")
    return result.data

# ── Publisher: Guarda el artículo en disco ────────────────
def publicar_articulo(articulo: BlogArticle) -> str:
    """Guarda el artículo como archivo HTML en la carpeta del blog."""
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = output_dir / f"{articulo.slug}.html"
    html = generar_html_pagina(articulo)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    # También guardar metadata en JSON para el índice del blog
    meta_path = output_dir / f"{articulo.slug}.meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "titulo": articulo.titulo,
            "slug": articulo.slug,
            "meta_description": articulo.meta_description,
            "region": articulo.region,
            "dificultad": articulo.dificultad,
            "palabras_clave": articulo.palabras_clave,
            "fecha": datetime.now().isoformat(),
            "url": f"{BASE_URL}/{articulo.slug}"
        }, f, ensure_ascii=False, indent=2)
    
    return str(filepath)

# ── Runner Principal ──────────────────────────────────────
async def main(tema: Optional[str] = None):
    print("🚀 Lifextreme Blog Agent - Iniciando...")
    print(f"📊 Dataset: {CIXTUR_PATH}")
    print(f"📁 Output: {OUTPUT_DIR}")
    
    try:
        articulo = await generar_articulo(tema)
        ruta = publicar_articulo(articulo)
        
        print(f"\n✅ Artículo generado exitosamente!")
        print(f"   📄 Título: {articulo.titulo}")
        print(f"   🔗 Slug: {articulo.slug}")
        print(f"   📍 Región: {articulo.region}")
        print(f"   🔑 Keywords: {', '.join(articulo.palabras_clave[:3])}...")
        print(f"   💾 Guardado en: {ruta}")
        print(f"   🌐 URL: {BASE_URL}/{articulo.slug}")
        
        return articulo
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    import sys
    tema_arg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    asyncio.run(main(tema_arg))
