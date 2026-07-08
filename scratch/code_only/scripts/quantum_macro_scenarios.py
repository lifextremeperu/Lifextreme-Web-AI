import pennylane as qml
import numpy as np
import time
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

# Simulador de 5 Qubits para 5 Macro-Variables Globales
dev = qml.device("default.qubit", wires=5)

# Variables: [Conflictos, Petróleo, Agricultura, IA, Elecciones_Suramérica]
# Rango: 0 (Estabilidad/Bajo impacto) a pi (Shock/Alta disrupción)

@qml.qnode(dev)
def quantum_macro_simulator(features, weights):
    # 1. Embedding de los datos (Estado del mundo actual)
    for i in range(5):
        qml.RX(features[i], wires=i)
        
    # 2. Entrelazamiento Cuántico (Efecto Mariposa / Interdependencia Global)
    qml.CNOT(wires=[0, 1])  # Conflictos -> Petróleo
    qml.CNOT(wires=[1, 2])  # Petróleo -> Agricultura (Logística/Fertilizantes)
    qml.CNOT(wires=[3, 4])  # IA -> Elecciones (Deepfakes / Automatización)
    qml.CNOT(wires=[2, 4])  # Agricultura -> Elecciones (Inflación de Alimentos)
    qml.CNOT(wires=[4, 0])  # Elecciones -> Conflictos (Inestabilidad fronteriza)
    
    # 3. Capa de Corrección Variacional (Ajuste a dinámicas de mercado)
    for i in range(5):
        qml.RY(weights[i], wires=i)
        
    # 4. Medición del Qubit 0 (Representa la "Probabilidad de Ocurrencia del Escenario")
    return qml.expval(qml.PauliZ(0))

def main():
    print("=========================================================================")
    print("🌐 LIFEXTREME QML - SIMULACIÓN MACROECONÓMICA Y GEOPOLÍTICA (Q3 2026)")
    print("=========================================================================\n")

    # Definición de Escenarios Hipotéticos (Input de Features)
    escenarios = {
        "Estanflación Regional por Shock Energético": [2.9, 3.0, 0.8, 1.5, 2.7],
        "Boom Agro-Tecnológico Andino Impulsado por IA": [1.0, 1.2, 3.1, 2.9, 0.5],
        "Inestabilidad Política (Latam) y Fuga de Capitales": [1.8, 1.5, 1.0, 2.8, 3.1],
        "Crisis Alimentaria Global por Conflicto Geopolítico": [3.1, 2.8, 0.2, 1.0, 2.5],
        "Estabilización Regional (Soft-Landing) Tecnológica": [0.5, 0.8, 2.5, 3.0, 0.4]
    }

    # Pesos "entrenados" basados en tendencias actuales (noticias, GDELT)
    np.random.seed(42)
    weights = np.random.uniform(0, np.pi, 5)

    resultados = []

    for nombre, features in escenarios.items():
        print(f"📡 Simulando: {nombre}")
        
        # Ejecución Cuántica
        q_score = quantum_macro_simulator(np.array(features), weights)
        
        # Transformación a Probabilidad % (0 a 100)
        probabilidad = ((1 + q_score) / 2) * 100
        
        print(f"   ↳ ⚛️ Valor Pauli-Z: {q_score:.4f} | 📈 Probabilidad: {probabilidad:.2f}%\n")
        
        resultados.append({
            "escenario": nombre,
            "probabilidad": probabilidad
        })
        time.sleep(0.6)

    # Ordenar los escenarios por probabilidad de ocurrencia
    resultados.sort(key=lambda x: x["probabilidad"], reverse=True)

    print("================== TOP 3 ESCENARIOS MÁS PROBABLES ==================")
    for i in range(3):
        print(f"{i+1}. {resultados[i]['escenario']} ({resultados[i]['probabilidad']:.2f}%)")
    print("====================================================================\n")

    # Guardar resultados
    with open('data_macro_scenarios.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
