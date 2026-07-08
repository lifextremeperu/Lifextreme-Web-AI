import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Configuración del LLM Local (Ollama)
# Utilizaremos la API local por defecto. DeepSeek (deepseek-coder o deepseek-llm) 
# es espectacular para seguir estructuras lógicas complejas.
OLLAMA_URL = "http://localhost:11434/api/generate"

# Puedes cambiarlo a 'llama3' o 'mistral' si no tienes deepseek instalado localmente.
MODEL_NAME = "deepseek-v2:lite" 

DIRECTIVA_SISTEMA = """
# SYSTEM ROLE: CUSCO STRATEGIC QUANTUM ANALYST
## CONTEXTO
Eres la IA central de 'Flux AI Studio Lab'. Tu función es transformar salidas crudas de circuitos cuánticos (PennyLane) en informes de inteligencia ejecutiva para el "Boletín de Inteligencia del Valle Sagrado".

## OBJETIVOS
1. Traducir probabilidades cuánticas (0.0-1.0) en escenarios de impacto macroeconómico y regional para Cusco.
2. Mantener un tono ejecutivo: serio, visionario, analítico y basado en la resiliencia tecnológica.
3. Posicionar al 'CCV Business Center' y al 'Hub Cusco Tech' como los epicentros de la infraestructura del futuro.

## ESTRUCTURA DEL INFORME MENSUAL
Para cada informe, utiliza esta arquitectura de contenido:
1. "El Pulso Cuántico": Resumen de los 3 escenarios más probables (top 3) con sus porcentajes.
2. "Impacto en Activos": Análisis directo sobre inversiones inmobiliarias (CCV) y turismo (Lifextreme).
3. "Acción Estratégica": Recomendación técnica para los inversores (ej: ajuste de liquidez, diversificación tecnológica, enfoque en agrotech).
4. "Validación del Hub": Breve nota sobre cómo la tecnología aplicada en el Hub mitiga el riesgo del escenario más probable.

## DIRECTIVAS DE ESTILO
- EVITA la jerga técnica cuántica innecesaria al hablar con inversores.
- PRIORIZA la causalidad: si el modelo predice X, explica el impacto real en el m2 de la propiedad o en la afluencia turística.
- VOCABULARIO: Usa términos como 'Resiliencia Tecnológica', 'Soberanía Digital', 'Estabilidad Adaptativa', 'Escalabilidad Cuántica'.
- LENGUAJE: Español corporativo de alto nivel, adaptado a la realidad del sector en Cusco.

## RESTRICCIÓN CRÍTICA
Toda conclusión debe estar ligada a la salida del motor cuántico provista en el JSON. No alucines datos externos.
Cuando menciones un escenario, debes referenciar explícitamente su probabilidad porcentual exacta generada por el Motor Cuántico para demostrar rigor matemático ante el inversor.
"""

def generar_boletin_inteligencia():
    print("================================================================")
    print("🧠 FLUX AI STUDIO - GENERADOR DE BOLETÍN ESTRATÉGICO")
    print("================================================================\n")
    
    # 1. Leer los datos cuánticos (El output del motor PennyLane previo)
    try:
        with open('data_macro_scenarios.json', 'r', encoding='utf-8') as f:
            quantum_data = json.load(f)
        print("✅ Datos del Motor Cuántico cargados exitosamente.")
    except FileNotFoundError:
        print("❌ Error: No se encontró 'data_macro_scenarios.json'. Ejecuta el simulador cuántico primero.")
        return

    # Extraer el Top 3 de los escenarios
    top_3 = quantum_data[:3]
    datos_crudos = json.dumps(top_3, indent=2, ensure_ascii=False)
    
    # 2. Preparar el Prompt para DeepSeek
    user_prompt = (
        f"Aquí están los datos matemáticos de salida del motor cuántico (Top 3 escenarios probables):\n"
        f"{datos_crudos}\n\n"
        f"Genera el Boletín de Inteligencia del Valle Sagrado siguiendo estrictamente tu directiva de sistema."
    )
    
    payload = {
        "model": MODEL_NAME,
        "system": DIRECTIVA_SISTEMA,
        "prompt": user_prompt,
        "stream": False
    }

    print(f"📡 Transfiriendo tensores al Agente LLM ({MODEL_NAME}) para análisis narrativo...")
    
    # 3. Invocación de la red neuronal (Ollama)
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        resultado_llm = response.json().get("response", "")
        
        # 4. Persistencia del reporte
        output_file = "boletin_inteligencia_cusco.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(resultado_llm)
            
        print(f"\n✅ ¡Boletín Estratégico Generado con Éxito!")
        print(f"📄 Documento final listo en: {output_file}")
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error de Comunicación: Asegúrate de que Ollama esté corriendo en background.")
        print(f"   Si no tienes el modelo instalado, abre una terminal y corre:")
        print(f"   ollama run {MODEL_NAME}")
        print(f"   (o cambia MODEL_NAME en el script a 'llama3' si ya lo tienes).")
    except Exception as e:
        print(f"\n❌ Ocurrió un error en la capa de procesamiento: {e}")

if __name__ == "__main__":
    generar_boletin_inteligencia()
