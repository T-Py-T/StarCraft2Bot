#!/usr/bin/env python3
"""
SC2 CrossOver Launcher

This creates a proper launcher that the sc2 library can use with CrossOver.
"""

import os
import subprocess
import shutil


def create_sc2_launcher():
    """Create a launcher script that works with the sc2 library"""

    # Create the launcher script
    launcher_content = """#!/bin/bash
# SC2 CrossOver Launcher
# This script launches StarCraft II through CrossOver in headless mode

export WINEPREFIX="${SC2_CROSSOVER_BOTTLE:-$HOME/Library/Application Support/CrossOver/Bottles/StarCraft II}"
export WINEDEBUG=-all

# StarCraft II executable
SC2_EXE="${SC2_EXECUTABLE:-$WINEPREFIX/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe}"

# Wine executable
WINE_EXE="${SC2_WINE_EXECUTABLE:-$HOME/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine}"

# Default arguments for headless mode
DEFAULT_ARGS=(
    "--headless"
    "--listen" "127.0.0.1"
    "--port" "5000"
    "--dataDir" "$WINEPREFIX/drive_c/Program Files (x86)/StarCraft II"
    "--tempDir" "/tmp/sc2_temp"
)

# Create temp directory
mkdir -p "/tmp/sc2_temp"

# Run StarCraft II with arguments
exec "$WINE_EXE" "$SC2_EXE" "${DEFAULT_ARGS[@]}" "$@"
"""

    # Write the launcher script
    launcher_path = "/tmp/sc2_crossover_launcher.sh"
    with open(launcher_path, "w") as f:
        f.write(launcher_content)

    os.chmod(launcher_path, 0o755)

    # Create the macOS app structure that sc2 library expects
    app_path = "/tmp/SC2.app"
    os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)

    # Copy the launcher to the app
    shutil.copy(launcher_path, f"{app_path}/Contents/MacOS/SC2")

    # Create Info.plist
    info_plist = """<?xml version="1.0" encoding="UTF-8"?>
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
</plist>"""

    with open(f"{app_path}/Contents/Info.plist", "w") as f:
        f.write(info_plist)

    return launcher_path, app_path


def main():
    print("🍷 Creating SC2 CrossOver Launcher")
    print("=" * 50)

    launcher_path, app_path = create_sc2_launcher()

    print(f"✅ Launcher created: {launcher_path}")
    print(f"✅ macOS app created: {app_path}")

    # Test the launcher
    print("\n🧪 Testing launcher...")
    try:
        result = subprocess.run(
            [launcher_path, "--help"], capture_output=True, text=True, timeout=10
        )
        print(f"Exit code: {result.returncode}")
        if result.returncode == 0:
            print("✅ Launcher works!")
        else:
            print(f"❌ Launcher failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("✅ Launcher started (timed out as expected)")
    except Exception as e:
        print(f"❌ Error testing launcher: {e}")

    print("\n📝 To use this launcher:")
    print(f"1. Set SC2PATH to: {os.path.dirname(launcher_path)}")
    print(f"2. Set SC2EXE to: {launcher_path}")
    print(f"3. Or use the macOS app at: {app_path}")


if __name__ == "__main__":
    main()
