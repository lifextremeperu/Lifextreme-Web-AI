import os
from pathlib import Path

PDF_DIR = Path("data/documentos/pymes")
PDF_DIR.mkdir(parents=True, exist_ok=True)

docs = [
    {
        "filename": "sunafil_multas_2026.md",
        "content": """# Tabla de Multas e Infracciones SUNAFIL 2026

La Superintendencia Nacional de Fiscalización Laboral (SUNAFIL) aplica multas basadas en la gravedad de la infracción, el tipo de empresa y el número de trabajadores afectados, calculadas usando la UIT vigente.

## Infracción por Exceso de Jornada Laboral (Horas Extras)
El trabajo en sobretiempo sin el pago correspondiente o el obligar a los trabajadores a superar los límites legales de la jornada constituye una **Infracción Muy Grave** en materia de relaciones laborales.

### Criterios de Graduación de Multas (Régimen General - No MYPE)
Para una infracción **Muy Grave** que afecta a un grupo pequeño de trabajadores, los inspectores aplican la siguiente escala:
* Si afecta de 1 a 10 trabajadores (por ejemplo, **3 trabajadores**): La multa es de **2.63 UIT**.
* Si afecta de 11 a 25 trabajadores: La multa asciende a 5.25 UIT.
* Si afecta a más de 1000 trabajadores: La multa máxima es de 52.53 UIT.

El inspector utilizará el acta de infracción tipificando el exceso de horas extras como Infracción Muy Grave, aplicando la multa de 2.63 UIT por afectar a 3 trabajadores en el establecimiento.
"""
    },
    {
        "filename": "sunafil_ley_extranjeros_689.md",
        "content": """# Ley de Contratación de Trabajadores Extranjeros (Decreto Legislativo N° 689)

El Estado Peruano regula la contratación de personal extranjero para proteger el empleo nacional mediante el D.L. 689 y su Reglamento (D.S. N° 014-92-TR).

## Límites Porcentuales (Cuotas)
Toda empresa u hotel en Perú que contrate personal extranjero está sujeta a los siguientes límites máximos obligatorios:
1. **Límite sobre la Planilla:** El personal extranjero no podrá superar el **20%** del número total de trabajadores, empleados y obreros de la empresa.
2. **Límite sobre la Masa Salarial:** Las remuneraciones totales del personal extranjero no podrán exceder el **30%** del total de la planilla de sueldos y salarios de la empresa.

## Excepciones Verificables por SUNAFIL
El Artículo 3 de la ley establece que SUNAFIL puede exonerar del cumplimiento de estos porcentajes (es decir, permitir contratar más allá del 20% o 30%) a los siguientes extranjeros:
* Profesionales o técnicos altamente especializados (ej. Chefs internacionales de alta cocina, Gerentes hoteleros con certificaciones únicas).
* Personal de dirección o gerencia de una nueva inversión empresarial.
* Inversionistas extranjeros que mantengan un monto de inversión superior a 5 UIT.
Para que la excepción sea válida, la empresa debe presentar el contrato y solicitar la exoneración expresa ante la Autoridad Administrativa de Trabajo.
"""
    },
    {
        "filename": "haccp_restaurantes_fqsa.md",
        "content": """# Manual HACCP y FQSA para Cadenas Hoteleras Internacionales

Los estándares FQSA (Food Quality and Safety Audits) de nivel 3 exigen la implementación estricta del sistema HACCP (Análisis de Peligros y Puntos Críticos de Control).

## Puntos Críticos de Control (PCC) en Pescados y Mariscos
Para productos del mar (pescados crudos, mariscos, sushi), el registro documental de la cadena de frío es un PCC obligatorio.
* **Temperatura Objetivo:** Debe mantenerse estrictamente entre **0°C y 4°C** durante la recepción y almacenamiento.
* **Margen de Tolerancia Térmica:** El estándar FQSA establece una tolerancia máxima de **+2°C** por un período no mayor a 30 minutos.
* **Destrucción del Lote:** Si los productos del mar superan los **6°C** en el registro termográfico, o se rompe la cadena de frío por más de 30 minutos, se debe exigir la **destrucción inmediata del lote** para prevenir intoxicaciones por histamina o salmonella.

## Protocolo de Acción Correctiva (CAPA) por Contaminación Cruzada
Si en una auditoría FQSA de nivel 3 el inspector detecta **contaminación cruzada grave** (por ejemplo, usar la misma tabla de picar para pollos crudos y vegetales cocidos):
1. **Acción Inmediata:** Detener toda la producción de alimentos en esa zona, desechar los alimentos expuestos y desinfectar el área con químicos nivel hospitalario (amonio cuaternario).
2. **Registro CAPA:** Documentar el incidente en el formulario CAPA, especificando el reentrenamiento del personal involucrado (mínimo 4 horas de capacitación certificada en BPM) y establecer auditorías internas semanales por un mes. 
Sin el registro CAPA firmado, la cadena hotelera enfrenta la suspensión inmediata de la licencia del restaurante.
"""
    },
    {
        "filename": "expedia_visibility_booster.md",
        "content": """# Expedia Partner Central: Revenue Management & Visibility Booster

El "Visibility Booster" (Acelerador) de Expedia es una herramienta de pago por conversión que aumenta el multiplicador de visibilidad (Search Impression Share) de un hotel en los resultados de búsqueda.

## Impacto Matemático sobre el RevPAR Neto a Largo Plazo
Activar el Acelerador (ej. pagar un +5% extra de comisión por reserva) incrementa las reservas a corto plazo, aumentando la Tasa de Ocupación. Sin embargo, el **RevPAR Neto** (Revenue Per Available Room después de deducir comisiones y costos de distribución) puede disminuir a largo plazo si la tarifa promedio diaria (ADR) no se incrementa para compensar el alto costo de adquisición. Matemáticamente, el RevPAR bruto sube, pero el Net RevPAR baja si la elasticidad de la demanda no absorbe la sobrecomisión.

## Diferenciación del Algoritmo (Conversión Orgánica vs Pagada)
El algoritmo de clasificación de Expedia (Sort Algorithm) etiqueta estrictamente cada impresión y conversión.
* **Conversión Orgánica:** Mejora el "Quality Score" permanente del hotel. Expedia premia a los hoteles que convierten bien sin pagar extra, manteniéndolos en la primera página a largo plazo de forma gratuita.
* **Conversión Pagada (Visibility Booster):** El algoritmo etiqueta estas reservas bajo el flag `sponsored_boost`. Aunque generen ventas, **NO incrementan el Quality Score orgánico**. Cuando el hotel apaga el Booster, su ranking vuelve exactamente a la posición original, creando una dependencia artificial a las altas comisiones.
"""
    },
    {
        "filename": "airbnb_api_timeout.md",
        "content": """# Airbnb API Connectivity Guidelines para Channel Managers

La infraestructura de microservicios de Airbnb es sumamente estricta respecto al rendimiento y la disponibilidad de los Channel Managers de los hoteles (ej. SiteMinder, Cloudbeds).

## Latencia Superior a 3000 Milisegundos
El límite estricto de timeout (tiempo de espera máximo) para una respuesta de sincronización de disponibilidad o tarifas desde el Channel Manager es de **3000 milisegundos (3 segundos)**.

## Tasa de Desconexión y Códigos de Error
* Si la latencia supera los 3000 ms, la pasarela de Airbnb corta la conexión para proteger sus propios servidores.
* Esto genera un código de error interno **HTTP 504 Gateway Timeout**.
* **Tasa de Timeout (Timeout Rate):** Si la API registra más del 5% de errores 504 en una ventana de 1 hora, el algoritmo de Airbnb penaliza temporalmente la propiedad, reduciendo su visibilidad en el mapa y desactivando el Instant Book (Reserva Inmediata) por riesgo de overbooking, hasta que la conexión se estabilice por debajo de los 1000ms.
"""
    }
]

print("==================================================")
print(" LIFEXTREME EXAM SPIDER - GENERANDO KNOWLEDGE")
print("==================================================")

for doc in docs:
    file_path = PDF_DIR / doc["filename"]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(doc["content"])
    print(f"[+] Archivo generado: {doc['filename']}")

print("\n[+] El Spider ha finalizado.")
