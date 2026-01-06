# 🚀 PLAN DE IMPLEMENTACIÓN MVP - 48 HORAS
## Lifextreme - Listo para Vender

---

## ✅ COMPLETADO (Hoy - 05 Enero 2026)

### **Fase 1: Información Legal y Contacto** ✅
- [x] Página de Términos y Condiciones (`terminos.html`)
- [x] Página de Política de Privacidad (`privacidad.html`)
- [x] Footer profesional con enlaces legales
- [x] Datos de contacto estructurados
- [x] Archivo de configuración centralizada (`config.js`)

**Tiempo invertido:** 2 horas  
**Estado:** ✅ LISTO PARA PRODUCCIÓN

---

## 📋 PENDIENTE - DÍA 1 (06 Enero 2026)

### **Fase 2: Integración de Pagos** 🔴 CRÍTICO
**Tiempo estimado:** 4-6 horas

#### **Opción A: Mercado Pago (Recomendado para Perú)**

**Pasos:**
1. **Crear cuenta Mercado Pago Business** (30 min)
   - Ir a: https://www.mercadopago.com.pe/developers
   - Registrar empresa
   - Verificar cuenta

2. **Obtener credenciales** (15 min)
   - Public Key: `APP_USR-XXXXXXXX`
   - Access Token: `APP_USR-XXXXXXXX` (SECRETO)

3. **Instalar SDK** (15 min)
   ```html
   <!-- En index.html, antes de </body> -->
   <script src="https://sdk.mercadopago.com/js/v2"></script>
   ```

4. **Crear archivo de integración** (2 horas)
   ```javascript
   // js/payment-mercadopago.js
   const mp = new MercadoPago('TU_PUBLIC_KEY');
   
   async function processPayment(bookingData) {
       const preference = {
           items: [{
               title: bookingData.tourName,
               unit_price: bookingData.totalPrice,
               quantity: 1
           }],
           back_urls: {
               success: 'https://lifextreme.com/pago-exitoso',
               failure: 'https://lifextreme.com/pago-fallido',
               pending: 'https://lifextreme.com/pago-pendiente'
           }
       };
       
       // Crear preferencia en backend
       const response = await fetch('/api/create-preference', {
           method: 'POST',
           body: JSON.stringify(preference)
       });
       
       const data = await response.json();
       mp.checkout({
           preference: { id: data.id }
       });
   }
   ```

5. **Testing** (1 hora)
   - Usar tarjetas de prueba de Mercado Pago
   - Verificar flujo completo

**Archivos a crear:**
- `js/payment-mercadopago.js`
- `pago-exitoso.html`
- `pago-fallido.html`

---

### **Fase 3: Backend con Supabase** 🔴 CRÍTICO
**Tiempo estimado:** 3-4 horas

#### **Por qué Supabase:**
- ✅ Gratis hasta 500MB
- ✅ PostgreSQL completo
- ✅ API REST automática
- ✅ Auth incluido
- ✅ Sin código backend

#### **Pasos:**

1. **Crear proyecto Supabase** (20 min)
   - Ir a: https://supabase.com
   - Crear cuenta
   - Nuevo proyecto: "lifextreme-prod"

2. **Crear tablas** (30 min)
   ```sql
   -- Tabla de reservas
   CREATE TABLE bookings (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       user_name VARCHAR(255) NOT NULL,
       user_email VARCHAR(255) NOT NULL,
       user_phone VARCHAR(50),
       tour_id INTEGER NOT NULL,
       tour_name VARCHAR(255) NOT NULL,
       tour_date DATE NOT NULL,
       participants INTEGER DEFAULT 1,
       total_price DECIMAL(10,2) NOT NULL,
       payment_status VARCHAR(50) DEFAULT 'pending',
       payment_id VARCHAR(255),
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW()
   );

   -- Tabla de perfiles IA
   CREATE TABLE ai_profiles (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       user_email VARCHAR(255) UNIQUE NOT NULL,
       profile_data JSONB NOT NULL,
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW()
   );

   -- Índices
   CREATE INDEX idx_bookings_email ON bookings(user_email);
   CREATE INDEX idx_bookings_status ON bookings(payment_status);
   CREATE INDEX idx_ai_profiles_email ON ai_profiles(user_email);
   ```

