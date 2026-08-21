# Setup StarCraft2Bot in Windows VM
# Run this script after SSH is working and you've cloned the repository

Write-Host "🤖 Setting up StarCraft2Bot in Windows VM" -ForegroundColor Cyan
Write-Host "=" * 50

# Check if we're in the right directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "❌ Not in StarCraft2Bot directory!" -ForegroundColor Red
    Write-Host "Please navigate to the StarCraft2Bot directory first:" -ForegroundColor Yellow
    Write-Host "cd starcraft2-ppo-agent" -ForegroundColor White
    exit 1
}

Write-Host "✅ Found StarCraft2Bot project" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan

if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "Using uv to install dependencies..."
    uv sync
    Write-Host "✅ Dependencies installed with uv" -ForegroundColor Green
} else {
    Write-Host "uv not found, using pip..."
    pip install -r requirements.txt
    Write-Host "✅ Dependencies installed with pip" -ForegroundColor Green
}

# Find StarCraft II installation
Write-Host ""
Write-Host "🎮 Looking for StarCraft II installation..." -ForegroundColor Cyan

$commonPaths = @(
    "C:\Program Files (x86)\StarCraft II\StarCraft II.exe",
    "C:\Program Files\StarCraft II\StarCraft II.exe",
    "D:\Program Files (x86)\StarCraft II\StarCraft II.exe",
    "E:\Program Files (x86)\StarCraft II\StarCraft II.exe"
)

$sc2Path = $null
foreach ($path in $commonPaths) {
    if (Test-Path $path) {
        $sc2Path = $path
        Write-Host "✅ Found StarCraft II at: $path" -ForegroundColor Green
        break
    }
}

if (-not $sc2Path) {
    Write-Host "❌ StarCraft II not found in common locations" -ForegroundColor Red
    Write-Host "Please install StarCraft II through Battle.net first" -ForegroundColor Yellow
    Write-Host "Common installation paths:" -ForegroundColor Cyan
    foreach ($path in $commonPaths) {
        Write-Host "  $path" -ForegroundColor White
    }
    exit 1
}

# Update config.py
Write-Host ""
Write-Host "⚙️  Updating configuration..." -ForegroundColor Cyan

$configPath = "src\config.py"
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw
    
    # Update the Windows path
    $escapedPath = $sc2Path -replace "\\", "\\\\"
    $config = $config -replace 'STARCRAFT_II_PATH_WINDOWS = r"[^"]*"', "STARCRAFT_II_PATH_WINDOWS = r`"$sc2Path`""
    
    Set-Content -Path $configPath -Value $config
    Write-Host "✅ Updated StarCraft II path in config.py" -ForegroundColor Green
    Write-Host "Path set to: $sc2Path" -ForegroundColor Yellow
} else {
    Write-Host "❌ config.py not found at $configPath" -ForegroundColor Red
    exit 1
}

# Test the installation
Write-Host ""
Write-Host "🧪 Testing bot installation..." -ForegroundColor Cyan

try {
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        $result = uv run src/test_bot.py
    } else {
        $result = python src/test_bot.py
    }
    Write-Host "✅ Bot test completed!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Bot test encountered an issue (this might be normal)" -ForegroundColor Yellow
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Display final information
Write-Host ""
Write-Host "🎉 StarCraft2Bot setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Available commands:" -ForegroundColor Cyan
Write-Host "Test bot:     uv run src/test_bot.py" -ForegroundColor White
Write-Host "Train bot:    uv run src/trainppo.py" -ForegroundColor White
Write-Host "Play game:    uv run scripts/play.py" -ForegroundColor White
Write-Host ""
Write-Host "⚙️  Configuration:" -ForegroundColor Cyan
Write-Host "StarCraft II: $sc2Path" -ForegroundColor White
Write-Host "Config file:  src\config.py" -ForegroundColor White
Write-Host ""
Write-Host "🔗 To connect from macOS:" -ForegroundColor Cyan
Write-Host "ssh $env:USERNAME@$(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } | Select-Object -First 1).IPAddress" -ForegroundColor White
