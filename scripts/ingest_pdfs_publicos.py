"""
Ingesta de 20 PDFs públicos (normativa, seguridad de aventura, sostenibilidad,
mercado y marketing) en Lifextreme_Knowledge.

Uso:
    python -P scripts/ingest_pdfs_publicos.py --descargar      # baja los PDFs que falten
    python -P scripts/ingest_pdfs_publicos.py --seco           # extrae y trocea, sin tocar Qdrant
    python -P scripts/ingest_pdfs_publicos.py                  # ingesta real
    python -P scripts/ingest_pdfs_publicos.py --solo 1,8,9     # solo algunos documentos

Todos los puntos llevan payload "lote" = LOTE, así que se pueden borrar juntos.
Los IDs son deterministas (uuid5 de url + índice), así que re-ejecutar reemplaza, no duplica.
"""
import argparse
import asyncio
import bisect
import hashlib
import json
import os
import re
import uuid
from datetime import datetime

import fitz  # PyMuPDF
import httpx
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import FieldCondition, Filter, FilterSelector, MatchValue, PointStruct

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(BASE_DIR, "data", "pdfs_publicos")
REPORTE = os.path.join(PDF_DIR, "_reporte_ingesta.json")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"  # mismo modelo y endpoint que backend/src/rag_service.py
COLLECTION = "Lifextreme_Knowledge"
LOTE = "pdfs_publicos_2026-10-30"

CHUNK_SIZE = 1000      # mediana actual de la colección ~1023 caracteres
CHUNK_OVERLAP = 150
MIN_CHARS = 80         # fragmentos más cortos son ruido (números de página, encabezados)
MAX_PDF_BYTES = 60 * 1024 * 1024
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

