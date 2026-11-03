# 🚨 AUDITORÍA DE PRODUCCIÓN — LIFEXTREME (READY TO LAUNCH?)

**Fecha:** 30 Octubre 2026 · **Repositorio:** `lifextremeperu/Lifextreme-Web-AI` · **Target:** `www.lifextreme.store`

---

## 🔴 DIAGNÓSTICO GENERAL

El frontend (`www.lifextreme.store`) está **vivo y responde 200 OK**, pero el **cerebro de la plataforma (MAX AI) está caído** (`max.lifextreme.store/health` → `error code: 502`). Además, hay **credenciales de administrador de la base de datos expuestas públicamente** en archivos estáticos que se sirven desde el CDN.

**Veredicto: NO está listo para producción.** El sitio se ve bien, pero la parte que convierte usuarios en clientes (chat + reservas + pagos) falla o es insegura.

Con respecto al repositorio de GitHub: tu checkout local es mucho más completo que lo que queda en Git remoto (hay HTMLs, scripts de datos, SQL de Supabase y agente de ventas B2B que no llegan al deploy). El pipeline `deploy.ps1` hace commit de TODO sin revisión, lo que explica por qué hay una carpeta `reportes_b2b` y 100+ archivos experimentales mezclados con el código del sitio.

---

## 🔴 CRÍTICO #1 — Cerebro AI caído: el chat MAX no funciona

**Archivo:** `max.lifextreme.store` → tunnel Cloudflare a tu PC local

```
curl https://max.lifextreme.store/health
→ error code: 502
```

**Qué está pasando:** el FastAPI (`backend/src/server.py`), Qdrant (Docker 336K vectores), Ollama y el notebook del LLM corren en tu PC de Cusco, expuestas por un Cloudflare Tunnel (`iniciar_MAX.bat`, `docker-compose.qdrant.yml`). Si tu PC duerme, se apaga o pierde internet, el chat de TODOS los usuarios muere. Ahora mismo está muerto.

**Impacto comercial:** 0% de las cotizaciones conversacionales funcionan. El 30% de cierre vía WhatsApp del `chat_webhook` nunca se dispara. Es la pérdida de conversión más grande del proyecto.

**Corrección (en orden de esfuerzo):**

| Opción | Descripción | Costo | Riesgo |
|--------|-------------|-------|--------|
| **A - Recomendada: VPS cloud 24/7** | Migrar FastAPI + Qdrant a un VPS (DigitalOcean/Railway/Hetzner ~$12-25/mes), Cloudflare Tunnel apuntando al VPS con `restart: always` y Docker Compose | $12-25/mes | Bajo, migración limitada |
| **B - Serverless parcial** | Portar el endpoint `/webhook/lifextreme` a Vercel Function usando Qdrant Cloud (managed) + Groq Cloud (sin Ollama) | ~$0-40/mes por uso | Medio — hay que portar embeddings y Qdrant cloud-hosted |
| **C - Doble túnel con watchdog** | Mantener VPS + script `keepalive` en tu PC que reinicia el proceso si un health check falla 3 veces seguidas | $0 | Alto — sigue dependiendo de tu conexión |

**Mínimo indispensable hoy:** reiniciar `start_max_backend.bat` y `docker start rag_lifextreme` AHORA para que el health check vuelva a dar 200 OK aun si la solución definitiva viene después.

---

## 🔴 CRÍTICO #2 — Clave maestra de Supabase expuesta públicamente

**Archivo:** `admin-setup.html` líneas 215-217, y `create-partner.html` línea 37-40

```js
const SUPABASE_URL = 'https://zobpkmiqrvhbepqnjshr.supabase.co'
const SERVICE_KEY = 'sb_secret_7d_j2u37-hVXO_2VkvCc8A_tEaP_LDS'
```

**Qué está pasando:** estas páginas son estáticas y Vercel las sirve al mundo. Cualquier persona que lea el código fuente obtiene la **clave de servicio** de Supabase, con la que puede **borrar, editar o leer TODO tu CRM, reservas, emails y datos de usuarios**, saltándose las políticas RLS.

Es lo más grave que hay en el repo. Ni siquiera requiere ser hacker: es leer ctrl+U.

**Corrección inmediata (hoy):**

1. **Rota la clave YA.** Ve a Supabase Dashboard → Settings → API → `sb_secret_7d_...` → **Rotate key** antes de hacer push a GitHub.
2. **Elimina `admin-setup.html` y `admin-brain.html` del repo** (o sácalos del CDN con `.vercelignore`).
3. La funcionalidad de admin debe migrar a una **Serverless Function protegida** (`/api/admin/*.js` con JWT role check, o clave en `process.env.ADMIN_SECRET` + Bearer token).
4. Añade `.vercelignore` para todas las páginas de administración: `admin-*.html`, `login.html`, `test-*.html`, `eliminar-datos.html`, `supabase-*.sql`, `PAYPAL_SETUP_GUIDE.md`, y del secret (`SUPABASE_CREDENTIALS.md`).

**Archivos sospechosos adicionales a ocultar del CDN:**

