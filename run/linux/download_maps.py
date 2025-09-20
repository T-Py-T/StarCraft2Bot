#!/usr/bin/env python3
"""
Helper script to download StarCraft II maps
This is useful for users with incomplete StarCraft II installations (e.g., Xbox Game Pass)
"""

import os
import sys
import urllib.request
import zipfile
import tempfile

# Add src to path so we can import config
sys.path.insert(0, 'src')

from config import *

def download_maps():
    """Download basic StarCraft II maps"""
    print("=== StarCraft II Maps Downloader ===")
    
    # Get the SC2PATH from environment (set by config.py)
    sc2path = os.environ.get("SC2PATH")
    if not sc2path:
        print("Error: SC2PATH not set. Run the bot first to set it up.")
        return False
    
    maps_dir = os.path.join(sc2path, "Maps")
    print(f"SC2PATH: {sc2path}")
    print(f"Maps directory: {maps_dir}")
    
    # Create Maps directory if it doesn't exist
    if not os.path.exists(maps_dir):
        os.makedirs(maps_dir)
        print(f"Created Maps directory: {maps_dir}")
    
    # Also create a Maps directory in the project root for fallback
    project_maps_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Maps")
    if not os.path.exists(project_maps_dir):
        os.makedirs(project_maps_dir)
        print(f"Created project Maps directory: {project_maps_dir}")
    
    # List of basic maps to download
    maps = [
        "Simple64",
        "2000AtmospheresAIE", 
        "AcropolisLE",
        "Bel'ShirVestigeLE",
        "CactusValleyLE",
        "CatallenaLE",
        "CentralProtocol",
        "DuskTowers",
        "EchoLE",
        "FrostLE",
        "HabitationStationLE",
        "KairosJunction",
        "KingSejongStation",
        "NewkirkPrecinctTE",
        "PaladinoTerminalLE",
        "ProximaStation",
        "Sequencer",
        "ThunderbirdLE",
        "Triton",
        "WintersGateLE"
    ]
    
    print(f"\nAttempting to download {len(maps)} maps...")
    print("Note: This script will try to download maps from the sc2 library.")
    print("If this fails, you may need to:")
    print("1. Install StarCraft II from Battle.net instead of Xbox Game Pass")
    print("2. Or manually download maps from the StarCraft II community")
    print("3. Or use only built-in maps (Simple64, etc.)")
    
    success_count = 0
    for map_name in maps:
        try:
            # Try to get the map from sc2 library
            from sc2 import maps
            map_path = maps.get(map_name)
            if map_path and os.path.exists(map_path):
                # Copy to both Maps directories
                import shutil
                
                # Copy to StarCraft II Maps directory
                dest_path = os.path.join(maps_dir, f"{map_name}.SC2Map")
                shutil.copy2(map_path, dest_path)
                
                # Copy to project Maps directory as fallback
                project_dest_path = os.path.join(project_maps_dir, f"{map_name}.SC2Map")
                shutil.copy2(map_path, project_dest_path)
                
                print(f"✓ Downloaded: {map_name} (copied to both locations)")
                success_count += 1
            else:
                print(f"✗ Not available: {map_name}")
        except Exception as e:
            print(f"✗ Failed to download {map_name}: {e}")
    
    print(f"\nDownload complete: {success_count}/{len(maps)} maps downloaded")
    
    if success_count == 0:
        print("\nNo maps were downloaded. You can still run the bot with built-in maps:")
        print("- Simple64")
        print("- 2000AtmospheresAIE") 
        print("- And other maps that come with the sc2 library")
    
    return success_count > 0

if __name__ == "__main__":
    download_maps() 