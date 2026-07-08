#!/usr/bin/env python3
"""
=============================================================================
  LIFEXTREME — AGENTE CAZADOR DE FLYERS OUTDOOR 2026
  Versión: 1.0 | Motor: Ollama (Local LLMs) + DuckDuckGo + Supabase Storage
=============================================================================
  Funciona SIN coste de API externo. Usa tus modelos locales de Ollama.
  
  FLUJO:
  1. Lee los eventos del calendario 2026 definidos en este script
  2. Busca imágenes en DuckDuckGo por cada evento
  3. Descarga las imágenes candidatas en RAM
  4. Las valida visualmente con Ollama (llava si disponible, si no usa heurística)
  5. Sube la mejor imagen a Supabase Storage (bucket: event_flyers)
  6. Actualiza js/data.js con la URL de Supabase
=============================================================================
"""

import os
import re
import sys

# Forzar codificación UTF-8 en Windows para evitar crasheos con emojis/caracteres especiales
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding='utf-8')

import time
import json
import base64
import hashlib
import requests
import io
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from duckduckgo_search import DDGS
from supabase import create_client, Client

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OLLAMA_BASE   = "http://localhost:11434"
DATA_JS_PATH  = Path(__file__).parent.parent / "js" / "data.js"
BUCKET_NAME   = "event_flyers"

# Modelos disponibles en tu Ollama (en orden de preferencia para visión)
VISION_MODELS = ["llava:latest", "llava", "llama3.2-vision:latest"]
TEXT_MODEL    = "mistral:latest"   # fallback para análisis de texto

# Colores para la consola
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

# ─────────────────────────────────────────────
# CALENDARIO OUTDOOR 2026 — DATOS DE BÚSQUEDA
# Cada entrada: (event_id_en_data.js, nombre, departamento, mes)
# ─────────────────────────────────────────────
EVENTS_TO_HUNT = [
    (201, "Mi Primer Trail La Molina",              "Lima",        "junio 2026"),
    (202, "Ruta de la Chirimoya Callahuanca",       "Huarochirí",  "junio 2026"),
    (203, "Cajatambo Raid aventura",                "Lima",        "junio 2026"),
    (204, "Geoconsciencia Quelccaya glaciar",        "Cusco",       "junio 2026"),
    (205, "Tatoo Terra Challenge Morro Edition",    "Lima",        "junio 2026"),
    (206, "Carrera Sauce Tarapoto Laguna Azul",     "San Martín",  "junio 2026"),
    (207, "Marcahuasi Ultra SkyRunning MUT",        "Lima",        "junio 2026"),
    (208, "Picha Trail Fest Junín",                 "Junín",       "junio 2026"),
    (209, "Ranking Nacional DH Andahuaylas MTB",   "Apurímac",    "junio 2026"),
    (210, "Andes Pacific MTB Cup Huachupampa",      "Lima",        "junio 2026"),
    (211, "Ranking Nacional XCO Arequipa MTB",      "Arequipa",    "junio 2026"),
    (212, "Ultra Trail Cordillera Blanca UTCB",     "Huaraz",      "julio 2026"),
    (213, "Ai Apaec Trail Moche Trujillo",          "La Libertad", "julio 2026"),
    (214, "Sierra Andina Mountain Trail Matara",    "Áncash",      "julio 2026"),
    (215, "Desafio Manchay trail Lima",             "Lima",        "julio 2026"),
    (216, "Tingo María Trail Huánuco selva",        "Huánuco",     "julio 2026"),
    (217, "Valley Camp Urubamba Cusco exploradores","Cusco",       "julio 2026"),
    (218, "Ranking Nacional DH Cusco MTB",          "Cusco",       "julio 2026"),
    (219, "adidas Andes Race ultra maratón Cusco",  "Cusco",       "agosto 2026"),
    (220, "Ranking Nacional DH Cajamarca MTB",      "Cajamarca",   "agosto 2026"),
    (221, "Ranking Nacional XCO Cusco MTB",         "Cusco",       "agosto 2026"),
    (222, "Sudamericano BMX Racing Costa Verde",    "Lima",        "septiembre 2026"),
    (223, "Ranking Nacional DH Amancay MTB",        "Lima",        "septiembre 2026"),
    (224, "Peru Outdoor Expo Amazonas aventura",    "Amazonas",    "septiembre 2026"),
    (225, "MTB Pongo de Maenique selva Cusco",      "Cusco",       "octubre 2026"),
    (226, "Triatlón Paracas Medio Ironman",         "Ica",         "noviembre 2026"),
    (227, "Huacho Half Marathon media maratón",     "Lima",        "noviembre 2026"),
    (228, "Trail cierre temporada Arequipa 2026",   "Arequipa",    "diciembre 2026"),
]

# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────
def banner():
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════╗
║   🏔️  LIFEXTREME — AGENTE CAZADOR DE FLYERS OUTDOOR 2026    ║
║   Motor: Ollama Local | DuckDuckGo | Supabase Storage        ║
╚══════════════════════════════════════════════════════════════╝{RESET}
{YELLOW}  Objetivo: {len(EVENTS_TO_HUNT)} eventos | Inicio: {datetime.now().strftime("%H:%M:%S")}
  Bucket Supabase: {BUCKET_NAME}
  Modelo visión: llava (con fallback heurístico)
{RESET}""")

def log(prefix, color, msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{ts}] {prefix}{RESET} {msg}")

def progress_bar(current, total, width=40):
    pct = current / total
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r  {CYAN}[{bar}] {current}/{total} ({pct*100:.0f}%){RESET}", end="", flush=True)

# ─────────────────────────────────────────────
# AGENTE 1: RASTREADOR (DuckDuckGo)
# ─────────────────────────────────────────────
def agent_search(event_name: str, dept: str, month: str) -> list[dict]:
    """Busca imágenes del evento y retorna lista de {url, title}"""
    queries = [
        f'"{event_name}" flyer poster {month}',
        f'{event_name} {dept} trail running inscripcion',
        f'{event_name} carrera evento afiche',
    ]
    
    results = []
    with DDGS() as ddgs:
        for query in queries:
            try:
                imgs = list(ddgs.images(query, max_results=4, safesearch="off"))
                for img in imgs:
                    if img.get("image") and img["image"] not in [r["url"] for r in results]:
                        results.append({
                            "url": img["image"],
                            "title": img.get("title", ""),
                            "source": img.get("url", "")
                        })
                if len(results) >= 8:
                    break
                time.sleep(0.5)
            except Exception as e:
                pass
    
    return results[:8]  # máximo 8 candidatos

# ─────────────────────────────────────────────
# AGENTE 2: VALIDADOR VISUAL (Ollama llava)
# ─────────────────────────────────────────────
def check_vision_available() -> str | None:
    """Comprueba qué modelo de visión está disponible en Ollama"""
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            for vm in VISION_MODELS:
                vm_clean = vm.replace(":latest", "")
                for m in models:
                    if vm_clean in m:
                        return m
    except:
        pass
    return None

def download_image(url: str, timeout: int = 8) -> bytes | None:
    """Descarga una imagen en memoria, retorna bytes o None"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        r = requests.get(url, headers=headers, timeout=timeout, stream=True)
        if r.status_code == 200:
            content_type = r.headers.get("content-type", "")
            if any(t in content_type for t in ["image/", "jpeg", "png", "webp", "gif"]):
                data = r.content
                # Validación básica: al menos 10KB
                if len(data) > 10000:
                    return data
    except:
        pass
    return None

def validate_with_ollama(image_bytes: bytes, event_name: str, vision_model: str) -> tuple[bool, str]:
    """Usa llava para validar si la imagen es un flyer/poster del evento"""
    try:
        # Comprimir imagen para no saturar Ollama
        img = Image.open(io.BytesIO(image_bytes))
        img.thumbnail((800, 800))
        buffer = io.BytesIO()
        img.convert("RGB").save(buffer, format="JPEG", quality=75)
        img_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        prompt = (
            f"You are an image classifier for a Peruvian outdoor sports platform. "
            f"Look at this image. Is this a promotional flyer, poster, or high-quality photo "
            f"from a sports event called '{event_name}'? "
            f"The event involves outdoor sports like trail running, MTB, cycling, or adventure in Peru. "
            f"Answer ONLY with YES or NO, then one sentence explaining why."
        )
        
        payload = {
            "model": vision_model,
            "prompt": prompt,
            "images": [img_b64],
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 50}
        }
        
        resp = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload, timeout=45)
        if resp.status_code == 200:
            answer = resp.json().get("response", "").strip()
            is_valid = answer.upper().startswith("YES")
            return is_valid, answer[:100]
    except Exception as e:
        pass
    return False, "timeout/error"

