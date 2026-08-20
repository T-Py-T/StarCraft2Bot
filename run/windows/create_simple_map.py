#!/usr/bin/env python3
"""
Install a genuine Simple64 map archive for StarCraft II.

The source defaults to Maps/Simple64.SC2Map and can be overridden with
SC2_MAP_SOURCE.
"""

import shutil
import sys
from pathlib import Path

# Add src to path so we can import config
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import config  # noqa: E402  # sets SC2PATH for the detected platform


def create_simple_map():
    """Copy a genuine Simple64 archive into the SC2 Maps directory."""
    print("=== Creating Simple64 Test Map ===")

    # Get the SC2PATH
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

    # Copy a genuine map archive; plain XML is not a valid .SC2Map file.
    simple64_path = maps_dir / "Simple64.SC2Map"
    source_path = Path(
        config.os.environ.get(
            "SC2_MAP_SOURCE", PROJECT_ROOT / "Maps" / "Simple64.SC2Map"
        )
    )
    try:
        if not source_path.is_file():
            print(
                "✗ A genuine SC2 map archive is required. Set SC2_MAP_SOURCE "
                "to a Simple64.SC2Map exported by the SC2 Editor."
            )
            return False
        shutil.copy2(source_path, simple64_path)
        print(f"✓ Created test map: {simple64_path}")
        return True
    except OSError as e:
        print(f"✗ Failed to create map: {e}")
        return False


if __name__ == "__main__":
    create_simple_map()
