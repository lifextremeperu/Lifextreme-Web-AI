import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ==============================================================================
# STRICT LIFEXTREME LOGO PALETTE ONLY (Extracted from LIFEXTREME OUTDOOR EXPERIENCE)
# ==============================================================================
C_OBSIDIAN = (2, 6, 24)        # #020618 Deep Midnight ("LIFE")
C_CARD     = (15, 19, 36)      # #0f1324 Dark Card Surface
C_SLATE_BD = (42, 49, 72)      # #2a3148 Subtle Border
C_ORANGE   = (255, 142, 29)    # #ff8e1d Vivid Adventure Orange ("X")
C_MAGMA    = (244, 63, 94)     # #f43f5e Magma Crimson ("TREME")
C_STEEL    = (148, 164, 187)   # #94a4bb Steel Slate ("OUTDOOR EXPERIENCE")
C_WHITE    = (255, 255, 255)   # #ffffff Crisp White

RGB_WHITE  = RGBColor(*C_WHITE)
RGB_STEEL  = RGBColor(*C_STEEL)
RGB_ORANGE = RGBColor(*C_ORANGE)
RGB_MAGMA  = RGBColor(*C_MAGMA)

BG_DIR = "scratch/pitch_canvases_v2"
os.makedirs(BG_DIR, exist_ok=True)
W, H = 1920, 1080


def font(size, bold=False):
    paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def load_crop(path, tw, th, darken=0.55, sat=1.1):
    if not os.path.exists(path):
        return Image.new("RGB", (tw, th), C_CARD)
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    sc = max(tw / iw, th / ih)
    nw, nh = int(iw * sc), int(ih * sc)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    img = img.crop(((nw - tw) // 2, (nh - th) // 2, (nw + tw) // 2, (nh + th) // 2))
    img = ImageEnhance.Color(img).enhance(sat)
    img = ImageEnhance.Brightness(img).enhance(darken)
    return img


def make_base(photo=None, opacity=0.22):
    base = Image.new("RGBA", (W, H), (*C_OBSIDIAN, 255))
    if photo and os.path.exists(photo):
        ph = load_crop(photo, W, H, darken=0.55, sat=1.15).convert("RGBA")
        mask = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(mask)
        for x in range(W):
            val = int(255 * opacity * (0.35 + 0.65 * (x / W)))
            md.line([(x, 0), (x, H)], fill=val)
        base = Image.composite(ph, base, mask)

    # Subtle Orange & Magma ambient glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-200, -150, 700, 650], fill=(*C_ORANGE, 28))
    gd.ellipse([1250, 450, 2100, 1200], fill=(*C_MAGMA, 26))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=110))
    base = Image.alpha_composite(base, glow)

    # Top Orange-to-Magma gradient bar
    d = ImageDraw.Draw(base)
    for x in range(W):
        t = x / W
        r = int(C_ORANGE[0] * (1 - t) + C_MAGMA[0] * t)
        g = int(C_ORANGE[1] * (1 - t) + C_MAGMA[1] * t)
        b = int(C_ORANGE[2] * (1 - t) + C_MAGMA[2] * t)
        d.line([(x, 0), (x, 8)], fill=(r, g, b, 255))

    d.line([(100, 155), (1820, 155)], fill=(*C_SLATE_BD, 220), width=2)
    d.rectangle([0, 1028, W, 1080], fill=(*C_OBSIDIAN, 240))
    d.line([(100, 1028), (1820, 1028)], fill=(*C_SLATE_BD, 180), width=1)
    return base


def card(canvas, x, y, w, h, accent=C_ORANGE, photo=None, photo_h=220):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle([x + 4, y + 6, x + w + 4, y + h + 6], radius=16, fill=(0, 0, 0, 120))
    od.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=(*C_CARD, 225), outline=(*accent, 210), width=2)
    od.rounded_rectangle([x + 2, y + 2, x + w - 2, y + 7], radius=3, fill=(*accent, 255))
    res = Image.alpha_composite(canvas, ov)

    if photo and os.path.exists(photo):
        ph = load_crop(photo, w - 4, photo_h, darken=0.80, sat=1.2).convert("RGBA")
        pm = Image.new("L", (w - 4, photo_h), 0)
        pmd = ImageDraw.Draw(pm)
        pmd.rounded_rectangle([0, 0, w - 4, photo_h + 20], radius=14, fill=255)
        for py in range(photo_h):
            mult = 1.0 if py < photo_h * 0.6 else (1.0 - (py - photo_h * 0.6) / (photo_h * 0.4))
            for px in range(w - 4):
                pm.putpixel((px, py), int(pm.getpixel((px, py)) * mult))
        res.paste(ph, (x + 2, y + 6), pm)
    return res


