# EXPEDIENTE TÉCNICO DE GOBERNANZA DE INTELIGENCIA ARTIFICIAL, PROTECCIÓN DE DATOS E INTEGRIDAD DIGITAL
## INSTITUTO DE EDUCACIÓN SUPERIOR TECNOLÓGICO PRIVADO (IESTP) "URUSAYHUA" — LICENCIADO POR MINEDU

**Código de Expediente:** `DIR-AG-QDRANT-2026-URU-001`  
**Entidad Auditada:** Instituto de Educación Superior Tecnológico Privado (IESTP) Urusayhua (`https://urusayhua.edu.pe/`)  
**Sede Principal:** Jr. Quillabamba N° 110, Distrito de Santa Ana, Provincia de La Convención, Región Cusco  
**Condición Regulatoria:** Primer Instituto Licenciado por el MINEDU en la Provincia de La Convención y Entidad Elegible PRONABEC (Beca 18)  
**Marco Legal Rector:** Ley N° 31814 | D.S. N° 115-2025-PCM | Ley N° 29733 y D.S. N° 016-2024-JUS (ANPD) | Ley N° 30512 (MINEDU) | Estándares ISO/IEC 42001:2023, ISO/IEC 42005 y OWASP GenAI Top 10 (2026)  
**Fecha de Emisión:** Noviembre 2026  

---

### EQUIPO CONSULTOR MULTIDISCIPLINARIO ACREDITADO (FIRMAS RESPONSABLES)

| Rol en el Comité Consultor | Especialidad y Grado Académico | Competencia Normativa y Técnica Asignada |
| :--- | :--- | :--- |
| **Director de Arquitectura IA & Ciberseguridad** | **Ing. Engelberth Egoavil** — Arquitecto Senior de Sistemas IA & RAG | Cumplimiento Técnico Art. 31.1 D.S. N° 115-2025-PCM, ISO/IEC 42001, Auditoría Algorítmica de *"Otito Beca 18"* y Controles OWASP Agentic Top 10 (2026). |
| **Directora de Gestión Pedagógica & Licenciamiento** | **Magíster en Educación & Directora Educativa (Cusco)** | Adecuación del Reglamento Institucional (RI), Proyecto Educativo Institucional (PEI), Semáforo de Integridad Académica y Condiciones Básicas de Calidad (CBC - MINEDU / DRE Cusco). |
| **Directora de Impacto Cognitivo & Ética Psicométrica** | **Magíster en Psicología** | Evaluación de Impacto Algorítmico en Salud Mental y Desarrollo Cognitivo Estudiantil (ISO/IEC 42005), Protocolos para Postulantes Menores de Edad (16-17 años) y Prevención de Sesgos Psicométricos. |
| **Director de Equidad Intercultural & Enfoque Territorial** | **Magíster en Antropología** | Auditoría de No Discriminación Algorítmica, Pertinencia Cultural y Lingüística (Quechua / Matsigenka / Ámbito Amazónico-Andino de La Convención) conforme al Principio de Equidad de la Ley N° 31814 y PRONABEC Beca 18. |

<div class="page-break" style="page-break-after: always;"></div>

## MÓDULO 1: DIAGNÓSTICO DE URGENCIA LEGAL Y MAPEO DE BRECHAS (ANPD / PCM / MINEDU / INDECOPI)

### 1.1 Perfilamiento Técnico-Institucional (`Agente_1_Profiler`)
El **IESTP Urusayhua** opera como la institución líder de educación superior tecnológica licenciada por el MINEDU en la provincia de La Convención (Cusco), ofertando cinco (05) programas de estudios en modalidades **presencial, semipresencial y virtual/a distancia**:
1. **Arquitectura de Plataformas y Servicios de TI** (desarrollo web, infraestructura cloud, soporte e IA aplicada).
2. **Enfermería Técnica** (tratamiento de datos clínicos, prácticas de salud y simulación).
3. **Contabilidad** (sistemas tributarios, financieros y automatización contable).
4. **Gestión Administrativa** (ERP, ofimática avanzada y procesos empresariales).
5. **Producción Agropecuaria** (sanidad agraria, agroexportación e innovación rural en ceja de selva).

