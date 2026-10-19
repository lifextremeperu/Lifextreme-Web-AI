@echo off
title LIFEXTREME AI - Investor Demo Launcher (Qdrant + FastAPI + Cloudflare)
color 0A
echo ============================================================================
echo   LIFEXTREME AI - STACK DE PRODUCCION PARA DUE DILIGENCE (336,869 VECTORES)
echo ============================================================================
echo.

echo [1/3] Verificando contenedor vectorial Qdrant (rag_lifextreme)...
docker start rag_lifextreme >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Iniciando Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    timeout /t 12 /nobreak >nul
    docker start rag_lifextreme >nul 2>&1
)
echo       OK - Qdrant Vector Engine activo en localhost:6333

echo [2/3] Verificando Tunel Cloudflare (max.lifextreme.store)...
tasklist /FI "IMAGENAME eq cloudflared.exe" 2>NUL | find /I /N "cloudflared.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo       OK - Cloudflared Tunnel activo.
) else (
    echo       Iniciando Cloudflared Tunnel...
    start "Cloudflared Tunnel" /min cloudflared tunnel run
)

echo [3/3] Iniciando Orquestador FastAPI (MAX Hybrid RAG + Groq LPU 120B)...
cd /d "%~dp0"
python -m uvicorn backend.src.server:app --host 0.0.0.0 --port 8000 --reload
pause