3. **Configurar API** (1 hora)
   ```javascript
   // js/supabase-client.js
   import { createClient } from '@supabase/supabase-js';

   const supabaseUrl = 'https://XXXXXXXX.supabase.co';
   const supabaseKey = 'TU_ANON_KEY';
   const supabase = createClient(supabaseUrl, supabaseKey);

   // Guardar reserva
   async function saveBooking(bookingData) {
       const { data, error } = await supabase
           .from('bookings')
           .insert([bookingData]);
       
       if (error) throw error;
       return data;
   }

   // Guardar perfil IA
   async function saveAIProfile(profileData) {
       const { data, error } = await supabase
           .from('ai_profiles')
           .upsert([profileData]);
       
       if (error) throw error;
       return data;
   }
   ```

4. **Integrar con frontend** (1.5 horas)
   - Modificar `addToCartFinal()` para guardar en Supabase
   - Modificar `submitAIProfile()` para guardar en Supabase
   - Agregar manejo de errores

**Archivos a crear:**
- `js/supabase-client.js`

---

### **Fase 4: Emails Automáticos** 🔴 CRÍTICO
**Tiempo estimado:** 2-3 horas

#### **Opción: EmailJS (Más rápido, sin backend)**

1. **Crear cuenta EmailJS** (15 min)
   - Ir a: https://www.emailjs.com
   - Plan gratuito: 200 emails/mes

2. **Configurar servicio** (30 min)
   - Conectar Gmail/Outlook
   - Crear templates:
     - Confirmación de reserva
     - Confirmación de pago
     - Bienvenida con perfil IA

3. **Integrar en frontend** (1.5 horas)
   ```javascript
   // js/email-service.js
   import emailjs from '@emailjs/browser';

   emailjs.init('TU_PUBLIC_KEY');

   async function sendBookingConfirmation(bookingData) {
       const templateParams = {
           user_name: bookingData.userName,
           user_email: bookingData.userEmail,
           tour_name: bookingData.tourName,
           tour_date: bookingData.tourDate,
           total_price: bookingData.totalPrice,
           booking_id: bookingData.id
       };

       try {
           await emailjs.send(
               'service_id',
               'template_booking_confirmation',
               templateParams
           );
           console.log('Email enviado exitosamente');
       } catch (error) {
           console.error('Error enviando email:', error);
       }
   }
   ```

**Archivos a crear:**
- `js/email-service.js`
- Templates en EmailJS dashboard

---

## 📋 PENDIENTE - DÍA 2 (07 Enero 2026)

### **Fase 5: Hosting y Dominio** 🟡 IMPORTANTE
**Tiempo estimado:** 2-3 horas

#### **Opción: Netlify (Recomendado)**

1. **Preparar para producción** (30 min)
   - Actualizar `config.js` con datos reales
   - Reemplazar XXX con números/emails reales
   - Verificar todos los enlaces

2. **Deploy en Netlify** (1 hora)
   - Crear cuenta en https://netlify.com
   - Conectar repositorio Git (o drag & drop)
   - Configurar dominio personalizado
   - SSL automático (gratis)

3. **Configurar dominio** (1 hora)
   - Comprar dominio: `lifextreme.com` (GoDaddy, Namecheap)
   - Configurar DNS en Netlify
   - Esperar propagación (1-24h)

**URLs finales:**
- Producción: `https://lifextreme.com`
- Staging: `https://lifextreme-staging.netlify.app`

---

### **Fase 6: SEO Básico** 🟡 IMPORTANTE
**Tiempo estimado:** 1-2 horas

1. **Meta tags** (30 min)
   ```html
   <!-- En index.html <head> -->
   <meta name="description" content="Descubre las mejores aventuras extremas en Perú...">
   <meta name="keywords" content="aventuras perú, trekking cusco, inca trail">
   
   <!-- Open Graph -->
   <meta property="og:title" content="Lifextreme - Aventuras Extremas en Perú">
   <meta property="og:description" content="Tours de trekking, escalada...">
   <meta property="og:image" content="https://lifextreme.com/og-image.jpg">
   <meta property="og:url" content="https://lifextreme.com">
   
   <!-- Twitter Card -->
   <meta name="twitter:card" content="summary_large_image">
   <meta name="twitter:title" content="Lifextreme">
   <meta name="twitter:description" content="Aventuras extremas en Perú">
   ```

2. **Google Analytics** (20 min)
   - Crear cuenta GA4
   - Agregar tracking code

3. **Google Search Console** (20 min)
   - Verificar propiedad
   - Enviar sitemap

