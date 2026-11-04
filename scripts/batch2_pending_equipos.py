"""
LIFEXTREME - GENERADOR AUTOMÁTICO DE EQUIPOS RESTANTES (BATCH 2)
Este script contiene las especificaciones y prompts exactos para generar
las 10 imágenes restantes de equipos técnicos en 4K HD en cuanto se restaure la cuota.
"""

PENDING_EQUIPMENT = [
    {
        "id": "ferrino_svalbard",
        "name": "Ferrino Svalbard 3P Expedición",
        "target_file": "assets/images/equipos/equipo_ferrino_svalbard.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD de la carpa de expedición Ferrino Svalbard 3P. "
            "Carpa técnica de 4 estaciones en color naranja andino brillante con detalles negros, faldones de nieve "
            "ajustables y vientos de tormenta de alta resistencia. Montada sobre nieve dura en la Cordillera Blanca al amanecer, "
            "con un piolet apoyado al costado. Estilo catálogo comercial Ferrino Outdoor / REI."
        )
    },
    {
        "id": "ferrino_nightec",
        "name": "Sleeping Ferrino Nightec 800 -12°C",
        "target_file": "assets/images/equipos/equipo_ferrino_nightec.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD del saco de dormir técnico Ferrino Nightec 800 (-12°C). "
            "Saco tipo momia en color azul marino y verde lima técnico con aislamiento de microfibra abullonada, "
            "cremallera YKK con solapa térmica. Extendido sobre una esterilla dentro de una carpa de montaña. Estilo catálogo Ferrino."
        )
    },
    {
        "id": "thermarest_neoair",
        "name": "Matra Therm-a-Rest NeoAir XTherm NXT",
        "target_file": "assets/images/equipos/equipo_thermarest_neoair.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD de la colchoneta aislante inflable ultraligera Therm-a-Rest NeoAir XTherm NXT. "
            "Diseño acolchado con cámaras horizontales reflectantes en color gris metálico / plata con válvula WingLock negra, "
            "colocada sobre el suelo de nieve dentro de una carpa alpina con una taza de titanio al lado. Estilo Therm-a-Rest / Cascade Designs."
        )
    },
    {
        "id": "tnf_summit_l3",
        "name": "Parka Plumas The North Face Summit L3 (800FP)",
        "target_file": "assets/images/equipos/equipo_tnf_summit_l3.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD de la chaqueta de plumas The North Face Summit L3 800FP. "
            "Chaqueta abullonada ultra-ligera en color azul cobalto y negro con micro-celdas de plumón de ganso, "
            "capucha ajustada y cremalleras selladas. Mostrada en un mirador andino con viento suave y picos nevados al fondo. Estilo Summit Series."
        )
    },
    {
        "id": "patagonia_triolet",
        "name": "Pantalón Hardshell Patagonia Triolet Gore-Tex 3L",
        "target_file": "assets/images/equipos/equipo_patagonia_triolet.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD del pantalón técnico Patagonia Triolet Gore-Tex 3L. "
            "Pantalón alpino impermeable en color negro grafito mate con cremalleras laterales completas WaterTight, "
            "polainas integradas y refuerzos en los tobillos para crampones. Apoyado sobre una roca andina con nieve escarchada. Estilo Patagonia Alpine."
        )
    },
    {
        "id": "petzl_sirocco",
        "name": "Casco de Escalada Petzl Sirocco Ultraligero",
        "target_file": "assets/images/equipos/equipo_petzl_sirocco.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD del casco de escalada Petzl Sirocco. "
            "Casco ultraligero de espuma EPP con corona de policarbonato en color naranja Petzl brillante y blanco, "
            "sistema de ventilación ergonómico y clips para linterna frontal. Apoyado sobre una roca de granito andino con cuerda de escalada al lado."
        )
    },
    {
        "id": "bd_solution_guide",
        "name": "Arnés Black Diamond Solution Guide",
        "target_file": "assets/images/equipos/equipo_bd_solution.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD del arnés de escalada Black Diamond Solution Guide. "
            "Arnés técnico ultra-resistente confeccionado con tejido Super Fabric en color negro y gris con costuras amarillas, "
            "4 anillos portamaterial contorneados y hebilla Speed Adjust de aluminio. Apoyado en una pared de roca caliza con mosquetones de seguridad."
        )
    },
    {
        "id": "osprey_aether_65",
        "name": "Osprey Aether 65 Pro Expedition",
        "target_file": "assets/images/equipos/equipo_osprey_aether.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD de la mochila de expedición Osprey Aether 65 Pro. "
            "Mochila técnica de trekking de 65L en color gris oscuro grafito y detalles azul glaciar / naranja, "
            "con soporte para piolets ToolLock, cinturón lumbar ergonómico y correas de compresión. Erguida sobre una roca en el mirador del Paso Salkantay."
        )
    },
    {
        "id": "bd_trail_pro_shock",
        "name": "Bastones Black Diamond Trail Pro Shock (Par)",
        "target_file": "assets/images/equipos/equipo_bd_bastones.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD del par de bastones de trekking Black Diamond Trail Pro Shock. "
            "Bastones telescópicos de aluminio anodizado color negro y rojo con empuñaduras ergonómicas de goma de doble densidad, "
            "mecanismo de bloqueo FlickLock Pro y amortiguador Control Shock. Clavados en el sendero del Camino Inca con ichu y montañas al fondo."
        )
    },
    {
        "id": "garmin_inreach",
        "name": "GPS Satelital Garmin inReach Explorer+ SOS",
        "target_file": "assets/images/equipos/equipo_garmin_inreach.jpg",
        "prompt": (
            "Fotografía de producto hiperrealista 4K HD del GPS satelital Garmin inReach Explorer+ SOS. "
            "Dispositivo resistente a impactos en color naranja de alta visibilidad y negro mate, pantalla a color con coordenadas UTM "
            "y mapa topográfico andino, antena Iridium superior y botón SOS protegido. Sostenido por una mano con guante técnico frente a nevados andinos."
        )
    }
]

if __name__ == "__main__":
    print(f"Total productos pendientes para el Batch 2: {len(PENDING_EQUIPMENT)}")
    for idx, eq in enumerate(PENDING_EQUIPMENT, 1):
        print(f"{idx:02d}. {eq['name']} -> {eq['target_file']}")
