@echo off
REM Quick setup batch file for StarCraft2Bot in Windows VM
REM This provides a simple double-click setup option

echo.
echo ========================================
echo   StarCraft2Bot Windows VM Quick Setup
echo ========================================
echo.

REM Check if PowerShell is available
where powershell >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: PowerShell not found!
    echo Please install PowerShell or run the .ps1 files manually
    pause
    exit /b 1
)

echo Step 1: Setting up SSH Server...
echo Running windows_ssh_setup.ps1...
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0windows_ssh_setup.ps1"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: SSH setup failed!
    echo Please run PowerShell as Administrator and try again
    pause
    exit /b 1
)

echo.
echo ========================================
echo SSH setup complete!
echo.
echo Next steps:
echo 1. Note your VM IP address from above
echo 2. Run setup script on your macOS machine
echo 3. Clone StarCraft2Bot repository in this VM
echo 4. Run setup_bot_in_vm.ps1 in the cloned directory
echo.
echo Press any key to continue...
pause >nul
