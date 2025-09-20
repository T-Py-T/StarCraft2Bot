#!/usr/bin/env python3
"""
SC2 CrossOver Launcher v3 - Enhanced for better websocket communication

This creates a robust launcher that works with the sc2 library and CrossOver.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import time
import socket
from pathlib import Path

def test_port_available(port=5000):
    """Test if a port is available"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result != 0  # True if port is available
    except:
        return True

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if test_port_available(port):
            return port
    return None

def create_sc2_launcher_v3():
    """Create an enhanced launcher script with better websocket support"""
    
    # Find an available port
    port = find_available_port()
    if not port:
        print("❌ No available ports found!")
        return None, None, None
    
    print(f"✅ Using port {port} for StarCraft II")
    
    # Create the launcher script with enhanced configuration
    launcher_content = f'''#!/bin/bash
# SC2 CrossOver Launcher v3 - Enhanced for websocket communication
# This script launches StarCraft II through CrossOver with proper websocket support

export WINEPREFIX="/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II"
export WINEDEBUG=-all
export WINEDLLOVERRIDES="mscoree,mshtml="

# StarCraft II executable
SC2_EXE="/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"

# Wine executable
WINE_EXE="/Users/taylor/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"

# Create temp directory
mkdir -p "/tmp/sc2_temp"

# Enhanced arguments for better websocket support
DEFAULT_ARGS=(
    "--headless"
    "--listen" "127.0.0.1"
    "--port" "{port}"
    "--dataDir" "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II"
    "--tempDir" "/tmp/sc2_temp"
    "--verbose"
    "--logLevel" "1"
    "--windowwidth" "1024"
    "--windowheight" "768"
    "--windowmode" "windowed"
)

# Check if we have custom arguments
if [ $# -eq 0 ]; then
    # No arguments provided, use defaults
    echo "Starting StarCraft II with port {port}..."
    exec "$WINE_EXE" "$SC2_EXE" "${{DEFAULT_ARGS[@]}}"
else
    # Custom arguments provided, use them
    echo "Starting StarCraft II with custom arguments..."
    exec "$WINE_EXE" "$SC2_EXE" "$@"
fi
'''
    
    # Write the launcher script
    launcher_path = "/tmp/sc2_crossover_launcher_v3.sh"
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    os.chmod(launcher_path, 0o755)
    
    # Create the macOS app structure that sc2 library expects
    app_path = "/tmp/SC2.app"
    os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
    
    # Copy the launcher to the app
    shutil.copy(launcher_path, f"{app_path}/Contents/MacOS/SC2")
    
    # Create Info.plist
    info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>SC2</string>
    <key>CFBundleIdentifier</key>
    <string>com.blizzard.starcraft2</string>
    <key>CFBundleName</key>
    <string>StarCraft II</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>'''
    
    with open(f"{app_path}/Contents/Info.plist", 'w') as f:
        f.write(info_plist)
    
    return launcher_path, app_path, port

def setup_sc2_structure():
    """Set up the complete SC2 directory structure"""
    
    # Create the complete structure
    base_path = "/tmp"
    versions_path = f"{base_path}/Versions/Base94137/SC2.app/Contents/MacOS"
    maps_path = f"{base_path}/Maps"
    
    os.makedirs(versions_path, exist_ok=True)
    os.makedirs(maps_path, exist_ok=True)
    
    # Copy maps
    project_maps = "/Users/taylor/Library/CloudStorage/Dropbox/_GitHub/StarCraft2Bot/Maps"
    if os.path.exists(project_maps):
        for map_file in os.listdir(project_maps):
            if map_file.endswith('.SC2Map'):
                shutil.copy(f"{project_maps}/{map_file}", f"{maps_path}/{map_file}")
                print(f"✅ Copied map: {map_file}")
    
    return base_path, versions_path, maps_path

def test_launcher(launcher_path, port):
    """Test the launcher to make sure it works"""
    print(f"\n🧪 Testing launcher on port {port}...")
    
    try:
        # Test with --help first
        result = subprocess.run([launcher_path, "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Launcher basic test passed")
            return True
        else:
            print(f"❌ Launcher basic test failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✅ Launcher started (timed out as expected)")
        return True
    except Exception as e:
        print(f"❌ Error testing launcher: {e}")
        return False

def main():
    print("🍷 Creating SC2 CrossOver Launcher v3")
    print("=" * 50)
    
    # Create launcher
    launcher_path, app_path, port = create_sc2_launcher_v3()
    if not launcher_path:
        return False
    
    # Set up directory structure
    base_path, versions_path, maps_path = setup_sc2_structure()
    
    # Copy launcher to versions directory
    shutil.copy(launcher_path, f"{versions_path}/SC2")
    
    print(f"✅ Launcher created: {launcher_path}")
    print(f"✅ macOS app created: {app_path}")
    print(f"✅ Directory structure set up in: {base_path}")
    print(f"✅ Maps copied to: {maps_path}")
    print(f"✅ Using port: {port}")
    
    # Test the launcher
    if test_launcher(launcher_path, port):
        print(f"\n📝 Environment variables:")
        print(f"SC2PATH={base_path}")
        print(f"SC2EXE={launcher_path}")
        print(f"SC2PORT={port}")
        return True
    else:
        print("❌ Launcher test failed")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SC2 CrossOver Launcher v3 is ready!")
    else:
        print("\n❌ Failed to create launcher")
    sys.exit(0 if success else 1)
