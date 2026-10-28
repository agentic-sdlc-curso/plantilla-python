# Creates the course backlog (H1-H6) as GitHub issues in the current repository.
# Requirements: GitHub CLI installed and authenticated (gh auth status).
$ErrorActionPreference = "Stop"

$stories = @(
  @{ Id = "H1"; Title = "Crear una solicitud" },
  @{ Id = "H2"; Title = "Listar solicitudes con filtro por estado" },
  @{ Id = "H3"; Title = "Consultar una solicitud por id" },
  @{ Id = "H4"; Title = "Cambiar el estado de una solicitud" },
  @{ Id = "H5"; Title = "Añadir comentarios a una solicitud" },
  @{ Id = "H6"; Title = "Revisar especificaciones con Amazon Bedrock" }
)

gh label create historia --color 0E8A16 --description "Historia de usuario del backlog" --force | Out-Null

foreach ($story in $stories) {
  $title = "$($story.Id) · $($story.Title)"
  $bodyFile = Join-Path $PSScriptRoot "..\docs\backlog\$($story.Id).md"
  gh issue create --title $title --body-file $bodyFile --label historia
}
