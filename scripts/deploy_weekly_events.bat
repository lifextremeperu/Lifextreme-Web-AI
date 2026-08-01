@echo off
echo ==============================================================
echo LIFEXTREME - AUTOMATIZACION SEMANAL DE EVENTOS (SearXNG + Git)
echo ==============================================================
echo.

:: 1. Cambiar al directorio del proyecto (Ajusta la ruta si es necesario)
cd "c:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI"

:: 2. Activar el entorno virtual si existe (Opcional, asumiendo Python global o .venv)
if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Activando entorno virtual...
    call .venv\Scripts\activate.bat
)

:: 3. Ejecutar el Agente de SearXNG (Python)
echo [INFO] Ejecutando agent_searxng_events.py...
python scripts\agent_searxng_events.py

:: 4. Verificar si hubo cambios en js/data.js
echo [INFO] Verificando cambios en el repositorio (Git)...
git status --porcelain | findstr "js/data.js" >nul
if %errorlevel% neq 0 (
    echo [INFO] No se agregaron nuevos eventos esta semana. Saliendo...
    goto :fin
)

:: 5. Hay cambios, hacer commit y push a Vercel
echo [INFO] Cambios detectados. Preparando despliegue a Vercel...
git add js\data.js
git commit -m "Auto-update: Nuevos eventos encontrados por SearXNG"
echo [INFO] Subiendo a GitHub para despliegue automatico en Vercel...
git push origin main

echo [EXITO] ¡Los nuevos eventos ya estan en proceso de publicacion en www.lifextreme.store!

:fin
echo.
echo Proceso finalizado.
