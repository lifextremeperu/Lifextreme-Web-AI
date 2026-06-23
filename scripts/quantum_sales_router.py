import pennylane as qml
from pennylane import numpy as np
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

# Definimos 3 Qubits de entrada (El Estado del Cliente)
# Qubit 0: Urgencia (0 = Viaja el prox año, 1 = Viaja mañana)
# Qubit 1: Presupuesto (0 = Mochilero/Oferta, 1 = VIP/Exclusivo)
# Qubit 2: Ansiedad (0 = Extremo/Relajado, 1 = Miedoso/Desconfiado)
n_qubits = 3
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def sales_state_circuit(client_state, weights):
    # Inicializamos el estado del cliente basándonos en el análisis previo del texto
    for i in range(n_qubits):
        qml.RY(client_state[i] * np.pi, wires=i)
        
    # Rotaciones parametrizadas (El "Cerebro" de Ventas de MAX)
    for i in range(n_qubits):
        qml.RX(weights[i], wires=i)
        
    # Entrelazamiento Emocional (Sinergias de Venta)
    # Si hay Alta Urgencia y Alta Ansiedad -> Bloqueo mental (Necesita mucha empatía)
    qml.CNOT(wires=[0, 2])
    # Si hay Alto Presupuesto y Baja Ansiedad -> Cierre rápido (Necesita specs VIP)
    qml.CNOT(wires=[1, 2])
    
    # Medimos la probabilidad de 4 enfoques de respuesta (Triggers)
    return qml.probs(wires=[0, 1])

def calculate_sales_recipe(urgency, budget, anxiety):
    # Estado del cliente (0.0 a 1.0)
    client_state = np.array([urgency, budget, anxiety], requires_grad=False)
    
    # Pesos pre-entrenados del "Mejor Vendedor de Cusco" (Hypothetical trained weights)
    # Estos pesos se calibrarían con las ventas reales de Lifextreme
    trained_weights = np.array([0.5, 1.2, -0.8], requires_grad=True)
    
    # Obtenemos las probabilidades (La "Receta")
    probs = sales_state_circuit(client_state, trained_weights)
    
    # Mapeamos las probabilidades a los 4 Gatillos de Venta de MAX
    recipe = {
        "Empatia_y_Seguridad": float(probs[0] * 100), # Para calmar dudas
        "Datos_Tecnicos_VIP": float(probs[1] * 100),  # Para clientes de alto presupuesto
        "Urgencia_FOMO": float(probs[2] * 100),       # Escasez ("Quedan 2 cupos")
        "Oferta_Descuento": float(probs[3] * 100)     # Para cerrar a los dudosos por precio
    }
    
    return recipe

def main():
    print("=========================================================================")
    print("🧠 MAX Q-RAG: ENRUTADOR CUÁNTICO DE VENTAS")
    print("=========================================================================\n")
    
    # CASO DE PRUEBA: "El Cliente Difícil"
    # Mensaje: "Hola, viajo mañana a Cusco. Tengo mucho miedo del mal de altura y no sé si el tour sea seguro. Además mi presupuesto está ajustado."
    
    print("📩 MENSAJE DEL CLIENTE DETECTADO:")
    print('"Hola, viajo mañana a Cusco. Tengo mucho miedo del mal de altura y no sé si el tour sea seguro. Además mi presupuesto está ajustado."\n')
    
    # El LLM (o un parser simple) extrajo estos valores:
    urgency = 0.95  # Viaja mañana (Alta urgencia)
    budget = 0.20   # Presupuesto ajustado (Bajo)
    anxiety = 0.90  # Miedo al mal de altura (Alta ansiedad)
    
    print("📊 1. ESTADO CUÁNTICO DEL LEAD (Entradas):")
    print(f"   - Nivel de Urgencia   : {urgency*100:.0f}%")
    print(f"   - Flexibilidad Presup.: {budget*100:.0f}%")
    print(f"   - Nivel de Ansiedad   : {anxiety*100:.0f}%\n")
    
    print("⚙️ 2. COLAPSANDO ONDAS DE PROBABILIDAD DE VENTA...\n")
    
    recipe = calculate_sales_recipe(urgency, budget, anxiety)
    
    print("✅ 3. RECETA DE CIERRE DE VENTAS GENERADA PARA MAX:")
    print("MAX debe redactar su respuesta usando esta mezcla exacta de Gatillos Mentales:\n")
    
    print(f"   🛡️ Empatía y Seguridad : {recipe['Empatia_y_Seguridad']:.1f}%")
    print(f"   📉 Oferta / Descuento  : {recipe['Oferta_Descuento']:.1f}%")
    print(f"   🔥 Urgencia (FOMO)     : {recipe['Urgencia_FOMO']:.1f}%")
    print(f"   💼 Specs Técnicos VIP  : {recipe['Datos_Tecnicos_VIP']:.1f}%\n")
    
    print("-------------------------------------------------------------------")
    print("DIRECTIVA PARA EL RAG:")
    print("1. Buscar en BD: Protocolos de mal de altura y Balones de Oxígeno.")
    print("2. Buscar en BD: Descuentos de última hora para rellenar grupos.")
    print("3. Instrucción a MAX: Responde calmando sus miedos primero, ofrécele un descuento pequeño por compra inmediata (aprovechando que viaja mañana). No le des detalles técnicos aburridos ni le vendas paquetes VIP caros.")
    print("===================================================================")

if __name__ == "__main__":
    main()
