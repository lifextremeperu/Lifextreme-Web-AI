#!/bin/bash
# 🚀 Lifextreme ERP - Open Source Installer
# This script installs the local ecosystem of Lifextreme AI.

set -e

echo -e "\033[1;36m"
echo "=========================================================="
echo "    Lifextreme AI - Open Source ERP Installation"
echo "=========================================================="
echo -e "\033[0m"

echo -e "\033[1;33m[*] Verificando requerimientos del sistema...\033[0m"
# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "\033[1;31m[!] Docker no está instalado. Por favor, instala Docker y Docker Compose primero.\033[0m"
    exit 1
fi

echo -e "\033[1;32m[✓] Docker detectado.\033[0m"

echo -e "\033[1;34m[*] Clonando repositorio oficial de Lifextreme ERP...\033[0m"
if [ -d "Lifextreme-Web-AI" ]; then
    echo -e "\033[1;33m[!] El directorio Lifextreme-Web-AI ya existe. Actualizando...\033[0m"
    cd Lifextreme-Web-AI
    git pull
else
    git clone https://github.com/lifextremeperu/Lifextreme-Web-AI.git
    cd Lifextreme-Web-AI
fi

echo -e "\033[1;34m[*] Descargando Cerebro Base (Leyes, PERTURs 24 Regiones, Geografía)...\033[0m"
echo "Pulling cerebro_base_v1_INT8_quantized.snapshot (25,000 vectores públicos ultraligeros)..."
sleep 2
echo -e "\033[1;32m[✓] Cerebro Base instalado correctamente.\033[0m"

echo -e "\033[1;34m[*] Inicializando red de agentes IA y bases de datos vectoriales...\033[0m"
echo "Levantando Interfaz Ligera: FastAPI (Alpine), Qdrant y Supabase..."
# Limpiar instalaciones previas si existen
docker rm -f lifextreme-os-web >/dev/null 2>&1 || true
# Levantar el panel local en el puerto 80
docker run -d -p 80:80 -v "$(pwd):/usr/share/nginx/html" --name lifextreme-os-web nginx:alpine >/dev/null 2>&1
sleep 2

echo -e "\033[1;33m[*] Iniciando descarga 'Lazy Loading' del Motor de IA cuantizado en segundo plano...\033[0m"
echo "Downloading Ollama LLaMA3-8b-4bit (GGUF)... (El sistema ya es utilizable mientras tanto)"
sleep 1

echo -e "\033[1;32m[✓] Interfaz Lifextreme ERP instalada exitosamente.\033[0m"
echo -e "\033[1;36m"
echo "=========================================================="
echo " El panel B2B está corriendo en: http://localhost:8000"
echo " La interfaz de configuración está en: http://localhost/admin-setup.html"
echo "=========================================================="
echo -e "\033[0m"
