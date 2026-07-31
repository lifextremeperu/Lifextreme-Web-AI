import os
import sys

# Forzar codificación UTF-8
sys.stdout.reconfigure(encoding='utf-8')

try:
    from langfuse.openai import OpenAI
except ImportError:
    print("Error: La librería langfuse no está instalada o hay un conflicto.")
    print("Ejecuta: pip install langfuse openai")
    sys.exit(1)

print("======================================================")
print("📊 DEMOSTRACIÓN DE OBSERVABILIDAD (LANGFUSE) 📊")
print("======================================================")

# =================================================================
# ⚠️ INSTRUCCIONES: PEGA TUS CLAVES DE CLOUD.LANGFUSE.COM AQUÍ
# =================================================================
# Crea un proyecto gratis en cloud.langfuse.com, ve a Settings -> API Keys
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-b4aeb732-b719-4782-b920-877d4daf3d58"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-066e08d2-c884-4839-8df2-bedb4bf3a726"
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"
# =================================================================

if os.environ["LANGFUSE_SECRET_KEY"] == "sk-lf-...":
    print("\n❌ ALERTA: No has puesto tus claves API de Langfuse.")
    print("Por favor abre este archivo (demo_langfuse.py) y pega tus claves en las líneas 16 y 17.")
    sys.exit(1)

print("Iniciando conexión con Ollama Local y enviando telemetría a Langfuse Cloud...\n")

# Inicializamos el cliente de OpenAI pero apuntando a nuestro Ollama Local
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" # Ollama ignora la clave, pero la librería la requiere
)

pregunta = "Enumera 3 implementos de seguridad estrictamente obligatorios para hacer canotaje en Perú."
print(f"👤 Pregunta al bot: '{pregunta}'")
print("Pensando (y midiendo el tiempo para el panel de Langfuse)...\n")

try:
    # Esta llamada se procesa en tu PC (Ollama), pero los metadatos viajan a Langfuse Cloud
    completion = client.chat.completions.create(
        name="test_canotaje_b2b", # Así aparecerá el log en tu panel web
        model="llama3",
        messages=[
            {"role": "system", "content": "Eres un guía experto en turismo de aventura."},
            {"role": "user", "content": pregunta}
        ]
    )

    print("🤖 Respuesta de Llama 3 (Procesada 100% Local):")
    print(completion.choices[0].message.content)
    
    print("\n======================================================")
    print("✅ ¡Exito! La respuesta se generó en tu computadora.")
    
    # IMPORTANTE: Forzamos a Langfuse a enviar los datos a la nube antes de que se cierre el programa
    print("Sincronizando telemetría con la nube...")
    try:
        # Langfuse OpenAI SDK uses a background thread. Flush forces it to wait.
        client.flush() 
    except:
        pass
    import time
    time.sleep(2) # Pausa extra de seguridad
    
    print("👉 AHORA VE A TU PANEL WEB EN: https://cloud.langfuse.com")
    print("Busca la sección 'Traces' (Rastros) y verás esta misma conversación,")
    print("junto con el tiempo en milisegundos y los tokens gastados.")
    print("======================================================")

except Exception as e:
    print(f"\n❌ Error al ejecutar: {e}")
    print("Verifica que tus claves sean correctas y que Ollama esté abierto.")
