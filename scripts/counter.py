import os
import time

def count_code():
    total_lines = 0
    total_bytes = 0
    total_files = 0
    
    exclude_dirs = ['.venv', '.git', 'node_modules', '__pycache__']
    include_exts = ['.py', '.js', '.html', '.css', '.sql']
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in include_exts):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        total_lines += len(lines)
                    total_bytes += os.path.getsize(filepath)
                    total_files += 1
                except:
                    pass
                    
    print(f"Archivos: {total_files}")
    print(f"Lineas: {total_lines}")
    print(f"Bytes: {total_bytes}")
    print(f"Tokens (Aprox): {total_bytes // 4}")

count_code()
