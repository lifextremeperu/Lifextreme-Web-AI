import requests

preguntas = [
    'DS 006-2016-MINCETUR canotaje nivel IV Urubamba certificaciones guias seguridad paridad OTAs',
    'Lodge ANP Booking alerta paridad valor añadido SERNANP trekking',
    'Barranquismo cascadas Chucuito riesgos salud infraestructura contingencia canales directos',
    'Kayak avistamiento ANP norte permisos SERNANP Autoridad Maritima Turismo Emprende paridad',
    'Atuncolla bloqueo carreteras plan B gastronomia contingencia soles exencion responsabilidad DS 005-2016',
    'Infracciones turismo agencia sin categorizacion sanciones dark marketing OTAs',
    'La Punta Chucuito reglas locales prohibiciones protocolo seguridad valor añadido',
    'Hospedaje rural Startup Peru Cambio Climatico infraestructura sostenibilidad glamping paridad',
    'Walk-in hostal Valle Sagrado Narrow Parity Booking efectivo desayuno disparidad',
    'Paquete norte glamping canopy avistamiento ballenas SERNANP clima paridad Visibility Booster'
]

def fetch_context():
    with open('rag_context.txt', 'w', encoding='utf-8') as out:
        for i, q in enumerate(preguntas, 1):
            out.write(f'=== PREGUNTA {i} ===\nQuery: {q}\n')
            try:
                res = requests.post(
                    'http://localhost:11434/api/embeddings', 
                    json={'model': 'nomic-embed-text', 'prompt': q},
                    timeout=30.0
                )
                vector = res.json().get('embedding')
            except Exception as e:
                out.write(f'Error embedding: {e}\n')
                continue
                
            if vector:
                try:
                    qdrant_res = requests.post(
                        'http://localhost:6333/collections/Lifextreme_Knowledge/points/search',
                        json={'vector': vector, 'limit': 3, 'with_payload': True},
                        timeout=30.0
                    )
                    hits = qdrant_res.json().get('result', [])
                    for hit in hits:
                        p = hit.get('payload', {})
                        score = hit.get('score', 0)
                        out.write(f'- FUENTE: {p.get("source")} (Score: {score:.3f})\n')
                        out.write(f'{p.get("text_content", "")[:600]}...\n\n')
                except Exception as e:
                    out.write(f'Error qdrant: {e}\n')
    print('Contexto guardado en rag_context.txt')

if __name__ == '__main__':
    fetch_context()
