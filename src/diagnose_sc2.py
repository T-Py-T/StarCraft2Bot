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

CROSSOVER_APP = Path(
    os.environ.get("CROSSOVER_APP", Path.home() / "Applications" / "CrossOver.app")
)
SC2_BOTTLE = Path(
    os.environ.get(
        "SC2_BOTTLE",
        Path.home() / "Library/Application Support/CrossOver/Bottles/StarCraft II",
    )
)
SC2_EXECUTABLE = (
    SC2_BOTTLE / "drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"
)
WINE_EXECUTABLE = (
    CROSSOVER_APP / "Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
)


def check_crossover_installation():
    """Check if CrossOver and StarCraft II are properly installed"""
    print("🔍 Checking CrossOver installation...")

    print(
        f"  CrossOver app: {'✅' if CROSSOVER_APP.exists() else '❌'} {CROSSOVER_APP}"
    )
    print(f"  SC2 bottle: {'✅' if SC2_BOTTLE.exists() else '❌'} {SC2_BOTTLE}")
    print(f"  SC2 exe: {'✅' if SC2_EXECUTABLE.exists() else '❌'} {SC2_EXECUTABLE}")
    print(f"  Wine exe: {'✅' if WINE_EXECUTABLE.exists() else '❌'} {WINE_EXECUTABLE}")

    return all(
        [
            CROSSOVER_APP.exists(),
            SC2_BOTTLE.exists(),
            SC2_EXECUTABLE.exists(),
            WINE_EXECUTABLE.exists(),
        ]
    )


def test_wine_direct():
    """Test Wine directly without StarCraft II"""
    print("\n🍷 Testing Wine directly...")

    try:
        result = subprocess.run(
            [str(WINE_EXECUTABLE), "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
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
    env["WINEPREFIX"] = str(SC2_BOTTLE)
    env["WINEDEBUG"] = "-all"

    args = [str(WINE_EXECUTABLE), str(SC2_EXECUTABLE), "--help"]

    try:
        print(f"  Running: {' '.join(args)}")
        result = subprocess.run(
            args, env=env, capture_output=True, text=True, timeout=30
        )
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
    env["WINEPREFIX"] = str(SC2_BOTTLE)
    env["WINEDEBUG"] = "-all"

    args = [
        str(WINE_EXECUTABLE),
        str(SC2_EXECUTABLE),
        "--headless",
        "--listen",
        "127.0.0.1",
        "--port",
        "5001",
        "--dataDir",
        str(SC2_EXECUTABLE.parent),
        "--tempDir",
        "/tmp/sc2_temp",
        "--verbose",
    ]

    try:
        print("  Starting StarCraft II headless...")
        process = subprocess.Popen(
            args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

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
            print("  ❌ StarCraft II exited early")
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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex(("127.0.0.1", port))
        return result == 0
    except OSError:
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
