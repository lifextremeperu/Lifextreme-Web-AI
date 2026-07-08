import sys, json

sys.stdout.reconfigure(encoding='utf-8')

JSONL = r'data/cixtur_knowledge.jsonl'

knowledge = []
with open(JSONL, 'r', encoding='utf-8') as f:
    for line in f:
        knowledge.append(json.loads(line.strip()))

print(f'Base cargada: {len(knowledge)} registros')
print(f'Fuentes: {len(set(k["source"] for k in knowledge))} destinos')
print()

def buscar(pregunta, top=3):
    pregunta_lower = pregunta.lower()
    palabras = set(pregunta_lower.replace("?","").replace("¿","").split())
    resultados = []
    for item in knowledge:
        prompt_lower = item['prompt'].lower()
        # Dar mas peso a palabras largas o clave
        score = sum(1 for p in palabras if len(p) > 3 and p in prompt_lower)
        if score > 0:
            resultados.append((score, item))
    resultados.sort(key=lambda x: x[0], reverse=True)
    return resultados[:top]

preguntas = [
    '¿Cuánto cuesta el boleto turistico del Cusco?',
    '¿Qué necesito llevar para hacer rafting?',
    '¿Cómo llego a Machu Picchu en tren?',
    '¿Qué es el Valle Rojo?',
    '¿Cuánto tiempo dura el Camino Inca?'
]

for pregunta in preguntas:
    print(f'PREGUNTA: {pregunta}')
    resultados = buscar(pregunta)
    if resultados:
        score, item = resultados[0]
        print(f'FUENTE: {item["source"]} (relevancia: {score})')
        print(f'PROMPT ENCONTRADO: {item["prompt"]}')
        # Imprimimos hasta 300 caracteres de la respuesta
        resp = item["completion"]
        if len(resp) > 300:
            resp = resp[:300] + '...'
        print(f'RESPUESTA: {resp}')
    else:
        print('Sin resultado')
    print('-' * 60)
