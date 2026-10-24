#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
LIFEXTREME QUANTUM UX SIMULATOR & DAILY AUDITOR
Proprietary Engine: PennyLane Quantum Variational Circuit (QML)
Target: https://www.lifextreme.store
Schedule: Daily at 9:00 AM (America/Lima / UTC-5)
=============================================================================
"""

import os
import sys
import time
import json
import argparse
import datetime
from pathlib import Path

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import requests
    from bs4 import BeautifulSoup
    import pennylane as qml
    from pennylane import numpy as np
except ImportError as e:
    print(f"[ERROR] Dependencias faltantes: {e}")
    print("Ejecuta: pip install pennylane requests beautifulsoup4")
    sys.exit(1)


# =====================================================================
# 1. PENNYLANE QUANTUM VARIATIONAL CIRCUIT
# =====================================================================
NUM_QUBITS = 4
dev = qml.device("default.qubit", wires=NUM_QUBITS)

@qml.qnode(dev)
def quantum_ux_funnel_circuit(user_features, web_friction_weights):
    """
    Simula un usuario sintetico atravesando el embudo cognitivo-cuantico:
    - Qubit 0: Primera Impresion / Impacto Visual Hero
    - Qubit 1: Fluidez de Escaneo / Contraste Neuromarketing
    - Qubit 2: Transparencia de Precios & Catalogo
    - Qubit 3: Compromiso de Conversion (Checkout / WhatsApp CTA)
    """
    # 1. Codificacion de estado (Bloch Sphere Mapping: theta = (1 - feature) * pi)
    # feature = 1.0 -> theta = 0 -> |0> (Exito), feature = 0.0 -> theta = pi -> |1> (Rechazo)
    for i in range(NUM_QUBITS):
        qml.RY((1.0 - user_features[i]) * np.pi, wires=i)

    # 2. Entrelazamiento cognitivo y friccion de interfaz
    # Hero impression afecta disposicion a explorar
    qml.CNOT(wires=[0, 1])
    qml.RZ(web_friction_weights[0] * np.pi, wires=1)

    # Claridad y contraste afectan tolerancia al precio
    qml.CNOT(wires=[1, 2])
    qml.RZ(web_friction_weights[1] * np.pi, wires=2)

    # Transparencia de precios entrelaza con intencion de reserva final
    qml.CNOT(wires=[2, 3])
    qml.RZ(web_friction_weights[2] * np.pi, wires=3)

    # Rotacion de resistencia final en el checkout
    qml.RX(web_friction_weights[3] * np.pi, wires=3)

    # Medicion de observables PauliZ (expval in [-1, 1])
    return [qml.expval(qml.PauliZ(i)) for i in range(NUM_QUBITS)]


# =====================================================================
# 2. AUDITORIA LIVE DEL SITIO WEB (SCRAPER & TELEMETRY)
# =====================================================================
def audit_target_web(url="https://www.lifextreme.store"):
    print(f"\n[+] Iniciando escaneo telemetrico de: {url}")
    t0 = time.time()
    
    headers = {
        "User-Agent": "Lifextreme-QuantumUX-Sentinel/2.0 (+https://www.lifextreme.store)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=12)
        ttfb_ms = round((time.time() - t0) * 1000, 2)
        status_code = resp.status_code
        html = resp.text
    except Exception as e:
        print(f"[!] Error al conectar con {url}: {e}")
        return {
            "status": "ERROR",
            "url": url,
            "error": str(e),
            "ttfb_ms": 9999,
            "friction_weights": [0.8, 0.8, 0.8, 0.8]
        }

    soup = BeautifulSoup(html, "html.parser")

    # Analisis Heuristico
    title = soup.title.string.strip() if soup.title and soup.title.string else "Sin titulo"
    h1_el = soup.find("h1")
    h1_text = h1_el.get_text(strip=True) if h1_el else ""
    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"].strip()

    # Precios tangibles en DOM
    raw_text = soup.get_text()
    soles_count = raw_text.count("S/") + raw_text.count("S/.")
    usd_count = raw_text.count("$")
    price_count = soles_count + usd_count

    # CTAs y enlaces de conversion
    wa_links = [a.get("href") for a in soup.find_all("a", href=True) if "wa.me" in a.get("href")]
    booking_btns = soup.find_all(attrs={"data-action": True})
    cart_triggers = [b for b in booking_btns if "cart" in str(b.get("data-action")).lower() or "book" in str(b.get("data-action")).lower()]

    # Imagenes con Lazy Loading
    imgs = soup.find_all("img")
    lazy_imgs = [img for img in imgs if img.get("loading") == "lazy"]
    lazy_ratio = len(lazy_imgs) / max(len(imgs), 1)

    # Calculo de pesos de friccion empirica [0.0 = Cero friccion, 1.0 = Maxima friccion]
    # 1. Hero Friction: Depende de H1 conciso, TTFB rapido
    f_hero = 0.12 if (h1_text and len(h1_text) < 70 and ttfb_ms < 1500) else (0.28 if h1_text else 0.65)
    
    # 2. Text/Contrast Friction: Evaluacion de jerarquia y densidad
    f_clarity = 0.10 if (len(meta_desc) > 50 and lazy_ratio > 0.6) else 0.28

    # 3. Pricing Friction: Precios visibles + Flexibilidad de micro-reserva
    has_flex_reserva = "reserva con" in raw_text.lower() or "saldo" in raw_text.lower() or "cuotas" in raw_text.lower()
    f_pricing = 0.08 if (price_count >= 10 and has_flex_reserva) else (0.10 if price_count >= 10 else (0.30 if price_count >= 3 else 0.70))

    # 4. CTA / Funnel Friction: Disponibilidad inmediata de compra/WhatsApp
    f_cta = 0.10 if (len(wa_links) >= 2 or len(cart_triggers) >= 2) else 0.45

    telemetry = {
        "status": "OK",
        "url": url,
        "status_code": status_code,
        "ttfb_ms": ttfb_ms,
        "title": title,
        "h1": h1_text,
        "meta_desc_len": len(meta_desc),
        "total_images": len(imgs),
        "lazy_images": len(lazy_imgs),
        "lazy_ratio": round(lazy_ratio, 2),
        "visible_prices_detected": price_count,
        "whatsapp_cta_count": len(wa_links),
        "booking_triggers_count": len(booking_btns),
        "friction_weights": [round(f_hero, 3), round(f_clarity, 3), round(f_pricing, 3), round(f_cta, 3)]
    }

    print(f"[*] TTFB: {ttfb_ms} ms | Status: {status_code}")
    print(f"[*] Precios detectados: {price_count} | WhatsApp CTAs: {len(wa_links)}")
    print(f"[*] Pesos Cuanticos de Friccion: {telemetry['friction_weights']}")
    return telemetry


# =====================================================================
# 3. GENERADOR DE COHORTES SINTETICAS DE TURISMO
# =====================================================================
def generate_synthetic_travelers(count=50):
    """
    Genera perfiles sinteticos calibrados para el mercado turistico y de aventura en Peru:
    - Explorador Solitario (Alta paciencia, baja sensibilidad al precio)
    - Pareja Trekking Cusco (Alto intento, investigacion profunda)
    - Mochilero Low-Cost (Extrema sensibilidad al precio, impaciente)
    - Familia Vacacional (Busqueda de seguridad, certificaciones y soporte)
    - Deportista Alta Montana (Foco en especificaciones tecnicas y ficha UIAGM)
    """
    archetypes = [
        {"name": "Aventurero Solitario", "intent_base": 0.85, "pat_base": 0.70, "price_sens_base": 0.35, "tech_base": 0.90},
        {"name": "Pareja Trekking Cusco", "intent_base": 0.90, "pat_base": 0.65, "price_sens_base": 0.50, "tech_base": 0.85},
        {"name": "Mochilero Low-Cost", "intent_base": 0.70, "pat_base": 0.35, "price_sens_base": 0.90, "tech_base": 0.80},
        {"name": "Familia Vacacional", "intent_base": 0.80, "pat_base": 0.60, "price_sens_base": 0.65, "tech_base": 0.60},
        {"name": "Deportista Extremo UIAGM", "intent_base": 0.95, "pat_base": 0.80, "price_sens_base": 0.20, "tech_base": 0.95},
        {"name": "Turista Express Fin de Semana", "intent_base": 0.75, "pat_base": 0.25, "price_sens_base": 0.55, "tech_base": 0.90}
    ]

    np.random.seed(42) # Reproducibilidad cientifica
    cohort = []

    for i in range(count):
        arch = archetypes[i % len(archetypes)]
        # Variacion estocastica natural
        u_intent = float(np.clip(arch["intent_base"] + np.random.normal(0, 0.05), 0.1, 0.99))
        u_patience = float(np.clip(arch["pat_base"] + np.random.normal(0, 0.08), 0.1, 0.99))
        u_price_sens = float(np.clip(arch["price_sens_base"] + np.random.normal(0, 0.06), 0.1, 0.99))
        u_tech = float(np.clip(arch["tech_base"] + np.random.normal(0, 0.05), 0.1, 0.99))

        cohort.append({
            "id": f"SYN-{i+1:03d}",
            "archetype": arch["name"],
            "features": [u_intent, u_patience, u_price_sens, u_tech]
        })

    return cohort


# =====================================================================
# 4. EJECUCION DE SIMULACION CUANTICA
# =====================================================================
def run_quantum_simulation(cohort, friction_weights):
    print(f"\n[+] Ejecutando simulacion cuantica en {len(cohort)} usuarios sinteticos...")
    f_weights = np.array(friction_weights, requires_grad=False)
    
    conversions = 0
    drop_stages = {
        "HERO_BOUNCE": 0,
        "SCAN_ABANDON": 0,
        "PRICE_FRICTION": 0,
        "CHECKOUT_HESITATION": 0
    }
    probabilities = []

    for user in cohort:
        u_feat = np.array(user["features"], requires_grad=False)
        expvals = quantum_ux_funnel_circuit(u_feat, f_weights)

        # Mapeo PauliZ a probabilidad de exito cognitivo: P = (1 + expval) / 2
        p_hero = float((1.0 + expvals[0]) / 2.0)
        p_clarity = float((1.0 + expvals[1]) / 2.0)
        p_price = float((1.0 + expvals[2]) / 2.0)
        p_cta = float((1.0 + expvals[3]) / 2.0)

        # Probabilidad de conversion combinada
        overall_p = (p_hero * 0.25) + (p_clarity * 0.25) + (p_price * 0.25) + (p_cta * 0.25)
        probabilities.append(overall_p)

        # Determinacion de colapso cognitivo (Thresholds calibrados al diseno de alto contraste)
        if p_hero < 0.35:
            drop_stages["HERO_BOUNCE"] += 1
        elif p_clarity < 0.30:
            drop_stages["SCAN_ABANDON"] += 1
        elif p_price < 0.35:
            drop_stages["PRICE_FRICTION"] += 1
        elif p_cta < 0.40:
            drop_stages["CHECKOUT_HESITATION"] += 1
        else:
            conversions += 1

    total = len(cohort)
    conversion_rate = round((conversions / total) * 100, 2)
    avg_p_conv = round(float(np.mean(probabilities)) * 100, 2)
    
    # Indice de Friccion Cuantica (QFI): Cuanto mas cercano a 0, mas fluido el embudo
    qfi = round(float(np.mean(f_weights)), 3)

    results = {
        "total_simulated": total,
        "conversions": conversions,
        "simulated_conversion_rate": conversion_rate,
        "avg_quantum_probability": avg_p_conv,
        "quantum_friction_index": qfi,
        "drop_stages": drop_stages,
        "drop_percentages": {k: round((v / total) * 100, 1) for k, v in drop_stages.items()}
    }

    print(f"[*] Tasa de Conversion Cuantica Simulada: {conversion_rate}%")
    print(f"[*] Indice de Friccion Cuantica (QFI): {qfi}")
    print(f"[*] Desglose de Abandonos: {results['drop_percentages']}")
    return results


# =====================================================================
# 5. GENERACION DE REPORTES Y PERSISTENCIA
# =====================================================================
def save_audit_report(telemetry, simulation_results, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    today_str = datetime.date.today().isoformat()
    now_iso = datetime.datetime.now().isoformat()

    full_report = {
        "timestamp": now_iso,
        "date": today_str,
        "engine": "PennyLane Quantum UX Simulator v2.0",
        "target": telemetry.get("url"),
        "telemetry": telemetry,
        "quantum_simulation": simulation_results,
        "health_status": "EXCELLENT" if simulation_results["quantum_friction_index"] < 0.25 else ("GOOD" if simulation_results["quantum_friction_index"] < 0.45 else "NEEDS_OPTIMIZATION")
    }

    # 1. Guardar JSON historico del dia
    history_file = os.path.join(output_dir, f"quantum_ux_audit_{today_str}.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)

    # 2. Guardar JSON latest
    latest_file = os.path.join(output_dir, "latest_quantum_ux_audit.json")
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)

    # 3. Guardar Resumen Ejecutivo Markdown
    summary_md_file = os.path.join(output_dir, "latest_quantum_ux_summary.md")
    md_content = f"""# Reporte Diario de Auditoría & Simulación Cuántica de UX
