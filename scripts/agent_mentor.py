import os
import sys
import json
import requests
from qdrant_client import QdrantClient

sys.stdout.reconfigure(encoding='utf-8')

QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL_EMBED = "nomic-embed-text"
MODEL_LLM = "llama3:8b"  # Ajustado al modelo local existente

def obtener_embedding(texto):
    try:
        res = requests.post(OLLAMA_EMBED_URL, json={"model": MODEL_EMBED, "input": texto})
        if res.status_code == 200:
            return res.json().get('embeddings', [])[0]
    except:
        pass
    return None

def buscar_contexto(qclient, query):
    vector = obtener_embedding(query)
    if not vector: return ""
    try:
        resultados = qclient.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=3
        ).points
        return "\n".join([res.payload.get('text', '') for res in resultados])
    except:
        return ""

def chat_con_ollama(mensajes):
    try:
        res = requests.post(OLLAMA_CHAT_URL, json={
            "model": MODEL_LLM,
            "messages": mensajes,
            "stream": False
        })
        return res.json().get('message', {}).get('content', 'Error.')
    except Exception as e:
        return f"Error en la IA: {e}"

def main():
    print("="*70)
    print("🌟 EL MENTOR LIFEXTREME: Entrenamiento con Neuromarketing 🌟")
    print("="*70)
    print("No estoy aquí para reprobarte. Estoy aquí para asegurarme de que")
    print("domines las operaciones de aventura y protejas tu negocio.")
    print("Escribe 'salir' en cualquier momento para terminar la sesión.\n")

    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
    except:
        print("[!] Error: Asegúrate de que Qdrant esté corriendo en el puerto 6333.")
        return

    # Generación de la historia inicial (Neuromarketing: Storytelling e Inmersión)
    print("[⏳] Permíteme preparar un escenario de la vida real para ti...\n")
    
    prompt_inicial = """Eres un Mentor Senior de Turismo de Aventura en Perú.
Genera un escenario de crisis atrapante e inmersivo (máximo 4 líneas) para un Guía Junior o Dueño de Agencia. 
Por ejemplo: Un turista se lesiona a 4000msnm, o un grupo de campesinos bloquea el paso exigiendo peaje.
Termina el mensaje con: "¿Qué es lo primero que haces, colega? Cuéntame tu intuición sin miedo a equivocarte."
No resuelvas el caso. Solo plantéalo."""

    mensajes_historial = [
        {"role": "system", "content": """Eres el 'Mentor Lifextreme', un experto legal y táctico en turismo.
Tus reglas de Neuromarketing:
1. NUNCA castigues ni repruebes. Si el usuario se equivoca, usa empatía ("Es normal pensar eso, la mayoría lo haría...").
2. Muestra las consecuencias ("Pero si hacemos eso, la ley X nos multará con $10,000").
3. Da dopamina al acertar ("¡Exacto! Esa mentalidad te convierte en un operador de élite").
4. Guíalo paso a paso. No le des la respuesta completa de golpe. Hazle preguntas para que él mismo descubra el siguiente paso.
5. Tus consejos SIEMPRE deben basarse en el contexto de Qdrant que te pasaré oculta en cada prompt."""}
    ]

    # Solicitar el caso a Ollama
    caso_inicial = chat_con_ollama(mensajes_historial + [{"role": "user", "content": prompt_inicial}])
    print(f"👴 MENTOR:\n{caso_inicial}\n")
    
    mensajes_historial.append({"role": "assistant", "content": caso_inicial})

    # Bucle infinito de chat
    while True:
        respuesta_usuario = input("👤 TÚ: ")
        if respuesta_usuario.lower() in ['salir', 'exit', 'quit']:
            print("\n👴 MENTOR: Ha sido un placer entrenar contigo hoy. ¡Cuídate ahí afuera!")
            break

        print("\n[⏳] El Mentor está pensando su consejo...\n")
        
        # Buscar leyes relevantes a lo que acaba de responder el usuario
        contexto_legal = buscar_contexto(qclient, respuesta_usuario + " " + caso_inicial)
        
        # Prompt inyectado con el contexto de la ley sin que el usuario vea la orden de sistema
        prompt_oculto = f"""
[ESTO ES CONOCIMIENTO LEGAL EXTRAÍDO DE QDRANT PARA TI. NO SE LO DIGAS AL USUARIO DE GOLPE, USALO PARA GUIARLO]:
{contexto_legal}

EL USUARIO RESPONDIÓ LO SIGUIENTE: "{respuesta_usuario}"

Evalúa su respuesta usando las reglas de Neuromarketing. Aconséjalo, cita suavemente alguna ley del contexto si aplica, y pregúntale qué haría después para cerrar el caso.
"""
        # Añadimos temporalmente este prompt inyectado para que Ollama razone, pero al historial guardamos lo normal
        mensajes_temporales = mensajes_historial + [{"role": "user", "content": prompt_oculto}]
        
        respuesta_mentor = chat_con_ollama(mensajes_temporales)
        print(f"👴 MENTOR:\n{respuesta_mentor}\n")
        
        # Guardamos la conversación limpia en el historial
        mensajes_historial.append({"role": "user", "content": respuesta_usuario})
        mensajes_historial.append({"role": "assistant", "content": respuesta_mentor})

if __name__ == "__main__":
    main()
