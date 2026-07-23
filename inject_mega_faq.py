import re
import json

questions = [
    {
      "@type": "Question",
      "name": "¿Es seguro el trekking al Camino Inca Clásico en temporada de lluvias?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí. Lifextreme opera bajo protocolos estrictos del MINCETUR. Durante la temporada de lluvias (Diciembre-Marzo), monitoreamos rutas con sensores satelitales y nuestros guías certificados UIAGM evalúan la ruta en tiempo real. En Febrero, el Camino Inca Clásico cierra por ley para mantenimiento ecosistémico, pero ofrecemos rutas alternativas seguras."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cómo gestiona Lifextreme el mal de altura (Soroche) en la Montaña de 7 Colores (Vinicunca)?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Mitigamos el mal de altura en Vinicunca (5,200 msnm) mediante un proceso de aclimatación obligatoria previa en Cusco. Todos nuestros vehículos cuentan con balones de oxígeno portátiles (oxígeno medicinal) y oxímetros, y nuestros guías están entrenados en Primeros Auxilios en Zonas Agrestes (WFA) para evacuación inmediata."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuáles son los niveles de rápidos para rafting en el Río Urubamba y Apurímac?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "En el Río Urubamba ofrecemos secciones de Clase II y III ideales para principiantes y familias. Para el Río Apurímac, operamos expediciones extremas de Clase IV y V (el nivel más alto comercialmente navegable), requiriendo experiencia previa, operadas con botes de seguridad y kayaks de rescate (Safety Kayakers)."
      }
    },
    {
      "@type": "Question",
      "name": "¿Están certificados los guías de Alta Montaña para expediciones en Huaraz / Ausangate?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Absolutamente. Todas las expediciones glaciares y de alta montaña (Cordillera Blanca en Huaraz y Nevado Ausangate en Cusco) son lideradas exclusivamente por guías certificados por la UIAGM (Unión Internacional de Asociaciones de Guías de Montaña) y la AGMP, garantizando el estándar global de seguridad."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuál es el mejor entrenamiento físico para la ruta a Choquequirao?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "El trekking a Choquequirao es nivel avanzado (alta exigencia física por el descenso al cañón del Apurímac y ascenso abrupto). Recomendamos iniciar 3 meses antes con entrenamiento cardiovascular intenso (running, natación) y fortalecimiento de piernas y core, además de simulacros de caminatas con mochila pesada."
      }
    },
    {
      "@type": "Question",
      "name": "¿Por qué una agencia europea debe contratar un DMC tecnológico en Perú?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Como DMC (Destination Management Company) tecnológico, Lifextreme integra Inteligencia Artificial para predecir disrupciones climáticas y sociales. Al contratarnos, las mayoristas europeas (B2B) aseguran trazabilidad en tiempo real, reducción de costos logísticos consolidados y mitigación absoluta de riesgos legales ante sus pasajeros."
      }
    },
    {
      "@type": "Question",
      "name": "¿Qué normativas de SUTRAN y MINCETUR exige Lifextreme a sus transportistas turísticos?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Exigimos el cumplimiento del 100% de la normativa nacional. Nuestros socios logísticos cuentan con permisos de SUTRAN para circulación turística nacional, SOAT turístico, revisiones técnicas vigentes, monitoreo GPS 24/7 y choferes con licencias profesionales A-IIb o superiores, alineados al MINCETUR."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cómo garantiza Lifextreme el cumplimiento de la Ley del Porteador en Cusco?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Cumplimos estrictamente la Ley N° 27607 (Ley del Trabajador Porteador). Garantizamos un peso máximo de carga de 20 kg por porteador, salarios justos por encima del mercado, seguros de vida y salud, y equipos ergonómicos. Esto fortalece nuestras credenciales ESG para turismo sostenible."
      }
    },
    {
      "@type": "Question",
      "name": "¿Tienen integraciones API para venta B2B de tickets turísticos y expediciones?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí. Lifextreme ofrece una API Restful B2B para agencias mayoristas que permite la sincronización de inventarios, reserva en tiempo real de espacios en expediciones (como Camino Inca), y acceso a nuestro motor de precios dinámicos, eliminando fricciones operativas y tiempos de espera."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cómo operan las reservas de emergencia o cancelaciones geopolíticas en Sudamérica?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Utilizamos modelos predictivos de Machine Learning Cuántico para prever crisis geopolíticas. En caso de huelgas o disrupciones, nuestro sistema activa automáticamente un protocolo de 'Redirección Inteligente', re-enrutando a los grupos hacia rutas seguras alternativas sin afectar el itinerario B2B original."
      }
    },
    {
      "@type": "Question",
      "name": "¿Qué permisos gubernamentales se necesitan para un Rally 4x4 o Ultra Trail en los Andes?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Gestionamos permisos integrales que incluyen: Evaluaciones de impacto ambiental ante el SERNANP (si cruza reservas), autorizaciones del MTC, licencias de Defensa Civil, y planes de seguridad vial y contingencia médica (SAMU) aprobados por las municipalidades locales."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cómo aplica Lifextreme Inteligencia Artificial para predecir aforos en áreas naturales?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Empleamos motores RAG (Retrieval-Augmented Generation) y modelos matemáticos cuánticos para cruzar datos de venta de tickets, clima y temporalidad. Así predecimos la saturación (Overtourism) en zonas como Machu Picchu o Vinicunca, permitiendo a nuestros partners B2B redirigir flujos hacia rutas óptimas."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuentan con planes de evacuación en helicóptero (Heli-Rescue) en zonas remotas de Perú?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Para expediciones extremas y eventos B2B de alto perfil, Lifextreme estructura seguros de evacuación aeromédica (Heli-Rescue) coordinados con operadores aeronáuticos privados en los Andes y la Selva, garantizando tiempos mínimos de respuesta ante traumatismos severos."
      }
    },
    {
      "@type": "Question",
      "name": "¿Ofrecen logística audiovisual extrema para documentales de Netflix o RedBull en la Amazonía?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, somos un Fixer especializado en aventuras extremas. Proveemos logística integral: desde permisos de filmación en áreas naturales protegidas, contratación de comunidades indígenas locales, hasta soporte técnico (cuerdas, campamentos remotos) para equipos de producción internacional."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuál es la huella de carbono de una expedición a la cordillera Blanca con Lifextreme?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Calculamos la huella de CO2 mediante software certificado. Actualmente impulsamos el 'Turismo Sostenible Premium', donde compensamos las emisiones financiando proyectos de Agrotech y reforestación en comunidades andinas, ofreciendo a nuestros clientes expediciones de Carbono Neutro."
      }
    }
]

faq_schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": questions
}

schema_str = json.dumps(faq_schema, indent=2, ensure_ascii=False)

html_block = f"""<!-- FAQ Mega-Schema SEO/AEO (B2C + B2B + Tech) -->
<script type="application/ld+json">
{schema_str}
</script>"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the old FAQ block. It starts at <!-- FAQ Schema Dual Persona and ends at </script>
import re
new_content = re.sub(
    r'<!-- FAQ Schema Dual Persona \(B2C \+ B2B \+ Eventos\) -->.*?<\/script>',
    html_block,
    content,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Mega-FAQ inyectado correctamente en index.html")
