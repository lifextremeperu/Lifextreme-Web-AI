"""
ingest_marketing_phd.py — Ingesta del Documento PhD de Marketing Turístico
Colección Qdrant: Marketing_PHD_Knowledge

ESTRATEGIA DE CHUNKING:
  NO usamos chunks de tamaño fijo (eso destruye el contexto semántico).
  Usamos chunking POR PILAR: cada sub-pilar (1.1, 1.2, 2.3...) es 1 chunk completo
  con su análisis magistral + casos corporativos + directivas IF/THEN + fuentes.

  Esto permite que cuando el agente pregunta "¿cómo usar Meta Ads?",
  reciba el chunk completo del Pilar 2.2 con benchmarks, casos y directivas.

METADATOS POR CHUNK:
  - pilar: "2.2"
  - titulo: "META ADS (FACEBOOK/INSTAGRAM)"
  - nivel: "phd" 
  - tiene_directiva: True/False
  - tiene_casos: True/False
  - pais_foco: "peru_latam"
  - categoria: "paid_media" | "neuromarketing" | "legal" | "ia_tools" | etc.

EJECUTAR:
  python ingest_marketing_phd.py

AUTOR: Lifextreme AI Team | v1.0.0
"""

import os
import sys
import asyncio
import uuid
import re
import httpx
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

# ── Dependencias opcionales con fallback graceful ────────────────
try:
    import pdfplumber
    PDF_OK = True
except ImportError:
    PDF_OK = False
    print("[!] pdfplumber no instalado. Instalando...")

try:
    from qdrant_client import AsyncQdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    QDRANT_OK = True
except ImportError:
    QDRANT_OK = False
    print("[!] qdrant-client no instalado.")

# ══════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════
PDF_PATH    = r"C:\Users\ASUS\Downloads\Investigación Marketing Turístico Avanzado LATAM.pdf"
QDRANT_URL  = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_URL  = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"
COLLECTION  = "Marketing_PHD_Knowledge"
VECTOR_DIM  = 768  # nomic-embed-text produce 768 dimensiones

qclient = AsyncQdrantClient(url=QDRANT_URL) if QDRANT_OK else None


# ══════════════════════════════════════════════
# MAPA DE PILARES Y CATEGORÍAS
# ══════════════════════════════════════════════
MAPA_CATEGORIAS = {
    "1.1": "neuromarketing_decision",
    "1.2": "neuromarketing_biometria",
    "1.3": "sesgos_cognitivos",
    "2.1": "estrategia_funnel",
    "2.2": "paid_media_meta",
    "2.3": "paid_media_google_seo",
    "2.4": "paid_media_tiktok",
    "3.1": "revenue_pricing",
    "3.2": "distribucion_otas",
    "3.3": "customer_ltv",
    "4.1": "ecosistema_tecnologico",
    "4.2": "herramientas_ia",
    "4.3": "metaverso_vr",
    "5.1": "marca_pais",
    "5.2": "destinos_estrategia",
    "5.3": "mercados_emisores",
    "6.1": "marco_legal",
    "6.2": "beneficios_fiscales_igv",
    "6.3": "fondos_turismo_emprende",
    "6.4": "areas_protegidas_sernanp",
    "7.1": "analisis_estrategico_porter",
    "7.2": "inteligencia_competitiva",
    "7.3": "megatendencias_2025",
}


