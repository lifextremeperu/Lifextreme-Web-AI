import json

with open('qdrant_inventory.json', encoding='utf-8') as f:
    data = json.load(f)
    
fuentes = data.get('fuentes', {})
files = list(fuentes.keys())

pertur_files = [f for f in files if 'PERTUR' in f.upper() or 'PLAN_ESTRATEGICO' in f.upper()]
faq_files = [f for f in files if 'FAQ' in f.upper() or 'MANUAL' in f.upper()]
other_files = [f for f in files if f not in pertur_files and f not in faq_files]

print(f'Total archivos mapeados: {len(files)}')

print(f'\n--- PLANES ESTRATÉGICOS (Departamentos) [{len(pertur_files)}] ---')
for f in sorted(pertur_files): 
    print(f" - {f} ({fuentes[f]['count']} vectores)")

print(f'\n--- FAQs y MANUALES [{len(faq_files)}] ---')
for f in sorted(faq_files): 
    print(f" - {f} ({fuentes[f]['count']} vectores)")

print(f'\n--- OTROS ARCHIVOS PRINCIPALES (Top 25) ---')
sorted_others = sorted(other_files, key=lambda x: fuentes[x]['count'], reverse=True)
for f in sorted_others[:25]:
    print(f" - {f} ({fuentes[f]['count']} vectores)")
