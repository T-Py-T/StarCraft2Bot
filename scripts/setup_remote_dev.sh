#!/bin/bash
# Quick setup script for remote development with Parallels Windows VM

echo "🖥️  Setting up Remote Development with Parallels Windows VM"
echo "=" * 60

# Check if SSH key exists
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "🔑 SSH key not found. Generating new SSH key..."
    read -p "Enter your email: " email
    ssh-keygen -t rsa -b 4096 -C "$email"
    echo "✅ SSH key generated"
else
    echo "✅ SSH key already exists"
fi

# Get VM IP address
echo ""
echo "📡 You need to find your Windows VM IP address"
echo "In your Windows VM, open Command Prompt and run: ipconfig"
echo "Look for the IPv4 Address (e.g., 192.168.1.100)"
echo ""
read -p "Enter your Windows VM IP address: " vm_ip
read -p "Enter your Windows VM username: " vm_user

# Test SSH connection
echo ""
echo "🔌 Testing SSH connection..."
if ssh -o ConnectTimeout=5 -o BatchMode=yes $vm_user@$vm_ip exit 2>/dev/null; then
    echo "✅ SSH connection successful!"
else
    echo "❌ SSH connection failed"
    echo ""
    echo "📝 You need to set up SSH in your Windows VM first:"
    echo "1. Install OpenSSH Server in Windows"
    echo "2. Start the SSH service"
    echo "3. Configure Windows Firewall"
    echo ""
    echo "See REMOTE_DEV_SETUP.md for detailed instructions"
    exit 1
fi

# Copy SSH key to VM
echo ""
echo "🔐 Copying SSH key to Windows VM..."
if command -v ssh-copy-id >/dev/null 2>&1; then
    ssh-copy-id $vm_user@$vm_ip
    echo "✅ SSH key copied"
else
    echo "⚠️  ssh-copy-id not found. You'll need to manually copy your SSH key"
    echo "Your public key:"
    cat ~/.ssh/id_rsa.pub
    echo ""
    echo "Copy this key to: C:\\Users\\$vm_user\\.ssh\\authorized_keys in your Windows VM"
fi

# Create SSH config
echo ""
echo "📝 Creating SSH config..."
ssh_config="$HOME/.ssh/config"
if ! grep -q "Host starcraft2-vm" "$ssh_config" 2>/dev/null; then
    cat >> "$ssh_config" << EOF

# StarCraft2Bot Windows VM
Host starcraft2-vm
    HostName $vm_ip
    User $vm_user
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF
    echo "✅ SSH config created"
else
    echo "✅ SSH config already exists"
fi

# Test the configured connection
echo ""
echo "🧪 Testing configured SSH connection..."
if ssh -o ConnectTimeout=5 starcraft2-vm exit 2>/dev/null; then
    echo "✅ Configured SSH connection works!"
    echo ""
    echo "🎉 Setup complete! You can now connect with:"
    echo "   ssh starcraft2-vm"
else
    echo "❌ Configured SSH connection failed"
    echo "You may need to manually set up SSH keys"
fi

# Create sync script
echo ""
echo "📜 Creating sync script..."
cat > sync_and_run.sh << EOF
#!/bin/bash
# Sync changes and run bot in Windows VM

VM_HOST="starcraft2-vm"

echo "📤 Pushing changes to Git..."
git add .
git commit -m "Auto sync: \$(date)"
git push origin main

echo "📥 Pulling changes in Windows VM and running bot..."
ssh \$VM_HOST "cd StarCraft2Bot && git pull origin main && uv run src/test_bot.py"
EOF

chmod +x sync_and_run.sh
echo "✅ Created sync_and_run.sh script"

echo ""
echo "🎯 Next Steps:"
echo "1. SSH into your VM: ssh starcraft2-vm"
echo "2. Clone the repository in the VM"
echo "3. Install Python, uv, and dependencies in the VM"
echo "4. Configure StarCraft II path in src/config.py"
echo "5. Test the bot!"
echo ""
echo "📖 See run/macos/REMOTE_DEV_SETUP.md for detailed instructions"
echo "📁 Windows VM files are in: run/macos/remote_vm/"
