import os
import json
import urllib.request
import ssl
from pathlib import Path

# Deshabilitar verificación SSL estricta por si las webs del estado tienen certificados expirados
ssl._create_default_https_context = ssl._create_unverified_context

TARGET_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\MODULOS TURISMO"
METADATA_FILE = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\knowledge\gov_metadata.json"

DOCUMENTS = [
    {
        "filename": "MINCETUR_Ley_32392.pdf",
        "url": "https://www.sunat.gob.pe/legislacion/procedim/normasadua/gja-03/ctrlCambios/anexos/Ley_32392.pdf",
        "entidad_emisora": "MINCETUR",
        "nivel_legal": "Ley",
        "jurisdiccion": "Nacional",
        "titulo": "Nueva Ley General de Turismo"
    },
    {
        "filename": "MINCETUR_Reglamento_Ley_32392.pdf",
        "url": "https://www.gob.pe/institucion/mincetur/informes-publicaciones/8059787-ley-n-32392-nueva-ley-general-de-turismo-y-de-su-reglamento-aprobado-mediante-decreto-supremo-n-002-2026-mincetur", 
        "entidad_emisora": "MINCETUR",
        "nivel_legal": "Decreto Supremo",
        "jurisdiccion": "Nacional",
        "titulo": "Reglamento de la Ley 32392"
    },
    {
        "filename": "MINCETUR_Seguridad_Aventura.pdf",
        "url": "https://www.aptae.pe/wp-content/uploads/2018/10/Reglamento-de-Seguridad-en-Turismo-de-Aventura-Decreto-Supremo-005-2016-MINCETUR.pdf",
        "entidad_emisora": "MINCETUR",
        "nivel_legal": "Decreto Supremo",
        "jurisdiccion": "Nacional",
        "titulo": "Reglamento de Seguridad en Turismo de Aventura"
    },
    {
        "filename": "MINCETUR_Agencias_Viajes.pdf",
        "url": "http://www.aptae.pe/wp-content/uploads/2018/10/Reglamento-de-Agencias-de-Viajes-y-Turismo-D.S.-005-2020-MINCETUR.pdf",
        "entidad_emisora": "MINCETUR",
        "nivel_legal": "Decreto Supremo",
        "jurisdiccion": "Nacional",
        "titulo": "Reglamento de Agencias de Viajes y Turismo"
    },
    {
        "filename": "MINCETUR_PENTUR_2025.pdf",
        "url": "https://transparencia.mincetur.gob.pe/documentos/newweb/portals/0/transparencia/pmi/RM_050-2024-MINCETUR-ANEXO.pdf",
        "entidad_emisora": "MINCETUR",
        "nivel_legal": "Plan Nacional",
        "jurisdiccion": "Nacional",
        "titulo": "Plan Estratégico Nacional de Turismo PENTUR 2025"
    },
    {
        "filename": "MINCETUR_Plan_Proteccion_Turista.pdf",
        "url": "https://transparencia.mincetur.gob.pe/documentos/newweb/Portals/0/transparencia/proyectos%20resoluciones/PLAN_PROTECCION_TURISTA.pdf",
        "entidad_emisora": "MINCETUR",
        "nivel_legal": "Plan Sectorial",
        "jurisdiccion": "Nacional",
        "titulo": "Plan de Protección al Turista y Red de Seguridad"
    },
    {
        "filename": "MINCETUR_Manual_Ambiental_Hospedaje.pdf",
        "url": "https://sinia.minam.gob.pe/sites/default/files/siar-huancavelica/archivos/public/docs/manual-buenas-practicas-ambientales-establecimiento-hospedaje-mincetur.pdf",
        "entidad_emisora": "MINCETUR",
        "nivel_legal": "Manual",
        "jurisdiccion": "Nacional",
        "titulo": "Manual CalTur: Buenas Prácticas Ambientales para Establecimientos de Hospedaje"
    },
    {
        "filename": "MINCETUR_Manual_Ambiental_Transporte.pdf",
        "url": "https://sinia.minam.gob.pe/sites/default/files/siar-huancavelica/archivos/public/docs/manual_de_buenas_practicas_ambientales_para_el_servicio_de_transporte_turistico_terrestre.pdf",
        "entidad_emisora": "MINCETUR",
        "nivel_legal": "Manual",
        "jurisdiccion": "Nacional",
        "titulo": "Manual CalTur: Buenas Prácticas en Transporte Turístico Terrestre"
    },
    {
        "filename": "PROMPERU_Perfil_Vacacionista_2019.pdf",
        "url": "https://www.promperu.gob.pe/TurismoIn/archivos/CifrasPdf/PVN%202019%20-%20Publicacion%20-%20Perfil%20del%20Vacacionista%20Nacional.pdf",
        "entidad_emisora": "PROMPERÚ",
        "nivel_legal": "Estudio Técnico",
        "jurisdiccion": "Nacional",
        "titulo": "Estudio de Demanda: Perfil del Vacacionista Nacional 2019"
    },
    {
        "filename": "MEF_Directiva_Invierte_pe.pdf",
        "url": "https://www.mef.gob.pe/es/normatividad-inv-publica/instrumento/directivas/19114-resolucion-directoral-n-001-2019-ef-63-01-2/file",
        "entidad_emisora": "MEF",
        "nivel_legal": "Directiva",
        "jurisdiccion": "Nacional",
        "titulo": "Directiva General del Sistema Nacional de Inversiones Invierte.pe"
    },
    {
        "filename": "MEF_Guia_Proyectos_Turismo.pdf",
        "url": "https://www.mef.gob.pe/contenidos/inv_publica/docs/instrumentos_metod/turismo/Guia_de_turismo.pdf",
        "entidad_emisora": "MEF",
        "nivel_legal": "Guía Metodológica",
        "jurisdiccion": "Nacional",
        "titulo": "Guía Metodológica para la Formulación de Proyectos de Turismo"
    },
    {
        "filename": "MEF_Ficha_Tecnica_Cultura_Turismo.pdf",
        "url": "https://www.mef.gob.pe/contenidos/inv_publica/docs/ficha_tecnica/cultura/instructivo.pdf",
        "entidad_emisora": "MEF",
        "nivel_legal": "Instructivo",
        "jurisdiccion": "Nacional",
        "titulo": "Instructivo de Ficha Técnica Simplificada Sector Cultura/Turismo"
    },
    {
        "filename": "GERCETUR_PERTUR_Cusco.pdf",
        "url": "https://cdn.www.gob.pe/uploads/document/file/836566/229526057450009451620200615-9105-10wh1zo.pdf",
        "entidad_emisora": "GERCETUR",
        "nivel_legal": "Plan Regional",
        "jurisdiccion": "Regional Cusco",
        "titulo": "Plan Estratégico Regional de Turismo Cusco (PERTUR)"
    },
    {
        "filename": "GERCETUR_TUPA_Cusco.pdf",
        "url": "https://copesco.gob.pe/attach/PTE/repositorio/TUPA-GORE-CUSCO.pdf",
        "entidad_emisora": "GERCETUR",
        "nivel_legal": "TUPA",
        "jurisdiccion": "Regional Cusco",
        "titulo": "TUPA del Gobierno Regional de Cusco"
    },
    {
        "filename": "MINCUL_Ley_28296.pdf",
        "url": "https://leyes.congreso.gob.pe/Documentos/2016_2021/Dictamenes/Proyectos_de_Ley/05934DC05MAY20210708.pdf",
        "entidad_emisora": "MINCUL",
        "nivel_legal": "Ley",
        "jurisdiccion": "Nacional",
        "titulo": "Ley General de Patrimonio Cultural"
    },
    {
        "filename": "MINCUL_SERNANP_Plan_Maestro_Machupicchu.pdf",
        "url": "https://transparencia.cultura.gob.pe/sites/default/files/transparencia/2026/03/resoluciones-ministeriales/resolucion-ministerial-ndeg-000075-2026-mc-anexo-plan-maestro-mcch.pdf",
        "entidad_emisora": "MINCUL / SERNANP",
        "nivel_legal": "Plan Maestro",
        "jurisdiccion": "Local Machupicchu",
        "titulo": "Plan Maestro del Santuario Histórico de Machupicchu 2026-2031"
    },
    {
        "filename": "SERNANP_Turismo_Sostenible.pdf",
        "url": "https://visitaareasnaturales.sernanp.gob.pe/wp-content/uploads/2022/01/DT_Turismo_final200121.pdf",
        "entidad_emisora": "SERNANP",
        "nivel_legal": "Documento de Trabajo",
        "jurisdiccion": "Nacional",
        "titulo": "Integración del Turismo Sostenible en ANPs"
    },
    {
        "filename": "SERNANP_Plan_Sitio_Ampay.pdf",
        "url": "https://sis.sernanp.gob.pe/biblioteca/descargarPublicacionAdjunto.action?strIdInterno=75750825209317363214657289660577056043",
        "entidad_emisora": "SERNANP",
        "nivel_legal": "Plan de Sitio",
        "jurisdiccion": "Local Ampay",
        "titulo": "Plan de Sitio del Santuario Nacional Ampay"
    },
    {
        "filename": "SERNANP_Registro_Guias_Inka.pdf",
        "url": "https://sis.sernanp.gob.pe/serviciotur/media/documentos-formato?file=media/caminosinca/comunicado-proceso-inscripcion-periodos20242026-20240206053506981.pdf",
        "entidad_emisora": "SERNANP",
        "nivel_legal": "Comunicado",
        "jurisdiccion": "Local Machupicchu",
        "titulo": "Registro de Guías para la Red de Caminos Inka"
    },
    {
        "filename": "INDECOPI_DS_011_2011_PCM.pdf",
        "url": "https://www.inei.gob.pe/media/libro_reclamaciones/DS011_2011_PCM.pdf",
        "entidad_emisora": "INDECOPI",
        "nivel_legal": "Decreto Supremo",
        "jurisdiccion": "Nacional",
        "titulo": "Reglamento del Libro de Reclamaciones"
    },
    {
        "filename": "INDECOPI_Sanciones.pdf",
        "url": "https://consumidor.gob.pe/wp-content/uploads/2020/07/LibroDeReclamaciones.pdf",
        "entidad_emisora": "INDECOPI",
        "nivel_legal": "Metodología",
        "jurisdiccion": "Nacional",
        "titulo": "Metodología y Graduación de Sanciones Administrativas al Consumidor"
    },
    {
        "filename": "SUTRAN_Transporte_Terrestre.pdf",
        "url": "http://www.sutran.gob.pe/wp-content/uploads/2015/08/convenio-peru-ecuador.pdf",
        "entidad_emisora": "SUTRAN",
        "nivel_legal": "Acuerdo Binacional",
        "jurisdiccion": "Nacional",
        "titulo": "Acuerdo Binacional y Control Fronterizo de Transporte"
    },
    {
        "filename": "OSINERGMIN_Seguridad_Hidrocarburos.pdf",
        "url": "https://www.osinergmin.gob.pe/seccion/centro_documental/PlantillaMarcoLegalBusqueda/Reglamento%20de%20Seguridad%20para%20las%20Actividades%20de%20Hidrocarburos%20y%20modificaci%C3%B3n%20de%20diversas%20disposiciones.pdf",
        "entidad_emisora": "OSINERGMIN",
        "nivel_legal": "Reglamento",
        "jurisdiccion": "Nacional",
        "titulo": "Reglamento de Seguridad para Actividades de Hidrocarburos"
    },
    {
        "filename": "MUNICIPIO_Ordenanza_Tingo_Maria.pdf",
        "url": "https://munitingomaria.gob.pe/sisarchivo//download.php?file=uploads/Ordenanzas%20municipales/ORDENANZA%20MUNICIPAL%20N%C2%B0015-2025-MPLP.pdf",
        "entidad_emisora": "MUNICIPIO",
        "nivel_legal": "Ordenanza",
        "jurisdiccion": "Local Tingo Maria",
        "titulo": "Ordenanza Local de Zonificación"
    },
    {
        "filename": "MINSA_Directivas_Salud.pdf",
        "url": "http://www.dirislimaeste.gob.pe/virtual2/capacitaciones/anticorrup/libro-reclamaciones-salud.pdf",
        "entidad_emisora": "MINSA",
        "nivel_legal": "Directiva",
        "jurisdiccion": "Nacional",
        "titulo": "Directivas de Salud y Prevención Epidemiológica"
    },
    {
        "filename": "POLTUR_Mapeo_Emergencias.pdf",
        "url": "https://visitaareasnaturales.sernanp.gob.pe/wp-content/uploads/2024/05/MAPA-CIRCUITO-TURISTICO-NORTE-RNPAR.pdf",
        "entidad_emisora": "POLTUR",
        "nivel_legal": "Mapa de Riesgo",
        "jurisdiccion": "Local Paracas",
        "titulo": "Modelo de Mapeo y Directorio de Emergencias Paracas"
    }
]

def main():
    print(f"[*] Iniciando descarga de documentos gubernamentales...")
    
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"[*] Creado directorio: {TARGET_DIR}")

    # Guardar metadata
    metadata_dir = os.path.dirname(METADATA_FILE)
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)
        
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(DOCUMENTS, f, indent=4, ensure_ascii=False)
    print(f"[*] Archivo de metadatos guardado en {METADATA_FILE}")

    # Descargar PDFs
    for doc in DOCUMENTS:
        file_path = os.path.join(TARGET_DIR, doc['filename'])
        if os.path.exists(file_path):
            print(f"    [SKIP] Ya existe: {doc['filename']}")
            continue
            
        print(f"    [DOWNLOADING] {doc['filename']}...")
        try:
            req = urllib.request.Request(
                doc['url'], 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            with urllib.request.urlopen(req, timeout=30) as response, open(file_path, 'wb') as out_file:
                data = response.read()
                out_file.write(data)
            print(f"    [OK] Descargado: {doc['filename']}")
        except Exception as e:
            print(f"    [ERROR] No se pudo descargar {doc['filename']}: {e}")

    print(r"[*] Proceso finalizado. Verifica los archivos en C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\MODULOS TURISMO")

if __name__ == "__main__":
    main()