# ══════════════════════════════════════════════
# EXTRACCIÓN DE TEXTO POR PILAR (CHUNKING SEMÁNTICO)
# ══════════════════════════════════════════════
def extraer_chunks_por_pilar(pdf_path: str) -> list[dict]:
    """
    Extrae el texto del PDF y lo divide por sub-pilar.
    Cada chunk contiene el análisis completo de 1 sub-pilar.
    """
    if not PDF_OK:
        print("[!] pdfplumber requerido. Instala con: pip install pdfplumber")
        return []

    print(f"[1/4] Leyendo PDF: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        texto_completo = ""
        for page in pdf.pages:
            texto_completo += (page.extract_text() or "") + "\n"

    print(f"      Total caracteres: {len(texto_completo):,}")

    # ── Detectar los delimitadores de cada Pilar ──────────────────
    # Patrón: "PILAR X.Y" (con variaciones de formato del PDF)
    patron_pilar = re.compile(
        r'PILAR\s+(\d+\.\d+)\s*[—–-]*\s*([A-ZÁÉÍÓÚÑ][^\n]{10,80})',
        re.IGNORECASE
    )

    matches = list(patron_pilar.finditer(texto_completo))
    print(f"      Pilares detectados: {len(matches)}")

    chunks = []
    for i, match in enumerate(matches):
        numero_pilar = match.group(1).strip()
        titulo_pilar = match.group(2).strip()
        inicio       = match.start()
        fin          = matches[i + 1].start() if i + 1 < len(matches) else len(texto_completo)

        texto_chunk = texto_completo[inicio:fin].strip()

        # Limpiar artefactos comunes del PDF (saltos de línea múltiples, etc.)
        texto_chunk = re.sub(r'\n{3,}', '\n\n', texto_chunk)
        texto_chunk = re.sub(r'[ \t]{2,}', ' ', texto_chunk)

        # Detectar si tiene directiva IF/THEN y casos corporativos
        tiene_directiva = "SI el cliente" in texto_chunk or "ENTONCES" in texto_chunk
        tiene_casos     = "Caso Perú" in texto_chunk or "Aplicación Corporativa" in texto_chunk
        tiene_fuentes   = "http" in texto_chunk or "DOI" in texto_chunk

        # Extraer hasta 5 fuentes del chunk
        urls = re.findall(r'https?://[^\s\)\]]+', texto_chunk)[:5]

        categoria = MAPA_CATEGORIAS.get(numero_pilar, "general")

        chunk = {
            "pilar":            numero_pilar,
            "titulo":           titulo_pilar,
            "texto":            texto_chunk,
            "categoria":        categoria,
            "tiene_directiva":  tiene_directiva,
            "tiene_casos":      tiene_casos,
            "tiene_fuentes":    tiene_fuentes,
            "fuentes_url":      urls,
            "longitud":         len(texto_chunk),
            "pais_foco":        "peru_latam",
            "nivel_academico":  "phd",
            "documento_origen": "Investigación Marketing Turístico Avanzado LATAM",
            "fecha_ingesta":    datetime.now().isoformat(),
        }
        chunks.append(chunk)

        print(f"      ✓ Pilar {numero_pilar}: {titulo_pilar[:50]} ({len(texto_chunk):,} chars) "
              f"{'[DIRECTIVA]' if tiene_directiva else ''} {'[CASOS]' if tiene_casos else ''}")

    return chunks


# ══════════════════════════════════════════════
# FUNCIÓN DE EMBEDDING
# ══════════════════════════════════════════════
async def obtener_embedding(texto: str) -> list[float]:
    """Genera embedding con nomic-embed-text via Ollama."""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={"model": EMBED_MODEL, "prompt": texto[:4000]}  # límite de contexto
            )
            if res.status_code == 200:
                return res.json().get("embedding", [])
            print(f"   [!] Error embedding HTTP {res.status_code}")
            return []
    except Exception as e:
        print(f"   [!] Error embedding: {e}")
        return []


