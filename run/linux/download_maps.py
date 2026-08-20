#!/usr/bin/env python3
"""Copy genuine StarCraft II maps already discoverable by python-sc2.

This stages existing archives in both the SC2 installation and project Maps
directories; it does not download maps from the network.
"""

import shutil
import sys
from pathlib import Path

# Add src to path so we can import config
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import config  # noqa: E402, F401  # sets SC2PATH for the detected platform


def download_maps():
    """Copy discoverable map archives into the configured map directories."""
    print("=== StarCraft II Maps Downloader ===")

    # Get the SC2PATH from environment (set by config.py)
    sc2path = config.os.environ.get("SC2PATH")
    if not sc2path:
        print("Error: SC2PATH not set. Run the bot first to set it up.")
        return False

    maps_dir = Path(sc2path) / "Maps"
    print(f"SC2PATH: {sc2path}")
    print(f"Maps directory: {maps_dir}")

    # Create Maps directory if it doesn't exist
    if not maps_dir.exists():
        maps_dir.mkdir(parents=True)
        print(f"Created Maps directory: {maps_dir}")

    # Also create a Maps directory in the project root for fallback
    project_maps_dir = PROJECT_ROOT / "Maps"
    if not project_maps_dir.exists():
        project_maps_dir.mkdir(parents=True)
        print(f"Created project Maps directory: {project_maps_dir}")

    # Map names python-sc2 may already be able to resolve.
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
        "WintersGateLE",
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
            if map_path and Path(map_path).exists():
                # Copy to StarCraft II Maps directory
                dest_path = maps_dir / f"{map_name}.SC2Map"
                shutil.copy2(map_path, dest_path)

                # Copy to project Maps directory as fallback
                project_dest_path = project_maps_dir / f"{map_name}.SC2Map"
                shutil.copy2(map_path, project_dest_path)

                print(f"✓ Downloaded: {map_name} (copied to both locations)")
                success_count += 1
            else:
                print(f"✗ Not available: {map_name}")
        except Exception as e:
            print(f"✗ Failed to download {map_name}: {e}")

    print(f"\nDownload complete: {success_count}/{len(maps)} maps downloaded")

    if success_count == 0:
        print(
            "\nNo maps were downloaded. You can still run the bot with built-in maps:"
        )
        print("- Simple64")
        print("- 2000AtmospheresAIE")
        print("- And other maps that come with the sc2 library")

    return success_count > 0


if __name__ == "__main__":
    download_maps()
