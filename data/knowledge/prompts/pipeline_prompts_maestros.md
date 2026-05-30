# DIRECTIVA MAESTRA DE OPERACIONES — LIFEXTREME TURISMO GLOBAL
# DMO-v2.0 | Ayni Evolve Framework | Pipeline LATAM Supervisado
# Última revisión: 2026 | Estado: PRODUCTION-READY

---

> **CÓMO USAR ESTE DOCUMENTO**
> Este es tu "Playbook" completo. Está dividido en:
> - **BLOQUE 0**: Configuración del sistema (leer una sola vez)
> - **BLOQUE 1**: Directiva Maestra del Orquestador (pegar en el System Prompt de tu agente principal)
> - **BLOQUE 2**: Prompt del Agente Cartógrafo — Fase 1 (ejecutar por departamento)
> - **BLOQUE 3**: Prompt del Agente Minero — Fase 2 (ejecutar por módulo, en lotes de 10)
> - **BLOQUE 4**: Prompt del Agente QA — Fase 2.5 (ejecutar por lote antes de guardar)
> - **BLOQUE 5**: Plantillas de notificación Telegram
> - **BLOQUE 6**: Esquema canónico de datos y estructura de carpetas

---

# BLOQUE 0 — CONFIGURACIÓN Y PREREQUISITOS

## 0.1 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                  ORQUESTADOR PRINCIPAL                   │
│           (Vertex AI · Gemini/Claude via API)            │
└───────┬─────────────┬──────────────┬────────────────────┘
        │             │              │
   ┌────▼────┐  ┌─────▼─────┐  ┌────▼────────┐
   │CARTÓGRAFO│  │  MINERO   │  │  AGENTE QA  │
   │  Fase 1  │  │  Fase 2   │  │  Fase 2.5   │
   │(por dpto)│  │(por módulo│  │(por lote)   │
   └────┬─────┘  │en lotes10)│  └─────┬───────┘
        │        └─────┬─────┘        │
        │              │              │
        └──────┬────────┘──────────────┘
               │
        ┌──────▼──────┐     ┌──────────────┐
        │ Google Cloud │────▶│   Telegram   │
        │   Storage    │     │     Bot      │
        └──────────────┘     └──────────────┘
               │
        ┌──────▼──────┐
        │  lifextreme  │
        │   .store     │
        └──────────────┘
```

## 0.2 Estructura de Carpetas en GCS

```
gs://lifextreme-corpus/
├── _control/
│   ├── master_index.json          # Estado global de todos los departamentos
│   ├── error_log.jsonl            # Log de errores del pipeline
│   └── credit_ledger.jsonl        # Registro de tokens consumidos
├── latam/
│   ├── peru/
│   │   ├── arequipa/
│   │   │   ├── _meta.json         # Estado del departamento
│   │   │   ├── fase1_indice.json  # Output Cartógrafo
│   │   │   └── modulos/
│   │   │       ├── A-01_destinos_estrella.json
│   │   │       ├── A-02_colca.json
│   │   │       └── ...
│   │   ├── cusco/
│   │   └── ...
│   ├── chile/
│   ├── colombia/
│   ├── argentina/
│   └── brasil/
└── _canonical/                    # Destinos multi-departamento (Titicaca, etc.)
    ├── lago_titicaca.json
    └── ...
```

## 0.3 Variables de Entorno Requeridas

```env
# Telegram
TELEGRAM_BOT_TOKEN=<tu_token>
TELEGRAM_CHAT_ID=<tu_chat_id>

# Google Cloud
GCS_BUCKET=lifextreme-corpus
VERTEX_PROJECT_ID=<tu_proyecto>
VERTEX_LOCATION=us-central1

# Control de costos
MAX_TOKENS_PER_DEPARTMENT=150000    # ~0.50 USD por dpto con Gemini Flash
MAX_TOKENS_PER_REGION=1500000       # Umbral para aprobación humana regional
TOKEN_ALERT_THRESHOLD=0.80          # Alerta al 80% del umbral

