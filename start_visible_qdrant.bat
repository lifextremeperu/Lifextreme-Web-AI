@echo off
title Orquestador de Ingesta Qdrant - Lifextreme AI
color 0A

echo =======================================================
echo 🚀 INICIANDO MOTOR VECTORIAL QDRANT (Puerto 6333)
echo =======================================================
docker-compose -f docker-compose.qdrant.yml up -d
echo.
echo [*] Esperando inicializacion de Qdrant...
timeout /t 5 >nul
echo.
echo =======================================================
echo 🧠 INYECTANDO VECTORES GUBERNAMENTALES (TIER 0)
echo =======================================================
python scripts\queue_to_qdrant.py

echo.
echo =======================================================
echo ✅ FINALIZADO. Enviando mensaje de confirmacion a Telegram...
echo =======================================================
python -c "import sys; sys.path.append('.'); from scripts.telegram_notifier import send_message; send_message('✅ *MAX - Actualización Completa*\n\nLa inyección masiva de normativas gubernamentales (SUTRAN, OSINERGMIN, MEF, MINCU) a la bóveda vectorial Qdrant (Tier 0) ha finalizado con éxito.\n\nLa IA ya opera como *Experto Consultor Gubernamental*.')"

echo.
echo [!] Proceso terminado. Puedes cerrar esta ventana.
pause
