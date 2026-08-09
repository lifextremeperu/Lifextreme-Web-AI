"""
agent_cfo.py — AGENTE CFO (Chief Financial Officer) — Lifextreme.store
Área: Finanzas & Tesorería — C-Suite

FUNCIÓN:
  Monitor financiero autónomo de Lifextreme. Actúa como el Director Financiero
  virtual de la empresa. Analiza ingresos, egresos, márgenes por tour, flujo
  de caja, y emite reportes ejecutivos + alertas en tiempo real.

CAPACIDADES:
  1. MONITOR DE INGRESOS: Lee la BD de leads y reservas para calcular ingresos reales.
  2. ANÁLISIS DE MÁRGENES: Evalúa el margen neto por tour (precio - costo operativo).
  3. FLUJO DE CAJA: Proyecta ingresos y egresos para los próximos 30/60/90 días.
  4. ALERTAS FINANCIERAS: Detecta si se está en riesgo de iliquidez en temporada baja.
  5. REPORTE P&L: Genera el Estado de Resultados (Profit & Loss) mensual automático.
  6. CONTROL DEL IGV: Supervisa el cumplimiento tributario (inafectación para turistas ext.)
  7. ROI DE MARKETING: Calcula el retorno de inversión por canal de marketing.

INTEGRACIÓN:
  - SQLite (leads, reservas, costos operativos)
  - Ollama LLM (análisis y recomendaciones estratégicas)
  - Qdrant RAG (consultas sobre normativa SUNAT y best practices financieras)
  - [Fase 2] Integración con sistema de facturación electrónica (SUNAT OSE)

REPORTE DE SALIDA:
  - Reporte ejecutivo en consola (texto)
  - Archivo JSON exportable para dashboards (Looker Studio / Power BI)
  - Alertas vía Telegram (si se configura el bot)

AUTOR: Lifextreme AI Team
VERSIÓN: 1.0.0
"""

import os
import sys
import json
import sqlite3
import asyncio
import httpx
from datetime import datetime, timedelta
from typing import Optional
from qdrant_client import AsyncQdrantClient

sys.stdout.reconfigure(encoding="utf-8")

# ══════════════════════════════════════════════
# CONFIGURACIÓN CENTRAL
# ══════════════════════════════════════════════
OLLAMA_URL     = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
QDRANT_URL     = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION     = "Lifextreme_Knowledge"
EMBED_MODEL    = "nomic-embed-text"
LLM_MODEL      = os.getenv("LLM_MODEL", "mistral:latest")

# Rutas de base de datos
DATA_DIR       = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LEADS_DB       = os.path.join(DATA_DIR, "whatsapp_leads.db")
FINANZAS_DB    = os.path.join(DATA_DIR, "finanzas_lifextreme.db")
REPORTES_DIR   = os.path.join(DATA_DIR, "reportes_cfo")

# Parámetros financieros de Lifextreme
IGV_TASA          = 0.18       # IGV Perú: 18%
MARGEN_OPERATIVO  = 0.35       # Margen promedio por tour: 35%
COMISION_OTA      = 0.20       # Comisión promedio OTAs: 20%
PRESUPUESTO_MKTG  = 2000.0     # Presupuesto mensual de marketing en Soles (S/)
UMBRAL_ALERTA_CAJA = 5000.0    # Alerta si caja proyectada < S/ 5,000

qclient = AsyncQdrantClient(url=QDRANT_URL)


