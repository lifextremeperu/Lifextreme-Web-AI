import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

def audit_html():
    print("=" * 50)
    print(" 🕷️ CAZA-BUGS: AUDITORÍA DE CÓDIGO WEB ")
    print("=" * 50)
    
    html_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        if 'node_modules' in root or '.git' in root or 'dist' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"[*] Escaneando {len(html_files)} archivos HTML...")
    
    issues_found = 0
    files_with_issues = 0
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        file_issues = []
        if 'javascript:void(0)' in content:
            file_issues.append("Contiene 'javascript:void(0)' (Bloquea SEO)")
        if '<title>' not in content:
            file_issues.append("Falta etiqueta <title>")
        if '<img ' in content and 'alt=' not in content:
            file_issues.append("Faltan etiquetas 'alt' en imágenes")
            
        if file_issues:
            files_with_issues += 1
            issues_found += len(file_issues)
            print(f"\n[!] Archivo: {os.path.relpath(filepath, ROOT_DIR)}")
            for issue in file_issues:
                print(f"    - {issue}")
                
    print("-" * 50)
    print(f"[✔] Auditoría terminada.")
    print(f"    - Archivos analizados: {len(html_files)}")
    print(f"    - Archivos con alertas: {files_with_issues}")
    print(f"    - Total alertas: {issues_found}")
    print("=" * 50)

if __name__ == "__main__":
    audit_html()
