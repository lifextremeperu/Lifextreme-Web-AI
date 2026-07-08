import pennylane as qml
from pennylane import numpy as np
import sys
import json
import time

sys.stdout.reconfigure(encoding='utf-8')

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
    
    recipe = {
        "Empatia_y_Seguridad": float(probs[0] * 100),
        "Datos_Tecnicos_VIP": float(probs[1] * 100),
        "Urgencia_FOMO": float(probs[2] * 100),
        "Oferta_Descuento": float(probs[3] * 100)
    }
    return recipe

def main():
    print("=========================================================================")
    print("🤖 MAX Q-RAG: SIMULADOR DE ESCENARIOS MÚLTIPLES (CUSCO TECH HUB)")
    print("=========================================================================\n")
    time.sleep(1)
    
    # Extraídos y adaptados del ADN limpio de ventas reales de Lifextreme
    escenarios = [
        {
            "id": 1,
            "perfil": "El VIP Organizado",
            "mensaje": "Hola, estamos planeando un viaje a Perú para Octubre del próximo año. Queremos reservar el restaurante Central y hoteles 5 estrellas en Valle Sagrado.",
            "urgency": 0.10, # Falta un año
            "budget": 0.95,  # Mucho dinero (Central, 5 estrellas)
            "anxiety": 0.20  # Relajado, planeando con tiempo
        },
        {
            "id": 2,
            "perfil": "El Mochilero Desesperado",
            "mensaje": "Bueno... acabo de llegar al aeropuerto y cancelaron el vuelo. ¿Tienen algún tour barato para hoy en la tarde? Me quedé sin planes.",
            "urgency": 0.99, # Para HOY
            "budget": 0.30,  # Presupuesto bajo/barato
            "anxiety": 0.90  # Vuelo cancelado, frustrado
        },
        {
            "id": 3,
            "perfil": "El Negociador Desconfiado",
            "mensaje": "Me mandas el presupuesto porfa, pero sería sin tren y sin hoteles porque lo voy a comprar por mi cuenta. Por seguridad, ¿están registrados?",
            "urgency": 0.40, # Urgencia media
            "budget": 0.40,  # Quiere ahorrar (compra por su cuenta)
            "anxiety": 0.85  # Pide seguridad, desconfía del intermediario
        },
        {
            "id": 4,
            "perfil": "La Pareja de Aventura Extrema",
            "mensaje": "Llegamos mañana. Queremos hacer trekking, cuatrimotos y zip-line. ¡No nos importa el precio, queremos lo más extremo posible!",
            "urgency": 0.90, # Llegan mañana
            "budget": 0.85,  # No les importa el precio
            "anxiety": 0.05  # Cero ansiedad, buscan riesgo
        }
    ]

    for esc in escenarios:
        print(f"🔸 ESCENARIO {esc['id']}: {esc['perfil']}")
        print(f"💬 Mensaje: \"{esc['mensaje']}\"")
        
        recipe = calculate_sales_recipe(esc['urgency'], esc['budget'], esc['anxiety'])
        
        # Encontramos la táctica principal (la de mayor porcentaje)
        tactica_principal = max(recipe, key=recipe.get)
        
        print("🧪 Receta Cuántica de Respuesta generada para MAX:")
        print(f"   - 🛡️ Empatía/Seguridad : {recipe['Empatia_y_Seguridad']:.1f}%")
        print(f"   - 💼 Specs VIP         : {recipe['Datos_Tecnicos_VIP']:.1f}%")
        print(f"   - 🔥 Urgencia (FOMO)   : {recipe['Urgencia_FOMO']:.1f}%")
        print(f"   - 📉 Oferta/Descuento  : {recipe['Oferta_Descuento']:.1f}%")
        
        print("\n🎯 ESTRATEGIA DE CIERRE (Instrucción para el LLM):")
        if tactica_principal == "Empatía_y_Seguridad":
            print("   -> 'Demuestra autoridad legal, muéstrale registros y bríndale confianza total antes de vender.'")
        elif tactica_principal == "Datos_Tecnicos_VIP":
            print("   -> 'Háblale con elegancia. Menciona marcas premium, atención personalizada y exclusividad.'")
        elif tactica_principal == "Urgencia_FOMO":
            print("   -> 'Crea escasez. Dile que quedan pocos cupos para mañana y que debe reservar inmediatamente.'")
        else: # Oferta_Descuento
            print("   -> 'Ofrécele un combo rápido y económico para salvarle el día. La velocidad y el precio ganan aquí.'")
            
        print("-" * 75)
        time.sleep(0.5)

    print("✅ PRUEBA COMPLETADA: La IA adapta su personalidad matemáticamente a cada tipo de turista.")

if __name__ == "__main__":
    main()