# area: b2c lee ventas/operaciones/general; b2b lee finanzas/ceo/alianzas/marketing/tecnologia/operaciones
# tier: 1 = norma oficial peruana (boost 1.15 en rag_service), 2 = referencia
# modulo_nombre llega al LLM en el contexto, por eso incluye avisos de vigencia.
DOCS = [
    {"n": 1, "url": "https://cdn.www.gob.pe/uploads/document/file/10858668/8760616-r-m-n-392-2026-proyecto-ds.pdf",
     "filename": "MINCETUR_Proyecto_Reglamento_Turismo_Aventura_2026.pdf",
     "titulo": "Proyecto de Decreto Supremo que aprueba el Reglamento de Turismo de Aventura (RM 392-2026-MINCETUR)",
     "modulo_nombre": "PROYECTO NO VIGENTE - Reglamento de Turismo de Aventura 2026 (rige D.S. 005-2016-MINCETUR)",
     "entidad_emisora": "MINCETUR", "nivel_legal": "Proyecto de Decreto Supremo", "estado": "Proyecto en consulta",
     "jurisdiccion": "Nacional", "categoria": "seguridad_aventura", "area": "operaciones", "region": "peru", "tier": 1, "idioma": "es"},
    {"n": 2, "url": "https://cdn.www.gob.pe/uploads/document/file/6771364/4251894-guia_turismo_de_aventura-3.pdf",
     "filename": "MINCETUR_Guia_Tecnica_Lugares_Turismo_Aventura_2024.pdf",
     "titulo": "Identificación y autorización de los lugares para el desarrollo de las modalidades de turismo de aventura - Guía técnica para gobiernos regionales (MINCETUR, 2024)",
     "modulo_nombre": "Guía técnica MINCETUR - Lugares y modalidades de turismo de aventura (2024)",
     "entidad_emisora": "MINCETUR", "nivel_legal": "Guía técnica", "estado": "Vigente",
     "jurisdiccion": "Nacional", "categoria": "seguridad_aventura", "area": "operaciones", "region": "peru", "tier": 1, "idioma": "es"},
    {"n": 3, "url": "https://cdn.adventuretravel.biz/wp-content/uploads/2021/01/ATGS-2021.pdf",
     "filename": "ATTA_Adventure_Travel_Guide_Standard_2021.pdf",
     "titulo": "Adventure Travel Guide Standard (ATTA, 2021)",
     "modulo_nombre": "Estándar internacional de guías de aventura - ATTA 2021",
     "entidad_emisora": "Adventure Travel Trade Association", "nivel_legal": "Estándar voluntario", "estado": "Referencia",
     "jurisdiccion": "Internacional", "categoria": "seguridad_aventura", "area": "operaciones", "region": "global", "tier": 2, "idioma": "en"},
    {"n": 4, "url": "https://www.supportadventure.co.nz/assets/ccc96fda7a/Audit-Team-Good-Practice-Guide.pdf",
     "filename": "SupportAdventure_NZ_Good_Practice_Adventure_Activities.pdf",
     "titulo": "Good Practice for Adventure Activities (SupportAdventure, Nueva Zelanda)",
     "modulo_nombre": "Buenas prácticas de seguridad en actividades de aventura - SupportAdventure NZ",
     "entidad_emisora": "SupportAdventure (Nueva Zelanda)", "nivel_legal": "Guía de buenas prácticas", "estado": "Referencia",
     "jurisdiccion": "Internacional", "categoria": "seguridad_aventura", "area": "operaciones", "region": "global", "tier": 2, "idioma": "en"},
    {"n": 5, "url": "https://www.aafp.org/pubs/afp/issues/2020/0415/p505.pdf",
     "filename": "AAFP_2020_Mal_de_Altura_Guias_WMS.pdf",
     "titulo": "Acute Altitude Illness: Updated Prevention and Treatment Guidelines from the Wilderness Medical Society (AAFP, 2020)",
     "modulo_nombre": "Mal de altura: prevención y tratamiento - guías Wilderness Medical Society (AAFP 2020)",
     "entidad_emisora": "American Academy of Family Physicians / Wilderness Medical Society", "nivel_legal": "Guía clínica", "estado": "Referencia",
     "jurisdiccion": "Internacional", "categoria": "seguridad_aventura", "area": "operaciones", "region": "global", "tier": 2, "idioma": "en"},
    {"n": 6, "url": "https://img.lpderecho.pe/wp-content/uploads/2020/05/DS-5-2020-mincetur-LP.pdf",
     "filename": "DS_005-2020-MINCETUR_Reglamento_Agencias_Viajes.pdf",
     "titulo": "Decreto Supremo 005-2020-MINCETUR - Reglamento de Agencias de Viajes y Turismo",
     "modulo_nombre": "D.S. 005-2020-MINCETUR - Reglamento de Agencias de Viajes y Turismo",
     "entidad_emisora": "MINCETUR", "nivel_legal": "Decreto Supremo", "estado": "Vigente",
     "jurisdiccion": "Nacional", "categoria": "normativa", "area": "operaciones", "region": "peru", "tier": 1, "idioma": "es"},
    {"n": 7, "url": "https://leyes.congreso.gob.pe/Documentos/2021_2026/ADLP/Texto_Consolidado/31614-TXM.pdf",
     "filename": "Ley_31614_Trabajador_Porteador.pdf",
     "titulo": "Ley 31614 - Nueva Ley del Trabajador Porteador (texto consolidado)",
     "modulo_nombre": "Ley 31614 - Trabajador Porteador (texto consolidado, incl. Ley 32137)",
     "entidad_emisora": "Congreso de la República", "nivel_legal": "Ley", "estado": "Vigente",
     "jurisdiccion": "Nacional", "categoria": "normativa", "area": "operaciones", "region": "peru", "tier": 1, "idioma": "es"},
    {"n": 8, "url": "https://faolex.fao.org/docs/pdf/per167816anx.pdf",
     "filename": "RM_069-2017-MC_Reglamento_Red_Caminos_Inka.pdf",
     "titulo": "Reglamento de Uso Turístico Sostenible de la Red de Caminos Inka del Santuario Histórico de Machupicchu (RM 069-2017-MC)",
     "modulo_nombre": "Reglamento Red de Caminos Inka (RM 069-2017-MC; modificado por RM 294-2025-MC y RM 333-2026-MC)",
     "entidad_emisora": "Ministerio de Cultura / SERNANP", "nivel_legal": "Resolución Ministerial", "estado": "Vigente con modificaciones",
     "jurisdiccion": "Santuario Histórico de Machupicchu", "categoria": "normativa", "area": "operaciones", "region": "cusco", "tier": 1, "idioma": "es"},
    {"n": 9, "url": "https://machupicchu.gob.pe/wp-content/uploads/2024/05/1-8A-RM-528-2023-MC.pdf",
     "filename": "RM_528-2023-MC_Circuitos_Machu_Picchu.pdf",
     "titulo": "Resolución Ministerial 528-2023-MC - Circuitos y rutas de visita a la Llaqta de Machupicchu",
     "modulo_nombre": "RM 528-2023-MC - Circuitos de Machu Picchu (aforos 2026 en RM 285-2025-MC)",
     "entidad_emisora": "Ministerio de Cultura", "nivel_legal": "Resolución Ministerial", "estado": "Vigente con modificaciones",
     "jurisdiccion": "Santuario Histórico de Machupicchu", "categoria": "normativa", "area": "operaciones", "region": "cusco", "tier": 1, "idioma": "es"},
    {"n": 10, "url": "https://sinia.minam.gob.pe/sites/default/files/sial-sialtrujillo/archivos/public/docs/371.pdf",
     "filename": "DS_018-2009-MINAM_Reglamento_Uso_Turistico_ANP.pdf",
     "titulo": "Decreto Supremo 018-2009-MINAM - Reglamento de Uso Turístico en Áreas Naturales Protegidas",
     "modulo_nombre": "D.S. 018-2009-MINAM - Uso turístico en Áreas Naturales Protegidas (SERNANP)",
     "entidad_emisora": "MINAM", "nivel_legal": "Decreto Supremo", "estado": "Vigente",
     "jurisdiccion": "Nacional", "categoria": "normativa", "area": "operaciones", "region": "peru", "tier": 1, "idioma": "es"},
    {"n": 11, "url": "https://cdn.www.gob.pe/uploads/document/file/7756037/6554453-reglamento-de-la-ley-n-29733.pdf",
     "filename": "DS_016-2024-JUS_Reglamento_Proteccion_Datos_Personales.pdf",
     "titulo": "Decreto Supremo 016-2024-JUS - Reglamento de la Ley 29733, Ley de Protección de Datos Personales",
     "modulo_nombre": "D.S. 016-2024-JUS - Reglamento de Protección de Datos Personales (vigente desde 31/03/2025)",
     "entidad_emisora": "Ministerio de Justicia y Derechos Humanos", "nivel_legal": "Decreto Supremo", "estado": "Vigente",
     "jurisdiccion": "Nacional", "categoria": "normativa", "area": "tecnologia", "region": "peru", "tier": 1, "idioma": "es"},
    {"n": 12, "url": "https://www.gstc.org/wp-content/uploads/GSTC-Industry-Criteria-with-tour-opertaors-indicators-and-sdgs_Dec2016_Spanish-Espanol.pdf",
     "filename": "GSTC_Criterios_Operadores_Turisticos_v3_ES.pdf",
     "titulo": "Criterios GSTC para la Industria con indicadores para operadores turísticos (versión 3, 2016)",
     "modulo_nombre": "Criterios GSTC de turismo sostenible para operadores turísticos",
     "entidad_emisora": "Global Sustainable Tourism Council", "nivel_legal": "Estándar voluntario", "estado": "Referencia",
     "jurisdiccion": "Internacional", "categoria": "sostenibilidad", "area": "operaciones", "region": "global", "tier": 2, "idioma": "es"},
    {"n": 13, "url": "https://www.gstc.org/wp-content/uploads/Guia-para-Operadores-Turisticos-sobre-como-obtener-la-Certificacion.pdf",
     "filename": "GSTC_Guia_Certificacion_Operadores_ES.pdf",
     "titulo": "Guía para operadores turísticos sobre cómo obtener la certificación (GSTC)",
     "modulo_nombre": "Guía GSTC - Cómo certificar a un operador turístico en sostenibilidad",
     "entidad_emisora": "Global Sustainable Tourism Council", "nivel_legal": "Guía", "estado": "Referencia",
     "jurisdiccion": "Internacional", "categoria": "sostenibilidad", "area": "alianzas", "region": "global", "tier": 2, "idioma": "es"},
    {"n": 14, "url": "https://www.helvetas.org/Publications-PDFs/Latin-America/Peru/SeCompetitivo/BuenasPracticas_TurimosNaturaleza_AGENCIASOPERADORES.pdf",
     "filename": "Helvetas_Buenas_Practicas_Turismo_Naturaleza_Agencias_Operadores.pdf",
     "titulo": "Buenas prácticas para el turismo de naturaleza - Agencias y operadores (Helvetas Perú)",
     "modulo_nombre": "Buenas prácticas de turismo de naturaleza para agencias y operadores - Helvetas Perú",
     "entidad_emisora": "Helvetas Perú", "nivel_legal": "Manual", "estado": "Referencia",
     "jurisdiccion": "Nacional", "categoria": "sostenibilidad", "area": "operaciones", "region": "peru", "tier": 2, "idioma": "es"},
    {"n": 15, "url": "https://www.codespa.org/app/uploads/manual-buenas-practicas-turismo-rural-comunitario.pdf",
     "filename": "CODESPA_Manual_Buenas_Practicas_Turismo_Rural_Comunitario.pdf",
     "titulo": "Manual de buenas prácticas de turismo rural comunitario (Fundación CODESPA)",
     "modulo_nombre": "Manual de buenas prácticas de turismo rural comunitario - CODESPA",
     "entidad_emisora": "Fundación CODESPA", "nivel_legal": "Manual", "estado": "Referencia",
     "jurisdiccion": "Internacional", "categoria": "sostenibilidad", "area": "alianzas", "region": "global", "tier": 2, "idioma": "es"},
    {"n": 16, "url": "https://www.promperu.gob.pe/TurismoIn/archivos/ReportesPdf/PERFIL%20DEL%20VACACIONISTA%20EXTRANJERO%20DE%20AVENTURA.pdf",
     "filename": "PromPeru_Perfil_Vacacionista_Extranjero_Aventura.pdf",
     "titulo": "Perfil del vacacionista extranjero de aventura (PromPerú, datos 2019)",
     "modulo_nombre": "PromPerú - Perfil del vacacionista extranjero de aventura",
     "entidad_emisora": "PromPerú", "nivel_legal": "Estudio de mercado", "estado": "Referencia",
     "jurisdiccion": "Nacional", "categoria": "mercado", "area": "marketing", "region": "peru", "tier": 2, "idioma": "es"},
    {"n": 17, "url": "https://www.promperu.gob.pe/TurismoIn/archivos/ReportesPdf/PERFIL%20DEL%20VACACIONISTA%20DE%20NATURALEZA.pdf",
     "filename": "PromPeru_Perfil_Vacacionista_Naturaleza.pdf",
     "titulo": "Perfil del vacacionista de naturaleza (PromPerú)",
     "modulo_nombre": "PromPerú - Perfil del vacacionista de naturaleza",
     "entidad_emisora": "PromPerú", "nivel_legal": "Estudio de mercado", "estado": "Referencia",
     "jurisdiccion": "Nacional", "categoria": "mercado", "area": "marketing", "region": "peru", "tier": 2, "idioma": "es"},
    {"n": 18, "url": "https://www.promperu.gob.pe/TurismoIn/archivos/ReportesPdf/2025-10%20El%20viaje%20del%20peruano_PROMPER%C3%9A.pdf",
     "filename": "PromPeru_El_Viaje_del_Peruano_2025-10.pdf",
     "titulo": "El viaje del peruano (PromPerú, octubre 2025)",
     "modulo_nombre": "PromPerú - El viaje del peruano: vacacionista nacional (oct. 2025)",
     "entidad_emisora": "PromPerú", "nivel_legal": "Estudio de mercado", "estado": "Referencia",
     "jurisdiccion": "Nacional", "categoria": "mercado", "area": "marketing", "region": "peru", "tier": 2, "idioma": "es"},
    {"n": 19, "url": "https://unwto-ap.org/cms/wp-content/uploads/2026/06/International-Tourism-Highlights-2025.pdf",
     "filename": "UNTourism_International_Tourism_Highlights_2025.pdf",
     "titulo": "International Tourism Highlights, 2025 Edition (ONU Turismo)",
     "modulo_nombre": "ONU Turismo - International Tourism Highlights 2025 (datos 2024)",
     "entidad_emisora": "ONU Turismo", "nivel_legal": "Informe estadístico", "estado": "Referencia",
     "jurisdiccion": "Internacional", "categoria": "mercado", "area": "marketing", "region": "global", "tier": 2, "idioma": "en"},
    {"n": 20, "url": "https://www.promperu.gob.pe/TurismoIn/archivos/CapacitacionesPdf/Lineamientos%20para%20un%20plan%20de%20marketing%20turistico%20de%20destinos.pdf",
     "filename": "PromPeru_Lineamientos_Plan_Marketing_Turistico.pdf",
     "titulo": "Lineamientos para un plan de marketing turístico de destinos (PromPerú)",
     "modulo_nombre": "PromPerú - Lineamientos para un plan de marketing turístico",
     "entidad_emisora": "PromPerú", "nivel_legal": "Guía", "estado": "Referencia",
     "jurisdiccion": "Nacional", "categoria": "marketing", "area": "marketing", "region": "peru", "tier": 2, "idioma": "es"},
]


