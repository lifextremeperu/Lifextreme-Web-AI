"""
Generador de Video TikTok / Reel Real (100% clips de video en movimiento)
Tema: Equipo esencial para el Salkantay Trek - Lifextreme Perú
"""

import asyncio
import os
import shutil
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import VideoFileClip, AudioFileClip, VideoClip, concatenate_videoclips

WORKSPACE = r"c:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI"
BROLL_DIR = r"D:\Proyectos\.tmp\tiktok_broll"
OUT_DIR = r"D:\Proyectos\ShortGPT\videos"
TMP_DIR = r"D:\Proyectos\.tmp\tiktok_salkantay"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

VOICE = "es-PE-AlexNeural"
W, H = 720, 1280  # Vertical TikTok / Reels HD

SCENES = [
    {
        "text": "¿Vas a hacer el Salkantay Trek? No empaques de más. Este es el equipo exacto que necesitas.",
        "caption": "❌ NO EMPAQUES DE MÁS\nEquipo exacto para SALKANTAY",
        "video": os.path.join(BROLL_DIR, "clip_salkantay.mp4"),
        "start": 0.0,
    },
    {
        "text": "Primero: botas de trekking impermeables ya amoldadas y tres capas de ropa térmica.",
        "caption": "1️⃣ Botas impermeables\n+ 3 Capas térmicas",
        "video": os.path.join(BROLL_DIR, "clip_gear.mp4"),
        "start": 0.0,
    },
    {
        "text": "Segundo: mochila de ataque de veinticinco litros. Tu duffle de siete kilos lo llevan nuestros arrieros.",
        "caption": "2️⃣ Mochila de 25 Litros\n(Duffle 7 kg por arriero)",
        "video": os.path.join(WORKSPACE, "assets", "videos", "hero_peru_adventure.mp4"),
        "start": 0.0,
    },
    {
        "text": "Tercero: gorro, guantes, linterna frontal y bloqueador para el abra a cuatro mil seiscientos metros.",
        "caption": "3️⃣ Gorro, guantes y frontal\nPara el Abra a 4,630 msnm",
        "video": os.path.join(BROLL_DIR, "clip_camp.mp4"),
        "start": 0.0,
    },
    {
        "text": "Reserva tu expedición con domos glamping y asesoría completa en lifextreme punto com punto pe.",
        "caption": "Domos Glamping + Guía UIAGM\n👉 www.lifextreme.com.pe",
        "video": os.path.join(WORKSPACE, "assets", "videos", "hero_peru_adventure.mp4"),
        "start": 4.0,
    },
]


async def generate_tts(text, out_audio):
    communicate = edge_tts.Communicate(text, VOICE, rate="+10%")
    await communicate.save(out_audio)


def create_tiktok_overlay(caption, step_idx):
    """Capa gráfica estilo TikTok: badge superior, subtítulos dinámicos y CTA abajo."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gradientes sutiles arriba/abajo para contraste
    for y in range(160):
        alpha = int(160 * (1 - y / 160))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    for y in range(H - 340, H):
        alpha = int(190 * ((y - (H - 340)) / 340))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))

    font_paths = [
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
    ]
    font_path = next((p for p in font_paths if os.path.exists(p)), None)
    font_brand = ImageFont.truetype(font_path, 24) if font_path else ImageFont.load_default()
    font_sub = ImageFont.truetype(font_path, 40) if font_path else ImageFont.load_default()
    font_cta = ImageFont.truetype(font_path, 24) if font_path else ImageFont.load_default()

    # Tag superior estilo TikTok
    pill_w, pill_h = 440, 48
    px = (W - pill_w) // 2
    py = 64
    draw.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=24, fill=(230, 57, 70, 235))
    draw.text((W // 2, py + pill_h // 2), "CHECKLIST SALKANTAY · LIFEXTREME", font=font_brand, fill=(255, 255, 255, 255), anchor="mm")

    # Caja de texto viral en tercio medio-bajo
    lines = caption.split("\n")
    line_heights = 52
    total_h = len(lines) * line_heights + 28
    box_w = 650
    bx = (W - box_w) // 2
    by = H - 360 - (total_h // 2)
    draw.rounded_rectangle([bx, by, bx + box_w, by + total_h], radius=16, fill=(10, 15, 28, 215), outline=(255, 165, 0, 235), width=3)

    for i, line in enumerate(lines):
        ty = by + 38 + i * line_heights
        draw.text((W // 2 + 2, ty + 2), line, font=font_sub, fill=(0, 0, 0, 230), anchor="mm")
        if step_idx == 0 and i == 0:
            col = (255, 110, 90, 255)
        elif step_idx == len(SCENES) - 1 and i == len(lines) - 1:
            col = (255, 215, 60, 255)
        else:
            col = (255, 255, 255, 255)
        draw.text((W // 2, ty), line, font=font_sub, fill=col, anchor="mm")

    # Footer badge
    cta_w, cta_h = 400, 44
    cx = (W - cta_w) // 2
    cy = H - 115
    draw.rounded_rectangle([cx, cy, cx + cta_w, cy + cta_h], radius=22, fill=(255, 255, 255, 235))
    draw.text((W // 2, cy + cta_h // 2), "www.lifextreme.com.pe", font=font_cta, fill=(15, 23, 42, 255), anchor="mm")

    return img


def crop_vertical_frame(frame_np):
    """Recorta y escala un frame horizontal/cuadrado a 720x1280 (9:16) centrado."""
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
    return im.resize((W, H), Image.Resampling.BILINEAR)


async def build_tiktok():
    print("[1/4] Generando locución rápida estilo TikTok...")
    final_clips = []
    opened_sources = []

    for i, sc in enumerate(SCENES):
        audio_file = os.path.join(TMP_DIR, f"tts_{i}.mp3")
        await generate_tts(sc["text"], audio_file)
        audio_clip = AudioFileClip(audio_file)
        dur = audio_clip.duration + 0.25

        src_clip = VideoFileClip(sc["video"]).without_audio()
        opened_sources.append(src_clip)

        start_t = min(sc["start"], max(0.0, src_clip.duration - 1.0))
        overlay_pil = create_tiktok_overlay(sc["caption"], i)

        print(f"   Escena {i+1}: {dur:.2f}s | {os.path.basename(sc['video'])}")

        def make_frame_fn(clip=src_clip, st=start_t, ov=overlay_pil):
            clip_dur = clip.duration

            def mf(t):
                # Loop suave si el clip fuente es más corto que el audio
                local_t = (st + t) % max(0.1, clip_dur - 0.05)
                raw = clip.get_frame(local_t)
                vert = crop_vertical_frame(raw).convert("RGBA")
                vert.alpha_composite(ov)
                return np.array(vert.convert("RGB"))

            return mf

        v_clip = VideoClip(make_frame_fn(), duration=dur).with_audio(audio_clip)
        final_clips.append(v_clip)

    print("[2/4] Uniendo clips en secuencia TikTok...")
    full_video = concatenate_videoclips(final_clips, method="chain")

    out_path = os.path.join(OUT_DIR, "tiktok_salkantay_equipo.mp4")
    workspace_copy = os.path.join(WORKSPACE, "reportes_b2b", "tiktok_salkantay_equipo.mp4")

    print(f"[3/4] Exportando TikTok MP4 (720x1280) -> {out_path}...")
    full_video.write_videofile(
        out_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=2,
        logger=None,
    )

    for s in opened_sources:
        s.close()

    shutil.copy2(out_path, workspace_copy)
    print(f"[4/4] ¡Listo! TikTok exportado en {out_path}")


if __name__ == "__main__":
    asyncio.run(build_tiktok())
