# Windows SSH Setup Script for StarCraft2Bot Remote Development
# Run this script in PowerShell as Administrator in your Windows VM

Write-Host "🖥️  Setting up SSH Server in Windows VM" -ForegroundColor Cyan
Write-Host "=" * 50

# Check if running as administrator
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Running as Administrator" -ForegroundColor Green

# Install OpenSSH Server
Write-Host ""
Write-Host "🔧 Installing OpenSSH Server..." -ForegroundColor Cyan

$sshFeature = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'

if ($sshFeature.State -eq "Installed") {
    Write-Host "✅ OpenSSH Server already installed" -ForegroundColor Green
} else {
    Write-Host "📦 Installing OpenSSH Server..."
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
    Write-Host "✅ OpenSSH Server installed" -ForegroundColor Green
}

# Start SSH service
Write-Host ""
Write-Host "🚀 Starting SSH service..." -ForegroundColor Cyan

Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

$sshStatus = Get-Service sshd
if ($sshStatus.Status -eq "Running") {
    Write-Host "✅ SSH service is running" -ForegroundColor Green
} else {
    Write-Host "❌ SSH service failed to start" -ForegroundColor Red
    exit 1
}

# Configure firewall
Write-Host ""
Write-Host "🔥 Configuring Windows Firewall..." -ForegroundColor Cyan

$existingRule = Get-NetFirewallRule -DisplayName "OpenSSH Server (sshd)" -ErrorAction SilentlyContinue

if ($existingRule) {
    Write-Host "✅ Firewall rule already exists" -ForegroundColor Green
} else {
    New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
    Write-Host "✅ Firewall rule created" -ForegroundColor Green
}

# Create .ssh directory
Write-Host ""
Write-Host "📁 Creating .ssh directory..." -ForegroundColor Cyan

$sshDir = "$env:USERPROFILE\.ssh"
if (-not (Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir -Force
    Write-Host "✅ Created .ssh directory: $sshDir" -ForegroundColor Green
} else {
    Write-Host "✅ .ssh directory already exists" -ForegroundColor Green
}

# Set proper permissions on .ssh directory
icacls $sshDir /inheritance:r
icacls $sshDir /grant:r "$env:USERNAME:(F)"

# Display network information
Write-Host ""
Write-Host "🌐 Network Information:" -ForegroundColor Cyan
Write-Host "=" * 30

$networkInfo = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" }

foreach ($ip in $networkInfo) {
    $adapter = Get-NetAdapter -InterfaceIndex $ip.InterfaceIndex
    Write-Host "Interface: $($adapter.Name)" -ForegroundColor Yellow
    Write-Host "IP Address: $($ip.IPAddress)" -ForegroundColor Green
    Write-Host ""
}

# Display connection information
Write-Host "🔗 SSH Connection Information:" -ForegroundColor Cyan
Write-Host "=" * 30
Write-Host "Username: $env:USERNAME" -ForegroundColor Green
Write-Host "SSH Port: 22" -ForegroundColor Green
Write-Host ""
Write-Host "From macOS, connect with:" -ForegroundColor Yellow
Write-Host "ssh $env:USERNAME@YOUR_VM_IP_ADDRESS" -ForegroundColor White

# Install Chocolatey if not present
Write-Host ""
Write-Host "🍫 Checking for Chocolatey..." -ForegroundColor Cyan

if (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Host "✅ Chocolatey already installed" -ForegroundColor Green
} else {
    Write-Host "📦 Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    Write-Host "✅ Chocolatey installed" -ForegroundColor Green
}

# Install Python and Git
Write-Host ""
Write-Host "🐍 Installing Python and Git..." -ForegroundColor Cyan

if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python already installed" -ForegroundColor Green
} else {
    Write-Host "📦 Installing Python..."
    choco install python -y
}

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "✅ Git already installed" -ForegroundColor Green
} else {
    Write-Host "📦 Installing Git..."
    choco install git -y
}

# Refresh environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Install uv
Write-Host ""
Write-Host "📦 Installing uv..." -ForegroundColor Cyan

if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "✅ uv already installed" -ForegroundColor Green
} else {
    pip install uv
    Write-Host "✅ uv installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Windows VM SSH setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Note your VM IP address from the network information above"
Write-Host "2. Run the setup script on your macOS machine"
Write-Host "3. Clone the StarCraft2Bot repository in this VM"
Write-Host "4. Configure StarCraft II path in src/config.py"
Write-Host ""
Write-Host "🔗 Test SSH connection from macOS:" -ForegroundColor Yellow
Write-Host "ssh $env:USERNAME@YOUR_VM_IP_ADDRESS" -ForegroundColor White
