import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import requests
import json
import argparse
from pathlib import Path
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "deepseek-coder:latest" # You can also use deepseek-r1 if installed

SYSTEM_PROMPT = """Eres un Ingeniero Principal de Software y Auditor de Código Senior.
Tu trabajo es revisar de manera exhaustiva el código proporcionado. Eres estricto, detallista y te enfocas en:
1. Errores Críticos y Bugs: Identifica fallos lógicos, condiciones de carrera o excepciones no manejadas.
2. Arquitectura y Diseño: Revisa principios SOLID, DRY, y acoplamiento.
3. Rendimiento y Seguridad: Inyecciones, fugas de memoria, optimizaciones.
4. Buenas Prácticas: Nombrado de variables, type hinting, legibilidad.

Devuelve tu revisión EXCLUSIVAMENTE en formato Markdown siguiendo esta estructura:

# 🕵️‍♂️ Auditoría de Código: `{filename}`

## ❌ Errores Críticos y Bugs
- (Detalla aquí si hay fallos graves. Si no, escribe "Ninguno detectado".)

## ⚠️ Advertencias y Deuda Técnica
- (Problemas menores, código repetido, falta de tipado o documentación.)

## 💡 Mejoras de Arquitectura y Refactorización
- (Cómo estructurar mejor el código, patrones de diseño recomendados.)

## ✅ Buenas Prácticas Encontradas
- (Qué se hizo bien en este código.)

## 🛠️ Snippet de Código Refactorizado (Opcional)
(Si aplica, incluye un bloque de código mostrando cómo refactorizarías la parte más crítica).
"""

def auditar_codigo(filepath, model=DEFAULT_MODEL):
    file_path = Path(filepath)
    if not file_path.exists():
        print(f"[-] ERROR: El archivo '{filepath}' no existe.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        codigo = f.read()

    print(f"==================================================")
    print(f" 🕵️‍♂️ AGENTE AUDITOR DE CÓDIGO (Modelo: {model}) ")
    print(f"==================================================")
    print(f"[+] Archivo objetivo: {file_path.name}")
    print(f"[+] Tamaño del código: {len(codigo)} caracteres")
    print(f"[+] Procesando auditoría (esto puede tardar unos minutos)...")

    prompt = SYSTEM_PROMPT.replace("{filename}", file_path.name)
    user_message = f"Por favor, audita el siguiente código fuente:\n\n```\n{codigo}\n```"

    try:
        res = requests.post(OLLAMA_URL, json={
            "model": model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False
        }, timeout=900)
        
        if res.ok:
            return res.json()['message']['content']
        else:
            print(f"[-] Error HTTP {res.status_code}: {res.text}")
            sys.exit(1)
    except Exception as e:
        print(f"[-] Error de conexión con Ollama: {e}")
        print("    Asegúrate de que Ollama está corriendo y el modelo está instalado (ej: 'ollama run deepseek-coder').")
        sys.exit(1)

def guardar_reporte(filename, content):
    base_dir = Path("docs/audits")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"audit_{Path(filename).stem}_{timestamp}.md"
    report_path = base_dir / report_name
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[✔] REPORTE GUARDADO: {report_path}")
    return report_path

def main():
    parser = argparse.ArgumentParser(description="Ejecutar el Agente Senior Auditor de Código")
    parser.add_argument("archivo", help="Ruta del archivo a auditar")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Modelo de Ollama a utilizar")
    args = parser.parse_args()
    
    reporte = auditar_codigo(args.archivo, args.model)
    guardar_reporte(args.archivo, reporte)

if __name__ == "__main__":
    main()
