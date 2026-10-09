import os
import json
from qdrant_client import QdrantClient

def generate_transnational_report():
    print("Iniciando conexión a Qdrant Local (Puerto 6333)...")
    try:
        client = QdrantClient("http://localhost:6333")
    except Exception as e:
        print(f"Error conectando a Qdrant: {e}")
        return

    # Definimos los 9 módulos de extracción
    collections = [
        ("Lifextreme_Finance_Vault", "Análisis Micro/Macro Económico y Rentabilidad"),
        ("Lifextreme_Operations_Vault", "Logística, Cierres Predictivos y Riesgos (SENAMHI/SUTRAN)"),
        ("Lifextreme_Knowledge", "Marco Regulatorio y Cumplimiento Legal (MINCETUR/TUPA)"),
        ("Marketing_PHD_Knowledge", "Comportamiento del Consumidor y Neuromarketing"),
        ("Lifextreme_Partners_Vault", "Inteligencia Competitiva B2B y Alianzas"),
        ("Lifextreme_Sales_Vault", "Estrategias de Conversión y Pricing Dinámico"),
        ("Perplexity_Knowledge", "Inteligencia de Mercados Globales y Vuelos"),
        ("Lifextreme_FQSA_Knowledge", "Fricciones del Cliente y Resolución Operativa"),
        ("Lifextreme_CEO_Vault", "Visión Transnacional y Crecimiento a 5 años")
    ]

    report_path = "Lifextreme_Reporte_Transnacional_Real.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🌐 REPORTE TRANSNACIONAL DE INTELIGENCIA TURÍSTICA (Q3)\n")
        f.write("**Emisor:** Lifextreme Big Data Analytics (Cerebro Qdrant RAG)\n")
        f.write("**Nivel de Confidencialidad:** Alto (Corporativo / B2B)\n")
        f.write("---\n\n")
        f.write("> **NOTA DEL SISTEMA:** Toda la información aquí presentada es extraída en TIEMPO REAL de los vectores alojados en el clúster local de Inteligencia Artificial.\n\n")

        for coll_name, coll_title in collections:
            f.write(f"## 📊 Módulo: {coll_title}\n")
            f.write(f"*Extrayendo datos de la colección: `{coll_name}`...*\n\n")
            
            try:
                # Extraemos 2 vectores reales usando scroll (sin necesidad de embedder)
                records, _ = client.scroll(
                    collection_name=coll_name,
                    limit=2,
                    with_payload=True,
                    with_vectors=False
                )
                
                if not records:
                    f.write("⚠️ *Colección activa pero sin vectores indexados temporalmente.*\n\n")
                    continue
                
                for idx, record in enumerate(records, 1):
                    payload = record.payload
                    # Extraer el texto principal (usualmente text, page_content, content, o la llave principal)
                    text_content = payload.get("page_content", payload.get("text", payload.get("content", str(payload))))
                    
                    # Truncar si es demasiado largo
                    if len(text_content) > 600:
                        text_content = text_content[:600] + "... [TRUNCADO POR SISTEMA]"
                        
                    f.write(f"**Vector Real #{idx} (ID: {record.id}):**\n")
                    f.write(f"> {text_content}\n\n")
                    
                    # Imprimir metadata si existe
                    meta = {k:v for k,v in payload.items() if k not in ["page_content", "text", "content"]}
                    if meta:
                        f.write(f"*- Metadata asociada: {json.dumps(meta, ensure_ascii=False)[:200]}*\n\n")
                        
            except Exception as e:
                f.write(f"⚠️ *Error al extraer vectores de {coll_name}: {e}*\n\n")
                
        f.write("---\n**FIN DEL REPORTE.** Generado exitosamente.")

    print(f"Reporte masivo generado con éxito en: {report_path}")

if __name__ == "__main__":
    generate_transnational_report()
