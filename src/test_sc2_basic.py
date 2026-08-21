#!/usr/bin/env python3
"""
Test StarCraft II basic launch through CrossOver
"""

import os
import sys
import subprocess
import time
import socket


def test_sc2_basic_launch():
    """Test StarCraft II with minimal arguments"""
    print("🎮 Testing StarCraft II basic launch...")

    env = os.environ.copy()
    env["WINEPREFIX"] = os.path.expanduser(
        os.environ.get(
            "SC2_CROSSOVER_BOTTLE",
            "~/Library/Application Support/CrossOver/Bottles/StarCraft II",
        )
    )
    env["WINEDEBUG"] = "-all"
    env["WINEDLLOVERRIDES"] = "mscoree,mshtml="

    wine_exe = os.path.expanduser(
        os.environ.get(
            "SC2_WINE_EXECUTABLE",
            "~/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/"
            "CrossOver-Hosted Application/wine",
        )
    )
    sc2_exe = os.path.expanduser(
        os.environ.get(
            "SC2_EXECUTABLE",
            "~/Library/Application Support/CrossOver/Bottles/StarCraft II/"
            "drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe",
        )
    )

    # Try with minimal arguments first
    args = [wine_exe, sc2_exe]

    try:
        print(f"  Running: {' '.join(args)}")
        print("  This will open StarCraft II in windowed mode...")
        print("  Please check if a StarCraft II window appears!")

        process = subprocess.Popen(
            args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Wait a bit for it to start
        print("  ⏳ Waiting for StarCraft II to start...")
        time.sleep(15)

        # Check if it's still running
        if process.poll() is None:
            print("  ✅ StarCraft II is running!")
            print("  🎉 Basic launch successful!")

            # Let it run for a bit more
            time.sleep(5)
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print("  ❌ StarCraft II exited early")
            print(f"  Exit code: {process.returncode}")
            print(f"  Stdout: {stdout[:200]}...")
            print(f"  Stderr: {stderr[:200]}...")
            return False

    except Exception as e:
        print(f"  ❌ Basic launch failed: {e}")
        return False


def test_sc2_with_listen():
    """Test StarCraft II with listen arguments"""
    print("\n🎮 Testing StarCraft II with listen arguments...")

    env = os.environ.copy()
    env["WINEPREFIX"] = os.path.expanduser(
        os.environ.get(
            "SC2_CROSSOVER_BOTTLE",
            "~/Library/Application Support/CrossOver/Bottles/StarCraft II",
        )
    )
    env["WINEDEBUG"] = "-all"
    env["WINEDLLOVERRIDES"] = "mscoree,mshtml="

    wine_exe = os.path.expanduser(
        os.environ.get(
            "SC2_WINE_EXECUTABLE",
            "~/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/"
            "CrossOver-Hosted Application/wine",
        )
    )
    sc2_exe = os.path.expanduser(
        os.environ.get(
            "SC2_EXECUTABLE",
            "~/Library/Application Support/CrossOver/Bottles/StarCraft II/"
            "drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe",
        )
    )

    # Try with listen arguments
    args = [wine_exe, sc2_exe, "--listen", "127.0.0.1", "--port", "5001"]

    try:
        print(f"  Running: {' '.join(args)}")
        print("  This will open StarCraft II with network listening...")

        process = subprocess.Popen(
            args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Wait a bit for it to start
        print("  ⏳ Waiting for StarCraft II to start...")
        time.sleep(15)

        # Check if it's still running
        if process.poll() is None:
            print("  ✅ StarCraft II is running with listen mode!")

            # Test port
            if test_port_connection(5001):
                print("  ✅ Port 5001 is responding!")
                print("  🎉 Listen mode successful!")
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
        print(f"  ❌ Listen mode failed: {e}")
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
    print("🔧 Testing StarCraft II Basic Launch")
    print("=" * 50)

    # Test basic launch
    basic_success = test_sc2_basic_launch()

    if basic_success:
        # Test with listen mode
        listen_success = test_sc2_with_listen()

        if listen_success:
            print("\n🎉 SUCCESS! StarCraft II works with CrossOver!")
            print("The bot should be able to connect to it.")
            return True
        else:
            print("\n⚠️  Basic launch works, but listen mode failed.")
            print("This might be a configuration issue.")
            return False
    else:
        print("\n❌ Basic launch failed.")
        print("StarCraft II is not working properly through CrossOver.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
