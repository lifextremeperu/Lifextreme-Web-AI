# 📊 CONFIGURACIÓN DE MONITOREO Y LOGS

## 🎯 Herramientas de Monitoreo Implementadas

### 1. **Netlify Analytics** (Incluido Gratis)
Ya está activo automáticamente en tu cuenta de Netlify.

**Qué Monitorea:**
- ✅ Tráfico en tiempo real
- ✅ Bandwidth usage
- ✅ Top pages
- ✅ Top sources
- ✅ 404 errors
- ✅ Unique visitors

**Cómo Acceder:**
1. Ve a: https://app.netlify.com
2. Selecciona tu sitio "lifextreme-v29-pro"
3. Click en "Analytics" en el menú lateral

---

### 2. **Error Tracking con Sentry** (Recomendado)

#### Configuración de Sentry:

**Paso 1: Crear Cuenta**
```
1. Ve a: https://sentry.io/signup/
2. Crea cuenta con: lifextremeperu@gmail.com
3. Crea nuevo proyecto:
   - Platform: JavaScript
   - Project name: lifextreme-web
```

**Paso 2: Obtener DSN**
Después de crear el proyecto, copia tu DSN (formato: https://xxxxx@sentry.io/xxxxx)

**Paso 3: Integrar en el Sitio**

Agrega este código en el `<head>` de `index.html`:

```html
<!-- Sentry Error Tracking -->
<script
  src="https://browser.sentry-cdn.com/7.91.0/bundle.min.js"
  integrity="sha384-xxxx"
  crossorigin="anonymous"
></script>

<script>
  Sentry.init({
    dsn: "TU_DSN_AQUI",
    integrations: [
      new Sentry.BrowserTracing(),
      new Sentry.Replay()
    ],
    
    // Performance Monitoring
    tracesSampleRate: 1.0,
    
    // Session Replay
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
    
    // Environment
    environment: "production",
    
    // Release tracking
    release: "lifextreme@1.0.0",
    
    // Configuración adicional
    beforeSend(event, hint) {
      // Filtrar errores de extensiones del navegador
      if (event.exception) {
        const error = event.exception.values[0];
        if (error.value && error.value.includes('chrome-extension://')) {
          return null;
        }
      }
      return event;
    }
  });
</script>
```

**Eventos Personalizados:**

```javascript
// Rastrear errores personalizados
try {
  // Tu código
} catch (error) {
  Sentry.captureException(error);
}

// Rastrear mensajes
Sentry.captureMessage('Algo importante sucedió', 'info');

// Rastrear breadcrumbs
Sentry.addBreadcrumb({
  category: 'booking',
  message: 'Usuario inició proceso de reserva',
  level: 'info'
});
```

---

### 3. **Uptime Monitoring** (Gratis)

#### Opción A: UptimeRobot (Recomendado)

**Configuración:**
```
1. Ve a: https://uptimerobot.com
2. Crea cuenta gratuita
3. Add New Monitor:
   - Monitor Type: HTTP(s)
   - Friendly Name: Lifextreme Web
   - URL: https://lifextreme-v29-pro.netlify.app
   - Monitoring Interval: 5 minutes
4. Alert Contacts: lifextremeperu@gmail.com
```

**Beneficios:**
- ✅ Monitoreo cada 5 minutos
- ✅ Alertas por email si el sitio cae
- ✅ Status page pública
- ✅ 50 monitores gratis

#### Opción B: Netlify Deploy Notifications

Ya configurado en `netlify.toml`. Recibirás emails cuando:
- ✅ Deploy exitoso
- ✅ Deploy fallido
- ✅ Build errors

---

### 4. **Performance Monitoring**

#### Google PageSpeed Insights

**Monitoreo Manual:**
```
1. Ve a: https://pagespeed.web.dev/
2. Ingresa: https://lifextreme-v29-pro.netlify.app
3. Analiza resultados
4. Implementa sugerencias
```

#### Lighthouse CI (Automático)

Ya configurado en `netlify.toml` con el plugin `@netlify/plugin-lighthouse`.

**Qué Hace:**
- ✅ Ejecuta Lighthouse en cada deploy
- ✅ Reporta métricas de performance
- ✅ Alerta si el score baja

**Ver Reportes:**
1. Ve a Netlify Dashboard
2. Click en un deploy
3. Busca "Lighthouse Report"

---

### 5. **Real User Monitoring (RUM)**

#### Web Vitals Tracking

Agrega este código en `index.html`:

```html
<script type="module">
  import {getCLS, getFID, getFCP, getLCP, getTTFB} from 'https://unpkg.com/web-vitals@3/dist/web-vitals.js?module';

  function sendToAnalytics(metric) {
    // Enviar a Google Analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', metric.name, {
        event_category: 'Web Vitals',
        event_label: metric.id,
        value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
        non_interaction: true,
      });
    }
    
    // Log en consola (desarrollo)
    console.log(metric);
  }

  getCLS(sendToAnalytics);
  getFID(sendToAnalytics);
  getFCP(sendToAnalytics);
  getLCP(sendToAnalytics);
  getTTFB(sendToAnalytics);
</script>
```

**Métricas Rastreadas:**
- **CLS** (Cumulative Layout Shift): Estabilidad visual
- **FID** (First Input Delay): Interactividad
- **FCP** (First Contentful Paint): Velocidad de carga
- **LCP** (Largest Contentful Paint): Rendimiento de carga
- **TTFB** (Time to First Byte): Tiempo de respuesta del servidor

---

## 📈 Dashboard de Monitoreo Centralizado

### Herramientas Recomendadas:

| Herramienta | Propósito | Costo | Prioridad |
|-------------|-----------|-------|-----------|
| **Netlify Analytics** | Tráfico y bandwidth | Gratis | 🔥 Alta |
| **Google Analytics** | Comportamiento usuarios | Gratis | 🔥 Alta |
| **Sentry** | Error tracking | Gratis (5k errors/mes) | ⭐ Media |
| **UptimeRobot** | Uptime monitoring | Gratis | ⭐ Media |
| **PageSpeed Insights** | Performance | Gratis | ⭐ Media |
| **Hotjar** | Heatmaps y grabaciones | $39/mes | 💡 Baja |

---

## 🚨 Configuración de Alertas

### Alertas Críticas (Email):
- ✅ Sitio caído (UptimeRobot)
- ✅ Deploy fallido (Netlify)
- ✅ Errores JavaScript críticos (Sentry)
- ✅ Performance score < 80 (Lighthouse)

### Alertas de Advertencia (Dashboard):
- ⚠️ Tráfico inusual
- ⚠️ 404 errors aumentando
- ⚠️ Tiempo de carga > 3s
- ⚠️ Tasa de rebote > 60%

---

## 📊 KPIs a Monitorear

### Performance:
- **Lighthouse Score**: > 90
- **Tiempo de Carga**: < 2s
- **Time to Interactive**: < 3s
- **First Contentful Paint**: < 1.5s

### Uptime:
- **Disponibilidad**: > 99.9%
- **Tiempo de respuesta**: < 500ms
- **SSL Certificate**: Válido

### Errores:
- **Error Rate**: < 1%
- **JavaScript Errors**: < 10/día
- **404 Errors**: < 5%

### Tráfico:
- **Usuarios únicos**: Crecimiento mensual
- **Páginas por sesión**: > 3
- **Tasa de rebote**: < 50%
- **Duración sesión**: > 2 min

---

## 🔧 Comandos Útiles

### Ver Logs de Netlify:
```bash
netlify logs
```

### Ver Status del Sitio:
```bash
netlify status
```

### Ver Funciones (si las usas):
```bash
netlify functions:list
```

---

## 📞 Contactos de Emergencia

**Si el sitio cae:**
1. Revisa Netlify Status: https://www.netlifystatus.com
2. Revisa logs: `netlify logs`
3. Rollback: Netlify Dashboard → Deploys → Deploy anterior → "Publish deploy"

**Si hay errores críticos:**
1. Revisa Sentry Dashboard
2. Identifica el error
3. Haz hotfix
4. Deploy con: `.\deploy.ps1 "hotfix: Descripción"`

---

## ✅ Checklist de Configuración

- [ ] Netlify Analytics activado
- [ ] Google Analytics configurado
- [ ] Sentry cuenta creada
- [ ] Sentry DSN integrado
- [ ] UptimeRobot monitor creado
- [ ] Alertas de email configuradas
- [ ] Web Vitals tracking agregado
- [ ] Lighthouse CI verificado

---

**Última actualización:** 06 Enero 2026  
**Proyecto:** Lifextreme Web AI  
**Estado:** 🟢 Configuración Lista
