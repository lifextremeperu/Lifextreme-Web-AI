import os
import sys
import json
import traceback
from datetime import datetime
from openai import OpenAI

# Para forzar codificación UTF-8 en consola
sys.stdout.reconfigure(encoding='utf-8')

# Constantes
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'templates', 'auditor_template.html')
REPORT_DIR = os.path.join(os.path.dirname(__file__), '..', 'reportes_b2b')

def obtener_color_por_score(score):
    if score >= 80: return "success-glow"
    if score >= 50: return "warning-glow"
    return "critical-glow"

def generar_reporte():
    print("======================================================")
    print("🚀 LIFEXTREME AI - GENERADOR DE AUDITORÍA B2B ENTERPRISE")
    print("======================================================")
    
    agencia = input("1. Nombre de la Agencia Cliente: ")
    print("2. Pega el texto principal de su web o la lista de tours que venden.")
    print("   (Ej: 'Vendemos Camino Inca 4 dias, Salkantay y Cuatrimotos Maras'):")
    tours = input("   > ")
    
    print("\n[+] Inicializando Cerebro Lifextreme (Llama 3)...")
    print("[+] Cruzando datos con los 50 módulos de conocimiento...")
    
    # Cliente Ollama Local
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
    
    prompt_sistema = """Eres el Auditor B2B Experto de Lifextreme.
    Tu tarea es analizar los tours de una agencia peruana y generar un reporte estratégico cruzando la información con las leyes del MINCETUR, SEO, y AEO.
    
    DEBES responder estrictamente en formato JSON válido con las siguientes llaves:
    {
        "seo_score": 0-100,
        "seo_analysis": "Texto de analisis SEO",
        "legal_score": 0-100,
        "legal_analysis": "Analisis de brechas legales MINCETUR para esos tours",
        "geo_score": 0-100,
        "geo_analysis": "Analisis de visibilidad IA",
        "market_analysis": "Analisis de precios y recomendacion de nuevos nichos",
        "faq_json": "Un JSON-LD valido como string de FAQPage para esos tours específicos"
    }
    No agregues texto extra fuera del JSON."""
    
    try:
        completion = client.chat.completions.create(
            model="llama3",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Agencia: {agencia}. Tours: {tours}"}
            ],
            response_format={"type": "json_object"}
        )
        
        resultado_str = completion.choices[0].message.content
        datos = json.loads(resultado_str)
        
        print("[+] Análisis completado. Fabricando el Dashboard HTML...")
        
        # Leer Plantilla
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Reemplazar variables
        html = html.replace('{{AGENCY_NAME}}', agencia)
        html = html.replace('{{SEO_SCORE}}', str(datos.get('seo_score', 0)))
        html = html.replace('{{SEO_ANALYSIS}}', datos.get('seo_analysis', ''))
        html = html.replace('{{SEO_COLOR_CLASS}}', obtener_color_por_score(datos.get('seo_score', 0)))
        
        html = html.replace('{{LEGAL_SCORE}}', str(datos.get('legal_score', 0)))
        html = html.replace('{{LEGAL_ANALYSIS}}', datos.get('legal_analysis', ''))
        html = html.replace('{{LEGAL_COLOR_CLASS}}', obtener_color_por_score(datos.get('legal_score', 0)))
        
        html = html.replace('{{GEO_SCORE}}', str(datos.get('geo_score', 0)))
        html = html.replace('{{GEO_ANALYSIS}}', datos.get('geo_analysis', ''))
        html = html.replace('{{GEO_COLOR_CLASS}}', obtener_color_por_score(datos.get('geo_score', 0)))
        
        html = html.replace('{{MARKET_ANALYSIS}}', datos.get('market_analysis', ''))
        html = html.replace('{{FAQ_JSON}}', datos.get('faq_json', ''))
        
        # Guardar reporte
        if not os.path.exists(REPORT_DIR):
            os.makedirs(REPORT_DIR)
            
        nombre_archivo = f"reporte_{agencia.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M')}.html"
        ruta_salida = os.path.join(REPORT_DIR, nombre_archivo)
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print("\n======================================================")
        print("✅ ¡DASHBOARD EMPRESARIAL GENERADO CON ÉXITO!")
        print(f"👉 ARCHIVO CREADO EN: {ruta_salida}")
        print("Instrucciones: Dale doble clic al archivo HTML para abrirlo en tu navegador.")
        print("Puedes presionar Ctrl+P para imprimirlo como PDF y enviarlo a tu cliente.")
        print("======================================================")
        
    except Exception as e:
        print(f"\n❌ Error generando el reporte: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    generar_reporte()
