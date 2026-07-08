import json
import os
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

def clean_sales_dna():
    input_path = os.path.join("data", "knowledge", "max_sales_dna.json")
    output_path = os.path.join("data", "knowledge", "max_sales_dna_cleaned.json")
    
    print("=========================================================================")
    print("🧹 LIFEXTREME AI: PURIFICADOR DE ADN DE VENTAS (RAG CLEANER)")
    print("=========================================================================\n")
    
    if not os.path.exists(input_path):
        print(f"❌ Error: No se encontró el archivo en {input_path}")
        return
        
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    print(f"📊 Analizando {len(raw_data)} interacciones crudas de WhatsApp...")
    
    cleaned_data = []
    junk_count = 0
    
    # Palabras clave para detectar el tipo de escenario
    objections = ["no me acepto", "retraso", "cancelaron", "problema", "miedo", "duda"]
    logistics = ["aeropuerto", "hotel", "equipaje", "vuelo", "pasaporte", "recojo", "hora"]
    closing = ["pago", "paypal", "abonar", "reserva", "confirmar"]
    
    for item in raw_data:
        ctx = item.get("context", "").strip()
        resp = item.get("response", "").strip()
        
        # 1. Filtros de Basura (Noise Reduction)
        if len(ctx) < 15 and len(resp) < 15:
            junk_count += 1
            continue
            
        if "<Multimedia omitido>" in ctx or "<Multimedia omitido>" in resp:
            junk_count += 1
            continue
            
        if "Eliminaste este mensaje" in resp or "Eliminaste este mensaje" in ctx:
            junk_count += 1
            continue
            
        if not ctx or not resp:
            junk_count += 1
            continue
            
        # 2. Reestructuración a "Escenario de Venta"
        tags = []
        ctx_lower = ctx.lower()
        
        if any(word in ctx_lower for word in objections):
            tags.append("Manejo_de_Objeciones")
        if any(word in ctx_lower for word in logistics):
            tags.append("Logistica_y_Operaciones")
        if any(word in ctx_lower for word in closing):
            tags.append("Cierre_de_Venta")
            
        if not tags:
            tags.append("Informacion_General")
            
        clean_item = {
            "escenario_id": f"SCENARIO_{len(cleaned_data)+1}",
            "intencion_cliente": ctx,
            "respuesta_experta": resp,
            "etiquetas_venta": tags,
            "longitud_contexto": len(ctx)
        }
        
        # Filtro final: Solo guardamos si la respuesta experta tiene sustancia (más de 20 caracteres)
        # Esto evita que MAX aprenda a responder con "Ok gracias"
        if len(resp) > 20:
            cleaned_data.append(clean_item)
        else:
            junk_count += 1
            
    # Ordenamos por longitud de contexto (las preguntas más largas suelen tener más valor para el RAG)
    cleaned_data.sort(key=lambda x: x["longitud_contexto"], reverse=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4, ensure_ascii=False)
        
    print(f"🗑️ Se eliminaron {junk_count} interacciones basura (Multimedia, 'Ok', 'Gracias').")
    print(f"💎 Se rescataron y estructuraron {len(cleaned_data)} Escenarios de Venta de Alto Valor.")
    print(f"✅ Archivo RAG purificado guardado en: {output_path}")
    print("=========================================================================")

if __name__ == "__main__":
    time.sleep(1)
    clean_sales_dna()