Adicionalmente, el instituto despliega en su ecosistema digital (`https://urusayhua.edu.pe/`) un activo crítico diferenciador: el **Simulador y Programa de Acompañamiento "Otito Beca 18"**, orientado a captar, perfilar y preparar postulantes a **Beca 18 de PRONABEC**.

### 1.2 Matriz de Brechas Normativas Detectadas y Riesgo Sancionador (2026)

| Eje Regulatorio | Norma Peruana Exigible | Hallazgo en `urusayhua.edu.pe` | Nivel de Riesgo | Sanción / Contingencia Legal |
| :--- | :--- | :--- | :---: | :--- |
| **1. Protección de Datos de Postulantes y Menores ("Otito Beca 18")** | **Ley N° 29733 y Nuevo Reglamento D.S. N° 016-2024-JUS (ANPD)** | Captación de datos personales, socioeconómicos (SISFOH) y académicos de escolares de 5to de secundaria (menores de 16-17 años) y jóvenes de comunidades rurales sin protocolo verificable de **Consentimiento Parental Expreso** ni cláusula de flujo transfronterizo (servidores cloud/IA). | **CRÍTICO (ROJO)** | Multas de la **ANPD (Ministerio de Justicia)** desde **5 UIT hasta 100 UIT** (S/ 26,750 a S/ 535,000) por tratamiento de datos de menores y datos sensibles sin consentimiento válido. |
| **2. Gobernanza y Registro de Sistemas de IA** | **Ley N° 31814 y Reglamento D.S. N° 115-2025-PCM (Art. 31.1)** | Ausencia de un **Registro Técnico Vivo de Sistemas de IA** para el simulador *"Otito Beca 18"*, el Aula Virtual (modalidad a distancia), chatbots de admisión (`+51 956 899 969`) y herramientas generativas usadas en las 5 carreras. | **ALTO (ROJO)** | Observación regulatoria en supervisión de **Condiciones Básicas de Calidad (MINEDU / DRE Cusco)** y pérdida de elegibilidad en convenios estatales. |
| **3. Datos Sensibles de Salud y Equidad Intercultural** | **D.S. N° 115-2025-PCM (Sistemas de Riesgo Alto en Educación y Salud)** | En la carrera de **Enfermería Técnica** y en el perfilamiento de becarios **PRONABEC** de poblaciones quechua y amazónicas (Matsigenka) de La Convención, no existe una Evaluación de Impacto Algorítmico ni protocolo contra sesgos lingüísticos/culturales. | **ALTO (ÁMBAR)** | Infracción al Principio de No Discriminación (Ley N° 31814) y contingencias ante **INDECOPI** por idoneidad del servicio educativo (Código de Protección al Consumidor Ley N° 29571). |
| **4. Designación de Oficial de Datos Personales (ODP) y Comité IA** | **D.S. N° 016-2024-JUS (Vigencia escalonada 2025-2026)** | No figura publicado en el portal web institucional el acto de designación ni el canal de contacto del **Oficial de Datos Personales (ODP)** ni la inscripción actualizada de Bancos de Datos en el **RNPDP**. | **CRÍTICO (ROJO)** | Infracción grave tipificada por la Autoridad Nacional de Protección de Datos Personales (ANPD). |

<div class="page-break" style="page-break-after: always;"></div>

## MÓDULO 2: REGISTRO TÉCNICO VIVO DE SISTEMAS DE IA (ART. 31.1 D.S. N° 115-2025-PCM)

Conforme al **Artículo 31.1 del Reglamento de la Ley N° 31814 (D.S. N° 115-2025-PCM)** y la cláusula 6.1 de la norma **ISO/IEC 42001:2023**, se estructura el inventario inicial de activos algorítmicos y digitales del **IESTP Urusayhua** sujetos a supervisión humana:

