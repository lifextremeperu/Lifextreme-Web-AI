import re
import os

UPDATES = {
    "The North Face Mountain 25 (4 Estaciones)": {
        "img": "assets/images/equipos/equipo_mountain_25.jpg",
        "views360": [
            "assets/images/equipos/equipo_mountain_25.jpg",
            "assets/images/equipos/equipo_msr_hubba.jpg",
            "assets/images/equipos/equipo_ferrino_svalbard.jpg",
            "assets/images/equipos/equipo_marmot_col.jpg"
        ]
    },
    "MSR Hubba Hubba NX 2P Ultraligera": {
        "img": "assets/images/equipos/equipo_msr_hubba.jpg",
        "views360": [
            "assets/images/equipos/equipo_msr_hubba.jpg",
            "assets/images/equipos/equipo_mountain_25.jpg",
            "assets/images/equipos/equipo_ferrino_svalbard.jpg",
            "assets/images/equipos/equipo_thermarest_neoair.jpg"
        ]
    },
    "Ferrino Svalbard 3P Expedición": {
        "img": "assets/images/equipos/equipo_ferrino_svalbard.jpg",
        "views360": [
            "assets/images/equipos/equipo_ferrino_svalbard.jpg",
            "assets/images/equipos/equipo_mountain_25.jpg",
            "assets/images/equipos/equipo_msr_hubba.jpg",
            "assets/images/equipos/equipo_ferrino_nightec.jpg"
        ]
    },
    "Bolsa de Dormir Marmot Col -29°C (800FP)": {
        "img": "assets/images/equipos/equipo_marmot_col.jpg",
        "views360": [
            "assets/images/equipos/equipo_marmot_col.jpg",
            "assets/images/equipos/equipo_ferrino_nightec.jpg",
            "assets/images/equipos/equipo_thermarest_neoair.jpg",
            "assets/images/equipos/equipo_mountain_25.jpg"
        ]
    },
    "Sleeping Ferrino Nightec 800 -12°C": {
        "img": "assets/images/equipos/equipo_ferrino_nightec.jpg",
        "views360": [
            "assets/images/equipos/equipo_ferrino_nightec.jpg",
            "assets/images/equipos/equipo_marmot_col.jpg",
            "assets/images/equipos/equipo_thermarest_neoair.jpg",
            "assets/images/equipos/equipo_ferrino_svalbard.jpg"
        ]
    },
    "Matra Therm-a-Rest NeoAir XTherm NXT": {
        "img": "assets/images/equipos/equipo_thermarest_neoair.jpg",
        "views360": [
            "assets/images/equipos/equipo_thermarest_neoair.jpg",
            "assets/images/equipos/equipo_ferrino_nightec.jpg",
            "assets/images/equipos/equipo_marmot_col.jpg",
            "assets/images/equipos/equipo_mountain_25.jpg"
        ]
    },
    "Casaca Arc'teryx Alpha SV Gore-Tex Pro": {
        "img": "assets/images/equipos/equipo_arcteryx_alpha.jpg",
        "views360": [
            "assets/images/equipos/equipo_arcteryx_alpha.jpg",
            "assets/images/equipos/equipo_tnf_summit_l3.jpg",
            "assets/images/equipos/equipo_patagonia_triolet.jpg",
            "assets/images/equipos/equipo_petzl_quark.jpg"
        ]
    },
    "Parka Plumas The North Face Summit L3 (800FP)": {
        "img": "assets/images/equipos/equipo_tnf_summit_l3.jpg",
        "views360": [
            "assets/images/equipos/equipo_tnf_summit_l3.jpg",
            "assets/images/equipos/equipo_arcteryx_alpha.jpg",
            "assets/images/equipos/equipo_patagonia_triolet.jpg",
            "assets/images/equipos/equipo_mountain_25.jpg"
        ]
    },
    "Pantalón Hardshell Patagonia Triolet Gore-Tex 3L": {
        "img": "assets/images/equipos/equipo_patagonia_triolet.jpg",
        "views360": [
            "assets/images/equipos/equipo_patagonia_triolet.jpg",
            "assets/images/equipos/equipo_arcteryx_alpha.jpg",
            "assets/images/equipos/equipo_tnf_summit_l3.jpg",
            "assets/images/equipos/equipo_grivel_g12.jpg"
        ]
    },
    "Piolets Técnicos Petzl Quark (Par Hielo/Mixto)": {
        "img": "assets/images/equipos/equipo_petzl_quark.jpg",
        "views360": [
            "assets/images/equipos/equipo_petzl_quark.jpg",
            "assets/images/equipos/equipo_grivel_g12.jpg",
            "assets/images/equipos/equipo_petzl_sirocco.jpg",
            "assets/images/equipos/equipo_bd_solution.jpg"
        ]
    },
    "Crampones Semiautomáticos Grivel G12 New-Matic": {
        "img": "assets/images/equipos/equipo_grivel_g12.jpg",
        "views360": [
            "assets/images/equipos/equipo_grivel_g12.jpg",
            "assets/images/equipos/equipo_petzl_quark.jpg",
            "assets/images/equipos/equipo_petzl_sirocco.jpg",
            "assets/images/equipos/equipo_arcteryx_alpha.jpg"
        ]
    },
    "Casco de Escalada Petzl Sirocco Ultraligero": {
        "img": "assets/images/equipos/equipo_petzl_sirocco.jpg",
        "views360": [
            "assets/images/equipos/equipo_petzl_sirocco.jpg",
            "assets/images/equipos/equipo_bd_solution.jpg",
            "assets/images/equipos/equipo_petzl_quark.jpg",
            "assets/images/equipos/equipo_grivel_g12.jpg"
        ]
    },
    "Arnés Black Diamond Solution Guide": {
        "img": "assets/images/equipos/equipo_bd_solution.jpg",
        "views360": [
            "assets/images/equipos/equipo_bd_solution.jpg",
            "assets/images/equipos/equipo_petzl_sirocco.jpg",
            "assets/images/equipos/equipo_grivel_g12.jpg",
            "assets/images/equipos/equipo_petzl_quark.jpg"
        ]
    },
    "Osprey Aether 65 Pro Expedition": {
        "img": "assets/images/equipos/equipo_osprey_aether.jpg",
        "views360": [
            "assets/images/equipos/equipo_osprey_aether.jpg",
            "assets/images/equipos/equipo_bd_bastones.jpg",
            "assets/images/equipos/equipo_garmin_inreach.jpg",
            "assets/images/equipos/equipo_marmot_col.jpg"
        ]
    },
    "Bastones Black Diamond Trail Pro Shock (Par)": {
        "img": "assets/images/equipos/equipo_bd_bastones.jpg",
        "views360": [
            "assets/images/equipos/equipo_bd_bastones.jpg",
            "assets/images/equipos/equipo_osprey_aether.jpg",
            "assets/images/equipos/equipo_garmin_inreach.jpg",
            "assets/images/equipos/equipo_thermarest_neoair.jpg"
        ]
    },
    "GPS Satelital Garmin inReach Explorer+ SOS": {
        "img": "assets/images/equipos/equipo_garmin_inreach.jpg",
        "views360": [
            "assets/images/equipos/equipo_garmin_inreach.jpg",
            "assets/images/equipos/equipo_osprey_aether.jpg",
            "assets/images/equipos/equipo_bd_bastones.jpg",
            "assets/images/equipos/equipo_ferrino_svalbard.jpg"
        ]
    }
}

