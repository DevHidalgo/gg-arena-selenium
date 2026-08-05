# Levanta unicamente la aplicacion GG Arena para la demostracion manual del video.
#
#   .\iniciar_app.ps1              -> http://127.0.0.1:5055
#   .\iniciar_app.ps1 -Puerto 8080
param(
    [int]$Puerto = 5055
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Host "No se encontro el entorno virtual. Ejecute primero .\ejecutar_pruebas.ps1" -ForegroundColor Red
    exit 1
}

Write-Host "`nGG Arena disponible en http://127.0.0.1:$Puerto" -ForegroundColor Green
Write-Host "Credenciales: admin / Arena2026*`n" -ForegroundColor Gray
Write-Host "Presione Ctrl+C para detener el servidor.`n" -ForegroundColor Gray

& $python -m app.app --port $Puerto