| ID Activo | Nombre del Sistema / Proceso | Programa / Área Usuaria | Clasificación de Riesgo (D.S. 115-2025-PCM) | Datos Tratados | Medida de Control Obligatoria (Human-in-the-Loop) |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **IA-URU-01** | **Simulador y Perfilador "Otito Beca 18"** | Admisión / Bienestar y PRONABEC | **Riesgo Alto** (Evaluación de acceso a educación y becas) | Datos de postulantes (incluye menores de 16-17 años), puntajes simulados, condición socioeconómica y procedencia rural/indígena. | Validación psicopedagógica y antropológica del algoritmo de puntaje; prohibición de exclusión automatizada sin revisión humana; consentimiento parental digital previo. |
| **IA-URU-02** | **Aula Virtual / LMS (Modalidad Semipresencial y a Distancia)** | Los 5 Programas de Estudio | **Riesgo Alto** (Seguimiento académico y evaluación) | Historial de calificaciones, analítica de aprendizaje, entregas de proyectos y asistencia virtual. | Transparencia de rúbricas asistidas por IA; derecho de impugnación estudiantil ante evaluaciones automatizadas. |
| **IA-URU-03** | **Asistente de Captación y Atención WhatsApp / Web** | Marketing y Admisión (`informes@urusayhua.edu.pe`) | **Riesgo Limitado** (Obligación de Transparencia) | Nombres, teléfonos, colegio de procedencia e intereses vocacionales. | Aviso explícito de interacción con IA; cláusula informativa Art. 18 Ley N° 29733 al primer mensaje. |
| **IA-URU-04** | **Laboratorios de IA Generativa y Desarrollo de Software** | Carrera de **Arquitectura de Plataformas y Servicios de TI** | **Riesgo Moderado** | Código fuente, bases de datos de prueba y prompts de estudiantes/docentes. | Prohibición de inyectar datos reales de alumnos o pacientes en LLMs públicos; entorno aislado (Sandbox). |
| **IA-URU-05** | **Asistentes de Triaje/Casos Clínicos y Gestión Agraria** | Carreras de **Enfermería Técnica** y **Producción Agropecuaria** | **Riesgo Alto / Moderado** | Casos clínicos pedagógicos, fichas sanitarias y diagnósticos fitosanitarios del valle de La Convención. | Anonimización absoluta de historias clínicas (D.S. 016-2024-JUS) y validación docente obligatoria. |

<div class="page-break" style="page-break-after: always;"></div>

## MÓDULO 3: POLÍTICA INSTITUCIONAL Y SEMÁFORO ACADÉMICO / OPERATIVO POR CARRERA

Para blindar el licenciamiento MINEDU del **IESTP Urusayhua** e incorporar la Gobernanza de IA en su **Reglamento Institucional (RI)**, se establece el **Semáforo de Integridad Académica y Operativa**:

### 🟢 NIVEL VERDE (Usos Permitidos y Fomentados con Cita Metodológica)
* **Arquitectura de Plataformas y Servicios de TI:** Generación asistida de código boilerplate, refactorización, pruebas unitarias y diseño de arquitecturas en la nube, documentando el prompt utilizado.
* **Producción Agropecuaria:** Uso de modelos predictivos climáticos y de plagas en cultivos tropicales de La Convención (café, cacao, frutales) como insumo de apoyo técnico.
* **Contabilidad y Gestión Administrativa:** Automatización de conciliaciones sobre datos sintéticos y simulación de planes de negocio regionales.
* **Docencia Transversal:** Diseño de sílabos adaptativos y materiales bilingües/interculturales revisados por el docente titular.

### 🟡 NIVEL ÁMBAR (Usos Supervisados que Requieren Validación Humana y Registro)
* **Simulador "Otito Beca 18":** Generación de retroalimentación vocacional y simulacros de examen PRONABEC, bajo supervisión del área psicopedagógica para evitar sesgos contra estudiantes cuya lengua materna sea el quechua o matsigenka.
* **Enfermería Técnica:** Uso de IA para consulta bibliográfica de protocolos de atención primaria, exigiendo contraste obligatorio con las Guías Técnicas del MINSA.
* **Trabajos de Aplicación Profesional (Titulación):** Uso de IA para corrección de estilo o estructuración metodológica, con declaración jurada de autoría original anexada al expediente de titulación.

