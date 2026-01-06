# 🚀 Funcionalidad "Invitar a un Amigo" - Lifextreme

## 📋 Descripción General

Se ha implementado una funcionalidad completa de **"Invitar a un Amigo"** que permite a los usuarios compartir actividades específicas (tours y eventos) con sus contactos mediante WhatsApp, incluyendo un link directo a la página de reserva.

## ✨ Características Principales

### 1. **Compartir por WhatsApp**
- Botón flotante en cada tarjeta de tour y evento
- Mensaje personalizado con detalles de la actividad
- Link directo que abre automáticamente la actividad compartida
- Integración nativa con WhatsApp Web y App móvil

### 2. **Copiar Link Directo**
- Botón adicional para copiar el link al portapapeles
- Notificación de confirmación cuando se copia exitosamente
- Fallback para navegadores antiguos

### 3. **Deep Linking Automático**
- Los links compartidos incluyen parámetros únicos (`?activity=tour&id=1&ref=share`)
- Al abrir el link, la página automáticamente:
  - Navega a la sección correcta (Destinos o Eventos)
  - Abre el modal de reserva de la actividad específica
  - Muestra una notificación de bienvenida

## 🎨 Diseño de UI

### Botones de Compartir
- **Botón WhatsApp**: Aparece al hacer hover sobre las tarjetas
- **Botón Copiar Link**: Ícono de link en la esquina superior de cada tarjeta
- **Estilo**: Gradiente verde de WhatsApp con animaciones suaves
- **Responsive**: Funciona perfectamente en móvil y desktop

### Notificaciones
- Toast notifications elegantes
- Animaciones de entrada y salida
- Auto-dismiss después de 3 segundos

## 📁 Archivos Modificados/Creados

### Nuevos Archivos:
1. **`js/share-engine.js`** - Motor principal de compartir
   - Generación de links con parámetros
   - Mensajes personalizados de WhatsApp
   - Manejo de deep links entrantes
   - Sistema de notificaciones

### Archivos Modificados:
1. **`css/styles.css`** - Estilos para botones de compartir
2. **`index.html`** - Inclusión del script share-engine.js
3. **`js/app.js`** - Integración de botones en tarjetas

## 🔧 Cómo Funciona

### Flujo de Usuario 1: Compartir por WhatsApp

```
1. Usuario hace hover sobre una tarjeta de tour/evento
2. Aparece el botón de WhatsApp (verde)
3. Usuario hace clic en el botón
4. Se abre WhatsApp con mensaje pre-cargado:
   
   🏔️ ¡Mira esta increíble expedición!
   
   📍 Inca Trail 4D
   🌎 Cusco
   ⏱️ Duración: 4 días
   💰 Desde S/ 2450
   
   ✨ ¿Te animas a esta aventura conmigo?
   
   👉 Reserva aquí: http://localhost:8080?activity=tour&id=1&ref=share
   
   Compartido desde Lifextreme - Tu plataforma de aventuras extremas

5. Usuario envía el mensaje a su contacto
```

### Flujo de Usuario 2: Recibir Invitación

```
1. Usuario 2 recibe el mensaje de WhatsApp
2. Hace clic en el link
3. La página se abre y automáticamente:
   - Detecta los parámetros URL
   - Navega a la sección "Destinos"
   - Abre el modal de reserva del tour específico
   - Muestra: "🎉 ¡Tu amigo te invitó a esta aventura!"
4. Usuario 2 puede proceder directamente a reservar
```

### Flujo de Usuario 3: Copiar Link

```
1. Usuario hace clic en el ícono de link
2. El link se copia al portapapeles
3. Aparece notificación: "✅ Link copiado al portapapeles"
4. Usuario puede pegar el link donde desee
```

## 💻 Código de Ejemplo

### Compartir una Actividad Manualmente

```javascript
// Compartir un tour
window.ShareEngine.shareViaWhatsApp({
    id: 1,
    title: 'Inca Trail 4D',
    dept: 'Cusco',
    duration: '4 días',
    price: 2450
}, 'tour');

// Compartir un evento
window.ShareEngine.shareViaWhatsApp({
    id: 10,
    title: 'Maratón de Montaña',
    dept: 'Huaraz',
    date: '15 Marzo',
    price: 180
}, 'event');
```

