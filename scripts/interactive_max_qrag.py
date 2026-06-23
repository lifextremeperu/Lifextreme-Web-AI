import pennylane as qml
from pennylane import numpy as np
import requests
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURACIÓN DE OLLAMA ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-v2:lite"

# --- CIRCUITO CUÁNTICO DE VENTAS ---
n_qubits = 3
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def sales_state_circuit(client_state, weights):
    for i in range(n_qubits):
        qml.RY(client_state[i] * np.pi, wires=i)
    for i in range(n_qubits):
        qml.RX(weights[i], wires=i)
    qml.CNOT(wires=[0, 2])
    qml.CNOT(wires=[1, 2])
    return qml.probs(wires=[0, 1])

def calculate_sales_recipe(urgency, budget, anxiety):
    client_state = np.array([urgency, budget, anxiety], requires_grad=False)
    trained_weights = np.array([0.5, 1.2, -0.8], requires_grad=False)
    probs = sales_state_circuit(client_state, trained_weights)
    return {
        "Empatia_y_Seguridad": float(probs[0] * 100),
        "Datos_Tecnicos_VIP": float(probs[1] * 100),
        "Urgencia_FOMO": float(probs[2] * 100),
        "Oferta_Descuento": float(probs[3] * 100)
    }

# --- 1. ACTUALIZACIÓN: CLASIFICADOR LIGERO (0.01 segundos) ---
# En producción web esto sería una API ultra-rápida (Groq) o heurística.
# Aquí usamos un analizador léxico local ultrarrápido para eliminar el cuello de botella.
def fast_extract_intent(user_message):
    msg = user_message.lower()
    
    # Valores por defecto
    urgency, budget, anxiety = 0.5, 0.5, 0.5
    
    # Heurística de Urgencia
    if any(w in msg for w in ["mañana", "hoy", "ya", "urgente", "ahora"]):
        urgency = 0.95
    elif any(w in msg for w in ["año", "meses", "planeando", "futuro"]):
        urgency = 0.10
        
    # Heurística de Presupuesto
    if any(w in msg for w in ["barato", "descuento", "poco", "ajustado", "oferta", "económico"]):
        budget = 0.20
    elif any(w in msg for w in ["lujo", "vip", "central", "estrellas", "exclusivo", "dinero no"]):
        budget = 0.90
        
    # Heurística de Ansiedad
    if any(w in msg for w in ["miedo", "seguro", "altura", "peligro", "estafa", "ayuda"]):
        anxiety = 0.90
    elif any(w in msg for w in ["extremo", "adrenalina", "fuerte", "riesgo", "sin miedo"]):
        anxiety = 0.10
        
    return {"urgency": urgency, "budget": budget, "anxiety": anxiety}

# --- 2. ACTUALIZACIÓN: STREAMING ACTIVO ---
def stream_max_response(user_message, recipe):
    system_prompt = f"""
    Eres MAX, Asesor de Aventura en Perú de la empresa Lifextreme. Eres persuasivo y experto.
    Debes responder al siguiente mensaje del cliente usando esta mezcla EXACTA de estrategias de venta:
    - Empatía y Seguridad: {recipe['Empatia_y_Seguridad']:.1f}%
    - Datos y Lujo VIP: {recipe['Datos_Tecnicos_VIP']:.1f}%
    - Urgencia (FOMO/Cupos limitados): {recipe['Urgencia_FOMO']:.1f}%
    - Ofertas/Descuentos rápidos: {recipe['Oferta_Descuento']:.1f}%
    
    Ajusta tu tono según la estrategia dominante. Responde corto, persuasivo y como un humano que escribe por chat.
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": f"Turista: {user_message}\nMAX:",
        "system": system_prompt,
        "stream": True  # <--- MAGIA: STREAMING ACTIVADO
    }
    
    print("\n==================================================")
    print("🔥 MAX: ", end="", flush=True)
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                word = chunk.get("response", "")
                sys.stdout.write(word)
                sys.stdout.flush()
                
        print("\n==================================================\n")
    except Exception as e:
        print(f"\nError conectando a Ollama: {str(e)}")

# --- BUCLE INTERACTIVO ---
def main():
    print("=========================================================================")
    print("🚀 TERMINAL MAX Q-RAG PRO (STREAMING + LIGHT-CLASSIFIER ACTIVADOS)")
    print("=========================================================================")
    print("Escribe un mensaje como si fueras un turista en www.lifextreme.store")
    print("Escribe 'salir' para terminar.")
    print("=========================================================================\n")
    
    while True:
        try:
            user_input = input("👤 Turista: ")
            if user_input.lower() in ['salir', 'exit', 'quit']:
                break
            if not user_input.strip():
                continue
                
            start_time = time.time()
            
            # 1. Extracción Ultra-Rápida
            intent = fast_extract_intent(user_input)
            
            # 2. Enrutamiento Cuántico
            recipe = calculate_sales_recipe(intent['urgency'], intent['budget'], intent['anxiety'])
            
            calc_time = time.time() - start_time
            print(f"⚡ [Intención + Cuántica procesada en {calc_time:.4f} seg]")
            print(f"📊 Receta: Empatía {recipe['Empatia_y_Seguridad']:.0f}% | VIP {recipe['Datos_Tecnicos_VIP']:.0f}% | FOMO {recipe['Urgencia_FOMO']:.0f}% | Oferta {recipe['Oferta_Descuento']:.0f}%")
            
            # 3. Streaming de Respuesta (Empieza a generar instantáneamente)
            stream_max_response(user_input, recipe)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