def heuristic_validate(image_bytes: bytes, url: str) -> tuple[bool, str]:
    """
    Validación heurística cuando no hay modelo de visión disponible.
    Analiza: tamaño, resolución, formato, palabras clave en la URL.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        w, h = img.size
        size_kb = len(image_bytes) / 1024
        
        # Criterios positivos
        good_resolution = w >= 400 and h >= 300
        decent_size = size_kb >= 50
        
        # Palabras clave en URL (flyer, poster, event, carrera, etc.)
        url_lower = url.lower()
        keywords = ["flyer", "poster", "event", "carrera", "trail", "race", "competencia",
                    "inscripcion", "registro", "convocatoria", "afiche", "facebook", "instagram"]
        has_keyword = any(kw in url_lower for kw in keywords)
        
        # Proporción razonable (no extremadamente panorámica)
        ratio = w / h if h > 0 else 1
        good_ratio = 0.5 <= ratio <= 2.5
        
        score = sum([good_resolution, decent_size, has_keyword, good_ratio])
        is_valid = score >= 2
        
        reason = f"Res:{w}x{h} Size:{size_kb:.0f}KB Ratio:{ratio:.1f} Keyword:{has_keyword}"
        return is_valid, reason
    except:
        return False, "invalid image"

# ─────────────────────────────────────────────
# AGENTE 3: PROCESADOR Y UPLOADER
# ─────────────────────────────────────────────
def process_and_upload(image_bytes: bytes, event_id: int, event_name: str, supabase: Client) -> str | None:
    """Optimiza la imagen y la sube a Supabase Storage"""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Redimensionar a máximo 1200px en el lado más largo
        img.thumbnail((1200, 1200), Image.LANCZOS)
        
        # Guardar como WebP optimizado
        buffer = io.BytesIO()
        img.save(buffer, format="WEBP", quality=82, method=6)
        webp_bytes = buffer.getvalue()
        
        # Nombre único del archivo
        slug = re.sub(r"[^a-z0-9]+", "-", event_name.lower())[:50]
        filename = f"event-{event_id}-{slug}.webp"
        
        # Subir a Supabase Storage
        supabase.storage.from_(BUCKET_NAME).upload(
            path=filename,
            file=webp_bytes,
            file_options={"content-type": "image/webp", "upsert": "true"}
        )
        
        # Generar URL pública
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(filename)
        return public_url
        
    except Exception as e:
        log("  ✗ UPLOAD ERROR", RED, str(e))
        return None

def update_data_js(event_id: int, new_img_url: str) -> bool:
    """Actualiza la URL img del evento en js/data.js usando regex"""
    try:
        content = DATA_JS_PATH.read_text(encoding="utf-8")
        
        # Pattern: busca la línea del evento por su id y reemplaza img:
        # Maneja comillas simples y dobles en la URL
        pattern = rf"({{ id: {event_id},[^}}]+?img: ')([^']+)(')"
        replacement = rf"\g<1>{new_img_url}\g<3>"
        
        new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
        
        # Si no encontró con comillas simples, intentar con dobles
        if count == 0:
            pattern2 = rf'({{ id: {event_id},[^}}]+?img: ")([^"]+)(")'
            replacement2 = rf'\g<1>{new_img_url}\g<3>'
            new_content, count = re.subn(pattern2, replacement2, content, flags=re.DOTALL)
        
        if count > 0:
            DATA_JS_PATH.write_text(new_content, encoding="utf-8")
            return True
        else:
            log("  ⚠ REGEX", YELLOW, f"No se encontró id: {event_id} en data.js")
            return False
            
    except Exception as e:
        log("  ✗ FILE ERROR", RED, str(e))
        return False

# ─────────────────────────────────────────────
# ORQUESTADOR PRINCIPAL
# ─────────────────────────────────────────────
def main():
    banner()
    
    # Inicializar Supabase
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        log("✓ SUPABASE", GREEN, "Conectado correctamente")
    except Exception as e:
        log("✗ SUPABASE", RED, f"Error de conexión: {e}")
        sys.exit(1)
    
    # Detectar modelo de visión
    vision_model = check_vision_available()
    if vision_model:
        log("✓ VISIÓN", GREEN, f"Modelo disponible: {vision_model}")
    else:
        log("⚠ VISIÓN", YELLOW, "No hay modelo llava disponible → usando validación heurística")
    
    print(f"\n{BOLD}{'═'*62}{RESET}\n")
    
    # Contadores
    results_log = []
    success = 0
    skipped = 0
    failed = 0
    
    total = len(EVENTS_TO_HUNT)
    
    for idx, (event_id, event_name, dept, month) in enumerate(EVENTS_TO_HUNT, 1):
        print(f"\n{BOLD}{BLUE}[{idx}/{total}] Evento ID={event_id}: {event_name}{RESET}")
        log("  ⟳ BÚSQUEDA", CYAN, f'Buscando: "{event_name} {month}"...')
        
        # AGENTE 1: Buscar imágenes
        candidates = agent_search(event_name, dept, month)
        
        if not candidates:
            log("  ✗ SIN RESULTADOS", RED, "No se encontraron imágenes")
            failed += 1
            results_log.append({"id": event_id, "name": event_name, "status": "FAILED", "reason": "no images found"})
            time.sleep(1)
            continue
        
        log("  ✓ CANDIDATOS", GREEN, f"{len(candidates)} imágenes encontradas. Validando...")
        
        # AGENTE 2: Validar imágenes
        best_image_bytes = None
        best_url = None
        
        for ci, candidate in enumerate(candidates, 1):
            url = candidate["url"]
            log(f"    [{ci}/{len(candidates)}] ANALIZAR", YELLOW, f"{url[:60]}...")
            
            # Descargar
            img_bytes = download_image(url)
            if not img_bytes:
                log(f"    [{ci}] ✗ DESCARGA", RED, "Falló o tamaño insuficiente")
                continue
            
            # Validar
            if vision_model:
                is_valid, reason = validate_with_ollama(img_bytes, event_name, vision_model)
            else:
                is_valid, reason = heuristic_validate(img_bytes, url)
            
            mode = "🤖 LLM" if vision_model else "📐 HEURÍSTICA"
            if is_valid:
                log(f"    [{ci}] ✓ APROBADA", GREEN, f"{mode}: {reason}")
                best_image_bytes = img_bytes
                best_url = url
                break
            else:
                log(f"    [{ci}] ✗ RECHAZADA", RED, f"{mode}: {reason}")
        
        if not best_image_bytes:
            # Fallback: tomar la primera imagen descargable sin validar
            log("  ⚠ FALLBACK", YELLOW, "Usando mejor candidato disponible sin validación...")
            for candidate in candidates:
                img_bytes = download_image(candidate["url"])
                if img_bytes:
                    best_image_bytes = img_bytes
                    best_url = candidate["url"]
                    break
        
        if not best_image_bytes:
            log("  ✗ SIN IMAGEN VÁLIDA", RED, "Omitiendo evento")
            failed += 1
            results_log.append({"id": event_id, "name": event_name, "status": "FAILED", "reason": "no valid image"})
            time.sleep(1)
            continue
        
        # AGENTE 3: Subir a Supabase
        log("  ⬆ SUPABASE", CYAN, "Optimizando y subiendo imagen...")
        public_url = process_and_upload(best_image_bytes, event_id, event_name, supabase)
        
        if not public_url:
            log("  ✗ UPLOAD FALLIDO", RED, "No se pudo subir a Supabase")
            failed += 1
            results_log.append({"id": event_id, "name": event_name, "status": "FAILED", "reason": "upload failed"})
            time.sleep(2)
            continue
        
        log("  ✓ URL PÚBLICA", GREEN, f"{public_url[:70]}...")
        
        # Actualizar data.js
        updated = update_data_js(event_id, public_url)
        if updated:
            log("  ✓ DATA.JS", GREEN, "URL actualizada correctamente en js/data.js")
            success += 1
            results_log.append({"id": event_id, "name": event_name, "status": "SUCCESS", "url": public_url})
        else:
            log("  ⚠ DATA.JS", YELLOW, "Subida OK pero no se actualizó data.js (check regex)")
            skipped += 1
            results_log.append({"id": event_id, "name": event_name, "status": "PARTIAL", "url": public_url})
        
        # Pausa entre eventos para no saturar DuckDuckGo
        time.sleep(2)
        
        # Progress bar
        print()
        progress_bar(idx, total)
    
    # ─── REPORTE FINAL ───
    print(f"\n\n{BOLD}{'═'*62}{RESET}")
    print(f"{BOLD}{GREEN}  📊 REPORTE FINAL — AGENTE CAZADOR DE FLYERS{RESET}")
    print(f"{'═'*62}")
    print(f"  {GREEN}✓ Exitosos:  {success}/{total}{RESET}")
    print(f"  {YELLOW}⚠ Parciales: {skipped}/{total}{RESET}")
    print(f"  {RED}✗ Fallidos:  {failed}/{total}{RESET}")
    print(f"{'═'*62}")
    
    # Guardar log
    log_path = Path(__file__).parent.parent / "scripts" / "flyer_hunt_log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "run_at": datetime.now().isoformat(),
            "success": success, "skipped": skipped, "failed": failed,
            "results": results_log
        }, f, ensure_ascii=False, indent=2)
    print(f"\n  {CYAN}Log guardado en: scripts/flyer_hunt_log.json{RESET}")
    
    if success > 0:
        print(f"\n{BOLD}{GREEN}  🚀 ¡Listo! {success} imágenes reales cargadas en data.js{RESET}")
        print(f"  {YELLOW}  Recuerda hacer git add + commit + push para publicar en Vercel.{RESET}\n")

if __name__ == "__main__":
    main()
