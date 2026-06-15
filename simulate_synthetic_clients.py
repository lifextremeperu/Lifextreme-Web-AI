import os
import sys
import requests
import json
import time

API_URL = "http://127.0.0.1:8000/chat"
OLLAMA_URL = "http://localhost:11434/api/chat"

PROFILES = [
    {
        "id": "Carlos",
        "desc": "El Ahorrador Crítico",
        "system": "Eres Carlos, un turista peruano tacaño. Buscas el precio más bajo para hacer trekking. Exiges descuentos, preguntas si hay opciones grupales. Eres directo. Habla de forma concisa.",
        "init_msg": "Hola, quiero hacer un trekking cerca a Cusco pero todo está carísimo en las agencias. ¿Qué opciones tienen que sean baratas o cómo puedo hacer para no pagar tanto?"
    },
    {
        "id": "Elena",
        "desc": "La Mamá Segura",
        "system": "Eres Elena, una madre sobreprotectora. Quieres viajar con tus dos hijos adolescentes. Te aterra la altura, la falta de oxígeno y los accidentes. Preguntas por certificaciones. Habla de forma concisa.",
        "init_msg": "Buenas tardes. Quiero ir con mis hijos de 14 y 16 años a la montaña de colores, pero me da muchísimo miedo el soroche y un accidente. ¿Tienen oxígeno? ¿Es peligroso?"
    },
    {
        "id": "David",
        "desc": "El Alpinista Élite",
        "system": "Eres David, montañista profesional. Usas términos técnicos (crampones, piolets, UIAGM). Buscas montañas de más de 6000 metros en Huaraz o Cusco. Eres exigente. Habla de forma concisa.",
        "init_msg": "Qué tal. Busco una expedición técnica, algo sobre los 6000m en la Cordillera Blanca. Necesito guías certificados UIAGM y saber si alquilan equipo nivel pro para hielo."
    },
    {
        "id": "Sofia",
        "desc": "La Turista de Bienestar",
        "system": "Eres Sofía, una turista de lujo. Buscas paz, meditación, sonoterapia y glampings de alta gama. El dinero no es problema, buscas exclusividad. Habla de forma concisa y espiritual.",
        "init_msg": "Namasté. Necesito desconectarme. Busco alguna experiencia de sanación, sonoterapia o un glamping de lujo muy exclusivo lejos del ruido. ¿Qué tienen en esa línea?"
    },
    {
        "id": "Andres",
        "desc": "El Emprendedor",
        "system": "Eres Andrés, un emprendedor. Quieres saber cómo afiliarte al Portal Partners, vender tours de Lifextreme y las comisiones. Mensajes directos de negocios.",
        "init_msg": "Hola, vi su sección de Partners. Tengo una agencia y quiero saber cómo es el modelo de negocio con ustedes. ¿Qué porcentaje de comisión dan y cómo afilio a mi empresa?"
    }
]

TURNS = 2

def ask_max(message):
    try:
        res = requests.post(API_URL, json={"message": message}, timeout=60)
        if res.ok:
            return res.json().get('mensaje_principal', 'Sin mensaje principal')
        return f"Error HTTP {res.status_code}"
    except Exception as e:
        return f"Error de conexión con MAX: {e}"

def ask_persona(profile, chat_history):
    messages = [{"role": "system", "content": profile["system"]}]
    for msg in chat_history:
        messages.append(msg)
    
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": "phi3:latest",
            "messages": messages,
            "stream": False
        }, timeout=90)
        return res.json()['message']['content']
    except Exception as e:
        return f"Error de Ollama: {e}"

def run_simulation():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==================================================================")
    print(" 🚀 INICIANDO SIMULACIÓN MULTI-AGENTE (5 CLIENTES SINTÉTICOS) ")
    print("==================================================================")
    
    transcript = "# Reporte de Simulación Sintética MAX\n\n"
    
    for p in PROFILES:
        print(f"\n[>>>] CONECTANDO AGENTE: {p['id']} ({p['desc']})")
        transcript += f"## Cliente: {p['id']} - {p['desc']}\n"
        
        chat_history = []
        msg_user = p["init_msg"]
        
        print(f"👤 {p['id']}: {msg_user}")
        transcript += f"**👤 {p['id']}:** {msg_user}\n\n"
        chat_history.append({"role": "assistant", "content": msg_user})
        
        for turn in range(TURNS):
            print("🤖 MAX (Procesando con RAG...)")
            msg_max = ask_max(msg_user)
            print(f"🤖 MAX: {msg_max}")
            transcript += f"**🤖 MAX:** {msg_max}\n\n"
            
            chat_history.append({"role": "user", "content": f"El vendedor respondió: {msg_max}"})
            
            if turn < TURNS - 1:
                print(f"👤 {p['id']} (Razonando...)")
                msg_user = ask_persona(p, chat_history)
                print(f"👤 {p['id']}: {msg_user}")
                transcript += f"**👤 {p['id']}:** {msg_user}\n\n"
                chat_history.append({"role": "assistant", "content": msg_user})
        
        transcript += "---\n"
        
    print("\n[+] SIMULACIÓN COMPLETADA. Evaluando la calidad comercial de MAX...")
    
    eval_prompt = "Actúa como un Director de Ventas experto. Analiza la siguiente transcripción entre nuestro bot MAX y 5 clientes distintos. Extrae:\n1. ❌ Errores Críticos (alucinaciones, no resolver objeciones de precio, falta de empatía).\n2. ✅ Aciertos (buen uso del RAG, precisión).\n3. 🎯 Recomendación de Prompting para arreglar los errores.\n\nAquí la transcripción:\n" + transcript
    
    try:
        evaluation = ask_persona({"system": "Eres un auditor estricto de QA para IA de ventas de turismo."}, [{"role": "assistant", "content": eval_prompt}])
    except:
        evaluation = "Error evaluando el reporte final."
        
    transcript += f"\n## ⚖️ Auditoría Comercial Automática\n{evaluation}\n"
    
    with open("reporte_simulacion_max.md", "w", encoding="utf-8") as f:
        f.write(transcript)
        
    print(f"\n[✔] REPORTE DE CALIDAD GUARDADO: reporte_simulacion_max.md")
    print("\nPROCESO TERMINADO. ESTA VENTANA SE CERRARÁ EN 30 SEGUNDOS...")
    time.sleep(30)

if __name__ == "__main__":
    run_simulation()
