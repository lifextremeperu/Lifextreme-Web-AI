"""
ETIQUETADO MASIVO POR ÁREAS — Lifextreme_Knowledge
Agrega campo 'area' y 'confidencial' al payload de los 336,165 vectores
usando set_payload con filtro por 'source' (una llamada API por fuente)
"""
import json, sys, time, urllib.request, re
sys.stdout.reconfigure(encoding='utf-8')

QDRANT = 'http://localhost:6333'
COLLECTION = 'Lifextreme_Knowledge'

# ══════════════════════════════════════════════════════════════
# REGLAS DE CLASIFICACIÓN POR NOMBRE DE FUENTE
# Orden importa: la primera regla que matchea gana
# ══════════════════════════════════════════════════════════════
REGLAS = [
    # ── CONFIDENCIAL (primero, tiene prioridad) ──────────────
    {'area': 'ventas',      'confidencial': True,  'patrones': [
        'FICHA RUC LIFEXTREME', 'ficha ruc final', 'Boleta Venta Lifextreme',
        'Ticket_Lifextreme', 'Reserva Lifextreme',
    ]},

    # ── ÁREA 2 — VENTAS & CRM ────────────────────────────────
    {'area': 'ventas',      'confidencial': False, 'patrones': [
        'tours_faq', 'Chat de WhatsApp', 'chat whatsapp',
        'tarifario', 'Tarifario', 'FAQs_Turisticos', '1_FAQs',
        'Manual_Asesor_Turistico', 'Manual_Ventas', 'Catalogo_Tours',
        'Politicas_Reserva', 'Flujos_Venta', 'Manual_Ventas_Turisticas',
        'Flujos_Conversacionales', '5_Caso_Uso_Tour', 'GLAMPING COYA',
        'PROYECTO GLAMPING', 'FAQs_Agencias',
    ]},

    # ── ÁREA 3 — MARKETING DIGITAL ───────────────────────────
    {'area': 'marketing',   'confidencial': False, 'patrones': [
        'Facebook Ad', 'facebook ad', 'KPIS TURISMO', 'Kpis Turismo',
        'COMPENDIO 2023', 'Estudio_Competencia', 'Guia_Estilo_Chatbot',
        'PITCH DESK TOUR BOT', 'WEB TOUR BOT', 'FLYER',
        'storytelling', 'marketing', 'social images',
    ]},

    # ── ÁREA 4 — OPERACIONES TURÍSTICAS ──────────────────────
    {'area': 'operaciones', 'confidencial': False, 'patrones': [
        'TUPA_', 'GERCETUR_TUPA', 'tupa_', 'Reglamento_', 'Reglamento ',
        'Leyes Turismo', 'leyes turismo', 'RM_Nro', 'RM_N',
        'MINCETUR', 'mincetur', 'Instrumentos de Gestion',
        'GUIA TRABAJOS VERTICALES', 'trabajos verticales',
        'REGLAMENTO MV', 'canotaje', 'Canotaje',
        'Entorno ANP', 'SERNANP', 'sernanp', 'cusco.pdf',
        'manual_de_buenas_practicas', 'GUIA LEGAL ECHECOPAR',
        'SOSTENIBILIDAD', 'Tuo Procedimiento', 'OSINERGMIN',
        'Leyes Turismo', '4.- Entorno', '4_Itinerario',
        'Itinerario_Lifextreme', 'VUELO CUSCO',
    ]},

    # ── ÁREA 5 — FINANZAS & REVENUE ──────────────────────────
    {'area': 'finanzas',    'confidencial': False, 'patrones': [
        'sunat_', 'SUNAT', 'Legal Societario', 'Fiscal, Laboral',
        'Fiscal_Laboral', 'Codigo Civil', 'codigo civil',
        'TASACIONES', 'tasaciones', 'TEXTO UNICO ORDENADO',
        'IGV', 'Proteccion Consumidor', 'Marcas y Datos',
        'INVERSION PRIVADA MEF', 'presupuesto', 'Presupuesto',
        'Modelo_Financiero', 'sunafil', 'SUNAFIL',
        'Tupac Indecopi', 'INDECOPI', 'COSTOS Y PRESUPUESTO',
        'RIESGOS GLOBALES', 'TASACIONES SBS',
        '1.- Legal', '2.- Fiscal', '3.- Proteccion',
        'Capitulo XVI', 'TEXTO ÚNICO', 'Capitulo X',
    ]},

    # ── ÁREA 6 — TECNOLOGÍA & IA ─────────────────────────────
    {'area': 'tecnologia',  'confidencial': False, 'patrones': [
        'TOUR BOT', 'tour bot', 'LIFEXTREME_PLATFORM',
        'Mapa_Integraciones', 'GTmetrix', 'gtmetrix',
        'qdrant-essentials', 'INTELIGENCIA ARTIFICIAL INTEGRADA',
        'Manual_Tecnico', 'Lista_Software', 'Cronograma_Implementacion',
        'Pitch_Inversion', 'PITCH DESK', 'Casos_Uso_Reales',
        'requirements.txt', 'expansion_log', 'PENTUR',
        'Plantillas_PDF', 'Fuentes_Oficiales_LifextremeGPT',
    ]},

    # ── ÁREA 7 — ALIANZAS & B2B ──────────────────────────────
    {'area': 'alianzas',    'confidencial': False, 'patrones': [
        'airbnb', 'Airbnb', 'expedia', 'Expedia',
        'OTAs', 'otas', 'Politicas_Paridad',
        'Manual_Capacitacion_Agencias', 'WORKANA',
        'FEDPE', 'FAQs_Agencias', 'AGORA LATINOAMERICA',
        'COREA PERU', 'B2B', 'b2b', 'partners',
        'Manual_Capacitacion',
    ]},

    # ── ÁREA 1 — CEO & ESTRATEGIA ────────────────────────────
    {'area': 'ceo',         'confidencial': False, 'patrones': [
        'PENTUR 2025', 'Plan_estrategico_tursimo_PERTUR',
        'Plan_estrategico_turismo_PERTUR', 'PERTUR',
        'PENTUR_', 'pentur',
    ]},
]

