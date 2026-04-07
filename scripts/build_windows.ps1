param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $projectRoot ".venv\\Scripts\\python.exe"

if (-not (Test-Path $venvPython)) {
    throw "No se encontro Python del entorno virtual en $venvPython"
}

if ($Clean) {
    $buildDir = Join-Path $projectRoot "build"
    $distDir = Join-Path $projectRoot "dist"
    if (Test-Path $buildDir) {
        Remove-Item -LiteralPath $buildDir -Recurse -Force
    }
    if (Test-Path $distDir) {
        Remove-Item -LiteralPath $distDir -Recurse -Force
    }
}

Push-Location $projectRoot
try {
    & $venvPython -m PyInstaller --noconfirm mus_simulator.spec

    $sourceCardsDir = Join-Path $projectRoot "card_images"
    $targetCardsDir = Join-Path $projectRoot "dist\\MusSimulator\\card_images"
    if (Test-Path $sourceCardsDir) {
        if (Test-Path $targetCardsDir) {
            Remove-Item -LiteralPath $targetCardsDir -Recurse -Force
        }
        Copy-Item -LiteralPath $sourceCardsDir -Destination $targetCardsDir -Recurse
    }

    Write-Host ""
    Write-Host "Build completada."
    Write-Host "Ejecutable: $projectRoot\\dist\\MusSimulator\\MusSimulator.exe"
    Write-Host "Cartas:     $projectRoot\\dist\\MusSimulator\\card_images"
} finally {
    Pop-Location
}
