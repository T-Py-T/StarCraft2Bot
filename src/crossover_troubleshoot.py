#!/usr/bin/env python3
"""
CrossOver Troubleshooting and Fallback Solution
"""

import os
import sys
import subprocess
import time
import socket
from pathlib import Path

def check_crossover_status():
    """Check CrossOver installation and status"""
    print("🔍 Checking CrossOver Status")
    print("=" * 30)
    
    crossover_app = Path("/Users/taylor/Applications/CrossOver.app")
    sc2_bottle = Path("/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II")
    sc2_exe = sc2_bottle / "drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"
    wine_exe = crossover_app / "Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
    
    print(f"CrossOver app: {'✅' if crossover_app.exists() else '❌'}")
    print(f"SC2 bottle: {'✅' if sc2_bottle.exists() else '❌'}")
    print(f"SC2 exe: {'✅' if sc2_exe.exists() else '❌'}")
    print(f"Wine exe: {'✅' if wine_exe.exists() else '❌'}")
    
    return all([crossover_app.exists(), sc2_bottle.exists(), sc2_exe.exists(), wine_exe.exists()])

def test_wine_basic():
    """Test Wine basic functionality"""
    print("\n🍷 Testing Wine Basic Functionality")
    print("=" * 30)
    
    wine_exe = "/Users/taylor/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
    
    try:
        result = subprocess.run([wine_exe, "--version"], 
                              capture_output=True, text=True, timeout=10)
        print(f"Wine version: {result.stdout.strip()}")
        print(f"Exit code: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"Wine test failed: {e}")
        return False

def test_sc2_installation():
    """Test StarCraft II installation"""
    print("\n🎮 Testing StarCraft II Installation")
    print("=" * 30)
    
    sc2_exe = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"
    
    if not os.path.exists(sc2_exe):
        print("❌ StarCraft II executable not found")
        return False
    
    # Check file size and permissions
    stat = os.stat(sc2_exe)
    print(f"File size: {stat.st_size:,} bytes")
    print(f"Executable: {os.access(sc2_exe, os.X_OK)}")
    
    return True

def test_sc2_launch():
    """Test StarCraft II launch"""
    print("\n🚀 Testing StarCraft II Launch")
    print("=" * 30)
    
    env = os.environ.copy()
    env["WINEPREFIX"] = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II"
    env["WINEDEBUG"] = "-all"
    
    wine_exe = "/Users/taylor/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
    sc2_exe = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"
    
    try:
        print("Attempting to launch StarCraft II...")
        process = subprocess.Popen([wine_exe, sc2_exe], env=env, 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ StarCraft II is running!")
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ StarCraft II exited with code {process.returncode}")
            print(f"Stdout: {stdout[:200]}...")
            print(f"Stderr: {stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Launch failed: {e}")
        return False

def provide_solutions():
    """Provide solutions for CrossOver issues"""
    print("\n🔧 Solutions for CrossOver Issues")
    print("=" * 30)
    
    print("1. **Reinstall StarCraft II through CrossOver:**")
    print("   - Open CrossOver")
    print("   - Uninstall StarCraft II")
    print("   - Reinstall StarCraft II")
    print("   - Make sure it runs properly in CrossOver GUI")
    
    print("\n2. **Check CrossOver Bottle:**")
    print("   - Open CrossOver")
    print("   - Select 'StarCraft II' bottle")
    print("   - Click 'Run' to test StarCraft II")
    print("   - If it doesn't work, try creating a new bottle")
    
    print("\n3. **Alternative: Use Parallels Desktop:**")
    print("   - Install Parallels Desktop")
    print("   - Create a Windows VM")
    print("   - Install StarCraft II in the VM")
    print("   - Run the bot from within the VM")
    
    print("\n4. **Alternative: Use VMware Fusion:**")
    print("   - Install VMware Fusion")
    print("   - Create a Windows VM")
    print("   - Install StarCraft II in the VM")
    print("   - Run the bot from within the VM")

def create_parallels_setup_guide():
    """Create a setup guide for Parallels"""
    print("\n📝 Creating Parallels Setup Guide")
    print("=" * 30)
    
    guide_content = """# Parallels Desktop Setup Guide

## Prerequisites
- Parallels Desktop for Mac
- Windows 10/11 license
- At least 8GB RAM
- 50GB free disk space

## Setup Steps

### 1. Install Parallels Desktop
- Download from [Parallels](https://www.parallels.com/)
- Install and activate

### 2. Create Windows VM
- Open Parallels Desktop
- Click "Create New"
- Select "Install Windows"
- Choose Windows 10/11
- Allocate at least 4GB RAM
- Allocate at least 50GB disk space

### 3. Install StarCraft II
- Start the Windows VM
- Open a web browser
- Go to [Battle.net](https://battle.net)
- Download and install Battle.net
- Install StarCraft II through Battle.net

### 4. Configure the Bot
- Copy the StarCraft2Bot project to the VM
- Install Python and dependencies in the VM
- Update `src/config.py` with the Windows StarCraft II path
- Run the bot from within the VM

### 5. Network Configuration
- Enable network sharing between Mac and VM
- The bot will run in the VM but you can develop on Mac
- Use shared folders to sync code changes

## Advantages of Parallels
- Native Windows performance
- Full StarCraft II compatibility
- Easy to set up and maintain
- Can run multiple VMs for testing

## Disadvantages
- Requires Windows license
- Uses more system resources
- Slightly more complex setup
"""
    
    with open("run/macos/PARALLELS_SETUP.md", "w") as f:
        f.write(guide_content)
    
    print("✅ Created Parallels setup guide: run/macos/PARALLELS_SETUP.md")

def main():
    print("🔧 CrossOver Troubleshooting and Solutions")
    print("=" * 50)
    
    # Check CrossOver status
    if not check_crossover_status():
        print("\n❌ CrossOver installation issues found!")
        provide_solutions()
        return False
    
    # Test Wine
    if not test_wine_basic():
        print("\n❌ Wine is not working!")
        provide_solutions()
        return False
    
    # Test SC2 installation
    if not test_sc2_installation():
        print("\n❌ StarCraft II installation issues!")
        provide_solutions()
        return False
    
    # Test SC2 launch
    if not test_sc2_launch():
        print("\n❌ StarCraft II launch issues!")
        print("\nThis is a common problem with CrossOver.")
        print("StarCraft II may not be compatible with CrossOver on your system.")
        
        provide_solutions()
        create_parallels_setup_guide()
        
        print("\n💡 Recommendation: Use Parallels Desktop for the best experience.")
        return False
    
    print("\n🎉 CrossOver is working! The bot should work.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
