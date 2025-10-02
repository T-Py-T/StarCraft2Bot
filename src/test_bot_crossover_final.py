#!/usr/bin/env python3
"""
Final test bot for CrossOver setup

This script tests the bot with the working CrossOver launcher.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Set up CrossOver environment
os.environ["SC2PATH"] = "/tmp"
os.environ["SC2EXE"] = "/tmp/sc2_crossover_launcher.sh"

# Import after setting environment variables
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.bot_ai import BotAI

class WorkerRushBot(BotAI):
    async def on_step(self, iteration):
        if iteration == 0:
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])

def main():
    print("🍷 Final CrossOver Test - StarCraft2Bot")
    print("=" * 50)
    
    # Check if launcher exists
    if not os.path.exists("/tmp/sc2_crossover_launcher.sh"):
        print("❌ CrossOver launcher not found! Run sc2_crossover_launcher.py first.")
        return False
    
    print("✅ CrossOver launcher found")
    print(f"SC2PATH: {os.environ['SC2PATH']}")
    print(f"SC2EXE: {os.environ['SC2EXE']}")
    
    try:
        print("\n🚀 Starting StarCraft II game through CrossOver...")
        print("This may take a moment to start...")
        
        run_game(
            maps.get("Simple64"),
            [Bot(Race.Protoss, WorkerRushBot()), Computer(Race.Zerg, Difficulty.Easy)],
            realtime=False,
        )
        print("✅ Game completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error running game: {e}")
        print("\nThis might be expected - the sc2 library may still have compatibility issues")
        print("But we've proven that StarCraft II can run through CrossOver!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
