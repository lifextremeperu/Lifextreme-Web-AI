$body = @{
    host = "www.lifextreme.store"
    key = "6b273d72c060439da28d58ec61809f4a"
    keyLocation = "https://www.lifextreme.store/6b273d72c060439da28d58ec61809f4a.txt"
    urlList = @(
        "https://www.lifextreme.store/",
        "https://www.lifextreme.store/empresa.html",
        "https://www.lifextreme.store/embajadores.html",
        "https://www.lifextreme.store/community.html",
        "https://www.lifextreme.store/recompensas.html",
        "https://www.lifextreme.store/investors.html",
        "https://www.lifextreme.store/blog.html",
        "https://www.lifextreme.store/blog-article.html",
        "https://www.lifextreme.store/destinos/global.html",
        "https://www.lifextreme.store/destinos/peru.html",
        "https://www.lifextreme.store/destinos/cusco.html",
        "https://www.lifextreme.store/destinos/arequipa.html",
        "https://www.lifextreme.store/destinos/lima.html",
        "https://www.lifextreme.store/destinos/amazonas.html",
        "https://www.lifextreme.store/destinos/ancash.html",
        "https://www.lifextreme.store/destinos/piura.html",
        "https://www.lifextreme.store/destinos/turismo.html",
        "https://www.lifextreme.store/partners/",
        "https://www.lifextreme.store/partners/registro.html",
        "https://www.lifextreme.store/registro-guia.html",
        "https://www.lifextreme.store/seguros.html",
        "https://www.lifextreme.store/privacidad.html",
        "https://www.lifextreme.store/terminos.html",
        "https://www.lifextreme.store/cookies.html",
        "https://www.lifextreme.store/reclamaciones.html",
        "https://www.lifextreme.store/politica-proveedores.html"
    )
} | ConvertTo-Json -Depth 3

Write-Host "Enviando 26 URLs a IndexNow..." -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri "https://api.indexnow.org/indexnow" -Method POST -ContentType "application/json; charset=utf-8" -Body $body
    Write-Host "EXITO! Codigo HTTP: $($response.StatusCode)" -ForegroundColor Green
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    Write-Host "Codigo HTTP: $code" -ForegroundColor Yellow
    if ($code -eq 200 -or $code -eq 202) {
        Write-Host "URLs enviadas correctamente!" -ForegroundColor Green
    }
}
