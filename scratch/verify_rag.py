import os, json, glob
from collections import defaultdict
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

print('Consultando Supabase...')
limit = 1000
all_data = []
for i in range(100):
    res = supabase.table('knowledge_vectors').select('id, region, modulo_nombre').range(i*limit, (i+1)*limit - 1).execute()
    all_data.extend(res.data)
    if len(res.data) < limit:
        break

db_counts = defaultdict(int)
for d in all_data:
    key = f"{d.get('region', 'UNKNOWN')} - {d.get('modulo_nombre', 'UNKNOWN')}"
    db_counts[key] += 1

print('--- DATOS EN SUPABASE ---')
for k, v in sorted(db_counts.items()):
    print(f'{k}: {v} vectores')
print(f'TOTAL VECTORES: {len(all_data)}')

local_counts = defaultdict(int)

for p in Path('data/knowledge/peru').rglob('*.json'):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            fqsas_dict = data.get('fqsas', {})
            count = sum(len(lst) for lst in fqsas_dict.values() if isinstance(lst, list))
            region = p.parents[1].name.lower()
            mod = data.get('modulo_contexto', data.get('modulo_nombre', 'UNKNOWN'))
            local_counts[f'{region} - {mod}'] += count
    except: pass

try:
    with open('data/knowledge/infraestructura_seed.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for d in data:
            region = d.get('ubicacion', {}).get('departamento', 'Perú').lower()
            local_counts[f'{region} - InfraestructuraAventura'] += 1
except: pass

print('\n--- DATOS LOCALES ---')
for k, v in sorted(local_counts.items()):
    print(f'{k}: {v} FQSAs/Items')
print(f'TOTAL LOCAL: {sum(local_counts.values())}')

print('\n--- FALTAN POR VECTORIZAR ---')
missing_found = False
for k, v in sorted(local_counts.items()):
    diff = v - db_counts.get(k, 0)
    if diff > 0:
        print(f'Faltan {diff} de {k}')
        missing_found = True
if not missing_found:
    print('Todo el contenido local de Peru e Infraestructura esta 100% sincronizado.')
