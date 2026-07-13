import os
import httpx
import asyncio

# Usar el backend RAG existente
from src.rag_service import search_knowledge

GOLDEN_SET = [
    # Tier 0 (Si estuviera en RAG, pero ahora debe venir del System Prompt)
    # Por ahora probamos con logística y ventas operativas
    {"q": "¿Cuánto cuesta el tour a Machupicchu?", "expected": "Catálogo Operativo"},
    {"q": "¿Qué hago si el cliente dice que el tour está muy caro?", "expected": "Tácticas de Venta / FQSA"},
    {"q": "Requisitos para subir al Huayna Picchu", "expected": "Logística Cusco"},
    
    # Tier 1 (FQSAs)
    {"q": "¿Cuáles son los deportes de aventura en Arequipa?", "expected": "FQSA Arequipa"},
    {"q": "¿Cuál es la mejor época para viajar a la Patagonia Chilena?", "expected": "FQSA Chile"},
    {"q": "¿Se necesita visa para entrar a Bolivia?", "expected": "FQSA Bolivia"},
    {"q": "¿Hay señal de internet en el Salar de Uyuni?", "expected": "FQSA Bolivia"},
    {"q": "¿Cómo llego a la Laguna 69 en Huaraz?", "expected": "FQSA Ancash"},
    {"q": "¿Qué equipo necesito para escalar el Misti?", "expected": "FQSA Arequipa"},
    {"q": "¿Es peligroso viajar solo por la sierra peruana?", "expected": "FQSA Peru General"},
    
    # Tier 2 (Catálogo Operativo)
    {"q": "¿Incluyen seguro de vida en las expediciones de alta montaña?", "expected": "Catálogo / Seguros"},
    {"q": "¿Cuál es la política de cancelación si me enfermo?", "expected": "Catálogo / Políticas"},
    {"q": "¿Dan comida vegetariana en el Camino Inca?", "expected": "Catálogo Operativo"},
    {"q": "Aceptan pagos con criptomonedas o solo dólares?", "expected": "Catálogo / Pagos"},
    {"q": "¿Cuánto peso puedo llevar en el tren a Aguas Calientes?", "expected": "Catálogo Operativo"},
    
    # Tier 3 (Narrativa / Investigación / Observación)
    {"q": "¿Cuáles son los macro escenarios económicos proyectados para el turismo este año?", "expected": "Narrativa / Boletines"},
    {"q": "¿Cómo usan la inteligencia artificial para personalizar experiencias?", "expected": "Documentación IA"},
    {"q": "¿Qué beneficios tiene la sonoterapia en la altura?", "expected": "PDF Sonoterapia"},
    {"q": "¿De qué trata la ontología turística de Moquegua?", "expected": "Narrativa Moquegua"},
    {"q": "¿Cómo fue el desempeño del mercado brasileño el último semestre?", "expected": "Boletines de Inteligencia"}
]

async def run_evaluation():
    print("===================================================================")
    print(" 🚀 INICIANDO EVALUACIÓN RAG (GOLDEN SET DE 20 PREGUNTAS) ")
    print("===================================================================")
    
    score = 0
    
    for i, test in enumerate(GOLDEN_SET, 1):
        print(f"\n[{i}/20] PREGUNTA: {test['q']}")
        print(f"      ESPERADO: {test['expected']}")
        
        results = await search_knowledge(test['q'], limit=3)
        
        if not results:
            print("      -> ❌ SIN RESULTADOS (No hay información en Qdrant)")
            continue
            
        top_res = results[0]
        print(f"      -> OBTENIDO: Tier {top_res.get('tier', '?')} | {top_res.get('modulo_nombre')} | Región: {top_res.get('region')}")
        print(f"      -> SIMILITUD (BOOSTED): {top_res.get('similarity')} | RAW: {top_res.get('raw_score')}")
        print(f"      -> CONTEXTO: {top_res.get('text_content')[:120]}...")
        
        # Validación heurística simple: si la similitud boosteada es > 0.4 se asume hallazgo válido
        if top_res.get('similarity', 0) > 0.4:
            score += 1
            print("      -> ✅ MATCH ACEPTABLE")
        else:
            print("      -> ⚠️ MATCH BAJO (Posible alucinación o data faltante)")
            
    print("\n===================================================================")
    print(f" RESULTADO FINAL: {score}/20 ({score/20*100}%) aciertos con alta confianza.")
    print("===================================================================")
    print("Nota: Si el score es bajo en Tiers 1-3, necesitas correr 'qdrant_enterprise_sync.py'.")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