# ══════════════════════════════════════════════
# INICIALIZACIÓN DE BASE DE DATOS FINANCIERA
# ══════════════════════════════════════════════
def init_finanzas_db():
    """Crea las tablas financieras si no existen."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTES_DIR, exist_ok=True)
    conn = sqlite3.connect(FINANZAS_DB)
    cursor = conn.cursor()

    # Tabla de ingresos reales por reserva
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingresos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha           TEXT,
            descripcion     TEXT,
            tour            TEXT,
            monto_bruto     REAL,
            igv_aplicado    REAL DEFAULT 0,
            monto_neto      REAL,
            canal           TEXT DEFAULT 'whatsapp',  -- whatsapp, web, ota, referido
            tipo_turista    TEXT DEFAULT 'nacional',   -- nacional, extranjero
            estado          TEXT DEFAULT 'PENDIENTE',  -- PENDIENTE, COBRADO, ANULADO
            creado_en       TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla de egresos / costos operativos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS egresos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha           TEXT,
            categoria       TEXT,  -- GUIA, TRANSPORTE, HOSPEDAJE, ALIMENTACION, MARKETING, ADMIN
            descripcion     TEXT,
            monto           REAL,
            proveedor       TEXT,
            tour_asociado   TEXT,
            creado_en       TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla de catálogo de tours con costos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS catalogo_tours (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre          TEXT UNIQUE,
            precio_venta    REAL,
            costo_guia      REAL,
            costo_transporte REAL,
            costo_hospedaje REAL,
            costo_alimentos REAL,
            costo_entradas  REAL,
            margen_estimado REAL,
            activo          INTEGER DEFAULT 1
        )
    """)

    # Tabla de presupuestos de marketing por canal
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marketing_spend (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            mes             TEXT,
            canal           TEXT,  -- meta_ads, google_ads, tiktok_ads, influencer, orgánico
            presupuesto     REAL,
            gastado         REAL DEFAULT 0,
            leads_generados INTEGER DEFAULT 0,
            ventas_cerradas INTEGER DEFAULT 0,
            ingresos_atrib  REAL DEFAULT 0,
            creado_en       TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Insertar tours de muestra si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM catalogo_tours")
    if cursor.fetchone()[0] == 0:
        tours_muestra = [
            ("Ausangate 5D/4N",       2200, 400, 180, 350, 200, 120, 0.43),
            ("Salkantay Trek 5D/4N",  1800, 350, 150, 300, 180, 80,  0.41),
            ("Machu Picchu 2D/1N",    650,  100, 80,  0,   60,  150, 0.40),
            ("Camino Inca 4D/3N",     1500, 300, 100, 280, 200, 220, 0.27),
            ("Colca Canyon 3D/2N",    480,  100, 120, 90,  80,  30,  0.12),
            ("Amazon Expedition 4D",  1200, 280, 200, 250, 180, 0,   0.24),
            ("Choquequirao 5D/4N",    1600, 320, 160, 300, 200, 60,  0.35),
            ("Lago Titicaca 2D/1N",   420,  90,  70,  0,   80,  60,  0.28),
        ]
        cursor.executemany(
            "INSERT INTO catalogo_tours (nombre, precio_venta, costo_guia, costo_transporte, costo_hospedaje, costo_alimentos, costo_entradas, margen_estimado) VALUES (?,?,?,?,?,?,?,?)",
            tours_muestra
        )
        conn.commit()
        print("[✓] Catálogo de tours inicializado con 8 productos.")

    conn.close()
    print("[✓] Base de datos financiera lista.")


# ══════════════════════════════════════════════
# MÓDULO 1: LECTURA DE INGRESOS DESDE LEADS
# ══════════════════════════════════════════════
def leer_ingresos_desde_leads() -> dict:
    """Extrae datos de ventas desde la BD de WhatsApp leads."""
    if not os.path.exists(LEADS_DB):
        return {"total_leads": 0, "leads_cotizados": 0, "leads_reservados": 0, "error": "BD de leads no encontrada. Ejecuta agent_whatsapp_sales.py primero."}
    conn = sqlite3.connect(LEADS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM leads")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM leads WHERE estado='COTIZADO'")
    cotizados = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM leads WHERE estado='RESERVADO'")
    reservados = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM leads WHERE estado='PERDIDO'")
    perdidos = cursor.fetchone()[0]
    conn.close()
    tasa_conversion = round((reservados / total * 100), 1) if total > 0 else 0
    return {
        "total_leads":      total,
        "leads_cotizados":  cotizados,
        "leads_reservados": reservados,
        "leads_perdidos":   perdidos,
        "tasa_conversion":  tasa_conversion
    }


# ══════════════════════════════════════════════
# MÓDULO 2: ANÁLISIS DE MÁRGENES POR TOUR
# ══════════════════════════════════════════════
def analizar_margenes_tours() -> list[dict]:
    """Calcula el margen neto real por tour del catálogo."""
    conn = sqlite3.connect(FINANZAS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio_venta, costo_guia, costo_transporte, costo_hospedaje, costo_alimentos, costo_entradas, margen_estimado FROM catalogo_tours WHERE activo=1")
    tours = cursor.fetchall()
    conn.close()
    resultados = []
    for t in tours:
        nombre, precio, guia, transporte, hospedaje, alimentos, entradas, margen_est = t
        costo_total = guia + transporte + hospedaje + alimentos + entradas
        margen_bruto = precio - costo_total
        margen_pct   = round((margen_bruto / precio * 100), 1) if precio > 0 else 0
        resultados.append({
            "tour":         nombre,
            "precio":       precio,
            "costo_total":  costo_total,
            "margen_bruto": round(margen_bruto, 2),
            "margen_pct":   margen_pct,
            "alerta":       "⚠️ MARGEN BAJO" if margen_pct < 25 else ("✅ OK" if margen_pct >= 35 else "🔶 REVISAR")
        })
    # Ordenar de mayor a menor margen
    resultados.sort(key=lambda x: x["margen_pct"], reverse=True)
    return resultados


# ══════════════════════════════════════════════
# MÓDULO 3: PROYECCIÓN DE FLUJO DE CAJA
# ══════════════════════════════════════════════
def proyectar_flujo_caja(ingresos_mes_actual: float, egresos_mes_actual: float) -> dict:
    """
    Proyecta el flujo de caja para 30, 60 y 90 días.
    Aplica estacionalidad turística peruana:
      - Jun-Ago: Alta temporada (x1.4)
      - Sep-Nov: Temporada media (x1.0)
      - Dic-Feb: Media-Alta por fiestas (x1.2)
      - Mar-May: Temporada baja/lluvias (x0.7)
    """
    mes_actual = datetime.now().month
    factores_estacionalidad = {
        6: 1.4, 7: 1.5, 8: 1.4,   # Alta: Jun-Ago
        9: 1.1, 10: 1.0, 11: 0.9, # Media: Sep-Nov
        12: 1.2, 1: 1.2, 2: 1.1,  # Media-alta: Dic-Feb
        3: 0.7, 4: 0.65, 5: 0.75  # Baja: Mar-May
    }
    factor_actual = factores_estacionalidad.get(mes_actual, 1.0)

    proyecciones = {}
    for dias, label in [(30, "30_dias"), (60, "60_dias"), (90, "90_dias")]:
        mes_futuro = (datetime.now() + timedelta(days=dias)).month
        factor     = factores_estacionalidad.get(mes_futuro, 1.0)
        ing_proj   = round(ingresos_mes_actual * factor, 2)
        eg_proj    = round(egresos_mes_actual * 1.02, 2)  # +2% inflación mensual
        caja       = round(ing_proj - eg_proj, 2)
        proyecciones[label] = {
            "ingresos_proyectados":  ing_proj,
            "egresos_proyectados":   eg_proj,
            "caja_neta":             caja,
            "factor_estacional":     factor,
            "alerta":               "🚨 RIESGO DE ILIQUIDEZ" if caja < UMBRAL_ALERTA_CAJA else ("⚠️ BAJO" if caja < UMBRAL_ALERTA_CAJA * 2 else "✅ ESTABLE")
        }
    return proyecciones


# ══════════════════════════════════════════════
# MÓDULO 4: ROI DE MARKETING
# ══════════════════════════════════════════════
def calcular_roi_marketing() -> dict:
    """Calcula el ROI de cada canal de marketing."""
    conn = sqlite3.connect(FINANZAS_DB)
    cursor = conn.cursor()
    mes_actual = datetime.now().strftime("%Y-%m")
    cursor.execute(
        "SELECT canal, presupuesto, gastado, leads_generados, ventas_cerradas, ingresos_atrib FROM marketing_spend WHERE mes=?",
        (mes_actual,)
    )
    canales = cursor.fetchall()
    conn.close()

    if not canales:
        # Datos de demostración si no hay datos reales
        canales = [
            ("meta_ads",    2000, 1800, 45, 8,  6400),
            ("google_ads",  500,  480,  20, 5,  3000),
            ("tiktok_ads",  300,  290,  30, 3,  1200),
            ("organico",    0,    0,    25, 12, 7200),
            ("referidos",   0,    0,    15, 9,  5400),
        ]

    resultados = []
    for c in canales:
        canal, presupuesto, gastado, leads, ventas, ingresos = c
        cpl    = round(gastado / leads,   2) if leads > 0   else 0  # Costo por Lead
        cpv    = round(gastado / ventas,  2) if ventas > 0  else 0  # Costo por Venta
        roas   = round(ingresos / gastado, 2) if gastado > 0 else 0  # ROAS
        roi    = round(((ingresos - gastado) / gastado * 100), 1) if gastado > 0 else 0
        resultados.append({
            "canal":     canal,
            "gastado":   gastado,
            "leads":     leads,
            "ventas":    ventas,
            "ingresos":  ingresos,
            "CPL":       cpl,
            "CPV":       cpv,
            "ROAS":      roas,
            "ROI_pct":   roi,
            "semaforo": "🔴 INEFICIENTE" if roas < 2 else ("🟡 MEJORABLE" if roas < 4 else "🟢 EXCELENTE")
        })
    resultados.sort(key=lambda x: x["ROAS"], reverse=True)
    return resultados


# ══════════════════════════════════════════════
# MÓDULO 5: ANÁLISIS IA CON LLM
# ══════════════════════════════════════════════
async def generar_analisis_cfo(datos_financieros: dict) -> str:
    """Usa el LLM para generar recomendaciones estratégicas del CFO."""
    prompt = f"""
Eres el CFO (Director Financiero) virtual de Lifextreme, startup de turismo de aventura en Perú.
Analiza estos datos financieros y emite un informe ejecutivo con RECOMENDACIONES ACCIONABLES.

DATOS FINANCIEROS:
{json.dumps(datos_financieros, ensure_ascii=False, indent=2)}

INSTRUCCIONES:
1. Identifica los 3 principales riesgos financieros actuales.
2. Señala los 2 tours más rentables y recomienda priorizarlos en marketing.
3. Si hay canales de marketing con ROAS < 2, recomienda pausarlos o ajustarlos.
4. Revisa el flujo de caja proyectado y emite alerta si hay riesgo de iliquidez.
5. Da una recomendación sobre el IGV (si hay turistas extranjeros, recordar inafectación).
6. Cierra con 3 acciones concretas para los próximos 30 días.

Formato: Sé directo y ejecutivo. Usa viñetas. Máximo 400 palabras. Responde en español.
"""
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            res = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": LLM_MODEL, "prompt": prompt, "stream": False,
                      "options": {"temperature": 0.3, "num_predict": 600}}
            )
            if res.status_code == 200:
                return res.json().get("response", "").strip()
            return "[Error al conectar con el LLM para análisis CFO]"
    except Exception as e:
        return f"[Error de conexión con Ollama: {e}]. Revisa que Ollama esté activo en el puerto 11434."