```
admin-setup.html
admin-brain.html
lifextreme_admin_portal.html
eliminar-datos.html
login.html
test-supabase.html
test-rag-live.py
create-partner.html
SUPABASE_CREDENTIALS.md
partner_migration.sql
```

---

## 🔴 CRÍTICO #3 — URLs privadas (Tailscale) en el CSP de producción

**Archivos:** `index.html` (línea 356), `en/index.html` (línea 356)

```
connect-src 'self' ... https://hub-cusco-2026.tail883d62.ts.net
 ee https://desktop-sedhoop.tail883d62.ts.net ...
```

**Qué está pasando:** estás exponiendo los dominios de tu red Tailscale (la VPN privada entre tus PCs) en el CSP de producción, además de localhost. Esto es:
- **Fuga de arquitectura** (le dice al mundo tu red interna)
- **Riesgo de CORS/CSP misconfigured** si el navegador intenta resolver `.ts.net` sin VPN
- Velocidad de perfil y no militar.

**Corrección:**
```js
// index.html y en/index.html
const CSP_PRODUCTION = "default-src 'self' https: data: blob: 'unsafe-inline' 'unsafe-eval'; connect-src 'self' https://max.lifextreme.store wss://max.lifextreme.store https://*.supabase.co ...;
```
Solo dominios reales. Localhost y Tailscale van a un `CSP_DEV` separado en development.

---

## 🟡 ALTO — Fallbacks que silencian errores en flujo de reservas

**Archivo:** `js/supabase-client.js`

En `createGuideBooking()` y `createEliteProfile()`:

```js
catch (error) {
  console.warn('⚠️ Error guardando solicitud (Usando fallback local):', error);
  // Fallback: Simulamos éxito para no romper UX
  return { success: true, mock: true };  // ← Mentira al usuario
}
```

**Qué está pasando:** si Supabase falla, el usuario ve "Reserva creada" cuando **NUNCA se guardó nada**. Un lead perdido sin que el equipo se entere. En manufactura tendrías un cliente esperando que no existe.

**Corrección:**
```js
catch (error) {
  console.error('❌ Error guardando solicitud:', error);
  Sentry?.captureException(error);
  // Mostrar error real y opción de WhatsApp como canal de recovery
  return { success: false, error, fallbackWhatsApp: 'https://wa.me/51958050928' };
}
```
El WhatsApp sí puede ser el plan B visiblemente ofrecido, pero **nunca fingir que la reserva se procesó**.

---

## 🟡 ALTO — 10 páginas de admin/test/datos públicos sin auth

**Archivos expuestos en el CDN público (verificable en lifextreme.store):**

| Archivo | Contenido | Gravedad |
|---------|-----------|----------|
| `admin-setup.html` | Wizard con SERVICE KEY | 🔴 Crítico |
| `admin-brain.html` | Admin vectorial Qdrant | 🔴 Alto |
| `lifextreme_admin_portal.html` | Portal CRM interno | 🔴 Alto |
| `eliminar-datos.html` | Tool de borrado de datos | 🔴 Crítico |
| `login.html` | Página de login sin puerta | 🟡 Alto |
| `test-supabase.html`, `test.html`, `test-blog.html`, `test-alpaca.html` | Páginas de prueba | 🟡 Medio |
| `test-rag-live.py`, `simulate_synthetic_clients.py`, `agente_geo_validador.py` | Scripts backend | 🟡 Medio |
| `agencias_emails_reporte.md`, `B2B_Prospectos_Cusco.csv`, `Lifextreme_B2B_Prospects.csv` | **Emails reales de prospectos** | 🔴 Crítico (ley de protección de datos / Data Leak) |

Los CSV de prospectos B2B con emails reales de terceros **públicamente descargables son responsabilidad legal** (Reglamento UE si hay EU / Peru (Ley 29733), y parecen haber sido generados por el pipeline de prospección con datos reales).

**Corrección en una sola pasada** — añade a `.vercelignore` y `.gitignore`:

```
# Admin y debug
admin-*.html
lifextreme_admin_portal.html
eliminar-datos.html
login.html
test-*.html
test-*.py
*_setup.html

# Datos sensibles
*.csv
agencias_emails_reporte.md
SUPABASE_CREDENTIALS.md
service_account.json
gcp-ai-key.json
data_expediente_*.json
```

Y PARA USD/CONSISTENCIA GLOBAL: mueve esos archivos a una carpeta `_private/` (fuera del root del deploy) para que ni Vercel ni nadie cuelgue nada.

---

## 🟡 ALTO — Datos falsos sembrados en el código del frontend

**Archivo:** `js/app.js`

```js
let completedTours = [
    { id: 1, title: 'Inca Trail 4D', ratings: { guide: 5, equipment: 4, difficulty: 5 } },
    ...
];
```

**Impacto:** Los usuarios ven tanto ratings/fotos de viajes no vividos, cosmetics que desincentivan confiar (y también inflan el FOMO que el juego deí Games de "Socio Elite").

**Corrección:** leer `completed_tours` de la tabla Supabase del usuario autenticado, y el estado vacío que no mienta.

---

## 🟡 MEDIO — Niubiz / PayPal sin flujo real de cobro