### Copiar Link al Portapapeles

```javascript
// Copiar link de tour
await window.ShareEngine.copyLinkToClipboard('tour', 1);

// Copiar link de evento
await window.ShareEngine.copyLinkToClipboard('event', 10);
```

### Generar Link Personalizado

```javascript
const link = window.ShareEngine.generateActivityLink('tour', 1);
console.log(link); 
// Output: http://localhost:8080?activity=tour&id=1&ref=share
```

## 📊 Tracking y Analytics

El sistema incluye hooks para tracking de eventos:

```javascript
// En share-engine.js
function trackShareEvent(activity, type) {
    if (window.gtag) {
        window.gtag('event', 'share', {
            event_category: 'engagement',
            event_label: `${type}_${activity.id}`,
            value: activity.title
        });
    }
}
```

Puedes integrar con:
- Google Analytics
- Facebook Pixel
- Mixpanel
- Cualquier otra plataforma de analytics

## 🎯 Beneficios para el Negocio

1. **Marketing Viral**: Los usuarios se convierten en embajadores de marca
2. **Reducción de Fricción**: Link directo a la actividad = más conversiones
3. **Tracking**: Saber qué actividades se comparten más
4. **Social Proof**: Las recomendaciones de amigos tienen mayor tasa de conversión
5. **Crecimiento Orgánico**: Adquisición de usuarios sin costo publicitario

## 🔮 Mejoras Futuras Posibles

1. **Programa de Referidos**: Dar descuentos al usuario que comparte
2. **Compartir en Otras Redes**: Facebook, Instagram, Twitter
3. **Códigos de Descuento Personalizados**: Cada link con código único
4. **Dashboard de Compartidos**: Ver estadísticas de qué se comparte más
5. **Gamificación**: Badges por compartir X cantidad de actividades

## 🚀 Cómo Probar

1. Abre el proyecto en: `http://localhost:8080`
2. Navega a "Destinos" o "Eventos"
3. Haz hover sobre cualquier tarjeta
4. Verás aparecer el botón verde de WhatsApp
5. Haz clic y se abrirá WhatsApp con el mensaje
6. También puedes hacer clic en el ícono de link para copiar

## 📱 Compatibilidad

- ✅ Chrome/Edge (Desktop y Mobile)
- ✅ Firefox (Desktop y Mobile)
- ✅ Safari (Desktop y Mobile)
- ✅ WhatsApp Web
- ✅ WhatsApp Mobile App
- ✅ Navegadores antiguos (con fallback para copiar)

## 🎨 Personalización

### Cambiar el Mensaje de WhatsApp

Edita la función `generateWhatsAppMessage` en `js/share-engine.js`:

```javascript
function generateWhatsAppMessage(activity, type) {
    // Personaliza el mensaje aquí
    let message = `¡Hola! Te recomiendo esta aventura...`;
    // ...
    return encodeURIComponent(message);
}
```

### Cambiar Estilos de Botones

Edita los estilos en `css/styles.css`:

```css
.share-btn-compact {
    /* Personaliza colores, tamaños, etc. */
    background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
}
```

## 🐛 Solución de Problemas

### El botón no aparece
- Verifica que `share-engine.js` esté cargado
- Revisa la consola del navegador por errores
- Asegúrate de que las tarjetas tengan la clase `card`, `tour-card` o `event-card`

### WhatsApp no se abre
- Verifica que el usuario tenga WhatsApp instalado
- En desktop, debe tener WhatsApp Web configurado
- El navegador puede bloquear pop-ups (permitir en configuración)

### El link no funciona
- Verifica que el servidor esté corriendo
- Asegúrate de que los parámetros URL sean correctos
- Revisa que `handleIncomingShare()` se esté ejecutando

## 📞 Soporte

Para cualquier duda o problema con esta funcionalidad, contacta al equipo de desarrollo.

---

**Desarrollado con ❤️ para Lifextreme**
**Fecha: Enero 2026**
