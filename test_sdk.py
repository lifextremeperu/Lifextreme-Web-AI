import asyncio
import sys
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig

async def main():
    print("=== INICIANDO AGENTE ANTIGRAVITY SDK ===")
    
    # Configuramos el agente (con capacidades de leer/escribir si fuera necesario)
    config = LocalAgentConfig(
        system_instructions="Eres el asistente experto de turismo de Lifextreme. Tu tarea es redactar correos profesionales.",
        capabilities=CapabilitiesConfig(), # Permite usar herramientas si es necesario
    )

    # Inicializamos el agente
    async with Agent(config) as agent:
        prompt = """
        Redacta un correo electrónico corto y persuasivo para un cliente potencial interesado 
        en nuestro tour al Ausangate. Menciónale que somos expertos certificados y 
        cumplimos con el Reglamento de Seguridad del MINCETUR.
        """
        
        print("\n[Solicitando redacción de correo al Agente...]\n")
        response = await agent.chat(prompt)

        # Imprimimos la respuesta en tiempo real
        async for token in response:
            sys.stdout.write(token)
            sys.stdout.flush()
        print("\n\n=== FIN TAREA AUTOMÁTICA ===")

if __name__ == "__main__":
    asyncio.run(main())
