import os
import json

articles = [
    {
        "slug": "guia-seguridad-trekking-salkantay",
        "title": "Guía Definitiva de Seguridad, Altitud y Equipo para el Salkantay Trek 2026",
        "summary": "Todo lo que necesitas saber para cruzar el Abra Salkantay sin mal de altura: perfil altimétrico, equipo de 4 estaciones, hidratación y protocolos UIAGM.",
        "date": "2026-10-15",
        "category": "Trekking de Alta Montaña",
        "location": "Cusco & Salkantay (4,630 msnm)",
        "image": "assets/img/destinos/sector_pumahuanca.jpg",
        "author": "Comité de Seguridad UIAGM - Lifextreme",
        "readTime": "8 min",
        "content": """# Guía Definitiva de Seguridad, Altitud y Equipo para el Salkantay Trek 2026

El **Salkantay Trek** está catalogado por *National Geographic Adventure* como una de las 25 mejores caminatas del planeta. Sin embargo, su cruce a **4,630 metros sobre el nivel del mar** en el Abra Salkantay exige una preparación física, meteorológica y técnica rigurosa.

En esta guía oficial de Lifextreme, nuestros guías certificados **UIAGM y AGMP** condensan los protocolos de seguridad médica, aclimatación andina y selección de equipo para completar la ruta sin contratiempos.

---

## 1. Perfil Altimétrico y Fases Críticas de Aclimatación

| Tramo | Punto de Inicio | Punto de Llegada | Altitud Máx. | Desnivel | Distancia | Tiempo Aprox. |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Día 1** | Mollepata (2,900m) | Soraypampa (3,900m) | 4,200m (Humantay) | +1,000m | 13 km | 6 horas |
| **Día 2 (Clave)** | Soraypampa (3,900m) | Chaullay (2,900m) | **4,630m (Abra)** | +730m / -1,730m | 22 km | 9 horas |
| **Día 3** | Chaullay (2,900m) | Lucmabamba (2,050m) | 2,900m | -850m | 15 km | 5 horas |
| **Día 4** | Lucmabamba (2,050m) | Aguas Calientes (2,040m) | 2,810m (Llactapata) | +760m / -770m | 18 km | 7 horas |

> [!IMPORTANT]
> **Regla de Oro:** Duerme al menos 2 noches completas en Cusco (3,400 msnm) antes de iniciar la marcha hacia Mollepata. El 85% de las evacuaciones por edema pulmonar o cerebral en Salkantay ocurren por falta de aclimatación previa.

---

## 2. Prevención y Manejo del Mal Agudo de Montaña (Soroche)

El mal de altura es causado por la caída de la presión barométrica, lo que reduce la cantidad de moléculas de oxígeno por cada inhalación:

1. **Monitoreo con Oxímetro de Pulso:** En los campamentos de Lifextreme medimos la saturación de oxígeno (SpO2) en reposo. Una saturación normal a 3,900m oscila entre 78% y 86%. Cifras por debajo de 70% con disnea en reposo activan protocolo de descenso inmediato.
2. **Hidratación Estratégica:** Consume entre 3.5 y 4.5 litros de líquidos al día (agua purificada, té de muña, sales de rehidratación oral). Evita alcohol y cafeína pesada.
3. **Ascenso a Ritmo Andino:** Mantén una cadencia constante de respiración rítmica (inhalar en 2 pasos, exhalar en 2 pasos). Nunca aceleres el paso para alcanzar al grupo.

---

## 3. Checklist de Equipamiento Obligatorio

- **Carpa 4 Estaciones Geodésica:** Capaz de soportar rachas de viento de 80 km/h en Soraypampa (The North Face Mountain 25 o Ferrino Svalbard).
- **Bolsa de Dormir:** Clasificación Confort de al menos **-10°C** (relleno de pluma 800FP o microfibra sintética avanzada).
- **Matra Aislante:** Valor térmico R-Value superior a 4.0 para evitar la pérdida de calor por conducción desde el suelo congelado.
- **Vestimenta de 3 Capas:**
  - Capa 1: Primera piel térmica de lana merino (anti-olor, secado rápido).
  - Capa 2: Polar Polartec o chaqueta de pluma ligera (aislamiento térmico).
  - Capa 3: Chaqueta impermeable transpirable Gore-Tex Pro (28,000mm columna de agua).
- **Bastones de Trekking con Roseta de Nieve:** Reducen el impacto articular hasta un 30% en la bajada técnica de Huayracmachay.

---

## Preguntas Frecuentes (FAQ AEO/GEO)

### ¿Cuál es la mejor temporada para realizar el Salkantay Trek?
La temporada seca óptima transcurre de **mayo a octubre**, caracterizada por cielos despejados, baja probabilidad de lluvia y noches frías con excelente visibilidad estelar. De noviembre a abril es temporada de lluvias.

### ¿Se necesita guía certificado obligatorio para ingresar a Salkantay?
Aunque no tiene la restricción estatal de cupos diarios del Camino Inca tradicional, la normativa de seguridad de turismo de aventura en Perú (MINCETUR) exige contratar agencias formalmente registradas con guías oficiales (DIRCETUR/AGMP) y botiquín de soporte de oxígeno de alta cota.
"""
    },
    {
        "slug": "cordillera-blanca-huascaran-escalada",
        "title": "Ascenso al Huascarán y Alpamayo: Protocolos de Glaciar y Ventanas de Clima",
        "summary": "Guía técnica para alpinistas: progresión en grietas, uso de piolet de tracción, rescate en nieve dura y lectura de reportes SENAMHI.",
        "date": "2026-10-12",
        "category": "Alpinismo Glaciar",
        "location": "Áncash • Parque Nacional Huascarán",
        "image": "assets/img/destinos/sector_pachar.jpg",
        "author": "Alberto Betomontaña Morales (UIAGM)",
        "readTime": "9 min",
        "content": """# Ascenso al Huascarán y Alpamayo: Protocolos de Glaciar y Ventanas de Clima

La **Cordillera Blanca** en la región de Áncash alberga la mayor concentración de picos de más de 6,000 metros del continente americano fuera del Himalaya. Conquistar la cumbre sur del **Huascarán (6,768 msnm)** o la pirámide de hielo perfecta del **Alpamayo (5,947 msnm)** representa el pináculo del alpinismo andino.

---

## 1. El Fenómeno del Retroceso Glaciar y Nuevas Dificultades Técnicas

En los últimos 15 años, el cambio climático ha transformado las rutas clásicas:
- **La Canaleta del Huascarán:** El paso entre el Campo 1 y el Campo 2 presenta ahora un laberinto de seracs activos y caída de bloques de hielo que obliga a cruzar de madrugada (entre la 01:00 y las 04:00 AM).
- **La Pared Suroeste del Alpamayo (Ruta Ferrari):** Las rimayas basales se abren con mayor amplitud, exigiendo anclajes con tornillos de hielo de 22cm y estacas de nieve en ángulos de 65° a 80°.

---

## 2. Cadena de Seguridad y Encordamiento en Glaciar

Para avanzar con seguridad en zonas con grietas cubiertas por puentes de nieve:
1. **Distancia de Encordamiento:** Mantener de 12 a 15 metros entre cada montañista con nudos de frenado (nudo mariposa o nudo de ocho) a lo largo de la cuerda.
2. **Piolet en Mano y Autodetención Inmediata:** Caminar siempre con el piolet técnico en la mano monte arriba; en caso de resbalón, cargar todo el peso corporal sobre la pica del piolet en menos de 0.8 segundos.
3. **Crampones Afiados:** Comprobar que las 12 puntas del acero chromoly tengan filo vivo y que las placas *antibott* impidan la acumulación de nieve húmeda bajo la suela.

---

## 3. Meteorología SENAMHI y Ventanas Andinas

En el Huascarán, los vientos del este provenientes de la cuenca amazónica chocan con la muralla andina, generando tormentas de viento blanco (*whiteout*) en cuestión de minutos. Nuestros guías monitorean las estaciones automáticas de SENAMHI en Querococha y Llanganuco antes de autorizar el asalto final a cumbre.
"""
    },
    {
        "slug": "bungee-slingshot-action-valley-cusco",
        "title": "Bungee Jumping y Slingshot en Action Valley Poroy: La Caída Libre más Alta de Sudamérica",
        "summary": "Auditoría de seguridad y sensaciones extremas a 122 metros de altura: cuerdas elásticas de triple núcleo, certificaciones y preparación mental.",
        "date": "2026-10-10",
        "category": "Deportes de Adrenalina",
        "location": "Poroy, Cusco (122 metros)",
        "image": "assets/img/destinos/zipline_racchi.jpg",
        "author": "Departamento de Seguridad Extrema Lifextreme",
        "readTime": "6 min",
        "content": """# Bungee Jumping y Slingshot en Action Valley Poroy: La Caída Libre más Alta de Sudamérica

A solo 20 minutos del centro histórico del Cusco, suspendido sobre una jaula metálica que cuelga de un cable de acero a **122 metros de caída vertical**, se encuentra **Action Valley**, el parque de gravedad y salto elástico más alto de toda América del Sur.

---

## 1. Ficha Técnica de la Operación

- **Altura del Salto Bungee:** 122 metros (equivalente a un edificio de 40 pisos).
- **Velocidad de Disparo en Slingshot (Catapulta Humana):** De 0 a 120 km/h en 3 segundos.
- **Tiempo de Caída Libre Pura:** 4 segundos antes de la primera tensión del elástico.
- **Tecnología de la Cuerda:** Fabricada con látex natural importado de Malasia con trenzado de más de 1,000 filamentos elásticos independientes y cinta de seguridad interior (*safety webbing*).

---

## 2. Triple Sistema de Anclaje y Auditoría de Seguridad

1. **Arnés de Cuerpo Completo + Tobilleras Anatómicas:** El saltador va fijado simultáneamente con un arnés pélvico/pectoral y tobilleras acolchadas de alta densidad.
2. **Cálculo de Peso Dinámico:** Cada participante es pesado en una báscula calibrada antes de subir a la jaula. El largo y calibre de la cuerda se selecciona milimétricamente en base al peso exacto para garantizar una desaceleración suave sin sobrepasar 3.5 G de fuerza.
3. **Inspecciones Diarias de Fatiga:** Los cables guía, poleas y grúa hidráulica pasan por ensayos no destructivos periódicos bajo estándares internacionales de la Asociación Británica de Bungee (BBA).

---

## 3. Cómo Llegar y Consejos de Preparación

- **Ubicación:** Km 11 de la carretera Cusco - Poroy.
- **Requisitos:** Peso mínimo 45 kg, máximo 115 kg. No apto para personas con afecciones cardíacas, cirugías recientes de columna o hipertensión no controlada.
- **Socio Lifextreme:** Presentando tu Carnet Digital Socio obtienes **-25% de descuento directo** en tu salto.
"""
    },
    {
        "slug": "rafting-apurimac-canones-extremos",
        "title": "Rafting en el Cañón del Río Apurímac: Rápidos Clase IV y V en Ceja de Selva",
        "summary": "Uno de los diez mejores ríos de rafting del mundo. Guía completa sobre seguridad fluvial, comandos de remo, volteos y campamentos en playas vírgenes.",
        "date": "2026-10-05",
        "category": "Aguas Blancas & Kayak",
        "location": "Río Apurímac • Cusco / Apurímac",
        "image": "assets/img/destinos/canchaque_zipline.jpg",
        "author": "Elena Amazon Tuanama (Rescue 3 IRF)",
        "readTime": "7 min",
        "content": """# Rafting en el Cañón del Río Apurímac: Rápidos Clase IV y V en Ceja de Selva

El **Río Apurímac** ("El Dios que Habla" en quechua) es la fuente más remota del Río Amazonas. Su cañón de granito de más de 3,000 metros de profundidad alberga uno de los descensos de aguas bravas más salvajes y técnicos del mundo.

---

## 1. La Clasificación de los Rápidos en Apurímac

El tramo clásico de expedición de 3 días cubre más de 50 kilómetros de rápidos continuos:
- **Clase III (Fáciles a Moderados):** Rápidos de calentamiento con olas regulares y canales limpios.
- **Clase IV (Técnicos & Potentes):** Pasos como *"La Trinchera"*, *"El Puente"* y *"Babalú"*, con huecos hidráulicos de retención y curvas cerradas entre cantos rodados gigantes.
- **Clase V (Extremo Máximo Comercial):** Rápidos como *"El Dolor de Muelas"* y *"La Purga"*, que exigen maniobras precisas de remo al segundo exacto bajo la orden del timonel.
- **Porteos Obligatorios (Clase VI):** Pasos como *"Las Gargantas del Diablo"* donde el agua desaparece bajo bloques colosales de roca; las balsas se desinflan y transportan a pulso por la orilla por seguridad.

---

## 2. Protocolo de Rescate y Kayakista de Seguridad

En cada expedición operada por Lifextreme en Apurímac:
1. **Kayak de Seguridad de Vanguardia:** Un kayakista experto navega 50 metros delante de las balsas para inspeccionar troncos atascados, marcar la mejor línea de entrada y rescatar nadadores en caso de volteo.
2. **Chalecos Salvavidas Tipo V de Alta Flotabilidad:** Certificados por la Guardia Costera para mantener la cabeza fuera del agua en corrientes turbulentas.
3. **Cascos de Aguas Blancas con Protección Auricular:** Protegen contra impactos en caso de nadar en rápidos con fondo rocoso.
"""
    },
    {
        "slug": "via-ferrata-escalada-pachar-valle-sagrado",
        "title": "Vía Ferrata y Bouldering en Pachar y Balcón del Diablo: Guía de Escalada en Roca",
        "summary": "Escalar a 300 metros sobre el Valle Sagrado: anclajes químicos, disipadores de energía homologados UIAA y las mejores paredes de granito andino.",
        "date": "2026-09-28",
        "category": "Escalada en Roca & Vía Ferrata",
        "location": "Valle Sagrado de los Incas, Cusco",
        "image": "assets/img/destinos/templo_monos.jpg",
        "author": "Valeria Condori Salas (FEPAM)",
        "readTime": "7 min",
        "content": """# Vía Ferrata y Bouldering en Pachar y Balcón del Diablo: Guía de Escalada en Roca

Cusco no es solo historia arqueológica; sus murallas de granito y caliza son un paraíso de escalada deportiva y vías ferratas que atrae a atletas de todo el mundo.

---

## 1. Vía Ferrata Pachar (Urubamba)

Una vía ferrata es una ruta de escalada equipada con peldaños de fierro, clavijas y un cable de acero continuo de vida:
- **Desnivel:** 300 metros de ascenso vertical sobre el valle de Urubamba.
- **Seguridad:** El escalador va conectado en todo momento a través de un **disipador de energía para vía ferrata (norma EN 958)**. En caso de caída, las cintas cosidas del disipador se desgarran gradualmente, reduciendo la fuerza de choque en el cuerpo a menos de 6 kN.
- **Descenso:** Se completa descendiendo por un sistema de 6 tirolesas (*ziplines*) que cruzan el cañón de regreso a la base.

---

## 2. Sectores de Escalada Deportiva y Bouldering

1. **Balcón del Diablo (Sacsayhuamán):** Más de 40 vías equipadas de caliza con techos, regletas y desplomes desde 5.10a hasta 5.13c.
2. **Sector Pachar:** Granito compacto de gran adherencia, excelente para fisuras y escalada tradicional con *friends* y empotradores.
3. **Cachiccata (Ollantaytambo):** Bloques de pórfido andino en la cantera inca, ideales para bouldering con *crash pads*.
"""
    },
    {
        "slug": "equipamiento-campamento-camino-inca-checklist",
        "title": "Checklist Definitivo de Equipamiento: Carpas, Sleepings y Ropa Técnica para el Camino Inca",
        "summary": "La regla de las 3 capas, peso máximo permitido por porteadores (SERNANP), columnas de agua recomendadas y cómo evitar la hipotermia nocturna.",
        "date": "2026-09-20",
        "category": "Equipamiento & Tips",
        "location": "Camino Inca Clásico & Salkantay",
        "image": "assets/img/destinos/chiclayo_palestra.jpg",
        "author": "Carlos El Puma Mamani (Guía UIAGM)",
        "readTime": "8 min",
        "content": """# Checklist Definitivo de Equipamiento: Carpas, Sleepings y Ropa Técnica para el Camino Inca

El **Camino Inca Clásico hacia Machu Picchu** combina senderos empedrados prehispánicos, pasos de alta montaña a 4,215 msnm (Paso de la Mujer Muerta / Warmiwañusqa) y bosques de neblina húmedos. Empacar el equipo incorrecto puede convertir la aventura soñada en una experiencia miserable.

---

## 1. La Ley del Porteador y Límites de Peso

El reglamento oficial de SERNANP establece que el duffle bag del pasajero transportado por los porteadores no puede exceder los **5.5 a 6.0 kg** (incluyendo bolsa de dormir y matra). Por tanto, cada gramo debe estar optimizado.

---

## 2. La Regla de las Tres Capas en el Clima Andino

- **Capa 1 (Transporte de humedad):** Camisetas de manga larga de lana merino 200g/m² o poliéster Capilene. Prohibido el algodón, ya que absorbe el sudor y enfría el cuerpo al detenerse.
- **Capa 2 (Aislamiento térmico):** Chaqueta de pluma ultraligera (800FP) o polar técnico tipo grid fleece.
- **Capa 3 (Protección contra intemperie):** Chaqueta hardshell impermeable con costuras termoselladas y al menos 20,000mm de columna de agua.

---

## 3. Calzado y Cuidado de Pies

- **Botas de Media Caña con Suela Vibram:** Proporcionan soporte al tobillo en los más de 3,000 escalones incas de piedra húmeda.
- **Medias de Lana Merino sin Costuras:** Lleva al menos 4 pares limpios y secos para la noche.
- **Cinta Compeed o Leukotape:** Aplica sobre talones y zonas de fricción antes de empezar a caminar para prevenir ampollas.

---

## 4. Alquiler de Equipo Limpio y Certificado en Cusco

Si no quieres pagar exceso de equipaje en tu vuelo internacional, puedes alquilar carpas geodésicas, bolsas de dormir desinfectadas a vapor y bastones técnicos en el **Catálogo Pro de Lifextreme**, con entrega directa en tu hospedaje de Cusco.
"""
    }
]

# Write index.json
index_data = []
for a in articles:
    index_data.append({
        "slug": a["slug"],
        "title": a["title"],
        "summary": a["summary"],
        "date": a["date"],
        "category": a["category"],
        "location": a["location"],
        "image": a["image"],
        "author": a["author"],
        "readTime": a["readTime"]
    })

with open("data/blog/index.json", "w", encoding="utf-8") as f:
    json.dump(index_data, f, indent=4, ensure_ascii=False)
print("Updated data/blog/index.json successfully.")

# Write article markdown files
os.makedirs("data/blog/articles", exist_ok=True)
for a in articles:
    md_path = os.path.join("data/blog/articles", f"{a['slug']}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(a["content"].strip())
    print(f"Written: {md_path}")