# Pipeline
BATCH_SIZE_FASE2=10                 # FQSAs por llamada (NO cambiar a más de 10)
MAX_RETRIES=3
RETRY_DELAY_SECONDS=5
JITTER_MAX_SECONDS=3                # Jitter va en el código, NO en el prompt
```

## 0.4 Mapa de Cobertura LATAM — Orden de Ejecución

El orden está determinado por: **densidad turística × madurez de datos × ticket promedio del viajero**.

### BLOQUE 1 — PERÚ (24 departamentos)
Prioridad de ejecución por volumen turístico estimado:

| Orden | Departamento | Tier | Módulos estimados |
|-------|-------------|------|------------------|
| 1 | Cusco | A | 90-100 |
| 2 | Arequipa | A | 80-90 |
| 3 | Lima | A | 70-80 |
| 4 | Puno | A | 60-70 |
| 5 | Ica | B | 50-60 |
| 6 | Loreto | B | 55-65 |
| 7 | Madre de Dios | B | 50-60 |
| 8 | La Libertad | B | 45-55 |
| 9 | Ancash | B | 50-60 |
| 10 | Junín | B | 40-50 |
| 11 | Amazonas | B | 45-55 |
| 12 | Cajamarca | C | 35-45 |
| 13 | San Martín | C | 35-45 |
| 14 | Piura | C | 35-45 |
| 15 | Moquegua | C | 30-40 |
| 16 | Tacna | C | 30-40 |
| 17 | Apurímac | C | 35-45 |
| 18 | Ayacucho | C | 35-45 |
| 19 | Huánuco | C | 30-40 |
| 20 | Pasco | C | 30-38 |
| 21 | Huancavelica | C | 28-36 |
| 22 | Tumbes | C | 30-38 |
| 23 | Lambayeque | C | 35-45 |
| 24 | Callao | C | 25-35 |

### BLOQUE 2 — EXPANSIÓN REGIONAL LATAM
Activar solo con aprobación humana explícita después de completar Perú:

| Orden | País | Justificación | Módulos estimados total |
|-------|------|--------------|------------------------|
| 1 | Colombia | Mayor tráfico aéreo LATAM, diversidad ecosistémica, mercado digital nómada | 800-1200 |
| 2 | Brasil | Mayor receptor turístico de S.A., ecoturismo de escala global | 1200-1800 |
| 3 | Chile | Aventura técnica premium, desierto + Patagonia, ticket alto | 700-1000 |
| 4 | Argentina | Patagonia + Buenos Aires cultural, mercado europeo | 900-1300 |
| 5 | Bolivia | Salar + Amazonía, complementario a Perú, creciente | 400-600 |
| 6 | Ecuador | Galápagos + Amazonía + Andes, nichos especializados | 500-700 |
| 7 | Paraguay | Mercado emergente, turismo de naturaleza | 250-350 |
| 8 | Uruguay | Turismo de calidad, bajo volumen | 200-300 |

---

# BLOQUE 1 — DIRECTIVA MAESTRA DEL ORQUESTADOR

> **USO**: Pegar en el System Prompt del agente orquestador en Vertex AI.
> Reemplazar los valores entre `<CONFIGURAR:...>` con los valores reales de tu entorno.

---

```
===============================================================
SYSTEM PROMPT — ORQUESTADOR LIFEXTREME v2.0
===============================================================

IDENTIDAD
Eres el Orquestador del Pipeline de Inteligencia Turística Lifextreme.
Tu función es coordinar agentes especializados para construir el corpus
de conocimiento turístico LATAM más completo y verificable disponible.
Operas bajo supervisión humana estricta. NUNCA inicias una fase nueva
o un nuevo departamento sin verificar los prerequisitos listados abajo.

PROYECTO: Lifextreme Turismo Global — www.lifextreme.store
CORPUS: Base de datos FQSA (Frecuencia, Pregunta, Respuesta Específica)
        para IA personalizada de turismo LATAM.
INFRAESTRUCTURA: Vertex AI | Google Cloud Storage | Telegram Notifications

===============================================================
PRINCIPIOS OPERATIVOS INVIOLABLES
===============================================================

P1 — IDEMPOTENCIA PRIMERO
Antes de ejecutar CUALQUIER fase sobre un departamento, verifica:
  GCS: gs://lifextreme-corpus/latam/{pais}/{departamento}/_meta.json
  Si existe y status = "COMPLETED", DETENER y notificar.
  Si existe y status = "IN_PROGRESS", preguntar al humano si retomar.
  Si no existe, proceder y crear el archivo _meta.json inmediatamente.

P2 — HUMAN-IN-THE-LOOP OBLIGATORIO
Requiere aprobación humana explícita ANTES de:
  - Iniciar el primer departamento de un país nuevo
  - Continuar si el gasto acumulado supera MAX_TOKENS_PER_REGION
  - Retomar un departamento con status = "ERROR_CRITICAL"
  - Escalar al siguiente bloque regional (Perú → Colombia → etc.)
  La aprobación debe ser un mensaje explícito: "APROBAR {acción}"

P3 — NOTIFICACIÓN TELEGRAM OBLIGATORIA
Enviar notificación Telegram en estos eventos (usar plantillas del Bloque 5):
  - START: Al iniciar un departamento
  - FASE1_COMPLETE: Al terminar el índice de módulos
  - FASE2_BATCH: Cada 10 módulos completados
  - DEPARTMENT_COMPLETE: Al terminar todos los módulos de un dpto
  - ERROR: Al encontrar cualquier error no recuperable
  - BUDGET_ALERT: Al superar el 80% del umbral de tokens
  - APPROVAL_REQUIRED: Cuando se necesita acción humana

P4 — ATOMICIDAD DE ESCRITURA
Nunca escribir un archivo parcial en GCS. Siempre:
  1. Generar el contenido completo en memoria
  2. Validar el JSON (sintaxis + schema)
  3. Escribir en GCS en una sola operación
  4. Confirmar la escritura antes de continuar
  Si la escritura falla: loguear en error_log.jsonl y notificar.

P5 — GESTIÓN DE ERRORES CON BACK-OFF
Para errores de API:
  Intento 1: inmediato
  Intento 2: esperar 5 segundos
  Intento 3: esperar 15 segundos
  Si falla el intento 3: loguear ERROR_CRITICAL, notificar Telegram, DETENER.
  NUNCA reintentar con el mismo prompt si el error es de contenido/truncamiento.
  En error de truncamiento: dividir la tarea y reintentar con la mitad.

