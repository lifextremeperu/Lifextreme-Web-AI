#!/bin/bash
# ==============================================================================
# LIFEXTREME OS - SCRIPT DE INSTALACIÓN "UN CLIC" (PILOTO)
# Este script simula lo que experimentará una agencia al instalar tu sistema.
# ==============================================================================

# Colores para que se vea elegante en la terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "    __    __________________  ____________  _____  ___  ___  _____"
echo "   / /   /  _/ ____/ ____/ / / /_  __/ __ \/ __ \/  |/  / |/ / __ \\"
echo "  / /    / // /_  / __/ / /_/ / / / / /_/ / / / / /|_/ /    / / / /"
echo " / /____/ // __/ / /___/ __  / / / / _, _/ /_/ / /  / / /|  / /_/ / "
echo "/_____/___/_/   /_____/_/ /_/ /_/ /_/ |_|\____/_/  /_/_/ |_/\____/  "
echo -e "${NC}"
echo -e "${GREEN}Bienvenido al instalador automatizado de Lifextreme AI OS.${NC}"
echo "Iniciando proceso de validación e instalación..."
echo "------------------------------------------------------------------"
sleep 2

# 1. Verificar si Docker está instalado
echo -n "[1/4] Verificando Docker... "
if command -v docker &> /dev/null; then
    echo -e "${GREEN}¡Docker detectado!${NC}"
else
    echo -e "${YELLOW}No se encontró Docker. Instalando automáticamente...${NC}"
    # En la vida real, aquí ejecutaríamos: curl -fsSL https://get.docker.com | bash
    sleep 2
    echo -e "${GREEN}Docker instalado exitosamente (Simulado).${NC}"
fi

# 2. Verificar Docker Compose
echo -n "[2/4] Verificando Docker Compose... "
if docker compose version &> /dev/null; then
    echo -e "${GREEN}¡Docker Compose detectado!${NC}"
else
    echo -e "${YELLOW}No se encontró Docker Compose. Instalando...${NC}"
    sleep 1
    echo -e "${GREEN}Docker Compose instalado exitosamente (Simulado).${NC}"
fi

# 3. Descargar el entorno (Simulado)
echo -e "[3/4] Preparando el entorno de Lifextreme... "
INSTALL_DIR="lifextreme-agencia-demo"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}El directorio $INSTALL_DIR ya existe. Actualizando...${NC}"
else
    mkdir "$INSTALL_DIR"
    echo -e "${GREEN}Directorio creado: $INSTALL_DIR${NC}"
fi

cd "$INSTALL_DIR" || exit

# En la vida real, aquí haríamos un "git clone" o "wget" del docker-compose.yml de tu GitHub.
# Para este piloto, el script creará un compose básico en el momento.
echo -e "${BLUE}>>> Descargando Arquitectura Lifextreme (docker-compose.yml)...${NC}"
cat << 'EOF' > docker-compose.yml
version: '3.8'
services:
  # Base de Datos Vectorial (El Cerebro RAG)
  qdrant_demo:
    image: qdrant/qdrant:latest
    container_name: lx_qdrant_demo
    ports:
      - "6335:6333" # Usamos 6335 para no chocar con tu Qdrant actual
    restart: unless-stopped
    
  # Servidor Web Frontend (Simulado)
  frontend_demo:
    image: nginx:alpine
    container_name: lx_frontend_demo
    ports:
      - "8085:80" # Usamos 8085 para la demo
    restart: unless-stopped
EOF
sleep 2

# 4. Levantar el sistema
echo -e "[4/4] Encendiendo el Ecosistema IA..."
# Ejecutamos docker compose
docker compose up -d

echo "------------------------------------------------------------------"
echo -e "${GREEN}¡INSTALACIÓN COMPLETADA CON ÉXITO! 🚀${NC}"
echo "------------------------------------------------------------------"
echo -e "Tu sistema privado Lifextreme ya está operativo."
echo -e "👉 ${BLUE}Frontend de la Agencia:${NC} http://localhost:8085"
echo -e "👉 ${BLUE}Cerebro Vectorial (API):${NC} http://localhost:6335"
echo -e ""
echo -e "${YELLOW}Nota: Este es un piloto. Para detenerlo, ejecuta:${NC}"
echo "cd $INSTALL_DIR && docker compose down"
echo "=================================================================="
