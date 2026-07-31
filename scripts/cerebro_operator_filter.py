import pandas as pd
import json
import os
import sys
try:
    from langchain_community.chat_models import ChatOllama
    from langchain.prompts import PromptTemplate
except ImportError:
    print("Falta instalar dependencias. Ejecuta: pip install langchain-community langchain-ollama pandas")
    sys.exit(1)

def main():
    print("==========================================================")
    print("🧠 CEREBRO LIFEXTREME: FILTRO DE OPERADORES DIRECTOS (B2B)")
    print("==========================================================\n")
    
    input_file = "../Lifextreme_B2B_Prospects.csv"
    output_file = "../Lifextreme_B2B_Operadores_Directos_Verificados.csv"
    
    if not os.path.exists(input_file):
        print(f"❌ No se encontró el archivo {input_file}. Ejecuta el scraper primero.")
        sys.exit(1)
        
    print("[1/3] Cargando la base de datos de prospectos en bruto...")
    df = pd.read_csv(input_file)
    print(f"      Se encontraron {len(df)} prospectos totales.\n")
    
    print("[2/3] Conectando al Cerebro de IA Local (Llama 3)...")
    try:
        # Iniciamos Ollama local.
        llm = ChatOllama(model="llama3", temperature=0.0)
    except Exception as e:
        print("❌ Error conectando a Ollama. Asegúrate de que esté corriendo (ollama run llama3).")
        sys.exit(1)
        
    prompt = PromptTemplate(
        input_variables=["nombre", "tipo", "reviews"],
        template="""Eres un analista experto del MINCETUR y asesor B2B de Lifextreme. 
Tu trabajo es distinguir a los verdaderos "Operadores Directos de Aventura" de las simples "Agencias Tercerizadoras".
Un operador directo suele llamarse "Operador de aventura", "Escuela de surf", "Centro de canotaje", "Trekking", "Expedition", etc.
Una agencia tercerizadora suele llamarse "Travel", "Agencia de viajes y turismo", "Tours genéricos".

Analiza esta empresa:
- Nombre: {nombre}
- Tipo de Negocio en Google: {tipo}
- Cantidad de Reseñas: {reviews}

¿Es esta empresa altamente probable de ser un OPERADOR DIRECTO DE AVENTURA con equipos y logística propia?
Responde ÚNICAMENTE con la palabra "SI" o "NO". No agregues ninguna otra palabra.
"""
    )
    
    print("[3/3] La Inteligencia Artificial está evaluando cada empresa una por una...")
    
    resultados_filtrados = []
    
    for index, row in df.iterrows():
        nombre = str(row.get('name', 'Desconocido'))
        tipo = str(row.get('place_type', 'No especificado'))
        reviews = str(row.get('reviews_count', '0'))
        
        # Saltamos si no hay nombre válido
        if nombre == "nan" or nombre == "Desconocido":
            continue
            
        print(f"  Analizando: {nombre}...", end=" ")
        
        try:
            # Consultar a la IA
            _input = prompt.format(nombre=nombre, tipo=tipo, reviews=reviews)
            respuesta = llm.predict(_input).strip().upper()
            
            # Limpiamos la respuesta de la IA (a veces agregan puntos o espacios)
            es_directo = "SI" in respuesta or "YES" in respuesta or "SÍ" in respuesta
            
            if es_directo:
                print("✅ APROBADO (Operador Directo)")
                resultados_filtrados.append(row)
            else:
                print("❌ DESCARTADO (Revendedor / Genérico)")
                
        except Exception as e:
            print(f"⚠️ Error al analizar {nombre}: {e}")
            
    # Guardar resultados
    df_filtrado = pd.DataFrame(resultados_filtrados)
    if not df_filtrado.empty:
        df_filtrado.to_csv(output_file, index=False)
        print(f"\n🎉 ¡PROCESO COMPLETADO! Se encontraron {len(df_filtrado)} OPERADORES DIRECTOS reales.")
        print(f"   La lista dorada se ha guardado en: {output_file}")
    else:
        print("\n⚠️ Ninguna agencia pasó el estricto filtro del MINCETUR.")

if __name__ == "__main__":
    main()