# ---------------------------------------------------------------- descarga
async def descargar(doc: dict, client: httpx.AsyncClient) -> str:
    destino = os.path.join(PDF_DIR, doc["filename"])
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        return "ya existe"
    tmp = destino + ".part"
    size = 0
    async with client.stream("GET", doc["url"], headers={"User-Agent": UA}, follow_redirects=True, timeout=180.0) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            async for block in r.aiter_bytes():
                if size == 0 and not block.startswith(b"%PDF"):
                    raise ValueError("la respuesta no es un PDF")
                size += len(block)
                if size > MAX_PDF_BYTES:
                    raise ValueError("supera el tamaño máximo")
                f.write(block)
    os.replace(tmp, destino)
    return f"{size / 1_048_576:.1f} MB"


# ---------------------------------------------------------------- extracción y troceado
def limpiar(texto: str) -> str:
    texto = texto.replace("\x00", "").replace("­", "")
    texto = re.sub(r"(\w)-\n(\w)", r"\1\2", texto)       # palabras cortadas con guion al final de línea
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r" *\n *", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def _unidades(texto: str, inicio: int, seps: list[str]) -> list[tuple[int, str]]:
    """Parte el texto en piezas contiguas <= CHUNK_SIZE, cortando primero por párrafo, luego línea, frase y palabra."""
    if len(texto) <= CHUNK_SIZE:
        return [(inicio, texto)]
    if not seps:
        return [(inicio + i, texto[i:i + CHUNK_SIZE]) for i in range(0, len(texto), CHUNK_SIZE)]
    sep, resto = seps[0], seps[1:]
    out, pos = [], 0
    while pos < len(texto):
        k = texto.find(sep, pos)
        fin = len(texto) if k == -1 else k + len(sep)
        out.extend(_unidades(texto[pos:fin], inicio + pos, resto))
        pos = fin
    return out


