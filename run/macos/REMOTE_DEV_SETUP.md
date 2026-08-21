# Remote Development with Parallels Windows VM

This guide shows you how to set up remote development where you develop on macOS but run the bot in the Windows VM, maintaining proper Git versioning.

## Overview

**Development Flow:**
- Code on macOS (your main machine)
- Git repository stays on macOS
- SSH into Windows VM to run the bot
- Use VS Code Remote SSH for seamless development

## Step 1: Enable SSH in Windows VM

### 1.1 Install OpenSSH Server in Windows

1. **Open Settings in Windows VM**
2. **Go to Apps > Optional Features**
3. **Click "Add an optional feature"**
4. **Search for "OpenSSH Server"**
5. **Install OpenSSH Server**

### 1.2 Start SSH Service

Open PowerShell as Administrator in Windows VM:

```powershell
# Start SSH service
Start-Service sshd

# Set SSH to start automatically
Set-Service -Name sshd -StartupType 'Automatic'

# Confirm SSH is running
Get-Service sshd
```

### 1.3 Configure Windows Firewall

```powershell
# Allow SSH through firewall
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

## Step 2: Configure Parallels Networking

### 2.1 Set Network Mode

1. **Shut down Windows VM**
2. **Open Parallels Desktop**
3. **Right-click your Windows VM > Configure**
4. **Go to Hardware > Network**
5. **Set to "Bridged Network" or "Shared Network"**
   - **Bridged**: VM gets its own IP on your network (recommended)
   - **Shared**: VM uses NAT through macOS

### 2.2 Find VM IP Address

In Windows VM, open Command Prompt:

```cmd
ipconfig
```

Note the IPv4 address (e.g., `192.168.1.100`)

## Step 3: Set Up SSH Keys (Recommended)

On your macOS:

```bash
# Generate SSH key if you don't have one
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# Copy public key to Windows VM
ssh-copy-id username@VM_IP_ADDRESS
```

If `ssh-copy-id` doesn't work, manually copy the key:

```bash
# Display your public key
cat ~/.ssh/id_rsa.pub

# Then paste it into Windows VM at:
# C:\Users\username\.ssh\authorized_keys
```

## Step 4: Test SSH Connection

From macOS:

```bash
# Test SSH connection
ssh username@VM_IP_ADDRESS

# If successful, you should get a Windows command prompt
```

## Step 5: Set Up Development Environment in VM

### 5.1 Install Python and Git in Windows VM

```powershell
# Install Chocolatey (package manager for Windows)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python and Git
choco install python git -y

# Refresh environment
refreshenv
```

### 5.2 Install uv in Windows VM

```powershell
# Install uv
pip install uv

# Verify installation
uv --version
```

## Step 6: Clone Repository in Windows VM

```powershell
# Navigate to desired directory
cd C:\Users\username\

# Clone the repository
git clone https://github.com/T-Py-T/starcraft2-ppo-agent.git
cd starcraft2-ppo-agent

# Install dependencies
uv sync
```

## Step 7: Configure VS Code Remote SSH

### 7.1 Install VS Code Extensions on macOS

1. **Install "Remote - SSH" extension**
2. **Install "Remote - SSH: Editing Configuration Files" extension**

### 7.2 Configure SSH Connection

1. **Open VS Code on macOS**
2. **Press `Cmd+Shift+P`**
3. **Type "Remote-SSH: Connect to Host"**
4. **Add new SSH target: `username@VM_IP_ADDRESS`**
5. **Select the config file to update (usually `~/.ssh/config`)**

### 7.3 Connect and Develop

1. **Press `Cmd+Shift+P`**
2. **Type "Remote-SSH: Connect to Host"**
3. **Select your Windows VM**
4. **Open the StarCraft2Bot folder in the VM**
5. **Install Python extension in the remote VS Code**

## Step 8: Development Workflow

### 8.1 Daily Workflow

```bash
# On macOS - make changes and commit
git add .
git commit -m "Your changes"
git push origin main

# SSH into Windows VM
ssh username@VM_IP_ADDRESS

# In Windows VM - pull latest changes
cd C:\Users\username\StarCraft2Bot
git pull origin main

# Run the bot
uv run src/test_bot.py
# or
make train
```

### 8.2 Alternative: Use VS Code Remote SSH

1. **Connect to VM via VS Code Remote SSH**
2. **Make changes in VS Code (running on VM)**
3. **Use VS Code's built-in Git interface**
4. **Commit and push from within VS Code**

## Step 9: Configure StarCraft II Path

In Windows VM, update `src/config.py`:

```python
# Update the Windows path to match your installation
STARCRAFT_II_PATH_WINDOWS = r"C:\Program Files (x86)\StarCraft II\StarCraft II.exe"
```

## Step 10: Test the Setup

### 10.1 Test SSH Connection

From macOS:
```bash
ssh username@VM_IP_ADDRESS "cd starcraft2-ppo-agent && uv run --version"
```

### 10.2 Test Bot

SSH into VM and run:
```powershell
cd C:\Users\username\StarCraft2Bot
uv run src/test_bot.py
```

## Troubleshooting

### SSH Connection Issues

1. **Check Windows VM IP address**
2. **Verify SSH service is running in VM**
3. **Check firewall settings**
4. **Try connecting with password first, then set up keys**

### Git Issues

1. **Configure Git in Windows VM:**
   ```powershell
   git config --global user.name "Your Name"
   git config --global user.email "your-email@example.com"
   ```

2. **Set up Git credentials for GitHub**

### Performance Issues

1. **Allocate more RAM to VM (at least 4GB)**
2. **Enable hardware acceleration**
3. **Close unnecessary applications in VM**

## Advanced: Automated Sync Script

Create a script on macOS to automatically sync and run:

```bash
#!/bin/bash
# File: sync_and_run.sh

VM_IP="192.168.1.100"  # Replace with your VM IP
VM_USER="username"      # Replace with your VM username

# Push changes from macOS
git add .
git commit -m "Auto sync: $(date)"
git push origin main

# SSH into VM and pull changes
ssh $VM_USER@$VM_IP "cd starcraft2-ppo-agent && git pull origin main && uv run src/test_bot.py"
```

Make it executable:
```bash
chmod +x sync_and_run.sh
```

## Benefits of This Setup

✅ **Git versioning maintained**  
✅ **Develop on macOS with your preferred tools**  
✅ **Run bot on Windows with full StarCraft II compatibility**  
✅ **Easy to sync changes**  
✅ **Can use VS Code Remote SSH for seamless development**  
✅ **Performance benefits of native Windows**  

This setup gives you the best of both worlds - macOS development experience with Windows StarCraft II compatibility!
