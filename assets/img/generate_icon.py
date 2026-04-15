from PIL import Image, ImageDraw, ImageFont
import math
import os

# ---- Config ----
SIZE = 1024  # Facebook requires minimum 1024x1024
OUTPUT = os.path.join(os.path.dirname(__file__), "lifextreme_app_icon.png")

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# ---- Background Circle with dark gradient ----
cx, cy, r = SIZE // 2, SIZE // 2, SIZE // 2 - 2
# Draw filled black circle
draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 10, 15, 255))

# ---- Inner orange ring ----
ring_w = 18
draw.ellipse(
    [cx - r + ring_w, cy - r + ring_w, cx + r - ring_w, cy + r - ring_w],
    outline=(255, 110, 0, 255),
    width=ring_w,
)

# ---- Mountain silhouette ----
# Main peak (center)
peak_x, peak_y = cx, int(cy * 0.52)
left_base = (cx - 290, int(cy * 1.35))
right_base = (cx + 290, int(cy * 1.35))
# Left shoulder
left_shoulder = (cx - 120, int(cy * 0.78))
right_shoulder = (cx + 120, int(cy * 0.78))

mountain_poly = [
    left_base,
    left_shoulder,
    (cx - 45, int(cy * 0.70)),
    (peak_x, peak_y),  # main peak
    (cx + 45, int(cy * 0.70)),
    right_shoulder,
    right_base,
]
draw.polygon(mountain_poly, fill=(255, 110, 0, 255))

# ---- Snow cap ----
snow = [
    (peak_x, peak_y),
    (cx - 35, int(cy * 0.68)),
    (cx - 15, int(cy * 0.67)),
    (cx, int(cy * 0.63)),
    (cx + 15, int(cy * 0.67)),
    (cx + 35, int(cy * 0.68)),
]
draw.polygon(snow, fill=(240, 240, 250, 255))

# ---- "LX" Text ----
text_y = int(cy * 1.38)
try:
    font_large = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 160)
    font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 45)
except:
    font_large = ImageFont.load_default()
    font_small = font_large

# LX letters
lx_text = "LX"
bbox = draw.textbbox((0, 0), lx_text, font=font_large)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
draw.text((cx - tw // 2, text_y - th // 2), lx_text, font=font_large, fill=(255, 255, 255, 255))

# Sub-label
sub = "LIFEXTREME"
bbox2 = draw.textbbox((0, 0), sub, font=font_small)
sw = bbox2[2] - bbox2[0]
draw.text((cx - sw // 2, text_y + th // 2 + 10), sub, font=font_small, fill=(255, 110, 0, 230))

# ---- Save ----
img.save(OUTPUT, "PNG")
print(f"Icon saved: {OUTPUT} ({SIZE}x{SIZE}px)")
