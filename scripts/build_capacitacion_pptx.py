"""
build_capacitacion_pptx.py
Genera el PPTX del Programa LifeIntelligence Pro — Capacitacion IA para Agencias de Viaje
Estilo ejecutivo oscuro Navy + Gold (igual que la version HTML)
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import sys

# ── Paleta oficial
NAVY    = RGBColor(0x0A, 0x16, 0x28)
NAVY2   = RGBColor(0x0F, 0x20, 0x42)
GOLD    = RGBColor(0xF0, 0xB4, 0x29)
GOLD2   = RGBColor(0xFF, 0xD0, 0x60)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
MUTED   = RGBColor(0x94, 0xA3, 0xB8)
CYAN    = RGBColor(0x00, 0xE5, 0xFF)
GREEN   = RGBColor(0x00, 0xE6, 0x76)
SLATE   = RGBColor(0x1E, 0x29, 0x3B)
CARD_BG = RGBColor(0x16, 0x20, 0x36)

W = Inches(13.33)   # Widescreen 16:9
H = Inches(7.5)


def prs_init():
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H
    return prs


def add_blank(prs):
    blank = prs.slide_layouts[6]  # completely blank
    return prs.slides.add_slide(blank)


def bg(slide, color=NAVY):
    """Rellena el fondo de la diapositiva con un color solido."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def rect(slide, l, t, w, h, fill_color=None, border_color=None, border_pt=0):
    """Agrega un rectangulo de color."""
    from pptx.util import Pt as UPt
    shp = slide.shapes.add_shape(1, l, t, w, h)   # MSO_SHAPE_TYPE.RECTANGLE = 1
    if fill_color:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill_color
    else:
        shp.fill.background()
    if border_color and border_pt:
        shp.line.color.rgb = border_color
        shp.line.width = Pt(border_pt)
    else:
        shp.line.fill.background()
    return shp


def txt(slide, text, l, t, w, h,
        size=18, bold=False, italic=False, color=WHITE,
        align=PP_ALIGN.LEFT, wrap=True, font="Calibri"):
    """Agrega un cuadro de texto."""
    txb = slide.shapes.add_textbox(l, t, w, h)
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name   = font
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def eyebrow(slide, text, t=Inches(0.55)):
    txt(slide, text.upper(), Inches(0.6), t, Inches(12), Inches(0.4),
        size=9, bold=True, color=GOLD, align=PP_ALIGN.LEFT)


def title_line(slide, text, t=Inches(0.95), size=36, color=WHITE):
    txt(slide, text, Inches(0.6), t, Inches(12.1), Inches(1.4),
        size=size, bold=True, color=color, align=PP_ALIGN.LEFT, font="Montserrat")


def subtitle_line(slide, text, t=Inches(1.9), size=16, color=MUTED):
    txt(slide, text, Inches(0.6), t, Inches(10), Inches(0.6),
        size=size, color=color, align=PP_ALIGN.LEFT)


def gold_bar(slide, t=Inches(0.45), h=Inches(0.04)):
    """Barra dorada decorativa superior."""
    rect(slide, Inches(0.6), t, Inches(1.4), h, fill_color=GOLD)


def card_box(slide, l, t, w, h, title, desc, icon="", num_label="",
             title_size=13, desc_size=10.5):
    """Tarjeta con fondo oscuro, titulo y descripcion."""
    rect(slide, l, t, w, h, fill_color=CARD_BG, border_color=RGBColor(0x2D,0x3D,0x5C), border_pt=0.75)
    off = Inches(0.12)
    if icon:
        txt(slide, icon, l+off, t+off, Inches(0.5), Inches(0.4), size=18, color=WHITE)
    if num_label:
        txt(slide, num_label.upper(), l+off, t+off, w-off*2, Inches(0.25),
            size=8, bold=True, color=GOLD)
        off_title = Inches(0.4)
    else:
        off_title = Inches(0.14) if not icon else Inches(0.55)
    txt(slide, title, l+off, t+off_title, w-off*2, Inches(0.35),
        size=title_size, bold=True, color=WHITE)
    txt(slide, desc, l+off, t+off_title+Inches(0.32), w-off*2, h-off_title-Inches(0.45),
        size=desc_size, color=MUTED, wrap=True)


