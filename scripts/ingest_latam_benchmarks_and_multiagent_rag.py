import os
import sys
import json
import uuid
import urllib.request
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    PayloadSchemaType,
    Filter,
    FieldCondition,
    MatchValue,
    HnswConfigDiff
)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://127.0.0.1:11434/api/embeddings")
EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_SIZE = 768

def get_ollama_embedding(text: str) -> list[float]:
    req_data = json.dumps({"model": EMBEDDING_MODEL, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    return res["embedding"]

COLLECTIONS_CONFIG = [
    {
        "name": "lifextreme_benchmark_best_practices",
        "indexes": ["source_operator", "country", "pillar", "target_agent"]
    },
    {
        "name": "lifextreme_safety_protocols",
        "indexes": ["altitude_band", "medical_risk", "certification_level", "target_agent"]
    },
    {
        "name": "lifextreme_porter_welfare_peru",
        "indexes": ["law_reference", "max_weight_kg", "gear_compliance", "target_agent"]
    },
    {
        "name": "lifextreme_peru_routes",
        "indexes": ["route_name", "max_elevation_m", "campsite_type", "target_agent"]
    }
]

def init_qdrant_collections(client: QdrantClient):
    print("🚀 Verificando e inicializando colecciones vectoriales en Qdrant...")
    for col in COLLECTIONS_CONFIG:
        name = col["name"]
        if not client.collection_exists(name):
            print(f"  ✨ Creando colección: '{name}' (768 Dim, Cosine)...")
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
                hnsw_config=HnswConfigDiff(m=16, ef_construct=100)
            )
        else:
            print(f"  ℹ️ Colección existente: '{name}'")

        for idx_field in col["indexes"]:
            try:
                client.create_payload_index(
                    collection_name=name,
                    field_name=idx_field,
                    field_schema=PayloadSchemaType.KEYWORD
                )
            except Exception:
                pass
    print("✅ Todas las colecciones e índices de payload están listos.\n")

# Corpus de Conocimiento Estructurado
BENCHMARKS_CORPUS = [
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-mlp-001",
        "text": "Mountain Lodges of Peru (MLP) — Cusco (Salkantay y Lares). Modelo Operativo: Pioneros mundiales del trekking lodge-to-lodge de alta montaña en los Andes. Sustituyeron el campamento tradicional por una red de lodges fijos con calefacción, jacuzzis exteriores frente a glaciares y alta gastronomía maridada. Innovación Social y Sostenibilidad: Crearon la asociación civil sin fines de lucro Yanapana Perú antes de edificar su primer lodge, transformando a las comunidades arrieras en socias de la cadena de valor y formalizando jornales dignos muy por encima del promedio del mercado.",
        "payload": {
            "source_operator": "Mountain Lodges of Peru (MLP)",
            "country": "Peru",
            "region": "Cusco",
            "pillar": "alojamiento_glamping_social",
            "target_agent": "Agente_Disenador_Tailor_Made",
            "pricing_model": "premium_2500_4500_usd",
            "territory": "Salkantay y Lares"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-mlp-002",
        "text": "Mountain Lodges of Peru (MLP) — Mejores Prácticas para Lifextreme: Protocolos de Confort y Fisioterapia Post-Marcha: Integrar en los puntos de descanso tinas calientes, masajes terapéuticos de descarga muscular y tisanas desinflamatorias con botánica andina tras jornadas de 7 a 9 horas de marcha. Tarificación Prémium: Desmarcarse de la guerra de precios de Cusco comercializando expediciones de $2,500 a $4,500 USD por pasajero, justificadas por la exclusividad de infraestructura y la hospitalidad de montaña.",
        "payload": {
            "source_operator": "Mountain Lodges of Peru (MLP)",
            "country": "Peru",
            "region": "Cusco",
            "pillar": "fisioterapia_post_marcha_tarifas",
            "target_agent": "Agente_Disenador_Tailor_Made",
            "pricing_model": "premium_2500_4500_usd",
            "territory": "Cusco"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-alpaca-001",
        "text": "Alpaca Expeditions — Perú (Cusco: Camino Inca, Salkantay, Ausangate). Modelo Operativo: La operadora con mayor volumen, consistencia operativa y tracción de reseñas globales en Cusco (reconocida consecutivamente con el Tripadvisor Travelers' Choice Best of the Best). Políticas de Bienestar Laboral y Seguridad: Lideran el estándar de protección al trabajador con su equipo 'The Green Machine', aplicando estrictamente la Ley del Porteador (Ley N° 31614) con pesaje electrónico riguroso (máximo legal de 20 kg de carga y 5 kg de equipo personal). Cuentan con un médico exclusivo para el personal (Porter's Doctor) y entrenamientos anuales obligatorios en soporte vital dictados por médicos colegiados cada mes de febrero.",
        "payload": {
            "source_operator": "Alpaca Expeditions",
            "country": "Peru",
            "region": "Cusco",
            "pillar": "bienestar_laboral_seguridad",
            "target_agent": "Agente_Centinela_Despacho",
            "law_compliance": "Ley_31614",
            "territory": "Camino Inca, Salkantay, Ausangate"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-alpaca-002",
        "text": "Alpaca Expeditions — Mejores Prácticas para Lifextreme: El Bienestar del Personal como Activo de Marca: Certificar y transparentar ante el cliente internacional que el equipo de porteo y arriería de Lifextreme cuenta con calzado técnico, seguro médico, límites de carga fiscalizados y comidas calientes idénticas a las del pasajero. Embudo Automatizado de Reputación: Un protocolo estructurado donde los guías aplican una encuesta de satisfacción digital en el tren de retorno de Machu Picchu a Ollantaytambo, activando recordatorios automáticos de reseña a las 24 horas.",
        "payload": {
            "source_operator": "Alpaca Expeditions",
            "country": "Peru",
            "region": "Cusco",
            "pillar": "reputacion_embudo_resenas",
            "target_agent": "Agente_Calidad_Reputacion",
            "territory": "Machu Picchu - Cusco"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-inkaland-001",
        "text": "Inkaland Treks — Perú (Huaraz: Cordillera Blanca y Huayhuash). Modelo Operativo: Operador técnico de alta montaña especializado en trekking de altura y ascensos alpinos de 5,000 m y 6,000 m en el norte peruano. Rigor en Seguridad y Ratios Guía-Cliente: Emplea exclusivamente guías certificados AGMP / UIAGM / IFMGA (el estándar alpino más riguroso del mundo) para escalada, y guías AGOCP / UIMLA para trekking. Mantienen ratios estrictos de seguridad de 1:2 o máximo 1:3 (un guía por cada dos o tres escaladores) en cumbres técnicas como Vallunaraju, Mateo o Chopicalqui.",
        "payload": {
            "source_operator": "Inkaland Treks",
            "country": "Peru",
            "region": "Huaraz",
            "pillar": "seguridad_alpina_ratios",
            "target_agent": "Agente_Asesor_Medico_Aclimatacion",
            "certification": "UIAGM_AGMP",
            "territory": "Cordillera Blanca y Huayhuash"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-inkaland-002",
        "text": "Inkaland Treks — Mejores Prácticas para Lifextreme: Escalera Metódica de Aclimatación: Protocolos obligatorios de 2 a 3 días de aclimatación progresiva por encima de los 4,000 msnm (ej. Laguna Llaca, Wilcacocha o Humantay) antes de autorizar el cruce de pasos críticos. Logística de 4 Estaciones: Implementación de carpas de alta montaña de 4 estaciones, colchonetas aislantes de celda cerrada más autoinflables, y botiquines con pulsioxímetro, tensiómetro y oxígeno medicinal en todas las salidas.",
        "payload": {
            "source_operator": "Inkaland Treks",
            "country": "Peru",
            "region": "Huaraz",
            "pillar": "aclimatacion_logistica_4estaciones",
            "target_agent": "Agente_Asesor_Medico_Aclimatacion",
            "territory": "Cordillera Blanca"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-ecocamp-001",
        "text": "EcoCamp Patagonia — Chile (Parque Nacional Torres del Paine). Modelo Operativo: El primer hotel de domos geodésicos del planeta (creado en 2001 por Cascada Expediciones), referente mundial en sostenibilidad arquitectónica y hospitalidad de bajo impacto. Infraestructura Ecológica: El 95% de su energía proviene de fuentes solares y microhidroeléctricas; utiliza baños secos con compostaje biológico de última generación, pasarelas elevadas de madera para evitar la erosión del suelo y estufas de combustión limpia a base de leña recolectada. Domos escalonados: Standard (10 m², bajo carbono, baño compartido), Superior (23 m², calefactor a gas, baño privado), Suite (28 m²) y Suite Loft (37 m², dos plantas).",
        "payload": {
            "source_operator": "EcoCamp Patagonia",
            "country": "Chile",
            "region": "Patagonia",
            "pillar": "domos_sostenibles_ecologia",
            "target_agent": "Agente_Disenador_Tailor_Made",
            "territory": "Torres del Paine"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-ecocamp-002",
        "text": "EcoCamp Patagonia — Mejores Prácticas para Lifextreme: Segmentación de Domos Geodésicos: Estructurar los futuros campamentos de Lifextreme (en Salkantay o Ausangate) con domos escalonados, combinando opciones accesibles con suites prémium. Filosofía de Desconexión Digital (Digital Detox): Ausencia intencionada de Wi-Fi en las unidades de descanso para favorecer la inmersión natural, concentrando la electricidad y la interacción comunitaria en los domos centrales de sala y comedor.",
        "payload": {
            "source_operator": "EcoCamp Patagonia",
            "country": "Chile",
            "region": "Patagonia",
            "pillar": "digital_detox_segmentacion_domos",
            "target_agent": "Agente_Disenador_Tailor_Made",
            "territory": "Salkantay y Ausangate"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-explora-001",
        "text": "Explora — Chile, Argentina y Perú (Valle Sagrado, Patagonia, Atacama). Modelo Operativo: Fundado en 1993 por Pedro Ibáñez, redefinió los viajes de exploración bajo el concepto de 'lujo de lo esencial': los hoteles no son destinos estáticos, sino bases logísticas para explorar a fondo el territorio. Escuela Propietaria de Formación (Explora Guide School): En lugar de contratar guías independientes al azar, cuentan con una academia interna permanente donde científicos, arqueólogos y montañistas entrenan intensivamente a los guías en geología, botánica, astronomía, historia andina y rescate agreste.",
        "payload": {
            "source_operator": "Explora",
            "country": "Peru_Chile_Argentina",
            "region": "Valle Sagrado",
            "pillar": "escuela_guias_territorio",
            "target_agent": "Agente_Calidad_Reputacion",
            "territory": "Valle Sagrado y Atacama"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-explora-002",
        "text": "Explora — Mejores Prácticas para Lifextreme: Narrativa y Profundidad del Relato: Elevar el estándar de los guías de Lifextreme en Perú más allá de las explicaciones turísticas rutinarias, formándolos en arqueoastronomía inca, glaciología andina y ecología de queñuales. Exploraciones Multimodales: Combinar en una misma travesía senderismo de montaña, rutas en bicicleta eléctrica de montaña (e-MTB), cabalgatas y avistamiento de flora endémica.",
        "payload": {
            "source_operator": "Explora",
            "country": "Peru",
            "region": "Cusco",
            "pillar": "narrativa_profunda_multimodal",
            "target_agent": "Agente_Disenador_Tailor_Made",
            "territory": "Valle Sagrado"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-awasi-001",
        "text": "Awasi — Chile y Argentina (Atacama, Patagonia, Iguazú — Relais & Châteaux). Modelo Operativo: La cúspide de la personalización en expediciones de Sudamérica. Cada villa o habitación tiene asignado de manera exclusiva un guía privado y un vehículo 4x4 todo terreno durante toda la estancia. Cero Horarios Fijos: No existen grupos predeterminados ni salidas calendarizadas obligatorias; el programa de cada día se diseña la víspera entre el huésped y su guía según el ritmo físico, el clima y los intereses individuales. Su cocina ostenta el sello Relais & Châteaux, integrando ingredientes hiperlocales como chañar, papas nativas, carob y quinua.",
        "payload": {
            "source_operator": "Awasi",
            "country": "Chile_Argentina",
            "region": "Atacama_Patagonia",
            "pillar": "private_tailor_made_4x4",
            "target_agent": "Agente_Disenador_Tailor_Made",
            "territory": "Atacama e Iguazú"
        }
    },
    {
        "collection": "lifextreme_benchmark_best_practices",
        "id": "bench-awasi-002",
        "text": "Awasi — Mejores Prácticas para Lifextreme: Línea Private Tailor-Made: Crear para Lifextreme Perú una línea 'VIP Private Expedition' con guía y transporte 4x4 exclusivo, captando al segmento de viajeros que rehúye de los grupos organizados de 12 personas. Gastronomía de Autor en Campamento: Transformar los menús de montaña utilizando insumos autóctonos peruanos (trucha de laguna altoandina, maíces del Valle Sagrado, tubérculos nativos) preparados con técnicas gourmet por chefs de expedición.",
        "payload": {
            "source_operator": "Awasi",
            "country": "Peru",
            "region": "Cusco",
            "pillar": "vip_private_gastronomia_autor",
            "target_agent": "Agente_Disenador_Tailor_Made",
            "territory": "Cusco y Valle Sagrado"
        }
    }
]

SAFETY_CORPUS = [
    {
        "collection": "lifextreme_safety_protocols",
        "id": "safe-001",
        "text": "Protocolo de Soporte Fisiológico y Aclimatación Escalonada: Para pasos por encima de 4,000 msnm (Paso Salkantay 4,630m, Paso Incachiriasca 5,100m, Paso Llanganuco 4,767m), se exige 48h a 72h de estancia previa en Cusco o Huaraz. Monitoreo diario biométrico matutino y vespertino con pulsioxímetro y tensiómetro. Registro de Score Lake Louise para detección temprana de Mal Agudo de Montaña (MAM).",
        "payload": {
            "altitude_band": "alta_montana_4000_5200m",
            "medical_risk": "mal_agudo_montana_edema",
            "certification_level": "WFR_WAFA",
            "target_agent": "Agente_Asesor_Medico_Aclimatacion"
        }
    },
    {
        "collection": "lifextreme_safety_protocols",
        "id": "safe-002",
        "text": "Protocolo de Evacuación Agreste y Telemetría Satelital: Cada expedición cuenta con botiquín de trauma y oxígeno medicinal comprimido de 3 m3 con regulador de flujo. Si la saturación de oxígeno del usuario desciende por debajo del 70% (SpO2 < 70%) o se detectan estertores pulmonares, se activa de inmediato el caballo de auxilio y el descenso de emergencia, notificando vía Garmin inReach SOS a la base de despacho y a O2 Medical Network en Cusco.",
        "payload": {
            "altitude_band": "alta_cota_critica",
            "medical_risk": "hipoxia_severa_evacuacion",
            "certification_level": "UIAGM_WFR",
            "target_agent": "Agente_Centinela_Despacho"
        }
    },
    {
        "collection": "lifextreme_safety_protocols",
        "id": "safe-003",
        "text": "Ratios Estrictos Guía-Cliente para Cumbres Glaciares y Rutas Técnicas: Para ascensos de alta montaña sobre glaciares andinos (Nevado Vallunaraju 5,686m, Nevado Mateo 5,150m, Nevado Chachani 6,057m), ratio de 1 guía oficial UIAGM / AGMP por cada 2 o 3 escaladores máximo. Prohibida la progresión encordada con más de 3 clientes por guía certificado.",
        "payload": {
            "altitude_band": "cumbres_glaciares_5000_6500m",
            "medical_risk": "caida_grieta_alpinismo",
            "certification_level": "UIAGM_IFMGA",
            "target_agent": "Agente_Centinela_Despacho"
        }
    }
]

PORTER_CORPUS = [
    {
        "collection": "lifextreme_porter_welfare_peru",
        "id": "porter-001",
        "text": "Protocolo de Bienestar para Porteadores y Arrieros basado en Ley N° 31614: Límite estricto de carga de 20 kg por porteador controlado en balanza digital electrónica al inicio y en cada puesto de control, más 5 kg asignados para pertenencias personales. Dotación obligatoria de calzado de montaña ergonómico con suela adherente, faja lumbar de protección, uniforme térmico de 2 capas impermeable y seguro de salud/accidentes de trabajo.",
        "payload": {
            "law_reference": "Ley_31614_Porteador",
            "max_weight_kg": "20kg_carga_5kg_personal",
            "gear_compliance": "calzado_faja_uniforme_termico",
            "target_agent": "Agente_Centinela_Despacho"
        }
    },
    {
        "collection": "lifextreme_porter_welfare_peru",
        "id": "porter-002",
        "text": "Regla de 7 kg de Duffle Bag para Pasajeros y Cadena de Suministro: Cada viajero recibe un bolso duffle bag técnico impermeable provisto por Lifextreme con capacidad máxima sellada de 7 kg para ropa de campamento y sleeping. El equipaje restante de día viaja en mochila personal de 20-30 L. El equipo de porteadores y arrieros recibe alimentos calientes con la misma dieta hipercalórica y balanceada que los clientes y pernocta en carpas de 4 estaciones con colchonetas aislantes.",
        "payload": {
            "law_reference": "Regla_7kg_Lifextreme",
            "max_weight_kg": "7kg_duffle_bag_pasajero",
            "gear_compliance": "duffle_bag_sellado_campamento_4estaciones",
            "target_agent": "Agente_Logistica_Duffle_Optimizer"
        }
    }
]

ROUTES_CORPUS = [
    {
        "collection": "lifextreme_peru_routes",
        "id": "route-001",
        "text": "Salkantay Trek 5D/4N Clásico & Sky Domes: Recorrido desde Mollepata hacia Soraypampa (3,900 msnm), ascenso al Abra Salkantay (4,630 msnm) frente a los glaciares del Nevado Salkantay y descenso hacia ceja de selva en Chaullay, Lucmabamba (cafetales y baños termales Cocalmayo) y arribo final a Machu Picchu vía Hidroeléctrica / Aguas Calientes.",
        "payload": {
            "route_name": "Salkantay_Trek_5D4N",
            "max_elevation_m": "4630m",
            "campsite_type": "domos_geodesicos_glamping",
            "target_agent": "Agente_Disenador_Tailor_Made"
        }
    },
    {
        "collection": "lifextreme_peru_routes",
        "id": "route-002",
        "text": "Circuito Cordillera Huayhuash Alpino 8D/7N: Travesía de alta montaña en los Andes centrales de Perú, cruzando pasos sobre 4,800 msnm (Punta Cacanan, Paso Carhuac, Portachuelo de Huayhuash, Paso Cuyoc 5,000 msnm). Campamentos junto a lagunas glaciares Siula Grande, Yerupajá y Carhuacocha. Aislamiento geográfico total con apoyo de arriería y equipo 4 estaciones.",
        "payload": {
            "route_name": "Huayhuash_Alpino_8D7N",
            "max_elevation_m": "5000m",
            "campsite_type": "campamento_4estaciones_expedicion",
            "target_agent": "Agente_Disenador_Tailor_Made"
        }
    },
    {
        "collection": "lifextreme_peru_routes",
        "id": "route-003",
        "text": "Camino Inca Clásico 4D/3N a Machu Picchu: Trekking patrimonial incaico recorriendo 43 km por senderos empedrados ancestrales, cruzando el temido Paso de la Mujer Muerta (Warmiwañusqa 4,215 msnm), Runqurakay, Sayacmarca, Phuyupatamarca y la Puerta del Sol (Inti Punku) con vista panorámica a Machu Picchu.",
        "payload": {
            "route_name": "Camino_Inca_Clasico_4D3N",
            "max_elevation_m": "4215m",
            "campsite_type": "campamentos_sernanp_autorizados",
            "target_agent": "Agente_Logistica_Duffle_Optimizer"
        }
    }
]

def ingest_all():
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    init_qdrant_collections(client)

    all_data = BENCHMARKS_CORPUS + SAFETY_CORPUS + PORTER_CORPUS + ROUTES_CORPUS
    total = len(all_data)
    print(f"📦 Total de nodos de benchmarking y arquitectura de agentes a vectorizar: {total}...")

    # Ingestar en cada colección correspondiente
    for idx, item in enumerate(all_data, 1):
        col_name = item["collection"]
        point_id = str(uuid.uuid4())
        print(f"  [{idx:02d}/{total:02d}] Vectorizando '{item['id']}' con {EMBEDDING_MODEL} -> {col_name}...")
        
        emb = get_ollama_embedding(item["text"])
        
        pt = PointStruct(
            id=point_id,
            vector=emb,
            payload={
                "doc_id": item["id"],
                "text": item["text"],
                **item["payload"]
            }
        )
        client.upsert(collection_name=col_name, points=[pt])

    print("\n🎉 ¡Ingestión en las 4 colecciones completada exitosamente!")

    # Smoke tests para los 5 agentes
    print("\n🔍 ================= SMOKE TESTS: MALLA MULTIAGENTE =================")

    agent_tests = [
        {
            "agent": "Agente Asesor Médico y de Aclimatación",
            "col": "lifextreme_safety_protocols",
            "query": "plan de aclimatacion previa en cusco y deteccion de mal de montana lake louise",
            "filter": Filter(must=[FieldCondition(key="target_agent", match=MatchValue(value="Agente_Asesor_Medico_Aclimatacion"))])
        },
        {
            "agent": "Agente de Logística y Duffle Bag Optimizer",
            "col": "lifextreme_porter_welfare_peru",
            "query": "limite maximo de peso duffle bag de 7 kilos en mulas y mochila ligera",
            "filter": Filter(must=[FieldCondition(key="target_agent", match=MatchValue(value="Agente_Logistica_Duffle_Optimizer"))])
        },
        {
            "agent": "Agente de Personalización Private Tailor-Made",
            "col": "lifextreme_benchmark_best_practices",
            "query": "expedicion privada vip con guia exclusivo vehiculo 4x4 y gastronomia de autor",
            "filter": Filter(must=[FieldCondition(key="target_agent", match=MatchValue(value="Agente_Disenador_Tailor_Made"))])
        },
        {
            "agent": "Agente Centinela de Operaciones y Seguridad",
            "col": "lifextreme_safety_protocols",
            "query": "evacuacion de emergencia con caballo de auxilio y notificacion garmin inreach",
            "filter": Filter(must=[FieldCondition(key="target_agent", match=MatchValue(value="Agente_Centinela_Despacho"))])
        },
        {
            "agent": "Agente de Calidad y Cierre Reputacional",
            "col": "lifextreme_benchmark_best_practices",
            "query": "encuesta automatizada en el tren de retorno a cusco y resenas en tripadvisor",
            "filter": Filter(must=[FieldCondition(key="target_agent", match=MatchValue(value="Agente_Calidad_Reputacion"))])
        }
    ]

    for t in agent_tests:
        print(f"\n🤖 Prueba: {t['agent']}")
        print(f"  Colección: {t['col']} | Query: \"{t['query']}\"")
        q_emb = get_ollama_embedding(t["query"])
        hits = client.query_points(
            collection_name=t["col"],
            query=q_emb,
            query_filter=t["filter"],
            limit=1
        ).points
        
        if hits:
            h = hits[0]
            print(f"  ✅ Top Match [Score: {h.score:.4f}] Doc: {h.payload.get('doc_id')}")
            snippet = h.payload.get('text', '')[:160].replace('\n', ' ')
            print(f"    Texto: \"{snippet}...\"")
        else:
            print("  ❌ No se encontraron coincidencias para el filtro.")

    print("\n✅ ¡Todos los agentes superaron las pruebas de recuperación vectorial con filtrado de metadatos!")

if __name__ == "__main__":
    ingest_all()
