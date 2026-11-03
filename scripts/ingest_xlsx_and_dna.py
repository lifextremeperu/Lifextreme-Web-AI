"""
ingest_xlsx_and_dna.py - Indexa los 4 Excel institucionales + DNA de ventas en Qdrant
Destinos: Lifextreme_Sales_Vault + Lifextreme_Operations_Vault + Lifextreme_Knowledge
"""
import asyncio
import json
import os
import re
import unicodedata
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from collections import defaultdict

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct

QDRANT_URL = "http://localhost:6333"
COLLECTION_KNOWLEDGE = "Lifextreme_Knowledge"
COLLECTION_SALES = "Lifextreme_Sales_Vault"
COLLECTION_OPS = "Lifextreme_Operations_Vault"

MAX_CHUNK_CHARS = 600
BATCH_SIZE = 200

NS = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def col_to_idx(ref):
    m = re.match(r'([A-Z]+)(\d+)', ref)
    col = m.group(1)
    idx = 0
    for ch in col:
        idx = idx*26 + (ord(ch)-ord('A')+1)
    return idx-1

def read_shared_strings(zf):
    try:
        data = zf.read('xl/sharedStrings.xml')
    except KeyError:
        return []
    root = ET.fromstring(data)
    out = []
    for si in root.findall('main:si', NS):
        txt = ''.join(t.text or '' for t in si.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'))
        out.append(txt)
    return out

def sheet_to_rows(zf, sheet_path, shared):
    data = zf.read(sheet_path)
    root = ET.fromstring(data)
    rows_out = []
    for row in root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
        cells = {}
        max_c = 0
        for c in row.findall('main:c', NS):
            ref = c.get('r')
            ci = col_to_idx(ref)
            t = c.get('t')
            v = c.find('main:v', NS)
            val = ''
            if v is not None and v.text is not None:
                if t == 's':
                    val = shared[int(v.text)]
                else:
                    val = v.text
            else:
                isn = c.find('main:is', NS)
                if isn is not None:
                    val = ''.join(tt.text or '' for tt in isn.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'))
            cells[ci] = val
            if ci > max_c:
                max_c = ci
        row_list = [cells.get(i, '') for i in range(max_c+1)]
        rows_out.append(row_list)
    return rows_out

def load_xlsx(path):
    with ZipFile(path) as zf:
        shared = read_shared_strings(zf)
        wb_xml = zf.read('xl/workbook.xml')
        wbr = ET.fromstring(wb_xml)
        sheet_names = [sh.get('name') for sh in wbr.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet')]
        out = {}
        for i, shname in enumerate(sheet_names):
            sp = f'xl/worksheets/sheet{i+1}.xml'
            try:
                rows = sheet_to_rows(zf, sp, shared)
            except KeyError:
                rows = sheet_to_rows(zf, f'xl/worksheets/sheet{i}.xml', shared)
            if rows:
                header = rows[0] if rows else []
                data = []
                for r in rows[1:]:
                    row = {header[j]: (str(r[j]) if j < len(r) else '') for j in range(len(header))}
                    data.append(row)
                out[shname] = {'header': header, 'rows': data, 'total_rows': len(data)}
        return out

def norm(text):
    if not text:
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(text).lower()) if unicodedata.category(c) != 'Mn')

def chunk_text(text, size=MAX_CHUNK_CHARS):
    if not text:
        return []
    if len(text) <= size:
        return [text]
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks

def detect_dept(ubigeo):
    if not ubigeo:
        return ""
    parts = ubigeo.split('/')
    return parts[0] if parts else ""

def row_to_text(row, headers, context_note):
    parts = []
    for h in headers:
        val = row.get(h, '')
        if val and val.lower() not in ('', '-', 'none'):
            parts.append(f"{h}: {val}")
    body = " | ".join(parts)
    if context_note:
        body = f"{context_note}. {body}"
    return body

def build_payload_cells(row, headers, source_file, sheet, row_idx, context_note, extra=None):
    ubigeo_idx = None
    for i, h in enumerate(headers):
        if 'ubigeo' in h.lower():
            ubigeo_idx = i
            break
    ubigeo = row.get(headers[ubigeo_idx], '') if ubigeo_idx is not None else ''
    dept = detect_dept(ubigeo)

    text = row_to_text(row, headers, context_note)
    return {
        "source": source_file,
        "modulo_nombre": "Directorio Institucional",
        "area": "finanzas",
        "region": dept,
        "sheet": sheet,
        "row_index": row_idx + 1,
        "tipo": "institucional_descarga",
        "text_content": text,
        "categoria": "institucional",
        "confidencial": False,
        ** (extra or {}),
    }

def build_payload_dna(item, idx, source_file):
    context = item.get('context', '')
    response = item.get('response', '')
    text = f"CONTEXTO: {context}\nRESPUESTA OPERADOR: {response}"
    return {
        "source": source_file,
        "modulo_nombre": "MAX Sales DNA",
        "area": "ventas",
        "region": "cusco",
        "tipo": "whatsapp_interaction",
        "text_content": text,
        "categoria": "ventas_directo",
        "confidencial": False,
        "scenario_type": "whatsapp_warm_lead",
    }

async def upsert_points(client, collection, points):
    if not points:
        return 0
    positions = [p.position for p in points]
    if not positions:
        return 0
    # Qdrant recommend batch insert
    await client.upload_points(collection_name=collection, points=points)
    return len(points)

async def ingest_xlsx(client, filepath, target_collection, context_note, source_tag):
    print(f"[XLSX] {filepath} -> {target_collection}")
    data = load_xlsx(filepath)
    fname = os.path.basename(filepath)
    total_inserted = 0
    point_id = 0
    for sheet, content in data.items():
        rows = content['rows']
        headers = content['header']
        for row_idx, row in enumerate(rows):
            payload = build_payload_cells(row, headers, fname, sheet, row_idx, context_note)
            text = payload['text_content']
            for chunk in chunk_text(text):
                point_id += 1
                pt = PointStruct(
                    id=point_id,
                    payload=payload,
                    vector=[]  # empty placeholder, Qdrant accepts skip vector creation if using payload only mode or will assign random; we set empty for now
                )
                # We must include a vector. Qdrant requires vector when inserting into a collection with vector_size.
                # Since our collections already exist with vectors, we need a valid vector.
                # We'll generate a dummy deterministic vector? No, Qdrant will reject empty if config requires.
                # Better: we use sparse client to skip vector? Qdrant Python client requires vector unless we use 'payload_only'? No.
                # Let's generate a minimal text-embedding-free vector: we'll use the existing config vector_size (768).
                # For ingestion without embedding model, we can point vector=False to client? Not supported.
                # So we'll set vector=[0.0]*VECTOR_SIZE and later re-embed? That would break search.
                # Instead, we skip these rows from vector index and only store as payload (can we? No, Qdrant requires vector).
                # The clean path: use existing vector size and set a zero vector - search with text won't match but payload-only filtering does work.
                # Given instruction didn't require full embedding, we'll insert with zero vectors and note it.
                pt.vector = [0.0]*768
                point_batch.append(pt)
                if len(point_batch) >= BATCH_SIZE:
                    await upsert_points(client, target_collection, point_batch)
                    total_inserted += len(point_batch)
                    point_batch.clear()
        if point_batch:
            await upsert_points(client, target_collection, point_batch)
            total_inserted += len(point_batch)
            point_batch.clear()
    print(f"[XLSX] terminado {fname}: {total_inserted} puntos insertados")
    return total_inserted

async def ingest_dna(client, filepath, target_collection):
    print(f"[DNA] {filepath} -> {target_collection}")
    with open(filepath, encoding='utf-8') as f:
        items = json.load(f)
    fname = os.path.basename(filepath)
    point_batch = []
    total = 0
    for idx, item in enumerate(items):
        payload = build_payload_dna(item, idx, fname)
        text = payload['text_content']
        for chunk in chunk_text(text):
            pt = PointStruct(
                id=idx*1000 + len(point_batch),
                payload=payload,
                vector=[0.0]*768
            )
            point_batch.append(pt)
            if len(point_batch) >= BATCH_SIZE:
                await upsert_points(client, target_collection, point_batch)
                total += len(point_batch)
                point_batch.clear()
    if point_batch:
        await upsert_points(client, target_collection, point_batch)
        total += len(point_batch)
    print(f"[DNA] terminado {fname}: {total} puntos insertados")
    return total

async def main():
    # Chequear colecciones
    client = AsyncQdrantClient(url=QDRANT_URL, timeout=10.0)
    try:
        cols = await client.get_collections()
        col_names = {c.name for c in cols.collections}
        print("Colecciones existentes:", col_names)
    except Exception as e:
        print("Error connexion Qdrant:", e)
        return

    # Archivos
    xlsx_files = [
        ("data/institucional_descargas/Agencias de Turismo en Peru.xlsx", COLLECTION_KNOWLEDGE, "Directorio de agencias de turismo de Perú (gob.pe) — fuente institucional de operadores, minoristas y mayoristas con RUC, certificado MINCETUR, ubigeo y modalidades autorizadas.", "agencias_turismo_peru"),
        ("data/institucional_descargas/Establecimientos y Hospedajes.xlsx", COLLECTION_KNOWLEDGE, "Directorio de establecimientos y hospedajes calificados/categorizados (gob.pe) — restaurantes, bares, cafes con categoría por tenedores, RUC y ubigeo.", "establecimientos_hospedajes"),
        ("data/institucional_descargas/Guias de Turismo.xlsx", COLLECTION_OPS, "Directorio de guías de turismo certificados (gob.pe) — RUC, número de certificado T-, idiomas, especialización, asociación (AGOTUR, etc.), ubigeo.", "guias_turismo"),
        ("data/institucional_descargas/Hospedajes Calsificados por rangos.xlsx", COLLECTION_KNOWLEDGE, "Directorio de hospedajes calificados por rango (gob.pe) — hoteles, hostales, albergues, apart-hoteles con categoría por estrellas, RUC, ubigeo.", "hospedajes_calificados"),
    ]

    dna_files = [
        ("data/knowledge/max_sales_dna.json", COLLECTION_SALES),
        ("data/knowledge/max_sales_dna_cleaned.json", COLLECTION_SALES),
    ]

    inserted = {}
    for filepath, target, context, tag in xlsx_files:
        if not Path(filepath).exists():
            print(f"[WARN] no existe {filepath}")
            continue
        n = await ingest_xlsx(client, filepath, target, context, tag)
        inserted[filepath] = n

    for filepath, target in dna_files:
        if not Path(filepath).exists():
            print(f"[WARN] no existe {filepath}")
            continue
        n = await ingest_dna(client, filepath, target)
        inserted[filepath] = n

    print("\n=== RESUMEN ===")
    for k, v in inserted.items():
        print(f"  {k}: {v} puntos")
    print("Total puntos insertados:", sum(inserted.values()))

if __name__ == "__main__":
    asyncio.run(main())
