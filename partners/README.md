# LifExtreme Partners Platform

**Plataforma completa para operadores de turismo de aventura**

🚀 **Versión Final - 6 de Enero 2026**

---

## 🌐 Demo en Vivo

**URL:** [Próximamente - Desplegando en Netlify]

---

## 📋 Descripción

LifExtreme Partners es una plataforma integral que permite a operadores de turismo de aventura:

- ✅ Registrarse y crear su cuenta
- ✅ Gestionar sus experiencias de aventura
- ✅ Recibir y administrar reservas
- ✅ Monitorear ingresos y estadísticas
- ✅ Acceder a un dashboard completo en tiempo real

---

## 🎨 Características del Diseño

### **Branding LifExtreme**
- Paleta de colores oficial: `#4338ca` (Primary), `#10B981` (Secondary), `#f85640` (Accent)
- Tipografía: Outfit (Display) + Montserrat (Body)
- Bordes redondeados modernos (16px, 24px, 32px)
- Animaciones suaves y micro-interacciones

### **Páginas Incluidas**
1. **Landing Page** - Presentación de la plataforma
2. **Login** - Acceso a cuenta
3. **Registro** - Creación de cuenta para partners
4. **Dashboard** - Panel de control completo

---

## 📁 Estructura del Proyecto

```
lifextreme_partners_final/
├── index.html              # Landing page
├── login.html              # Página de login
├── registro.html           # Página de registro
├── dashboard.html          # Dashboard de partners
├── css/
│   ├── styles.css          # Estilos globales
│   ├── auth.css            # Estilos de autenticación
│   └── dashboard.css       # Estilos del dashboard
├── js/
│   ├── main.js             # JavaScript principal
│   ├── auth.js             # Lógica de autenticación
│   └── dashboard.js        # Lógica del dashboard
├── README.md               # Este archivo
├── BRANDING_UPDATE.md      # Documentación de branding
└── netlify.toml            # Configuración de Netlify
```

---

## 🚀 Cómo Usar

### **Opción 1: Abrir Localmente**

1. Descarga o clona el proyecto
2. Abre `index.html` en tu navegador
3. Navega por las diferentes páginas

### **Opción 2: Demo en Línea**

Visita el link de Netlify (próximamente)

---

## 🔐 Sistema de Autenticación (Demo)

### **Login**
- Email: `cualquier email`
- Password: `cualquier contraseña`
- El sistema acepta cualquier credencial para facilitar las pruebas

### **Registro**
- Completa el formulario
- Acepta términos y condiciones
- Automáticamente crea una sesión y redirige al dashboard

---

## 📊 Dashboard

El dashboard incluye:

- **Estadísticas en Tiempo Real**
  - Ingresos del mes
  - Reservas activas
  - Nuevos clientes
  - Calificación promedio

- **Próximas Reservas**
  - Lista de actividades programadas
  - Estados (Confirmada, Pendiente)
  - Información de clientes

- **Acciones Rápidas**
  - Nueva actividad
  - Gestionar slots
  - Subir multimedia
  - Generar reportes

- **Gráfico de Ingresos**
  - Visualización mensual
  - Tendencias de crecimiento

---

## 🎯 Tecnologías Utilizadas

- **HTML5** - Estructura semántica
- **CSS3** - Diseño moderno y responsive
- **JavaScript (Vanilla)** - Funcionalidad sin frameworks
- **Lucide Icons** - Iconografía moderna
- **Google Fonts** - Outfit + Montserrat
- **LocalStorage** - Gestión de sesiones (demo)

---

## 📱 Responsive Design

Completamente optimizado para:

- 💻 **Desktop** (1920px+)
- 💻 **Laptop** (1280px - 1920px)
- 📱 **Tablet** (768px - 1280px)
- 📱 **Mobile** (320px - 768px)

---

## 🎨 Secciones de la Landing Page

1. **Hero Section** - Presentación impactante
2. **Stats** - Estadísticas de la plataforma
3. **Value Propositions** - Pilares de LifExtreme
4. **Features** - Herramientas para partners
5. **Pricing** - Planes (Starter, Pro, Elite)
6. **FAQ** - Preguntas frecuentes
7. **CTA Final** - Llamado a la acción
8. **Footer** - Enlaces y redes sociales

---

## 🔧 Configuración para Producción

### **Para Integrar con Backend:**

1. Reemplazar `simulateLogin()` en `js/auth.js` con llamadas API reales
2. Conectar `simulateRegistro()` con endpoint de registro
3. Implementar autenticación JWT o similar
4. Conectar dashboard con API de datos reales

### **Variables de Entorno Sugeridas:**

```env
API_URL=https://api.lifextreme.com
AUTH_ENDPOINT=/auth/login
REGISTER_ENDPOINT=/auth/register
DASHBOARD_ENDPOINT=/partners/dashboard
```

---

## 📈 Próximas Funcionalidades

- [ ] Integración con backend real
- [ ] Sistema de pagos (Stripe/PayPal)
- [ ] Gestión completa de actividades
- [ ] Chat de soporte en vivo
- [ ] Notificaciones push
- [ ] Analytics avanzados
- [ ] Exportación de reportes
- [ ] Multi-idioma (ES/EN)
- [ ] Dark mode

---

## 🤝 Soporte

Para preguntas o soporte:

- **Email**: partners@lifextreme.com
- **Website**: https://lifextreme.com
- **Documentación**: Ver `BRANDING_UPDATE.md`

---

## 📄 Licencia

Copyright © 2026 LifExtreme Global Ltd. Todos los derechos reservados.

---

## 🎉 Créditos

**Diseñado y Desarrollado para LifExtreme**

- Branding: LifExtreme Design Team
- Desarrollo: LifExtreme Tech Team
- Fecha: 6 de Enero, 2026

---

**Hecho con ❤️ y ⚡ para revolucionar el turismo de aventura**

---

## 📝 Changelog

### Versión 1.0.0 (6 Enero 2026)

✅ **Completado:**
- Landing page completa con branding LifExtreme
- Sistema de autenticación (login + registro)
- Dashboard funcional con estadísticas
- Diseño 100% responsive
- Pricing section mejorada
- FAQ section con acordeón
- Footer completo
- Sistema de sesiones con localStorage

✅ **Mejoras de Diseño:**
- Actualización completa de paleta de colores
- Tipografía Outfit + Montserrat
- Bordes redondeados modernos
- Animaciones suaves
- Hover effects premium
- Gradientes de marca

✅ **Funcionalidades:**
- Login funcional con redirección
- Registro con validación
- Dashboard interactivo
- Sidebar colapsable
- Gráficos de ingresos
- Lista de reservas
- Acciones rápidas

---

**¡Listo para compartir y presentar!** 🚀
