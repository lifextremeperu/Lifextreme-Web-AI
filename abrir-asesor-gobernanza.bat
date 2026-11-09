@echo off
chcp 65001 >nul
title Asesor Senior de Arquitectura y Gobernanza IA (Qdrant 18,932 Vectores)
color 0B
echo =====================================================================
echo   CONSORCIO DE ARQUITECTURA Y GOBERNANZA DE IA - CUSCO, PERU (2026)
echo   Motor RAG: Qdrant `peru_ai_governance` (18,932 vectores Tier 1)
echo =====================================================================
echo.
python scripts\generar_expediente.py %*
echo.
pause
