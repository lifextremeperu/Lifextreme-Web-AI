import pennylane as qml
import numpy as np
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Definimos un simulador cuántico local con 3 qubits
# Esto crea el entorno donde las operaciones de mecánica cuántica serán simuladas.
dev = qml.device("default.qubit", wires=3)

# 2. Definimos el Circuito Cuántico (Quantum Node)
@qml.qnode(dev)
def quantum_route_evaluator(features, weights):
    # A. Embedding: Convertimos datos clásicos (clima, distancia, etc) a estados cuánticos
    for i in range(3):
        qml.RX(features[i], wires=i)
        
    # B. Entrelazamiento (Entanglement): Conectamos los qubits para que interactúen simultáneamente
    # Esto es algo que la computación clásica no puede hacer de forma nativa.
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    qml.CNOT(wires=[2, 0])
    
    # C. Capa Variacional: Aplicamos rotaciones basadas en nuestros "pesos" entrenables
    for i in range(3):
        qml.RY(weights[i], wires=i)
        
    # D. Medición: Obtenemos el valor esperado (Expectation Value) del primer qubit
    return qml.expval(qml.PauliZ(0))

def main():
    print("\n========================================================")
    print("🚀 INICIANDO MOTOR DE INTELIGENCIA CUÁNTICA LIFEXTREME")
    print("========================================================\n")
    time.sleep(1)
    
    # Datos de entrada de una ruta ficticia (ej. Cusco - Laguna Humantay)
    # [Dificultad Terreno, Factor Clima, Tráfico/Bloqueos] (Normalizados entre 0 y pi)
    ruta_features = np.array([0.8, 1.2, 0.3]) 
    
    # Pesos del modelo (en producción esto se entrena con PyTorch/Descenso de Gradiente)
    np.random.seed(42)
    weights = np.random.uniform(0, np.pi, 3)
    
    print(f"📊 Evaluando Ruta con variables clásicas: {ruta_features}")
    print(f"⚙️ Configurando Superposición y Entrelazamiento en 3 Qubits...")
    time.sleep(1.5)
    
    # Ejecutamos el circuito cuántico
    print(f"🧠 Ejecutando modelo QML (Quantum Machine Learning)...")
    start_time = time.time()
    quantum_score = quantum_route_evaluator(ruta_features, weights)
    execution_time = time.time() - start_time
    
    # Convertimos la salida cuántica (-1 a 1) a un score de viabilidad (0 a 100%)
    viability = ((quantum_score + 1) / 2) * 100
    
    time.sleep(1)
    print("\n------------------ RESULTADOS --------------------------")
    print(f"✅ Valor Cuántico (Pauli-Z expval): {quantum_score:.4f}")
    print(f"🌟 Índice de Viabilidad de Ruta (Q-Score): {viability:.2f}%")
    print(f"⏱️ Tiempo de computación cuántica: {execution_time:.4f} segundos")
    print("--------------------------------------------------------")
    print("STATUS: Lifextreme 'Quantum-Ready' Arquitecture [ACTIVA]\n")

if __name__ == "__main__":
    main()
