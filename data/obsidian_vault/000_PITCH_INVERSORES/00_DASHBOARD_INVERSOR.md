# 🧠 Cerebro Lifextreme: Escala Masiva + Precisión Láser

Este diagrama demuestra cómo el Motor RAG tiene acceso a toda la bóveda (Huchuy Qosqo, Ausangate), pero dispara un láser de precisión matemática únicamente hacia los vectores de Salkantay.

```mermaid
graph TD
    A["👤 Input: Salkantay, Dolor de rodilla"] --> B{"🧠 Motor NLP MAX"}
    B --> C["🗄️ Búsqueda RAG (Similitud del Coseno)"]
    
    C --> S1([Vector: Salkantay Salud y Altitud])
    C --> S2([Vector: Salkantay Seguridad])
    C --> S3([Vector: Salkantay Precios])
    
    S1 --> D["🏔️ Topología Extraída"]
    S2 --> D
    
    B -.-> E(("⚠️ Alerta Médica"))
    E --> F["🛡️ Agente de Seguridad"]
    F --> G["🚁 Logística: Caballo de Rescate + Bastones"]
    
    B -.-> H(("💰 Oportunidad Negocio"))
    H --> I["📈 Agente de Ventas"]
    I --> J["💎 Up-selling VIP"]
    J --> K["💵 Rentabilidad: Margen +35%"]
    
    G --> L{"⚙️ Motor de Síntesis (Llama-3)"}
    K --> L
    D --> L
    L --> M["✅ Output: Cierre por $580 USD c/u + Link"]
    
    classDef cliente fill:#9B59B6,stroke:#fff,stroke-width:2px,color:#fff;
    classDef ia fill:#3498DB,stroke:#fff,stroke-width:2px,color:#fff;
    classDef alerta fill:#E74C3C,stroke:#fff,stroke-width:2px,color:#fff;
    classDef ventas fill:#2ECC71,stroke:#fff,stroke-width:2px,color:#fff;
    classDef db fill:#F39C12,stroke:#fff,stroke-width:2px,color:#fff;
    classDef vector fill:#00FF00,stroke:#fff,stroke-width:2px,color:#000;
    
    class A cliente;
    class B,L,M ia;
    class C,D db;
    class E,F,G alerta;
    class H,I,J,K ventas;
    class S1,S2,S3 vector;
```

