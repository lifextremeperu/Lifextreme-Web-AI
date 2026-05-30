Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  ORQUESTADOR AUTOMATICO: BLOQUE 3 Y 4 (ANCASH)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

Start-Sleep -Seconds 10

Write-Host "`n[>>>] INICIANDO CARTOGRAFO - BLOQUE 3" -ForegroundColor Yellow
python scripts\run_cartographer_batch.py ancash --batch 3

Write-Host "`n[>>>] INICIANDO MINERO PROFUNDO - BLOQUE 3" -ForegroundColor Yellow
python scripts\run_miner_latam.py ancash

Write-Host "`n[>>>] INICIANDO CARTOGRAFO - BLOQUE 4" -ForegroundColor Yellow
python scripts\run_cartographer_batch.py ancash --batch 4

Write-Host "`n[>>>] INICIANDO MINERO PROFUNDO - BLOQUE 4" -ForegroundColor Yellow
python scripts\run_miner_latam.py ancash

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "  MINERIA TOTAL DE ANCASH COMPLETADA (60 MODULOS)" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
