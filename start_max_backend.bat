@echo off
:: ============================================================
:: start_max_backend.bat - Inicia el backend MAX + Tunnel
:: Lifextreme Web AI | Ejecutar como: start_max_backend.bat
:: ============================================================

echo.
echo  ====================================================
echo   MAX BACKEND LAUNCHER - Lifextreme AI OS
echo  ====================================================
echo.

:: Verificar que Ollama este corriendo
echo [1/3] Verificando Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo   ERROR: Ollama no esta corriendo. Iniciando...
    start "" ollama serve
    timeout /t 3 /nobreak >nul
) else (
    echo   OK: Ollama activo.
)

:: Iniciar FastAPI backend en background
echo.
echo [2/3] Iniciando FastAPI (puerto 8000)...
start "MAX Backend" cmd /k "cd /d "%~dp0" && python -m uvicorn backend.src.server:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo   OK: Backend iniciado en http://localhost:8000

:: Iniciar Cloudflare Tunnel
echo.
echo [3/3] Iniciando tunnel publico con Cloudflare...
echo   La URL publica aparecera en la ventana de cloudflared.
echo   Copia esa URL y actualiza LIFEXTREME_BACKEND_URL en index.html
echo.
start "MAX Tunnel" cmd /k "cloudflared tunnel --url http://localhost:8000"

echo.
echo  ====================================================
echo   PASOS SIGUIENTES:
echo   1. Copia la URL de la ventana de cloudflared
echo      (formato: https://XXXX.trycloudflare.com)
echo   2. Esa URL ya esta configurada en el chatbot
echo      del frontend via js/max-chatbot.js
echo  ====================================================
echo.
pause