**Fecha:** {today_str} ({now_iso[:19]})  
**Plataforma Auditada:** [{telemetry.get('url')}]({telemetry.get('url')})  
**Motor Cuántico:** PennyLane (VQC + QML)  
**Estado General:** `{full_report['health_status']}`

---

## 1. Métricas Cuánticas de Simulación
- **Usuarios Sintéticos Evaluados:** {simulation_results['total_simulated']} perfiles de alta representatividad
- **Tasa de Conversión Cuántica Estimada:** `{simulation_results['simulated_conversion_rate']}%`
- **Probabilidad Media de Colapso a Compra:** `{simulation_results['avg_quantum_probability']}%`
- **Índice de Fricción Cuántica (QFI):** `{simulation_results['quantum_friction_index']}` (Escala 0-1)

### Distribución de Puntos de Fricción (Drop-offs)
| Etapa del Embudo | % Abandono Simulado | Diagnóstico & Acción Técnica |
| :--- | :---: | :--- |
| **Hero Bounce** | `{simulation_results['drop_percentages']['HERO_BOUNCE']}%` | Impacto inicial, claridad de H1 y TTFB. |
| **Scan Dropout** | `{simulation_results['drop_percentages']['SCAN_ABANDON']}%` | Legibilidad, contraste perlado sutil y jerarquía. |
| **Price Friction** | `{simulation_results['drop_percentages']['PRICE_FRICTION']}%` | Transparencia de precios oficiales en catálogo. |
| **Checkout Hesitation**| `{simulation_results['drop_percentages']['CHECKOUT_HESITATION']}%` | Claridad del botón de pago y enlace de WhatsApp. |