def build_slides():
    canvases = []

    # --- SLIDE 1: COVER ---
    c = make_base("assets/images/neuromarketing/hero_tech_andes.jpg", 0.45)
    tiles = [
        ("assets/images/destinos/huaraz/alpinismo.jpg", 1040, 110, 395, 280, C_ORANGE, "ALPINISMO >5,000M"),
        ("assets/images/destinos/cusco/ciclismo.jpg", 1455, 110, 385, 280, C_MAGMA, "DOWNHILL 3D DEM"),
        ("assets/images/destinos/arequipa/rafting.jpg", 1040, 410, 385, 280, C_MAGMA, "RAFTING CLASE V"),
        ("assets/images/neuromarketing/qdrant_brain.jpg", 1445, 410, 395, 280, C_ORANGE, "336,869 VECTORES"),
    ]
    for p, x, y, w, h, col, cap in tiles:
        c = card(c, x, y, w, h, col)
        im = load_crop(p, w - 12, h - 46, darken=0.85, sat=1.25).convert("RGBA")
        c.paste(im, (x + 6, y + 8))
        d = ImageDraw.Draw(c)
        d.text((x + 16, y + h - 30), cap, fill=(*C_WHITE, 255), font=font(15, bold=True))

    # Bottom 4 Big Numbers Strip
    c = card(c, 100, 735, 1740, 245, C_ORANGE)
    d = ImageDraw.Draw(c)
    stats = [
        ("336K+", "Vectores Qdrant", C_ORANGE),
        ("251", "Rutas Extremas", C_WHITE),
        ("164", "Parques Mapeados", C_ORANGE),
        ("$0.00", "Costo Marginal IA", C_MAGMA),
    ]
    for i, (val, lbl, col) in enumerate(stats):
        sx = 145 + i * 425
        d.rounded_rectangle([sx, 765, sx + 385, 950], radius=14, fill=(*C_OBSIDIAN, 245), outline=(*col, 200), width=2)
        d.text((sx + 28, 785), val, fill=(*col, 255), font=font(56, bold=True))
        d.text((sx + 28, 868), lbl.upper(), fill=(*C_STEEL, 255), font=font(18, bold=True))
    p1 = os.path.join(BG_DIR, "s1.png")
    c.save(p1)
    canvases.append(p1)

    # --- SLIDE 2: THE PROBLEM (VISUAL) ---
    c = make_base("assets/images/destinos/cusco/choquequirao.jpg", 0.25)
    # Left: Big 30% vs 90% Retention Graphic
    c = card(c, 100, 195, 840, 790, C_MAGMA)
    d = ImageDraw.Draw(c)
    d.text((140, 230), "OTAS EXTRACTIVAS VS LIFEXTREME", fill=(*C_WHITE, 255), font=font(24, bold=True))
    d.text((140, 268), "Retencion de valor por cada reserva de $100 USD", fill=(*C_STEEL, 255), font=font(16))

    d.text((140, 355), "Viator / GetYourGuide", fill=(*C_STEEL, 255), font=font(20, bold=True))
    d.rounded_rectangle([140, 395, 890, 465], radius=10, fill=(*C_OBSIDIAN, 255))
    d.rounded_rectangle([140, 395, 365, 465], radius=10, fill=(*C_MAGMA, 255))
    d.text((160, 416), "-30% Comision", fill=(*C_WHITE, 255), font=font(20, bold=True))
    d.text((400, 416), "Sin IA ni Seguridad", fill=(*C_STEEL, 255), font=font(20, bold=True))

    d.text((140, 525), "Lifextreme AI (Split-Pay)", fill=(*C_ORANGE, 255), font=font(20, bold=True))
    d.rounded_rectangle([140, 565, 890, 635], radius=10, fill=(*C_ORANGE, 255))
    d.rounded_rectangle([140, 565, 225, 635], radius=10, fill=(*C_MAGMA, 255))
    d.text((155, 586), "10%", fill=(*C_WHITE, 255), font=font(20, bold=True))
    d.text((255, 586), "90% PARA EL OPERADOR LOCAL", fill=(*C_OBSIDIAN, 255), font=font(22, bold=True))

    # Big Callout
    d.rounded_rectangle([140, 710, 890, 930], radius=16, fill=(*C_OBSIDIAN, 245), outline=(*C_MAGMA, 220), width=2)
    d.text((175, 740), "4,200m+", fill=(*C_MAGMA, 255), font=font(64, bold=True))
    d.text((175, 830), "ZONA SIN SENAL CLOUD · RIESGO HAPE 96%", fill=(*C_WHITE, 255), font=font(20, bold=True))
    d.text((175, 868), "Las apps tradicionales colapsan donde mas se necesitan.", fill=(*C_STEEL, 255), font=font(16))

    # Right 3 crisp problem tiles
    for i, col in enumerate([C_MAGMA, C_ORANGE, C_MAGMA]):
        c = card(c, 980, 195 + i * 270, 840, 245, col)
    p2 = os.path.join(BG_DIR, "s2.png")
    c.save(p2)
    canvases.append(p2)

    # --- SLIDE 3: THE SOLUTION (3 VISUAL PILLARS) ---
    c = make_base("assets/images/destinos/huaraz/alpinismo.jpg", 0.25)
    pillars = [
        (100, C_ORANGE, "assets/images/destinos/cusco/trekking.jpg"),
        (685, C_MAGMA, "assets/images/neuromarketing/qdrant_brain.jpg"),
        (1270, C_ORANGE, "assets/images/destinos/cusco.jpg"),
    ]
    for x, col, ph in pillars:
        c = card(c, x, 195, 550, 790, col, photo=ph, photo_h=300)
    p3 = os.path.join(BG_DIR, "s3.png")
    c.save(p3)
    canvases.append(p3)

    # --- SLIDE 4: TRACTION & VELOCITY (JAN 6 - NOV 2026) ---
    c = make_base("assets/images/neuromarketing/qdrant_brain.jpg", 0.22)
    # 4 Big Metric Cards across top
    for i, col in enumerate([C_ORANGE, C_MAGMA, C_ORANGE, C_MAGMA]):
        c = card(c, 100 + i * 440, 195, 410, 280, col)

    # Bottom Velocity Chart
    c = card(c, 100, 515, 1720, 470, C_ORANGE)
    d = ImageDraw.Draw(c)
    d.text((140, 545), "CRECIMIENTO DEL CEREBRO VECTORIAL QDRANT (ENE 06 -> NOV 2026)", fill=(*C_WHITE, 255), font=font(22, bold=True))

    gx, gy, gw, gh = 160, 915, 1580, 265
    d.line([(gx, gy), (gx + gw, gy)], fill=(*C_STEEL, 180), width=2)
    months = ["Ene 06", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov 2026"]
    vals = [2, 15, 32, 55, 105, 150, 200, 250, 295, 322, 336.8]
    pts = []
    for i, v in enumerate(vals):
        px = gx + int((i / (len(vals) - 1)) * gw)
        py = gy - int((v / 350.0) * gh)
        pts.append((px, py))
        d.text((px - 22, gy + 12), months[i], fill=(*C_STEEL, 255), font=font(15, bold=True))

    al = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ald = ImageDraw.Draw(al)
    ald.polygon([(gx, gy)] + pts + [(gx + gw, gy)], fill=(*C_ORANGE, 55))
    c = Image.alpha_composite(c, al)
    d = ImageDraw.Draw(c)
    d.line(pts, fill=(*C_ORANGE, 255), width=5)
    for i, (px, py) in enumerate(pts):
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(*C_MAGMA, 255), outline=(*C_WHITE, 255), width=2)
        if i in [0, 4, 7, 10]:
            d.text((px - 24, py - 34), f"{vals[i]}K", fill=(*C_WHITE, 255), font=font(18, bold=True))

    p4 = os.path.join(BG_DIR, "s4.png")
    c.save(p4)
    canvases.append(p4)

    # --- SLIDE 5: GEOINT 3D & ALTIMETRIC PROFILE ---
    c = make_base("assets/images/destinos/cusco/ciclismo.jpg", 0.28)
    c = card(c, 100, 195, 1140, 790, C_ORANGE)
    d = ImageDraw.Draw(c)
    d.text((140, 230), "PERFIL ALTIMETRICO EN VIVO · RUTA SALKANTAY - MACHU PICCHU", fill=(*C_WHITE, 255), font=font(22, bold=True))
    d.text((140, 265), "Telemetria Three.js / CesiumJS + Trenes Turf.js + Alertas HAPE", fill=(*C_STEEL, 255), font=font(16))

    gx, gy, gw, gh = 155, 760, 1020, 390
    d.rectangle([gx, gy - gh, gx + gw, gy - int(gh * 0.62)], fill=(58, 16, 30, 255))
    d.line([(gx, gy - int(gh * 0.62)), (gx + gw, gy - int(gh * 0.62))], fill=(*C_MAGMA, 255), width=2)
    d.text((gx + 16, gy - gh + 14), "ZONA CRITICA >4,000m (ALERTA AUTOMATICA MAX AI)", fill=(*C_MAGMA, 255), font=font(16, bold=True))

    wpts = [
        ("Cusco\n3,400m", 0.0, 0.50, C_ORANGE),
        ("Mollepata\n2,900m", 0.17, 0.34, C_STEEL),
        ("Soraypampa\n3,900m", 0.35, 0.60, C_ORANGE),
        ("ABRA SALKANTAY\n4,630m", 0.52, 0.90, C_MAGMA),
        ("Chaullay\n2,900m", 0.70, 0.34, C_STEEL),
        ("Tren\n1,890m", 0.85, 0.15, C_ORANGE),
        ("Machu Picchu\n2,430m", 1.0, 0.28, C_WHITE),
    ]
    pts = [(gx + int(rx * gw), gy - int(ry * gh), nm, col) for nm, rx, ry, col in wpts]
    al = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ald = ImageDraw.Draw(al)
    ald.polygon([(gx, gy)] + [(p[0], p[1]) for p in pts] + [(gx + gw, gy)], fill=(*C_ORANGE, 55))
    c = Image.alpha_composite(c, al)
    d = ImageDraw.Draw(c)
    d.line([(p[0], p[1]) for p in pts], fill=(*C_ORANGE, 255), width=5)
    d.line([(gx, gy), (gx + gw, gy)], fill=(*C_STEEL, 220), width=2)
    for px, py, nm, col in pts:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(*col, 255), outline=(*C_WHITE, 255), width=2)
        d.text((px - 38, py - 48), nm, fill=(*C_WHITE, 255), font=font(15, bold=True))

    # Bottom 3 compact pills
    for i, txt in enumerate(["CesiumJS / Three.js 3D", "Turf.js Trenes en Vivo", "HLS Webcams Cordillera"]):
        bx = 150 + i * 345
        d.rounded_rectangle([bx, 835, bx + 325, 925], radius=12, fill=(*C_OBSIDIAN, 245), outline=(*C_ORANGE, 200), width=2)
        d.text((bx + 24, 868), txt, fill=(*C_WHITE, 255), font=font(18, bold=True))

    c = card(c, 1280, 195, 540, 790, C_MAGMA, photo="assets/images/destinos/cusco.jpg", photo_h=340)
    p5 = os.path.join(BG_DIR, "s5.png")
    c.save(p5)
    canvases.append(p5)

    # --- SLIDE 6: NEURAL BRAIN & ARCHITECTURE ---
    c = make_base("assets/images/neuromarketing/opensource_hero_system.jpg", 0.20)
    c = card(c, 100, 195, 1020, 790, C_ORANGE)
    d = ImageDraw.Draw(c)
    d.text((140, 230), "ARQUITECTURA SOBERANA EN 4 CAPAS", fill=(*C_WHITE, 255), font=font(22, bold=True))
    layers = [
        ("1. EDGE & 3D", "Vercel + Three.js + neural-brain-3d.html (4,481 Nodos)", C_ORANGE),
        ("2. AGENTES IA", "FastAPI SSE + Pydantic-AI (MAX B2C & CORE B2B)", C_MAGMA),
        ("3. PROTOCOLO MCP", "SUTRAN · SENAMHI · MINCETUR · SERNANP · IGP", C_ORANGE),
        ("4. EDGE CLUSTER CUSCO", "Qdrant (336K Vec) + Supabase RLS + Ollama ($0/token)", C_MAGMA),
    ]
    for i, (lt, ld, col) in enumerate(layers):
        ly = 310 + i * 165
        d.rounded_rectangle([140, ly, 1080, ly + 125], radius=14, fill=(*C_OBSIDIAN, 245), outline=(*col, 220), width=2)
        d.rectangle([140, ly, 156, ly + 125], fill=(*col, 255))
        d.text((180, ly + 22), lt, fill=(*col, 255), font=font(22, bold=True))
        d.text((180, ly + 64), ld, fill=(*C_WHITE, 255), font=font(18))

    c = card(c, 1160, 195, 660, 790, C_MAGMA, photo="assets/images/neuromarketing/qdrant_brain.jpg", photo_h=340)
    p6 = os.path.join(BG_DIR, "s6.png")
    c.save(p6)
    canvases.append(p6)

    # --- SLIDE 7: UNIT ECONOMICS & COST CHART ---
    c = make_base("assets/images/destinos/arequipa/rafting.jpg", 0.20)
    c = card(c, 100, 195, 1040, 790, C_ORANGE)
    d = ImageDraw.Draw(c)
    d.text((140, 230), "COSTO POR 1 MILLON DE CONSULTAS RAG", fill=(*C_WHITE, 255), font=font(24, bold=True))
    d.text((140, 266), "Ahorro de 98.4% al operar en nuestro Cluster Edge AI local", fill=(*C_STEEL, 255), font=font(16))

    bars = [
        ("APIs Comerciales (OpenAI / Claude)", 30000, "$30,000", C_MAGMA),
        ("Nube Vectorial + LLM Serverless", 12500, "$12,500", C_STEEL),
        ("Lifextreme Hibrido (Groq + Qdrant)", 1800, "$1,800", C_ORANGE),
        ("Lifextreme Edge AI Cusco (Ollama)", 450, "$0 Marginal", C_WHITE),
    ]
    for i, (lbl, val, txt, col) in enumerate(bars):
        by = 340 + i * 145
        d.text((140, by), lbl, fill=(*C_WHITE, 255), font=font(19, bold=True))
        mw = 670
        bw = max(30, int((val / 30000.0) * mw))
        d.rounded_rectangle([140, by + 38, 140 + mw, by + 84], radius=10, fill=(*C_OBSIDIAN, 255))
        d.rounded_rectangle([140, by + 38, 140 + bw, by + 84], radius=10, fill=(*col, 255))
        d.text((140 + mw + 22, by + 44), txt, fill=(*col, 255), font=font(26, bold=True))

    c = card(c, 1180, 195, 640, 790, C_MAGMA)
    p7 = os.path.join(BG_DIR, "s7.png")
    c.save(p7)
    canvases.append(p7)

    # --- SLIDE 8: MARKET (TAM / SAM / SOM) & PROJECTION ---
    c = make_base("assets/images/destinos/arequipa/volcan.jpg", 0.22)
    c = card(c, 100, 195, 830, 790, C_ORANGE)
    d = ImageDraw.Draw(c)
    d.text((140, 230), "MERCADO DIRECCIONABLE (CAGR 14.8%)", fill=(*C_WHITE, 255), font=font(22, bold=True))

    cx, cy = 515, 480
    spheres = [
        (205, (36, 28, 52, 255), C_STEEL, "TAM · $15.4B", "Turismo Aventura LATAM"),
        (142, (62, 34, 20, 255), C_ORANGE, "SAM · $2.4B", "Corredor Andino"),
        (82, (68, 18, 34, 255), C_MAGMA, "SOM · $48M", "Meta 24 Meses (450 Agencias)"),
    ]
    for r, fc, col, t, s in spheres:
        d.ellipse([cx - r, cy + (205 - r) - r, cx + r, cy + (205 - r) + r], fill=fc, outline=(*col, 255), width=3)
    for i, (_, _, col, t, s) in enumerate(spheres):
        ly = 740 + i * 72
        d.rounded_rectangle([140, ly, 890, ly + 56], radius=10, fill=(*C_OBSIDIAN, 245), outline=(*col, 200), width=2)
        d.text((160, ly + 14), t, fill=(*col, 255), font=font(20, bold=True))
        d.text((385, ly + 16), s, fill=(*C_WHITE, 255), font=font(16))

    c = card(c, 970, 195, 850, 790, C_MAGMA)
    d = ImageDraw.Draw(c)
    d.text((1010, 230), "PROYECCION GMV A 3 ANOS", fill=(*C_WHITE, 255), font=font(22, bold=True))
    yrs = [
        ("ANO 1", 0.22, "$4.2M", "85 Agencias", C_STEEL),
        ("ANO 2", 0.54, "$16.5M", "240 Agencias", C_ORANGE),
        ("ANO 3", 1.0, "$48.0M", "450+ Agencias", C_MAGMA),
    ]
    by0, mh = 840, 440
    for i, (yl, r, gmv, ag, col) in enumerate(yrs):
        bx = 1055 + i * 250
        bh = int(mh * r)
        d.rounded_rectangle([bx, by0 - bh, bx + 180, by0], radius=12, fill=(*col, 240))
        d.text((bx + 20, by0 - bh - 45), gmv, fill=(*C_WHITE, 255), font=font(30, bold=True))
        d.text((bx + 42, by0 + 18), yl, fill=(*C_WHITE, 255), font=font(20, bold=True))
        d.text((bx + 22, by0 + 48), ag, fill=(*C_STEEL, 255), font=font(16))

    p8 = os.path.join(BG_DIR, "s8.png")
    c.save(p8)
    canvases.append(p8)

    # --- SLIDE 9: THE ASK ($500K SEED) ---
    c = make_base("assets/images/neuromarketing/hero_tech_andes.jpg", 0.22)
    c = card(c, 100, 195, 860, 790, C_ORANGE)
    d = ImageDraw.Draw(c)
    d.text((140, 230), "ASIGNACION DE CAPITAL · $500K SEED", fill=(*C_WHITE, 255), font=font(22, bold=True))
    segs = [
        ("40% Edge AI Hardware ($200K)", 40, C_ORANGE),
        ("30% Core AI & MCP ($150K)", 30, C_MAGMA),
        ("20% Expansion Comercial ($100K)", 20, C_STEEL),
        ("10% DAO & Legal ($50K)", 10, C_WHITE),
    ]
    cx, cy, ro, ri = 320, 495, 165, 92
    ang = -90
    for _, pct, col in segs:
        sw = (pct / 100.0) * 360.0
        d.pieslice([cx - ro, cy - ro, cx + ro, cy + ro], start=ang, end=ang + sw - 2, fill=(*col, 255))
        ang += sw
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=(*C_CARD, 255))
    d.text((cx - 58, cy - 28), "$500K", fill=(*C_WHITE, 255), font=font(40, bold=True))
    d.text((cx - 42, cy + 20), "SEED USD", fill=(*C_ORANGE, 255), font=font(15, bold=True))

    for i, (lbl, _, col) in enumerate(segs):
        ly = 700 + i * 65
        d.rounded_rectangle([140, ly, 920, ly + 52], radius=10, fill=(*C_OBSIDIAN, 245), outline=(*col, 200), width=2)
        d.text((165, ly + 14), lbl, fill=(*C_WHITE, 255), font=font(18, bold=True))

    c = card(c, 1000, 195, 820, 790, C_MAGMA)
    p9 = os.path.join(BG_DIR, "s9.png")
    c.save(p9)
    canvases.append(p9)

    # --- SLIDE 10: ROADMAP, TEAM & CONTACT ---
    c = make_base("assets/images/neuromarketing/ayni_network.jpg", 0.30)
    for i, col in enumerate([C_ORANGE, C_MAGMA, C_ORANGE, C_MAGMA]):
        c = card(c, 100 + i * 438, 195, 412, 320, col)
    c = card(c, 100, 550, 840, 435, C_ORANGE, photo="assets/images/neuromarketing/agency_owner.jpg", photo_h=145)
    c = card(c, 980, 550, 840, 435, C_MAGMA, photo="assets/images/neuromarketing/hero_tech_andes.jpg", photo_h=145)
    p10 = os.path.join(BG_DIR, "s10.png")
    c.save(p10)
    canvases.append(p10)

    return canvases


