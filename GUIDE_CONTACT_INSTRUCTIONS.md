# Instrucciones: Conectar Botones "CONTRATAR" al Formulario de Guías

## ✅ Modal de Contacto Implementado

Se ha agregado un formulario completo de contacto para guías en `index.html`. Este modal incluye:

- **Información Personal**: Nombre, WhatsApp, Email
- **Detalles del Servicio**: 
  - Tipo de actividad (Trekking, Escalada, Montañismo, etc.)
  - Destino/Ruta
  - Fecha preferida
  - Duración en días
  - Número de personas
  - Nivel de experiencia (Principiante, Intermedio, Avanzado)
  - Requerimientos especiales

Al enviar el formulario, se genera automáticamente un mensaje de WhatsApp con todos los detalles y se abre la conversación con Lifextreme.

---

## 🔧 Cómo Conectar los Botones "CONTRATAR"

### Opción 1: Botones en HTML Estático

Si tienes botones "CONTRATAR" en tu HTML, actualízalos así:

```html
<button onclick="openGuideContactModal('Carlos El Puma Mamani', 'ALTA MONTAÑA', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200')"
    class="bg-slate-900 text-white px-6 py-3 rounded-xl font-black uppercase tracking-widest hover:bg-slate-800 transition-all">
    <i class="ri-user-add-line mr-2"></i> CONTRATAR
</button>
```

**Parámetros de la función:**
1. `guideName`: Nombre completo del guía
2. `guideSpecialty`: Especialidad (ej: "TREKKING & FLORA", "ALTA MONTAÑA")
3. `guideAvatar`: URL de la foto del guía

### Opción 2: Botones Generados Dinámicamente con JavaScript

Si generas las tarjetas de guías con JavaScript (como en `cms-service.js`), actualiza el código así:

```javascript
// Ejemplo de renderizado de tarjeta de guía
function renderGuideCard(guide) {
    return `
        <div class="guide-card bg-white rounded-3xl p-6 shadow-xl">
            <img src="${guide.avatar}" alt="${guide.name}" class="w-24 h-24 rounded-full mx-auto mb-4">
            <h3 class="text-xl font-black text-center mb-2">${guide.name}</h3>
            <p class="text-xs text-slate-500 uppercase tracking-widest text-center mb-4">${guide.specialty}</p>
            
            <button onclick="openGuideContactModal('${guide.name}', '${guide.specialty}', '${guide.avatar}')"
                class="w-full bg-slate-900 text-white px-6 py-3 rounded-xl font-black uppercase tracking-widest hover:bg-slate-800 transition-all flex items-center justify-center gap-2">
                <i class="ri-user-add-line"></i> CONTRATAR
            </button>
        </div>
    `;
}
```

### Opción 3: Desde el archivo `js/cms-service.js`

Si usas el servicio CMS para cargar guías desde `guides-cms.json`, actualiza la función de renderizado:

```javascript
// En cms-service.js o donde renderizan las tarjetas
guides.forEach(guide => {
    const card = document.createElement('div');
    card.innerHTML = `
        <!-- ... contenido de la tarjeta ... -->
        <button onclick="openGuideContactModal('${guide.name}', '${guide.specialty}', '${guide.photo}')"
            class="contratar-btn">
            CONTRATAR →
        </button>
    `;
    guidesContainer.appendChild(card);
});
```

---

## 📝 Ejemplo Completo de Tarjeta de Guía

