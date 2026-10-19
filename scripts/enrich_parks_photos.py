import re
import json

# Curated high-res, authentic adventure photography categorized by adventure activity
PHOTO_POOLS = {
    "Zipline": [
        "https://images.unsplash.com/photo-1527631746610-bca00a040d60?q=80&w=1000&auto=format&fit=crop", # Zipline canopy over canyon
        "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1506929562872-bb421503ef21?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=1000&auto=format&fit=crop"
    ],
    "Roca": [
        "https://images.unsplash.com/photo-1522163182402-834f871fd851?q=80&w=1000&auto=format&fit=crop", # Real rock climbing
        "https://images.unsplash.com/photo-1563299796-17596c35a7ac?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1502680390469-be75c86b636f?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1583623025817-d180a2221d0a?q=80&w=1000&auto=format&fit=crop"
    ],
    "Palestra": [
        "https://images.unsplash.com/photo-1564769662533-4f00a87b4056?q=80&w=1000&auto=format&fit=crop", # Climbing gym wall
        "https://images.unsplash.com/photo-1578768079052-aa76e520028b?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1522163182402-834f871fd851?q=80&w=1000&auto=format&fit=crop"
    ],
    "Rapel": [
        "https://images.unsplash.com/photo-1516245834210-c4c142787335?q=80&w=1000&auto=format&fit=crop", # Rappel waterfall
        "https://images.unsplash.com/photo-1501555088652-021faa106b9b?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?q=80&w=1000&auto=format&fit=crop"
    ],
    "Parque Aventura": [
        "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1533240332313-0db49b459ad6?q=80&w=1000&auto=format&fit=crop"
    ],
    "Bungee": [
        "https://images.unsplash.com/photo-1507034589631-9433cc6bc453?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?q=80&w=1000&auto=format&fit=crop"
    ],
    "Vía Ferrata": [
        "https://images.unsplash.com/photo-1551632811-561732d1e306?q=80&w=1000&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=1000&auto=format&fit=crop"
    ]
}

SPECIFIC_MAP = {
    "Playa Yacila (Paita)": "assets/img/destinos/yacila_escalada.jpg",
    "Canchaque (Villa Palambla)": "assets/img/destinos/canchaque_zipline.jpg",
    "Aventura Park Canchaque": "assets/img/destinos/canchaque_zipline.jpg",
    "Máncora": "assets/img/destinos/mancora_canopy.jpg",
    "Mancora": "assets/img/destinos/mancora_canopy.jpg",
    "Circuito Rapel Quebrada Seca (Máncora)": "assets/img/destinos/mancora_canopy.jpg",
    "Point Aventura (Chiclayo)": "assets/img/destinos/chiclayo_palestra.jpg",
    "Trujillo Bouldering": "assets/img/destinos/trujillo_bouldering.jpg",
    "Sector Pachar": "assets/img/destinos/sector_pachar.jpg",
    "Sector Pumahuanca": "assets/img/destinos/sector_pumahuanca.jpg",
    "Templo de la Luna": "assets/img/destinos/templo_monos.jpg",
    "Templo de los Monos": "assets/img/destinos/templo_monos.jpg",
    "Zipline Racchi": "assets/img/destinos/zipline_racchi.jpg",
    "Action Valley": "https://images.unsplash.com/photo-1507034589631-9433cc6bc453?q=80&w=1000&auto=format&fit=crop"
}

files = ['js/data.js', 'js/data-en.js', 'js/data-pt.js']

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search for the parks array definition
    # Pattern: match each park block
    def replace_park_photo(match):
        block = match.group(0)
        # extract name and tipo
        name_m = re.search(r'"nombre_infraestructura":\s*"([^"]+)"', block)
        tipo_m = re.search(r'"tipo":\s*"([^"]+)"', block)
        name = name_m.group(1) if name_m else ""
        tipo = tipo_m.group(1) if tipo_m else "Zipline"

        new_photo = None
        for key, path in SPECIFIC_MAP.items():
            if key.lower() in name.lower():
                new_photo = path
                break
        
        if not new_photo:
            pool = PHOTO_POOLS.get(tipo, PHOTO_POOLS["Zipline"])
            # hash name to pick deterministic varied photo
            idx = sum(ord(c) for c in name) % len(pool)
            new_photo = pool[idx]

        # replace url_foto in this block
        block = re.sub(r'"url_foto":\s*"[^"]+"', f'"url_foto": "{new_photo}"', block)
        return block

    pattern = r'\{\s*"id":\s*"INF-[^}]+?\}'
    updated_content = re.sub(pattern, replace_park_photo, content)

    if updated_content != content:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Updated photos in {fp}")
    else:
        print(f"No photo changes in {fp}")
