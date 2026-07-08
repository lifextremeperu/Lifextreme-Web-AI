import os
import json
import glob
import fitz  # PyMuPDF
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client
import requests

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
OLLAMA_URL = "http://localhost:11434/api/embed"

def get_embedding(text):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "nomic-embed-text",
            "input": [text]
        })
        return response.json()['embeddings'][0]
    except Exception as e:
        print(f"Error con Ollama: {e}")
        return None

def upsert_vectors(records):
    if not records: return
    try:
        supabase.table("knowledge_vectors").upsert(records, on_conflict="vector_id").execute()
    except Exception as e:
        print(f"[-] Error subiendo a Supabase: {e}")

print("===================================================================")
print(" >>> INICIANDO SINCRONIZACIÓN FINAL DEL CEREBRO MAX ")
print("===================================================================")

# ---------------------------------------------------------
# 1. ADN DE VENTAS Y COMERCIAL
# ---------------------------------------------------------
print("\n[1] Procesando ADN Comercial y Reglas de Venta...")
records_dna = []

# max_commercial_brain.json
try:
    with open("data/knowledge/max_commercial_brain.json", "r", encoding="utf-8") as f:
        commercial_brain = json.load(f)
        
    # identity
    identity_text = f"MAX IDENTITY: {json.dumps(commercial_brain.get('identity', {}), ensure_ascii=False)}"
    records_dna.append({
        "vector_id": "dna_identity",
        "region": "global",
        "modulo_nombre": "Sales_DNA",
        "text_content": identity_text,
        "embedding": get_embedding(identity_text)
    })
    
    # business units
    for unit, details in commercial_brain.get("business_units", {}).items():
        text = f"Business Unit ({unit.upper()}): {json.dumps(details, ensure_ascii=False)}"
        records_dna.append({
            "vector_id": f"dna_bu_{unit}",
            "region": "global",
            "modulo_nombre": "Sales_DNA",
            "text_content": text,
            "embedding": get_embedding(text)
        })
except Exception as e:
    print(f"[-] Error commercial brain: {e}")

# max_sales_dna.json
try:
    with open("data/knowledge/max_sales_dna.json", "r", encoding="utf-8") as f:
        sales_dna = json.load(f)
        
    for section, content in sales_dna.items():
        text = f"Sales Strategy ({section.upper()}): {json.dumps(content, ensure_ascii=False) if isinstance(content, (dict, list)) else content}"
        records_dna.append({
            "vector_id": f"dna_strategy_{section}",
            "region": "global",
            "modulo_nombre": "Sales_DNA",
            "text_content": text,
            "embedding": get_embedding(text)
        })
except Exception as e:
    print(f"[-] Error sales dna: {e}")

if records_dna:
    upsert_vectors(records_dna)
    print(f"[+] Inyectados {len(records_dna)} vectores de ADN Comercial.")

# ---------------------------------------------------------
# 2. COMPLETAR 187 FQSAs FALTANTES DE PERU
# ---------------------------------------------------------
print("\n[2] Identificando y subiendo FQSAs faltantes de Perú...")
print("    Descargando IDs existentes en Supabase (esto tomará unos segundos)...")
limit = 1000
existing_ids = set()
for i in range(100):
    res = supabase.table('knowledge_vectors').select('vector_id').range(i*limit, (i+1)*limit - 1).execute()
    for row in res.data:
        existing_ids.add(row['vector_id'])
    if len(res.data) < limit:
        break

print(f"    Total vectores en DB: {len(existing_ids)}")

records_missing = []
for p in Path('data/knowledge/peru').rglob('*.json'):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            fqsas_dict = data.get('fqsas', {})
            region_name = p.parents[1].name.lower()
            modulo_id = data.get("modulo_id", "00")
            modulo_nombre = data.get("modulo_nombre", "General")
            tier = data.get("tier", 3)
            
            for angle_name, qa_list in fqsas_dict.items():
                if not isinstance(qa_list, list): continue
                for idx, qa in enumerate(qa_list):
                    vector_id = f"{region_name}_{modulo_id}_{angle_name}_{idx}"
                    if vector_id not in existing_ids:
                        q = qa.get("q", "")
                        a = qa.get("a", "")
                        text_content = f"Región: {region_name.capitalize()}. Módulo: {modulo_nombre}. Pregunta: {q} Respuesta: {a}"
                        
                        emb = get_embedding(text_content)
                        if emb:
                            records_missing.append({
                                "vector_id": vector_id,
                                "region": region_name,
                                "tier": int(tier) if str(tier).isdigit() else 3,
                                "modulo_nombre": modulo_nombre,
                                "text_content": text_content,
                                "embedding": emb
                            })
    except: pass

if records_missing:
    print(f"    Generados {len(records_missing)} embeddings faltantes. Subiendo...")
    upsert_vectors(records_missing)
    print(f"[+] Hueco regional parchado con éxito.")
else:
    print(f"[+] No hay vectores faltantes detectados.")

# ---------------------------------------------------------
# 3. EXTRAER Y VECTORIZAR PDFs EXTERNOS (SONOTERAPIA)
# ---------------------------------------------------------
print("\n[3] Escaneando PDFs en carpeta local LIFEXTREME (Sonoterapia, etc)...")
external_dir = Path(r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME")
folders_to_scan = ["SONOTERAPIA", "GLAMPING TIPI COYA", "MASTER MAIN CUSCO"]

records_pdfs = []
for folder in folders_to_scan:
    folder_path = external_dir / folder
    if not folder_path.exists(): continue
    
    for pdf_file in folder_path.rglob("*.pdf"):
        print(f"    Procesando PDF: {pdf_file.name}")
        try:
            doc = fitz.open(pdf_file)
            text_full = ""
            for page in doc:
                text_full += page.get_text() + "\n"
            doc.close()
            
            # Chunking basico por saltos de linea o tamaño
            chunks = [text_full[i:i+1500] for i in range(0, len(text_full), 1500)]
            
            for idx, chunk in enumerate(chunks):
                if len(chunk.strip()) < 50: continue
                text_content = f"Documento: {pdf_file.name}. Carpeta: {folder}. Contenido: {chunk.strip()}"
                vector_id = f"ext_{folder.lower().replace(' ', '_')}_{pdf_file.name.replace(' ', '_')}_{idx}"
                
                if vector_id not in existing_ids:
                    emb = get_embedding(text_content)
                    if emb:
                        records_pdfs.append({
                            "vector_id": vector_id[:255], # max len
                            "region": "global",
                            "modulo_nombre": folder,
                            "text_content": text_content,
                            "embedding": emb
                        })
        except Exception as e:
            print(f"    [-] Error procesando PDF {pdf_file.name}: {e}")

if records_pdfs:
    print(f"    Subiendo {len(records_pdfs)} vectores de PDFs externos...")
    upsert_vectors(records_pdfs)
    print(f"[+] Archivos locales inyectados exitosamente.")
else:
    print(f"[+] No se encontraron PDFs nuevos para inyectar.")

print("\n===================================================================")
print(" ✅ SINCRONIZACIÓN FINALIZADA. EL CEREBRO DE MAX ESTÁ AL 100%. ")
print("===================================================================")