def trocear(texto: str) -> list[tuple[int, str]]:
    """Agrupa las piezas en fragmentos de hasta CHUNK_SIZE con ~CHUNK_OVERLAP de solape. Devuelve (offset, texto) en orden."""
    unidades = _unidades(texto, 0, ["\n\n", "\n", ". ", " "])
    chunks, i = [], 0
    while i < len(unidades):
        inicio, j, largo = unidades[i][0], i, 0
        while j < len(unidades) and (j == i or largo + len(unidades[j][1]) <= CHUNK_SIZE):
            largo += len(unidades[j][1])
            j += 1
        chunks.append((inicio, texto[inicio:inicio + largo]))
        if j >= len(unidades):
            break
        k, cola = j, 0
        while k - 1 > i and cola + len(unidades[k - 1][1]) <= CHUNK_OVERLAP:
            k -= 1
            cola += len(unidades[k][1])
        i = k
    return chunks


def extraer_y_trocear(doc: dict) -> dict:
    ruta = os.path.join(PDF_DIR, doc["filename"])
    paginas = []
    with fitz.open(ruta) as pdf:
        n_paginas = pdf.page_count
        for page in pdf:
            paginas.append(limpiar(page.get_text("text")))

    # Texto completo con el desplazamiento de inicio de cada página, para saber la página de cada fragmento
    inicios, partes, pos = [], [], 0
    for p in paginas:
        inicios.append(pos)
        partes.append(p)
        pos += len(p) + 2
    completo = "\n\n".join(partes)

    stats = {"paginas": n_paginas, "caracteres": len(completo), "fragmentos": 0, "cortos": 0, "duplicados": 0}
    stats["paginas_sin_texto"] = sum(1 for p in paginas if len(p) < 50)
    if len(completo) < 200 or stats["paginas_sin_texto"] > n_paginas * 0.6:
        stats["aviso"] = "PDF escaneado o sin capa de texto: requiere OCR"
        return {"stats": stats, "chunks": []}

    vistos, chunks = set(), []
    for offset, txt in trocear(completo):
        txt = txt.strip()
        if len(txt) < MIN_CHARS:
            stats["cortos"] += 1
            continue
        h = hashlib.md5(re.sub(r"\s+", " ", txt.lower()).encode()).hexdigest()
        if h in vistos:
            stats["duplicados"] += 1
            continue
        vistos.add(h)
        pagina = bisect.bisect_right(inicios, offset)
        chunks.append({"text": txt, "page": pagina})
    stats["fragmentos"] = len(chunks)
    return {"stats": stats, "chunks": chunks}


