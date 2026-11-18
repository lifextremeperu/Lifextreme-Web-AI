import os
from fpdf import FPDF

class LifextremePDF(FPDF):
    def header(self):
        # Andean Twilight Obsidian Header (#090d16)
        self.set_fill_color(9, 13, 22)
        self.rect(0, 0, 210, 20, 'F')
        
        # Brand Magma / Indigo Top Accent Strip (#4338ca -> #f43f5e -> #f59e0b)
        self.set_fill_color(67, 56, 202) # Indigo
        self.rect(0, 0, 70, 2, 'F')
        self.set_fill_color(244, 63, 94) # Sunset Flame
        self.rect(70, 0, 70, 2, 'F')
        self.set_fill_color(245, 158, 11) # Sunrise Amber
        self.rect(140, 0, 70, 2, 'F')

        # Logo if exists
        logo_path = "assets/images/lifextreme_logo_icon.png"
        if os.path.exists(logo_path):
            self.image(logo_path, 12, 4, 12)
            text_x = 27
        else:
            text_x = 12

        self.set_xy(text_x, 5)
        self.set_font('Arial', 'B', 9.5)
        self.set_text_color(248, 250, 252) # #f8fafc
        self.cell(90, 5, 'LIFEXTREME AI  |  PUBLIC GOODS GRANT PROPOSAL', 0, 0, 'L')
        
        self.set_xy(text_x, 10)
        self.set_font('Arial', '', 7.5)
        self.set_text_color(6, 182, 212) # Glacier Cyan #06b6d4
        self.cell(90, 5, 'Soberania Tecnologica · Edge AI · GEOINT 3D · DAO Andina', 0, 0, 'L')

        self.set_xy(130, 7.5)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(245, 158, 11) # Amber #f59e0b
        self.cell(68, 5, 'Cusco, Peru  |  Meta: $48,500 USD', 0, 0, 'R')
        
        self.set_y(24)

    def footer(self):
        self.set_y(-15)
        # Subtle Slate Line
        self.set_draw_color(226, 232, 240) # #e2e8f0
        self.line(12, 282, 198, 282)
        
        self.set_font('Arial', '', 7.5)
        self.set_text_color(100, 116, 139) # Slate 500
        self.set_xy(12, -12)
        self.cell(140, 6, 'Lifextreme Open Source Initiative  |  Web: lifextreme.com.pe  |  Email: contacto@lifextreme.com.pe  |  Tel: +51 958 050 928', 0, 0, 'L')
        
        self.set_font('Arial', 'B', 7.5)
        self.set_text_color(67, 56, 202) # Indigo #4338ca
        self.set_xy(160, -12)
        self.cell(38, 6, f'Pagina {self.page_no()}', 0, 0, 'R')

    def clean(self, text):
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'ñ': 'n', 'Ñ': 'N', '·': '-', '—': '-', '–': '-'
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text.encode('latin-1', 'replace').decode('latin-1')

    def section_header(self, title, accent_rgb=(67, 56, 202)):
        if self.get_y() > 255:
            self.add_page()
        self.ln(3)
        y = self.get_y()
        # Soft background card header (#f1f5f9)
        self.set_fill_color(241, 245, 249)
        self.rect(12, y, 186, 8.5, 'F')
        # Left accent bar
        self.set_fill_color(*accent_rgb)
        self.rect(12, y, 2.5, 8.5, 'F')
        
        self.set_xy(17, y + 1.5)
        self.set_font('Arial', 'B', 11)
        self.set_text_color(15, 23, 42) # #0f172a
        self.cell(180, 5.5, self.clean(title), 0, 1, 'L')
        self.ln(3)

    def sub_header(self, title):
        if self.get_y() > 265:
            self.add_page()
        self.set_font('Arial', 'B', 9.5)
        self.set_text_color(67, 56, 202) # Primary Indigo #4338ca
        self.cell(0, 6, self.clean(title), 0, 1, 'L')
        self.ln(0.5)

    def body_text(self, text):
        self.set_font('Arial', '', 9)
        self.set_text_color(30, 41, 59) # Slate 800
        self.multi_cell(0, 4.8, self.clean(text))
        self.ln(1.8)

    def bullet_item(self, title, desc):
        if self.get_y() > 268:
            self.add_page()
        self.set_x(15)
        # Bullet dot in Glacier Cyan
        self.set_font('Arial', 'B', 9)
        self.set_text_color(6, 182, 212)
        self.write(4.6, "- ")
        
        self.set_text_color(15, 23, 42)
        self.write(4.6, self.clean(f"{title}: "))
        
        self.set_font('Arial', '', 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.6, self.clean(desc))
        self.ln(1)

    def draw_kv_table(self, rows, col1_w=55, col2_w=131, header1="Atributo", header2="Especificacion"):
        if self.get_y() > 240:
            self.add_page()
        # Table Header in Andean Obsidian (#0f172a)
        self.set_fill_color(15, 23, 42)
        self.set_text_color(248, 250, 252)
        self.set_font('Arial', 'B', 8.5)
        self.cell(col1_w, 7, self.clean(f"  {header1}"), 0, 0, 'L', fill=True)
        self.cell(col2_w, 7, self.clean(f"  {header2}"), 0, 1, 'L', fill=True)

        for idx, (k, v) in enumerate(rows):
            fill = (idx % 2 == 0)
            self.set_fill_color(248, 250, 252) if fill else self.set_fill_color(255, 255, 255)
            self.set_draw_color(226, 232, 240)
            
            # Measure height needed
            self.set_font('Arial', '', 8.5)
            lines = self.multi_cell(col2_w - 4, 4.5, self.clean(v), split_only=True)
            row_h = max(6.5, len(lines) * 4.5 + 2)
            
            if self.get_y() + row_h > 275:
                self.add_page()
                
            y_start = self.get_y()
            self.rect(12, y_start, col1_w + col2_w, row_h, 'F')
            self.line(12, y_start + row_h, 12 + col1_w + col2_w, y_start + row_h)

            self.set_xy(14, y_start + 1.2)
            self.set_font('Arial', 'B', 8.5)
            self.set_text_color(15, 23, 42)
            self.multi_cell(col1_w - 4, 4.5, self.clean(k))

            self.set_xy(12 + col1_w + 2, y_start + 1.2)
            self.set_font('Arial', '', 8.5)
            self.set_text_color(51, 65, 85)
            self.multi_cell(col2_w - 4, 4.5, self.clean(v))

            self.set_y(y_start + row_h)
        self.ln(3)

    def draw_budget_table(self, rows):
        if self.get_y() > 235:
            self.add_page()
        widths = [38, 92, 30, 26]
        headers = ["Categoria", "Descripcion Tecnica", "Costo (USD)", "Hito"]
        
        self.set_fill_color(15, 23, 42)
        self.set_text_color(248, 250, 252)
        self.set_font('Arial', 'B', 8.5)
        for w, h in zip(widths, headers):
            self.cell(w, 7, f"  {h}", 0, 0, 'L', fill=True)
        self.ln()

        for idx, (cat, desc, cost, hito) in enumerate(rows):
            is_total = (cat == "Total Solicitado")
            if is_total:
                self.set_fill_color(238, 242, 255) # Light Indigo tint
            elif idx % 2 == 0:
                self.set_fill_color(248, 250, 252)
            else:
                self.set_fill_color(255, 255, 255)

            self.set_font('Arial', '', 8.2)
            lines = self.multi_cell(widths[1] - 3, 4.3, self.clean(desc), split_only=True)
            row_h = max(6.5, len(lines) * 4.3 + 2.5)

            if self.get_y() + row_h > 275:
                self.add_page()

            y_start = self.get_y()
            self.rect(12, y_start, sum(widths), row_h, 'F')
            self.set_draw_color(226, 232, 240)
            self.line(12, y_start + row_h, 12 + sum(widths), y_start + row_h)

            # Col 1
            self.set_xy(13.5, y_start + 1.3)
            self.set_font('Arial', 'B', 8.2)
            self.set_text_color(67, 56, 202) if is_total else self.set_text_color(15, 23, 42)
            self.multi_cell(widths[0] - 2, 4.3, self.clean(cat))

            # Col 2
            self.set_xy(12 + widths[0] + 1.5, y_start + 1.3)
            self.set_font('Arial', 'B' if is_total else '', 8.2)
            self.set_text_color(51, 65, 85)
            self.multi_cell(widths[1] - 3, 4.3, self.clean(desc))

            # Col 3
            self.set_xy(12 + widths[0] + widths[1] + 1.5, y_start + 1.3)
            self.set_font('Arial', 'B', 8.5)
            self.set_text_color(16, 185, 129) if is_total else self.set_text_color(15, 23, 42) # Emerald for total
            self.cell(widths[2] - 2, 4.3, self.clean(cost), 0, 0, 'L')

            # Col 4
            self.set_xy(12 + widths[0] + widths[1] + widths[2] + 1.5, y_start + 1.3)
            self.set_font('Arial', 'B' if is_total else '', 8.2)
            self.set_text_color(51, 65, 85)
            self.cell(widths[3] - 2, 4.3, self.clean(hito), 0, 0, 'L')

            self.set_y(y_start + row_h)
        self.ln(3)


