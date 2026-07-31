@echo off
title Certificacion Ragas x Qdrant
color 0E

echo =======================================================
echo    CERTIFICACION DE IA: LIFEXTREME VS QDRANT
echo =======================================================
echo.
echo Requisitos:
echo 1. Debes tener Ollama abierto en tu PC.
echo 2. El modelo "llama3" y "nomic-embed-text" deben estar listos.
echo.
pause

cd /d "%~dp0"
python ragas_qdrant_audit.py

echo.
pause
