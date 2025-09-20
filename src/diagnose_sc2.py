#!/usr/bin/env python3
"""
Diagnostic script to troubleshoot StarCraft II launch issues
"""

import os
import sys
import subprocess
import time
import socket
from pathlib import Path

def check_crossover_installation():
    """Check if CrossOver and StarCraft II are properly installed"""
    print("🔍 Checking CrossOver installation...")
    
    crossover_app = Path("/Users/taylor/Applications/CrossOver.app")
    sc2_bottle = Path("/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II")
    sc2_exe = sc2_bottle / "drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"
    wine_exe = crossover_app / "Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
    
    print(f"  CrossOver app: {'✅' if crossover_app.exists() else '❌'} {crossover_app}")
    print(f"  SC2 bottle: {'✅' if sc2_bottle.exists() else '❌'} {sc2_bottle}")
    print(f"  SC2 exe: {'✅' if sc2_exe.exists() else '❌'} {sc2_exe}")
    print(f"  Wine exe: {'✅' if wine_exe.exists() else '❌'} {wine_exe}")
    
    return all([crossover_app.exists(), sc2_bottle.exists(), sc2_exe.exists(), wine_exe.exists()])

def test_wine_direct():
    """Test Wine directly without StarCraft II"""
    print("\n🍷 Testing Wine directly...")
    
    wine_exe = "/Users/taylor/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
    
    try:
        result = subprocess.run([wine_exe, "--version"], 
                              capture_output=True, text=True, timeout=10)
        print(f"  Wine version: {result.stdout.strip()}")
        print(f"  Exit code: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"  ❌ Wine test failed: {e}")
        return False

def test_sc2_direct():
    """Test StarCraft II directly through Wine"""
    print("\n🎮 Testing StarCraft II directly...")
    
    env = os.environ.copy()
    env["WINEPREFIX"] = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II"
    env["WINEDEBUG"] = "-all"
    
    wine_exe = "/Users/taylor/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
    sc2_exe = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"
    
    args = [wine_exe, sc2_exe, "--help"]
    
    try:
        print(f"  Running: {' '.join(args)}")
        result = subprocess.run(args, env=env, capture_output=True, text=True, timeout=30)
        print(f"  Exit code: {result.returncode}")
        print(f"  Stdout: {result.stdout[:200]}...")
        print(f"  Stderr: {result.stderr[:200]}...")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("  ⏰ StarCraft II help command timed out (this might be normal)")
        return True
    except Exception as e:
        print(f"  ❌ StarCraft II test failed: {e}")
        return False

def test_sc2_headless():
    """Test StarCraft II in headless mode"""
    print("\n🎮 Testing StarCraft II headless mode...")
    
    env = os.environ.copy()
    env["WINEPREFIX"] = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II"
    env["WINEDEBUG"] = "-all"
    
    wine_exe = "/Users/taylor/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
    sc2_exe = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"
    
    args = [
        wine_exe, sc2_exe,
        "--headless",
        "--listen", "127.0.0.1",
        "--port", "5001",
        "--dataDir", "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II",
        "--tempDir", "/tmp/sc2_temp",
        "--verbose"
    ]
    
    try:
        print(f"  Starting StarCraft II headless...")
        process = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit for it to start
        time.sleep(5)
        
        # Check if it's still running
        if process.poll() is None:
            print("  ✅ StarCraft II is running in headless mode")
            
            # Test port
            if test_port_connection(5001):
                print("  ✅ Port 5001 is responding")
                process.terminate()
                return True
            else:
                print("  ❌ Port 5001 is not responding")
                process.terminate()
                return False
        else:
            stdout, stderr = process.communicate()
            print(f"  ❌ StarCraft II exited early")
            print(f"  Exit code: {process.returncode}")
            print(f"  Stdout: {stdout[:200]}...")
            print(f"  Stderr: {stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"  ❌ Headless test failed: {e}")
        return False

def test_port_connection(port, timeout=5):
    """Test if a port is responding"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    print("🔧 StarCraft II CrossOver Diagnostic Tool")
    print("=" * 50)
    
    # Check installation
    if not check_crossover_installation():
        print("\n❌ CrossOver or StarCraft II installation issues found!")
        print("Please ensure CrossOver and StarCraft II are properly installed.")
        return False
    
    # Test Wine
    if not test_wine_direct():
        print("\n❌ Wine is not working properly!")
        return False
    
    # Test StarCraft II
    if not test_sc2_direct():
        print("\n❌ StarCraft II is not working properly!")
        return False
    
    # Test headless mode
    if not test_sc2_headless():
        print("\n❌ StarCraft II headless mode is not working!")
        return False
    
    print("\n🎉 All tests passed! StarCraft II should work with the bot.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
