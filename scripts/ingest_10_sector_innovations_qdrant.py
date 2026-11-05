import os
import sys
import uuid
import json
import requests
from qdrant_client import QdrantClient
from qdrant_client.http import models

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/embeddings")
EMBED_MODEL = "nomic-embed-text"

def get_embedding(text: str) -> list[float]:
    resp = requests.post(
        OLLAMA_URL,
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()["embedding"]

# 10 Innovaciones y Buenas Prácticas del Sector para Lifextreme Perú
SECTOR_INNOVATIONS = [
    {
        "innovation_number": 1,
        "title": "Integración de Redes Mesh y Telemetría Satelital Off-Grid",
        "problem": "El 85% de las rutas de expedición (Ausangate, Choquequirao, Huayhuash) no tienen cobertura celular ni datos móviles. Los operadores dependen de reportes radiales VHF manuales o no reportan nada hasta volver al pueblo.",
        "solution": "Implementar enlaces satelitales fijos/móviles (Starlink Mini en campamentos base o dispositivos satelitales bidireccionales Garmin inReach por grupo) combinados con repetidores de radioenlace y redes LoRa/Mesh. Esto permite telemetría en tiempo real: monitoreo de ritmo cardíaco/SpO2 de pasajeros en pasos críticos, botón SOS con geolocalización milimétrica para rescates y comunicación continua con la base central.",
        "standard_common": "Silencio total / Cero telemetría en ruta",
        "standard_lifextreme": "Red LoRa/Mesh + Enlace Satelital Starlink Mini / inReach + Sensores biométricos SpO2/FC en tiempo real",
        "strategic_pillar": "seguridad_biomedica",
        "pillar": "telemetria_satelital_offgrid",
        "target_department": "Operaciones",
        "target_agent": "Agente_Centinela_Terreno",
        "region": "Cusco, Ausangate, Choquequirao, Huayhuash",
        "urgency_phase": "Fase_1_Inmediata",
        "extra_collections": ["lifextreme_safety_protocols"]
    },
    {
        "innovation_number": 2,
        "title": "Trazabilidad y Gestión Ética Certificada de la Cadena de Porteo y Arriería",
        "problem": "Aunque la Ley N° 31614 (Ley del Porteador) fija límites de carga (20 kg de carga útil + 5 kg personales), en muchas rutas libres (como Salkantay o Lares) no se fiscaliza el peso sobre mulas y caballos, provocando sobrecarga animal, informalidad laboral y malestar en el turista extranjero ético.",
        "solution": "Protocolo de Pesaje Digital en Balanza Certificada y Pasaporte del Animal/Porteador. Registrar la carga de cada animal y personal con pesaje visible ante el cliente antes de salir del campamento, dotación obligatoria de herraduras, mantas térmicas veterinarias y fajas lumbares ergonómicas para arrieros, publicando la auditoría de bienestar laboral directamente en la ficha técnica de la ruta.",
        "standard_common": "Control visual o informal de cargas sin registro auditable",
        "standard_lifextreme": "Pesaje digital verificado ante el cliente + Pasaporte ético animal y cumplimiento estricto Ley N° 31614",
        "strategic_pillar": "sostenibilidad_rsc",
        "pillar": "bienestar_laboral_arrieros_animales",
        "target_department": "Supervision_Calidad",
        "target_agent": "Agente_Duffle_Optimizer",
        "region": "Cusco, Salkantay, Lares",
        "urgency_phase": "Fase_1_Inmediata",
        "extra_collections": ["lifextreme_porter_welfare_peru"]
    },
    {
        "innovation_number": 3,
        "title": "Fisioterapia y Recuperación Activa de Altitud en Campamento",
        "problem": "Los operadores terminan la jornada de 8 horas de caminata y solo ofrecen una taza de té y una cama. La acumulación de ácido láctico, inflamación articular y fatiga por deshidratación en altura deterioran la experiencia en los días subsiguientes.",
        "solution": "Protocolos de Fisioterapia y Recuperación Física Andina. Incorporar botas de compresión neumática portátiles alimentadas por batería solar, rodillos miofasciales (foam rollers), pediluvios calientes con sales de sulfato y formulaciones botánicas andinas locales (infusiones de romero, llantén y molle para desinflamar extremidades), guiados por protocolos estandarizados de estiramiento post-marcha.",
        "standard_common": "Llegada al campamento con solo carpa y té caliente",
        "standard_lifextreme": "Descarga muscular con botas de compresión neumática solar, foam rollers, pediluvios botánicos andinos (romero, llantén, molle) y estiramiento guiado",
        "strategic_pillar": "alojamiento_glamping",
        "pillar": "fisioterapia_recuperacion_altura",
        "target_department": "Operaciones",
        "target_agent": "Agente_Asesor_Medico",
        "region": "Cusco, Salkantay, Ausangate",
        "urgency_phase": "Fase_2_Media",
        "extra_collections": ["lifextreme_safety_protocols"]
    },
    {
        "innovation_number": 4,
        "title": "Saneamiento Ecológico Avanzado y Cero Impacto en Suelos Frágiles",
        "problem": "Los baños rústicos tipo letrina de pozo ciego en las paradas de campamento contaminan mantos freáticos, ríos altoandinos y generan olores insoportables que degradan el paisaje natural.",
        "solution": "Instalación de baños secos de compostaje biológico con separación de orina y deshidratación solar (emulando el estándar de EcoCamp Patagonia). Implementar sistemas de tratamiento de aguas grises de cocina mediante filtros bio-vegetales móviles antes de devolver el agua al entorno, cumpliendo de forma estricta los principios internacionales Leave No Trace (No Deje Rastro).",
        "standard_common": "Letrinas rústicas de pozo ciego contaminantes",
        "standard_lifextreme": "Baños secos de compostaje biológico solar + Filtros bio-vegetales de aguas grises (Estándar Leave No Trace / EcoCamp)",
        "strategic_pillar": "sostenibilidad_rsc",
        "pillar": "saneamiento_ecologico_leave_no_trace",
        "target_department": "Supervision_Calidad",
        "target_agent": "Agente_Tailor_Made",
        "region": "Cusco, Salkantay, Ausangate, Vilcabamba",
        "urgency_phase": "Fase_2_Media",
        "extra_collections": []
    },
    {
        "innovation_number": 5,
        "title": "Algoritmos de Descongestión Horaria y Reverse / Offset Trekking",
        "problem": "La gran masa de agencias sale a las mismas horas de los mismos campamentos (ej. Soraypampa a las 5:00–6:00 AM rumbo al Abra Salkantay), provocando cuellos de botella humanos, ruido y pérdida de la sensación de naturaleza salvaje.",
        "solution": "Itinerarios con desfase horario inteligente (Offset Trekking) o rutas satélite intermedias. Salir 90 minutos antes o después de la masa, o ubicar puntos de pernocta en cotas 2 km más adelante o en valles laterales. Permite al cliente caminar en silencio absoluto, capturar fotos sin multitudes y avistar fauna local (cóndores, vizcachas, venados) que huye de las caravanas comerciales.",
        "standard_common": "Caravanas masivas simultáneas en horas punta (05:00-06:00 AM)",
        "standard_lifextreme": "Itinerarios con desfase horario inteligente (+/- 90 min Offset Trekking) y pernocta avanzada para silencio absoluto y avistamiento de fauna",
        "strategic_pillar": "logistica_marcha",
        "pillar": "offset_trekking_descongestion",
        "target_department": "Operaciones",
        "target_agent": "Agente_Tailor_Made",
        "region": "Cusco, Salkantay",
        "urgency_phase": "Fase_1_Inmediata",
        "extra_collections": ["lifextreme_peru_routes"]
    },
    {
        "innovation_number": 6,
        "title": "Homologación de Guías de Montaña Bajo Ratios Estrictos de Seguridad",
        "problem": "Es habitual ver grupos de 14 a 16 turistas extranjeros acompañados por un solo guía general de turismo, quien en caso de emergencia médica debe dividirse entre atender al herido o cuidar del resto del grupo en un paso de 4,600 msnm.",
        "solution": "Fijación de un ratio máximo estricto de 1:8 para trekking no técnico y 1:3 para travesías glaciares o pasos nevados de altitud. Exigir certificación internacional de rescate agreste (WAFA o WFR) vigente a cada guía, con un guía asistente (sweeper) que cierre la columna de marcha para garantizar que nadie quede rezagado o descompensado sin auxilio.",
        "standard_common": "Guía único para 14-16 pasajeros con botiquín básico",
        "standard_lifextreme": "Ratios estrictos 1:8 (trekking) y 1:3 (glaciar/técnico), certificación WAFA/WFR obligatoria y guía asistente sweeper de cierre",
        "strategic_pillar": "seguridad_biomedica",
        "pillar": "ratios_guias_wfr_seguridad",
        "target_department": "Guias_Campo",
        "target_agent": "Agente_Centinela_Terreno",
        "region": "Cusco, Cordillera Blanca, Huayhuash",
        "urgency_phase": "Fase_1_Inmediata",
        "extra_collections": ["lifextreme_safety_protocols"]
    },
    {
        "innovation_number": 7,
        "title": "Cadena de Suministro Alimentaria Hiperlocal y Gastronomía Funcional de Altura",
        "problem": "Las agencias compran víveres masivos y procesados en mercados centrales de Cusco o Huaraz (enlatados, fideos comerciales, embutidos) y los transportan en camiones, dejando un impacto económico casi nulo en los campesinos de la propia ruta.",
        "solution": "Cocina funcional de altura con trazabilidad comunitaria (Kilómetro Cero). Convenios de abastecimiento directo con las comunidades del sendero: compra de truchas frescas criadas en lagunas de la zona, papas y tubérculos nativos directo de las chacras, quesos artesanales y cereales andinos (quinua, kiwicha, cañihua). Esto reduce la huella de transporte y entrega al comensal una gastronomía de autor hiperlocal con valor nutricional adaptado a la demanda calórica de alta montaña.",
        "standard_common": "Víveres procesados/enlatados comprados en ciudad sin beneficio local",
        "standard_lifextreme": "Gastronomía funcional hiperlocal con abastecimiento directo de comunidades (trucha de laguna, papas nativas, quinua, kiwicha, cañihua)",
        "strategic_pillar": "sostenibilidad_rsc",
        "pillar": "gastronomia_funcional_hiperlocal",
        "target_department": "Operaciones",
        "target_agent": "Agente_Tailor_Made",
        "region": "Cusco, Valle Sagrado, Ausangate, Salkantay",
        "urgency_phase": "Fase_1_Inmediata",
        "extra_collections": []
    },
    {
        "innovation_number": 8,
        "title": "Protocolos Auditables de Bajas y Retiro de Material Técnico (Ciclo 30 Usos)",
        "problem": "Carpas filtrando agua por termosellados vencidos, bastones desgastados que colapsan ante el peso del usuario y sacos de dormir con plumas compactadas que no retienen la temperatura a -5 °C, todo por estirar la vida útil del equipo para abaratar costos.",
        "solution": "Sistema de auditoría y trazabilidad por código QR / ID único para cada equipo técnico. Cada carpa, colchoneta, arnés o saco de dormir tiene un contador de usos y lavados en base de datos. Al llegar a las 30 salidas en alta montaña, el material es retirado obligatoriamente de la línea prémium y donado a proyectos comunitarios o reemplazado, garantizando que el pasajero siempre duerma en material térmico íntegro.",
        "standard_common": "Sobreuso de sacos de dormir y carpas hasta que fallan en tormenta",
        "standard_lifextreme": "Trazabilidad por ID único con retiro automático a las 30 salidas de alta montaña y rotación a proyectos comunitarios",
        "strategic_pillar": "estructura_calidad",
        "pillar": "trazabilidad_retiro_equipo_30_usos",
        "target_department": "Supervision_Calidad",
        "target_agent": "Agente_Calidad_Reputacion",
        "region": "Cusco",
        "urgency_phase": "Fase_1_Inmediata",
        "extra_collections": []
    },
    {
        "innovation_number": 9,
        "title": "Diversificación Activa de Rutas Satélite (Descentralización del Monopolio Machu Picchu)",
        "problem": "El 90% del turismo de aventura en Cusco depende exclusivamente del cuello de botella de los boletos a la Llaqta de Machu Picchu y los trenes de PeruRail / Inca Rail, dejando a las agencias a merced de huelgas o falta de accesos.",
        "solution": "Desarrollo de expediciones autónomas de clase mundial sin paso obligado por Machu Picchu: 1) Circuitos integrales de altura en Ausangate y Laguna Sibinacocha. 2) Gran travesía Choquequirao - Vilcabamba (Espíritu Pampa), posicionada como la verdadera expedición arqueológica agreste. 3) Rutas de ciclomontañismo (enduro/bikepacking) y trekking botánico en el cañón del Apurímac o el Valle de Lares profundo.",
        "standard_common": "Dependencia del 90% del boleto a Machu Picchu y trenes comerciales",
        "standard_lifextreme": "Portafolio autónomo de clase mundial: Ausangate-Sibinacocha, Choquequirao-Vilcabamba (Espíritu Pampa) y Enduro/Bikepacking en Apurímac y Lares",
        "strategic_pillar": "politica_comercial",
        "pillar": "diversificacion_rutas_satelite",
        "target_department": "Ventas",
        "target_agent": "Agente_Tailor_Made",
        "region": "Ausangate, Vilcabamba, Valle Sagrado",
        "urgency_phase": "Fase_2_Media",
        "extra_collections": ["lifextreme_peru_routes"]
    },
    {
        "innovation_number": 10,
        "title": "Alianzas Directas con Redes Médicas e Infraestructura de Evacuación Fija",
        "problem": "Ante un edema pulmonar (HAPE) o cerebral (HACE) en montaña, muchas agencias improvisan la evacuación a lomo de mula sin oxígeno continuo, tardando hasta 12 horas en llegar a una posta médica que frecuentemente carece de insumos básicos.",
        "solution": "Corredor de evacuación médica garantizada. Contratos de atención preferencial directa con clínicas especializadas en medicina de altura (como O2 Medical Network en Cusco), disponibilidad permanente de caballos ensillados con montura de rescate en los puntos ciegos viales, y protocolo de derivación inmediata con ambulancias privadas esperando en el punto carretero más cercano con concentradores de oxígeno de alto flujo.",
        "standard_common": "Evacuación improvisada sin oxígeno continuo hacia postas sin insumos",
        "standard_lifextreme": "Corredor clínico directo O2 Medical Network, caballos de rescate ensillados en puntos ciegos y ambulancia con oxígeno de alto flujo en cabecera vial",
        "strategic_pillar": "seguridad_biomedica",
        "pillar": "corredor_evacuacion_medica_fija",
        "target_department": "Guias_Campo",
        "target_agent": "Agente_Centinela_Terreno",
        "region": "Cusco, Salkantay, Ausangate",
        "urgency_phase": "Fase_1_Inmediata",
        "extra_collections": ["lifextreme_safety_protocols"]
    }
]

SUMMARY_MATRIX_TEXT = (
    "[Contexto: Estrategia Lifextreme Perú | Pilar: estructura_calidad | Departamento: Direccion_General]\n"
    "MATRIZ DE DIFERENCIACIÓN SECTORIAL LIFEXTREME PERÚ (ESTÁNDAR COMÚN VS ESTÁNDAR DE EXCELENCIA LIFEXTREME):\n"
    "1. Conectividad en Ruta: De silencio total / cero telemetría -> A Red Mesh LoRa + Enlace Satelital Starlink Mini/inReach + Sensores biométricos.\n"
    "2. Porteo y Animales: De control visual o informal de cargas -> A Pesaje digital verificado + Pasaporte ético animal y humano (Ley 31614).\n"
    "3. Llegada al Campamento: De solo carpa y té caliente -> A Descarga muscular con botas de compresión, pediluvios botánicos andinos y recuperación activa.\n"
    "4. Saneamiento: De letrinas rústicas de pozo ciego -> A Baños secos de compostaje biológico solar + Filtros bio-vegetales de aguas grises.\n"
    "5. Flujo de Marcha: De caravanas masivas simultáneas -> A Itinerarios con desfase horario inteligente (Offset Trekking +/- 90 min).\n"
    "6. Seguridad Fisiológica: De guía único con botiquín básico -> A Ratios 1:8 / 1:3, certificación WAFA/WFR, guía sweeper y corredor de rescate clínico O2 Medical Network."
)

def main():
    print("=" * 75)
    print(" 🏔️ INGESTIÓN DE LAS 10 BUENAS PRÁCTICAS E INNOVACIONES DEL SECTOR EN QDRANT")
    print("=" * 75)

    client = QdrantClient(url=QDRANT_URL)

    points_best_practices = []
    points_strategy = []
    points_safety = []
    points_porter = []
    points_routes = []

    for item in SECTOR_INNOVATIONS:
        enriched_text = (
            f"[Contexto: Estrategia Lifextreme Perú | Pilar: {item['strategic_pillar']} | Departamento: {item['target_department']}]\n"
            f"Innovación Sectorial #{item['innovation_number']}: {item['title']}\n"
            f"Problema Actual en el Sector Perú: {item['problem']}\n"
            f"Mejora e Innovación Lifextreme: {item['solution']}\n"
            f"Diferenciación Competitiva: Estándar Común ({item['standard_common']}) vs Estándar Lifextreme ({item['standard_lifextreme']})."
        )

        vec = get_embedding(enriched_text)
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"lifextreme-sector-innovation-{item['innovation_number']}"))

        # 1. Payload para lifextreme_benchmark_best_practices
        payload_bp = {
            "text": enriched_text,
            "title": item["title"],
            "innovation_number": item["innovation_number"],
            "source_operator": "Lifextreme Sector Innovation Standard",
            "country": "Peru",
            "region": item["region"],
            "pillar": item["pillar"],
            "strategic_pillar": item["strategic_pillar"],
            "target_agent": item["target_agent"],
            "target_department": item["target_department"],
            "standard_common": item["standard_common"],
            "standard_lifextreme": item["standard_lifextreme"],
            "doc_type": "directiva_operativa"
        }
        points_best_practices.append(models.PointStruct(id=point_id, vector=vec, payload=payload_bp))

        # 2. Payload para lifextreme_peru_strategy
        payload_strat = {
            "text": enriched_text,
            "title": item["title"],
            "country": "Peru",
            "region": item["region"],
            "strategic_pillar": item["strategic_pillar"],
            "benchmark_target": "Lifextreme Peru",
            "doc_type": "directiva_operativa",
            "target_department": item["target_department"],
            "urgency_phase": item["urgency_phase"]
        }
        points_strategy.append(models.PointStruct(id=point_id, vector=vec, payload=payload_strat))

        # 3. Colecciones especializadas adicionales
        if "lifextreme_safety_protocols" in item["extra_collections"]:
            points_safety.append(models.PointStruct(
                id=point_id,
                vector=vec,
                payload={
                    "text": enriched_text,
                    "title": item["title"],
                    "altitude_band": "3800m_5200m",
                    "medical_risk": "Prevencion_Integral_Evacuacion",
                    "certification_level": "WAFA_WFR_UIAGM",
                    "target_agent": item["target_agent"]
                }
            ))
        if "lifextreme_porter_welfare_peru" in item["extra_collections"]:
            points_porter.append(models.PointStruct(
                id=point_id,
                vector=vec,
                payload={
                    "text": enriched_text,
                    "title": item["title"],
                    "law_reference": "Ley_31614_y_Bienestar_Equino",
                    "max_weight_kg": 20,
                    "gear_compliance": "Pesaje_Digital_Visible_y_Pasaporte_Animal",
                    "target_agent": item["target_agent"]
                }
            ))
        if "lifextreme_peru_routes" in item["extra_collections"]:
            points_routes.append(models.PointStruct(
                id=point_id,
                vector=vec,
                payload={
                    "text": enriched_text,
                    "title": item["title"],
                    "route_name": item["region"],
                    "max_elevation_m": 5100,
                    "campsite_type": "Offset_Trekking_Satelite",
                    "target_agent": item["target_agent"]
                }
            ))

        print(f"  [✓] Vectorizada Innovación #{item['innovation_number']}: {item['title']}")

    # Agregar nodo de la Matriz Resumen
    matrix_vec = get_embedding(SUMMARY_MATRIX_TEXT)
    matrix_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, "lifextreme-sector-innovation-summary-matrix"))
    points_best_practices.append(models.PointStruct(
        id=matrix_id,
        vector=matrix_vec,
        payload={
            "text": SUMMARY_MATRIX_TEXT,
            "title": "Matriz Resumen de Diferenciación para Lifextreme Perú",
            "source_operator": "Lifextreme Sector Innovation Standard",
            "country": "Peru",
            "region": "Cusco",
            "pillar": "matriz_diferenciacion_excelencia",
            "strategic_pillar": "estructura_calidad",
            "target_agent": "Todos_Los_Agentes",
            "target_department": "Direccion_General",
            "doc_type": "directiva_operativa"
        }
    ))
    points_strategy.append(models.PointStruct(
        id=matrix_id,
        vector=matrix_vec,
        payload={
            "text": SUMMARY_MATRIX_TEXT,
            "title": "Matriz Resumen de Diferenciación para Lifextreme Perú",
            "country": "Peru",
            "region": "Cusco",
            "strategic_pillar": "estructura_calidad",
            "benchmark_target": "Lifextreme Peru",
            "doc_type": "directiva_operativa",
            "target_department": "Direccion_General",
            "urgency_phase": "Fase_1_Inmediata"
        }
    ))
    print("  [✓] Vectorizada Matriz Resumen de Diferenciación Lifextreme")

    # Upsert en todas las colecciones correspondientes
    client.upsert(collection_name="lifextreme_benchmark_best_practices", points=points_best_practices)
    print(f"\n  -> Upsert exitoso en 'lifextreme_benchmark_best_practices': {len(points_best_practices)} nodos.")

    client.upsert(collection_name="lifextreme_peru_strategy", points=points_strategy)
    print(f"  -> Upsert exitoso en 'lifextreme_peru_strategy': {len(points_strategy)} nodos.")

    if points_safety:
        client.upsert(collection_name="lifextreme_safety_protocols", points=points_safety)
        print(f"  -> Upsert exitoso en 'lifextreme_safety_protocols': {len(points_safety)} nodos.")

    if points_porter:
        client.upsert(collection_name="lifextreme_porter_welfare_peru", points=points_porter)
        print(f"  -> Upsert exitoso en 'lifextreme_porter_welfare_peru': {len(points_porter)} nodos.")

    if points_routes:
        client.upsert(collection_name="lifextreme_peru_routes", points=points_routes)
        print(f"  -> Upsert exitoso en 'lifextreme_peru_routes': {len(points_routes)} nodos.")

    # Smoke Test de verificación semántica
    print("\n" + "=" * 75)
    print(" 🔍 SMOKE TEST DE RECUPERACIÓN VECTORIAL EN QDRANT")
    print("=" * 75)
    test_queries = [
        ("¿Cómo solucionamos la falta de cobertura celular y telemetría en Ausangate y Choquequirao?", "lifextreme_benchmark_best_practices"),
        ("¿Qué protocolo de recuperación muscular y fisioterapia aplicamos al llegar al campamento?", "lifextreme_safety_protocols"),
        ("¿Cómo evitamos las multitudes a las 5 AM en Soraypampa y el monopolio de Machu Picchu?", "lifextreme_peru_routes"),
        ("¿Cómo garantizamos el trato ético a las mulas y porteadores con pesaje visible?", "lifextreme_porter_welfare_peru")
    ]

    for q_text, col_name in test_queries:
        q_vec = get_embedding(q_text)
        res = client.query_points(
            collection_name=col_name,
            query=q_vec,
            limit=1
        ).points
        if res:
            top = res[0]
            print(f"\n  [Colección: {col_name}]")
            print(f"  Pregunta: {q_text}")
            print(f"  Score Cosine: {top.score:.4f} | Título: {top.payload.get('title')}")
        else:
            print(f"\n  [!] Sin resultados en {col_name}")

    print("\n✅ INGESTIÓN Y VERIFICACIÓN COMPLETADAS AL 100%.")

if __name__ == "__main__":
    main()