**Estado actual:** `payment-niubiz.html`, `payment-paypal.html`, `payment-yape.html` son páginas estáticas con QR de WhatsApp / botón de PayPal sandbox, pero **la pasarela no está integrada con la API real**.

**Cómo verificar:** intenta crear una reserva y completar el pago de 30%. Si te pide transferencia manual vía WhatsApp, no está integrado real.

**Corrección MÍNIMA viable para El Salvador:**

Necesitas un webhook real. Opciones:
- **PayPal Checkout (nativo)**: Ya tienes PayPal, no requiere mucho código. Integrar con la fórmula `payment-paypal.html`.
- **Stripe webhook** (`api/webhooks/stripe-sentinel.js`) ya este archivo existe pero usa `process.env.SUPABASE_SERVICE_ROLE_KEY` y no está cableado al `checkSupabaseSchema`.
- **Izipay/Niubiz requiere server-side HTTPS** (no puedes correrlo en el browser por PCI-DSS).

**Recomendación de lanzamiento:** usa **PayPal Checkout + Yape QR manual con confirmación en el chat** para go-live rápido. Niubiz/Izipay lo integras después cuando el volumen lo justifique.

---

## 🚨 LA LISTA MAESTRA DE CORRECCIONES (PRIORIZADA)

### HOY (bloqueante — sin esto NO lanzar)

| # | Tarea | Dificultad | Tiempo |
|---|-------|-----------|--------|
| 1 | Rotar la SERVICE KEY de Supabase (fuga) | Fácil (dashboard) | 10 min |
| 2 | `.vercelignore` + `.gitignore` para todo lo privado/admin/CSV de prospectos | Fácil | 30 min |
| 3 | Eliminar `admin-setup.html` y reemplazar por una serverless function protegida | Media | 2h |
| 4 | Switch del CSP: quitar Tailscale/localhost de index.html + en/index.html | Fácil | 20 min |
| 5 | Reiniciar el backend MAX (`start_max_backend.bat` + `docker start rag_lifextreme`) para que el health `/health` dé 200 | Fácil | 5 min |
| 6 | Arreglar los falsos `success: true` en `supabase-client.js` (`createGuideBooking`, `createEliteProfile`) | Fácil | 30 min |
| 7 | Limpiar los `completedTours` hardcodeados en `js/app.js` | Fácil | 30 min |

### ESTA SEMANA (para que el flujo de usuario real funcione)

| # | Tarea | Dificultad | Tiempo |
|---|-------|-----------|--------|
| 8 | Migrar el backend MAX AI (FastAPI + Qdrant) a un VPS 24/7 (DigitalOcean droplet $12/mes con Docker Compose) | Media | 4-6h |
| 9 | Integrar **PayPal Checkout real** (client/server con webhook a Supabase) en `payment-paypal.html` | Media | 3-4h |
| 10 | Script `deploy.py` que haga `git pull` + `npm run build` + `vercel --prod --yes` después de un `test:quick` (reemplaza `deploy.ps1`).

### ESTE MES (hardening)

| # | Tarea | Dificultad |
|---|-------|-----------|
| 11 | Supabase Auth real (login + RLS por usuario) para socios Elite y Partners | Media |
| 12 | Tests automatizados (`vitest`) para el checkout, Booking y la API de email (`/api/send-email.js`) | Media |
| 13 | **CI/CD con GitHub Actions** (auto-deploy a Vercel tras PR merges, lint + build gates) | Media |
| 14 | **Sentry** para capturar errores en producción (`api/*.js` + js) | Fácil |
| 15 | **Uptime monitoring** de `/health`, `max.lifextreme.store`, `/api/send-email` con UptimeRobot Gratis | Fácil |
| 16 | Rotar limpiar GitHub history (revisar si la fuga de secreto quedó en commits anteriores) | Media |

---

## ✅ LO QUE YA ESTÁ BIEN (mérito real)

- Arquitectura modular Excelente (js modularizado, i18n ES/EN/PT nativo, el RAG híbrido determinista + vectorial es sofisticado)
- El flujo de reserva de "fraccionado 30/30/40" es un diferenciador comercial potente
- Headers de seguridad en `vercel.json` bien configurados
- Supabase como base relacional es la elección correcta
- El diseño y copy del frontend es inusualmente pulcro para estar pre-lanzamiento

---

## 📌 RESUMEN PARA FIRMAR HOY

Tu plataforma tiene la arquitectura correcta y visualmente se ve producción. Lo que la mata HOY son:

1. **El cerebro está caído** → el 90% de la magia (IA + cierre en WhatsApp botón) no computa.
2. **La puerta maestra del castillo está en la puerta del castillo** → la SERVICE KEY de Supabase es visible por cualquier usuario que haga ctrl+U.
3. **Datos de terceros (prospectos B2B) en el espacio público** → riesgo de ley de datos.

Estos tres puntos se arreglan en **1 día de trabajo**. El resto (VPS 24/7, PayPal real, tests, CI-CD) es la semana siguiente.

---

*Cambios recomendados sin tocar el sistema y con impacto directo en tu conversión.*

— Buffy, Codebuff
