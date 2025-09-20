# Simple StarCraft II Maps Downloader for Windows
# This script downloads maps to the Windows StarCraft II installation

param(
    [string]$StarCraftPath = "E:\XboxGames\StarCraft II"
)

Write-Host "=== Simple StarCraft II Maps Downloader (Windows) ===" -ForegroundColor Green

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
Write-Host "1. Create a simple test map:" -ForegroundColor White
Write-Host "   uv run create_simple_map.py" -ForegroundColor White
Write-Host "`n2. Then test the training:" -ForegroundColor White
Write-Host "   cd .." -ForegroundColor White
Write-Host "   uv run src/trainppo.py" -ForegroundColor White 