def stat_box(slide, l, t, number, label):
    w, h = Inches(2.6), Inches(1.4)
    rect(slide, l, t, w, h, fill_color=RGBColor(0x14,0x20,0x10), border_color=RGBColor(0x24,0x60,0x30), border_pt=0.75)
    txt(slide, number, l, t+Inches(0.12), w, Inches(0.72),
        size=34, bold=True, color=GOLD, align=PP_ALIGN.CENTER, font="Montserrat")
    txt(slide, label, l, t+Inches(0.78), w, Inches(0.5),
        size=9.5, color=MUTED, align=PP_ALIGN.CENTER, wrap=True)


def lesson_row(slide, t, icon, title, desc, dur):
    l, w, h = Inches(0.55), Inches(5.9), Inches(0.85)
    rect(slide, l, t, w, h, fill_color=CARD_BG, border_color=RGBColor(0x2A,0x3A,0x55), border_pt=0.6)
    txt(slide, icon, l+Inches(0.1), t+Inches(0.12), Inches(0.5), Inches(0.6), size=18, color=WHITE)
    txt(slide, title, l+Inches(0.65), t+Inches(0.08), Inches(4.5), Inches(0.32), size=12, bold=True, color=WHITE)
    txt(slide, desc,  l+Inches(0.65), t+Inches(0.38), Inches(4.5), Inches(0.35), size=9.5, color=MUTED, wrap=True)
    txt(slide, dur,   l+Inches(0.65), t+Inches(0.68), Inches(2), Inches(0.22), size=8.5, bold=True, color=GOLD)

    l2 = Inches(6.65)
    return l2  # segunda columna


def lesson_row2(slide, t, icon, title, desc, dur):
    l, w, h = Inches(6.9), Inches(5.9), Inches(0.85)
    rect(slide, l, t, w, h, fill_color=CARD_BG, border_color=RGBColor(0x2A,0x3A,0x55), border_pt=0.6)
    txt(slide, icon, l+Inches(0.1), t+Inches(0.12), Inches(0.5), Inches(0.6), size=18, color=WHITE)
    txt(slide, title, l+Inches(0.65), t+Inches(0.08), Inches(4.5), Inches(0.32), size=12, bold=True, color=WHITE)
    txt(slide, desc,  l+Inches(0.65), t+Inches(0.38), Inches(4.5), Inches(0.35), size=9.5, color=MUTED, wrap=True)
    txt(slide, dur,   l+Inches(0.65), t+Inches(0.68), Inches(2), Inches(0.22), size=8.5, bold=True, color=GOLD)


def price_card(slide, l, t, w, h, tier, name, amount, unit, features, featured=False):
    border = GOLD if featured else RGBColor(0x2D,0x3D,0x5C)
    bg_c   = RGBColor(0x18,0x24,0x0A) if featured else CARD_BG
    rect(slide, l, t, w, h, fill_color=bg_c, border_color=border, border_pt=1.5 if featured else 0.75)
    off = Inches(0.18)
    txt(slide, tier.upper(),  l+off, t+off,          w-off*2, Inches(0.3), size=8, bold=True, color=GOLD)
    txt(slide, name,          l+off, t+Inches(0.42), w-off*2, Inches(0.42), size=18, bold=True, color=WHITE, font="Montserrat")
    txt(slide, amount,        l+off, t+Inches(0.88), w-off*2, Inches(0.55), size=28, bold=True, color=GOLD, font="Montserrat")
    txt(slide, unit,          l+off, t+Inches(1.42), w-off*2, Inches(0.3), size=8.5, color=MUTED, wrap=True)
    for i, feat in enumerate(features):
        txt(slide, "✓  " + feat, l+off, t+Inches(1.75+i*0.33), w-off*2, Inches(0.32), size=9, color=WHITE)


# ════════════════════════════════════════
# BUILD ALL SLIDES
# ════════════════════════════════════════

