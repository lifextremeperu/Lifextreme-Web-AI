---
name: first-customer-finder-cusco
description: Skill de investigación GTM (adaptado de carolinacherry/claude-first-customer-finder-skill) para encontrar agencias de turismo en Cusco y LATAM con señales reales de compra (contratación en Computrabajo/Bumeran/LinkedIn, cuellos de botella en cotizaciones/reservas o reseñas de demora), verificar fuentes y generar base de datos + reporte HTML con mensajes 1-a-1.
---

# First Customer Finder · Lifextreme Cusco / LATAM

Skill de investigación comercial en modo **francotirador (solo lectura e investigación, nunca envía correos automáticamente)**.

## Flujo de 5 Fases

1. **Definición de ICP (Lifextreme B2B):**
   - **Producto:** Capacitación práctica In-Office e implementación de Agentes IA (Claude Cowork / automatización de cotizaciones, reservas y atención 24/7) para agencias de turismo.
   - **Cliente Ideal:** Agencias operadoras y receptivas en Cusco / Perú / LATAM con RUC 20, sitio web propio, correo corporativo y equipo comercial/operativo activo.
   - **Descalificadores:** Agencias sin web activa, correos gratuitos genéricos sin presencia operativa verificable, o empresas sin señales de crecimiento/demanda.

2. **Búsqueda de Señales Públicas de Compra (Perú / LATAM):**
   - **Señal 1 (Expansión / Saturación Comercial):** Vacantes activas en *Computrabajo Perú*, *Bumeran*, *LinkedIn Jobs*, *Indeed* u *OpciónEmpleo* buscando:
     - *Travel Designer / Ejecutivo de Ventas / Cotizador de Paquetes Turísticos*
     - *Asistente o Ejecutivo de Reservas / Operaciones* (mención de *Tourplan*, CRM, idiomas inglés/francés/alemán, alto volumen de WhatsApp).
   - **Señal 2 (Fricción Operativa en Reseñas):** Comentarios recientes en *TripAdvisor* o *Google Maps* mencionando demoras en cotizaciones o falta de respuesta por WhatsApp/correo.

3. **Pasada de Verificación Anti-Alucinaciones:**
   - Cruzar cada agencia encontrada contra fuentes reales (portal de empleo / web oficial / registro local `reportes_b2b/cusco_agencias_limpio.csv` y `reportes_b2b/prospectos_cusco.db`).
   - Verificar que el correo no tenga errores de tipeo y comprobar si ya fue contactada en lotes anteriores.

4. **Scoring y Priorización (0–100):**
   - **Urgencia / Señal (0–50):** Vacante activa reciente en ventas/reservas (+35), exigencia de múltiples idiomas o ERP como Tourplan (+15).
   - **Encaje ICP (0–50):** RUC 20 (+15), web activa (+15), correo corporativo (+10), operación receptiva multi-día (+10).

5. **Entregables (Sin Envío Automático):**
   - Base de datos estructurada: `reportes_b2b/prospectos_sniper_cusco.json` y tabla `prospectos_sniper_cusco` en `reportes_b2b/prospectos_cusco.db`.
   - Reporte HTML compartible: `reportes_b2b/reporte_sniper_10_agencias_cusco.html` con evidencia de la señal y mensaje 1-a-1 hiper-personalizado para revisión humana.
