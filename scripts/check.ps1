# Runs the same checks as the CI, using the virtual environment.
$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) { throw "No se encuentra .venv. Crea el entorno: python -m venv .venv" }

$steps = @(
  @("ruff", "check", "."),
  @("ruff", "format", "--check", "."),
  @("mypy"),
  @("pytest")
)
foreach ($step in $steps) {
  Write-Host "`n> python -m $($step -join ' ')" -ForegroundColor Cyan
  & $python -m @step
  if ($LASTEXITCODE -ne 0) { throw "Falló: $($step -join ' ')" }
}
Write-Host "`nTodo correcto." -ForegroundColor Green
