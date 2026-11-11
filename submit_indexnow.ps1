$body = @{
    host = "www.lifextreme.com.pe"
    key = "6b273d72c060439da28d58ec61809f4a"
    keyLocation = "https://www.lifextreme.com.pe/6b273d72c060439da28d58ec61809f4a.txt"
    urlList = @(
        "https://www.lifextreme.com.pe/",
        "https://www.lifextreme.com.pe/empresa.html",
        "https://www.lifextreme.com.pe/embajadores.html",
        "https://www.lifextreme.com.pe/community.html",
        "https://www.lifextreme.com.pe/recompensas.html",
        "https://www.lifextreme.com.pe/investors.html",
        "https://www.lifextreme.com.pe/blog.html",
        "https://www.lifextreme.com.pe/blog-article.html",
        "https://www.lifextreme.com.pe/destinos/global.html",
        "https://www.lifextreme.com.pe/destinos/peru.html",
        "https://www.lifextreme.com.pe/destinos/cusco.html",
        "https://www.lifextreme.com.pe/destinos/arequipa.html",
        "https://www.lifextreme.com.pe/destinos/lima.html",
        "https://www.lifextreme.com.pe/destinos/amazonas.html",
        "https://www.lifextreme.com.pe/destinos/ancash.html",
        "https://www.lifextreme.com.pe/destinos/piura.html",
        "https://www.lifextreme.com.pe/destinos/turismo.html",
        "https://www.lifextreme.com.pe/partners/",
        "https://www.lifextreme.com.pe/partners/registro.html",
        "https://www.lifextreme.com.pe/registro-guia.html",
        "https://www.lifextreme.com.pe/seguros.html",
        "https://www.lifextreme.com.pe/privacidad.html",
        "https://www.lifextreme.com.pe/terminos.html",
        "https://www.lifextreme.com.pe/cookies.html",
        "https://www.lifextreme.com.pe/reclamaciones.html",
        "https://www.lifextreme.com.pe/politica-proveedores.html"
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