def build():
    prs = prs_init()

    # ── SLIDE 1: PORTADA ──────────────────────────────────────
    sl = add_blank(prs); bg(sl, NAVY)
    # Degradado simulado con rects semitransparentes
    rect(sl, 0, 0, Inches(5), H, fill_color=RGBColor(0x0C,0x1A,0x40))
    rect(sl, 0, Inches(5.5), W, Inches(2), fill_color=RGBColor(0x08,0x12,0x28))
    # Barra dorada izquierda
    rect(sl, Inches(0.55), Inches(1.4), Inches(0.07), Inches(4.5), fill_color=GOLD)
    # Badge
    rect(sl, Inches(0.75), Inches(1.3), Inches(5.2), Inches(0.38), fill_color=RGBColor(0x20,0x18,0x04), border_color=RGBColor(0x60,0x48,0x0A), border_pt=0.6)
    txt(sl, "🤖  PROGRAMA OFICIAL DE CAPACITACION — LIFEXTREME", Inches(0.85), Inches(1.33), Inches(5), Inches(0.32), size=8.5, bold=True, color=GOLD)
    # Titulo
    txt(sl, "LifeIntelligence", Inches(0.75), Inches(1.75), Inches(9), Inches(1.3), size=58, bold=True, italic=True, color=WHITE, font="Montserrat")
    txt(sl, "Pro", Inches(0.75), Inches(2.95), Inches(5), Inches(1.0), size=68, bold=True, italic=True, color=GOLD, font="Montserrat")
    txt(sl, "Programa In-House de Inteligencia Artificial para Agencias de Viaje", Inches(0.75), Inches(4.1), Inches(8.5), Inches(0.6), size=16, color=MUTED)
    txt(sl, "Cusco & Peru  |  2026", Inches(0.75), Inches(4.65), Inches(5), Inches(0.4), size=13, color=RGBColor(0x64,0x74,0x8B))
    # Tags row
    tags = ["Turismo de Aventura","IA Generativa","Automatizacion","Precios Dinamicos","RAG & Chatbots","Marketing con IA"]
    for i, tag in enumerate(tags):
        col = i % 3
        row = i // 3
        tl = Inches(0.75 + col * 3.1)
        tt = Inches(5.35 + row * 0.52)
        rect(sl, tl, tt, Inches(2.9), Inches(0.4), fill_color=RGBColor(0x14,0x1E,0x38), border_color=RGBColor(0x2A,0x3A,0x58), border_pt=0.5)
        txt(sl, tag, tl+Inches(0.1), tt+Inches(0.06), Inches(2.7), Inches(0.28), size=10, bold=True, color=MUTED)
    # Logo bottom right
    txt(sl, "LIFEXTREME  ·  www.lifextreme.com.pe  ·  +51 958 050 928", Inches(0.75), Inches(7.1), Inches(10), Inches(0.3), size=8.5, color=RGBColor(0x40,0x50,0x68))

    # ── SLIDE 2: EL PROBLEMA ──────────────────────────────────
    sl = add_blank(prs); bg(sl)
    gold_bar(sl)
    eyebrow(sl, "El Contexto")
    title_line(sl, "Tu agencia compite contra gigantes que usan IA.\n¿La tuya tambien?", t=Inches(0.95), size=30)
    subtitle_line(sl, "Booking.com, Airbnb, GetYourGuide y Viator invierten millones en IA. Las agencias locales que\nno adopten estas herramientas perderan el 60% de sus reservas directas antes de 2027.", t=Inches(2.6), size=13)
    # Stats
    stats = [("78%","de viajeros usan IA\npara planificar su viaje"),
             ("3.4x","mas conversiones con\nchatbot vs. formulario"),
             ("-62%","costo de atencion al\ncliente con IA"),
             ("+41%","ingresos con precios\ndinamicos IA")]
    for i, (num, lab) in enumerate(stats):
        stat_box(sl, Inches(0.6 + i*3.17), Inches(4.5), num, lab)

    # ── SLIDE 3: LA SOLUCIÓN ──────────────────────────────────
    sl = add_blank(prs); bg(sl)
    gold_bar(sl)
    eyebrow(sl, "La Solucion")
    title_line(sl, "Programa LifeIntelligence Pro", size=34)
    subtitle_line(sl, "Capacitamos a tu equipo para implementar IA real, practica y funcional en tu agencia — sin programadores, sin inversiones millonarias.", t=Inches(1.95), size=13)
    cards = [
        ("🏛️","Formato","In-House en tu agencia","Capacitacion presencial en tus instalaciones. Tu equipo aprende en su propio entorno de trabajo."),
        ("⚡","Duracion","8 horas intensivas","1 dia completo (o 2 tardes de 4h). Sin teoria vacia — 70% practica hands-on."),
        ("👥","Grupos","Hasta 12 personas","Equipo completo: directores, asesores de viaje, marketing y operaciones."),
        ("🎯","Resultado","IA funcionando el Dia 1","Al terminar, tu agencia tendra herramientas activas y configuradas."),
    ]
    for i, (icon, num, title, desc) in enumerate(cards):
        card_box(sl, Inches(0.55 + i*3.2), Inches(3.0), Inches(3.05), Inches(3.9),
                 title=title, desc=desc, icon=icon, num_label=num)

    # ── SLIDES 4-8: MODULOS ───────────────────────────────────
    modulos = [
        ("01","Modulo 1  ·  60 min","Fundamentos de IA para el Sector Turistico","Del miedo a la IA → al dominio de la IA en tu agencia",[
            ("🧠","¿Que es la IA Generativa y por que importa?","GPT-4, Gemini, Claude — como funcionan y que pueden hacer por tu agencia HOY.","15 min"),
            ("🌍","Casos reales: agencias que duplicaron ventas","Ejemplos de Cusco, Lima, Colombia y Espana. Metricas y resultados verificables.","15 min"),
            ("🗺️","El ecosistema IA para turismo en 2026","Mapa de herramientas: chatbots, precios dinamicos y RAG normativo.","15 min"),
            ("⚠️","Riesgos y etica: que NO hacer con IA","ANPD, privacidad de datos, Ley 29733 y Ley 31814 de Gobernanza IA.","15 min"),
        ]),
        ("02","Modulo 2  ·  90 min  ·  PRACTICA","ChatBot IA para tu Agencia — WhatsApp + Web","Configura tu asistente virtual que responde 24/7 y cierra reservas",[
            ("💬","Arquitectura de un Chatbot Turistico con IA","Como entrenarlo con tus propios tours, precios y politicas.","20 min"),
            ("📱","Integracion con WhatsApp Business API","Setup en vivo: bot que responde cotizaciones y reservas por WhatsApp.","30 min · PRACTICA"),
            ("🌐","Bot en tu web: captura de leads automatica","Instalamos el widget. Captura nombre, destino, fecha y presupuesto.","20 min · PRACTICA"),
            ("🧩","RAG: Entrena tu bot con tu propio conocimiento","Alimenta el bot con tus PDF de tours, itinerarios, FAQs. Demo en vivo.","20 min · PRACTICA"),
        ]),
        ("03","Modulo 3  ·  75 min  ·  PRACTICA","Precios Dinamicos con IA — Vende Mas en Temporada Alta","El mismo motor que usa Booking.com — adaptado a tu agencia en Cusco",[
            ("📈","¿Como funciona el Revenue Management Turistico?","Temporada alta/baja, saturacion de rutas, prediccion de demanda.","20 min"),
            ("🤖","Motor de Precios IA: configuracion para tu agencia","Implementamos el modelo de precios por demanda, anticipacion y grupo.","25 min · PRACTICA"),
            ("🎯","Oferta dinamica por perfil de viajero","IA que detecta si el cliente es mochilero, familiar o corporativo.","15 min · PRACTICA"),
            ("🛡️","Anti-Overtourism: prediccion y redireccion de flujos","Detecta saturacion en Vinicunca / Machu Picchu y propone alternativas.","15 min"),
        ]),
        ("04","Modulo 4  ·  90 min  ·  PRACTICA","Marketing Digital con IA — Contenido, Email y Redes","Genera en minutos lo que antes tardabas dias — con calidad profesional",[
            ("✍️","Generacion de contenido con IA: tours y blogs","Descripciones de tours, blogs SEO y propuestas personalizadas en segundos.","25 min · PRACTICA"),
            ("📧","Secuencias de Email Marketing Automaticas","5 correos de bienvenida, follow-up y reactivacion con Zoho Campaigns + IA.","25 min · PRACTICA"),
            ("📸","Imagenes y videos con IA para Instagram y TikTok","Midjourney, Runway ML y CapCut AI: contenido visual sin fotografo.","20 min · PRACTICA"),
            ("🔍","SEO + AEO + GEO con IA: aparece en Google y en ChatGPT","Optimiza tu web para que la IA recomiende tu agencia organicamente.","20 min"),
        ]),
        ("05","Modulo 5  ·  60 min  ·  PRACTICA","CRM Inteligente + API B2B para Operadores","Gestiona leads, reservas y partners desde un sistema con IA integrada",[
            ("📊","CRM con IA: pipeline de ventas automatico","Zoho CRM configurado con IA: scoring de leads y seguimiento automatico.","20 min · PRACTICA"),
            ("🔗","API B2B: conectate con operadores y mayoristas","Sincronizacion de inventario en tiempo real. Socios reservan sin llamadas.","20 min"),
            ("📱","Dashboard de analytics en tiempo real","Looker Studio + GA4: visualiza reservas y conversiones con IA.","10 min"),
            ("🤝","Red de aliados automatizada con comisiones","Sistema de referidos con tracking automatico y liquidacion de comisiones.","10 min"),
        ]),
    ]

    for mod_num, mod_time, mod_title, mod_sub, lessons in modulos:
        sl = add_blank(prs); bg(sl)
        gold_bar(sl)
        # Numero grande decorativo
        txt(sl, mod_num, Inches(10.5), Inches(0.3), Inches(2.5), Inches(2.0), size=90, bold=True, color=RGBColor(0x14,0x24,0x44), font="Montserrat")
        eyebrow(sl, mod_time)
        title_line(sl, mod_title, size=28)
        subtitle_line(sl, mod_sub, t=Inches(1.9), size=12, color=MUTED)
        # 4 lecciones en 2 columnas x 2 filas
        t_rows = [Inches(2.6), Inches(3.6), Inches(4.6), Inches(5.6)]
        for idx, (icon, ltitle, ldesc, ldur) in enumerate(lessons):
            row = idx % 2
            col = idx // 2
            lt = t_rows[row + col*0]
            if idx < 2:
                lesson_row(sl, t_rows[idx], icon, ltitle, ldesc, ldur)
            else:
                lesson_row2(sl, t_rows[idx-2], icon, ltitle, ldesc, ldur)

    # ── SLIDE 9: HERRAMIENTAS ─────────────────────────────────
    sl = add_blank(prs); bg(sl)
    gold_bar(sl)
    eyebrow(sl, "Stack Tecnologico")
    title_line(sl, "Las 12 Herramientas IA que implementamos en tu agencia", size=26)
    tools = [
        ("🤖","ChatGPT / Gemini","Redaccion de tours, respuestas y\nitinerarios personalizados al instante.","→ Ahorra 3h/dia de escritura"),
        ("🗃️","Qdrant RAG","Tu chatbot entrenado con tus propios\ndocumentos, precios y politicas.","→ Bot que sabe TODO de tu agencia"),
        ("📱","WhatsApp Business AI","Automatiza cotizaciones y seguimiento\npor WhatsApp sin intervencion humana.","→ Responde 24/7 sin personal extra"),
        ("📧","Zoho Campaigns IA","Secuencias automaticas, A/B testing y\npersonalizacion por perfil de cliente.","→ Emails que se escriben solos"),
        ("🎨","Midjourney + Runway","Genera imagenes y videos de tus\ndestinos para Instagram y TikTok.","→ Sin fotografo ni disenador"),
        ("📊","Google Analytics 4","Predicciones de comportamiento,\naudiencias y alertas inteligentes.","→ Decisiones basadas en datos reales"),
        ("💰","Motor de Precios IA","Ajuste dinamico por demanda,\ntemporalidad y perfil de cliente.","→ +41% ingresos temporada alta"),
        ("🔍","SEO / AEO / GEO","Optimiza para Google Y para que\nChatGPT/Gemini recomienden tu agencia.","→ Aparece donde buscan tus clientes"),
        ("🤝","Supabase CRM","Base de datos inteligente con scoring\nautomatico y seguimiento predictivo.","→ Cierra mas ventas, menos esfuerzo"),
    ]
    cols, rows = 3, 3
    for i, (icon, name, desc, use) in enumerate(tools):
        col = i % cols
        row = i // cols
        l = Inches(0.55 + col * 4.26)
        t = Inches(1.9  + row * 1.82)
        w, h = Inches(4.0), Inches(1.65)
        rect(sl, l, t, w, h, fill_color=CARD_BG, border_color=RGBColor(0x2D,0x3D,0x5C), border_pt=0.6)
        txt(sl, icon+" "+name, l+Inches(0.12), t+Inches(0.1), w-Inches(0.24), Inches(0.35), size=12, bold=True, color=WHITE)
        txt(sl, desc, l+Inches(0.12), t+Inches(0.46), w-Inches(0.24), Inches(0.7), size=9.5, color=MUTED, wrap=True)
        txt(sl, use,  l+Inches(0.12), t+Inches(1.3), w-Inches(0.24), Inches(0.28), size=9, bold=True, color=GOLD)

    # ── SLIDE 10: CRONOGRAMA ──────────────────────────────────
    sl = add_blank(prs); bg(sl)
    gold_bar(sl)
    eyebrow(sl, "Agenda del Dia")
    title_line(sl, "Programa de 8 horas intensivas", size=30)
    schedule = [
        ("08:30","Bienvenida + Diagnostico de tu Agencia","Mapeamos herramientas actuales y potencial de mejora","30 min"),
        ("09:00","Modulo 1: Fundamentos de IA para Turismo","Contexto, casos reales y ecosistema de herramientas","60 min"),
        ("10:00","Modulo 2: ChatBot IA — WhatsApp + Web","PRACTICA: configuramos el bot de tu agencia en vivo","90 min"),
        ("11:30","Break — Networking + cafe","Preguntas uno a uno con el instructor","20 min"),
        ("11:50","Modulo 3: Precios Dinamicos con IA","PRACTICA: motor de revenue management configurado","75 min"),
        ("01:05","Almuerzo de trabajo (incluido)","Seguimos conversando casos de tu agencia","60 min"),
        ("02:05","Modulo 4: Marketing Digital con IA","PRACTICA: email, contenido y SEO/AEO/GEO","90 min"),
        ("03:35","Modulo 5: CRM + API B2B","PRACTICA: pipeline de ventas inteligente activo","60 min"),
        ("04:35","Cierre: Plan de Implementacion 30 dias","Hoja de ruta personalizada + materiales + soporte","30 min"),
    ]
    for i, (hora, titulo, sub, dur) in enumerate(schedule):
        t = Inches(1.55 + i * 0.65)
        rect(sl, Inches(0.55), t, Inches(12.2), Inches(0.58), fill_color=CARD_BG, border_color=RGBColor(0x25,0x35,0x52), border_pt=0.5)
        txt(sl, hora, Inches(0.65), t+Inches(0.08), Inches(0.9), Inches(0.42), size=10, bold=True, color=GOLD)
        txt(sl, titulo, Inches(1.65), t+Inches(0.05), Inches(8.5), Inches(0.28), size=11, bold=True, color=WHITE)
        txt(sl, sub,   Inches(1.65), t+Inches(0.3),  Inches(8.5), Inches(0.22), size=9, color=MUTED)
        rect(sl, Inches(10.5), t+Inches(0.1), Inches(1.9), Inches(0.38), fill_color=RGBColor(0x20,0x30,0x14), border_color=RGBColor(0x40,0x60,0x20), border_pt=0.5)
        txt(sl, dur, Inches(10.5), t+Inches(0.1), Inches(1.9), Inches(0.38), size=9, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

    # ── SLIDE 11: DIFERENCIALES ───────────────────────────────
    sl = add_blank(prs); bg(sl)
    gold_bar(sl)
    eyebrow(sl, "¿Por que Lifextreme?")
    title_line(sl, "No ensenamos IA de libro.\nEnsenamos la IA que nosotros usamos.", size=28)
    diffs = [
        ("🏔️","Experiencia real en turismo peruano","Operamos tours de aventura en Cusco. Conocemos permisos SERNANP, estacionalidad, operadores B2B y turismo extranjero."),
        ("🧠","18,932 vectores de conocimiento normativo","Nuestro sistema RAG contiene toda la legislacion turistica peruana (MINCETUR, SERNANP, INDECOPI) vectorizada y activa."),
        ("⚡","70% practica — salís con herramientas funcionando","Al terminar, tu agencia tiene el bot configurado, emails automatizados y CRM activo. Resultado el Dia 1."),
        ("🛡️","Cumplimiento legal incluido (Ley 29733 / 31814)","Implementamos IA dentro del marco de la Ley de Proteccion de Datos y la nueva Ley de Gobernanza de IA en Peru."),
        ("🤝","Soporte 30 dias post-taller","Canal de soporte por WhatsApp durante 30 dias. No quedas solo con las herramientas — acompanamos la implementacion."),
        ("🔗","Red de partners B2B Lifextreme","Agencias que completan el programa ingresan a nuestra red y reciben referidos de clientes que buscan tours complementarios."),
    ]
    for i, (icon, title, desc) in enumerate(diffs):
        col = i % 2
        row = i // 2
        l = Inches(0.55 + col * 6.4)
        t = Inches(2.55 + row * 1.6)
        w, h = Inches(6.1), Inches(1.4)
        rect(sl, l, t, w, h, fill_color=CARD_BG, border_color=RGBColor(0x2A,0x3A,0x55), border_pt=0.6)
        txt(sl, icon, l+Inches(0.12), t+Inches(0.12), Inches(0.5), Inches(0.6), size=20, color=WHITE)
        txt(sl, title, l+Inches(0.72), t+Inches(0.1), w-Inches(0.9), Inches(0.38), size=12, bold=True, color=WHITE)
        txt(sl, desc,  l+Inches(0.72), t+Inches(0.5), w-Inches(0.9), Inches(0.75), size=9.5, color=MUTED, wrap=True)

    # ── SLIDE 12: PRECIOS ─────────────────────────────────────
    sl = add_blank(prs); bg(sl)
    gold_bar(sl)
    eyebrow(sl, "Inversion")
    title_line(sl, "Planes de Capacitacion — ROI medible en 60 dias", size=28)
    plans = [
        (False,"ESENCIAL","Starter","S/ 1,800","hasta 4 personas · 4 horas · Modulos 1 y 2",
         ["Fundamentos de IA en Turismo","ChatBot WhatsApp + Web configurado","Base de datos RAG con tus tours","Material digital completo","Soporte 15 dias"]),
        (True,"PROFESIONAL","Pro Agency","S/ 3,900","hasta 8 personas · 8 horas · Todos los modulos",
         ["Los 5 modulos completos (8 horas)","Bot IA + Precios Dinamicos + CRM","Email marketing automatico activo","API B2B configurada","Almuerzo incluido","Soporte 30 dias · Red partners Lifextreme"]),
        (False,"CORPORATIVO","Enterprise","S/ 6,500","hasta 15 personas · 2 dias · Implementacion asistida",
         ["Programa completo 2 dias","Implementacion asistida por agencia","Modulo extra: seguros de aventura","Dashboard compartido de analytics","Soporte 60 dias dedicado","Certificado oficial Lifextreme IA"]),
    ]
    for i, (feat, tier, name, amount, unit, features) in enumerate(plans):
        price_card(sl, Inches(0.5 + i*4.3), Inches(1.9), Inches(4.1), Inches(5.3),
                   tier, name, amount, unit, features, featured=feat)
    if True:  # badge "mas popular" for middle card
        rect(sl, Inches(4.6), Inches(1.72), Inches(2.1), Inches(0.3), fill_color=GOLD)
        txt(sl, "⭐  MAS POPULAR", Inches(4.6), Inches(1.72), Inches(2.1), Inches(0.3), size=8, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

    # ── SLIDE 13: ENTREGABLES ─────────────────────────────────
    sl = add_blank(prs); bg(sl)
    gold_bar(sl)
    eyebrow(sl, "Entregables")
    title_line(sl, "¿Que se lleva tu agencia al terminar el programa?", size=28)
    entregables = [
        ("✅ ChatBot WhatsApp configurado con tus tours", GREEN),
        ("✅ Bot en tu web capturando leads 24/7", GREEN),
        ("✅ Base de conocimiento RAG con tus documentos", GREEN),
        ("📧 5 secuencias de email marketing activas", CYAN),
        ("📊 Dashboard GA4 con eventos de reserva", CYAN),
        ("🔗 CRM con pipeline de ventas configurado", CYAN),
        ("🎯 Motor de precios dinamicos activado", GOLD),
        ("📸 Guia de contenido IA para redes sociales", GOLD),
        ("🗺️ Plan de implementacion personalizado 30 dias", GOLD),
        ("📚 Acceso a todos los materiales y grabaciones", WHITE),
        ("🏆 Certificado LifeIntelligence Pro", WHITE),
        ("🤝 Ingreso a la red de partners Lifextreme", WHITE),
    ]
    for i, (ent, color) in enumerate(entregables):
        col = i % 3
        row = i // 3
        l = Inches(0.55 + col * 4.26)
        t = Inches(2.0  + row * 0.9)
        rect(sl, l, t, Inches(4.0), Inches(0.72), fill_color=CARD_BG, border_color=RGBColor(0x25,0x38,0x52), border_pt=0.5)
        txt(sl, ent, l+Inches(0.12), t+Inches(0.14), Inches(3.76), Inches(0.44), size=10.5, bold=True, color=color, wrap=True)
    # Stats
    for i, (num, lab) in enumerate([("12","Herramientas IA\ninstaladas"),("30","Dias de soporte\npost-taller"),("60","Dias para\nROI medible")]):
        stat_box(sl, Inches(1.5 + i * 3.5), Inches(5.85), num, lab)

    # ── SLIDE 14: CTA ─────────────────────────────────────────
    sl = add_blank(prs); bg(sl, RGBColor(0x06,0x14,0x08))
    rect(sl, 0, 0, W, H, fill_color=RGBColor(0x06,0x12,0x06))
    gold_bar(sl)
    eyebrow(sl, "¡Empecemos!")
    txt(sl, "2026", Inches(0.6), Inches(0.9), Inches(6), Inches(2.0), size=90, bold=True, color=GOLD, font="Montserrat")
    title_line(sl, "Es el año en que tu agencia da el salto a la IA real.", t=Inches(3.0), size=28)
    # Oferta
    rect(sl, Inches(0.6), Inches(4.0), Inches(12.1), Inches(1.0), fill_color=RGBColor(0x0C,0x24,0x0C), border_color=RGBColor(0x20,0x60,0x20), border_pt=0.75)
    txt(sl, "🔥  Los primeros 5 grupos que reserven antes del 30 de noviembre obtienen el plan Pro por el precio del Starter  (S/ 1,800 en vez de S/ 3,900)",
        Inches(0.75), Inches(4.1), Inches(11.8), Inches(0.8), size=13, bold=True, color=GREEN)
    # Contacto
    contacts = ["📱  +51 958 050 928", "📧  contacto@lifextreme.com.pe", "🌐  www.lifextreme.com.pe", "📍  San Blas 626, Cusco"]
    for i, c in enumerate(contacts):
        l = Inches(0.6 + i * 3.18)
        rect(sl, l, Inches(5.3), Inches(3.0), Inches(0.75), fill_color=CARD_BG, border_color=RGBColor(0x2A,0x3A,0x55), border_pt=0.6)
        txt(sl, c, l+Inches(0.12), Inches(5.37), Inches(2.76), Inches(0.6), size=11, bold=True, color=WHITE)

    return prs


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "LifeIntelligence_Pro_Capacitacion_IA_Agencias.pptx"
    prs = build()
    prs.save(out)
    print(f"PPTX generado: {out}")
