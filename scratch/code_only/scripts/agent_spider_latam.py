import os
import json
import time
import random
import requests
from urllib.parse import urlparse

# ==============================================================================
# CONFIGURACIÓN DEL AGENTE ARAÑA LATAM (CUMPLIMIENTO ÉTICO)
# ==============================================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_pdfs'))
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:latest"

# User-Agent que simula un navegador humano normal (No bot malicioso)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3'
}

# ==============================================================================
# BASE DE DATOS DE BÚSQUEDA ESTRATÉGICA POR PAÍS (ENLACES DIRECTOS)
# ==============================================================================
ENLACES_LATAM = {
    "argentina": [
        "https://www.argentina.gob.ar/sites/default/files/plan_estrategico_territorial.pdf",
        "https://www.argentina.gob.ar/sites/default/files/plan_nacional_de_reduccion_del_riesgo_de_desastres_2024-2030.pdf"
    ],
    "colombia": [
        "https://www.mincit.gov.co/getattachment/minturismo/calidad-y-desarrollo-sostenible/plan-sectorial-de-turismo-2022-2026/plan-sectorial-de-turismo-2022-2026.pdf.aspx",
        "https://www.invias.gov.co/index.php/documentos-tecnicos/11497-plan-nacional-de-seguridad-vial/file"
    ],
    "brasil": [
        "https://www.gov.br/turismo/pt-br/acesso-a-informacao/acoes-e-programas/plano-nacional-de-turismo/PNT20242027_aprovado.pdf"
    ],
    "bolivia": [
        "https://www.defensacivil.gob.bo/web/uploads/files/Plan_Nacional_Emergencias.pdf"
    ],
    "ecuador": [
        "https://www.turismo.gob.ec/wp-content/uploads/2020/03/PLANDETUR-2030.pdf"
    ],
    "chile": [
        "https://www.sernatur.cl/wp-content/uploads/2018/11/Estrategia-Nacional-de-Turismo-2012-2020.pdf",
        "https://senapred.cl/wp-content/uploads/2023/01/Plan-Estrategico-Nacional-para-la-Reduccion-del-Riesgo-de-Desastres.pdf"
    ]
}

def obtener_historial_pais(pais):
    hist_file = os.path.join(BASE_DIR, pais, f"historial_{pais}.json")
    if os.path.exists(hist_file):
        try:
            with open(hist_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_historial_pais(pais, historial):
    hist_file = os.path.join(BASE_DIR, pais, f"historial_{pais}.json")
    with open(hist_file, 'w', encoding='utf-8') as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def descarga_etica(url, filepath):
    """
    Descarga respetando límites y detectando bloqueos.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=20, stream=True)
        
        # Manejo de bloqueos (Too Many Requests)
        if response.status_code == 429:
            print("    [ALERTA ÉTICA] Servidor detectó muchas peticiones (HTTP 429).")
            print("    [ALERTA ÉTICA] Iniciando pausa de seguridad de 60 segundos...")
            time.sleep(60)
            return False
            
        response.raise_for_status()
        
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and not url.lower().endswith('.pdf'):
            print("    [RECHAZADO] La URL no dirige a un archivo PDF real.")
            return False
            
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: f.write(chunk)
                
        return True
    except requests.exceptions.RequestException as e:
        print(f"    [ERROR DE RED] Servidor inaccesible o enlace roto: {e}")
        return False
    except Exception as e:
        print(f"    [ERROR] {e}")
        return False

def evaluar_con_llm(titulo, url, pais):
    """
    Filtro estricto de IA. Solo documentos institucionales o logísticos.
    """
    prompt = f"""Eres un Analista de Inteligencia Estratégica gubernamental B2B.
Evalúa este documento de {pais} encontrado en internet.
Solo queremos: Planes maestros de turismo, reportes de infraestructura, vialidad, logística o gestión de riesgos de desastres institucionales.
RECHAZA terminantemente: Publicidad, guías turísticas comerciales, folletos de hoteles, agencias de viaje o artículos de opinión.

Título/Ruta: {titulo}
Enlace: {url}

¿Es este un documento oficial de inteligencia estratégica y logística valioso?
Responde ÚNICAMENTE con la palabra "SI" o "NO"."""

    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": prompt, "stream": False}, timeout=15)
        if response.status_code == 200:
            result = response.json().get("response", "").strip().upper()
            return "SI" in result or "SÍ" in result
    except:
        pass
    return True # Fail-safe

def iniciar_recoleccion():
    print("================================================================")
    print(" LIFEXTREME SPIDER LATAM - Minería Continental Segura y Ética")
    print(" Modelo: Phi-3 Local | Modo: Politeness/Anti-Block Activo")
    print("================================================================\n")
    
    for pais, urls in ENLACES_LATAM.items():
        pais_dir = os.path.join(BASE_DIR, pais)
        os.makedirs(pais_dir, exist_ok=True)
        
        historial = obtener_historial_pais(pais)
        urls_descargadas = [h.get("url") for h in historial]
        
        print(f"\n[>>>] INICIANDO OPERACIÓN EN: {pais.upper()}")
        
        for url in urls:
            if url in urls_descargadas:
                print(f"  - [OMITIDO] Ya descargado: {url}")
                continue
                
            title = os.path.basename(urlparse(url).path) or "documento_generico"
            print(f"  -> Evaluando IA: {url[:70]}...")
            
            if evaluar_con_llm(title, url, pais):
                print(f"    [APROBADO] Documento estratégico detectado.")
                
                safe_title = "".join([c if c.isalnum() else "_" for c in title]).strip("_")[:50]
                filepath = os.path.join(pais_dir, f"{safe_title}_{int(time.time())}.pdf")
                
                if descarga_etica(url, filepath):
                    print(f"    [ÉXITO] Guardado en: {pais}/{os.path.basename(filepath)}")
                    historial.append({"titulo": title, "url": url, "fecha": time.strftime("%Y-%m-%d %H:%M:%S")})
                    guardar_historial_pais(pais, historial)
                    urls_descargadas.append(url)
            else:
                print(f"    [RECHAZADO] La IA determinó que es publicidad o irrelevante.")
            
            # Pausa humana aleatoria entre cada revisión de documento (5 a 10 segundos)
            retraso = random.randint(5, 10)
            print(f"    [Zzz] Pausa ética anti-bloqueo de {retraso} segundos...")
            time.sleep(retraso)

if __name__ == "__main__":
    iniciar_recoleccion()
    print("\n[OK] Ciclo de patrullaje continental finalizado.")
