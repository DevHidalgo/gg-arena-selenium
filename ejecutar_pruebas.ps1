# Ejecuta la suite completa de pruebas automatizadas y abre el reporte HTML.
#
#   .\ejecutar_pruebas.ps1                  -> Edge con ventana visible (ideal para el video)
#   .\ejecutar_pruebas.ps1 -Headless        -> sin ventana del navegador
#   .\ejecutar_pruebas.ps1 -Navegador chrome
param(
    [string]$Navegador = "edge",
    [switch]$Headless,
    [switch]$NoAbrirReporte
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Host "No se encontro el entorno virtual. Creandolo..." -ForegroundColor Yellow
    python -m venv .venv
    & $python -m pip install --upgrade pip
    & $python -m pip install -r requirements.txt
}

$argumentos = @("-m", "pytest", "--navegador=$Navegador")
if ($Headless) { $argumentos += "--headless" }

Write-Host "`n=== GG Arena | Ejecutando pruebas automatizadas con Selenium ===`n" -ForegroundColor Cyan
& $python $argumentos
$codigo = $LASTEXITCODE

$reporte = Join-Path $PSScriptRoot "reports\reporte_pruebas.html"
if ((-not $NoAbrirReporte) -and (Test-Path $reporte)) {
    Write-Host "`nAbriendo el reporte HTML..." -ForegroundColor Cyan
    Start-Process $reporte
}

exit $codigo
