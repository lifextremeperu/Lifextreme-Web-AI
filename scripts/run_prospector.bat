@echo off
title Lifextreme B2B Prospector (IA Maps Scraper)
color 0B

echo =======================================================
echo          LIFEXTREME B2B PROSPECTOR (IA SCRAPER)
echo =======================================================
echo.
echo Iniciando verificacion de dependencias del sistema...
echo.

cd /d "%~dp0"
cd scraper

echo [1/3] Verificando e instalando librerias de Python...
pip install -r requirements.txt -q

echo [2/3] Verificando navegadores fantasma (Playwright)...
python -m playwright install chromium

echo.
echo =======================================================
echo                  CONFIGURACION DE BUSQUEDA
echo =======================================================
echo Ejemplo de busqueda: "agencias de turismo en Cusco"
echo Ejemplo de busqueda: "operadores de aventura en Huaraz"
echo.

set /p busqueda="Introduce los terminos de busqueda: "
set /p cantidad="Cuantos resultados deseas raspar (ej. 20, 50, 100): "

echo.
echo [3/3] Iniciando la extraccion de datos en vivo...
echo POR FAVOR NO CIERRES EL NAVEGADOR QUE SE ABRIRA AUTOMATICAMENTE
echo.

python main.py -s "%busqueda%" -t %cantidad% -o "../../Lifextreme_B2B_Prospects.csv"

echo.
echo =======================================================
echo                PROSPECCION COMPLETADA
echo =======================================================
echo Los resultados han sido guardados en la carpeta principal
echo del proyecto con el nombre: Lifextreme_B2B_Prospects.csv
echo.
pause
