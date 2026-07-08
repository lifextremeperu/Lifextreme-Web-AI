import os
import sys
import json
import argparse
from pathlib import Path

def validate_json_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {"status": "ERROR", "reason": f"No se pudo leer o parsear JSON: {e}", "fqsas_validas": 0, "fqsas_totales": 0}

    # Asume estructura de run_miner_latam.py:
    # {"destino_id": "...", "modulo_contexto": "...", "fqsas": { "1_Precios...": [ { "pregunta": "...", "respuesta": "..."} ] } }
    
    if "fqsas" not in data:
        return {"status": "ERROR", "reason": "No contiene llave 'fqsas'", "fqsas_validas": 0, "fqsas_totales": 0}
        
    fqsas_dict = data["fqsas"]
    fqsas_totales = 0
    fqsas_validas = 0
    errores = []
    
    for angulo, preguntas in fqsas_dict.items():
        if not isinstance(preguntas, list):
            errores.append(f"Ángulo {angulo} no contiene un array de preguntas.")
            continue
            
        for item in preguntas:
            fqsas_totales += 1
            if not isinstance(item, dict):
                errores.append(f"Elemento no es un diccionario en {angulo}")
                continue
                
            pregunta = item.get("pregunta", "")
            respuesta = item.get("respuesta", "")
            
            # Validación básica de calidad
            if len(pregunta) < 10 or len(respuesta) < 20:
                errores.append(f"Respuesta muy corta o vacía en {angulo}: {pregunta}")
            elif "ERROR" in pregunta.upper() or "ERROR" in respuesta.upper():
                errores.append(f"Error detectado en la extracción de {angulo}")
            else:
                fqsas_validas += 1

    if fqsas_totales == 0:
        return {"status": "FAIL", "reason": "Cero FQSAs extraídas.", "fqsas_validas": 0, "fqsas_totales": 0, "errores": errores}
        
    porcentaje_exito = (fqsas_validas / fqsas_totales) * 100
    status = "PASS" if porcentaje_exito > 80 else "WARNING"
    if porcentaje_exito < 50:
        status = "FAIL"
        
    return {
        "status": status,
        "fqsas_validas": fqsas_validas,
        "fqsas_totales": fqsas_totales,
        "porcentaje_exito": f"{porcentaje_exito:.1f}%",
        "errores": errores[:5] # mostrar max 5 errores por archivo para no saturar
    }

def main():
    parser = argparse.ArgumentParser(description="Ejecutar el Agente Verificador de Calidad (QA)")
    parser.add_argument("departamento", help="Nombre del departamento a auditar")
    parser.add_argument("--pais", default="Perú", help="País")
    args = parser.parse_args()
    
    departamento = args.departamento.lower()
    pais = args.pais.lower().replace(" ", "")
    
    print(f"==================================================")
    print(f"AGENTE QA VERIFICADOR - {departamento.upper()}, {pais.upper()}")
    print(f"==================================================")
    
    directorio_base = Path(f"data/knowledge/{pais}/{departamento}")
    directorio_fqsas = directorio_base / "fqsas_deep"
    
    if not directorio_fqsas.exists():
        print(f"[-] ERROR: El directorio {directorio_fqsas} no existe. No se ha extraído nada aún.")
        sys.exit(1)
        
    archivos = list(directorio_fqsas.glob("*.json"))
    if not archivos:
        print(f"[-] ERROR: No hay archivos JSON en {directorio_fqsas}.")
        sys.exit(1)
        
    print(f"[+] Auditando {len(archivos)} módulos extraídos...")
    
    reporte_global = {
        "pais": pais,
        "departamento": departamento,
        "modulos_evaluados": len(archivos),
        "modulos_aprobados": 0,
        "modulos_fallidos": 0,
        "modulos_advertencia": 0,
        "fqsas_totales_validadas": 0,
        "fqsas_totales_esperadas": 0,
        "detalles": {}
    }
    
    for archivo in archivos:
        resultado = validate_json_content(archivo)
        modulo_id = archivo.stem
        
        reporte_global["detalles"][modulo_id] = resultado
        reporte_global["fqsas_totales_validadas"] += resultado.get("fqsas_validas", 0)
        reporte_global["fqsas_totales_esperadas"] += resultado.get("fqsas_totales", 0)
        
        if resultado["status"] == "PASS":
            reporte_global["modulos_aprobados"] += 1
            print(f"    [OK] {modulo_id} -> {resultado['fqsas_validas']}/{resultado['fqsas_totales']} validas")
        elif resultado["status"] == "WARNING":
            reporte_global["modulos_advertencia"] += 1
            print(f"    [WARN] {modulo_id} -> Calidad media ({resultado['porcentaje_exito']})")
        else:
            reporte_global["modulos_fallidos"] += 1
            print(f"    [FAIL] {modulo_id} -> Errores detectados: {resultado.get('reason', 'Calidad insuficiente')}")
            
    print(f"\n[+] Auditoría Completada.")
    print(f"    Aprobados: {reporte_global['modulos_aprobados']}")
    print(f"    Advertencias: {reporte_global['modulos_advertencia']}")
    print(f"    Fallidos: {reporte_global['modulos_fallidos']}")
    print(f"    Total FQSAs viables: {reporte_global['fqsas_totales_validadas']}/{reporte_global['fqsas_totales_esperadas']}")
    
    with open(directorio_base / "qa_report.json", "w", encoding="utf-8") as f:
        json.dump(reporte_global, f, ensure_ascii=False, indent=4)
        
    print(f"[+] Reporte guardado en {directorio_base / 'qa_report.json'}")
    
    if reporte_global["modulos_fallidos"] > 0:
        print("\n[!] ALERTA B2B: Hay módulos fallidos. Revisa el reporte y considera relanzar la minería.")
        # Opcional: salir con código de error si se desea bloquear el pipeline
        # sys.exit(1)

if __name__ == "__main__":
    main()