```html
<div class="guide-card bg-white rounded-3xl p-8 shadow-2xl border border-slate-100">
    <!-- Avatar -->
    <div class="relative w-32 h-32 mx-auto mb-6">
        <img src="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200" 
             alt="Carlos Mamani" 
             class="w-full h-full rounded-full object-cover border-4 border-primary/20">
        <div class="absolute -bottom-2 -right-2 bg-emerald-500 text-white text-xs font-black px-3 py-1 rounded-full">
            ⭐ 4.9
        </div>
    </div>

    <!-- Info -->
    <h3 class="text-2xl font-black italic text-center mb-2">Carlos "El Puma" Mamani</h3>
    <p class="text-xs text-slate-500 uppercase tracking-widest text-center mb-1">ALTA MONTAÑA</p>
    
    <!-- Badges -->
    <div class="flex justify-center gap-2 mb-6">
        <span class="bg-slate-100 text-slate-600 px-3 py-1 rounded-lg text-[10px] font-bold">ESP</span>
        <span class="bg-slate-100 text-slate-600 px-3 py-1 rounded-lg text-[10px] font-bold">QUE</span>
        <span class="bg-slate-100 text-slate-600 px-3 py-1 rounded-lg text-[10px] font-bold">ING</span>
    </div>

    <!-- Description -->
    <p class="text-sm text-slate-600 text-center mb-6 leading-relaxed">
        Especialista en rutas de más de 5000msnm. Certificado UIAGM.
    </p>

    <!-- CTA Button -->
    <button onclick="openGuideContactModal('Carlos El Puma Mamani', 'ALTA MONTAÑA', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200')"
        class="w-full bg-slate-900 text-white px-8 py-4 rounded-2xl font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl shadow-slate-900/20 flex items-center justify-center gap-3 group">
        <i class="ri-user-add-line text-xl"></i>
        <span>CONTRATAR</span>
        <i class="ri-arrow-right-line text-xl group-hover:translate-x-1 transition-transform"></i>
    </button>
</div>
```

---

## 🎯 Datos de Ejemplo para Probar

```javascript
// Ejemplo 1
openGuideContactModal(
    'Carlos "El Puma" Mamani',
    'ALTA MONTAÑA',
    'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200'
);

// Ejemplo 2
openGuideContactModal(
    'Sarah "La Lince" Jenkins',
    'TREKKING & FLORA',
    'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200'
);

// Ejemplo 3
openGuideContactModal(
    'Marco "Cóndor" Quispe',
    'CULTURA INCA',
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200'
);
```

---

## ✨ Funcionalidades del Modal

1. **Validación de Formulario**: Todos los campos requeridos están marcados
2. **Animaciones Suaves**: Transiciones fluidas al abrir/cerrar
3. **Responsive**: Funciona perfectamente en móvil y desktop
4. **Cierre Múltiple**: 
   - Botón X
   - Tecla ESC
   - Click fuera del modal
5. **WhatsApp Integration**: Genera mensaje formateado automáticamente
6. **Estados Visuales**: Loading, Success, Error

---

## 🔄 Flujo de Usuario

1. Cliente hace click en "CONTRATAR" en la tarjeta del guía
2. Se abre el modal con la información del guía seleccionado
3. Cliente completa el formulario con sus datos y requerimientos
4. Al enviar, se genera un mensaje de WhatsApp con toda la información
5. Se abre WhatsApp con el mensaje pre-llenado
6. El equipo de Lifextreme recibe la solicitud y contacta al cliente

---

## 📱 Mensaje de WhatsApp Generado

El formulario genera automáticamente un mensaje estructurado como este:

```
🏔️ *SOLICITUD DE GUÍA*

👤 *Cliente:* Juan Pérez
📱 *WhatsApp:* +51 999 999 999
📧 *Email:* juan@email.com

🎯 *Guía Solicitado:* Carlos El Puma Mamani
⚡ *Especialidad:* ALTA MONTAÑA

📋 *DETALLES DEL SERVICIO:*
🏃 Actividad: Montañismo / Alta Montaña
📍 Destino: Huascarán
📅 Fecha: 2026-02-15
⏱️ Duración: 5 día(s)
👥 Personas: 4
📊 Nivel: intermedio

💬 *Comentarios:*
Necesitamos equipo de camping y tenemos experiencia previa en montañas de 4000m
```

---

## 🚀 Próximos Pasos

1. **Actualizar tus tarjetas de guías** con el `onclick` handler
2. **Probar el modal** haciendo click en cualquier botón CONTRATAR
3. **Verificar** que el mensaje de WhatsApp se genera correctamente
4. **(Opcional)** Personalizar los estilos del modal si es necesario

¡El sistema está listo para recibir solicitudes de clientes! 🎉
