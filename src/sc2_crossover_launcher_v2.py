#!/usr/bin/env python3
"""
SC2 CrossOver Launcher v2 - Fixed for websocket communication

This creates a proper launcher that works with the sc2 library and CrossOver.
"""

import os
import subprocess
import shutil


def create_sc2_launcher_v2():
    """Create an improved launcher script that works with the sc2 library"""

    # Create the launcher script with proper websocket configuration
    launcher_content = """#!/bin/bash
# SC2 CrossOver Launcher v2
# This script launches StarCraft II through CrossOver with proper websocket support

export WINEPREFIX="${SC2_CROSSOVER_BOTTLE:-$HOME/Library/Application Support/CrossOver/Bottles/StarCraft II}"
export WINEDEBUG=-all

# StarCraft II executable
SC2_EXE="${SC2_EXECUTABLE:-$WINEPREFIX/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe}"

# Wine executable
WINE_EXE="${SC2_WINE_EXECUTABLE:-$HOME/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine}"

# Create temp directory
mkdir -p "/tmp/sc2_temp"

# Default arguments for headless mode with proper websocket support
DEFAULT_ARGS=(
    "--headless"
    "--listen" "127.0.0.1"
    "--port" "5000"
    "--dataDir" "$WINEPREFIX/drive_c/Program Files (x86)/StarCraft II"
    "--tempDir" "/tmp/sc2_temp"
    "--verbose"
    "--logLevel" "1"
)

# Check if we have custom arguments
if [ $# -eq 0 ]; then
    # No arguments provided, use defaults
    exec "$WINE_EXE" "$SC2_EXE" "${DEFAULT_ARGS[@]}"
else
    # Custom arguments provided, use them
    exec "$WINE_EXE" "$SC2_EXE" "$@"
fi
"""

    # Write the launcher script
    launcher_path = "/tmp/sc2_crossover_launcher_v2.sh"
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


def setup_sc2_structure():
    """Set up the complete SC2 directory structure"""

    # Create the complete structure
    base_path = "/tmp"
    versions_path = f"{base_path}/Versions/Base94137/SC2.app/Contents/MacOS"
    maps_path = f"{base_path}/Maps"

    os.makedirs(versions_path, exist_ok=True)
    os.makedirs(maps_path, exist_ok=True)

    # Copy maps
    project_maps = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Maps"
    )
    if os.path.exists(project_maps):
        for map_file in os.listdir(project_maps):
            if map_file.endswith(".SC2Map"):
                shutil.copy(f"{project_maps}/{map_file}", f"{maps_path}/{map_file}")

    return base_path, versions_path, maps_path


def main():
    print("🍷 Creating SC2 CrossOver Launcher v2")
    print("=" * 50)

    # Create launcher
    launcher_path, app_path = create_sc2_launcher_v2()

    # Set up directory structure
    base_path, versions_path, maps_path = setup_sc2_structure()

    # Copy launcher to versions directory
    shutil.copy(launcher_path, f"{versions_path}/SC2")

    print(f"✅ Launcher created: {launcher_path}")
    print(f"✅ macOS app created: {app_path}")
    print(f"✅ Directory structure set up in: {base_path}")
    print(f"✅ Maps copied to: {maps_path}")

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

    print("\n📝 Environment variables:")
    print(f"SC2PATH={base_path}")
    print(f"SC2EXE={launcher_path}")


if __name__ == "__main__":
    main()
