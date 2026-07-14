import json
import asyncio
import httpx
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval import evaluate
from deepeval.models import DeepEvalBaseLLM

import sys
sys.path.insert(0, ".")
from scripts.max_chat_server import tool_search_rag

# ==========================================
# CUSTOM LLM PARA DEEPEVAL (USANDO OLLAMA)
# ==========================================
class OllamaLocalJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def load_model(self):
        return self.model_name

    def generate(self, prompt: str) -> str:
        try:
            # Llamada al servidor local de Ollama
            res = httpx.post("http://127.0.0.1:11434/api/generate", json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }, timeout=120.0)
            return res.json().get("response", "")
        except Exception as e:
            print(f"Error en el Juez Local: {e}")
            return "Error de generación"

    async def a_generate(self, prompt: str) -> str:
        # Envolvemos la llamada sincrónica para cumplir con la interfaz asíncrona de DeepEval
        return self.generate(prompt)

    def get_model_name(self):
        return "Llama-3-Local-Judge"


def get_max_response(query):
    try:
        response = tool_search_rag(query)
        return response
    except Exception as e:
        return str(e)

def run_tests():
    with open("golden_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    test_cases = []
    
    print("\n=======================================================")
    print(" 🚀 INICIANDO AUDITORÍA LLM CON JUEZ LOCAL (LLAMA-3) ...")
    print("=======================================================")
    
    for item in dataset:
        query = item["input"]
        expected = item["expected_output"]
        
        print(f"\n[?] Cliente (Query): {query}")
        actual_output = get_max_response(query)
        print(f"    [+] RAG Recuperó:\n {actual_output[:250]}...")
        
        test_case = LLMTestCase(
            input=query,
            actual_output=actual_output,
            expected_output=expected
        )
        test_cases.append(test_case)
        
    # Inicializar el Juez Local (Soberanía de Datos)
    juez_local = OllamaLocalJudge(model_name="llama3")
    
    # Definimos la métrica de relevancia obligando a que use el juez local
    print("\n[*] El Juez Local (Llama-3) está evaluando los resultados matemáticamente...")
    relevancy_metric = AnswerRelevancyMetric(threshold=0.6, model=juez_local)
    
    evaluate(test_cases, [relevancy_metric])
    
if __name__ == "__main__":
    run_tests()
