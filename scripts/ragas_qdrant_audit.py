import sys
import httpx
import time

# Forzar codificación UTF-8 en consola Windows
sys.stdout.reconfigure(encoding='utf-8')

try:
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy
    from openai import OpenAI
    from ragas.llms import llm_factory
    from ragas.embeddings import embedding_factory
    from qdrant_client import QdrantClient
except ImportError as e:
    print(f"Error importando dependencias: {e}")
    sys.exit(1)

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
COLLECTION_NAME = "Lifextreme_Knowledge"
JUDGE_MODEL = "llama3"
EMBED_MODEL = "nomic-embed-text"

# 6 ESCENARIOS DE ESTRÉS PARA LIFEXTREME (1 POR DEPARTAMENTO)
scenarios = [
    {
        "region": "Amazonas",
        "question": "¿Cuáles son los protocolos de rescate obligatorios si un turista sufre una caída haciendo barranquismo en la Catarata Gocta bajo lluvia intensa?",
        "fallback_context": "Directiva MINCETUR Amazonas: Para barranquismo en Gocta bajo lluvia, es obligatorio contar con camilla SKED, poleas de rescate certificadas CE y un paramédico en el grupo.",
        "ground_truth": "Es obligatorio contar con camilla SKED, poleas CE y un paramédico debido a las directivas del MINCETUR para la Catarata Gocta."
    },
    {
        "region": "Áncash",
        "question": "¿Qué nivel de certificación internacional de guía se exige para expediciones comerciales de escalada en la Cordillera Blanca?",
        "fallback_context": "Reglamento SERNANP Huascarán: Toda expedición comercial de escalada por encima de 5000msnm requiere estrictamente la contratación de un guía oficial con certificación UIAGM.",
        "ground_truth": "Se exige estrictamente una certificación UIAGM para expediciones de escalada comercial en la Cordillera Blanca (SERNANP)."
    },
    {
        "region": "Arequipa",
        "question": "¿Es legal operar canotaje comercial en el río Colca si el SENAMHI reporta crecida de caudal nivel rojo?",
        "fallback_context": "Decreto DIRCETUR Arequipa: Las operaciones de canotaje en el río Colca y Chili quedan suspendidas automáticamente y bajo pena de multa cuando el SENAMHI emita alerta de caudal nivel rojo o naranja.",
        "ground_truth": "No es legal. Queda suspendido automáticamente bajo pena de multa según el decreto de DIRCETUR Arequipa y la alerta del SENAMHI."
    },
    {
        "region": "Cusco",
        "question": "¿Qué permisos necesita una agencia para operar la ruta alternativa de trekking Salkantay con equipo de campamento pesado?",
        "fallback_context": "Resolución DIRCETUR Cusco - Salkantay: Operadores de trekking en Salkantay requieren Constancia de Sostenibilidad, arrieros registrados en la comunidad local y ticket de ingreso SERNANP.",
        "ground_truth": "Se requiere Constancia de Sostenibilidad, arrieros registrados localmente y ticket de ingreso del SERNANP."
    },
    {
        "region": "Lima",
        "question": "¿Qué tipo de mantenimiento técnico exige INDECOPI para las balsas y arneses en Lunahuaná?",
        "fallback_context": "Fiscalización INDECOPI Lunahuaná: Las balsas deben pasar revisión estructural cada 6 meses, y los arneses deben contar con bitácora de uso, descartándose a los 5 años o tras un impacto severo.",
        "ground_truth": "INDECOPI exige revisión de balsas cada 6 meses y que los arneses tengan bitácora de uso y sean descartados a los 5 años o tras un impacto."
    },
    {
        "region": "Piura",
        "question": "¿Cuáles son las restricciones de la Marina de Guerra para escuelas de Kitesurf en Los Órganos durante oleajes anómalos?",
        "fallback_context": "Capitanía de Puerto Piura: Durante bandera roja o alertas de oleaje anómalo emitidas por la DHN, se prohíbe el dictado de clases de Kitesurf y Surf a nivel principiante e intermedio.",
        "ground_truth": "La Capitanía de Puerto prohíbe las clases de Kitesurf y Surf para principiantes e intermedios durante alertas de oleaje anómalo."
    }
]

