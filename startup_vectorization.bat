@echo off
cd "c:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI"
echo Iniciando motor de IA local Ollama...
start /B ollama serve
timeout /t 5 >nul
echo Reanudando vectorizacion automatica...
set PYTHONIOENCODING=utf-8
python scripts\revectorize_nomic.py
pause
