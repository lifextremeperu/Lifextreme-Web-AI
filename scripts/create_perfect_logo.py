import os
from PIL import Image, ImageDraw

src_path = "assets/images/lifextreme_logo_pulso_montana_magma.jpg"
img = Image.open(src_path).convert("RGBA")

# Exact squircle coordinates
x1, y1, x2, y2 = 104, 104, 920, 920
cropped = img.crop((x1, y1, x2, y2))
cw, ch = cropped.size

# High-res anti-aliased rounded mask
scale = 4
mask_w, mask_h = cw * scale, ch * scale
mask = Image.new("L", (mask_w, mask_h), 0)
draw = ImageDraw.Draw(mask)
# Apple squircle / modern icon radius is ~ 22.5% of dimension
radius = int(mask_w * 0.225)
draw.rounded_rectangle([0, 0, mask_w, mask_h], radius=radius, fill=255)
mask = mask.resize((cw, ch), Image.Resampling.LANCZOS)

cropped.putalpha(mask)

# Save master PNG
cropped.save("assets/images/lifextreme_logo_icon.png", "PNG")
print("Saved assets/images/lifextreme_logo_icon.png")

sizes = {
    "assets/images/lifextreme_logo_icon_512.png": 512,
    "assets/images/lifextreme_logo_icon_192.png": 192,
    "assets/images/lifextreme_logo_icon_64.png": 64,
    "assets/images/lifextreme_logo_icon_32.png": 32,
    "logo.png": 512,
    "favicon.png": 64,
}

for path, sz in sizes.items():
    res = cropped.resize((sz, sz), Image.Resampling.LANCZOS)
    res.save(path, "PNG")
    print(f"Saved {path} ({sz}x{sz})")

# Favicon.ico
cropped.resize((32, 32), Image.Resampling.LANCZOS).save(
    "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)]
)
print("Saved favicon.ico")