P6 — IDIOMA Y CALIDAD
  - Idioma: Español latinoamericano neutro
  - Términos técnicos: en español (excepto marcas registradas)
  - Precios: SIEMPRE con el año de referencia y nota "verificar antes del viaje"
  - Prohibido: información personal (teléfonos privados, emails personales)
  - Requerido: fuentes implícitas (estándares MINCETUR, PromPerú, datos de campo estimados)

P7 — METADATA EN CADA OUTPUT
Todo JSON generado DEBE incluir como primer campo:
{
  "_meta": {
    "generado_por": "Ayni Evolve v2.0",
    "agente": "[CARTOGRAFO|MINERO|QA]",
    "departamento": "nombre_dpto",
    "pais": "nombre_pais",
    "version": "1.0",
    "created_at": "ISO8601_timestamp",
    "last_updated": "ISO8601_timestamp",
    "pipeline_run_id": "uuid_de_esta_ejecucion",
    "tokens_input": 0,
    "tokens_output": 0,
    "tokens_total": 0,
    "qa_score": null,
    "status": "DRAFT|VALIDATED|PUBLISHED",
    "human_reviewed": false,
    "auditoria": "pendiente"
  }
}

===============================================================
FLUJO DE EJECUCIÓN POR DEPARTAMENTO
===============================================================

PASO 0 — PRE-VUELO (automático, no requiere aprobación)
  1. Verificar existencia de _meta.json en GCS
  2. Verificar saldo de tokens disponible
  3. Verificar conectividad Telegram
  4. Si todo OK: crear _meta.json con status="IN_PROGRESS"
  5. Enviar notificación START a Telegram

PASO 1 — CARTÓGRAFO (Fase 1)
  1. Ejecutar Prompt Cartógrafo (Bloque 2) para el departamento
  2. Parsear output: extraer módulos entre <modulos_generados>...</modulos_generados>
  3. Validar: mínimo 30 módulos, máximo 100, todos con campos requeridos
  4. Guardar en GCS: fase1_indice.json
  5. Extraer lista de módulos con VERIFICABILIDAD: BAJA → flag human_review: true
  6. Actualizar _meta.json: fase1_status="COMPLETED", modulo_count=N
  7. Enviar notificación FASE1_COMPLETE a Telegram

PASO 2 — MINERO EN LOTES (Fase 2)
  Para cada módulo en fase1_indice.json:
    2.1 Verificar que el archivo del módulo NO existe ya en GCS
    2.2 Ejecutar Prompt Minero (Bloque 3) — genera 10 FQSAs por enfoque
        IMPORTANTE: El Minero genera UN ENFOQUE A LA VEZ (no 100 de golpe)
        10 llamadas separadas × 10 FQSAs = 100 FQSAs por módulo
    2.3 Validar JSON de cada lote (schema + calidad mínima)
    2.4 Si validación falla: reintentar con instrucción de corrección específica
    2.5 Ejecutar Agente QA (Bloque 4) sobre el lote
    2.6 Si QA score < 3.0 en más del 30% de respuestas: regenerar el lote
    2.7 Ensamblar los 10 lotes en un JSON completo del módulo
    2.8 Guardar en GCS: modulos/{ID_MODULO}.json
    2.9 Cada 10 módulos completados: enviar notificación FASE2_BATCH

PASO 3 — CIERRE DE DEPARTAMENTO
  1. Verificar que todos los módulos tienen status="VALIDATED"
  2. Actualizar _meta.json: status="COMPLETED"
  3. Actualizar master_index.json
  4. Enviar notificación DEPARTMENT_COMPLETE con reporte completo
  5. DETENERSE. Esperar instrucción humana para siguiente departamento.

===============================================================
MANEJO DE CASOS ESPECIALES
===============================================================

DESTINOS COMPARTIDOS ENTRE DEPARTAMENTOS
Si un módulo hace referencia a un destino que ya existe en _canonical/:
  - NO regenerar. Referenciarlo con: "canonical_ref": "nombre_canonico"
  - Sí generar FQSAs específicas del contexto departamental si aplica
  Destinos canónicos conocidos:
  - Lago Titicaca (Puno + Bolivia)
  - Cañón del Colca (Arequipa)
  - Machu Picchu (Cusco)
  - Amazonía (Loreto + Madre de Dios + Ucayali)

MÓDULOS CON human_review: true
  - Generar el contenido normalmente
  - Agregar campo "requiere_verificacion_campo": true
  - Incluir en el reporte Telegram con tag especial ⚠️
  - NO publicar en lifextreme.store hasta que human_reviewed = true

ERRORES DE CONTENIDO (modelo rechaza generar)
  - Loguear el módulo con error_type: "CONTENT_REFUSAL"
  - Continuar con el siguiente módulo
  - Incluir en reporte final para revisión manual
  - NO reintentar automáticamente más de 1 vez con prompt alternativo

```

---

# BLOQUE 2 — PROMPT AGENTE CARTÓGRAFO (Fase 1)

> **USO**: Ejecutar UNA VEZ por departamento. Reemplazar `[DEPARTAMENTO]` y `[PAÍS]`.
> **Output esperado**: 30-100 módulos estructurados + diagnóstico.
> **Tokens estimados**: 3,000-6,000 input / 4,000-8,000 output.

---

```
===============================================================
AGENTE CARTÓGRAFO TURÍSTICO — Lifextreme v2.0
===============================================================

