import os
import shutil
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PITCH_DIR = os.path.join(BASE_DIR, 'data', 'obsidian_vault', '000_PITCH_INVERSORES')

def sanitize_filename(name, max_length=60):
    clean_name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    if len(clean_name) > max_length:
        clean_name = clean_name[:max_length].strip()
    return clean_name or "Desconocido"

def create_showcase():
    if os.path.exists(PITCH_DIR):
        shutil.rmtree(PITCH_DIR)
    os.makedirs(PITCH_DIR)

    # 1. GENERAR LA BÓVEDA MASIVA (PARA MOSTRAR ESCALA)
    db_dir = os.path.join(PITCH_DIR, "DB_Cusco_Real")
    os.makedirs(db_dir)
    
    cusco_hub_name = "DB_MASTER_CUSCO"
    cusco_hub_file = os.path.join(db_dir, f"{cusco_hub_name}.md")
    
    with open(cusco_hub_file, "w", encoding="utf-8") as f:
        f.write("# 🏛️ Base de Datos Maestra: CUSCO\n\n")
        f.write("Esta es la red neuronal de fondo (Conocimiento inactivo).\n\n")

    destinos_cusco = [
        "Salkantay", "Machu_Picchu", "Valle_Sagrado", "Montana_7_Colores", "Laguna_Humantay",
        "Choquequirao", "Ausangate", "Cusco_City", "Sacsayhuaman", "Ollantaytambo",
        "Pisac", "Maras_Moray", "Chinchero", "Huchuy_Qosqo", "Lares_Trek"
    ]
    
    categorias = [
        "Logistica_Transporte", "Precios_Moneda", "Clima_Temporadas", "Seguridad_Riesgos",
        "Salud_Altitud", "Equipamiento_Tecnico", "Gastronomia", "Cultura_Historia",
        "Hoteles_Glamping", "Permisos_Tickets"
    ]

    for dest in destinos_cusco:
        dest_name = f"DB_DEST_{dest}"
        # Link en el hub maestro
        with open(cusco_hub_file, "a", encoding="utf-8") as f:
            f.write(f"- [[{dest_name}]]\n")
            
        # Crear hub del destino
        with open(os.path.join(db_dir, f"{dest_name}.md"), "w", encoding="utf-8") as f:
            f.write(f"# Destino: {dest.replace('_', ' ')}\n")
            f.write(f"Conectado a: [[{cusco_hub_name}]]\n\n")
            
            for cat in categorias:
                cat_name = f"{dest_name}_{cat}"
                f.write(f"- [[{cat_name}]]\n")
                
                # Crear nodo de categoria
                with open(os.path.join(db_dir, f"{cat_name}.md"), "w", encoding="utf-8") as cat_f:
                    cat_f.write(f"# {cat.replace('_', ' ')} en {dest.replace('_', ' ')}\n")
                    cat_f.write(f"Conectado a: [[{dest_name}]]\n")

    # 2. CREATE THE PRESENTATION NODES (PRECISIÓN LÁSER)
    with open(os.path.join(PITCH_DIR, "00_DASHBOARD_INVERSOR.md"), "w", encoding="utf-8") as f:
        f.write("# 🧠 Cerebro Lifextreme: Escala Masiva + Precisión Láser\n\n")
        f.write("Este diagrama demuestra cómo el Motor RAG tiene acceso a toda la bóveda (Huchuy Qosqo, Ausangate), pero dispara un láser de precisión matemática únicamente hacia los vectores de Salkantay.\n\n")
        f.write("```mermaid\n")
        f.write("graph TD\n")
        f.write("    A[\"👤 Input: Salkantay, Dolor de rodilla\"] --> B{\"🧠 Motor NLP MAX\"}\n")
        f.write("    B --> C[\"🗄️ Búsqueda RAG (Similitud del Coseno)\"]\n")
        f.write("    \n")
        f.write("    C --> S1([Vector: Salkantay Salud y Altitud])\n")
        f.write("    C --> S2([Vector: Salkantay Seguridad])\n")
        f.write("    C --> S3([Vector: Salkantay Precios])\n")
        f.write("    \n")
        f.write("    S1 --> D[\"🏔️ Topología Extraída\"]\n")
        f.write("    S2 --> D\n")
        f.write("    \n")
        f.write("    B -.-> E((\"⚠️ Alerta Médica\"))\n")
        f.write("    E --> F[\"🛡️ Agente de Seguridad\"]\n")
        f.write("    F --> G[\"🚁 Logística: Caballo de Rescate + Bastones\"]\n")
        f.write("    \n")
        f.write("    B -.-> H((\"💰 Oportunidad Negocio\"))\n")
        f.write("    H --> I[\"📈 Agente de Ventas\"]\n")
        f.write("    I --> J[\"💎 Up-selling VIP\"]\n")
        f.write("    J --> K[\"💵 Rentabilidad: Margen +35%\"]\n")
        f.write("    \n")
        f.write("    G --> L{\"⚙️ Motor de Síntesis (Llama-3)\"}\n")
        f.write("    K --> L\n")
        f.write("    D --> L\n")
        f.write("    L --> M[\"✅ Output: Cierre por $580 USD c/u + Link\"]\n")
        f.write("    \n")
        f.write("    classDef cliente fill:#9B59B6,stroke:#fff,stroke-width:2px,color:#fff;\n")
        f.write("    classDef ia fill:#3498DB,stroke:#fff,stroke-width:2px,color:#fff;\n")
        f.write("    classDef alerta fill:#E74C3C,stroke:#fff,stroke-width:2px,color:#fff;\n")
        f.write("    classDef ventas fill:#2ECC71,stroke:#fff,stroke-width:2px,color:#fff;\n")
        f.write("    classDef db fill:#F39C12,stroke:#fff,stroke-width:2px,color:#fff;\n")
        f.write("    classDef vector fill:#00FF00,stroke:#fff,stroke-width:2px,color:#000;\n")
        f.write("    \n")
        f.write("    class A cliente;\n")
        f.write("    class B,L,M ia;\n")
        f.write("    class C,D db;\n")
        f.write("    class E,F,G alerta;\n")
        f.write("    class H,I,J,K ventas;\n")
        f.write("    class S1,S2,S3 vector;\n")
        f.write("```\n\n")

    with open(os.path.join(PITCH_DIR, "01_Input_Cliente.md"), "w", encoding="utf-8") as f:
        f.write("# 01. Interacción del Cliente\n\n")
        f.write("**Mensaje Real:** *\"Hola, somos un grupo de 5 amigos. Queremos hacer el Salkantay Trek de 5 días y 4 noches. Uno sufre de las rodillas y no tenemos equipo...\"*\n\n")
        f.write("Se activa: [[02_Clasificador_Intencion]]\n")

    with open(os.path.join(PITCH_DIR, "02_Clasificador_Intencion.md"), "w", encoding="utf-8") as f:
        f.write("# 02. Clasificador de Intención y Riesgo\n\n")
        f.write("La IA fragmenta el mensaje:\n")
        f.write("- **Geografía detectada:** Salkantay Trek.\n")
        f.write("- **Alerta Médica:** Activa al agente de [[04_Agente_Seguridad]].\n")
        f.write("- **Ventas:** Se activa el agente de [[05_Agente_Ventas]].\n\n")
        f.write("Avanza a: [[03_RAG_Extraccion_Datos]]\n")

    with open(os.path.join(PITCH_DIR, "03_RAG_Extraccion_Datos.md"), "w", encoding="utf-8") as f:
        f.write("# 03. Motor RAG (Búsqueda Vectorial de Alta Precisión)\n\n")
        f.write("Aunque Lifextreme posee una bóveda masiva de 150+ nodos de Cusco en el fondo, el motor RAG dispara un láser de precisión extrayendo ÚNICAMENTE los vectores semánticos con altísima similitud al problema del cliente:\n\n")
        f.write("### Vectores Extraídos:\n")
        f.write("- [[DB_DEST_Salkantay_Logistica_Transporte]]\n")
        f.write("- [[DB_DEST_Salkantay_Seguridad_Riesgos]]\n")
        f.write("- [[DB_DEST_Salkantay_Salud_Altitud]]\n")
        f.write("- [[DB_DEST_Salkantay_Precios_Moneda]]\n\n")
        f.write("Esta información purificada alimenta a:\n")
        f.write("-> [[04_Agente_Seguridad]]\n")
        f.write("-> [[05_Agente_Ventas]]\n")

    with open(os.path.join(PITCH_DIR, "04_Agente_Seguridad.md"), "w", encoding="utf-8") as f:
        f.write("# 04. Evaluación de Riesgo\n\n")
        f.write("**Problema:** Rodillas.\n")
        f.write("**Solución RAG:** Caballo de emergencia y bastones.\n\n")
        f.write("Pasa a: [[05_Agente_Ventas]]\n")

    with open(os.path.join(PITCH_DIR, "05_Agente_Ventas.md"), "w", encoding="utf-8") as f:
        f.write("# 05. Estratega de Ventas y Up-selling\n\n")
        f.write("**Tácticas:** Upgrade a Domos Glamping, bolsas de pluma.\n")
        f.write("**Resultado:** Margen de rentabilidad escalado al vender equipo.\n\n")
        f.write("Genera: [[06_Output_Final_MAX]]\n")

    with open(os.path.join(PITCH_DIR, "06_Output_Final_MAX.md"), "w", encoding="utf-8") as f:
        f.write("# 06. Respuesta Entregada por MAX IA\n\n")
        f.write("> *¡Hola viajeros! Prepararse para el Salkantay es increíble. Al ser 5, mi recomendación es un **Servicio Privado VIP** por $580 USD c/u.*\n\n")

    print(f"Showcase Salkantay con Escala y Precisión generado.")

if __name__ == "__main__":
    create_showcase()
