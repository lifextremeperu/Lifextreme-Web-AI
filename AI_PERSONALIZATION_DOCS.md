# 🤖 LIFEXTREME AI PERSONALIZATION ENGINE
## Sistema Completo de Personalización con Inteligencia Artificial

---

## 📋 ÍNDICE
1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Flujo de Personalización](#flujo-de-personalización)
4. [Datos Capturados](#datos-capturados)
5. [Algoritmos de IA](#algoritmos-de-ia)
6. [Casos de Uso](#casos-de-uso)
7. [Integración con Backend](#integración-con-backend)

---

## 🎯 VISIÓN GENERAL

El **AI Personalization Engine** de Lifextreme es un sistema inteligente que:

- ✅ **Conoce al usuario** a nivel psicográfico y comportamental
- ✅ **Predice preferencias** antes de que el usuario las exprese
- ✅ **Adapta toda la experiencia** (contenido, precios, mensajes, recomendaciones)
- ✅ **Aprende continuamente** del comportamiento del usuario
- ✅ **Maximiza conversiones** mostrando lo más relevante

---

## 🏗️ ARQUITECTURA DEL SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO INGRESA                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│          FORMULARIO DE PERFIL AI (Modal)                     │
│  • Información Personal                                      │
│  • Perfil de Aventurero                                      │
│  • Preferencias de Experiencia                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         AI PERSONALIZATION ENGINE (ai-engine.js)             │
│                                                               │
│  1. loadUserProfile()      → Carga perfil de localStorage    │
│  2. activatePersonalization() → Activa 5 módulos:            │
│     ├─ personalizeHeroSection()                              │
│     ├─ generateSmartRecommendations()                        │
│     ├─ applyDynamicPricing()                                 │
│     ├─ personalizeMessaging()                                │
│     └─ filterRelevantContent()                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              EXPERIENCIA PERSONALIZADA                        │
│  • Hero adaptado al nivel de experiencia                     │
│  • Top 3 tours recomendados (scoring IA)                     │
│  • Precios dinámicos con descuentos inteligentes             │
│  • Mensajes del chatbot personalizados                       │
│  • Contenido filtrado por relevancia                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 FLUJO DE PERSONALIZACIÓN

### **PASO 1: Captura de Datos**
```javascript
// Usuario completa formulario → submitAIProfile()
const userProfile = {
    personal: { fullName, email, age, phone },
    adventure: { experienceLevel, interests[], budget, travelFrequency },
    preferences: { groupType, regions[], motivation }
}
```

### **PASO 2: Almacenamiento**
```javascript
// Guardado en localStorage
localStorage.setItem('lifextreme_ai_profile', JSON.stringify(userProfile));
```

### **PASO 3: Activación del Motor IA**
```javascript
// Al cargar la página
window.AIEngine = new AIPersonalizationEngine();
// → Detecta perfil → Activa personalización
```

### **PASO 4: Personalización Activa**
El motor ejecuta 5 módulos simultáneamente:

#### **Módulo 1: Hero Section Personalizado**
```javascript
// Cambia título y descripción según experiencia
experienceLevel: "beginner" → "Inicia tu Aventura"
experienceLevel: "expert" → "Territorio Elite"
```

#### **Módulo 2: Recomendaciones Inteligentes**
```javascript
// Algoritmo de scoring (0-100 puntos)
+30 pts → Coincide con región de interés
+25 pts → Nivel de dificultad apropiado
+20 pts → Intereses (keywords en título/descripción)
+15 pts → Presupuesto compatible
+10 pts → Tipo de grupo adecuado
```

#### **Módulo 3: Precios Dinámicos**
```javascript
// Descuentos por frecuencia de viaje
monthly: 15% descuento
quarterly: 10% descuento
biannual: 5% descuento
annual: 3% descuento
```

#### **Módulo 4: Mensajes Personalizados**
```javascript
// Chatbot adapta respuestas según motivación
motivation.includes('desconectar') → "Rutas de bienestar en selva"
motivation.includes('límites') → "Rutas extremas"
motivation.includes('naturaleza') → "Opciones eco-friendly"
```

#### **Módulo 5: Filtrado de Contenido**
```javascript
// Auto-filtrado inteligente
- Región preferida se aplica automáticamente
- Tours no aptos para nivel se ocultan
- Eventos irrelevantes se filtran
```

---

## 📊 DATOS CAPTURADOS

### **1. Información Personal**
| Campo | Tipo | Uso IA |
|-------|------|--------|
| `fullName` | String | Personalización de mensajes |
| `email` | String | Segmentación de campañas |
| `age` | Number | Filtrado de tours aptos |
| `phone` | String | Comunicación directa |

### **2. Perfil de Aventurero**
| Campo | Tipo | Uso IA |
|-------|------|--------|
| `experienceLevel` | Enum | Filtrado de dificultad |
| `interests[]` | Array | Scoring de recomendaciones |
| `budget` | Enum | Filtrado de precios |
| `travelFrequency` | Enum | Descuentos dinámicos |

### **3. Preferencias de Experiencia**
| Campo | Tipo | Uso IA |
|-------|------|--------|
| `groupType` | Enum | Recomendación de tours grupales |
| `regions[]` | Array | Auto-filtrado geográfico |
| `motivation` | Text | Análisis de sentimiento |

---

## 🧠 ALGORITMOS DE IA

### **Algoritmo de Scoring de Tours**
```javascript
function calculateTourScore(tour, userProfile) {
    let score = 0;
    
    // 1. Región (30 puntos)
    if (userProfile.preferences.regions.includes(tour.dept.toLowerCase())) {
        score += 30;
    }
    
    // 2. Dificultad (25 puntos)
    const difficultyMatch = {
        beginner: ['Baja', 'Media'],
        intermediate: ['Media', 'Alta'],
        advanced: ['Alta', 'Extrema'],
        expert: ['Extrema']
    };
    if (difficultyMatch[userProfile.adventure.experienceLevel].includes(tour.difficulty)) {
        score += 25;
    }
    
    // 3. Intereses (20 puntos por match)
    userProfile.adventure.interests.forEach(interest => {
        const keywords = {
            trekking: ['trek', 'camino', 'caminata'],
            climbing: ['escalada', 'climbing'],
            jungle: ['selva', 'jungle', 'amazonas'],
            // ... más keywords
        };
        
        const searchText = (tour.title + tour.detail).toLowerCase();
        keywords[interest]?.forEach(keyword => {
            if (searchText.includes(keyword)) score += 20;
        });
    });
    
    // 4. Presupuesto (15 puntos)
    const budgetRanges = {
        budget: [0, 1000],
        moderate: [1000, 2500],
        premium: [2500, 5000],
        luxury: [5000, Infinity]
    };
    const [min, max] = budgetRanges[userProfile.adventure.budget];
    if (tour.price >= min && tour.price <= max) {
        score += 15;
    }
    
    // 5. Tipo de grupo (10 puntos)
    if (userProfile.preferences.groupType === 'family' && tour.difficulty === 'Baja') {
        score += 10;
    }
    
    return score; // Máximo: 100 puntos
}
```

### **Generación de Persona**
```javascript
function generatePersona(userProfile) {
    const { experienceLevel } = userProfile.adventure;
    const { groupType } = userProfile.preferences;
    
    const personas = {
        'beginner-family': '👨‍👩‍👧 Familia Exploradora',
        'beginner-solo': '🎒 Aventurero Novato',
        'intermediate-friends': '🤝 Grupo de Amigos Activos',
        'advanced-solo': '⛰️ Montañista Solitario',
        'expert-solo': '🏔️ Alpinista Elite',
        'expert-couple': '💑 Pareja Extrema'
    };
    
    return personas[`${experienceLevel}-${groupType}`] || '🌟 Aventurero Único';
}
```

---

## 💡 CASOS DE USO

### **Caso 1: Usuario Principiante con Familia**
```javascript
// Perfil
{
    experienceLevel: 'beginner',
    groupType: 'family',
    budget: 'moderate',
    regions: ['cusco']
}

// Resultado IA
- Hero: "Inicia tu Aventura en Familia"
- Recomendaciones: Tours de baja dificultad en Cusco
- Precios: Descuentos familiares destacados
- Mensajes: "Rutas seguras para niños"
```

### **Caso 2: Experto Solitario Buscando Extremo**
```javascript
// Perfil
{
    experienceLevel: 'expert',
    groupType: 'solo',
    budget: 'luxury',
    interests: ['climbing', 'trekking'],
    motivation: 'superar mis límites'
}

// Resultado IA
- Hero: "Territorio Elite - Conquista lo Imposible"
- Recomendaciones: Rutas técnicas de escalada extrema
- Precios: Paquetes premium con guías privados
- Mensajes: "Desafíos dignos de tu experiencia"
```

### **Caso 3: Viajero Frecuente Económico**
```javascript
// Perfil
{
    travelFrequency: 'monthly',
    budget: 'budget',
    interests: ['camping', 'trekking']
}

// Resultado IA
- Descuento: 15% automático en todos los tours
- Recomendaciones: Tours económicos con camping
- Mensajes: "Programa de fidelidad activado"
```

---

## 🔌 INTEGRACIÓN CON BACKEND

### **Endpoint Recomendado**
```javascript
// POST /api/ai-profile
{
    "userId": "generated-uuid",
    "profile": { /* userProfile object */ },
    "timestamp": "2026-01-05T16:00:00Z"
}
```

### **Respuesta del Backend**
```javascript
{
    "status": "success",
    "recommendations": [
        { "tourId": 1, "score": 95, "reason": "Perfect match for your experience level" },
        { "tourId": 5, "score": 88, "reason": "Matches your budget and interests" }
    ],
    "dynamicDiscount": 0.15,
    "personalizedMessage": "¡Hola Carlos! Tenemos 12 aventuras perfectas para ti."
}
```

### **Implementación en Frontend**
```javascript
// En ai-personalization.js (línea 63)
async function submitAIProfile(formData) {
    const userProfile = { /* ... */ };
    
    // Enviar a backend
    try {
        const response = await fetch('/api/ai-profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userProfile)
        });
        
        const data = await response.json();
        
        // Aplicar recomendaciones del backend
        if (data.recommendations) {
            window.AIEngine.recommendations = data.recommendations;
        }
    } catch (error) {
        console.error('Error enviando perfil a backend:', error);
    }
}
```

---

## 🎯 MÉTRICAS DE ÉXITO

### **KPIs a Medir**
1. **Tasa de Conversión**: % usuarios que completan perfil → reservan
2. **Engagement**: Tiempo en sitio después de personalización
3. **Precisión IA**: % de recomendaciones que resultan en reserva
4. **Satisfacción**: NPS de usuarios con perfil vs sin perfil

### **Debugging en Consola**
```javascript
// Ver perfil del usuario
console.log(window.AIEngine.userProfile);

// Ver recomendaciones
console.log(window.AIEngine.recommendations);

// Ver insights completos
console.log(window.getAIInsights());
```

---

## 🚀 PRÓXIMOS PASOS

1. **Machine Learning Backend**: Entrenar modelo con datos reales
2. **A/B Testing**: Comparar conversiones con/sin IA
3. **Análisis de Sentimiento**: Procesar campo "motivación" con NLP
4. **Predicción de Churn**: Detectar usuarios en riesgo
5. **Recomendaciones Colaborativas**: "Usuarios como tú también reservaron..."

---

## 📞 SOPORTE

Para más información sobre el AI Engine:
- **Archivo**: `js/ai-engine.js`
- **Debugging**: Abre consola y ejecuta `window.getAIInsights()`
- **Documentación**: Este archivo

---

**Lifextreme AI Personalization Engine v1.0**  
*Transformando aventureros en experiencias únicas* 🏔️🤖