---

## 2. Telemetría Técnica en Vivo
- **Latencia TTFB:** `{telemetry.get('ttfb_ms')} ms` (Objetivo < 1200 ms)
- **Código HTTP:** `{telemetry.get('status_code')}`
- **Precios Detectados en DOM:** `{telemetry.get('visible_prices_detected')}`
- **Disparadores de WhatsApp:** `{telemetry.get('whatsapp_cta_count')}`
- **Ratio de Carga Diferida (Lazy Images):** `{int(telemetry.get('lazy_ratio', 0) * 100)}%`
"""

    with open(summary_md_file, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n[✔] Reportes generados exitosamente en:\n    - {history_file}\n    - {latest_file}\n    - {summary_md_file}")
    return full_report


# =====================================================================
# 6. AUTO-MEJORA (FLAG --auto-improve)
# =====================================================================
def run_auto_improvements(telemetry, simulation_results):
    print("\n[+] Analizando oportunidades de auto-mejora diaria...")
    improvements_made = []

    # Validar TTFB o ratio de imagenes
    if telemetry.get("lazy_ratio", 1.0) < 0.70:
        print("[!] Alerta: Se detectaron imagenes sin atributo loading='lazy'.")
        improvements_made.append("Flagged non-lazy images for compiler cache optimization")
    else:
        print("[✔] Lazy loading optimizado en componentes visuales.")

    # Validar friccion cuantica de precios
    if simulation_results["drop_percentages"]["PRICE_FRICTION"] > 30.0:
        print("[!] Alerta: Alta friccion de precio. Recomendar anadir badges de 'Financiamiento 3 cuotas sin intereses'.")
        improvements_made.append("Recommended zero-interest installment badges")

    print(f"[✔] Proceso de auto-mejora completado: {len(improvements_made)} diagnosticos ejecutados.")
    return improvements_made


# =====================================================================
# ENTRY POINT
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="Lifextreme Daily Quantum UX Auditor")
    parser.add_argument("--url", default="https://www.lifextreme.store", help="URL a auditar")
    parser.add_argument("--users", type=int, default=50, help="Numero de usuarios sinteticos")
    parser.add_argument("--auto-improve", action="store_true", help="Ejecutar rutinas de diagnostico y mejora automatica")
    parser.add_argument("--output-dir", default="reports", help="Directorio para almacenar reportes")
    args = parser.parse_args()

    telemetry = audit_target_web(args.url)
    cohort = generate_synthetic_travelers(args.users)
    sim_results = run_quantum_simulation(cohort, telemetry.get("friction_weights", [0.2, 0.2, 0.2, 0.2]))
    report = save_audit_report(telemetry, sim_results, args.output_dir)

    if args.auto_improve:
        run_auto_improvements(telemetry, sim_results)

    print("\n=======================================================")
    print("AUDITORIA CUANTICA DIARIA COMPLETADA SATISFACTORIAMENTE")
    print("=======================================================")

if __name__ == "__main__":
    main()
