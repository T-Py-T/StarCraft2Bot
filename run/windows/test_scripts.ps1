# Test script to verify PowerShell scripts work correctly
# This script tests the syntax of other scripts without actually running them

Write-Host "=== Testing PowerShell Scripts ===" -ForegroundColor Green

# Test setup_maps.ps1
Write-Host "Testing setup_maps.ps1..." -ForegroundColor Yellow
try {
    $setupContent = Get-Content "setup_maps.ps1" -Raw
    $tokens = [System.Management.Automation.PSParser]::Tokenize($setupContent, [ref]$null)
    Write-Host "✓ setup_maps.ps1 syntax is valid" -ForegroundColor Green
} catch {
    Write-Host "✗ setup_maps.ps1 has syntax errors: $($_.Exception.Message)" -ForegroundColor Red
}

# Test download_maps.ps1
Write-Host "Testing download_maps.ps1..." -ForegroundColor Yellow
try {
    $downloadContent = Get-Content "download_maps.ps1" -Raw
    $tokens = [System.Management.Automation.PSParser]::Tokenize($downloadContent, [ref]$null)
    Write-Host "✓ download_maps.ps1 syntax is valid" -ForegroundColor Green
} catch {
    Write-Host "✗ download_maps.ps1 has syntax errors: $($_.Exception.Message)" -ForegroundColor Red
}

# Test download_maps_simple.ps1
Write-Host "Testing download_maps_simple.ps1..." -ForegroundColor Yellow
try {
    $simpleContent = Get-Content "download_maps_simple.ps1" -Raw
    $tokens = [System.Management.Automation.PSParser]::Tokenize($simpleContent, [ref]$null)
    Write-Host "✓ download_maps_simple.ps1 syntax is valid" -ForegroundColor Green
} catch {
    Write-Host "✗ download_maps_simple.ps1 has syntax errors: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nScript testing complete!" -ForegroundColor Green 