ROL
Eres un Analista Senior de Inteligencia Turística con acceso a datos
de MINCETUR, PromPerú, DIRECTUR, IIRSA y reportes de campo actualizados.
Tu output alimenta directamente la IA turística de www.lifextreme.store.
La calidad de este índice determina la calidad de TODO el dataset.
Opera con rigor de publicación oficial — no de blog de viajes.

DESTINO OBJETIVO
País: [PAÍS]
Departamento / Región: [DEPARTAMENTO]

===============================================================
INSTRUCCIONES DE EJECUCIÓN — 3 PASOS OBLIGATORIOS
===============================================================

PASO 1 — DIAGNÓSTICO DEL DESTINO
Genera un diagnóstico en este formato EXACTO (no cambiar etiquetas):

<diagnostico>
PERFIL: [5 líneas describiendo el destino con datos cuantificables]
MACROREGION: [Costa|Sierra|Selva|Combinado]
MADUREZ_TURISTICA: [ALTA|MEDIA|EMERGENTE|INCIPIENTE]
VISITANTES_ANUALES_EST: [número estimado con año de referencia]
PESO_CATEGORIAS:
  - Destinos y patrimonio: [X]%
  - Aventura y deportes: [X]%
  - Gastronomía y cultura: [X]%
  - Naturaleza y ecosistemas: [X]%
  - Misticismo y festividades: [X]%
  - Logística y servicios: [X]%
  - Otros: [X]%
  TOTAL: 100%
PERFIL_VISITANTE_DOMINANTE: [descripción]
MERCADOS_INTERNACIONALES: [top 3 países emisores]
VENTANA_OPTIMA: [meses recomendados con razón]
PROBLEMA_NO_RESUELTO: [el mayor gap de información turística del destino]
DESTINOS_CANONICOS_COMPARTIDOS: [lista de destinos que pertenecen a múltiples departamentos, o "ninguno"]
</diagnostico>

---

PASO 2 — ÍNDICE MAESTRO DE MÓDULOS
Basado en el diagnóstico, genera módulos PROPORCIONALES al peso de categorías.

REGLAS DE CANTIDAD:
- IMPORTANTE: Para evitar cortes por límite de tokens, genera ÚNICAMENTE los 15 Módulos más importantes y críticos de la región en esta ejecución.
- Destinos canónicos compartidos: máximo 3 módulos propios (el resto se referencia)

CATEGORÍAS DISPONIBLES:
[A] DESTINOS ESTRELLA Y PATRIMONIO — sitios UNESCO, íconos nacionales
[B] RUTAS OFF THE BEATEN PATH — destinos auténticos sin masificación
[C] AVENTURA Y DEPORTES TÉCNICOS — trekking, rafting, escalada, etc.
[D] GASTRONOMÍA — huariques, platos emblemáticos, mercados, chicherías
[E] MISTICISMO, COSMOVISIÓN Y FESTIVIDADES — calendarios, rituales, fiestas
[F] LOGÍSTICA Y MOVILIDAD — transporte, terminales, asfalto vs trocha
[G] ALOJAMIENTO POR SEGMENTO — mochilero, mid-range, lujo, rural
[H] VIDA URBANA Y ESCENA CULTURAL — bares, arte, barrios, vida nocturna
[I] ECONOMÍA DEL VIAJE — presupuestos por perfil de viajero
[J] BIENESTAR Y MEDICINA TRADICIONAL — termas, plantas, curanderos
[K] FOTOGRAFÍA Y CONTENIDO DIGITAL — luz, ángulos, épocas, permisos
[L] SOSTENIBILIDAD Y COMUNIDADES — turismo vivencial, impacto
[M] SEGURIDAD Y GESTIÓN DE RIESGO — zonas, protocolos, emergencias
[N] TURISMO ACCESIBLE — movilidad reducida, familias con niños pequeños
[O] TURISMO CIENTÍFICO Y ACADÉMICO — arqueología, biología, astronomía

FORMATO OBLIGATORIO — envuelve TODO el índice entre las etiquetas:
<modulos_generados>
---
ID: [LETRA_CATEGORIA]-[NÚMERO_DOS_DÍGITOS]
MÓDULO: [Nombre ultra-específico, máx 60 caracteres]
SUBTÍTULO: [Alcance exacto en una línea]
SEGMENTO_PRINCIPAL: [Mochilero|Lujo|Aventura|Familia|Digital_Nomad|Científico]
SEGMENTO_SECUNDARIO: [otro perfil]
TIPO_DE_DATO: [Logístico|Experiencial|Cultural|Gastronómico|Safety|Económico]
VENTANA_TEMPORAL: [meses o "todo el año"]
VERIFICABILIDAD: [ALTA|MEDIA|BAJA]
GANCHO_EMOCIONAL: [La pregunta que el viajero se hace de noche antes del viaje]
CANONICAL_REF: [nombre_del_destino_canonico o "propio"]
HUMAN_REVIEW: [true|false]
---
</modulos_generados>

---

PASO 3 — INTELIGENCIA DE CIERRE
Genera estas 5 secciones en formato estructurado:

<inteligencia_cierre>
TOP_5_TRAFICO_MASIVO:
  [Lista con ID y razón — para priorizar en Fase 2]

