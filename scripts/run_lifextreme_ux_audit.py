import sys
import json
import pennylane as qml
from pennylane import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# =====================================================================
# LIFEXTREME PROPRIETARY QUANTUM UX AUDITOR (PennyLane QML Engine)
# Canonical Bloch Sphere Mapping: Theta = (1 - Feature) * pi
# Target: https://www.lifextreme.store
# =====================================================================

num_qubits = 4
dev = qml.device("default.qubit", wires=num_qubits)

@qml.qnode(dev)
def lifextreme_quantum_circuit(user_features, ux_parameters):
    """
    user_features: [intent, patience, price_sensitivity, tech_savviness]
    ux_parameters: [hero_friction, catalog_friction, group_value_boost, checkout_friction]
    """
    # 1. State preparation: Higher feature -> closer to Pole |0> (Success: +1 Pauli-Z)
    for i in range(num_qubits):
        theta = (1.0 - user_features[i]) * np.pi
        qml.RY(theta, wires=i)

    # 2. Entanglement across journey steps with UX resistance/boost
    # Hero impression: Low friction on clean white background allows high transmission
    qml.CNOT(wires=[0, 1])
    qml.RZ(ux_parameters[0] * np.pi, wires=1)

    # Catalog & Filter discovery: Live search & telemetry boosts engagement
    qml.CNOT(wires=[1, 2])
    qml.RZ(ux_parameters[1] * np.pi, wires=2)

    # Social Expeditions & 30% deposit anchor: Reduces resistance on checkout
    qml.CNOT(wires=[2, 3])
    qml.RY(-ux_parameters[2] * np.pi, wires=3)

    # Checkout clarity: Visible calendar and Yape/Plin direct
    qml.RX(ux_parameters[3] * np.pi, wires=3)

    return [qml.expval(qml.PauliZ(i)) for i in range(num_qubits)]

archetypes = [
    ("Solo Traveler Aventurero", "Móvil / Solo", 0.90, 0.45, 0.55, 0.90),
    ("Pareja Romántica Trekking", "Desktop / Pareja", 0.85, 0.65, 0.40, 0.75),
    ("Montañista Técnico UIAGM", "Desktop / Experto", 0.95, 0.80, 0.30, 0.85),
    ("Estudiante Universitario Mochilero", "Móvil / Low-Cost", 0.75, 0.35, 0.85, 0.95),
    ("Ejecutivo Fin de Semana Lima", "Móvil / Escapada", 0.80, 0.25, 0.35, 0.90),
    ("Grupo Amigos de Oficina (4 pax)", "Desktop / Líder Tribu", 0.90, 0.50, 0.60, 0.80),
    ("Turista Extranjero Inglés/Español", "Móvil / Internacional", 0.85, 0.40, 0.25, 0.75),
    ("Fotógrafo de Paisajes Andinos", "Desktop / Visual", 0.80, 0.70, 0.45, 0.85),
    ("Chica Outdoor Primeriza", "Móvil / Dudosa", 0.65, 0.40, 0.65, 0.80),
    ("Viajero Frecuente Cusco/Huaraz", "Móvil / Recurrente", 0.92, 0.55, 0.50, 0.90),
]

synthetic_users = []
for i in range(50):
    base = archetypes[i % len(archetypes)]
    jitter = (np.random.rand(4) - 0.5) * 0.08
    synthetic_users.append({
        "id": f"LX-U{(i+1):02d}",
        "name": f"{base[0]} #{((i//len(archetypes))+1)}",
        "segment": base[1],
        "intent": float(np.clip(base[2] + jitter[0], 0.1, 0.99)),
        "patience": float(np.clip(base[3] + jitter[1], 0.1, 0.99)),
        "price_sens": float(np.clip(base[4] + jitter[2], 0.05, 0.99)),
        "tech": float(np.clip(base[5] + jitter[3], 0.1, 0.99)),
    })

# Calibrated UX Parameters of CURRENT www.lifextreme.store:
# 1. Hero Friction = 0.10 (Clean white, high contrast H1, clear value prop, zero lag)
# 2. Catalog Friction = 0.12 (Live search, region chips, instant card loading, live telemetry)
# 3. Group Value Boost = 0.28 (Strong boost: 30% deposit anchor, Lifecoins -S/50, verified guides)
# 4. Checkout Friction = 0.15 (3-step wizard with readable text, visible calendar days, Yape/Plin direct)
current_ux_params = np.array([0.10, 0.12, 0.28, 0.15], requires_grad=False)

results = []
for u in synthetic_users:
    u_feat = np.array([u["intent"], u["patience"], 1.0 - u["price_sens"], u["tech"]], requires_grad=False)
    expvals = lifextreme_quantum_circuit(u_feat, current_ux_params)

    p_hero = float((1 + expvals[0]) / 2)
    p_catalog = float((1 + expvals[1]) / 2)
    p_group_eval = float((1 + expvals[2]) / 2)
    p_checkout = float((1 + expvals[3]) / 2)

    drop_stage = "RESERVA EXITOSA"
    if p_hero < 0.35:
        drop_stage = "Rebote en Hero"
    elif p_catalog < 0.35:
        drop_stage = "Abandono en Filtro/Búsqueda"
    elif p_group_eval < 0.35:
        drop_stage = "Duda en Tarifa / Espera de Quórum"
    elif p_checkout < 0.45:
        drop_stage = "Abandono en Pago / Firma Digital"

    converted = (drop_stage == "RESERVA EXITOSA")

    results.append({
        "id": u["id"],
        "name": u["name"],
        "segment": u["segment"],
        "p_hero": round(p_hero, 3),
        "p_catalog": round(p_catalog, 3),
        "p_group": round(p_group_eval, 3),
        "p_checkout": round(p_checkout, 3),
        "drop_stage": drop_stage,
        "converted": converted
    })

total = len(results)
conversions = sum(1 for r in results if r["converted"])
conv_rate = (conversions / total) * 100

drop_breakdown = {}
for r in results:
    s = r["drop_stage"]
    drop_breakdown[s] = drop_breakdown.get(s, 0) + 1

output = {
    "site": "https://www.lifextreme.store",
    "total_simulated": total,
    "conversions": conversions,
    "conversion_rate": round(conv_rate, 1),
    "drop_breakdown": drop_breakdown,
    "stage_retention_avg": {
        "hero_retention": round(float(np.mean([r["p_hero"] for r in results])) * 100, 1),
        "catalog_retention": round(float(np.mean([r["p_catalog"] for r in results])) * 100, 1),
        "group_value_retention": round(float(np.mean([r["p_group"] for r in results])) * 100, 1),
        "final_checkout_retention": round(float(np.mean([r["p_checkout"] for r in results])) * 100, 1)
    },
    "sample_users": results[:15]
}

print(json.dumps(output, indent=2, ensure_ascii=False))
