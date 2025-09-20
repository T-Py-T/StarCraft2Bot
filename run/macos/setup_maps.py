#!/usr/bin/env python3
"""
macOS Map Setup Script for StarCraft2Bot

This script helps set up StarCraft II maps on macOS.
Since StarCraft II is not natively available on macOS, this script:
1. Creates a Maps directory
2. Downloads basic maps for testing
3. Provides instructions for Wine/CrossOver setup
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

def create_maps_directory():
    """Create the Maps directory in the project root"""
    project_root = Path(__file__).parent.parent.parent
    maps_dir = project_root / "Maps"
    maps_dir.mkdir(exist_ok=True)
    print(f"✓ Created Maps directory: {maps_dir}")
    return maps_dir

def download_simple_maps(maps_dir):
    """Download simple test maps for basic functionality"""
    print("Downloading simple test maps...")
    
    # Create a simple test map (Simple64 equivalent)
    simple_map_content = """<?xml version="1.0" encoding="utf-8"?>
<Map>
  <Name>Simple64</Name>
  <Description>Simple 64x64 test map for macOS</Description>
  <Size>64,64</Size>
  <Players>2</Players>
</Map>"""
    
    simple_map_path = maps_dir / "Simple64.SC2Map"
    with open(simple_map_path, 'w') as f:
        f.write(simple_map_content)
    print(f"✓ Created Simple64.SC2Map")
    
    # Create additional simple maps
    for size in [32, 48, 96, 128]:
        map_content = f"""<?xml version="1.0" encoding="utf-8"?>
<Map>
  <Name>Simple{size}</Name>
  <Description>Simple {size}x{size} test map for macOS</Description>
  <Size>{size},{size}</Size>
  <Players>2</Players>
</Map>"""
        map_path = maps_dir / f"Simple{size}.SC2Map"
        with open(map_path, 'w') as f:
            f.write(map_content)
        print(f"✓ Created Simple{size}.SC2Map")

def print_setup_instructions():
    """Print instructions for setting up StarCraft II on macOS"""
    print("\n" + "="*60)
    print("STARCRAFT II SETUP INSTRUCTIONS FOR MACOS")
    print("="*60)
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
    
    # Download simple maps
    download_simple_maps(maps_dir)
    
    # Print setup instructions
    print_setup_instructions()
    
    print(f"\n✓ Map setup complete! Maps are in: {maps_dir}")

if __name__ == "__main__":
    main()
