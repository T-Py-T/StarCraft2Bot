#!/usr/bin/env python3
"""
Test StarCraft II through CrossOver's application launcher
"""

import os
import sys
import subprocess
from pathlib import Path


def test_crossover_app_launch():
    """Test launching StarCraft II through CrossOver's application launcher"""
    print("🍷 Testing StarCraft II through CrossOver app launcher...")

    # Try to find the CrossOver launcher
    crossover_app = Path("/Users/taylor/Applications/CrossOver.app")
    launcher_script = (
        crossover_app
        / "Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/run"
    )

    if not launcher_script.exists():
        print(f"  ❌ CrossOver launcher not found at {launcher_script}")
        return False

    # Try to launch StarCraft II through CrossOver
    try:
        print(f"  Using CrossOver launcher: {launcher_script}")

        # First, let's see what bottles are available
        print("  📋 Checking available bottles...")
        result = subprocess.run(
            [str(launcher_script), "--list-bottles"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        print(f"  Bottles: {result.stdout}")

        # Try to launch StarCraft II
        print("  🚀 Launching StarCraft II...")
        args = [
            str(launcher_script),
            "--bottle",
            "StarCraft II",
            "--executable",
            "StarCraft II.exe",
            "--args",
            "--help",
        ]

        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        print(f"  Exit code: {result.returncode}")
        print(f"  Stdout: {result.stdout[:200]}...")
        print(f"  Stderr: {result.stderr[:200]}...")

        return result.returncode == 0

    except Exception as e:
        print(f"  ❌ CrossOver app launch failed: {e}")
        return False


def test_direct_wine_with_env():
    """Test Wine directly with proper environment setup"""
    print("\n🍷 Testing Wine with proper environment...")

    env = os.environ.copy()
    env["WINEPREFIX"] = (
        "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II"
    )
    env["WINEDEBUG"] = "-all"
    env["WINEDLLOVERRIDES"] = "mscoree,mshtml="

    wine_exe = "/Users/taylor/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine"
    sc2_exe = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"

    try:
        print(f"  Running: {wine_exe} {sc2_exe} --help")
        result = subprocess.run(
            [wine_exe, sc2_exe, "--help"],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        print(f"  Exit code: {result.returncode}")
        print(f"  Stdout: {result.stdout[:200]}...")
        print(f"  Stderr: {result.stderr[:200]}...")

        return result.returncode == 0

    except Exception as e:
        print(f"  ❌ Direct Wine test failed: {e}")
        return False


def main():
    print("🔧 Testing CrossOver Application Launcher")
    print("=" * 50)

    # Test CrossOver app launcher
    app_success = test_crossover_app_launch()

    # Test direct Wine
    wine_success = test_direct_wine_with_env()

    if app_success or wine_success:
        print("\n🎉 SUCCESS! StarCraft II can be launched through CrossOver!")
        if app_success:
            print("  ✅ CrossOver app launcher works")
        if wine_success:
            print("  ✅ Direct Wine launch works")
    else:
        print("\n❌ Both launch methods failed.")
        print("This suggests a fundamental issue with the CrossOver setup.")
        print("You may need to reinstall StarCraft II through CrossOver.")

    return app_success or wine_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