FILES = [
    "js/data.js",
    "js/data-en.js",
    "js/data-pt.js"
]

def update_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Look for equips definition
    equips_match = re.search(r'(const equips = \[)([\s\S]*?)(\n\];)', content)
    if not equips_match:
        print(f"  [ERROR] equips array not found in {filepath}")
        return

    prefix = equips_match.group(1)
    body = equips_match.group(2)
    suffix = equips_match.group(3)

    # Replace within body for each item
    for name, data in UPDATES.items():
        # Escape name for regex
        escaped_name = re.escape(name)
        # Find the object block starting with name: '...'
        pattern = rf"(name:\s*['\"]{escaped_name}['\"][\s\S]*?img:\s*['\"][^'\"]+['\"][\s\S]*?views360:\s*\[[\s\S]*?\])"
        
        def replacer(m):
            block = m.group(1)
            # Replace img: '...'
            block = re.sub(r"img:\s*['\"][^'\"]+['\"]", f"img: '{data['img']}'", block)
            # Replace views360: [...]
            views_str = "views360: [\n" + ",\n".join(f"            '{v}'" for v in data['views360']) + "\n        ]"
            block = re.sub(r"views360:\s*\[[\s\S]*?\]", views_str, block)
            return block

        new_body, count = re.subn(pattern, replacer, body, count=1)
        if count > 0:
            body = new_body
            print(f"  Updated: {name}")
        else:
            print(f"  [WARN] Not matched: {name}")

    new_content = content[:equips_match.start()] + prefix + body + suffix + content[equips_match.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  Saved {filepath} successfully.")

if __name__ == "__main__":
    for f in FILES:
        update_file(f)