# ---------------------------------------------------------------- embeddings e ingesta
async def get_embedding(text: str, client: httpx.AsyncClient) -> list[float]:
    for intento in range(3):
        try:
            r = await client.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={"model": EMBED_MODEL, "prompt": text, "keep_alive": -1},
                timeout=120.0,
            )
            r.raise_for_status()
            return r.json()["embedding"]
        except Exception as e:
            if intento == 2:
                raise
            print(f"   reintento embedding ({e})")
            await asyncio.sleep(2 * (intento + 1))


async def ingestar(doc: dict, chunks: list[dict], qdrant: AsyncQdrantClient, http: httpx.AsyncClient, sem: asyncio.Semaphore) -> int:
    fecha = datetime.now().isoformat(timespec="seconds")

    async def construir(i: int, c: dict) -> PointStruct:
        async with sem:
            # El título va delante para que el vector sepa de qué documento sale el fragmento
            vector = await get_embedding(f"{doc['titulo']}\n{c['text']}", http)
        pid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{doc['url']}#{i}"))
        payload = {
            "tenant_id": "lifextreme",
            "vector_id": pid,
            "text_content": c["text"],
            "source": doc["filename"],
            "filename": doc["filename"],
            "url": doc["url"],
            "titulo": doc["titulo"],
            "modulo_nombre": doc["modulo_nombre"],
            "entidad_emisora": doc["entidad_emisora"],
            "nivel_legal": doc["nivel_legal"],
            "estado": doc["estado"],
            "jurisdiccion": doc["jurisdiccion"],
            "categoria": doc["categoria"],
            "area": doc["area"],
            "region": doc["region"],
            "tier": doc["tier"],
            "idioma": doc["idioma"],
            "confidencial": False,
            # Orden: doc_n (1-20) > page > chunk_index permite reconstruir cada documento en secuencia
            "doc_n": doc["n"],
            "page": c["page"],
            "chunk_index": i,
            "total_fragmentos": len(chunks),
            "lote": LOTE,
            "fecha_ingesta": fecha,
        }
        return PointStruct(id=pid, vector=vector, payload=payload)

    points = await asyncio.gather(*(construir(i, c) for i, c in enumerate(chunks)))

    # Borra la versión anterior de este documento (por si ahora salen menos fragmentos) y sube la nueva
    await qdrant.delete(
        collection_name=COLLECTION,
        points_selector=FilterSelector(filter=Filter(must=[
            FieldCondition(key="lote", match=MatchValue(value=LOTE)),
            FieldCondition(key="url", match=MatchValue(value=doc["url"])),
        ])),
        wait=True,
    )
    for i in range(0, len(points), 64):
        await qdrant.upsert(collection_name=COLLECTION, points=points[i:i + 64], wait=True)
    return len(points)


