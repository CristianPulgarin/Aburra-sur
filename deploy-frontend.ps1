# Compila el frontend apuntando al backend (Hugging Face Space) y lo publica en Firebase Hosting.
# Uso:
#   .\deploy-frontend.ps1 -ProjectId mi-proyecto -ApiUrl https://aburrasegura-api.onrender.com
# La primera vez pide iniciar sesión en Firebase (se abre el navegador).
param(
    [Parameter(Mandatory = $true)][string]$ProjectId,
    [Parameter(Mandatory = $true)][string]$ApiUrl
)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$ApiUrl = $ApiUrl.TrimEnd('/')

Write-Host "> Comprobando backend en $ApiUrl/health (si está dormido tarda ~1 minuto)..." -ForegroundColor Cyan
try { Invoke-RestMethod "$ApiUrl/health" -TimeoutSec 90 | Out-Null; Write-Host '  Backend en línea.' -ForegroundColor Green }
catch { Write-Warning "El backend no respondió. El frontend se publicará igual; revisa el Space en Hugging Face." }

Push-Location (Join-Path $root 'frontend')
try {
    if (-not (Test-Path 'node_modules')) { npm install }
    $env:VITE_API_URL = $ApiUrl
    npm run build
    if ($LASTEXITCODE -ne 0) { throw 'Falló la compilación del frontend.' }
} finally {
    Remove-Item Env:VITE_API_URL -ErrorAction SilentlyContinue
    Pop-Location
}

Push-Location $root
try {
    npx --yes firebase-tools@13 login
    npx --yes firebase-tools@13 deploy --only hosting --project $ProjectId
} finally { Pop-Location }

Write-Host ''
Write-Host "Listo: https://$ProjectId.web.app  -  Para restringir la API a este dominio ejecuta: .\deploy-backend.ps1 -ProjectId $ProjectId" -ForegroundColor Yellow
