param (
    [string]$backupName = "Lifextreme_AI_Respaldo_Maestro"
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$destinationFile = "$PSScriptRoot\${backupName}_${timestamp}.zip"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  INICIANDO RESPALDO MAESTRO - LIFEXTREME AI" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Directorios y archivos críticos a respaldar
$itemsToBackup = @(
    "src",
    "scripts",
    "data",
    ".env",
    "*.md",
    "*.json",
    "*.py"
)

# Filtramos los archivos que realmente existen para evitar errores
$validItems = @()
foreach ($item in $itemsToBackup) {
    if (Test-Path $item) {
        $validItems += $item
    }
}

Write-Host "[+] Comprimiendo el ecosistema en: $destinationFile" -ForegroundColor Yellow

# Comprimir ignorando bloqueos temporales de archivos abiertos
Compress-Archive -Path $validItems -DestinationPath $destinationFile -Force -ErrorAction SilentlyContinue

if (Test-Path $destinationFile) {
    Write-Host "[+] Respaldo Maestro creado con éxito." -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "Archivo: $destinationFile" -ForegroundColor White
} else {
    Write-Host "[-] Hubo un problema al crear el respaldo." -ForegroundColor Red
}

Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
