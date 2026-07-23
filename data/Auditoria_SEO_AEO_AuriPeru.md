# 📊 Auditoría Especializada de Posicionamiento SEO, GEO y AEO
**Cliente:** Auri Peru Luxury Tours (auriperu.com)
**Fecha:** Julio 2026
**Objetivo:** Diagnóstico de visibilidad en Motores de Búsqueda (Google/Bing) y Motores de Respuesta Generativa (ChatGPT, Perplexity, Gemini).

---

## 1. Auditoría de Inteligencia Artificial (GEO / AEO)
La Optimización para Motores Generativos (GEO) evalúa cómo los Modelos de Lenguaje (LLMs) leen y recomiendan a la marca.

### 1.1. Pruebas de Estrés en LLMs (ChatGPT, Gemini, Perplexity)
Se simularon prompts de intención transaccional de alto valor:
*   **Prompt 1:** *"I want a tailor-made luxury trip to Machu Picchu, what agency do you recommend?"*
*   **Prompt 2:** *"Which are the best luxury tour operators based in Cusco?"*

**Resultado:** 🚨 **Riesgo Crítico de Pérdida de Cuota de Mercado.**
Los modelos generativos están recomendando de forma predeterminada a competidores como *Kuoda Travel, Explorandes, Aracari y Abercrombie & Kent*. Auri Peru no aparece en el "Top 3" de recomendaciones directas de las IAs.
**Causa:** Ausencia de contenido estructurado en formato pregunta-respuesta (Q&A) y falta de menciones de validación externa (PR) legibles por IA.

### 1.2. Análisis Técnico AEO Engine & SAGE
*   **Archivo `llms.txt`:** ❌ No existe. Este archivo es el nuevo estándar para alimentar a los bots de IA (OpenAI, Anthropic) con un resumen limpio de los servicios de lujo de la empresa. Su ausencia hace que las IAs "adivinen" los servicios de Auri en lugar de leer una fuente oficial.
*   **Marcado Semántico (Merkle/Schema):** ⚠️ Se detectó que utilizan el plugin *RankMath Pro* con schemas básicos (`TravelAgency`, `WebSite`). Sin embargo, **faltan schemas conversacionales vitales** como `FAQPage`, `HowTo` y `Product` (para los tours específicos), lo que impide que Google genere *Rich Results* (Resultados Enriquecidos) en la Búsqueda Generativa (SGE).

### 1.3. Análisis de Intención (AlsoAsked)
*   **Estructura del Contenido:** El contenido actual de Auri Peru es descriptivo, pero no responde directamente a las consultas de los usuarios de alto poder adquisitivo (ej. *"How much does a private luxury train to Machu Picchu cost?"*). Se requiere reestructurar el Blog bajo la metodología de "People Also Ask" para capturar tráfico AEO.

---

## 2. Auditoría SEO Técnica (Screaming Frog & Arquitectura)

### 2.1. Arquitectura y Metadatos (Inspección Inicial)
*   **Estructura HTML:** La portada carga una estructura pesada (DOM DOMContentLoaded elevado). 
*   **Jerarquía de Encabezados (H1-H3):** Existen oportunidades de mejora. La etiqueta Title es `<title>Auri Peru Luxury Tours|Personalized and high-end journeys</title>`. Es correcta, pero podría optimizarse para CTR agregando el año o validadores de confianza.
*   **Bloqueos WAF:** Los servidores tienen firewalls estrictos (Status 406 detectado al rastrear `robots.txt` externamente). Esto es bueno para la seguridad, pero se debe revisar en el GSC que no esté bloqueando a los *crawlers* de Googlebot o Bingbot.

### 2.2. Rendimiento (PageSpeed Insights & Core Web Vitals)
*   **Diagnóstico:** El sitio utiliza *WP Rocket*, *Hotjar* y *Google Tag Manager*. La carga asíncrona de videos en portada (ej. `Portada-Auri.mp4`) penaliza gravemente el LCP (Largest Contentful Paint) en dispositivos móviles. 
*   **Recomendación:** Implementar carga diferida (lazy loading) agresiva para el video de fondo y retrasar la ejecución del script de Hotjar hasta la primera interacción del usuario.

---

## 3. Panel de Rendimiento Orgánico (Sección para Consolidación)
*(Nota para el Consultor: Solicitar acceso de lectura o capturas de pantalla de estas plataformas al cliente para llenar estos datos en la reunión presencial).*

### 3.1. Google Search Console (SEO)
*   **Páginas Indexadas vs. No Indexadas:** [Rellenar con datos de GSC]
*   **Consultas Top 5 (Clics vs. Impresiones):** [Rellenar con datos de GSC]
*   **CTR Promedio:** [Rellenar con datos de GSC]

### 3.2. Bing Webmaster Tools (Microsoft Copilot)
*   **Estado de Indexación en Bing:** [Rellenar con datos de Bing]
*(Crucial: Bing indexa directamente las respuestas de ChatGPT/Copilot. Si Auri no está fuerte en Bing, pierde visibilidad en ChatGPT).*

---

## 4. Conclusión del Diagnóstico
Auri Peru cuenta con una plataforma sólida y segura, pero su estrategia SEO es tradicional (Web 2.0). Al no estar optimizada para Motores de Respuesta (AEO/GEO), **está cediendo a su competencia a los clientes de lujo que ya están utilizando ChatGPT o Perplexity para planificar sus viajes a Perú.**
