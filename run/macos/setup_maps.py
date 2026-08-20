#!/usr/bin/env python3
"""
macOS Map Setup Script for StarCraft2Bot

This script helps set up StarCraft II maps on macOS.
Since StarCraft II is not natively available on macOS, this script:
1. Creates a Maps directory
2. Reports genuine map archives already present
3. Provides instructions for Wine/CrossOver setup
"""

from pathlib import Path


def create_maps_directory():
    """Create the Maps directory in the project root"""
    project_root = Path(__file__).parent.parent.parent
    maps_dir = project_root / "Maps"
    maps_dir.mkdir(exist_ok=True)
    print(f"✓ Created Maps directory: {maps_dir}")
    return maps_dir


def report_available_maps(maps_dir):
    """Report genuine SC2 map archives already available to the project."""
    maps = sorted(maps_dir.glob("*.SC2Map"))
    if maps:
        print(f"✓ Found {len(maps)} StarCraft II map archive(s)")
    else:
        print("No .SC2Map archives found; copy maps exported by the SC2 Editor here.")


def print_setup_instructions():
    """Print instructions for setting up StarCraft II on macOS"""
    print("\n" + "=" * 60)
    print("STARCRAFT II SETUP INSTRUCTIONS FOR MACOS")
    print("=" * 60)
    print()
    print("StarCraft II is not natively available on macOS. You have several options:")
    print()
    print("OPTION 1: Wine (Free)")
    print("- Install Wine: brew install --cask wine-stable")
    print("- Install StarCraft II through Wine")
    print("- Update config.py with your Wine installation path")
    print()
    print("OPTION 2: CrossOver (Paid)")
    print("- Install CrossOver from CodeWeavers")
    print("- Install StarCraft II through CrossOver")
    print("- Update config.py with your CrossOver installation path")
    print()
    print("OPTION 3: Virtualization")
    print("- Use Parallels Desktop, VMware, or VirtualBox")
    print("- Install Windows and StarCraft II in the VM")
    print("- Run the bot from within the VM")
    print()
    print("OPTION 4: Remote Development")
    print("- Develop on macOS, run on Windows/Linux")
    print("- Use VS Code Remote Development or similar")
    print()
    print("After setting up StarCraft II, update the paths in src/config.py")
    print("and run: uv run src/trainppo.py")


def main():
    print("StarCraft2Bot macOS Map Setup")
    print("=" * 40)

    # Create maps directory
    maps_dir = create_maps_directory()

    # A .SC2Map is an MPQ archive; plain XML placeholders are not launchable maps.
    report_available_maps(maps_dir)

    # Print setup instructions
    print_setup_instructions()

    print(f"\n✓ Map setup complete! Maps are in: {maps_dir}")


if __name__ == "__main__":
    main()