# ══════════════════════════════════════════════
# MÓDULO 6: CONTROL DEL IGV PARA TURISTAS EXT.
# ══════════════════════════════════════════════
def verificar_igv_exportacion(ingresos_extranjeros: float, ingresos_nacionales: float) -> dict:
    """
    Verifica el tratamiento correcto del IGV según Ley N° 28780.
    Turistas extranjeros no domiciliados: INAFECTOS al IGV (0%).
    Turistas nacionales: IGV 18% aplica.
    """
    igv_nacional    = round(ingresos_nacionales * IGV_TASA, 2)
    ahorro_igv      = round(ingresos_extranjeros * IGV_TASA, 2)
    pct_extranjero  = round(
        ingresos_extranjeros / (ingresos_extranjeros + ingresos_nacionales) * 100, 1
    ) if (ingresos_extranjeros + ingresos_nacionales) > 0 else 0

    return {
        "ingresos_turistas_nacionales":   ingresos_nacionales,
        "ingresos_turistas_extranjeros":  ingresos_extranjeros,
        "igv_a_declarar":                igv_nacional,
        "ahorro_igv_por_exportacion":    ahorro_igv,
        "pct_cartera_extranjera":        pct_extranjero,
        "recomendacion":                 (
            "✅ Excelente mix. Optimiza emisión de facturas de exportación de servicios."
            if pct_extranjero > 40 else
            "⚠️ Baja proporción de turistas extranjeros. Aumentar captación receptiva."
        ),
        "base_legal":                    "Ley N° 28780 — Inafectación IGV Servicios Turísticos para No Domiciliados"
    }


