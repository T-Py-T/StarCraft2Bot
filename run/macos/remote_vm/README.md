# Remote VM Setup Files

This folder contains all the files you need to set up remote development with your Windows VM.

## Files Overview

- `windows_ssh_setup.ps1` - Main SSH setup script for Windows VM
- `setup_bot_in_vm.ps1` - Bot setup script (run after cloning repository)
- `quick_setup.bat` - Simple double-click setup for non-technical users
- `README.md` - This file

## Quick Setup Process

### Step 1: Download Files to Windows VM

In your Windows VM, clone or download the repository:

```powershell
# Option A: Clone the entire repository
git clone https://github.com/T-Py-T/starcraft2-ppo-agent.git
cd starcraft2-ppo-agent\run\macos\remote_vm

# Option B: Download just these files
# Navigate to: https://github.com/T-Py-T/starcraft2-ppo-agent/tree/main/run/macos/remote_vm
# Download each file individually
```

### Step 2: Run SSH Setup

**Option A: PowerShell (Recommended)**
```powershell
# Right-click PowerShell and "Run as Administrator"
cd path\to\starcraft2-ppo-agent\run\macos\remote_vm
.\windows_ssh_setup.ps1
```

**Option B: Batch File (Simple)**
```cmd
# Double-click quick_setup.bat
# Follow the prompts
```

### Step 3: Complete Setup on macOS

On your macOS machine:
```bash
# Navigate to your StarCraft2Bot project
cd /path/to/StarCraft2Bot

# Run the remote development setup
make setup-remote-dev
```

### Step 4: Clone Repository in Windows VM

```powershell
# In Windows VM (after SSH is working)
git clone https://github.com/T-Py-T/starcraft2-ppo-agent.git
cd starcraft2-ppo-agent
```

### Step 5: Setup Bot in Windows VM

```powershell
# In the cloned StarCraft2Bot directory
.\run\macos\remote_vm\setup_bot_in_vm.ps1
```

## What Each Script Does

### `windows_ssh_setup.ps1`
- ✅ Installs OpenSSH Server
- ✅ Starts SSH service
- ✅ Configures Windows Firewall
- ✅ Creates .ssh directory with proper permissions
- ✅ Installs Chocolatey, Python, Git, and uv
- ✅ Displays network information for connection

### `setup_bot_in_vm.ps1`
- ✅ Installs Python dependencies with uv
- ✅ Finds StarCraft II installation automatically
- ✅ Updates config.py with correct StarCraft II path
- ✅ Tests the bot installation
- ✅ Displays available commands

### `quick_setup.bat`
- ✅ Simple double-click setup
- ✅ Runs PowerShell scripts automatically
- ✅ Provides clear error messages
- ✅ Good for non-technical users

## Troubleshooting

### SSH Setup Issues

1. **"Must be run as Administrator"**
   - Right-click PowerShell and select "Run as Administrator"

2. **Firewall blocking connections**
   - Check Windows Firewall settings
   - Ensure OpenSSH Server rule is enabled

3. **Can't connect from macOS**
   - Verify VM IP address with `ipconfig`
   - Check Parallels network settings (use Bridged Network)

### Bot Setup Issues

1. **StarCraft II not found**
   - Install StarCraft II through Battle.net
   - Verify installation path in script output

2. **Python/uv not found**
   - Run `refreshenv` in PowerShell
   - Restart PowerShell/Command Prompt
   - Manually install Python from python.org

3. **Dependencies installation fails**
   - Try using pip instead: `pip install -r requirements.txt`
   - Check internet connection in VM

## Network Configuration

### Parallels Network Settings

1. **Bridged Network (Recommended)**
   - VM gets its own IP on your network
   - Easier to connect from macOS
   - Better for development

2. **Shared Network**
   - VM uses NAT through macOS
   - May require port forwarding
   - More secure but complex

### Finding VM IP Address

In Windows VM:
```cmd
ipconfig
```

Look for IPv4 Address (e.g., 192.168.1.100)

## Development Workflow

Once setup is complete:

### From macOS
```bash
# Test connection
ssh starcraft2-vm

# Run bot remotely
make test-remote

# Sync changes and run
make sync-and-run
```

### From Windows VM
```powershell
# Test bot
uv run src/test_bot.py

# Train bot
uv run src/trainppo.py

# Play game
uv run scripts/play.py
```

## VS Code Remote Development

1. Install "Remote - SSH" extension in VS Code
2. Connect to Windows VM
3. Open StarCraft2Bot folder
4. Develop with full IntelliSense and Git integration

## Security Notes

- SSH keys are recommended over passwords
- Windows Firewall rules are created automatically
- Only SSH port (22) is opened
- All connections are encrypted

## Support

If you encounter issues:

1. Check this README
2. Review the main documentation in `run/macos/REMOTE_DEV_SETUP.md`
3. Ensure all prerequisites are met
4. Try running scripts individually to isolate issues

Happy coding! 🚀
