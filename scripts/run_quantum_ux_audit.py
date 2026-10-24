import sys
import json
import pennylane as qml
from pennylane import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# =====================================================================
# LIFEXTREME QUANTUM UX SIMULATOR (PROPRIETARY ENGINE - NO EXTERNAL AI)
# PennyLane Quantum Variational Circuit for Funnel & UX Friction
# =====================================================================

num_qubits = 4
dev = qml.device("default.qubit", wires=num_qubits)

@qml.qnode(dev)
def user_ux_quantum_circuit(user_features, web_friction_weights):
    # 1. State Preparation: Encode user emotional/cognitive baseline
    for i in range(num_qubits):
        qml.RY(user_features[i] * np.pi, wires=i)

    # 2. Entanglement: Cognitive interaction between expectations & UI friction
    qml.CNOT(wires=[0, 1])
    qml.RZ(web_friction_weights[0] * np.pi, wires=1)

    qml.CNOT(wires=[1, 2])
    qml.RZ(web_friction_weights[1] * np.pi, wires=2)

    qml.CNOT(wires=[2, 3])
    qml.RZ(web_friction_weights[2] * np.pi, wires=3)

    qml.RX(web_friction_weights[3] * np.pi, wires=3)

    return [qml.expval(qml.PauliZ(i)) for i in range(num_qubits)]

synthetic_users = [
    {"id": "U01", "name": "Novios Millennials (Móvil)", "type": "Móvil / Rápido", "intent": 0.85, "patience": 0.25, "price_sens": 0.70, "tech": 0.90},
    {"id": "U02", "name": "Novia Planificadora Detallista", "type": "Desktop / Analítica", "intent": 0.90, "patience": 0.85, "price_sens": 0.40, "tech": 0.70},
    {"id": "U03", "name": "Novio Ejecutivo Ocupado", "type": "Móvil / Impaciente", "intent": 0.65, "patience": 0.20, "price_sens": 0.30, "tech": 0.85},
    {"id": "U04", "name": "Pareja Presupuesto Ajustado", "type": "Desktop / Cazaofertas", "intent": 0.60, "patience": 0.60, "price_sens": 0.95, "tech": 0.65},
    {"id": "U05", "name": "Pareja Safari de Lujo", "type": "Tablet / Alta Gama", "intent": 0.95, "patience": 0.70, "price_sens": 0.15, "tech": 0.80},
    {"id": "U06", "name": "Curioso de Instagram", "type": "Móvil / Tráfico Frío", "intent": 0.30, "patience": 0.15, "price_sens": 0.80, "tech": 0.95},
    {"id": "U07", "name": "Padres Regalando Luna de Miel", "type": "Desktop / Senior", "intent": 0.75, "patience": 0.50, "price_sens": 0.50, "tech": 0.35},
    {"id": "U08", "name": "Novios Románticos Espontáneos", "type": "Móvil / Visual", "intent": 0.70, "patience": 0.30, "price_sens": 0.60, "tech": 0.85},
    {"id": "U09", "name": "Pareja Viajera Frecuente", "type": "Desktop / Crítica", "intent": 0.80, "patience": 0.40, "price_sens": 0.45, "tech": 0.90},
    {"id": "U10", "name": "Novia buscando Inspiración", "type": "Tablet / Estética", "intent": 0.55, "patience": 0.65, "price_sens": 0.55, "tech": 0.75},
    {"id": "U11", "name": "Pareja Aventura & Trekking", "type": "Móvil / Práctico", "intent": 0.80, "patience": 0.35, "price_sens": 0.65, "tech": 0.80},
    {"id": "U12", "name": "Novios Escépticos de Agencias", "type": "Desktop / Desconfiado", "intent": 0.50, "patience": 0.45, "price_sens": 0.75, "tech": 0.85},
    {"id": "U13", "name": "Luna de Miel Urgente (1 mes)", "type": "Móvil / Alta Urgencia", "intent": 0.95, "patience": 0.15, "price_sens": 0.40, "tech": 0.75},
    {"id": "U14", "name": "Pareja Boomer Aniversario", "type": "Desktop / Tradicional", "intent": 0.70, "patience": 0.80, "price_sens": 0.50, "tech": 0.30},
    {"id": "U15", "name": "Novia Diseñadora UX/UI", "type": "Desktop / Ultra Crítica", "intent": 0.60, "patience": 0.25, "price_sens": 0.50, "tech": 1.00},
    {"id": "U16", "name": "Pareja Nómadas Digitales", "type": "Laptop / Técnico", "intent": 0.65, "patience": 0.30, "price_sens": 0.70, "tech": 0.95},
    {"id": "U17", "name": "Novios buscando Japón/Asia", "type": "Móvil / Específico", "intent": 0.85, "patience": 0.40, "price_sens": 0.60, "tech": 0.80},
    {"id": "U18", "name": "Cliente VIP Ultra High Net", "type": "Móvil / Cero Tiempo", "intent": 0.90, "patience": 0.10, "price_sens": 0.05, "tech": 0.70},
    {"id": "U19", "name": "Novia Comparando 5 Agencias", "type": "Desktop / Multitab", "intent": 0.75, "patience": 0.55, "price_sens": 0.85, "tech": 0.85},
    {"id": "U20", "name": "Novio Pragmático 'Solo Precio'", "type": "Móvil / Sin Rodeos", "intent": 0.70, "patience": 0.20, "price_sens": 0.90, "tech": 0.75}
]

# Friction values based on real HTML analysis of agenciaviajeros.com
web_friction = np.array([0.35, 0.65, 0.75, 0.55], requires_grad=False)

results = []

for u in synthetic_users:
    u_feat = np.array([u["intent"], u["patience"], u["price_sens"], u["tech"]], requires_grad=False)
    expvals = user_ux_quantum_circuit(u_feat, web_friction)
    
    p_hero = float((1 + expvals[0]) / 2)
    p_depth = float((1 + expvals[1]) / 2)
    p_price_tol = float((1 + expvals[2]) / 2)
    p_cta_conv = float((1 + expvals[3]) / 2)
    
    drop_stage = "CONVERTIDO"
    if p_hero < 0.40:
        drop_stage = "Rebote Inmediato (Hero)"
    elif p_depth < 0.40:
        drop_stage = "Abandono en Lectura (Bloque Texto H3)"
    elif p_price_tol < 0.40:
        drop_stage = "Fuga por Falta de Precios / Sin Catálogo"
    elif p_cta_conv < 0.50:
        drop_stage = "Duda en CTA ('Café Viajero' sin Formulario)"
        
    converted = drop_stage == "CONVERTIDO"
    
    results.append({
        "id": u["id"],
        "name": u["name"],
        "type": u["type"],
        "p_hero": round(p_hero, 3),
        "p_depth": round(p_depth, 3),
        "p_price_tol": round(p_price_tol, 3),
        "p_cta_conv": round(p_cta_conv, 3),
        "drop_stage": drop_stage,
        "converted": converted
    })

total_users = len(results)
conversions = sum(1 for r in results if r["converted"])
conv_rate = (conversions / total_users) * 100

drop_breakdown = {}
for r in results:
    stage = r["drop_stage"]
    drop_breakdown[stage] = drop_breakdown.get(stage, 0) + 1

output_data = {
    "target_url": "https://agenciaviajeros.com/",
    "total_simulated": total_users,
    "conversions": conversions,
    "conversion_rate": round(conv_rate, 1),
    "drop_breakdown": drop_breakdown,
    "user_details": results
}

print(json.dumps(output_data, indent=2, ensure_ascii=False))
