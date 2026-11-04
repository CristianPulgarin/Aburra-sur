# Publica el backend FastAPI en Hugging Face Spaces (gratis, sin GitHub).
# Uso:
#   .\deploy-backend.ps1                                   # primer despliegue
#   .\deploy-backend.ps1 -ProjectId mi-proyecto-firebase   # además restringe CORS al dominio de Firebase
# Pide el token de https://huggingface.co/settings/tokens (tipo Write) si no está en $env:HF_TOKEN.
param(
    [string]$Space = 'aburrasegura-api',
    [string]$ProjectId = ''
)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$py = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }

& $py -m pip install -q "huggingface_hub>=0.24"

$origins = ''
if ($ProjectId) { $origins = "https://$ProjectId.web.app,https://$ProjectId.firebaseapp.com" }

& $py (Join-Path $root 'scripts\deploy_hf_space.py') --space $Space --origins $origins