# ---------------------------------------------------------------- main
async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--descargar", action="store_true", help="descarga los PDFs que falten y termina")
    ap.add_argument("--seco", action="store_true", help="extrae y trocea sin escribir en Qdrant")
    ap.add_argument("--solo", help="números de documento separados por coma, ej. 1,8,9")
    args = ap.parse_args()

    docs = DOCS
    if args.solo:
        elegidos = {int(x) for x in args.solo.split(",")}
        docs = [d for d in DOCS if d["n"] in elegidos]
    os.makedirs(PDF_DIR, exist_ok=True)

    if args.descargar:
        async with httpx.AsyncClient() as http:
            for d in docs:
                try:
                    print(f"[{d['n']:>2}] {d['filename']}: {await descargar(d, http)}")
                except Exception as e:
                    print(f"[{d['n']:>2}] {d['filename']}: ERROR {e}")
        return

    reporte = {"lote": LOTE, "coleccion": COLLECTION, "seco": args.seco, "documentos": []}
    qdrant = None if args.seco else AsyncQdrantClient(url=QDRANT_URL, timeout=300)
    sem = asyncio.Semaphore(4)
    total = 0
    async with httpx.AsyncClient() as http:
        for d in docs:
            ruta = os.path.join(PDF_DIR, d["filename"])
            fila = {"n": d["n"], "filename": d["filename"], "area": d["area"], "region": d["region"]}
            if not os.path.exists(ruta):
                fila["aviso"] = "no descargado"
                print(f"[{d['n']:>2}] {d['filename']}: falta el PDF (usa --descargar)")
                reporte["documentos"].append(fila)
                continue
            res = extraer_y_trocear(d)
            fila.update(res["stats"])
            linea = f"[{d['n']:>2}] {d['filename']}: {res['stats']['paginas']} págs, {res['stats']['fragmentos']} fragmentos"
            if res["stats"].get("aviso"):
                linea += f"  AVISO: {res['stats']['aviso']}"
            if res["chunks"] and not args.seco:
                fila["subidos"] = await ingestar(d, res["chunks"], qdrant, http, sem)
                total += fila["subidos"]
                linea += f" -> {fila['subidos']} vectores en Qdrant"
            print(linea, flush=True)
            reporte["documentos"].append(fila)

    reporte["total_subidos"] = total
    with open(REPORTE, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    print(f"\nTotal vectores subidos: {total}. Reporte: {REPORTE}")
    if qdrant:
        await qdrant.close()


if __name__ == "__main__":
    asyncio.run(main())
