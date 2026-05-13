import os, sys, subprocess

sys.stdout.reconfigure(encoding='utf-8')

SOURCE = r'D:\HUB-CUSCO-2026\apps\data\knowledge\lifextreme\sources'
BUCKET = 'gs://lifextreme-knowledge-cusco'
GSUTIL = r'C:\Users\ASUS\AppData\Local\Google\google-cloud-sdk\bin\gsutil.cmd'

env = os.environ.copy()
env['CLOUDSDK_PYTHON'] = r'C:\Python313\python.exe'

reglas = {
    'legal-normativas': ['reglamento', 'manual', 'protocolo', 'rm_nro', 'atta'],
    'inteligencia-mercado': ['perfil', 'pentur', 'plan_estrate', 'informe'],
    'itinerarios-tours': ['inka jungle', 'inti punku', 'laguna', 'machupicchu', 'treek', 'waqrapukara']
}

print('Iniciando sincronizacion total de 176 PDFs...')
archivos_subidos = 0
archivos_omitidos = 0

for root, dirs, files in os.walk(SOURCE):
    for file in files:
        if not file.lower().endswith('.pdf'):
            continue
            
        file_path = os.path.join(root, file)
        destino = 'otros-documentos'
        
        for carpeta, keywords in reglas.items():
            if any(kw in file.lower() for kw in keywords):
                destino = carpeta
                break
                
        dest_path = f'{BUCKET}/{destino}/{file}'
        
        try:
            # -n significa 'no sobreescribir si ya existe en destino'
            # Esto acelera el proceso omitiendo los 47 que ya subimos
            result = subprocess.run([GSUTIL, 'cp', '-n', file_path, dest_path], 
                                    env=env, capture_output=True, text=True)
            
            if "Skipping existing item" in result.stderr or "Skipping existing item" in result.stdout:
                archivos_omitidos += 1
            elif result.returncode == 0:
                archivos_subidos += 1
                if archivos_subidos % 10 == 0:
                    print(f'Procesados {archivos_subidos} archivos nuevos...')
            else:
                print(f'Error subiendo {file}')
                
        except Exception as e:
            print(f'Error critico con {file}')

print(f'\nRESUMEN FINAL:')
print(f'- Archivos nuevos subidos: {archivos_subidos}')
print(f'- Archivos ya existentes (omitidos): {archivos_omitidos}')
print(f'- Total en Google Cloud: {archivos_subidos + archivos_omitidos}')
