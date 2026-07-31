import time
import sys
import os
import random
from main import scrape_places, save_places_to_csv

def main():
    print("==========================================================")
    print("🌍 LIFEXTREME B2B: BARRIDO NACIONAL DE PROSPECTOS")
    print("==========================================================\n")
    print("Iniciando escaneo masivo del mercado de turismo de aventura peruano...")
    
    # Matriz de Búsqueda Nacional (Alineada con los 6 departamentos de Lifextreme)
    destinos = [
        "Amazonas", 
        "Ancash", 
        "Arequipa", 
        "Cusco", 
        "Lima",
        "Piura"
    ]
    
    keywords = [
        "Operador de canotaje",
        "Agencia de trekking",
        "Operador de deportes de aventura"
    ]
    
    output_file = "../../Lifextreme_B2B_Nacional_Bruto.csv"
    
    # Eliminar el archivo viejo si existe para empezar fresco
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
            print(f"[*] Archivo anterior {output_file} eliminado.")
        except Exception as e:
            print(f"[!] No se pudo eliminar el archivo anterior: {e}")

    total_prospects = 0
    cantidad_por_busqueda = 30 # Limitamos a 30 por nicho para no saturar y evitar bloqueos

    print(f"Se realizarán {len(destinos) * len(keywords)} búsquedas en total.\n")
    
    for destino in destinos:
        print(f"\n📍 BARRIDO EN: {destino.upper()}")
        print("--------------------------------------------------")
        
        for keyword in keywords:
            busqueda_exacta = f"{keyword} en {destino}"
            print(f"🔍 Buscando: '{busqueda_exacta}'")
            
            try:
                # Extraer datos usando el navegador fantasma
                lugares = scrape_places(busqueda_exacta, total=cantidad_por_busqueda)
                
                if lugares:
                    # Guardamos en modo append (agregar al final)
                    save_places_to_csv(lugares, output_file, append=True)
                    total_prospects += len(lugares)
                    print(f"   ✅ Se encontraron {len(lugares)} resultados.")
                else:
                    print("   ⚠️ No se encontraron resultados o el navegador fue bloqueado.")
                    
            except Exception as e:
                print(f"   ❌ Error en la búsqueda: {e}")
                
            # Pausa de seguridad anti-baneo de Google (entre 10 y 20 segundos)
            tiempo_espera = random.randint(10, 20)
            print(f"   ⏳ Pausa de seguridad anti-bot: {tiempo_espera} segundos...")
            time.sleep(tiempo_espera)

    print("\n==========================================================")
    print("🎉 BARRIDO NACIONAL COMPLETADO")
    print("==========================================================")
    print(f"Total de prospectos extraídos: {total_prospects}")
    print(f"Archivo guardado en: Lifextreme_B2B_Nacional_Bruto.csv")
    print("Siguiente paso: Ejecutar cerebro_operator_filter.py para limpiar la data.")

if __name__ == "__main__":
    main()