def put(slide, x, y, w, h, lines):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (txt, sz, bold, col, sp) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = txt
        p.font.size = Pt(sz)
        p.font.bold = bold
        p.font.color.rgb = col
        p.space_after = Pt(sp)
    return tb


def generate():
    canvases = build_slides()
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    titles = [
        ("", ""),
        ("01 · EL PROBLEMA", "El Turismo Extremo Pierde 30% de Margen y Opera a Ciegas"),
        ("02 · LA SOLUCION", "Tres Motores Integrados: B2C + B2B + GEOINT 3D"),
        ("03 · TRACCION 2026", "Construido en Produccion desde el 06 de Enero"),
        ("04 · GEOINT 3D", "Control Territorial y Seguridad en Tiempo Real"),
        ("05 · ARQUITECTURA", "Stack Soberano y Grafo Neuronal de 4,481 Nodos"),
        ("06 · UNIT ECONOMICS", "Costo Marginal Cero y Margen Bruto >82%"),
        ("07 · MERCADO", "De Cusco a un Mercado Andino de $2.4B USD"),
        ("08 · LA RONDA", "Semilla $500,000 USD · Runway 18 Meses"),
        ("09 · ROADMAP & CONTACTO", "Hoja de Ruta 2026-2027 y Cierre de Inversion"),
    ]

    logo = "assets/images/lifextreme_logo_icon.png"
    for idx, bg in enumerate(canvases):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.shapes.add_picture(bg, 0, 0, Inches(13.333), Inches(7.5))

        if idx == 0:
            if os.path.exists(logo):
                slide.shapes.add_picture(logo, Inches(0.72), Inches(0.65), Inches(0.95), Inches(0.95))
            put(slide, 0.72, 1.78, 6.2, 3.0, [
                ("LIFEXTREME AI", 44, True, RGB_WHITE, 6),
                ("OUTDOOR EXPERIENCE & SOVEREIGN AI", 15, True, RGB_ORANGE, 12),
                ("Geointeligencia 3D y Cerebro Vectorial de +336K registros para dominar el turismo de aventura en LATAM.", 13, False, RGB_STEEL, 16),
                ("SEED ROUND: $500,000 USD", 15, True, RGB_MAGMA, 6),
                ("www.lifextreme.com.pe  ·  contacto@lifextreme.com.pe  ·  +51 958 050 928", 10.5, True, RGB_STEEL, 0),
            ])
        else:
            if os.path.exists(logo):
                slide.shapes.add_picture(logo, Inches(12.05), Inches(0.26), Inches(0.55), Inches(0.55))
            cat, tit = titles[idx]
            put(slide, 0.7, 0.22, 11.1, 0.85, [
                (cat, 10, True, RGB_ORANGE, 2),
                (tit, 22, True, RGB_WHITE, 0),
            ])
            put(slide, 0.7, 7.16, 11.9, 0.28, [
                (f"LIFEXTREME  ·  www.lifextreme.com.pe  ·  contacto@lifextreme.com.pe  ·  +51 958 050 928          {idx+1:02d} / 10", 8.5, True, RGB_STEEL, 0)
            ])

            # Slide-specific concise visual text
            if idx == 1:
                for i, (t, d, col) in enumerate([
                    ("30% COMISIONES OTAS", "Viator y Booking drenan la rentabilidad local.", RGB_MAGMA),
                    ("47 NORMAS DISPERSAS", "Riesgo legal y multas constantes en agencias.", RGB_ORANGE),
                    ("APAGON EN ALTURA", "Sin 4G sobre 4,200m ni alertas medicas HAPE.", RGB_MAGMA),
                ]):
                    put(slide, 7.05, 1.55 + i * 1.88, 5.2, 1.4, [
                        (t, 16, True, col, 4),
                        (d, 13, False, RGB_WHITE, 0),
                    ])
            elif idx == 2:
                for i, (x, t, d, col) in enumerate([
                    (0.88, "MAX AI (B2C)", "Concierge de altitud.\nPrevencion HAPE y reserva directa.", RGB_ORANGE),
                    (4.94, "CORE (B2B)", "Copiloto legal MINCETUR.\nCero alucinaciones con Pydantic-AI.", RGB_MAGMA),
                    (9.00, "GEOINT 3D", "Topografia Three.js + Cesium.\nTrenes y clima en tiempo real.", RGB_ORANGE),
                ]):
                    put(slide, x, 3.65, 3.45, 2.8, [
                        (t, 18, True, col, 10),
                        (d, 13, False, RGB_WHITE, 0),
                    ])
            elif idx == 3:
                for i, (val, lbl, col) in enumerate([
                    ("336,869+", "VECTORES QDRANT", RGB_ORANGE),
                    ("396", "COMMITS EN PROD", RGB_MAGMA),
                    ("251", "RUTAS VERIFICADAS", RGB_ORANGE),
                    ("164", "PARQUES EXTREMOS", RGB_MAGMA),
                ]):
                    put(slide, 0.85 + i * 3.05, 1.55, 2.6, 1.6, [
                        (val, 32, True, col, 4),
                        (lbl, 12, True, RGB_WHITE, 0),
                    ])
            elif idx == 4:
                put(slide, 9.1, 3.9, 3.4, 2.6, [
                    ("CONTROL EN VIVO", 17, True, RGB_MAGMA, 8),
                    ("• Rutas DEM 3D en Salkantay y Ausangate.\n• Alertas SUTRAN e IGP via MCP.\n\nDemo:\nlifextreme.com.pe/geoint.html", 12, False, RGB_WHITE, 0),
                ])
            elif idx == 5:
                put(slide, 8.25, 3.9, 4.2, 2.8, [
                    ("CEREBRO NEURONAL 3D", 17, True, RGB_MAGMA, 8),
                    ("4,481 Nodos y 19,114 Sinapsis conectando Qdrant con agentes MAX.\n\nVer en vivo:\nlifextreme.com.pe/neural-brain-3d.html", 12.5, False, RGB_WHITE, 0),
                ])
            elif idx == 6:
                put(slide, 8.4, 1.65, 4.0, 4.9, [
                    ("3 MOTORES DE INGRESO", 17, True, RGB_MAGMA, 12),
                    ("10% - 12% Split-Pay B2C", 15, True, RGB_ORANGE, 4),
                    ("30% reserva / 30% check-in / 40% cumbre.", 11.5, False, RGB_STEEL, 14),
                    ("SaaS B2B ($49 - $499/mes)", 15, True, RGB_ORANGE, 4),
                    ("Compliance MINCETUR + WhatsApp AI.", 11.5, False, RGB_STEEL, 14),
                    ("MARGEN BRUTO > 82%", 18, True, RGB_WHITE, 4),
                    ("Inferencia local a $0.00/token.", 11.5, False, RGB_ORANGE, 0),
                ])
            elif idx == 8:
                put(slide, 7.15, 1.65, 5.3, 4.9, [
                    ("HITOS DEL CAPITAL (18 MESES)", 17, True, RGB_MAGMA, 12),
                    ("MES 3 · Hardware Edge AI Cusco", 14, True, RGB_ORANGE, 3),
                    ("Cluster Memoria Unificada operando a $0/token.", 11.5, False, RGB_STEEL, 12),
                    ("MES 6 · $25,000 USD MRR", 14, True, RGB_ORANGE, 3),
                    ("60 agencias B2B y +1,500 reservas/mes.", 11.5, False, RGB_STEEL, 12),
                    ("MES 12 · Expansion + DAO Ayni", 14, True, RGB_ORANGE, 3),
                    ("Nodos en Huaraz, Colca y Layer 2.", 11.5, False, RGB_STEEL, 12),
                    ("MES 18 · Breakeven & Serie A", 14, True, RGB_MAGMA, 3),
                    ("+300 agencias activas en la region.", 11.5, False, RGB_WHITE, 0),
                ])
            elif idx == 9:
                for i, (q, d, col) in enumerate([
                    ("Q1-Q2 2026", "336K Vectores\nGEOINT 3D\nGrafo 4.4K Nodos", RGB_ORANGE),
                    ("Q3 2026", "Cluster Cusco\nCosto $0 Token\n60 Agencias", RGB_MAGMA),
                    ("Q4 2026", "App Offline\nHuaraz & Colca\n$50K MRR", RGB_ORANGE),
                    ("2027", "1M Vectores\nDAO Ayni L2\nSerie A Ready", RGB_MAGMA),
                ]):
                    put(slide, 0.88 + i * 3.04, 1.55, 2.6, 1.9, [
                        (q, 16, True, col, 6),
                        (d, 12, False, RGB_WHITE, 0),
                    ])
                put(slide, 0.9, 4.95, 5.4, 1.8, [
                    ("LIDERAZGO & VALIDACION", 15, True, RGB_ORANGE, 6),
                    ("Arquitecto Lider IA residente en Cusco.\nValidacion tecnica UNSAAC / UNI y red AGOTUR.", 12, False, RGB_WHITE, 0),
                ])
                put(slide, 7.0, 4.95, 5.4, 1.8, [
                    ("CONTACTO DE INVERSION", 15, True, RGB_MAGMA, 6),
                    ("www.lifextreme.com.pe\ncontacto@lifextreme.com.pe  ·  +51 958 050 928\nneural-brain-3d.html  ·  geoint.html", 12, True, RGB_WHITE, 0),
                ])

    out = "Lifextreme_Investor_Pitch_Deck_2026.pptx"
    prs.save(out)
    print(f"Created logo-branded minimal deck: {out}")


if __name__ == "__main__":
    generate()
