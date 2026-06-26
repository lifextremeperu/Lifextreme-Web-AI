@echo off
chcp 65001 >nul
:: ============================================================
:: iniciar_MAX.bat — Lanzador Completo del Chatbot MAX
:: Lifextreme AI | Doble-clic para activar todo
:: ============================================================

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   MAX CHATBOT — LIFEXTREME AI OS         ║
echo  ║   Backend + Tunnel + Deploy Automatico   ║
echo  ╚══════════════════════════════════════════╝
echo.

set PROJECT_DIR=%~dp0
set CLOUDFLARED=C:\Users\ASUS\cloudflared.exe
set LOG_FILE=C:\Users\ASUS\cloudflared_url.log
set INDEX_HTML=%PROJECT_DIR%index.html

:: ── PASO 1: Verificar Ollama ──────────────────────────────
echo [1/4] Verificando Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo   Iniciando Ollama...
    start "" ollama serve
    timeout /t 4 /nobreak >nul
) else (
    echo   OK: Ollama activo
)

:: ── PASO 2: Iniciar FastAPI Backend ──────────────────────
echo [2/4] Iniciando backend FastAPI en puerto 8000...
start "MAX-Backend" cmd /k "cd /d "%PROJECT_DIR%" && python -m uvicorn backend.src.server:app --host 0.0.0.0 --port 8000"
timeout /t 6 /nobreak >nul
echo   OK: Backend corriendo en http://localhost:8000

:: ── PASO 3: Iniciar Cloudflare Tunnel y capturar URL ─────
echo [3/4] Iniciando Cloudflare Tunnel...
if exist "%LOG_FILE%" del "%LOG_FILE%"
start "MAX-Tunnel" cmd /k "%CLOUDFLARED% tunnel --url http://localhost:8000 --logfile "%LOG_FILE%""
echo   Esperando URL publica (15 segundos)...
timeout /t 15 /nobreak >nul

:: Extraer URL del log via PowerShell
for /f "delims=" %%i in ('powershell -Command "if(Test-Path '%LOG_FILE%'){$c=Get-Content '%LOG_FILE%' -Raw;if($c -match 'https://[a-z0-9-]+\.trycloudflare\.com'){$Matches[0]}else{'NO_URL'}}"') do set TUNNEL_URL=%%i

if "%TUNNEL_URL%"=="NO_URL" (
    echo   ERROR: No se pudo obtener la URL. Revisa la ventana del tunnel.
    pause
    exit /b 1
)
echo   OK: URL publica = %TUNNEL_URL%

:: ── PASO 4: Actualizar index.html y hacer push a GitHub ──
echo [4/4] Actualizando index.html y desplegando en Vercel...
powershell -Command ^
  "$f='%INDEX_HTML%'.Replace('%%','%%');$c=Get-Content $f -Raw -Encoding UTF8;$old='window.LIFEXTREME_BACKEND_URL = \'http://localhost:8000\';';$old2=[regex]::Match($c,\"window\.LIFEXTREME_BACKEND_URL = '([^']+)';\").Value;if($old2){$new=\"window.LIFEXTREME_BACKEND_URL = '%TUNNEL_URL%';\";$c=$c.Replace($old2,$new);Set-Content $f $c -Encoding UTF8 -NoNewline;Write-Host 'index.html actualizado: %TUNNEL_URL%'}else{Write-Host 'No se encontro la linea de URL en index.html'}"

cd /d "%PROJECT_DIR%"
git add index.html
git commit -m "chore: actualizar tunnel URL a %TUNNEL_URL%"
git push origin main

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   ✅ MAX CHATBOT ACTIVO EN PRODUCCION   ║
echo  ║   Vercel desplegara en ~30 segundos     ║
echo  ║   Prueba en: www.lifextreme.store       ║
echo  ╚══════════════════════════════════════════╝
echo.
echo  URL Backend: %TUNNEL_URL%
echo.
pause