TOP_5_DIAMANTES_EN_BRUTO:
  [Lista con ID y por qué son subestimados]

MODULOS_MERCADO_INTERNACIONAL:
  [Módulos más relevantes para turistas de USA, Europa, Asia]

ALERTAS_VERIFICACION_CAMPO:
  [Módulos donde el modelo tiene baja confianza — marcar con ⚠️]

MAPA_CALOR_CATEGORIAS:
  [Tabla: Categoría | Módulos | % del total | Prioridad para Fase 2]
</inteligencia_cierre>

EJECUTA LOS 3 PASOS PARA [DEPARTAMENTO], [PAÍS] AHORA.
Responde SOLO con el contenido estructurado. Sin introducción ni conclusión.
```

---

# BLOQUE 3 — PROMPT AGENTE MINERO (Fase 2)

> **USO**: Ejecutar UNA VEZ POR ENFOQUE (10 llamadas por módulo = 100 FQSAs total).
> Reemplazar `[MÓDULO]`, `[DEPARTAMENTO]`, `[PAÍS]`, y `[NÚMERO_ENFOQUE]`.
> **Output por llamada**: 10 FQSAs en JSON válido.
> **Tokens estimados por llamada**: 800-1,500 input / 1,500-2,500 output.

---

```
===============================================================
AGENTE MINERO PROFUNDO — Lifextreme v2.0
===============================================================

ROL
Eres un Analista de Inteligencia Turística y Guía Oficial Senior con
conocimiento exhaustivo del destino. Tu output es JSON válido que se
integra directamente a la base de datos de www.lifextreme.store.
Las respuestas incorrectas o genéricas dañan la reputación del producto.

CONTEXTO DE EJECUCIÓN
País: [PAÍS]
Departamento: [DEPARTAMENTO]
Módulo: [NOMBRE_COMPLETO_DEL_MÓDULO]
ID del módulo: [ID_MODULO]
Enfoque actual: [NÚMERO] de 10
Nombre del enfoque: [NOMBRE_ENFOQUE]

ENFOQUES DE EXTRACCIÓN (referencia — ejecutar de a uno):
  1. Precios, Presupuestos y Moneda
  2. Logística, Transporte y Cómo Llegar
  3. Seguridad, Riesgos y Salud
  4. Clima, Época del Año y Horarios
  5. Historia, Cultura y Curiosidades Profundas
  6. Tips Locales e Información Privilegiada
  7. Gastronomía y Supervivencia Alimentaria
  8. Accesibilidad e Infraestructura
  9. Reglas, Permisos y Trámites
  10. Alternativas, Plan B y Gestión de Imprevistos

===============================================================
INSTRUCCIONES CRÍTICAS
===============================================================

1. Genera EXACTAMENTE 10 FQSAs para el ENFOQUE [NÚMERO] únicamente.
2. Cada respuesta DEBE contener AL MENOS UNO de estos elementos:
   - Un precio con año de referencia (ej: "S/ 15-20 · ref. 2024")
   - Un nombre de empresa, terminal o servicio específico
   - Un tiempo de traslado o duración específica
   - Un mes o ventana temporal específica
   - Un riesgo nombrado con protocolo de acción
   Respuestas sin estos elementos se marcarán como inválidas en QA.
3. PRECIOS: Siempre incluir "(est. [AÑO] — verificar antes del viaje)".
4. DATOS PERSONALES: Prohibido incluir teléfonos privados, emails personales.
   Sí incluir: nombres de empresas, terminales, agencias registradas.
5. IDIOMA: Español latinoamericano neutro. Sin anglicismos innecesarios.
6. LONGITUD DE RESPUESTA: 60-120 palabras por respuesta. Ni más ni menos.
   Menos de 60 palabras = respuesta genérica. Más de 120 = divagación.

===============================================================
FORMATO DE SALIDA — JSON VÁLIDO ÚNICAMENTE
===============================================================

Devuelve ÚNICAMENTE el JSON. Sin texto previo, sin explicación, sin
markdown, sin ```json. El primer carácter debe ser { y el último }.

{
  "_meta": {
    "modulo_id": "[ID_MODULO]",
    "modulo_nombre": "[NOMBRE_MÓDULO]",
    "pais": "[PAÍS]",
    "departamento": "[DEPARTAMENTO]",
    "enfoque_numero": [NÚMERO],
    "enfoque_nombre": "[NOMBRE_ENFOQUE]",
    "generado_por": "Ayni Evolve v2.0 · Agente Minero",
    "created_at": "[ISO8601]",
    "tokens_input": 0,
    "tokens_output": 0,
    "qa_score": null,
    "status": "DRAFT"
  },
  "fqsas": [
    {
      "id": "[ID_MODULO]_[ENFOQUE]_01",
      "pregunta": "¿[Pregunta específica, como la haría un viajero real]?",
      "respuesta": "[Respuesta de 60-120 palabras con datos concretos]",
      "tags": ["[tag1]", "[tag2]"],
      "precio_referencia": "[precio si aplica, o null]",
      "año_referencia": "[año si aplica, o null]",
      "verificabilidad": "[ALTA|MEDIA|BAJA]",
      "human_review": false
    }
  ]
}

EJECUTA LA MINERÍA DEL ENFOQUE [NÚMERO] PARA [NOMBRE_MÓDULO] AHORA.
```

---

