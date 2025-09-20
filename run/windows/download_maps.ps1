# StarCraft II Maps Downloader for Windows
# This script downloads maps to the Windows StarCraft II installation

param(
    [string]$StarCraftPath = "E:\XboxGames\StarCraft II"
)

Write-Host "=== StarCraft II Maps Downloader (Windows) ===" -ForegroundColor Green

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

# List of basic maps to download
$Maps = @(
    "Simple64",
    "2000AtmospheresAIE", 
    "AcropolisLE",
    "Bel'ShirVestigeLE",
    "CactusValleyLE",
    "CatallenaLE",
    "CentralProtocol",
    "DuskTowers",
    "EchoLE",
    "FrostLE",
    "HabitationStationLE",
    "KairosJunction",
    "KingSejongStation",
    "NewkirkPrecinctTE",
    "PaladinoTerminalLE",
    "ProximaStation",
    "Sequencer",
    "ThunderbirdLE",
    "Triton",
    "WintersGateLE"
)

Write-Host "Attempting to download $($Maps.Count) maps..." -ForegroundColor Yellow
Write-Host "Note: This script will try to download maps from the sc2 library." -ForegroundColor Yellow
Write-Host "If this fails, you may need to:" -ForegroundColor Yellow
Write-Host "1. Install StarCraft II from Battle.net instead of Xbox Game Pass" -ForegroundColor Yellow
Write-Host "2. Or manually download maps from the StarCraft II community" -ForegroundColor Yellow
Write-Host "3. Or use only built-in maps (Simple64, etc.)" -ForegroundColor Yellow

$SuccessCount = 0

# Try to import sc2 and download maps
try {
    # Install sc2 if not available
    if (-not (Get-Module -ListAvailable -Name sc2)) {
        Write-Host "Installing sc2 library..." -ForegroundColor Yellow
        pip install sc2
    }
    
    # Import sc2
    $sc2Module = Import-Module sc2 -ErrorAction SilentlyContinue
    if (-not $sc2Module) {
        Write-Host "Warning: Could not import sc2 module" -ForegroundColor Yellow
        Write-Host "You may need to install it manually: pip install sc2" -ForegroundColor Yellow
    }
    
    foreach ($MapName in $Maps) {
        try {
            # Try to get the map from sc2 library
            $MapPath = & python -c "import sc2.maps; print(sc2.maps.get('$MapName'))" 2>$null
            
            if ($MapPath -and (Test-Path $MapPath)) {
                # Copy to Maps directory
                $DestPath = Join-Path $MapsDir "$MapName.SC2Map"
                Copy-Item $MapPath $DestPath -Force
                Write-Host "✓ Downloaded: $MapName" -ForegroundColor Green
                $SuccessCount++
            } else {
                Write-Host "✗ Not available: $MapName" -ForegroundColor Red
            }
        } catch {
            Write-Host "✗ Failed to download $MapName : $($_.Exception.Message)" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "Error importing sc2 module: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "You may need to install it manually: pip install sc2" -ForegroundColor Yellow
}

Write-Host "`nDownload complete: $SuccessCount/$($Maps.Count) maps downloaded" -ForegroundColor Cyan

if ($SuccessCount -eq 0) {
    Write-Host "`nNo maps were downloaded. You can still run the bot with built-in maps:" -ForegroundColor Yellow
    Write-Host "- Simple64" -ForegroundColor Yellow
    Write-Host "- 2000AtmospheresAIE" -ForegroundColor Yellow
    Write-Host "- And other maps that come with the sc2 library" -ForegroundColor Yellow
} else {
    Write-Host "`nMaps downloaded successfully! You can now run the training script from Windows." -ForegroundColor Green
}

Write-Host "`nTo run the training script from Windows:" -ForegroundColor Cyan
Write-Host "cd E:\Dropbox\_GitHub\StarCraft2Bot" -ForegroundColor White
Write-Host "uv run src/trainppo.py" -ForegroundColor White 