# Arranca AburráSegura completo: backend FastAPI (:8000) y frontend Vite (:5173).
# Uso:  .\start.ps1        (la primera vez instala dependencias automáticamente)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$py = Join-Path $root '.venv\Scripts\python.exe'

if (-not (Test-Path $py)) {
    Write-Host '> Creando entorno virtual de Python...' -ForegroundColor Cyan
    python -m venv (Join-Path $root '.venv')
    & $py -m pip install -q -r (Join-Path $root 'requirements-dev.txt')
}
if (-not (Test-Path (Join-Path $root 'frontend\node_modules'))) {
    Write-Host '> Instalando dependencias del frontend...' -ForegroundColor Cyan
    Push-Location (Join-Path $root 'frontend'); npm install; Pop-Location
}

Write-Host '> Backend en http://127.0.0.1:8000 (Swagger en /docs)' -ForegroundColor Green
$backend = Start-Process -FilePath $py -ArgumentList '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000', '--reload' -WorkingDirectory $root -PassThru -NoNewWindow

try {
    Write-Host '> Frontend en http://localhost:5173' -ForegroundColor Green
    Push-Location (Join-Path $root 'frontend')
    npm run dev
} finally {
    Pop-Location
    if ($backend -and -not $backend.HasExited) { Stop-Process -Id $backend.Id -Force }
}