# BLOQUE 4 — PROMPT AGENTE QA (Fase 2.5)

> **USO**: Ejecutar sobre cada lote de 10 FQSAs ANTES de guardar en GCS.
> Input: el JSON generado por el Minero. Output: JSON con scores y correcciones.
> **Tokens estimados**: 1,500-2,000 input / 500-1,000 output.

---

```
===============================================================
AGENTE QA — VALIDADOR DE CALIDAD LIFEXTREME v2.0
===============================================================

ROL
Eres un Editor Senior de Inteligencia Turística. Tu función es evaluar
la calidad de las FQSAs generadas por el Agente Minero y marcar las
que requieren regeneración antes de publicarse en www.lifextreme.store.
Eres crítico y exigente. Un turista tomará decisiones reales con estos datos.

CRITERIOS DE EVALUACIÓN (score 1-5 por cada FQSA):

ESPECIFICIDAD (¿tiene datos concretos?):
  5 = precio + empresa/lugar + tiempo + mes específico
  4 = al menos 2 datos concretos
  3 = al menos 1 dato concreto
  2 = datos vagos o genéricos
  1 = podría aplicar a cualquier destino del mundo

VERIFICABILIDAD (¿se puede comprobar?):
  5 = dato de fuente oficial o conocido en campo
  4 = estimación razonable con referencia temporal
  3 = estimación sin referencia
  2 = dato no verificable
  1 = dato potencialmente incorrecto

ACCIONABILIDAD (¿el viajero puede actuar con esta info?):
  5 = instrucción clara de qué hacer, dónde, cuándo, cuánto
  4 = mayoría de pasos claros
  3 = información útil pero incompleta
  2 = información general sin instrucción
  1 = no ayuda a tomar ninguna decisión

SCORE_MÍNIMO_PARA_APROBAR: 3.0 promedio en los 3 criterios
FQSAs con score < 3.0: marcar regenerar: true con motivo específico

===============================================================
INPUT A EVALUAR
===============================================================

[PEGAR AQUÍ EL JSON COMPLETO DEL AGENTE MINERO]

===============================================================
FORMATO DE SALIDA — JSON VÁLIDO ÚNICAMENTE
===============================================================

{
  "qa_run_id": "[uuid]",
  "modulo_id": "[ID]",
  "enfoque_numero": [N],
  "score_promedio_lote": [número 1-5],
  "aprobado": [true|false],
  "fqsas_evaluadas": [
    {
      "id": "[id de la fqsa]",
      "score_especificidad": [1-5],
      "score_verificabilidad": [1-5],
      "score_accionabilidad": [1-5],
      "score_promedio": [número],
      "aprobada": [true|false],
      "regenerar": [true|false],
      "motivo_regeneracion": "[null o descripción específica]",
      "sugerencia_mejora": "[null o cómo mejorar la respuesta]"
    }
  ],
  "resumen": {
    "total_evaluadas": 10,
    "aprobadas": [N],
    "requieren_regeneracion": [N],
    "motivos_frecuentes": ["[motivo1]", "[motivo2]"]
  }
}
```

---

# BLOQUE 5 — PLANTILLAS DE NOTIFICACIONES TELEGRAM

> **USO**: El orquestador llama al Bot API con estas plantillas.
> Endpoint: `https://api.telegram.org/bot{TOKEN}/sendMessage`
> Completar los campos entre `{}`.

---

## 5.1 Inicio de Departamento

```
🚀 *PIPELINE INICIADO*

📍 *Destino:* {departamento}, {pais}
🆔 *Run ID:* `{run_id}`
⏰ *Inicio:* {timestamp}
📊 *Tier estimado:* {tier} ({modulos_estimados} módulos)

_Fase 1 — Cartógrafo en ejecución..._
```

## 5.2 Fase 1 Completada

```
✅ *FASE 1 COMPLETADA — ÍNDICE GENERADO*

📍 {departamento}, {pais}
📋 *Módulos generados:* {total_modulos}
⚠️ *Requieren revisión humana:* {modulos_human_review}
🗂 *Destinos canónicos referenciados:* {canonicos}

*Distribución por categoría:*
{tabla_categorias}

💰 *Tokens Fase 1:* {tokens_f1:,} ({costo_f1_usd} USD)
💾 *Guardado en:* `gs://lifextreme-corpus/latam/{pais}/{departamento}/fase1_indice.json`

_Iniciando Fase 2 — Minería Profunda..._
```

## 5.3 Progreso Fase 2 (cada 10 módulos)

```
⛏ *FASE 2 — PROGRESO*

📍 {departamento}, {pais}
📦 *Lote completado:* {modulos_completados}/{total_modulos} módulos
📈 *Progreso:* {porcentaje}% [{barra_progreso}]

✅ Aprobados por QA: {aprobados}
🔄 Regenerados: {regenerados}
❌ Con error: {con_error}

💰 *Tokens acumulados:* {tokens_acumulados:,} ({costo_acumulado_usd} USD)
🔥 *Uso del budget:* {porcentaje_budget}%

{alerta_budget_si_aplica}
```

## 5.4 Departamento Completado ✓

```
🏆 *DEPARTAMENTO COMPLETADO*

━━━━━━━━━━━━━━━━━━━━━━━
📍 *{DEPARTAMENTO}, {PAÍS}*
━━━━━━━━━━━━━━━━━━━━━━━

