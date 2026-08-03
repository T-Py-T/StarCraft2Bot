#!/usr/bin/env python3
"""
Test StarCraft II in windowed mode through CrossOver
"""

import os
import sys
import subprocess
import time
import socket


def test_sc2_windowed():
    """Test StarCraft II in windowed mode"""
    print("🎮 Testing StarCraft II in windowed mode...")

    env = os.environ.copy()
    env["WINEPREFIX"] = (
        "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II"
    )
    env["WINEDEBUG"] = "-all"

    wine_exe = "/Users/taylor/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
    sc2_exe = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"

    # Try windowed mode first
    args = [
        wine_exe,
        sc2_exe,
        "--listen",
        "127.0.0.1",
        "--port",
        "5001",
        "--dataDir",
        "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II",
        "--tempDir",
        "/tmp/sc2_temp",
        "--verbose",
        "--windowwidth",
        "1024",
        "--windowheight",
        "768",
        "--windowmode",
        "windowed",
    ]

    try:
        print("  Starting StarCraft II in windowed mode...")
        print(f"  Command: {' '.join(args)}")

        process = subprocess.Popen(
            args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Wait a bit for it to start
        print("  ⏳ Waiting for StarCraft II to start...")
        time.sleep(10)

        # Check if it's still running
        if process.poll() is None:
            print("  ✅ StarCraft II is running in windowed mode")

            # Test port
            if test_port_connection(5001):
                print("  ✅ Port 5001 is responding")
                print("  🎉 StarCraft II is working in windowed mode!")

                # Let it run for a bit more
                time.sleep(5)
                process.terminate()
                return True
            else:
                print("  ❌ Port 5001 is not responding")
                process.terminate()
                return False
        else:
            stdout, stderr = process.communicate()
            print("  ❌ StarCraft II exited early")
            print(f"  Exit code: {process.returncode}")
            print(f"  Stdout: {stdout[:200]}...")
            print(f"  Stderr: {stderr[:200]}...")
            return False

    except Exception as e:
        print(f"  ❌ Windowed test failed: {e}")
        return False


def test_port_connection(port, timeout=5):
    """Test if a port is responding"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        return result == 0
    except OSError:
        return False


def main():
    print("🔧 Testing StarCraft II Windowed Mode")
    print("=" * 50)

    success = test_sc2_windowed()

    if success:
        print("\n🎉 SUCCESS! StarCraft II works in windowed mode!")
        print("This means CrossOver is working correctly.")
        print("The issue might be with headless mode specifically.")
    else:
        print("\n❌ StarCraft II windowed mode failed.")
        print("This suggests a fundamental issue with CrossOver setup.")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
