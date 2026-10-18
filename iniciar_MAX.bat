@echo off
chcp 65001 >nul
:: ============================================================
:: iniciar_MAX.bat — Lanzador Oficial del Chatbot MAX
:: Conecta al tunel permanente: https://max.lifextreme.store
:: ============================================================

echo.
echo  ====================================================
echo   MAX CHATBOT — LIFEXTREME AI OS (Produccion)
echo   Dominio Backend: https://max.lifextreme.store
echo  ====================================================
echo.

set PROJECT_DIR=%~dp0
set CLOUDFLARED=C:\Users\ASUS\cloudflared.exe
set TUNNEL_ID=53e9fbf9-6af1-41ac-84e2-b72ddf5b08b5

:: ── PASO 1: Liberar puerto 8000 si el contenedor viejo esta activo ──
echo [1/4] Verificando puerto 8000 y Qdrant (6333)...
docker stop lifextreme-os-api >nul 2>&1
docker start rag_lifextreme >nul 2>&1

:: ── PASO 2: Verificar Ollama ──────────────────────────────
echo [2/4] Verificando Ollama (11434)...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo   Iniciando Ollama...
    start "" ollama serve
    timeout /t 4 /nobreak >nul
) else (
    echo   OK: Ollama activo.
)

:: ── PASO 3: Iniciar FastAPI Backend (puerto 8000) ─────────
echo [3/4] Iniciando backend FastAPI en puerto 8000...
start "MAX-Backend" /min cmd /k "cd /d "%PROJECT_DIR%" && python -m uvicorn backend.src.server:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 5 /nobreak >nul
echo   OK: Backend corriendo en http://localhost:8000

:: ── PASO 4: Iniciar Cloudflare Tunnel Permanente ──────────
echo [4/4] Verificando Tunel Permanente (https://max.lifextreme.store)...
tasklist /FI "IMAGENAME eq cloudflared.exe" 2>NUL | find /I /N "cloudflared.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   OK: cloudflared ya esta activo.
) else (
    start "MAX-Tunnel" /min cmd /k "%CLOUDFLARED% tunnel run %TUNNEL_ID%"
    timeout /t 4 /nobreak >nul
    echo   OK: Tunel https://max.lifextreme.store iniciado.
)

echo.
echo  ====================================================
echo   MAX CHATBOT ACTIVO EN WWW.LIFEXTREME.STORE
echo   Healthcheck: https://max.lifextreme.store/health
echo  ====================================================
echo.
pause