# TODO lo demás → general (transversal, accesible a todos)
AREA_DEFAULT = 'general'


def clasificar(source):
    src = source or ''
    for regla in REGLAS:
        for patron in regla['patrones']:
            if patron.lower() in src.lower():
                return regla['area'], regla['confidencial']
    return AREA_DEFAULT, False


def set_payload_por_source(source, payload_data):
    """Actualiza payload de TODOS los puntos con ese source en una llamada."""
    body = {
        'payload': payload_data,
        'filter': {
            'must': [{'key': 'source', 'match': {'value': source}}]
        }
    }
    req = urllib.request.Request(
        f'{QDRANT}/collections/{COLLECTION}/points/payload',
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    urllib.request.urlopen(req, timeout=30)


# ══════════════════════════════════════════════════════════════
# MAIN — Cargar inventario y etiquetar
# ══════════════════════════════════════════════════════════════
print('Cargando inventario de Qdrant...')
with open('qdrant_inventory.json', encoding='utf-8') as f:
    inv = json.load(f)

fuentes = inv['fuentes']
total_fuentes = len(fuentes)
print(f'Fuentes a etiquetar: {total_fuentes:,}')
print(f'Vectores totales:    {inv["total_vectores"]:,}')
print()

# Conteo por área
area_stats = {}
total_vectores_etiquetados = 0
errores = 0
start = time.time()

print(f"{'N°':>5} {'FUENTE':50} {'ÁREA':12} {'CONF':5} {'VECS':>6}")
print('-' * 85)

for idx, (source, info) in enumerate(fuentes.items(), 1):
    cnt = info['count']
    area, confidencial = clasificar(source)

    try:
        payload_nuevo = {
            'area': area,
            'confidencial': confidencial,
        }
        set_payload_por_source(source, payload_nuevo)
        total_vectores_etiquetados += cnt
        area_stats[area] = area_stats.get(area, 0) + cnt

        src_display = source.replace('%20', ' ')[:48]
        conf_str = '🔒' if confidencial else ''
        if idx % 50 == 0 or idx <= 10:
            print(f"{idx:>5} {src_display:50} {area:12} {conf_str:5} {cnt:>6,}")

    except Exception as e:
        errores += 1
        if idx <= 20:
            print(f"  ERROR [{source[:40]}]: {e}")

    # Progreso cada 500
    if idx % 500 == 0:
        elapsed = time.time() - start
        rate = idx / elapsed
        eta = (total_fuentes - idx) / rate
        pct = idx / total_fuentes * 100
        print(f"\n  [{idx:>5}/{total_fuentes}] {pct:.1f}% | "
              f"Vecs: {total_vectores_etiquetados:,} | "
              f"ETA: {eta/60:.1f} min\n")

# Etiquetar SIN_SOURCE → general
print("\nEtiquetando SIN_SOURCE → general...")
try:
    body = {
        'payload': {'area': 'general', 'confidencial': False},
        'filter': {
            'must_not': [{'has_id': []}],  # truco para actualizar todos
            'should': [
                {'is_null': {'key': 'source'}},
                {'is_empty': {'key': 'source'}}
            ]
        }
    }
    req = urllib.request.Request(
        f'{QDRANT}/collections/{COLLECTION}/points/payload',
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    urllib.request.urlopen(req, timeout=30)
    print("  SIN_SOURCE → general OK")
except Exception as e:
    print(f"  SIN_SOURCE error: {e}")

# ── RESUMEN FINAL
elapsed = time.time() - start
print()
print('=' * 60)
print('ETIQUETADO COMPLETADO')
print('=' * 60)
print(f'  Fuentes procesadas:  {total_fuentes:,}')
print(f'  Vectores etiquetados: {total_vectores_etiquetados:,}')
print(f'  Errores:             {errores}')
print(f'  Tiempo:              {elapsed/60:.1f} min')
print()
print('DISTRIBUCIÓN POR ÁREA:')
for area, cnt in sorted(area_stats.items(), key=lambda x: -x[1]):
    pct = cnt / inv['total_vectores'] * 100
    print(f'  {area:15s}: {cnt:>8,} vectores  ({pct:.1f}%)')
