# Script de instalacin rpida de Greenflare SEO Crawler para Windows
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " INSTALADOR DE GREENFLARE SEO CRAWLER" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$Url = "https://github.com/greenflare/greenflare/releases/latest/download/greenflare-windows.zip"
$ZipDest = "$PSScriptRoot\..\tmp\greenflare.zip"
$ExtractDest = "$PSScriptRoot\..\tools\greenflare"

# Crear carpetas si no existen
if (!(Test-Path "$PSScriptRoot\..\tmp")) { New-Item -ItemType Directory -Force -Path "$PSScriptRoot\..\tmp" | Out-Null }
if (!(Test-Path "$ExtractDest")) { New-Item -ItemType Directory -Force -Path "$ExtractDest" | Out-Null }

Write-Host "[1/3] Descargando Greenflare (puede tardar un momento)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $Url -OutFile $ZipDest -UseBasicParsing

Write-Host "[2/3] Extrayendo archivos..." -ForegroundColor Yellow
Expand-Archive -Path $ZipDest -DestinationPath $ExtractDest -Force

Write-Host "[3/3] Limpiando archivos temporales..." -ForegroundColor Yellow
Remove-Item -Path $ZipDest -Force

Write-Host "`nInstalacin Completa!" -ForegroundColor Green
Write-Host "Puedes iniciar Greenflare yendo a la carpeta:" -ForegroundColor White
Write-Host (Resolve-Path $ExtractDest).Path -ForegroundColor Cyan
Write-Host "Y abriendo el archivo .exe" -ForegroundColor White
