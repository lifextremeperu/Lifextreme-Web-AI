# 🚀 GUÍA COMPLETA: CONFIGURAR SUPABASE PARA LIFEXTREME

## 📋 RESUMEN DE ARCHIVOS CREADOS

```
✅ SUPABASE_SETUP.md - Guía inicial
✅ supabase_schema.sql - Script de base de datos
✅ supabase_rls.sql - Políticas de seguridad
✅ js/supabase-client.js - Cliente para frontend
✅ SUPABASE_COMPLETE_GUIDE.md - Esta guía
```

---

## 🎯 PASO A PASO: CONFIGURACIÓN COMPLETA

### **PASO 1: Crear Proyecto en Supabase** (5 minutos)

1. **Ve a**: https://supabase.com
2. **Inicia sesión** con: lifextremeperu@gmail.com
3. **Click en** "New Project"
4. **Configuración**:
   ```
   Organization: Lifextreme
   Project name: lifextreme-backend
   Database Password: [GENERA UNA SEGURA - GUÁRDALA]
   Region: South America (São Paulo)
   Plan: Free
   ```
5. **Espera 2-3 minutos** mientras se crea

---

### **PASO 2: Ejecutar Script de Base de Datos** (3 minutos)

1. En Supabase Dashboard, ve a **SQL Editor**
2. Click en **"New query"**
3. **Copia TODO el contenido** de `supabase_schema.sql`
4. **Pégalo** en el editor
5. Click en **"Run"** (esquina inferior derecha)
6. **Verifica**: Deberías ver "Database schema created successfully!"

---

### **PASO 3: Configurar Seguridad (RLS)** (2 minutos)

1. En SQL Editor, click en **"New query"**
2. **Copia TODO el contenido** de `supabase_rls.sql`
3. **Pégalo** en el editor
4. Click en **"Run"**
5. **Verifica**: "Row Level Security policies created successfully!"

---

### **PASO 4: Obtener Credenciales** (1 minuto)

1. Ve a **Settings** → **API**
2. **Copia y guarda**:
   ```
   Project URL: https://xxxxx.supabase.co
   anon/public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... [SECRETO]
   ```

---

### **PASO 5: Configurar Variables de Entorno** (2 minutos)

1. **Crea archivo** `.env.local` en la raíz del proyecto:

```env
# Supabase Configuration
VITE_SUPABASE_URL=https://TU-PROYECTO.supabase.co
VITE_SUPABASE_ANON_KEY=TU-ANON-KEY-AQUI

# NO EXPONGAS ESTA CLAVE EN EL FRONTEND
SUPABASE_SERVICE_ROLE_KEY=TU-SERVICE-ROLE-KEY-AQUI
```

2. **Agrega** `.env.local` al `.gitignore`:

```bash
echo ".env.local" >> .gitignore
```

---

### **PASO 6: Instalar Cliente de Supabase** (1 minuto)

```bash
npm install @supabase/supabase-js
```

---

### **PASO 7: Configurar Autenticación** (3 minutos)

1. En Supabase Dashboard, ve a **Authentication** → **Providers**
2. **Habilita**:
   - ✅ Email/Password
   - ✅ Google OAuth (opcional)
3. **Configura Email Templates**:
   - Ve a **Email Templates**
   - Personaliza "Confirm signup" y "Reset password"

---

### **PASO 8: Crear Buckets de Storage** (2 minutos)

1. Ve a **Storage** → **Create bucket**
2. **Crea estos buckets**:

```
Bucket: tour-images
  Public: Yes
  Max file size: 5MB

Bucket: user-avatars
  Public: Yes
  Max file size: 2MB

Bucket: partner-logos
  Public: Yes
  Max file size: 1MB

Bucket: review-images
  Public: Yes
  Max file size: 3MB
```

---

### **PASO 9: Insertar Datos de Ejemplo** (5 minutos)

1. En SQL Editor, ejecuta este script:

```sql
-- Insertar tours de ejemplo
INSERT INTO tours (title, slug, description, region, difficulty, duration_days, price_pen, category, active, featured) VALUES
('Camino Inca a Machu Picchu 4D', 'camino-inca-4d', 'La ruta de trekking más famosa del mundo', 'Cusco', 'challenging', 4, 2800, 'trekking', true, true),
('Rafting en Urubamba', 'rafting-urubamba', 'Adrenalina en rápidos nivel 3-4', 'Cusco', 'moderate', 1, 350, 'rafting', true, true),
('Escalada en Huaraz', 'escalada-huaraz', 'Conquista los Andes peruanos', 'Huaraz', 'extreme', 3, 1500, 'climbing', true, false);

-- Verificar
SELECT * FROM tours;
```

---

### **PASO 10: Probar la Conexión** (3 minutos)

