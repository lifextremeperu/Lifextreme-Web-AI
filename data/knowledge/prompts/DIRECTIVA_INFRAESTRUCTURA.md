# Directiva de Inteligencia: Mapeo Nacional de Infraestructura de Aventura

**Estado:** Activo  
**Objetivo:** Identificar, estructurar y catalogar el 100% de la infraestructura física dedicada a los deportes de aventura y riesgo controlado en los 24 departamentos del Perú.
**Stack del Equipo:** Python, Pydantic, Scrapy/BeautifulSoup, APIs de Redes Sociales (Meta/Graph, TikTok), Google Places, MINCETUR Open Data.

---

## 1. Alcance de la Investigación (Open Discovery)

La misión de los agentes no es limitativa. Deben descubrir, registrar y clasificar **CUALQUIER tipo de infraestructura** diseñada para turismo de aventura y riesgo, incluyendo aquellas no previstas inicialmente. Entre las categorías principales (y ejemplos de infraestructura a buscar) se encuentran:

- **Escalada y Montañismo:** Palestras (indoor/outdoor), vías ferratas, muros de búlder.
- **Aire y Vértigo:** Circuitos de Skybikes (bicicletas en el aire), parques de cuerdas altas (Ropes courses), circuitos de Canopy/Zipline, plataformas de Bungee Jumping / Slingshot, puentes colgantes extremos.
- **Tierra:** Bike parks (Downhill/Cross Country), skateparks de nivel pro, circuitos de motocross/ATV, sandboard parks.
- **Agua:** Wakeparks (cableski), canales artificiales de canotaje/slalom.
- **Otros:** Cualquier instalación física emergente, parques temáticos de aventura extrema, columpios extremos, etc.

## 2. Fuentes de Extracción (Data Sources)

Los agentes de *scraping* deben ser programados para rastrear sistemáticamente las siguientes fuentes:

1. **Gubernamentales (Oficiales):**
   - Directorio Nacional de Prestadores de Servicios Turísticos (MINCETUR).
   - Registros de las DIRCETUR (Dirección Regional de Comercio Exterior y Turismo) de cada departamento.
2. **Redes Sociales (Discovery & Sentiment):**
   - **Instagram / TikTok:** Búsquedas por hashtags locales (ej. `#PalestrasLima`, `#ZiplineCusco`, `#BikeParkPeru`).
   - **Facebook:** Páginas de negocios y grupos locales de deportistas (ej. "Escaladores del Perú").
3. **Motores de Búsqueda y Mapas:**
   - **Google Maps / Places API:** Extracción de coordenadas, horarios, reviews y fotografías.
   - **Directorios especializados:** TripAdvisor, blogs de montañismo, foros de ciclismo.

---

## 3. Estructura de Datos (Pydantic Schemas)

El equipo de desarrollo debe implementar los siguientes esquemas en **Pydantic** para garantizar que los LLMs extraigan la información de manera estructurada y validada para la base de datos de Lifextreme.

```python
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import date

class GeoLocation(BaseModel):
    departamento: str = Field(..., description="Región o departamento del Perú (ej. Cusco, Lima, Áncash)")
    provincia: str
    distrito: str
    direccion_exacta: str
    latitud: float
    longitud: float

class Pricing(BaseModel):
    moneda: str = Field(default="PEN")
    precio_base: float
    incluye_equipo: bool = Field(..., description="¿El precio incluye alquiler de equipo de seguridad?")
    detalles_paquete: Optional[str]

class InfraestructuraAventura(BaseModel):
    id_infraestructura: str = Field(..., description="ID único generado para el registro")
    nombre_oficial: str
    tipo_categoria: str = Field(..., description="Ej. Palestra, Canopy, Bike Park, Via Ferrata")
    descripcion_corta: str
    
    # Geolocalización
    ubicacion: GeoLocation
    
    # Presencia Digital
    website: Optional[HttpUrl]
    instagram_url: Optional[HttpUrl]
    facebook_url: Optional[HttpUrl]
    google_maps_url: Optional[HttpUrl]
    
    # Operaciones y Seguridad
    operador_responsable: str = Field(..., description="Nombre de la empresa o entidad administradora")
    certificaciones_seguridad: List[str] = Field(default=[], description="Ej. ISO, MINCETUR, UIAA")
    estado_actual: str = Field(..., description="Activo, Mantenimiento, Cerrado, Proyecto")
    
    # Oferta
    precios: Optional[Pricing]
    nivel_dificultad: str = Field(..., description="Principiante, Intermedio, Avanzado, Pro")
    
    # Metadatos del Scraping
    fuentes_verificadas: List[HttpUrl]
    fecha_extraccion: date
```

---

## 4. Flujo de Ejecución del Pipeline (Instrucciones para los Agentes)

El pipeline de los agentes debe operar en 4 fases secuenciales:

### Fase 1: Discovery (Mapeo Amplio)
- **Agente Spider:** Itera por una lista de los 24 departamentos. Lanza queries combinadas (ej. `"palestra" OR "muro de escalada" OR "canopy" + "Arequipa"`) en Google Places y SERP (Search Engine Results Page).
- **Output Fase 1:** Lista cruda de URLs y nombres de posibles infraestructuras.

### Fase 2: Deep Scrape (Extracción de Contexto)
- **Agente Scraper:** Visita las URLs recopiladas en la Fase 1. Lee el DOM de páginas web, perfiles de Instagram (vía API/Instaloader) y extrae texto, descripciones, tarifas y comentarios recientes.

### Fase 3: Procesamiento LLM (Extracción Estructurada)
- **Agente Parser (LLM + Pydantic):** Recibe el texto crudo de la Fase 2 y utiliza herramientas de `function_calling` o `structured_outputs` forzando la respuesta a través del esquema `InfraestructuraAventura`.
- *Instrucción Crítica:* Si el agente no encuentra el precio o las certificaciones, debe marcar el campo como `null` o `[]`, no debe alucinar información.

### Fase 4: Validación y Consolidación (Vector Database)
- **Agente Validador:** Elimina duplicados (cruzando coordenadas y nombres similares).
- Si la infraestructura pertenece a una entidad del estado, se etiqueta el `operador_responsable` como "Estatal/Municipal".
- Inyección final de la metadata consolidada en Supabase (o ChromaDB) para ser consumida por la plataforma web de Lifextreme.

---

## 5. Notas de Seguridad y Ética de Scraping
> [!WARNING]  
> - **Rate Limiting:** Los scripts de Python deben usar delays (`time.sleep`) y rotación de proxies para evitar bloqueos por parte de Meta, Google y páginas gubernamentales.
> - **Datos Sensibles:** No extraer datos personales de instructores o guías a menos que estén listados públicamente como contacto comercial oficial.
> - **Veracidad:** Dar prioridad de confianza a la data de MINCETUR sobre la data de redes sociales en caso de conflicto sobre el estado legal del recinto.