### 🔴 NIVEL ROJO (Usos Estrictamente Prohibidos — Falta Grave en el Reglamento Institucional)
* **Ingesta de Datos Personales o Clínicos en IA Pública:** Subir padrones de postulantes de *"Otito Beca 18"*, DNI, notas reales, fichas socioeconómicas o datos de pacientes de prácticas de Enfermería Técnica a cuentas gratuitas de ChatGPT, Claude, Gemini o DeepSeek.
* **Sustitución de Evaluación Docente:** Calificar exámenes finales o proyectos de titulación de forma 100% automatizada sin revisión humana documentada.
* **Suplantación Académica:** Presentar código, informes contables o proyectos productivos generados íntegramente por IA sin comprensión ni defensa oral verificable por el jurado.

<div class="page-break" style="page-break-after: always;"></div>

## MÓDULO 4: EVALUACIÓN DE IMPACTO ALGORÍTMICO MULTIDISCIPLINARIA (ISO/IEC 42005) Y CIBERSEGURIDAD AGÉNTICA (OWASP 2026)

A diferencia de una auditoría meramente informática, este Expediente cumple con el estándar internacional **ISO/IEC 42005 (AI System Impact Assessment)** y el **D.S. N° 115-2025-PCM** mediante **cuatro (04) dimensiones periciales obligatorias**:

### 4.1 Dimensión Psicológica y Cognitiva (Dirigida por Magíster en Psicología)
1. **Protocolo de Protección del Postulante Menor de Edad (16-17 años en "Otito Beca 18"):**
   * Evaluación del impacto emocional y de ansiedad ante resultados automatizados de simulacros de beca.
   * Diseño de mensajes de retroalimentación algorítmica con enfoque formativo y no punitivo.
2. **Prevención de Dependencia Cognitiva Estudiantil:**
   * Instrumento psicométrico de línea base para medir pensamiento crítico y autonomía en estudiantes de modalidades semipresencial y virtual.

### 4.2 Dimensión Antropológica e Intercultural (Dirigida por Magíster en Antropología)
1. **Auditoría de Sesgo Cultural y Lingüístico en La Convención (Cusco):**
   * Los modelos de lenguaje (LLMs) comerciales presentan sesgos estructurales frente a variantes dialectales andinas (Quechua) y amazónicas (Matsigenka / Asháninka) presentes en los distritos de Echarati, Megantoni, Pichari, Kimbiri y Santa Ana.
   * **Mitigación:** Calibración intercultural del simulador *"Otito Beca 18"* y de los instrumentos de evaluación del aula virtual para garantizar que ningún estudiante rural o indígena sea penalizado por constructos lingüísticos o culturales ajenos a su entorno territorial (cumplimiento estricto del **Art. 4 de la Ley N° 31814**).

### 4.3 Dimensión Pedagógica y Regulatoria MINEDU (Dirigida por Magíster en Educación / Directora Educativa)
1. **Alineamiento con Condiciones Básicas de Calidad (CBC - Ley N° 30512):**
   * Inserción formal de la Política de Gobernanza de IA en el Reglamento Institucional (RI) y en los sílabos de los 5 programas de estudio, lista para cualquier fiscalización de **MINEDU / DRE Cusco / PRONABEC**.

### 4.4 Dimensión de Arquitectura IA y Ciberseguridad (Dirigida por Ing. Engelberth Egoavil)
1. **Blindaje OWASP Top 10 for LLM & Agentic Applications (2026):**
   * **LLM01 (Prompt Injection):** Filtros de entrada en el simulador *"Otito Beca 18"* y chatbots para impedir manipulación de resultados o extracción de respuestas.
   * **LLM02 (Sensitive Information Disclosure):** Despliegue de pasarela de anonimización de PII (DNI, teléfonos, notas) antes de cualquier llamada a APIs de IA.
   * **Inscripción Formal ante la ANPD (Ministerio de Justicia):** Registro de los Bancos de Datos y comunicación de Flujo Transfronterizo conforme al **D.S. N° 016-2024-JUS**.

<div class="page-break" style="page-break-after: always;"></div>

## MÓDULO 5: PLAN DE IMPLEMENTACIÓN EN 5 SEMANAS Y PROPUESTA ECONÓMICA (TDR EN SOLES)

### 5.1 Cronograma de Ejecución (Sprint de 5 Semanas — Entregables Verificables ante MINEDU y ANPD)

