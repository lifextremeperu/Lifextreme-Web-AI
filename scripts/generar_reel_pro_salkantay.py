"""
Producción Cinematográfica Vertical (9:16) - Salkantay Trek to Machu Picchu
----------------------------------------------------------------------------
Mezcla de 3 capas de audio (Narración enérgica + Sonidos de Naturaleza + Música Épica)
+ Cortes dinámicos Full HD sin barras negras + Estética minimalista tipo NatGeo/RedBull.
"""

import asyncio
import os
import shutil
import edge_tts
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    VideoClip,
    CompositeAudioClip,
    concatenate_videoclips,
)

WORKSPACE = r"c:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI"
REF_HD = r"D:\Proyectos\.tmp\ref_salkantay_hd.mp4"
BROLL_SALKANTAY = r"D:\Proyectos\.tmp\tiktok_broll\clip_salkantay.mp4"
HERO_VID = os.path.join(WORKSPACE, "assets", "videos", "hero_peru_adventure.mp4")

NATURE_SFX = r"D:\Proyectos\.tmp\nature_sfx.m4a"
ADVENTURE_MUSIC = r"D:\Proyectos\.tmp\adventure_music.m4a"

OUT_DIR = r"D:\Proyectos\ShortGPT\videos"
TMP_DIR = r"D:\Proyectos\.tmp\reel_pro_salkantay"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

VOICE = "es-PE-AlexNeural"
W, H = 720, 1280

SCENES = [
    {
        "narration": "¿Listo para conquistar una de las rutas más épicas de los Andes?",
        "badge": "📍 CUSCO · PERÚ",
        "subtitle": "CONQUISTA EL SALKANTAY",
        "video": REF_HD,
        "start": 10.0,
        "remove_letterbox": True,
    },
    {
        "narration": "Día uno: cruzamos Soraypampa frente a glaciares gigantes hasta la Laguna Humantay.",
        "badge": "📍 SORAYPAMPA · 3,900 msnm",
        "subtitle": "Glaciares y Laguna Humantay",
        "video": BROLL_SALKANTAY,
        "start": 0.0,
        "remove_letterbox": False,
    },
    {
        "narration": "Dormimos en domos geodésicos bajo el cielo estrellado más limpio del planeta.",
        "badge": "📍 SKY CAMP · DOMOS GLAMPING",
        "subtitle": "Noche en Domos bajo las estrellas",
        "video": REF_HD,
        "start": 88.5,
        "remove_letterbox": True,
    },
    {
        "narration": "Día dos: desafiamos el Paso Salkantay a cuatro mil seiscientos treinta metros de altura.",
        "badge": "📍 PASO SALKANTAY · 4,630 msnm",
        "subtitle": "El punto más alto de la ruta",
        "video": REF_HD,
        "start": 144.0,
        "remove_letterbox": True,
    },
    {
        "narration": "Donde el esfuerzo se transforma en pura gloria junto al Apu nevado.",
        "badge": "📍 CUMBRE · 4,630 msnm",
        "subtitle": "Pura energía en los Andes",
        "video": REF_HD,
        "start": 151.0,
        "remove_letterbox": True,
    },
    {
        "narration": "Descendemos a la ceja de selva entre cascadas, bosque nublado y café orgánico.",
        "badge": "📍 VALLE AMAZÓNICO · 2,000 msnm",
        "subtitle": "De la nieve a la selva alta",
        "video": REF_HD,
        "start": 210.0,
        "remove_letterbox": True,
    },
    {
        "narration": "Caminamos por senderos incas hasta Llactapata con vistas secretas a Machu Picchu.",
        "badge": "📍 LLACTAPATA · 2,700 msnm",
        "subtitle": "Vistas secretas a Machu Picchu",
        "video": REF_HD,
        "start": 273.0,
        "remove_letterbox": True,
    },
    {
        "narration": "Vive la aventura con guías certificados y equipo incluido en lifextreme punto com punto pe.",
        "badge": "🏔️ LIFEXTREME PERÚ",
        "subtitle": "Reserva hoy · www.lifextreme.com.pe",
        "video": HERO_VID,
        "start": 2.0,
        "remove_letterbox": False,
    },
]


async def generate_tts(text, out_audio):
    communicate = edge_tts.Communicate(text, VOICE, rate="+8%", pitch="+2Hz")
    await communicate.save(out_audio)