def generate_full_pdf():
    pdf = LifextremePDF('P', 'mm', 'A4')
    pdf.set_margins(12, 24, 12)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # Hero Title Banner (#090d16)
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(12, 24, 186, 30, 'F')
    # Magma left accent
    pdf.set_fill_color(244, 63, 94) # #f43f5e
    pdf.rect(12, 24, 3, 30, 'F')

    pdf.set_xy(18, 27)
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(248, 250, 252)
    pdf.multi_cell(176, 6, pdf.clean("Infraestructura Soberana de Edge AI, RAG Normativo y Geointeligencia Territorial hacia una DAO Andina"))

    pdf.set_xy(18, 42)
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(6, 182, 212) # Cyan
    pdf.cell(176, 5, pdf.clean("Public Goods Grant Proposal  |  Gitcoin Grants / Arbitrum DAO / Lisk Grants  |  Cusco, Peru"), 0, 1, 'L')

    pdf.set_y(58)

    # Tabla de Atributos Tecnicos
    meta_rows = [
        ("Proyecto", "Lifextreme (Open Source Adventure Intelligence & Geospatial Commons)"),
        ("Jurisdiccion Territorial", "Cusco, Region Andina del Peru (Escalabilidad LATAM)"),
        ("Naturaleza del Protocolo", "Infraestructura Abierta de Geointeligencia, RAG Juridico-Territorial y Gobernanza Descentralizada (NO SaaS B2B tradicional)"),
        ("Objetivo del Grant", "Soberania Tecnologica y de Datos mediante despliegue de Cluster Edge AI / Memoria Unificada en Cusco para inferencia local de costo marginal cero"),
        ("Monto Solicitado / Meta", "$48,500 USD (DAI / USDC / ARB) estructurado en 3 hitos auditables"),
        ("Componentes Core", "FastAPI · Pydantic-AI · Model Context Protocol (MCP) · Qdrant (>336K vectores) · nomic-embed-text · WebGL / Three.js / CesiumJS · Ollama (qwen2.5:7b / Llama 3)"),
        ("Repositorio Oficial", "github.com/lifextreme / gitcoinco/gitcoin_co_30")
    ]
    pdf.draw_kv_table(meta_rows, header1="Atributo Tecnico", header2="Especificacion")

    # Resumen Ejecutivo
    pdf.section_header("Resumen Ejecutivo (Tesis de Soberania Tecnologica y Bienes Publicos)", (245, 158, 11)) # Amber
    pdf.body_text(
        "Lifextreme no opera como un modelo SaaS B2B centralizado ni como un intermediario extractivo convencional. "
        "Constituye una infraestructura abierta de turismo de aventura, seguridad en alta montana y geointeligencia territorial "
        "originada en Cusco, Peru, disenada bajo una hoja de ruta de descentralizacion progresiva hacia una Organizacion Autonoma "
        "Descentralizada (DAO) gobernada por guias de montana, portadores, cooperativas rurales y operadores locales (prototipado "
        "actualmente bajo el modelo de Gobernanza Andina / Protocolo Ayni en dao-comunidad.html y open-source.html con votacion "
        "sin gas respaldada por Snapshot e IPFS)."
    )
    pdf.body_text(
        "El nucleo tecnico de esta postulacion es la Soberania Tecnologica y de Datos: eliminar la dependencia estructural de APIs "
        "de inteligencia artificial centralizadas y corporativas para procesar conocimiento normativo, geoespacial y biomedico andino. "
        "Mediante el financiamiento de un nodo fisico local (Edge AI con arquitectura de Memoria Unificada en Cusco), la plataforma "
        "consolidara un sistema de inferencia abierto, auditable, sin censura y con costo marginal cero por consulta, garantizando "
        "la preservacion de datos latinoamericanos bajo control comunitario."
    )

    # Fase 1
    pdf.section_header("Fase 1: El Ecosistema Actual de Lifextreme (Foco Principal)", (67, 56, 202)) # Indigo
    pdf.body_text(
        "Lifextreme opera actualmente una arquitectura distribuida multi-capa orientada a tolerancia a fallos en conectividad andina, "
        "interoperabilidad abierta mediante estandares de contexto de modelos (MCP) y visualizacion espacial en tiempo real."
    )

    pdf.sub_header("1.1 Infraestructura Web, Capa Relacional y Contenerizacion")
    pdf.bullet_item(
        "Distribucion Perimetral y Capa Serverless (Vercel)",
        "El plano de presentacion se despliega sobre Vercel (vercel.json con cleanUrls: true, politicas estrictas de seguridad HTTP mediante Content-Security-Policy, X-Frame-Options: DENY, X-Content-Type-Options: nosniff y Referrer-Policy: strict-origin-when-cross-origin). La interfaz evita frameworks pesados con sobrecarga de hidratacion, empleando modulos Vanilla ES6+ para operar de manera deterministica sobre redes moviles 3G/4G de zonas rurales y pasos de alta montana. Las rutas perimetrales se reescriben hacia funciones serverless en api/ (api/windy-webcams.js, api/trains-telemetry.js, api/peru-govtech-mcp.js, api/max-chat.js, api/send-email.js), desacoplando la telemetria de lectura rapida del nucleo de inferencia."
    )
    pdf.bullet_item(
        "Backend Asincrono en FastAPI",
        "Plano Productivo (backend/src/server.py): Servidor FastAPI asincrono con soporte de Server-Sent Events (SSE) en /webhook/lifextreme/stream y /webhook/b2b/stream, integrando el router agentico maestro para streaming en tiempo real. Plano Operativo Local (api/main.py): Expone servicios de integracion B2B, endpoints de cotizacion (/api/v1/b2b/quote), verificacion de salud del ecosistema (/health, /api/v1/system/status) y pasarela unificada de telemetria."
    )
    pdf.bullet_item(
        "Persistencia Relacional y Seguridad Multi-Tenant (Supabase PostgreSQL)",
        "Gestion de datos estructurados, trazas de auditoria, reservas y perfiles de agencias sobre PostgreSQL (esquemas supabase_complete.sql, supabase_schema.sql). Implementacion de Row Level Security (RLS) estricto (supabase_rls.sql): Aislamiento a nivel de fila para garantizar que las cooperativas y agencias locales mantengan control soberano sobre sus registros comerciales."
    )
    pdf.bullet_item(
        "Orquestacion y Despliegue Reproducible (Docker)",
        "Contenerizacion modular mediante docker-compose.yml y docker-compose.qdrant.yml, asegurando paridad de entornos entre nodos de desarrollo local y servidores de alta disponibilidad."
    )

    pdf.sub_header("1.2 Agentes Inteligentes, Pydantic-AI y Model Context Protocol (MCP)")
    pdf.body_text("Lifextreme reemplaza los chatbots convencionales basados en cadenas de texto no estructuradas por un sistema multi-agente tipado y deterministico:")
    pdf.bullet_item(
        "Chatbot MAX (B2C - Concierge de Altitud y Rutas Extremas)",
        "Implementado en backend/src/max_agent.py y scripts/agent_whatsapp_sales.py. Disenado especificamente para responder ante contingencias fisiologicas de gran altitud (evaluacion de aclimatacion, riesgo de Soroche/HAPE en pasos superiores a 4,200 msnm), recomendacion de itinerarios de aventura y cierre transaccional transparente."
    )
    pdf.bullet_item(
        "LIFEXTREME-CORE (B2B - Analista de Cumplimiento Normativo y Operaciones)",
        "Implementado en backend/src/partner_agent.py y api/main.py. Asiste a operadores locales en la validacion de requisitos legales, estructuracion de expedientes para MINCETUR y analisis de solvencia operativa de prestadores turisticos."
    )
    pdf.bullet_item(
        "Tipado Estricto con Pydantic-AI",
        "La comunicacion inter-agente y la extraccion de entidades se rige por contratos tipados en backend/src/models.py (estructuras UserProfile, QuoteRequest, B2BQueryResponse, AgentAction). Elimina alucinaciones en cotizaciones financieras, cronogramas de expedicion y verificaciones de identidad."
    )
    pdf.bullet_item(
        "MCP Peru GovTech (backend/src/mcp_server.py)",
        "Servidor MCP nativo que expone herramientas estandarizadas para consultar fuentes publicas y de emergencia: sutran_alertas_viales (monitoreo de bloqueos viales), senamhi_clima_alertas (telemetria meteorologica andina y alertas de heladas), mincetur_consultar_prestador (verificacion de licencias de agencias y guias oficiales), sernanp_consultar_anp (regulacion de acceso y capacidad de carga en Areas Naturales Protegidas) e igp_ultimo_sismo (actividad sismica en tiempo real)."
    )
    pdf.bullet_item(
        "MCP Argon SRE (agents_core/mcp_argon.py)",
        "Servidor MCP para Site Reliability Engineering (SRE), auditoria de recursos, monitorizacion de salud del motor vectorial Qdrant, integracion Git y deteccion de credenciales expuestas."
    )

    pdf.sub_header("1.3 Geointeligencia (GEOINT) y Visualizacion Espacial 3D")
    pdf.body_text("La infraestructura integra una consola de operaciones tacticas (geoint.html, js/geoint-engine.js) para la toma de decisiones en tiempo real sobre la geografia andina:")
    pdf.bullet_item(
        "Motores de Renderizado WebGL (Three.js y CesiumJS)",
        "geoint.html y js/modules/cesium-bridge.js implementan navegacion 3D sobre modelos digitales de elevacion (DEM) del terreno andino, permitiendo auditar visualmente rutas de trekking como el Camino Inca, Salkantay y Ausangate. visualizador-3d.html y js/visualizer-3d-main.js despliegan mapas de calor y topologias de red tridimensionales en Three.js para la evaluacion del estado de las rutas."
    )
    pdf.bullet_item(
        "Telemetria de Transporte y Analisis Vectorial Geoespacial",
        "Interpolacion de trayectorias ferroviarias en tiempo real sobre la ruta Ollantaytambo - Machu Picchu (PeruRail / IncaRail) utilizando Turf.js v7 y proyecciones espaciales en WGS84. Monitorizacion meteorologica visual mediante transmisiones de video HLS (HLS.js) integradas con camaras en vivo en puertos de montana andinos."
    )

    # Fase 2
    pdf.section_header("Fase 2: El Motor de Datos y RAG (Foco Secundario)", (6, 182, 212)) # Cyan

    pdf.sub_header("2.1 Infraestructura de Base de Datos Vectorial: Qdrant")
    pdf.body_text("Lifextreme ha desplegado y configurado una instancia dedicada de Qdrant (docker-compose.qdrant.yml) que aloja la coleccion principal de conocimiento territorial:")
    pdf.bullet_item("Metrica de Distancia", "Similitud Coseno (Cosine Distance).")
    pdf.bullet_item("Dimensionalidad Vectorial", "768 dimensiones.")
    pdf.bullet_item("Volumen Indexado", "Mas de 336,869 vectores activos, estructurados con filtrado por metadatos (region, provincia, categoria normativa, tipo de prestador y nivel de riesgo de ruta).")

    pdf.sub_header("2.2 Volumen y Valor Publico: El Conocimiento Andino como Bien Publico Digital")
    pdf.body_text("El corpus vectorial no es propietario ni cerrado. Ha sido estructurado para constituir un Bien Publico Digital (DPG) accesible para la comunidad:")
    pdf.bullet_item(
        "Fuentes Integradas y Vectorizadas (>336,000 registros)",
        "Directorio Nacional de Prestadores de Servicios Turisticos Calificados del MINCETUR (guias oficiales, agencias de viajes, hospedajes y transporte turistico); Marco Legal y Regulatorio Peruano (codigos normativos de turismo de aventura, reglamentos de alta montana, TUPA de SERNANP y ordenanzas regionales de Cusco); Inventario Nacional de Recursos Turisticos y cartografia de areas naturales protegidas."
    )
    pdf.bullet_item(
        "Democratizacion Regulatoria y Soberania Comunitaria",
        "Permite que comunidades campesinas, porteadores y pequenos emprendedores quechuas accedan a auditorias de cumplimiento normativo gratuitas y en lenguaje natural, convierte regulaciones dispersas en alertas operativas directas para brigadas de rescate y resuelve la asimetria de informacion donde unicamente grandes operadoras internacionales podian operar licencias."
    )

    pdf.sub_header("2.3 Pipeline de Embeddings e Inferencia Local: nomic-embed-text")
    pdf.bullet_item(
        "Generacion de Embeddings Abiertos",
        "El pipeline vectorial emplea el modelo open-weight nomic-embed-text (scripts/embed_mincetur.py, scripts/vectorize_mincetur.py, backend/src/rag_pipeline.py)."
    )
    pdf.bullet_item(
        "Recuperacion Aumentada por Generacion (RAG)",
        "Implementa recuperacion hibrida (Dense Retrieval + Payload Filtering) conectada directamente al contexto de los agentes de Pydantic-AI, garantizando respuestas con trazabilidad documental estricta hacia las resoluciones del MINCETUR."
    )

    # Fase 3
    pdf.section_header("Fase 3: La Solicitud de Financiamiento (El Salto a la Soberania)", (244, 63, 94)) # Sunset Flame

    pdf.sub_header("3.1 El Problema: Vulnerabilidad de APIs Centralizadas y Modelo Financiero Inviable")
    pdf.bullet_item(
        "Fuga y Colonizacion de Datos",
        "El enrutamiento de consultas territoriales, normativas y biomedicas de los Andes a traves de APIs comerciales (OpenAI, Anthropic) transfiere soberania de datos estrategicos hacia centros de datos en el norte global, sin garantias de privacidad comunitaria ni control sobre sesgos algoritmicos."
    )
    pdf.bullet_item(
        "Inviabilidad Financiera para la Gobernanza DAO",
        "El costo variable por token en APIs propietarias destruye la viabilidad de un bien publico. En un modelo de alto volumen transaccional o ante situaciones de crisis/rescate, las tarifas de inferencia representan un cuello de botella financiero incompatible con una organizacion comunitaria sin fines extractivos."
    )

    pdf.sub_header("3.2 La Solucion Tecnologica: Cluster Local Edge AI en Cusco")
    pdf.body_text("El capital solicitado en este Grant sera destinado especificamente a la adquisicion y despliegue de infraestructura fisica de computo local en Cusco (Hardware Edge AI con arquitectura de Memoria Unificada):")
    pdf.bullet_item(
        "Especificaciones de Infraestructura Fisica Proyectada",
        "Servidor / Workstation de Memoria Unificada (Apple Silicon M-Series Ultra / Max con 64GB - 128GB de ancho de banda masivo >400 GB/s, o cluster de aceleracion local RTX Ada Lovelace), Nodo de Almacenamiento Solido NVMe PCIe Gen4 para baja latencia en Qdrant, y sistema de respaldo energetico UPS de onda senoidal pura."
    )
    pdf.bullet_item(
        "Modelos Open-Source Ejecutados Localmente via Ollama",
        "qwen2.5:7b (razonamiento logico estructurado, soporte multilingue y contratos Pydantic-AI/MCP), Familia Llama 3 / Llama-3.1-8B-Instruct (sintesis narrativa y atencion conversacional para MAX), sobre Ollama Daemon (http://localhost:11434) ya soportado en el codigo base."
    )
    pdf.bullet_item(
        "Impacto Tecnico y Social",
        "Costo Marginal Cero ($0.00 por token) eliminando el gasto recurrente por llamada de inferencia, Privacidad Absoluta y Resiliencia Offline ante caidas de conectividad internacional."
    )

    # Presupuesto Solicitado
    pdf.section_header("Presupuesto Solicitado y Desglose de Asignacion de Fondos", (16, 185, 129)) # Emerald
    budget_rows = [
        ("Hardware Edge AI", "Cluster de Memoria Unificada (Apple Silicon / RTX Workstation 128GB RAM) para inferencia local con Ollama", "$24,500", "Hito 1"),
        ("Infraestructura & Storage", "Nodos de almacenamiento NVMe enterprise, UPS redundante y networking local en Cusco", "$6,000", "Hito 1"),
        ("Despliegue & MCP Dev", "Desarrollo de conectores MCP restantes (SUTRAN/SENAMHI) y pipeline de vectorizacion local a 1M de vectores", "$10,000", "Hito 2"),
        ("Auditoria de Seguridad", "Evaluacion de contratos de privacidad, pruebas de penetracion y auditoria de esquemas RLS en Supabase", "$5,000", "Hito 3"),
        ("Gobernanza Andina (DAO)", "Despliegue de contratos de votacion comunitaria sin gas en Arbitrum / Lisk y frontend Ayni", "$3,000", "Hito 3"),
        ("Total Solicitado", "Meta de Financiamiento para Soberania Tecnologica", "$48,500 USD", "Plazo: 6 Meses")
    ]
    pdf.draw_budget_table(budget_rows)

    pdf.sub_header("Hitos de Ejecucion (Milestones Auditables)")
    pdf.bullet_item("Hito 1 (Mes 1 - 2)", "Adquisicion, ensamble y despliegue del nodo fisico de Memoria Unificada en Cusco. Migracion del 100% de las consultas de MAX y CORE a inferencia local via Ollama (qwen2.5:7b / Llama-3.1).")
    pdf.bullet_item("Hito 2 (Mes 3 - 4)", "Publicacion del dataset abierto de vectores normativos (>500,000 registros) como Bien Publico Digital y estandarizacion de la API publica MCP GovTech Peru.")
    pdf.bullet_item("Hito 3 (Mes 5 - 6)", "Despliegue de los contratos de gobernanza comunitaria en testnet/mainnet de L2 (Arbitrum/Lisk) y entrega de informe final de auditoria de impacto descentralizado.")

    # Informacion Institucional
    pdf.section_header("Informacion Institucional, Canales Oficiales y Contacto Tecnico", (15, 23, 42)) # Slate 900
    contact_rows = [
        ("Nombre del Proyecto", "Lifextreme (Lifextreme AI / Protocolo Ayni)"),
        ("Entidad / Organizacion", "Lifextreme Open Source Initiative"),
        ("Jurisdiccion Operativa", "Cusco, Region Andina, Peru (Codigo Postal 08000)"),
        ("Sitio Web Principal", "https://www.lifextreme.com.pe"),
        ("War Room & Demostracion 3D", "https://www.lifextreme.com.pe/geoint.html"),
        ("Visor Neuronal de Arquitectura (3D)", "https://www.lifextreme.com.pe/neural-brain-3d.html"),
        ("Correo Electronico Oficial", "contacto@lifextreme.com.pe"),
        ("Telefono / WhatsApp de Coordinacion", "+51 958 050 928"),
        ("Gobernanza y Bienes Publicos", "dao-comunidad.html · open-source.html")
    ]
    pdf.draw_kv_table(contact_rows, col1_w=62, col2_w=124, header1="Parametro Institucional", header2="Detalle Oficial")

    out_file = "LIFEXTREME_GRANT_PROPOSAL_SOBERANIA_EDGE_AI.pdf"
    pdf.output(out_file, 'F')
    print(f"PDF complete generated successfully: {out_file}")

if __name__ == "__main__":
    generate_full_pdf()