1. **Crea archivo de prueba** `test-supabase.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Test Supabase</title>
  <script type="module">
    import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'
    
    const supabase = createClient(
      'TU-PROJECT-URL',
      'TU-ANON-KEY'
    )
    
    // Probar conexión
    async function testConnection() {
      const { data, error } = await supabase
        .from('tours')
        .select('*')
        .limit(5)
      
      if (error) {
        console.error('Error:', error)
        document.body.innerHTML = `<h1 style="color:red">Error: ${error.message}</h1>`
      } else {
        console.log('Tours:', data)
        document.body.innerHTML = `
          <h1 style="color:green">✅ Conexión exitosa!</h1>
          <p>Tours encontrados: ${data.length}</p>
          <pre>${JSON.stringify(data, null, 2)}</pre>
        `
      }
    }
    
    testConnection()
  </script>
</head>
<body>
  <h1>Probando conexión...</h1>
</body>
</html>
```

2. **Abre el archivo** en tu navegador
3. **Verifica**: Deberías ver "✅ Conexión exitosa!"

---

## ✅ CHECKLIST FINAL

```
[ ] Proyecto Supabase creado
[ ] Script de base de datos ejecutado
[ ] Políticas RLS configuradas
[ ] Credenciales guardadas
[ ] Variables de entorno configuradas
[ ] Cliente Supabase instalado
[ ] Autenticación configurada
[ ] Buckets de storage creados
[ ] Datos de ejemplo insertados
[ ] Conexión probada y funcionando
```

---

## 🎯 PRÓXIMOS PASOS

### **1. Integrar en el Frontend**

Reemplaza las funciones mock en `js/app.js` con llamadas reales a Supabase:

```javascript
// Antes (mock)
const tours = mockData.tours

// Después (Supabase)
import { getTours } from './supabase-client.js'
const { data: tours } = await getTours()
```

### **2. Implementar Autenticación**

Actualiza `partners/js/auth.js` para usar Supabase:

```javascript
import { signIn, signUp } from '../../js/supabase-client.js'

// Login
const { data, error } = await signIn(email, password)
```

### **3. Conectar Reservas**

Actualiza el wizard de reservas para guardar en Supabase:

```javascript
import { createBooking } from './supabase-client.js'

const { data, error } = await createBooking({
  user_id: currentUser.id,
  tour_id: selectedTour.id,
  booking_date: selectedDate,
  num_people: numPeople,
  total_price: totalPrice,
  contact_name: name,
  contact_email: email,
  contact_phone: phone
})
```

---

## 📊 ESTRUCTURA DE DATOS

### **Tablas Principales:**

```
users_profiles     → Perfiles de usuarios
tours              → Catálogo de tours
bookings           → Reservas
partners           → Operadores
partner_activities → Tours de partners
reviews            → Reseñas
ai_recommendations → Recomendaciones IA
analytics_events   → Eventos de analytics
payments           → Pagos
```

### **Relaciones:**

```
users_profiles ←→ bookings ←→ tours
partners ←→ partner_activities ←→ tours
bookings ←→ reviews ←→ tours
users_profiles ←→ ai_recommendations ←→ tours
```

---

## 🔒 SEGURIDAD

### **Políticas RLS Activas:**

- ✅ Usuarios solo ven sus propios datos
- ✅ Partners solo ven sus propios tours y reservas
- ✅ Tours activos son públicos
- ✅ Reseñas verificadas son públicas
- ✅ Pagos protegidos por RLS

### **Mejores Prácticas:**

1. **NUNCA** expongas `service_role_key` en el frontend
2. **SIEMPRE** usa `anon_key` en el cliente
3. **VALIDA** datos en el backend con RLS
4. **SANITIZA** inputs del usuario
5. **USA** HTTPS en producción

---

## 📞 SOPORTE

### **Recursos Útiles:**

- **Documentación Supabase**: https://supabase.com/docs
- **Dashboard**: https://app.supabase.com
- **SQL Editor**: https://app.supabase.com/project/_/sql
- **Storage**: https://app.supabase.com/project/_/storage

### **Troubleshooting:**

**Error: "relation does not exist"**
→ Ejecuta `supabase_schema.sql` nuevamente

**Error: "permission denied"**
→ Verifica que RLS esté configurado correctamente

**Error: "Invalid API key"**
→ Verifica que las credenciales en `.env.local` sean correctas

---

## 🎉 ¡LISTO!

Tu backend de Supabase está completamente configurado y listo para usar.

**Siguiente paso**: Integrar las funciones de Supabase en tu frontend.

---

**Última actualización:** 06 Enero 2026  
**Proyecto:** Lifextreme Backend  
**Estado:** 🟢 Listo para producción