# ══════════════════════════════════════════════
# CREAR COLECCIÓN EN QDRANT
# ══════════════════════════════════════════════
async def crear_coleccion():
    """Crea la colección Marketing_PHD_Knowledge si no existe."""
    try:
        collections = await qclient.get_collections()
        nombres = [c.name for c in collections.collections]

        if COLLECTION in nombres:
            print(f"[2/4] ✓ Colección '{COLLECTION}' ya existe.")
            # Preguntar si recrear
            count = await qclient.count(collection_name=COLLECTION)
            print(f"      Vectores existentes: {count.count}")
            if count.count > 0:
                respuesta = input(f"\n¿Limpiar la colección y reingestar desde cero? (s/n): ").strip().lower()
                if respuesta == 's':
                    await qclient.delete_collection(COLLECTION)
                    print(f"      [✓] Colección borrada. Recreando...")
                else:
                    print(f"      [→] Manteniendo colección existente. Añadiendo chunks nuevos.")
                    return True
            # Colección existe con 0 puntos — no recrear, solo continuar
            return True
        else:
            print(f"[2/4] Creando colección '{COLLECTION}'...")
            await qclient.create_collection(
                collection_name=COLLECTION,
                vectors_config=VectorParams(
                    size=VECTOR_DIM,
                    distance=Distance.COSINE
                )
            )
            print(f"      [✓] Colección '{COLLECTION}' creada con {VECTOR_DIM} dimensiones (coseno).")
        return True

    except Exception as e:
        print(f"[!] Error creando colección: {e}")
        return False


# ══════════════════════════════════════════════
# INGESTAR CHUNKS EN QDRANT
# ══════════════════════════════════════════════
async def ingestar_chunks(chunks: list[dict]) -> int:
    """Genera embeddings e inserta todos los chunks en Qdrant."""
    print(f"\n[3/4] Ingesta de {len(chunks)} chunks en Qdrant...")
    print(f"      Modelo de embedding: {EMBED_MODEL}")

    puntos_ok = 0
    for i, chunk in enumerate(chunks):
        pilar   = chunk["pilar"]
        titulo  = chunk["titulo"][:60]
        texto   = chunk["texto"]

        print(f"\n   [{i+1}/{len(chunks)}] Pilar {pilar} — {titulo}...")

        # Generar texto para embedding: título + primeras 2000 chars del contenido
        texto_para_embed = f"Pilar {pilar}: {titulo}\n\n{texto[:2500]}"
        vector = await obtener_embedding(texto_para_embed)

        if not vector:
            print(f"      [✗] Sin embedding. Saltando...")
            continue

        # Construir el punto para Qdrant
        punto = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "pilar":             chunk["pilar"],
                "titulo":            chunk["titulo"],
                "text_content":      chunk["texto"],
                "categoria":         chunk["categoria"],
                "tiene_directiva":   chunk["tiene_directiva"],
                "tiene_casos":       chunk["tiene_casos"],
                "fuentes_url":       chunk["fuentes_url"],
                "pais_foco":         chunk["pais_foco"],
                "nivel_academico":   chunk["nivel_academico"],
                "documento_origen":  chunk["documento_origen"],
                "fecha_ingesta":     chunk["fecha_ingesta"],
                "longitud_chars":    chunk["longitud"],
                # Campos estándar para compatibilidad con el agente
                "source":            f"PhD Marketing LATAM — Pilar {chunk['pilar']}",
                "modulo_nombre":     chunk["titulo"],
                "region":            "peru_latam",
            }
        )

        try:
            await qclient.upsert(
                collection_name=COLLECTION,
                points=[punto]
            )
            puntos_ok += 1
            print(f"      [✓] Ingesta OK — {len(vector)} dims | {chunk['longitud']:,} chars")
        except Exception as e:
            print(f"      [✗] Error Qdrant: {e}")

        # Pausa para no saturar Ollama
        await asyncio.sleep(0.5)

    return puntos_ok


