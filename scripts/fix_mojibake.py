import re

files = ['js/data.js', 'js/data-en.js', 'js/data-pt.js']

replacements = [
    ('MÃ¡ncora', 'Máncora'),
    ('ApurÃ­mac', 'Apurímac'),
    ('ApurÃ\xadmac', 'Apurímac'),
    ('Ã\x81ncash', 'Áncash'),
    ('Ã ncash', 'Áncash'),
    ('JunÃ­n', 'Junín'),
    ('JunÃ\xadn', 'Junín'),
    ('San MartÃ­n', 'San Martín'),
    ('San MartÃ\xadn', 'San Martín'),
    ('montaÃ±a', 'montaña'),
    ('montaÃ±as', 'montañas'),
    ('esporÃ¡dica', 'esporádica'),
    ('esporÃ¡dicas', 'esporádicas'),
    ('aÃ©rea', 'aérea'),
    ('aÃ©reas', 'aéreas'),
    ('aÃ©reo', 'aéreo'),
    ('rÃ¡pido', 'rápido'),
    ('rÃ¡pidos', 'rápidos'),
    ('caÃ±Ã³n', 'cañón'),
    ('caÃ±on', 'cañón'),
    ('guÃ­a', 'guía'),
    ('guÃ\xada', 'guía'),
    ('guÃ­as', 'guías'),
    ('guÃ\xadas', 'guías'),
    ('vÃ­a', 'vía'),
    ('vÃ\xada', 'vía'),
    ('vÃ­as', 'vías'),
    ('vÃ\xadas', 'vías'),
    ('tirolesas', 'tirolesas'),
    ('tirolesa', 'tirolesa'),
    ('Ã¡', 'á'),
    ('Ã©', 'é'),
    ('Ã\xad', 'í'),
    ('Ã­', 'í'),
    ('Ã³', 'ó'),
    ('Ãº', 'ú'),
    ('Ã±', 'ñ'),
    ('Ã‘', 'Ñ'),
    ('Ã\x81', 'Á'),
    ('Ã‰', 'É'),
    ('Ã\x8d', 'Í'),
    ('Ã“', 'Ó'),
    ('Ãš', 'Ú'),
    ('Ã¼', 'ü'),
    ('Ãœ', 'Ü'),
    ('Â°', '°'),
    ('Â¿', '¿'),
    ('Â¡', '¡')
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    for bad, good in replacements:
        content = content.replace(bad, good)
    
    # Fix the description copied into name field
    content = content.replace(
        '"nombre_infraestructura": "Algunas agencias de montaña ofrecen descensos guiados en zonas rocosas de forma esporádica."',
        '"nombre_infraestructura": "Circuito Rapel Quebrada Seca (Máncora)"'
    )
    content = content.replace(
        '"nombre_infraestructura": "Algunas agencias de monta\\u00f1a ofrecen descensos guiados en zonas rocosas de forma espor\\u00e1dica."',
        '"nombre_infraestructura": "Circuito Rapel Quebrada Seca (Máncora)"'
    )

    if orig != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed mojibake in {filepath}")
    else:
        print(f"No changes in {filepath}")