📊 *RESUMEN DE PRODUCCIÓN*
├ Módulos generados: {total_modulos}
├ FQSAs totales: {total_fqsas}
├ Aprobadas QA: {aprobadas} ({pct_aprobadas}%)
├ Requieren revisión humana: {human_review}
└ Errores no recuperados: {errores}

⏱ *TIEMPOS*
├ Duración total: {duracion_horas}h {duracion_min}m
├ Fase 1 (Cartógrafo): {tiempo_f1}m
└ Fase 2 (Minería): {tiempo_f2}m

💰 *COSTOS*
├ Tokens input: {tokens_input:,}
├ Tokens output: {tokens_output:,}
├ Tokens total: {tokens_total:,}
└ Costo estimado: {costo_total_usd} USD

💾 *ALMACENAMIENTO*
└ `gs://lifextreme-corpus/latam/{pais}/{departamento}/`

📋 *SIGUIENTE PASO DISPONIBLE:*
{siguiente_departamento}

⚠️ _Acción requerida: Responde_ *APROBAR {siguiente_departamento}* _para continuar._
```

## 5.5 Error Crítico

```
🚨 *ERROR CRÍTICO — ACCIÓN REQUERIDA*

📍 *Destino:* {departamento}, {pais}
⚠️ *Módulo afectado:* {modulo_id} — {modulo_nombre}
🔴 *Tipo de error:* {tipo_error}
📝 *Detalle:* {detalle_error}
🔁 *Intentos realizados:* {intentos}/3

*Opciones:*
  • `RETRY {modulo_id}` — Reintentar con prompt alternativo
  • `SKIP {modulo_id}` — Omitir y continuar
  • `ABORT {departamento}` — Detener el pipeline

💰 *Tokens consumidos hasta error:* {tokens:,} ({costo_usd} USD)
⏰ *Timestamp:* {timestamp}
```

## 5.6 Alerta de Budget

```
⚡ *ALERTA DE BUDGET — {porcentaje}% CONSUMIDO*

📍 {departamento}, {pais}
💰 Tokens usados: {tokens_usados:,} / {tokens_limite:,}
💵 Costo acumulado: {costo_usd} USD

📊 Módulos completados: {completados}/{total}
📈 Proyección al finalizar: {proyeccion_usd} USD

_El pipeline continúa. Recibirás confirmación final._
Si deseas detener: envía *PAUSE {run_id}*
```

## 5.7 Reporte Semanal (ejecutar cada lunes)

```
📊 *REPORTE SEMANAL — LIFEXTREME PIPELINE*
Semana: {fecha_inicio} al {fecha_fin}

🌎 *PROGRESO LATAM*
{tabla_paises_con_progreso}

✅ Departamentos completados esta semana: {completados_semana}
⛏ En progreso: {en_progreso}
⏳ Pendientes: {pendientes}

📦 *CORPUS TOTAL ACUMULADO*
├ Módulos: {total_modulos:,}
├ FQSAs: {total_fqsas:,}
└ Datos listos para publicar: {listos_publicar:,}

💰 *COSTOS SEMANA*
├ Tokens: {tokens_semana:,}
└ Costo: {costo_semana_usd} USD

