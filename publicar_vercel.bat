@echo off
echo ==============================================================
echo   INICIANDO ACTUALIZACION AUTOMATICA HACIA GITHUB Y VERCEL
echo ==============================================================

echo [1/3] Añadiendo todos los nuevos archivos e imagenes 4K...
git add .

echo [2/3] Creando punto de guardado (Commit)...
git commit -m "feat(content): Inyectar 164 Parques de Aventura, Imagenes 4K y Sincronizar MCP Backend"

echo [3/3] Preparando y publicando Lifextreme Web en Vercel...

echo Construyendo indice de Blog SEO...
python scripts/build_blog.py

echo Sincronizando con GitHub...
git push origin main

echo ==============================================================
echo   ¡PROCESO COMPLETADO!
echo   Vercel esta compilando la nueva version de www.lifextreme.store
echo   Tardara 1-2 minutos en estar en vivo.
echo ==============================================================
pause
