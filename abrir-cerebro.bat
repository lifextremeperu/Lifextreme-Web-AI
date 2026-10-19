@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==============================================
echo   LX NeuroMap - el cerebro vivo de Lifextreme
echo ==============================================
if not exist neuromap\data\brain.json (
  echo [1/2] Indexando Qdrant por primera vez ^(~1 min^)...
  .venv\Scripts\python.exe neuromap\indexer.py
)
echo [2/2] Abriendo el visor en http://localhost:8765
start "" http://localhost:8765
.venv\Scripts\python.exe neuromap\server.py
