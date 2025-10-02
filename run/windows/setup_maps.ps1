# Simple StarCraft II Maps Setup for Windows
# This script creates the Maps directory and provides instructions

param(
    [string]$StarCraftPath = "E:\XboxGames\StarCraft II"
)

Write-Host "=== StarCraft II Maps Setup (Windows) ===" -ForegroundColor Green

# Check if StarCraft II path exists
if (-not (Test-Path $StarCraftPath)) {
    Write-Host "Error: StarCraft II not found at $StarCraftPath" -ForegroundColor Red
    Write-Host "Please update the StarCraftPath parameter or install StarCraft II" -ForegroundColor Yellow
    exit 1
}

# Create Maps directory if it doesn't exist
$MapsDir = Join-Path $StarCraftPath "Maps"
if (-not (Test-Path $MapsDir)) {
    New-Item -ItemType Directory -Path $MapsDir -Force
    Write-Host "Created Maps directory: $MapsDir" -ForegroundColor Green
} else {
    Write-Host "Maps directory exists: $MapsDir" -ForegroundColor Green
}

Write-Host "`nMaps directory is ready!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Run the Python create map script from Windows:" -ForegroundColor White
Write-Host "   cd E:\Dropbox\_GitHub\StarCraft2Bot" -ForegroundColor White
Write-Host "   uv run run/windows/create_simple_map.py" -ForegroundColor White
Write-Host "`n2. Then test the training:" -ForegroundColor White
Write-Host "   uv run src/trainppo.py" -ForegroundColor White 