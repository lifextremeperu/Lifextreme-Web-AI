# Script de Deploy Rápido para Lifextreme
# Uso: .\deploy.ps1 "mensaje del commit"

param(
    [Parameter(Mandatory=$true)]
    [string]$mensaje
)

Write-Host "🚀 Iniciando deploy de Lifextreme..." -ForegroundColor Cyan
Write-Host ""

# 1. Verificar cambios
Write-Host "📋 Verificando cambios..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "¿Continuar con el deploy? (S/N): " -ForegroundColor Green -NoNewline
$confirmacion = Read-Host

if ($confirmacion -ne "S" -and $confirmacion -ne "s") {
    Write-Host "❌ Deploy cancelado" -ForegroundColor Red
    exit
}

# 2. Agregar todos los cambios
Write-Host ""
Write-Host "📦 Agregando archivos..." -ForegroundColor Yellow
git add .

# 3. Hacer commit
Write-Host "💾 Creando commit..." -ForegroundColor Yellow
git commit -m $mensaje

# 4. Push a GitHub
Write-Host "⬆️  Subiendo a GitHub..." -ForegroundColor Yellow
git push origin main

# 5. Confirmación
Write-Host ""
Write-Host "✅ ¡Deploy completado exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Tu sitio se está actualizando en:" -ForegroundColor Cyan
Write-Host "   https://www.lifextreme.store" -ForegroundColor White
Write-Host ""
Write-Host "📊 GitHub:" -ForegroundColor Cyan
Write-Host "   https://github.com/lifextremeperu/Lifextreme-Web-AI" -ForegroundColor White
Write-Host ""
Write-Host "⏱️  El sitio estará actualizado en 30-60 segundos" -ForegroundColor Yellow