def create_pro_overlay(badge, subtitle, is_cta=False):
    """Overlay cinematográfico limpio estilo NatGeo / RedBull sin cajas toscas."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Degradado cinematográfico sutil arriba y abajo para legibilidad natural
    for y in range(170):
        alpha = int(145 * (1 - y / 170))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    for y in range(H - 310, H):
        alpha = int(185 * ((y - (H - 310)) / 310))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))

    font_paths = [
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
    ]
    font_path = next((p for p in font_paths if os.path.exists(p)), None)
    font_badge = ImageFont.truetype(font_path, 22) if font_path else ImageFont.load_default()
    font_sub = ImageFont.truetype(font_path, 38) if font_path else ImageFont.load_default()
    font_wm = ImageFont.truetype(font_path, 18) if font_path else ImageFont.load_default()

    # Badge minimalista translúcido arriba a la izquierda
    bbox = draw.textbbox((0, 0), badge, font=font_badge)
    bw_text = bbox[2] - bbox[0]
    pill_w = bw_text + 36
    pill_h = 40
    px, py = 36, 56
    draw.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=20, fill=(10, 15, 30, 175), outline=(255, 142, 29, 220), width=2)
    draw.text((px + pill_w // 2, py + pill_h // 2), badge, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")

    # Marca de agua sutil arriba a la derecha
    draw.text((W - 36, 76), "LIFEXTREME.COM.PE", font=font_wm, fill=(255, 255, 255, 180), anchor="rm")

    # Subtítulo cinematográfico limpio (solo texto con sombra fuerte + línea acento)
    ty = H - 180
    # Sombra suave múltiple para legibilidad cristalina
    for dx, dy in [(-2, 2), (2, 2), (0, 3), (3, 3)]:
        draw.text((W // 2 + dx, ty + dy), subtitle, font=font_sub, fill=(0, 0, 0, 210), anchor="mm")

    text_color = (255, 195, 65, 255) if is_cta else (255, 255, 255, 255)
    draw.text((W // 2, ty), subtitle, font=font_sub, fill=text_color, anchor="mm")

    # Línea de acento sutil debajo del subtítulo
    draw.rounded_rectangle([W // 2 - 45, ty + 32, W // 2 + 45, ty + 36], radius=2, fill=(255, 142, 29, 240))

    return img


def process_vertical_frame(frame_np, remove_letterbox=False):
    """Elimina barras negras si existen, recorta 9:16 y aplica gradación cinematográfica sutil."""
    if remove_letterbox:
        # El video de referencia tiene contenido activo entre y=98 y y=982 (de 1080)
        h_src = frame_np.shape[0]
        top_cut = int(h_src * 0.095)
        bot_cut = int(h_src * 0.905)
        frame_np = frame_np[top_cut:bot_cut, :, :]

    im = Image.fromarray(frame_np)
    target_ratio = W / H
    src_ratio = im.width / im.height
    if src_ratio > target_ratio:
        new_w = int(im.height * target_ratio)
        left = (im.width - new_w) // 2
        im = im.crop((left, 0, left + new_w, im.height))
    else:
        new_h = int(im.width / target_ratio)
        top = (im.height - new_h) // 2
        im = im.crop((0, top, im.width, top + new_h))

    im = im.resize((W, H), Image.Resampling.BILINEAR)
    # Ligero boost de contraste y color para look cinematográfico
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    return im


async def build_pro_reel():
    print("[1/5] Generando narración energética en español peruano...")
    video_clips = []
    voice_tracks = []
    opened_sources = {}
    current_t = 0.0

    for i, sc in enumerate(SCENES):
        audio_file = os.path.join(TMP_DIR, f"narration_{i}.mp3")
        await generate_tts(sc["narration"], audio_file)
        a_clip = AudioFileClip(audio_file)
        dur = a_clip.duration + 0.25

        # Posicionar narración en la línea de tiempo
        voice_tracks.append(a_clip.with_start(current_t))

        src_path = sc["video"]
        if src_path not in opened_sources:
            opened_sources[src_path] = VideoFileClip(src_path).without_audio()
        src_clip = opened_sources[src_path]

        start_t = min(sc["start"], max(0.0, src_clip.duration - 1.5))
        overlay_pil = create_pro_overlay(sc["badge"], sc["subtitle"], is_cta=(i == len(SCENES) - 1))

        print(f"   Escena {i+1}: {dur:.2f}s | {sc['badge']} | {os.path.basename(src_path)} @ {start_t}s")

        def make_frame_fn(clip=src_clip, st=start_t, ov=overlay_pil, rlb=sc["remove_letterbox"]):
            clip_dur = clip.duration

            def mf(t):
                local_t = (st + t) % max(0.1, clip_dur - 0.1)
                raw = clip.get_frame(local_t)
                vert = process_vertical_frame(raw, remove_letterbox=rlb).convert("RGBA")
                vert.alpha_composite(ov)
                return np.array(vert.convert("RGB"))

            return mf

        v_clip = VideoClip(make_frame_fn(), duration=dur)
        video_clips.append(v_clip)
        current_t += dur

    total_duration = current_t
    print(f"[2/5] Duración total del Reel: {total_duration:.2f}s")

    print("[3/5] Mezclando 3 capas de audio (Voz 100% + Naturaleza 32% + Música Épica 18%)...")
    # Capa 2: Sonidos de Naturaleza (viento, río, aves)
    nature_clip = AudioFileClip(NATURE_SFX).subclipped(0, min(total_duration, AudioFileClip(NATURE_SFX).duration))
    nature_clip = nature_clip.with_volume_scaled(0.32)

    # Capa 3: Música Épica de Aventura
    music_raw = AudioFileClip(ADVENTURE_MUSIC)
    music_clip = music_raw.subclipped(0, min(total_duration, music_raw.duration)).with_volume_scaled(0.18)

    mixed_audio = CompositeAudioClip(voice_tracks + [nature_clip, music_clip]).with_duration(total_duration)

    print("[4/5] Ensamblando video final HD...")
    final_video = concatenate_videoclips(video_clips, method="chain").with_audio(mixed_audio)

    out_path = os.path.join(OUT_DIR, "salkantay_aventura_pro.mp4")
    workspace_copy = os.path.join(WORKSPACE, "reportes_b2b", "salkantay_aventura_pro.mp4")

    print(f"[5/5] Exportando Reel Pro -> {out_path}...")
    final_video.write_videofile(
        out_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=2,
        logger=None,
    )

    for s in opened_sources.values():
        s.close()

    shutil.copy2(out_path, workspace_copy)
    print(f"[OK] ¡Reel Profesional listo en {out_path}!")


if __name__ == "__main__":
    asyncio.run(build_pro_reel())
