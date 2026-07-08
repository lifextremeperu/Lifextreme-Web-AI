# cleanup_cache.ps1 - Limpiador de cache Lifextreme
# Uso: .\cleanup_cache.ps1
# NO afecta codigo fuente ni datos del proyecto

$ProjectRoot = "c:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI"
$TotalFreed = 0

Write-Host ""
Write-Host "LIMPIADOR DE CACHE - LIFEXTREME WEB AI" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Python __pycache__
Write-Host "[1/5] Limpiando cache de Python (__pycache__)..." -ForegroundColor White
$caches = Get-ChildItem $ProjectRoot -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
foreach ($cache in $caches) {
    $size = (Get-ChildItem $cache.FullName -Recurse -File -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum).Sum
    $TotalFreed += $size
    Remove-Item $cache.FullName -Recurse -Force -ErrorAction SilentlyContinue
}
$pyc = Get-ChildItem $ProjectRoot -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue
foreach ($f in $pyc) {
    $TotalFreed += $f.Length
    Remove-Item $f.FullName -Force -ErrorAction SilentlyContinue
}
Write-Host "   OK: $($caches.Count) carpetas __pycache__ + $($pyc.Count) archivos .pyc eliminados" -ForegroundColor Green

# 2. Pytest y benchmarks
Write-Host "[2/5] Limpiando cache de tests..." -ForegroundColor White
foreach ($dir in @(".pytest_cache", ".benchmarks", ".mypy_cache", ".ruff_cache")) {
    $fullPath = Join-Path $ProjectRoot $dir
    if (Test-Path $fullPath) {
        $size = (Get-ChildItem $fullPath -Recurse -File -ErrorAction SilentlyContinue | 
                 Measure-Object -Property Length -Sum).Sum
        $TotalFreed += $size
        Remove-Item $fullPath -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "   OK: $dir eliminado ($([math]::Round($size/1MB,1)) MB)" -ForegroundColor Green
    }
}

# 3. Temporales
Write-Host "[3/5] Limpiando temporales (tmp/, scratch/)..." -ForegroundColor White
foreach ($dir in @("tmp", "scratch")) {
    $fullPath = Join-Path $ProjectRoot $dir
    if (Test-Path $fullPath) {
        $size = (Get-ChildItem $fullPath -Recurse -File -ErrorAction SilentlyContinue | 
                 Measure-Object -Property Length -Sum).Sum
        $TotalFreed += $size
        Remove-Item $fullPath -Recurse -Force -ErrorAction SilentlyContinue
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "   OK: $dir limpiado ($([math]::Round($size/1MB,1)) MB)" -ForegroundColor Green
    }
}

# 4. Archivos .gstmp (Google Sheets temp)
Write-Host "[4/5] Limpiando archivos temporales de Google (.gstmp)..." -ForegroundColor White
$gstmp = Get-ChildItem $ProjectRoot -Recurse -File -Filter "*.gstmp" -ErrorAction SilentlyContinue
foreach ($f in $gstmp) {
    $TotalFreed += $f.Length
    Remove-Item $f.FullName -Force -ErrorAction SilentlyContinue
}
Write-Host "   OK: $($gstmp.Count) archivos .gstmp eliminados" -ForegroundColor Green

# 5. Source maps de Node.js (fuera de node_modules)
Write-Host "[5/5] Limpiando source maps de Node.js (*.js.map)..." -ForegroundColor White
$maps = Get-ChildItem $ProjectRoot -Recurse -File -Filter "*.js.map" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notlike "*node_modules*" }
foreach ($f in $maps) {
    $TotalFreed += $f.Length
    Remove-Item $f.FullName -Force -ErrorAction SilentlyContinue
}
Write-Host "   OK: $($maps.Count) source maps eliminados" -ForegroundColor Green

# Resumen
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
$totalMB = [math]::Round($TotalFreed / 1MB, 2)
Write-Host "LIMPIEZA COMPLETA: $totalMB MB liberados" -ForegroundColor Green
Write-Host ""
Write-Host "CONSEJO: Reinicia el IDE para que tome efecto." -ForegroundColor Yellow
Write-Host "CONSEJO: Pausa OneDrive (clic derecho en bandeja) mientras trabajas." -ForegroundColor Yellow
Write-Host ""
