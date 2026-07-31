@echo off
title Lifextreme B2B - Piloto Automatico Nacional
color 0A

echo =======================================================
echo     LIFEXTREME B2B - PROSPECCION NACIONAL MASIVA
echo =======================================================
echo.
echo ESTA ACCION TOMARA APROXIMADAMENTE 30 A 45 MINUTOS.
echo VERAS EL NAVEGADOR ABRIRSE Y CERRARSE MULTIPLES VECES.
echo POR FAVOR NO CIERRES EL NAVEGADOR HASTA QUE TERMINE EL PROCESO.
echo.
pause

cd /d "%~dp0"
cd scraper

python scraper_nacional.py

echo.
echo =======================================================
echo                PROCESO FINALIZADO
echo =======================================================
echo Ya puedes ejecutar cerebro_operator_filter.py para filtrar
echo a los revendedores y quedarte solo con operadores directos.
echo.
pause
