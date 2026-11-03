# 🔑 ROTACIÓN DE CLAVE SUPABASE — PLAN EXACTO (30–45 min)

> **Por qué es urgente:** la clave `sb_secret_7d_j2u37-hVXO_2VkvCc8A_tEaP_LDS` está en
> `admin-setup.html` y `create-partner.html`, servidas al mundo por el CDN. Con esa clave
> cualquiera lee/borra/edita TODAS tus tablas, saltándose los permisos RLS.
> Cada minuto que sigue publicada es exposición real.

---

## PARTE 1 — Rotar la clave en Supabase (10 min)

1. Entra a https://supabase.com/dashboard
2. Abre el proyecto `zobpkmiqrvhbepqnjshr` (tu backend Lifextreme)
3. Menú lateral → **Project Settings** (⚙️) → **API**
4. Localiza **Service role key** (la que empieza con `sb_secret_`)
5. Pulsa el botón **Rotate** (o "Roll key") → Supabase te muestra la **clave nueva una sola vez**: cópiala de inmediato en un gestor de contraseñas. La vieja queda invalidada en ese momento.
   - Si tu plan/versión no muestra "Rotate": en Settings → API → "Legacy API keys" → **Delete/revoke** la `sb_secret_` actual y crea una nueva "Secret key".
6. NO cierres la pestaña sin haber copiado la clave nueva.

## PARTE 2 — Actualizar los 2 lugares donde vive (15 min)

La clave nueva solo debe existir en **variables de entorno del servidor**, nunca en HTML.

### a) Vercel (para `api/webhooks/stripe-sentinel.js` y futuras functions)
1. Dashboard Vercel → proyecto **lifextreme** → **Settings** → **Environment Variables**
2. Crea/actualiza:
   - `SUPABASE_URL` = `https://zobpkmiqrvhbepqnjshr.supabase.co`
   - `SUPABASE_SERVICE_ROLE_KEY` = *(la clave nueva guardada en el paso PARTE 1-5)*
3. Marca Production + Preview + Development
4. Tras guardar, **obligatorio**: Deployments → último deploy → **⋯ → Redeploy** (las env vars solo entran en un deploy nuevo)

### b) Tu PC local (tools admin que sí usan service key de forma legítima)
- Si tenías la clave en `.env`: actualízala a `SUPABASE_SERVICE_ROLE_KEY=<clave nueva>`
- En los scripts Python que la leen (`create_rpc_function.py`, `check_supabase_schema.py`, `check_rag.py`) ya usan `os.getenv("SUPABASE_URL")` / similar → solo cambia el `.env`

## PARTE 3 — Quitar la clave vieja del CDN y del repo (15 min)

1. Ya está hecho en este repo con el `.vercelignore` actualizado (admin pages no se despliegan). Verifica al redeploy:
   ```
   https://www.lifextreme.store/admin-setup.html   → debe dar 404
   https://www.lifextreme.store/create-partner.html → debe dar 404
   ```
2. Para que la clave vieja NO quede en el historial de GitHub:
   ```bash
   git rm --cached admin-setup.html create-partner.html
   # muévelas a una carpeta privada fuera del deploy (opción simple)
   ```
   Y en `deploy.ps1` el `git add .` seguiría re-agregándolas → sustituye esa línea por:
   ```powershell
   git add -u
   git ls-files --others --exclude-standard | Where-Object { $_ -notmatch '^admin-setup\.html$|^create-partner\.html$|\.csv$|\.md$' } | ForEach-Object { git add $_ }
   ```
3. **Opcional pero recomendado (semana 1):** limpiar el historial con BFG:
   `bfg --delete-files admin-setup.html` → `git reflog expire --expire=now --all && git gc --prune=now --aggressive`
   → reescribe el repo; avísame si quieres que lo haga contigo paso a paso (fuerza un push con `--force`).

## PARTE 4 — Verificación final (5 min)

| Check | Comando / acción | Esperado |
|---|---|---|
| Clave vieja muerta | Con la `sb_secret` vieja: `curl https://zobpkmiqrvhbepqnjshr.supabase.co/rest/v1/ -H "apikey: VIEJA"` | `401/403` |
| Clave nueva funciona | igual pero con clave nueva desde tu `.env` | `200` y lista de tablas |
| CDN limpio | abrir las URLs de admin en navegador | `404` |
| Web de reservas viva | crear una reserva de prueba en lifextreme.store | guarda en `bookings` |

⚠️ **Después de rotar:** cualquier integración que usara la clave vieja (n8n, scripts locales, informes agencias) hay que actualizarla, o dejará de conectar. Busca "sb_secret" en tu equipo para recordar dónde vivía:
`findstr /s /m "sb_secret" *.* ` (Windows) — te listo qué actualizar.

---

*Origen: paso 1 del plan DÍA 1 de [AUDITORIA_PRODUCCION_LIFEXTREME.md](AUDITORIA_PRODUCCION_LIFEXTREME.md)*
