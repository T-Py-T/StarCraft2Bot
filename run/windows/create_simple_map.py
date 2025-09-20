#!/usr/bin/env python3
"""
Create a simple test map for StarCraft II
This is a minimal map file that should allow the bot to start
"""

import os
import sys

# Add src to path so we can import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import *

def create_simple_map():
    """Create a simple test map file"""
    print("=== Creating Simple64 Test Map ===")
    
    # Get the SC2PATH
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
    
    # Create a simple test map file
    simple64_path = os.path.join(maps_dir, "Simple64.SC2Map")
    
    # This is a minimal SC2Map file content (simplified)
    map_content = """<?xml version="1.0" encoding="UTF-8"?>
<map>
    <name>Simple64</name>
    <description>Simple 64x64 test map</description>
    <size>64,64</size>
    <players>2</players>
</map>"""
    
    try:
        with open(simple64_path, 'w') as f:
            f.write(map_content)
        print(f"✓ Created test map: {simple64_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to create map: {e}")
        return False

if __name__ == "__main__":
    create_simple_map() 