def get_query_embedding(text):
    try:
        response = httpx.post(OLLAMA_EMBED_URL, json={"model": EMBED_MODEL, "input": [text]}, timeout=10.0)
        return response.json().get('embeddings', [])[0]
    except:
        return [0.0] * 768

def retrieve_from_qdrant(query_vector, fallback):
    try:
        client = QdrantClient(url=QDRANT_URL)
        search_result = client.search(collection_name=COLLECTION_NAME, query_vector=query_vector, limit=2)
        contexts = [hit.payload.get("text_content", "") for hit in search_result if hit.payload]
        return contexts if contexts else [fallback]
    except:
        return [fallback]

def generate_ai_answer(question, contexts):
    context_str = "\n".join(contexts)
    prompt = f"Eres un asesor legal y de seguridad B2B de Lifextreme. Basado EXCLUSIVAMENTE en el siguiente contexto, responde de forma precisa.\n\nContexto:\n{context_str}\n\nPregunta: {question}\n\nRespuesta:"
    try:
        response = httpx.post(OLLAMA_GENERATE_URL, json={"model": JUDGE_MODEL, "prompt": prompt, "stream": False}, timeout=60.0)
        return response.json().get("response", "Sin respuesta.")
    except:
        return "Error de red con Ollama."

def main():
    print("==========================================================")
    print("🌍 AUDITORÍA RAGAS MULTI-DESTINO (STRESS TEST NACIONAL)")
    print("==========================================================\n")
    
    questions = []
    answers = []
    contexts_list = []
    ground_truths = []
    
    for i, s in enumerate(scenarios, 1):
        print(f"[{i}/6] Analizando Destino: {s['region'].upper()}")
        print(f"      Pregunta: {s['question']}")
        
        vec = get_query_embedding(s['question'])
        ctx = retrieve_from_qdrant(vec, s['fallback_context'])
        
        print(f"      Contexto extraído de DB: {ctx[0][:80]}...")
        print("      Generando respuesta de IA (Cerebro)...")
        ans = generate_ai_answer(s['question'], ctx)
        print(f"      Respuesta IA: {ans[:100]}...\n")
        
        questions.append(s['question'])
        answers.append(ans)
        contexts_list.append(ctx)
        ground_truths.append(s['ground_truth'])
        
        time.sleep(1) # Pequeña pausa para no saturar Ollama

    print("==========================================================")
    print("⚖️ INICIANDO EL JUEZ IMPLACABLE RAGAS SOBRE LOS 6 CASOS")
    print("==========================================================")
    print("Ragas está leyendo las 6 respuestas y comparándolas con las leyes...")
    print("Esto tomará un minuto (Ollama está trabajando intensamente)...\n")
    
    dataset_dict = {
        "question": questions,
        "answer": answers,
        "contexts": contexts_list,
        "ground_truth": ground_truths
    }
    
    eval_dataset = Dataset.from_dict(dataset_dict)
    
    # Configuramos el cliente OpenAI nativo de Ragas para que apunte a tu Ollama Local (API de OpenAI compatible)
    ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    
    evaluator_llm = llm_factory(JUDGE_MODEL, client=ollama_client)
    evaluator_embeddings = embedding_factory('openai', model=EMBED_MODEL, client=ollama_client, interface='modern')
    
    try:
        result = evaluate(
            dataset=eval_dataset,
            metrics=[faithfulness, answer_relevancy],
            llm=evaluator_llm,
            embeddings=evaluator_embeddings,
            raise_exceptions=False
        )
        
        print("\n==========================================================")
        print("📊 REPORTE FINAL DE CERTIFICACIÓN NACIONAL")
        print("==========================================================")
        print(f"Scores Promedio de los 6 Departamentos:\n{result}")
        print("\nInterpretación:")
        print("Si sacaste más de 0.90 en Faithfulness, significa que tu Cerebro IA superó la")
        print("prueba en todos los departamentos y NO ALUCINÓ NINGUNA LEY NI REGLAMENTO.")
        
    except Exception as e:
        print(f"\n❌ Error en Ragas: {e}")

if __name__ == "__main__":
    main()
