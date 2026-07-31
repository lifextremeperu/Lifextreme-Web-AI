import sys
import time

# Forzar codificación UTF-8
sys.stdout.reconfigure(encoding='utf-8')

try:
    from mem0 import Memory
except ImportError:
    print("Error: mem0ai no está instalado. Ejecuta: pip install mem0ai")
    sys.exit(1)

print("======================================================")
print("🧠 INICIANDO CRM INTELIGENTE (MEM0 + OLLAMA) 🧠")
print("======================================================")
print("Conectando con tu cerebro local Llama 3 y Qdrant...\n")

# Configuración 100% Local (Cero costo de API)
config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3",
            "temperature": 0.1,
            "ollama_base_url": "http://localhost:11434",
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": "http://localhost:11434",
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "lifextreme_mem0_crm",
            "host": "localhost",
            "port": 6333,
        }
    }
}

try:
    m = Memory.from_config(config)
except Exception as e:
    print(f"Error inicializando Mem0: {e}")
    print("Asegúrate de tener Ollama y Qdrant ejecutándose.")
    sys.exit(1)

USER_ID = "andes_travel_sac"

print("======================================================")
print("Paso 1: EXTRAER Y MEMORIZAR PERFIL DEL CLIENTE")
print("======================================================")

mensaje_1 = "Hola, somos la agencia Andes Travel. Te aviso que a partir de ahora, todos los turistas que te enviemos son estrictamente veganos, y debido a su edad avanzada, no pueden hacer caminatas de más de 30 minutos. Exigen transporte privado tipo Sprinter."

print(f"[Mensaje entrante de Andes Travel]:\n\"{mensaje_1}\"")
print("\nPensando y guardando en Memoria a Largo Plazo...")

# Mem0 procesa el mensaje y extrae los recuerdos
m.add(mensaje_1, user_id=USER_ID)
print("✅ Preferencias guardadas exitosamente en Qdrant (Base de datos CRM).")

print("\n... (Pasan 3 meses) ...\n")
time.sleep(2)

print("======================================================")
print("Paso 2: RECUPERACIÓN MÁGICA Y PERSONALIZACIÓN")
print("======================================================")

mensaje_2 = "Hola Lifextreme, cotízame un full day a la Laguna 69 en Huaraz para un grupo que llega mañana."

print(f"[Nuevo Mensaje de Andes Travel]:\n\"{mensaje_2}\"")
print("\nConsultando el expediente del cliente en Mem0...")

# Recuperamos recuerdos relevantes para este usuario y contexto
recuerdos = m.search(query=mensaje_2, user_id=USER_ID)

if recuerdos and 'results' in recuerdos and recuerdos['results']:
    print("\n🧠 RECUERDOS ENCONTRADOS PARA 'Andes Travel':")
    for r in recuerdos['results']:
        print(f"   - {r['memory']}")
else:
    # Mem0 API puede variar ligeramente la estructura de respuesta
    print("\n🧠 RECUERDOS ENCONTRADOS PARA 'Andes Travel':")
    if isinstance(recuerdos, list):
         for r in recuerdos:
             mem_text = r.get('memory', r) if isinstance(r, dict) else r
             print(f"   - {mem_text}")
    else:
         print(f"   - {recuerdos}")

print("\n🤖 (Simulación de Respuesta de Llama 3 inyectada con recuerdos):")
print("¡Hola Andes Travel! Claro que sí. Para la Laguna 69, considerando que sus pasajeros no pueden caminar más de 30 minutos, les sugiero cambiar la ruta a la Laguna de Llanganuco (que permite acceso vehicular directo en Sprinter privada). Además, ya le comuniqué a nuestro chef que prepare un menú estrictamente vegano para todo el grupo. ¿Procedo con la reserva?")

print("\n======================================================")
print("¡Fase 3 Completada! Lifextreme ahora tiene memoria.")
print("======================================================")
