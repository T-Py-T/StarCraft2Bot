# Test SSH connection and bot functionality
# Run this script to verify everything is working

Write-Host "🔧 Testing StarCraft2Bot Remote Connection" -ForegroundColor Cyan
Write-Host "=" * 50

# Test 1: Check SSH service
Write-Host ""
Write-Host "1️⃣  Testing SSH service..." -ForegroundColor Cyan

$sshService = Get-Service sshd -ErrorAction SilentlyContinue
if ($sshService -and $sshService.Status -eq "Running") {
    Write-Host "✅ SSH service is running" -ForegroundColor Green
} else {
    Write-Host "❌ SSH service is not running" -ForegroundColor Red
    Write-Host "Run windows_ssh_setup.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Test 2: Check firewall
Write-Host ""
Write-Host "2️⃣  Testing firewall configuration..." -ForegroundColor Cyan

$firewallRule = Get-NetFirewallRule -DisplayName "OpenSSH Server (sshd)" -ErrorAction SilentlyContinue
if ($firewallRule -and $firewallRule.Enabled -eq "True") {
    Write-Host "✅ Firewall rule is configured" -ForegroundColor Green
} else {
    Write-Host "❌ Firewall rule not found or disabled" -ForegroundColor Red
    Write-Host "Run windows_ssh_setup.ps1 to configure firewall" -ForegroundColor Yellow
}

# Test 3: Check network connectivity
Write-Host ""
Write-Host "3️⃣  Testing network configuration..." -ForegroundColor Cyan

$networkInfo = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" }

if ($networkInfo) {
    Write-Host "✅ Network interfaces found:" -ForegroundColor Green
    foreach ($ip in $networkInfo) {
        $adapter = Get-NetAdapter -InterfaceIndex $ip.InterfaceIndex
        Write-Host "   $($adapter.Name): $($ip.IPAddress)" -ForegroundColor White
    }
} else {
    Write-Host "❌ No valid network interfaces found" -ForegroundColor Red
}

# Test 4: Check required software
Write-Host ""
Write-Host "4️⃣  Testing required software..." -ForegroundColor Cyan

# Check Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found" -ForegroundColor Red
}

# Check Git
if (Get-Command git -ErrorAction SilentlyContinue) {
    $gitVersion = git --version
    Write-Host "✅ Git: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Git not found" -ForegroundColor Red
}

# Check uv
if (Get-Command uv -ErrorAction SilentlyContinue) {
    $uvVersion = uv --version
    Write-Host "✅ uv: $uvVersion" -ForegroundColor Green
} else {
    Write-Host "⚠️  uv not found (will use pip instead)" -ForegroundColor Yellow
}

# Test 5: Check StarCraft II
Write-Host ""
Write-Host "5️⃣  Testing StarCraft II installation..." -ForegroundColor Cyan

$commonPaths = @(
    "C:\Program Files (x86)\StarCraft II\StarCraft II.exe",
    "C:\Program Files\StarCraft II\StarCraft II.exe",
    "D:\Program Files (x86)\StarCraft II\StarCraft II.exe",
    "E:\Program Files (x86)\StarCraft II\StarCraft II.exe"
)

$sc2Found = $false
foreach ($path in $commonPaths) {
    if (Test-Path $path) {
        Write-Host "✅ StarCraft II found: $path" -ForegroundColor Green
        $sc2Found = $true
        break
    }
}

if (-not $sc2Found) {
    Write-Host "❌ StarCraft II not found in common locations" -ForegroundColor Red
    Write-Host "Install StarCraft II through Battle.net" -ForegroundColor Yellow
}

# Test 6: Check bot project (if in project directory)
Write-Host ""
Write-Host "6️⃣  Testing bot project..." -ForegroundColor Cyan

if (Test-Path "pyproject.toml") {
    Write-Host "✅ Found StarCraft2Bot project" -ForegroundColor Green
    
    # Check if dependencies are installed
    if (Test-Path ".venv") {
        Write-Host "✅ Virtual environment found" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Virtual environment not found" -ForegroundColor Yellow
        Write-Host "Run: uv sync" -ForegroundColor White
    }
    
    # Check config.py
    if (Test-Path "src\config.py") {
        Write-Host "✅ Configuration file found" -ForegroundColor Green
    } else {
        Write-Host "❌ Configuration file not found" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  Not in StarCraft2Bot project directory" -ForegroundColor Yellow
    Write-Host "Clone the repository first:" -ForegroundColor White
    Write-Host "git clone https://github.com/yourusername/StarCraft2Bot.git" -ForegroundColor White
}

# Test 7: Port connectivity test
Write-Host ""
Write-Host "7️⃣  Testing SSH port connectivity..." -ForegroundColor Cyan

try {
    $listener = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners()
    $sshPort = $listener | Where-Object { $_.Port -eq 22 }
    
    if ($sshPort) {
        Write-Host "✅ SSH port 22 is listening" -ForegroundColor Green
    } else {
        Write-Host "❌ SSH port 22 is not listening" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️  Could not check port status" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "📋 Test Summary" -ForegroundColor Cyan
Write-Host "=" * 20

$primaryIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } | Select-Object -First 1).IPAddress

Write-Host "VM IP Address: $primaryIP" -ForegroundColor White
Write-Host "SSH Port: 22" -ForegroundColor White
Write-Host "Username: $env:USERNAME" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Connect from macOS with:" -ForegroundColor Cyan
Write-Host "ssh $env:USERNAME@$primaryIP" -ForegroundColor White
Write-Host ""

if ($sshService.Status -eq "Running" -and $firewallRule.Enabled -eq "True" -and $networkInfo) {
    Write-Host "🎉 SSH setup looks good!" -ForegroundColor Green
    Write-Host "Ready for remote development!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some issues found. Check the results above." -ForegroundColor Yellow
    Write-Host "Run windows_ssh_setup.ps1 if needed." -ForegroundColor Yellow
}