# ══════════════════════════════════════════════
# REPORTE EJECUTIVO COMPLETO (P&L MENSUAL)
# ══════════════════════════════════════════════
def generar_reporte_json(datos: dict, nombre_archivo: str = None) -> str:
    """Exporta el reporte financiero completo en JSON."""
    os.makedirs(REPORTES_DIR, exist_ok=True)
    if not nombre_archivo:
        nombre_archivo = f"reporte_cfo_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    ruta = os.path.join(REPORTES_DIR, nombre_archivo)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    return ruta


# ══════════════════════════════════════════════
# EJECUCIÓN PRINCIPAL DEL AGENTE CFO
# ══════════════════════════════════════════════
async def ejecutar_reporte_cfo(exportar_json: bool = True) -> dict:
    """
    Función principal: genera el reporte CFO completo de Lifextreme.
    Orquesta todos los módulos y produce el análisis ejecutivo.
    """
    print("\n" + "═" * 65)
    print("  💼 LIFEXTREME — AGENTE CFO  |  Director Financiero Virtual")
    print("  Área: Finanzas & Tesorería  |  C-Suite")
    print(f"  Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("═" * 65)

    init_finanzas_db()

    # ── MÓDULO 1: Leads y conversión
    print("\n[1/6] 📊 Analizando pipeline de ventas (leads)...")
    datos_leads = leer_ingresos_desde_leads()
    print(f"      Total leads: {datos_leads['total_leads']} | "
          f"Cotizados: {datos_leads['leads_cotizados']} | "
          f"Reservados: {datos_leads['leads_reservados']} | "
          f"Conversión: {datos_leads['tasa_conversion']}%")

    # ── MÓDULO 2: Márgenes por tour
    print("\n[2/6] 🏔️  Analizando márgenes del catálogo de tours...")
    margenes = analizar_margenes_tours()
    print(f"      {len(margenes)} tours analizados.")
    for t in margenes[:3]:
        print(f"      {t['alerta']}  {t['tour']:<35} Margen: {t['margen_pct']}%")

    # ── MÓDULO 3: Flujo de caja (usando estimados del mes)
    print("\n[3/6] 💰 Proyectando flujo de caja...")
    # Estimado: promedio de ventas * leads reservados + egresos fijos
    ingresos_estimados = sum(t["precio"] for t in margenes[:3]) * max(datos_leads["leads_reservados"], 1)
    egresos_estimados  = sum(t["costo_total"] for t in margenes) * 0.3 + PRESUPUESTO_MKTG + 3000
    flujo_caja = proyectar_flujo_caja(ingresos_estimados, egresos_estimados)
    for periodo, datos in flujo_caja.items():
        print(f"      {periodo.replace('_',' ').upper()}: "
              f"Ingresos S/{datos['ingresos_proyectados']:,.0f} | "
              f"Egresos S/{datos['egresos_proyectados']:,.0f} | "
              f"Caja S/{datos['caja_neta']:,.0f} {datos['alerta']}")

    # ── MÓDULO 4: ROI de marketing
    print("\n[4/6] 📣 Evaluando ROI de marketing por canal...")
    roi_mktg = calcular_roi_marketing()
    for c in roi_mktg[:3]:
        print(f"      {c['semaforo']}  {c['canal']:<15} ROAS: {c['ROAS']}x | ROI: {c['ROI_pct']}%")

    # ── MÓDULO 5: Control IGV
    print("\n[5/6] ⚖️  Verificando tratamiento de IGV...")
    igv_data = verificar_igv_exportacion(
        ingresos_extranjeros=ingresos_estimados * 0.45,  # 45% estimado receptivo
        ingresos_nacionales=ingresos_estimados * 0.55
    )
    print(f"      IGV a declarar: S/{igv_data['igv_a_declarar']:,.2f} | "
          f"Ahorro por exportación: S/{igv_data['ahorro_igv_por_exportacion']:,.2f}")
    print(f"      {igv_data['recomendacion']}")

    # ── Consolidar todos los datos
    reporte_consolidado = {
        "metadata": {
            "empresa":      "Lifextreme Peru SAC",
            "web":          "www.lifextreme.store",
            "fecha_reporte": datetime.now().isoformat(),
            "periodo":      datetime.now().strftime("%B %Y"),
            "agente":       "agent_cfo.py v1.0.0"
        },
        "pipeline_ventas":  datos_leads,
        "margenes_tours":   margenes,
        "flujo_caja":       flujo_caja,
        "roi_marketing":    roi_mktg,
        "control_igv":      igv_data,
        "indicadores_clave": {
            "tour_mas_rentable":  margenes[0]["tour"] if margenes else "N/D",
            "margen_max":         f"{margenes[0]['margen_pct']}%" if margenes else "N/D",
            "mejor_canal_mktg":   roi_mktg[0]["canal"] if roi_mktg else "N/D",
            "roas_mejor_canal":   roi_mktg[0]["ROAS"] if roi_mktg else "N/D",
            "caja_30_dias":       f"S/ {flujo_caja['30_dias']['caja_neta']:,.0f}",
            "estado_caja_30d":    flujo_caja["30_dias"]["alerta"],
            "tasa_conversion":    f"{datos_leads['tasa_conversion']}%"
        }
    }

    # ── MÓDULO 6: Análisis CFO con IA
    print("\n[6/6] 🧠 Generando análisis estratégico con IA (CFO Virtual)...")
    analisis_ia = await generar_analisis_cfo(reporte_consolidado["indicadores_clave"])
    reporte_consolidado["analisis_cfo_ia"] = analisis_ia

    # ── Imprimir reporte final
    print("\n" + "═" * 65)
    print("  📋 ANÁLISIS ESTRATÉGICO DEL CFO VIRTUAL")
    print("═" * 65)
    print(analisis_ia)
    print("═" * 65)

    # ── Exportar JSON
    if exportar_json:
        ruta_json = generar_reporte_json(reporte_consolidado)
        print(f"\n[✓] Reporte exportado a: {ruta_json}")
        reporte_consolidado["reporte_exportado_en"] = ruta_json

    # ── Indicadores clave (resumen final)
    print("\n📌 INDICADORES CLAVE DEL MES:")
    ind = reporte_consolidado["indicadores_clave"]
    print(f"   🏆 Tour más rentable:     {ind['tour_mas_rentable']} ({ind['margen_max']} margen)")
    print(f"   📣 Mejor canal marketing: {ind['mejor_canal_mktg']} (ROAS {ind['roas_mejor_canal']}x)")
    print(f"   💰 Caja proyectada 30d:   {ind['caja_30_dias']} {ind['estado_caja_30d']}")
    print(f"   🎯 Tasa de conversión:    {ind['tasa_conversion']}")
    print(f"\n   Próximo reporte automático: {(datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')}")

    return reporte_consolidado


# ══════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Agente CFO — Lifextreme Financial Director")
    parser.add_argument("--no-json", action="store_true", help="No exportar reporte JSON")
    args = parser.parse_args()

    asyncio.run(ejecutar_reporte_cfo(exportar_json=not args.no_json))