4. **Sitemap.xml** (30 min)
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
       <url>
           <loc>https://lifextreme.com/</loc>
           <priority>1.0</priority>
       </url>
       <url>
           <loc>https://lifextreme.com/terminos.html</loc>
           <priority>0.5</priority>
       </url>
       <!-- ... más URLs -->
   </urlset>
   ```

**Archivos a crear:**
- `sitemap.xml`
- `robots.txt`

---

### **Fase 7: Testing Final** 🟢 CRÍTICO
**Tiempo estimado:** 3-4 horas

#### **Checklist de Testing:**

**Funcionalidad:**
- [ ] Navegación entre secciones
- [ ] Búsqueda en tiempo real
- [ ] Filtros de región
- [ ] Abrir modal de reserva
- [ ] Wizard de 3 pasos completo
- [ ] Agregar al carrito
- [ ] Proceso de pago (con tarjeta de prueba)
- [ ] Recepción de email de confirmación
- [ ] Formulario de perfil IA
- [ ] Recomendaciones personalizadas

**Responsive:**
- [ ] Mobile (320px - 480px)
- [ ] Tablet (768px - 1024px)
- [ ] Desktop (1280px+)

**Navegadores:**
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

**Performance:**
- [ ] Lighthouse Score > 90
- [ ] Tiempo de carga < 3s
- [ ] Imágenes optimizadas

---

## 📊 RESUMEN DE TIEMPO

| Fase | Tiempo | Prioridad | Día |
|------|--------|-----------|-----|
| 1. Legal y Contacto | 2h | ✅ HECHO | Hoy |
| 2. Pagos (Mercado Pago) | 4-6h | 🔴 CRÍTICO | Día 1 |
| 3. Backend (Supabase) | 3-4h | 🔴 CRÍTICO | Día 1 |
| 4. Emails (EmailJS) | 2-3h | 🔴 CRÍTICO | Día 1 |
| 5. Hosting (Netlify) | 2-3h | 🟡 IMPORTANTE | Día 2 |
| 6. SEO Básico | 1-2h | 🟡 IMPORTANTE | Día 2 |
| 7. Testing Final | 3-4h | 🟢 CRÍTICO | Día 2 |

**TOTAL:** 17-24 horas de trabajo

---

## 🎯 HITOS

### **Fin del Día 1 (06 Enero):**
- ✅ Pagos funcionando
- ✅ Backend guardando reservas
- ✅ Emails automáticos
- ✅ Puedes procesar reservas de prueba

### **Fin del Día 2 (07 Enero):**
- ✅ Sitio en producción con dominio
- ✅ SEO configurado
- ✅ Testing completo
- ✅ **LISTO PARA VENDER** 🚀

---

## 📞 SIGUIENTE PASO INMEDIATO

**AHORA MISMO (Día 1 - Mañana):**
1. Crear cuenta Mercado Pago Business
2. Crear proyecto Supabase
3. Crear cuenta EmailJS

**Mientras tanto:**
- Actualizar `config.js` con datos reales
- Reemplazar todos los XXX con información real
- Preparar imágenes de tours (optimizadas)

---

## 🆘 PLAN B (Si algo falla)

**Si Mercado Pago tarda:**
- Usar formulario manual → WhatsApp
- Cobrar por Yape/Plin
- Migrar a Mercado Pago después

**Si Supabase falla:**
- Usar localStorage temporalmente
- Exportar datos manualmente
- Migrar después

**Si EmailJS falla:**
- Enviar confirmaciones por WhatsApp
- Implementar emails después

---

## ✅ CHECKLIST FINAL PRE-LANZAMIENTO

Antes de hacer público el sitio, verificar:

- [ ] Todos los XXX reemplazados con datos reales
- [ ] WhatsApp Business configurado
- [ ] Email info@lifextreme.com activo
- [ ] Mercado Pago en modo producción
- [ ] Supabase con datos reales
- [ ] SSL activo (https://)
- [ ] Términos y Privacidad revisados por legal
- [ ] RUC y licencias actualizadas
- [ ] Seguro de accidentes vigente
- [ ] Guías certificados verificados
- [ ] Precios finales confirmados
- [ ] Fotos de tours reales
- [ ] Testing completo en todos los dispositivos

---

**¿Listo para empezar el Día 1?** 🚀

Siguiente paso: Crear cuentas en:
1. Mercado Pago Business
2. Supabase
3. EmailJS

¿Necesitas ayuda con alguno de estos pasos?
