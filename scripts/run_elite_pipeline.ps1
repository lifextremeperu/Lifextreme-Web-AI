# run_elite_pipeline.ps1
# Orquestador automatizado para SEO Local de Lifextreme

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " INICIANDO PIPELINE DE SEO Y CONTENIDO AUTOMATIZADO" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Fase 1: Asegurarnos de que los 50 originales se refactoricen
Write-Host "`n[Fase 1] Refactorizando los 50 artículos originales..." -ForegroundColor Yellow
python scripts\agent_seo_refactor_local.py

# Fase 2: Lanzar la generación de los 50 nuevos
Write-Host "`n[Fase 2] Generando 50 artículos nuevos de Elite con RAG Qdrant..." -ForegroundColor Yellow
python scripts\agent_batch_seo_elite50.py

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " PIPELINE COMPLETADO EXITOSAMENTE" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