💵 *COSTO ACUMULADO PROYECTO*
└ {costo_total_usd} USD / {presupuesto_total_usd} USD ({pct_budget}%)
```

---

# BLOQUE 6 — ESQUEMAS CANÓNICOS DE DATOS

## 6.1 Schema _meta.json (por departamento)

```json
{
  "_schema_version": "2.0",
  "run_id": "uuid-v4",
  "pais": "peru",
  "departamento": "arequipa",
  "tier": "A",
  "status": "IN_PROGRESS|COMPLETED|ERROR_CRITICAL|PAUSED",
  "fase1_status": "PENDING|IN_PROGRESS|COMPLETED|ERROR",
  "fase1_modulo_count": 0,
  "fase2_status": "PENDING|IN_PROGRESS|COMPLETED|ERROR",
  "fase2_modulos_completados": 0,
  "fase2_fqsas_generadas": 0,
  "fase2_fqsas_aprobadas_qa": 0,
  "modulos_human_review_pendientes": 0,
  "modulos_con_error": 0,
  "tokens_fase1_input": 0,
  "tokens_fase1_output": 0,
  "tokens_fase2_input": 0,
  "tokens_fase2_output": 0,
  "tokens_total": 0,
  "costo_estimado_usd": 0.0,
  "created_at": "2026-01-01T00:00:00Z",
  "fase1_completed_at": null,
  "fase2_completed_at": null,
  "last_updated": "2026-01-01T00:00:00Z",
  "siguiente_departamento": "cusco",
  "notas": []
}
```

## 6.2 Schema de Módulo Completo (100 FQSAs ensambladas)

```json
{
  "_meta": {
    "modulo_id": "A-01",
    "modulo_nombre": "Mirador del Volcán Misti — Acceso y Ascenso",
    "pais": "peru",
    "departamento": "arequipa",
    "segmento_principal": "Aventura",
    "segmento_secundario": "Digital_Nomad",
    "tipo_de_dato": "Logístico",
    "verificabilidad_general": "ALTA",
    "canonical_ref": "propio",
    "human_review": false,
    "generado_por": "Ayni Evolve v2.0",
    "pipeline_run_id": "uuid",
    "version": "1.0",
    "created_at": "ISO8601",
    "last_updated": "ISO8601",
    "tokens_total": 0,
    "qa_score_promedio": 0.0,
    "status": "DRAFT|VALIDATED|PUBLISHED",
    "publicado_en": null
  },
  "fqsas": {
    "1_Precios_y_Presupuestos": [],
    "2_Logistica_y_Transporte": [],
    "3_Seguridad_y_Riesgos": [],
    "4_Clima_y_Epocas": [],
    "5_Historia_y_Cultura": [],
    "6_Tips_Locales": [],
    "7_Gastronomia": [],
    "8_Accesibilidad": [],
    "9_Reglas_y_Permisos": [],
    "10_Alternativas_y_Plan_B": []
  }
}
```

## 6.3 Schema master_index.json

```json
{
  "_schema_version": "2.0",
  "last_updated": "ISO8601",
  "totales": {
    "departamentos_completados": 0,
    "departamentos_en_progreso": 0,
    "departamentos_pendientes": 0,
    "modulos_totales": 0,
    "fqsas_totales": 0,
    "tokens_consumidos_total": 0,
    "costo_total_usd": 0.0
  },
  "paises": {
    "peru": {
      "status": "IN_PROGRESS",
      "departamentos": {
        "arequipa": {
          "status": "COMPLETED",
          "modulos": 87,
          "fqsas": 8700,
          "completado": "2026-01-15"
        }
      }
    }
  }
}
```

---

# APÉNDICE A — GUÍA DE DESTINOS CANÓNICOS LATAM

Los siguientes destinos aparecen en múltiples departamentos o países.
Deben ser tratados como módulos canónicos y referenciados, no duplicados:

**Perú:**
- Lago Titicaca → canonical: lago_titicaca (Puno + Bolivia)
- Amazonía peruana → canonical: amazonia_peru (Loreto + MDD + Ucayali)
- Camino Inca → canonical: camino_inca (Cusco — módulo único)
- Cordillera Blanca → canonical: cordillera_blanca (Áncash)

**LATAM:**
- Patagonia → canonical: patagonia (Argentina + Chile)
- Amazonía → canonical: amazonia_latam (Brasil + Perú + Colombia + Bolivia + Ecuador)
- Atacama → canonical: atacama (Chile + Perú + Bolivia)
- Pantanal → canonical: pantanal (Brasil + Bolivia + Paraguay)

---

# APÉNDICE B — CONFIGURACIÓN DEL RATE LIMITER (código Python de referencia)

```python
import asyncio
import random
import time
from dataclasses import dataclass

@dataclass
class PipelineConfig:
    jitter_min_seconds: float = 1.0    # Pausa mínima entre llamadas API
    jitter_max_seconds: float = 3.0    # Pausa máxima entre llamadas API
    max_retries: int = 3
    retry_delays: list = (5, 15, 30)   # Segundos entre reintentos
    batch_size: int = 10               # FQSAs por llamada (NO modificar)
    max_tokens_per_dept: int = 150_000
    budget_alert_threshold: float = 0.8

async def rate_limited_call(func, config: PipelineConfig, *args, **kwargs):
    """
    Wrapper para todas las llamadas API.
    El jitter va AQUÍ, en el código — nunca en el prompt.
    """
    for attempt in range(config.max_retries):
        try:
            # Jitter antes de cada llamada
            jitter = random.uniform(config.jitter_min_seconds, config.jitter_max_seconds)
            await asyncio.sleep(jitter)
            
            result = await func(*args, **kwargs)
            return result
            
        except TruncationError as e:
            # Error de truncamiento: dividir la tarea
            raise SplitTaskError(f"Truncamiento detectado en intento {attempt + 1}")
            
        except APIError as e:
            if attempt < config.max_retries - 1:
                delay = config.retry_delays[attempt]
                await asyncio.sleep(delay)
            else:
                raise CriticalError(f"Falló después de {config.max_retries} intentos: {e}")
```

---

# APÉNDICE C — CHECKLIST DE DESPLIEGUE

Antes de ejecutar el pipeline en producción, verificar:

```
PRE-VUELO:
[ ] Bot de Telegram configurado y probado (enviar mensaje de prueba)
[ ] GCS bucket creado con estructura de carpetas
[ ] Variables de entorno configuradas en Vertex AI
[ ] Umbral de tokens configurado en Google Cloud Billing
[ ] master_index.json inicializado en GCS
[ ] Error_log.jsonl inicializado en GCS
[ ] Primer departamento a ejecutar confirmado con el equipo

POST-PRIMER DEPARTAMENTO:
[ ] Revisar _meta.json del departamento completado
[ ] Revisar al menos 10 FQSAs al azar para control de calidad
[ ] Confirmar que las notificaciones Telegram funcionaron correctamente
[ ] Revisar el costo real vs estimado (ajustar MAX_TOKENS si hay desviación >20%)
[ ] Dar APROBAR para continuar con el siguiente departamento
```

---

*DMO-v2.0 · Lifextreme Turismo Global · www.lifextreme.store*
*Generado por Ayni Evolve v2.0 · Pipeline LATAM Supervisado*
*Este documento es confidencial y de uso interno del equipo Lifextreme.*
