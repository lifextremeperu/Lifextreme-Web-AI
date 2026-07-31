import json

def generate_investors_list():
    markdown = "# 🎯 Megabase de Inversionistas: Lifextreme AI (120 Targets Estratégicos)\n\n"
    markdown += "Esta es tu lista de ataque comercial, dividida por el tipo de capital o beneficio estratégico que buscas.\n\n"

    # 1. 20 Strategic Angels (Local Operators)
    markdown += "## 1. Ángeles Estratégicos: Operadores Locales & Mayoristas (20 Opciones)\n"
    markdown += "**Por qué invertirían:** Buscan exclusividad tecnológica. No quieren que su competencia tenga acceso al Cerebro Ayni Evolve. Tienen flujo de caja rápido.\n\n"
    local_ops = [
        "Amazonas Explorer (Cusco) - Mercado de lujo anglosajón.",
        "Condor Travel (Lima/Nacional) - El gigante corporativo que necesita optimizar costos B2B.",
        "Adventure Cusco Tours (Cusco) - Altísimo volumen de reviews, necesitan automatización urgente.",
        "Cusco Peru Adventure (Cusco) - Tour operador consolidado con alta necesidad de SEO.",
        "Encuentros Peru Adventure (Cusco) - Fuerte operación B2B.",
        "Aventuras.pe (Tarapoto/Nacional) - Para expandir la IA fuera de Cusco a la Amazonía.",
        "LimaTours (Lima) - El otro gigante corporativo peruano, competencia directa de Condor.",
        "Inca Expeditions (Cusco) - Operador de trekking masivo.",
        "Salkantay Trekking (Cusco) - Dominantes en la ruta Salkantay, necesitan respuestas automáticas.",
        "Machu Picchu Epic (Cusco) - Nicho de aventura premium.",
        "Green Peru Adventures (Cusco) - Fuerte enfoque en ecoturismo.",
        "Andean Adventures Peru (Cusco) - Operador B2B clásico que necesita modernizarse.",
        "Trip Alpaca Adventure (Cusco) - Alta tasa de reviews, listos para escalar.",
        "Ausangate Adventure (Cusco) - Nicho específico de alta montaña, ideal para IA hiper-entrenada.",
        "Peru For Less (Lima/Cusco) - Agencia gigante norteamericana operando en Perú, mucho capital.",
        "SA Expeditions (Nacional) - Alta tecnología y ventas remotas.",
        "Kuoda Travel (Cusco) - Turismo boutique de ultra-lujo.",
        "Explorandes (Nacional) - Pioneros en aventura, necesitan renovar su stack tecnológico.",
        "Inca Trail Reservations (Nacional) - El monopolio online de reservas del Camino Inca.",
        "Tour in Peru (Cusco) - Operador de alto volumen multicanal."
    ]
    for i, op in enumerate(local_ops, 1):
        markdown += f"{i}. **{op.split(' - ')[0]}**: {op.split(' - ')[1]}\n"

    # 2. 30 LATAM VCs
    markdown += "\n## 2. Venture Capital LATAM: Early Stage & Seed (30 Opciones)\n"
    markdown += "**Por qué invertirían:** Buscan startups SaaS con modelos escalables y rentables. Entienden el mercado andino.\n\n"
    latam_vcs = [
        "Salkantay Ventures (Perú) - Conocen el mercado local y apoyan startups andinas.",
        "Kalkuli (Perú) - Invierten en SaaS y B2B en fases tempranas.",
        "BuenTrip Ventures (Ecuador) - Muy activos en startups B2B de la región andina.",
        "Kaszek Ventures (Argentina/Regional) - El gigante de Latam, invierten en dominadores de mercado.",
        "Monashees (Brasil) - Buscan infraestructura tecnológica profunda.",
        "TheVentureCity (Global/Latam) - Enfoque en producto y métricas de retención.",
        "NXTP Ventures (Argentina) - Expertos en SaaS B2B.",
        "Alegra Capital (Colombia) - Inversionistas en software de gestión comercial.",
        "Magma Partners (Chile/Latam) - Invierten en SaaS B2B a lo largo de Latam.",
        "Alaya Capital (Latam) - Fuerte presencia en la región andina.",
        "Angel Ventures Peru (Perú) - Ecosistema local directo.",
        "Wayra Peru (Perú) - Brazo de inversión de Telefónica, mucha red corporativa.",
        "Innova Funding / Ángeles (Perú) - Red de ángeles peruanos.",
        "Genesis Ventures (Chile/Perú) - Capital para escalabilidad B2B.",
        "Cometa (México) - Fuerte inversión en infraestructura Latam.",
        "ALLVP (México) - Capital para startups transformacionales.",
        "Valor Capital Group (Brasil/Latam) - Inversión transfronteriza.",
        "Redpoint eventures (Brasil) - Expertos en SaaS.",
        "Canary (Brasil/Latam) - Fuerte enfoque en etapa Seed.",
        "Amador Holdings (Panamá/Latam) - Redes en todo Centro y Sudamérica.",
        "Dalus Capital (México) - Inversiones con propósito de eficiencia.",
        "GridX (Argentina) - Deep tech (tu modelo Ayni Evolve entra aquí).",
        "Salto Partners (Uruguay) - Búsqueda de software B2B.",
        "Endeavor Catalyst (Global/Latam) - Si logras entrar a Endeavor, ellos invierten.",
        "Ignia (México) - Soluciones para la clase media/emergente.",
        "Aventti (Colombia) - Red de ángeles andinos.",
        "Oikos (Perú) - Family offices peruanas buscando diversificar en tech.",
        "Devv (Chile) - Software developers funding software.",
        "B Venture Capital (Latam) - Fondo regional enfocado en pre-seed y seed.",
        "Polymath Ventures (Colombia) - Venture studio que arma tecnología para Latinoamérica."
    ]
    for i, op in enumerate(latam_vcs, 21):
        markdown += f"{i}. **{op.split(' - ')[0]}**: {op.split(' - ')[1]}\n"

    # 3. 30 Global Travel-Tech VCs
    markdown += "\n## 3. Global Travel-Tech VCs & Accelerators (30 Opciones)\n"
    markdown += "**Por qué invertirían:** Tú solucionas la 'alucinación legal' de la IA en turismo (con tu DeepEval), un problema que bloquea al Travel-Tech mundial.\n\n"
    global_vcs = [
        "Thayer Ventures (EE.UU.) - El fondo líder exclusivo en Travel & Hospitality Tech.",
        "Plug and Play Travel (Global) - La aceleradora turística más grande del mundo.",
        "Velocity Ventures (Singapur/Global) - Especialistas absolutos en traveltech.",
        "TravelTech.VC (Global) - Fondo especializado en SaaS turístico B2B (TT1 y TT2).",
        "Howzat Partners (Europa) - Inversores iniciales en Trivago, conocen B2B de viajes.",
        "Lazarus Ventures (EE.UU.) - Enfoque en infraestructuras complejas.",
        "Phocuswright Innovation (Global) - Plataforma de inversión y pitch de Travel Tech.",
        "Amadeus Ventures (Global) - Brazo VC del GDS más grande del mundo.",
        "JetBlue Technology Ventures (EE.UU.) - Invierten en el ecosistema amplio de viajes.",
        "Travel Capitalist Ventures (Global) - Expertos en turismo y capital privado.",
        "Bessemer Venture Partners (Global) - Gigantes de SaaS (inversores de Shopify).",
        "Sequoia Capital (Global) - Interesados en infraestructuras LLM puras (como tu Ayni Evolve).",
        "Y Combinator (EE.UU.) - Tienen un track específico para SaaS B2B e IA.",
        "Techstars Travel (Global) - Aceleradora con corporativos gigantes.",
        "500 Startups (Global/Latam) - Alto apetito por herramientas B2B hiper-especializadas.",
        "General Catalyst (EE.UU.) - Fuertes inversiones en IA y automatización corporativa.",
        "a16z (Andreessen Horowitz) (EE.UU.) - Tienen tesis activas sobre RAG y agentes autónomos.",
        "Benchmark (EE.UU.) - Inversores de infraestructura pura.",
        "Spark Capital (EE.UU.) - Capital para herramientas de productividad B2B.",
        "Lightspeed Venture Partners (Global) - Tesis en software de IA corporativo.",
        "Khosla Ventures (EE.UU.) - Buscan tecnologías que reemplacen ineficiencias masivas.",
        "Founders Fund (EE.UU.) - Les encanta el software que monopoliza nichos (Cusco).",
        "Index Ventures (Europa/EE.UU.) - Mucha experiencia en plataformas de gestión.",
        "Accel (Global) - Tesis fuerte en software de infraestructura en la nube.",
        "Bain Capital Ventures (EE.UU.) - Inversión en software de servicios B2B.",
        "Insight Partners (EE.UU.) - Maestros del escalamiento de SaaS B2B.",
        "Matrix Partners (Global) - Enfocados en fundadores técnicos solos (Solo-founders).",
        "Point Nine Capital (Europa) - El VC más enfocado en SaaS B2B early stage.",
        "SaaStr Fund (Global) - Especializados exclusivamente en B2B SaaS.",
        "First Round Capital (EE.UU.) - Expertos en llevar productos técnicos al mercado."
    ]
    for i, op in enumerate(global_vcs, 51):
        markdown += f"{i}. **{op.split(' - ')[0]}**: {op.split(' - ')[1]}\n"

    # 4. 20 Corporate VCs & OTAs
    markdown += "\n## 4. Corporate Venture Capital & Gigantes del Turismo (20 Opciones)\n"
    markdown += "**Por qué invertirían:** M&A (Fusiones y Adquisiciones). Quieren comprar tu tecnología para usarla en sus propios call centers o para ahogar a su competencia.\n\n"
    corporate = [
        "Booking Holdings (Global) - Les interesa optimizar la validación de proveedores locales.",
        "Despegar / Decolar (Latam) - El gigante regional que necesita IA para soporte B2B.",
        "Expedia Group (Global) - Fuerte inversión en optimización AEO y SEO algorítmico.",
        "TripAdvisor (Global) - Tu modelo de Auditoría B2B puede integrarse a su B2B Dashboard.",
        "Airbnb (Global) - Les interesa el software de validación de experiencias de aventura.",
        "G Adventures (Global) - Gigante del turismo de aventura, tu RAG audita sus rutas.",
        "Intrepid Travel (Global) - Interesados en cumplimiento de leyes locales y sostenibilidad.",
        "TUI Group (Europa/Global) - El tour operador más grande del mundo.",
        "CWT (Carlson Wagonlit Travel) (Global) - Gestión de viajes corporativos y compliance.",
        "American Express Global Business Travel (Global) - Necesitan validación de seguridad extrema.",
        "Flight Centre Travel Group (Global) - Constante adquisición de travel tech.",
        "BCD Travel (Global) - Optimización de operaciones B2B.",
        "Hopper (Global) - Aplicación de viajes basada en datos; tu data vectorial es oro.",
        "Traveloka (Asia/Global) - Expansión mediante adquisición de tecnología regional.",
        "Sabre Labs (Global) - Innovación en sistemas de reservas.",
        "Marriott International (Global) - Tienen fondos para experiencias en destino.",
        "Accor (Europa/Global) - Fuerte red hotelera que necesita conectar con tours hiperlocales.",
        "LATAM Airlines (Latam) - Inversión en fidelización y venta cruzada de tours.",
        "Copa Airlines (Hub de las Américas) - Buscan tecnología para retener al turista en Latam.",
        "Hotelbeds (Global) - Gigante del B2B (bedbank) que ahora compra tecnología de tours (ancillaries)."
    ]
    for i, op in enumerate(corporate, 81):
        markdown += f"{i}. **{op.split(' - ')[0]}**: {op.split(' - ')[1]}\n"

    # 5. 20 Impact, ESG & Regional Angels
    markdown += "\n## 5. Fondos de Impacto, ESG y Consorcios Regionales (20 Opciones)\n"
    markdown += "**Por qué invertirían:** Porque tu sistema RAG verifica leyes ambientales (MINCETUR, SERNANP) y fuerza la formalidad del turismo, lo cual tiene un impacto socioeconómico enorme.\n\n"
    esg = [
        "BID Lab (Latam) - Brazo de innovación del Banco Interamericano de Desarrollo.",
        "Acapulco Ventures (Latam) - Enfoque en desarrollo económico regional.",
        "Elevar Equity (Latam/India) - Capital para democratizar tecnología en pymes.",
        "EcoEnterprises Fund (Latam) - Invierten en biodiversidad y turismo sostenible.",
        "Oikocredit (Global) - Inversión de impacto social.",
        "NESsT (Latam) - Financian empresas que crean empleo digno (tu herramienta formaliza).",
        "Lumni (Latam) - Aunque enfocados en educación, tienen brazos de impacto tecnológico.",
        "PromPerú (Innovación) (Perú) - Tienen fondos concursables y programas de exportación de servicios.",
        "ProInnóvate (Perú) - Fondos no reembolsables del estado peruano (Startup Perú).",
        "Waykup Forum (Latam) - Foro de inversión de impacto andino.",
        "Vulcano (Chile) - Ángeles enfocados en soluciones de infraestructura andina.",
        "PEC (Private Equity Cusco) - Sindicatos no formales de hoteleros en Cusco buscando diversificar.",
        "Cámaras de Comercio Locales (Cusco/Lima) - Grupos empresariales buscando transformación digital.",
        "Agencias Suizas de Desarrollo (Global) - Fondos perdidos para formalización andina (SECO).",
        "GIZ (Cooperación Alemana) - Fondean herramientas digitales de turismo sostenible en Latam.",
        "USAID (Estados Unidos) - Subvenciones para cadenas de valor inclusivas en Perú.",
        "Yunus Social Business (Global) - Si enfocas Lifextreme como formalizador de pymes.",
        "Acumen (Global/Latam) - Fondo de impacto que resuelve pobreza mediante eficiencia corporativa.",
        "Althelia Funds (Global) - Enfoque en conservación (si el RAG audita impacto ambiental).",
        "Village Capital (Global/Latam) - Aceleradora de impacto que fondea a los ganadores (Peer-selected)."
    ]
    for i, op in enumerate(esg, 101):
        markdown += f"{i}. **{op.split(' - ')[0]}**: {op.split(' - ')[1]}\n"

    with open('Lifextreme_Top_120_Investors.md', 'w', encoding='utf-8') as f:
        f.write(markdown)

generate_investors_list()
