import sys

# Forzar codificación UTF-8 para la consola de Windows
sys.stdout.reconfigure(encoding='utf-8')

try:
    from semantic_router import Route, RouteLayer
    from semantic_router.encoders import OllamaEncoder
except ImportError as e:
    print(f"Error: La librería semantic-router no está instalada o falta una dependencia. Detalles: {e}")
    sys.exit(1)

print("======================================================")
print("🚦 INICIANDO EL RECEPCIONISTA B2B (SEMANTIC ROUTER) 🚦")
print("======================================================")
print("Conectando con tu modelo local 'nomic-embed-text' en Ollama...")

# 1. Configurar el Encoder usando el motor local de Ollama (100% Gratis y Privado)
try:
    encoder = OllamaEncoder(model="nomic-embed-text")
except Exception as e:
    print(f"Error conectando con Ollama: {e}")
    print("Asegúrate de que Ollama esté abierto en tu computadora.")
    sys.exit(1)

# 2. Diseñar las "Autopistas" (Routes)
ruta_ventas = Route(
    name="Ventas y Cotizaciones",
    utterances=[
        "quiero una cotización para un grupo",
        "cuánto cuesta el tour a salkantay",
        "precio del full day en lunahuaná",
        "tienen cupos disponibles para mañana?",
        "pasame su catálogo de paquetes",
        "necesito reservar para 5 pasajeros"
    ]
)

ruta_legal = Route(
    name="Leyes y Seguridad (Qdrant RAG)",
    utterances=[
        "cuáles son las leyes del mincetur",
        "qué protocolos de rescate exigen en la selva",
        "el clima en huaraz es seguro hoy?",
        "qué certificados de defensa civil necesito",
        "hay alerta del senamhi para arequipa?",
        "restricciones de la capitanía de puerto"
    ]
)

ruta_casual = Route(
    name="Conversación Casual",
    utterances=[
        "hola, buenos días",
        "cómo estás?",
        "quién eres?",
        "gracias por la información",
        "hasta luego"
    ]
)

# 3. Empaquetar todo en el Router
routes = [ruta_ventas, ruta_legal, ruta_casual]
router = RouteLayer(encoder=encoder, routes=routes)

print("\n✅ ¡Recepcionista Listo! El sistema analizará tus mensajes en 0.1 segundos.")
print("Escribe un mensaje de prueba simulando ser una agencia de turismo.")
print("(Escribe 'salir' para terminar)\n")

# 4. Bucle interactivo del chat
while True:
    mensaje_cliente = input("Mensaje del Cliente > ")
    if mensaje_cliente.lower() in ['salir', 'exit', 'quit']:
        print("Apagando el Recepcionista...")
        break
    
    if not mensaje_cliente.strip():
        continue

    # AQUÍ SUCEDE LA MAGIA: Clasificación instantánea sin usar un LLM pesado
    resultado = router(mensaje_cliente)
    
    print("-" * 50)
    if resultado.name == "Ventas y Cotizaciones":
        print("🎯 DECISIÓN DEL ROUTER: [Ventas B2B]")
        print("👉 Acción recomendada: Mostrar catálogo, dar precios, invitar a reservar.")
        
    elif resultado.name == "Leyes y Seguridad (Qdrant RAG)":
        print("⚖️ DECISIÓN DEL ROUTER: [Seguridad y Leyes]")
        print("👉 Acción recomendada: Buscar en la base de datos Qdrant y usar Llama 3 para redactar la ley.")
        
    elif resultado.name == "Conversación Casual":
        print("👋 DECISIÓN DEL ROUTER: [Charla Casual]")
        print("👉 Acción recomendada: Responder el saludo cordialmente.")
        
    else:
        print("❓ DECISIÓN DEL ROUTER: [No Identificado]")
        print("👉 Acción recomendada: Transferir con un humano o pedir que especifique.")
    
    print("-" * 50 + "\n")
