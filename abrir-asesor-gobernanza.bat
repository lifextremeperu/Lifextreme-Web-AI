@echo off
chcp 65001 >nul
title GovAI Studio 4D - Asesor de Arquitectura y Gobernanza IA (Puerto 8090)
color 0B
echo =====================================================================
echo   INICIANDO GOVAI STUDIO 4D (ESTILO CHATGPT / GEMINI + QDRANT 18.9K)
echo   Abriendo http://localhost:8090/asesor-gobernanza.html ...
echo =====================================================================
start http://localhost:8090/asesor-gobernanza.html
python scripts\governance_studio_server.py
pause