| Semana | Fase del Proyecto | Entregables Oficiales Firmados por el Comité de 4 Especialistas |
| :---: | :--- | :--- |
| **Semana 1** | **Auditoría Legal, Tecnológica y RNPDP (ANPD)** | • Informe de Brechas D.S. N° 016-2024-JUS y D.S. N° 115-2025-PCM.<br>• Expediente listo para inscripción/actualización de Bancos de Datos y designación del Oficial de Datos Personales (ODP) ante el Ministerio de Justicia. |
| **Semana 2** | **Registro Técnico Art. 31.1 y Blindaje "Otito Beca 18"** | • **Registro Técnico Vivo de Sistemas de IA** del IESTP Urusayhua.<br>• Formato legal de Consentimiento Parental Digital para menores postulantes a Beca 18 y cláusulas de privacidad web (`urusayhua.edu.pe`). |
| **Semana 3** | **Evaluación de Impacto Psicológico y Antropológico (ISO 42005)** | • **Informe Pericial Psicológico** (impacto cognitivo y protección de menores).<br>• **Informe Pericial Antropológico-Intercultural** (equidad lingüística y territorial en La Convención para postulantes PRONABEC). |
| **Semana 4** | **Reforma Pedagógica y Reglamento Institucional (MINEDU)** | • Resolución Directoral de aprobación del **Reglamento de Uso Ético de IA y Semáforo Académico** para las 5 carreras.<br>• Guías docentes para Arquitectura de TI, Enfermería, Contabilidad, Administración y Agropecuaria. |
| **Semana 5** | **Capacitación Directiva, Simulacro de Fiscalización y Certificación** | • Taller Ejecutivo para Dirección General, Jefes de Área Académica y Docentes.<br>• Entrega del **Dossier Maestro Impreso y Digital** blindado ante auditorías de **MINEDU, PRONABEC, ANPD e INDECOPI**. |

---

### 5.2 Propuesta Económica Escalonada (Expresada en Soles — S/)

| Modalidad de Contratación | Alcance para el IESTP Urusayhua | Plazo | Inversión Total (S/) |
| :--- | :--- | :---: | :---: |
| **PACK 1: ADECUACIÓN URGENTE & BLINDAJE LEGAL ANPD / MINEDU** | • Diagnóstico de Brechas + Adecuación Web `urusayhua.edu.pe` (Política de Privacidad, Consentimiento Parental *"Otito Beca 18"*).<br>• Registro Técnico de Sistemas de IA (Art. 31.1 D.S. 115-2025-PCM).<br>• Reglamento de IA y Semáforo Académico para el RI. | **2 a 3 Semanas** | **S/ 6,500.00** |
| **PACK 2: GOBERNANZA INTEGRAL 360° + PERITAJE MULTIDISCIPLINARIO (RECOMENDADO)** | • **Todo el Pack 1**, más:<br>• **Peritaje Psicológico (ISO 42005)** + **Peritaje Antropológico Intercultural (Beca 18 / La Convención)** + **Adecuación Curricular Pedagógica en las 5 Carreras**.<br>• Expediente de Inscripción de Bancos de Datos ante la ANPD + Capacitación Docente Certificada. | **5 Semanas** | **S/ 12,800.00** |
| **PACK 3: ACOMPAÑAMIENTO ANUAL (OFICIALÍA EXTERNA ODP / OIA AS A SERVICE)** | • Soporte continuo ante fiscalizaciones de MINEDU, PRONABEC, ANPD e INDECOPI.<br>• Actualización semestral del Registro Técnico Art. 31.1 y auditoría del Aula Virtual. | **Mensual (Opcional)** | **S/ 1,200.00 / mes** |

---

**Firmado en Cusco, noviembre de 2026:**

* **Ing. Engelberth Egoavil** — *Director de Arquitectura de IA, RAG & Ciberseguridad Agéntica*
* **Mg. en Psicología** — *Especialista en Evaluación de Impacto Cognitivo y Protección de Menores (ISO 42005)*
* **Mg. en Educación (Directora Educativa - Cusco)** — *Especialista en Gestión Pedagógica y Normativa MINEDU*
* **Mg. en Antropología** — *Especialista en Equidad Intercultural, Pueblos Originarios y Enfoque Territorial*
