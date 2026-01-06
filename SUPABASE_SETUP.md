# 🗄️ GUÍA RÁPIDA: CONFIGURAR SUPABASE

## PASO 1: Crear Proyecto (5 min)
1. Ir a https://supabase.com
2. Sign up / Login
3. "New Project"
4. Nombre: `lifextreme-prod`
5. Password: [guardar en lugar seguro]
6. Region: `South America (São Paulo)`

## PASO 2: Crear Tablas (10 min)
1. Ir a "SQL Editor" (menú izquierdo)
2. "New Query"
3. Copiar TODO el contenido de `supabase-schema.sql`
4. Pegar y ejecutar "Run"
5. Verificar en "Table Editor" que aparecen:
   - `bookings`
   - `ai_profiles`

## PASO 3: Obtener Credenciales (2 min)
1. Ir a "Settings" → "API"
2. Copiar:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## PASO 4: Configurar en Lifextreme (5 min)
1. Abrir `js/supabase-client.js`
2. Reemplazar:
   ```javascript
   const SUPABASE_URL = 'TU_PROJECT_URL';
   const SUPABASE_ANON_KEY = 'TU_ANON_KEY';
   ```

## PASO 5: Agregar Script en HTML (2 min)
En `index.html`, antes de `supabase-client.js`:
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="js/supabase-client.js"></script>
```

## ✅ LISTO
Ahora las reservas se guardan en la nube automáticamente.

## 📊 Ver Datos
Dashboard → Table Editor → bookings
