import os, json, glob
from collections import defaultdict
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

print('Consultando Supabase para todos los paises...')
limit = 1000
all_data = []
for i in range(100):
    res = supabase.table('knowledge_vectors').select('id, region, modulo_nombre').range(i*limit, (i+1)*limit - 1).execute()
    all_data.extend(res.data)
    if len(res.data) < limit:
        break

db_counts = defaultdict(int)
for d in all_data:
    key = f"{d.get('region', 'UNKNOWN').lower()} - {d.get('modulo_nombre', 'UNKNOWN')}"
    db_counts[key] += 1

countries = ['argentina', 'bolivia', 'chile', 'colombia', 'ecuador', 'peru']
local_counts = defaultdict(int)

for country in countries:
    for p in Path(f'data/knowledge/{country}').rglob('*.json'):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                data = json.load(f)
                fqsas_dict = data.get('fqsas', {})
                count = sum(len(lst) for lst in fqsas_dict.values() if isinstance(lst, list))
                # For non-Peru, region might be country or country + region
                region_name = p.parents[1].name.lower()
                mod = data.get('modulo_contexto', data.get('modulo_nombre', 'UNKNOWN'))
                local_counts[f'{region_name} - {mod}'] += count
        except: pass

print('\n--- DATOS LOCALES SUDAMERICA (Y PERU) ---')
for k, v in sorted(local_counts.items()):
    # Only print non-peru regions to avoid spam
    if not k.startswith(('amazonas', 'ancash', 'apurimac', 'arequipa', 'ayacucho', 'cajamarca', 'callao', 'huancavelica', 'huanuco', 'ica', 'junin', 'junín', 'lalibertad', 'lambayeque', 'lima', 'loreto', 'madrededios', 'moquegua', 'pasco', 'piura', 'puno', 'sanmartin', 'tacna', 'tumbes', 'ucayali')):
        print(f'{k}: {v} FQSAs/Items')
        
total_local = sum(local_counts.values())
print(f'TOTAL LOCAL (TODOS LOS PAISES): {total_local}')

print('\n--- FALTAN POR VECTORIZAR DE SUDAMERICA ---')
for k, v in sorted(local_counts.items()):
    if not k.startswith(('amazonas', 'ancash', 'apurimac', 'arequipa', 'ayacucho', 'cajamarca', 'callao', 'huancavelica', 'huanuco', 'ica', 'junin', 'junín', 'lalibertad', 'lambayeque', 'lima', 'loreto', 'madrededios', 'moquegua', 'pasco', 'piura', 'puno', 'sanmartin', 'tacna', 'tumbes', 'ucayali')):
        diff = v - db_counts.get(k, 0)
        if diff > 0:
            print(f'Faltan {diff} de {k}')
