import requests
from qdrant_client import QdrantClient

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
    client = QdrantClient(url='http://localhost:6333')
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
                resultados = client.search(
                    collection_name='Lifextreme_Knowledge',
                    query_vector=vector,
                    limit=4
                )
                for hit in resultados:
                    p = hit.payload
                    out.write(f'- FUENTE: {p.get("source")} (Score: {hit.score:.3f})\n')
                    out.write(f'{p.get("text_content", "")[:600]}...\n\n')
    print('Contexto guardado en rag_context.txt')

if __name__ == '__main__':
    fetch_context()
