import requests
import asyncio
import httpx

OLLAMA_URL = 'http://localhost:11434/api/generate'
EMBED_URL = 'http://localhost:11434/api/embeddings'

golden_dataset = [
    {
        "query": "¿Qué certificaciones necesita un guía de canotaje nivel IV según el MINCETUR?",
        "expected": "Necesita certificado en primeros auxilios/RCP y constancia de dominio en técnicas de rescate en aguas bravas. Se exige un kayakista de seguridad."
    },
    {
        "query": "¿Puedo alquilar kayaks directamente en las lagunas menores de Ancash?",
        "expected": "Generalmente no. La mayoría de los operadores en Huaraz ofrecen tours que incluyen el transporte y el equipo, pero alquilarlos directamente allí no es común."
    },
    {
        "query": "¿Qué pasa si vendo un tour más barato en mi web que en Booking.com?",
        "expected": "Booking te penaliza reduciendo tu visibilidad (Visibility Penalty) por violar la cláusula de Paridad de Tarifas. Para evitarlo, se debe usar valores añadidos o vender en canales offline."
    }
]

async def llm_generate(prompt: str) -> str:
    async with httpx.AsyncClient() as hc:
        try:
            res = await hc.post(OLLAMA_URL, json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }, timeout=120.0)
            return res.json().get("response", "")
        except:
            return "Error de LLM"

async def llm_judge(query: str, expected: str, generated: str) -> int:
    prompt = f"""
    Actúa como un juez estricto.
    Pregunta: {query}
    Respuesta Ideal: {expected}
    Respuesta Generada por el RAG: {generated}
    
    ¿Qué tan precisa es la respuesta generada comparada con la ideal?
    Responde ÚNICAMENTE con un número del 0 al 10 (donde 10 es perfecta).
    """
    resp = await llm_generate(prompt)
    try:
        nums = [int(s) for s in resp.split() if s.isdigit()]
        return nums[0] if nums else 0
    except:
        return 0

async def main():
    print("=============================================")
    print(" SIMULADOR DE EVALUACIÓN RAG (Mini-RAGAS) ")
    print("=============================================\n")
    
    total_score = 0
    
    for i, item in enumerate(golden_dataset, 1):
        q = item["query"]
        print(f"[{i}/3] Evaluando: {q}")
        
        # 1. Recuperar Contexto (RAG) vía REST a Qdrant
        context_text = ""
        async with httpx.AsyncClient() as hc:
            res = await hc.post(EMBED_URL, json={"model": "nomic-embed-text", "prompt": q})
            vector = res.json().get('embedding')
            
        if vector:
            try:
                qdrant_res = requests.post(
                    'http://localhost:6333/collections/Lifextreme_Knowledge/points/search',
                    json={'vector': vector, 'limit': 2, 'with_payload': True},
                    timeout=30.0
                )
                hits = qdrant_res.json().get('result', [])
                context_text = " ".join([h.get("payload", {}).get("text_content", "") for h in hits])
            except Exception as e:
                print(f"Error Qdrant: {e}")
            
        # 2. Generar Respuesta (Prompt de Sistema Reforzado Anti-Alucinaciones)
        rag_prompt = f"""Eres un Agente Corporativo B2B estricto. 
Tu única fuente de verdad es la INFORMACIÓN RECUPERADA.
REGLAS:
1. NUNCA des consejos generales, opiniones ni uses conocimiento previo de internet.
2. Si la respuesta exacta a la pregunta NO está en la INFORMACIÓN RECUPERADA, debes responder textualmente: "No hay información suficiente en la base de datos".
3. Cíñete estrictamente al contexto legal y políticas dadas.

INFORMACIÓN RECUPERADA:
{context_text}

Pregunta: {q}"""
        generated_answer = await llm_generate(rag_prompt)
        
        # 3. Juez LLM evalúa
        score = await llm_judge(q, item["expected"], generated_answer)
        total_score += score
        
        print(f"  -> Score Juez (LLM): {score}/10")
        print(f"  -> Respuesta RAG: {generated_answer[:150]}...\n")
        
    print(f"=== RESULTADO FINAL DE LA SIMULACIÓN ===")
    print(f"Precisión Promedio (Factual Accuracy): {(total_score / 30) * 100:.1f}%")
    
    if total_score < 20:
        print("Alerta: El RAG falló en recuperar datos legales específicos. (Requiere subir los PDFs en texto).")
    else:
        print("¡El RAG está funcionando excelentemente!")

if __name__ == "__main__":
    asyncio.run(main())
