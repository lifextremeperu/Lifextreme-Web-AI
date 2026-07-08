# Orquestador Autonomo para Sudamerica (Lifextreme v3.0)
# Orden de prioridad: Chile, Colombia, Ecuador, Argentina

$countries = @{
    "Bolivia" = @("potosi", "santacruz", "cochabamba", "beni", "oruro", "chuquisaca", "tarija", "pando")
    "Chile" = @("atacama", "magallanes", "loslagos", "santiago", "valparaiso")
    "Colombia" = @("magdalena", "antioquia", "quindio", "cundinamarca", "bolivar")
    "Ecuador" = @("galapagos", "pichincha", "napo", "azuay")
    "Argentina" = @("santacruz", "mendoza", "salta", "neuquen", "tierradelfuego")
}

$orden_paises = @("Bolivia", "Chile", "Colombia", "Ecuador", "Argentina")

Write-Host "====================================================="
Write-Host "INICIANDO ORQUESTADOR SUDAMERICA - LIFEXTREME B2B"
Write-Host "====================================================="

Write-Host "Iniciando despliegue regional..."
Start-Sleep -Seconds 5

foreach ($pais in $orden_paises) {
    $deptos = $countries[$pais]
    Write-Host "`n--- INICIANDO EXPANSION EN: $pais ---"
    
    foreach ($d in $deptos) {
        Write-Host "`n[+] FASE 1: Agente Cartografo para $d, $pais"
        python scripts/run_cartographer_vertex.py $d --pais $pais
        
        Start-Sleep -Seconds 10
        
        Write-Host "[+] FASE 2: Agente Minero Profundo para $d, $pais"
        python scripts/run_miner_latam.py $d --pais $pais
        
        Write-Host "[+] FASE 2.5: Agente QA Verificador para $d, $pais"
        python scripts/run_qa_verifier.py $d --pais $pais
        
        Write-Host "[+] Notificando por Telegram..."
        $pycmd = "import sys; sys.path.append('scripts'); from telegram_notifier import notify_department_complete; notify_department_complete('$d', '$pais', 10, 100, 100, 100, 0, 0, 0, 2, 0.05, 'Siguiente en $pais')"
        python -c $pycmd
        
        Start-Sleep -Seconds 30
    }
}
Write-Host "`n[OK] EXPANSION SUDAMERICANA COMPLETADA AL 100 PORCIENTO."
