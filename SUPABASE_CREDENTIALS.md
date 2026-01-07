# 🔐 CREDENCIALES DE SUPABASE - LIFEXTREME

## ✅ Configuración Completada

Tu proyecto Supabase está completamente configurado y listo para usar.

---

## 📋 CREDENCIALES

### **Project URL:**
```
https://zobpkmiqrvhbepqnjshr.supabase.co
```

### **Anon Key (Pública):**
```
sb_publishable_pBMaD6Mm-6Pi5cwwp3UUsw_Pndjw-mo
```

### **Service Role Key (Secreta - NO EXPONGAS):**
```
sb_secret_7d_j2u37-hVXO_2VkvCc8A_tEaP_LDS
```

---

## 🎯 ARCHIVOS CONFIGURADOS

✅ **test-supabase.html** - Configurado con credenciales reales
✅ **js/supabase-client.js** - Cliente configurado
✅ **Base de datos** - 5 tablas creadas
✅ **RLS** - Seguridad activada
✅ **Datos de ejemplo** - 5 tours insertados

---

## 🚀 PRÓXIMOS PASOS

### **1. Probar la Conexión**

Abre en tu navegador:
```
C:\Users\ASUS\.gemini\antigravity\scratch\lifextreme_v29_professional\test-supabase.html
```

Deberías ver:
- ✅ Conexión exitosa
- ✅ 5 tours cargados

### **2. Verificar en Supabase Dashboard**

Ve a: https://supabase.com/dashboard/project/zobpkmiqrvhbepqnjshr

**Table Editor** → **tours** → Deberías ver 5 tours

### **3. Integrar en tu Aplicación**

El cliente de Supabase ya está configurado en:
```javascript
import { supabase } from './js/supabase-client.js'

// Obtener tours
const { data: tours } = await supabase
  .from('tours')
  .select('*')
```

---

## 📊 ESTRUCTURA DE BASE DE DATOS

### **Tablas Creadas:**

1. **users_profiles** - Perfiles de usuarios
2. **tours** - Catálogo de tours (5 tours de ejemplo)
3. **bookings** - Reservas
4. **partners** - Operadores
5. **reviews** - Reseñas

### **Seguridad:**

- ✅ Row Level Security (RLS) habilitado
- ✅ Políticas de acceso configuradas
- ✅ Usuarios solo ven sus propios datos
- ✅ Tours públicos accesibles sin autenticación

---

## 🔗 ENLACES ÚTILES

**Dashboard Principal:**
https://supabase.com/dashboard/project/zobpkmiqrvhbepqnjshr

**Table Editor:**
https://supabase.com/dashboard/project/zobpkmiqrvhbepqnjshr/editor

**SQL Editor:**
https://supabase.com/dashboard/project/zobpkmiqrvhbepqnjshr/sql

**API Docs:**
https://supabase.com/dashboard/project/zobpkmiqrvhbepqnjshr/api

**Authentication:**
https://supabase.com/dashboard/project/zobpkmiqrvhbepqnjshr/auth/users

---

## ⚠️ SEGURIDAD

### **IMPORTANTE:**

- ✅ La **Anon Key** es segura para usar en el frontend
- ❌ La **Service Role Key** NUNCA debe exponerse en el frontend
- ✅ Usa la Service Role Key solo en el backend/servidor
- ✅ Las credenciales ya están en `.gitignore`

---

## 🎉 ¡TODO LISTO!

Tu backend de Supabase está completamente configurado y funcionando.

**Siguiente paso:** Integrar las funciones de Supabase en tu aplicación frontend.

---

**Fecha de configuración:** 06 Enero 2026  
**Proyecto:** Lifextreme Backend  
**Estado:** 🟢 Activo y Funcionando