# ══════════════════════════════════════════════
# VERIFICACIÓN POST-INGESTA
# ══════════════════════════════════════════════
async def verificar_ingesta():
    """Prueba la colección con 3 consultas representativas."""
    print(f"\n[4/4] Verificando colección con consultas de prueba...")

    consultas_prueba = [
        "¿Cómo usar Meta Ads para turistas extranjeros en Cusco?",
        "¿Cuáles son los beneficios fiscales del IGV para agencias de turismo?",
        "¿Qué herramientas de IA debe usar una agencia turística peruana?",
    ]

    for consulta in consultas_prueba:
        print(f"\n   🔍 Consulta: {consulta[:60]}")
        vector = await obtener_embedding(consulta)
        if not vector:
            continue
        resultados = await qclient.query_points(
            collection_name=COLLECTION,
            query=vector,
            limit=2,
            score_threshold=0.3
        )
        for r in resultados.points:
            pilar     = r.payload.get("pilar", "?")
            titulo    = r.payload.get("titulo", "")[:50]
            score     = round(r.score, 3)
            directiva = "🎯" if r.payload.get("tiene_directiva") else ""
            print(f"   ✓ Pilar {pilar}: {titulo} (score: {score}) {directiva}")


# ══════════════════════════════════════════════
# REPORTE FINAL
# ══════════════════════════════════════════════
async def generar_reporte(chunks: list[dict], puntos_ok: int):
    """Imprime el resumen final de la ingesta."""
    count = await qclient.count(collection_name=COLLECTION)

    print("\n" + "═" * 60)
    print("  📚 INGESTA COMPLETADA — Marketing_PHD_Knowledge")
    print("═" * 60)
    print(f"  Chunks procesados:  {len(chunks)}")
    print(f"  Vectores ingesta:   {puntos_ok}")
    print(f"  Total en Qdrant:    {count.count}")
    print(f"  Colección:          {COLLECTION}")
    print(f"  Embedding:          {EMBED_MODEL} ({VECTOR_DIM} dims)")
    print(f"  Distancia:          Coseno")
    print()
    print("  📊 Resumen por categoría:")

    categorias = {}
    for c in chunks:
        cat = c["categoria"]
        categorias[cat] = categorias.get(cat, 0) + 1
    for cat, n in sorted(categorias.items()):
        print(f"     {cat:<35} {n} chunk(s)")

    print()
    print("  🤖 Agentes que pueden consultar esta colección:")
    print("     • agent_marketing_phd.py  → Asesor de marketing")
    print("     • agent_cfo.py            → Benchmarks de ROI/ROAS")
    print("     • agent_whatsapp_sales.py → Técnicas de cierre")
    print("     • agent_b2b_outreach.py   → Asesoría a PYMES")
    print()
    print("  💡 Uso en código:")
    print('     from backend.src.rag_service import search_knowledge')
    print('     resultados = await search_knowledge(')
    print('         query="Meta Ads turismo Cusco",')
    print('         collection="Marketing_PHD_Knowledge"')
    print('     )')
    print("═" * 60)


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════
async def main():
    print("=" * 60)
    print("  📖 INGESTA — Marketing_PHD_Knowledge")
    print("  Investigación Marketing Turístico Avanzado LATAM")
    print(f"  Qdrant: {QDRANT_URL}")
    print("=" * 60)

    # Verificar dependencias
    if not PDF_OK:
        print("[✗] Instala: pip install pdfplumber")
        return
    if not QDRANT_OK:
        print("[✗] Instala: pip install qdrant-client")
        return
    if not os.path.exists(PDF_PATH):
        print(f"[✗] PDF no encontrado en: {PDF_PATH}")
        return

    # 1. Extraer chunks semánticos
    chunks = extraer_chunks_por_pilar(PDF_PATH)
    if not chunks:
        print("[✗] No se extrajeron chunks del PDF.")
        return

    # 2. Crear colección
    ok = await crear_coleccion()
    if not ok:
        return

    # 3. Ingestar
    puntos_ok = await ingestar_chunks(chunks)

    # 4. Verificar
    await verificar_ingesta()

    # 5. Reporte
    await generar_reporte(chunks, puntos_ok)


if __name__ == "__main__":
    asyncio.run(main())
