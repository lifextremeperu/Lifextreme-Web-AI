import json
import os
import sys

try:
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy
    from langchain_community.chat_models import ChatOllama
    from langchain_community.embeddings import OllamaEmbeddings
except ImportError as e:
    print(f"Error importando dependencias: {e}")
    print("Por favor ejecuta: pip install ragas langchain-community langchain-ollama datasets")
    sys.exit(1)

def main():
    print("===================================================")
    print("🛡️  LIFEXTREME CEREBRO - AUDITORIA DE SEGURIDAD RAGAS")
    print("===================================================\n")
    
    # 1. Configurar el LLM Evaluador Local (Ollama)
    # Por defecto usamos 'llama3' o 'deepseek-coder'. Puedes cambiarlo según tu modelo local.
    judge_model_name = "llama3"
    print(f"[1/4] Conectando al Juez Local Ollama (Modelo: {judge_model_name})...")
    
    # IMPORTANTE: Ragas requiere modelos que puedan retornar JSON / puntajes estructurados.
    evaluator_llm = ChatOllama(model=judge_model_name, temperature=0.0)
    
    # También necesitamos un modelo de embeddings para medir relevancia (ej. nomic-embed-text o mxbai-embed-large)
    # Asumimos que tienes 'nomic-embed-text' instalado en Ollama. Si no, cambiar por 'llama3'.
    embedding_model_name = "nomic-embed-text"
    evaluator_embeddings = OllamaEmbeddings(model=embedding_model_name)
    
    print("[2/4] Cargando el Dataset de Pruebas de Estrés (MINCETUR / SUTRAN)...")
    dataset_path = os.path.join(os.path.dirname(__file__), "eval_datasets", "test_dataset_mincetur.json")
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Preparar el formato Dataset que requiere Ragas
    ragas_dataset = {
        "question": [item["question"] for item in data],
        "answer": [item["answer"] for item in data], # Esta es la respuesta que "imaginamos" dio el RAG
        "contexts": [item["contexts"] for item in data],
        "ground_truth": [item["ground_truth"] for item in data]
    }
    
    eval_dataset = Dataset.from_dict(ragas_dataset)
    
    print(f"      Se cargaron {len(eval_dataset)} casos extremos para auditar.\n")
    print("[3/4] Evaluando Fidelidad (Hallucination Check) y Relevancia...")
    print("      (Esto puede tomar unos minutos dependiendo de la potencia de tu PC)\n")
    
    # 2. Ejecutar la Evaluación
    try:
        # Nota: Ollama a veces puede fallar en parsear JSON complejo requerido por ragas, 
        # pero para métricas básicas funciona bien con modelos potentes.
        result = evaluate(
            dataset=eval_dataset,
            metrics=[faithfulness, answer_relevancy],
            llm=evaluator_llm,
            embeddings=evaluator_embeddings,
            raise_exceptions=False
        )
        
        print("\n===================================================")
        print("📊 RESULTADOS DE LA AUDITORÍA RAGAS")
        print("===================================================")
        print("Nota: 1.0 es el puntaje perfecto.")
        print(f"Score Total del Cerebro: {result}")
        print("\nAnálisis:")
        print("- Faithfulness (Fidelidad): Mide si la IA alucinó inventando leyes. (Ej: La pregunta 1 y 3 del dataset son alucinaciones inducidas).")
        print("- Answer Relevancy (Relevancia): Mide si la IA respondió directamente a la pregunta de la agencia.")
        
    except Exception as e:
        print("\n❌ Error durante la evaluación. Esto puede ocurrir si el modelo Ollama no está corriendo, no soporta salida estructurada JSON adecuadamente, o falta el modelo de embeddings.")
        print(f"Detalle técnico: {e}")
        print("\nPara ejecutar este test asegúrate de tener:")
        print(f"1. Ollama ejecutándose: 'ollama run {judge_model_name}'")
        print(f"2. Modelo de embeddings instalado: 'ollama pull {embedding_model_name}'")

if __name__ == "__main__":
    main()
