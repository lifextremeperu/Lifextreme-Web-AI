import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from telegram_notifier import send_message

msg = """🧠 *REPORTE EJECUTIVO DE NEUROMARKETING E IA* 🧠

¡Hola! Hoy hemos dado un salto evolutivo en la plataforma Lifextreme. Hemos dejado atrás los "chatbots" tradicionales para construir una **Arquitectura Multi-Agente Autónoma**.

🎯 *¿Qué logramos hoy?*
1. **Auditoría Cognitiva en Tiempo Real:** Le dimos a la IA "ojos" (Web Scraper). Ahora entra a la web de las agencias de turismo y detecta sus puntos ciegos comerciales.
2. **Consultor B2B Premium:** Reprogramamos la mente de la IA para que deje de dar consejos teóricos. Ahora entrega tácticas de *Ventas de Guerrilla* que atacan directamente los "puntos de dolor" del operador.

🧠 *El Potencial Psicológico y Comercial:*
* **Reducción de Carga Cognitiva:** El operador ya no tiene que hacer un análisis FODA aburrido; la IA audita su modelo de negocio en 3 minutos.
* **Sesgo de Autoridad:** Al estructurar la respuesta con un diagnóstico rudo y táctico, el operador percibe a Lifextreme como la máxima autoridad del sector.
* **Activación del Cerebro Límbico:** Las tácticas generadas por nuestra IA le enseñan al operador a vender tocando las emociones del turista (generando escasez, urgencia y exclusividad) en lugar de competir por precio.

Estamos construyendo un ecosistema donde la Inteligencia Artificial no solo asiste, sino que *psicoanaliza* y escala negocios de forma automática. ¡El potencial de retención y conversión B2B es masivo! 🚀"""

if send_message(msg):
    print("Mensaje enviado con éxito a Telegram.")
else:
    print("Error: No se pudo enviar el mensaje a Telegram.")
