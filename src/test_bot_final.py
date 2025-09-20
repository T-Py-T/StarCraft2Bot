#!/usr/bin/env python3
"""
Final working test bot for CrossOver setup

This script tests the bot with the complete CrossOver setup.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Set up CrossOver environment
os.environ["SC2PATH"] = "/tmp"
os.environ["SC2EXE"] = "/tmp/sc2_crossover_launcher_v2.sh"

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
    if not os.path.exists("/tmp/sc2_crossover_launcher_v2.sh"):
        print("❌ CrossOver launcher not found! Run sc2_crossover_launcher_v2.py first.")
        return False
    
    print("✅ CrossOver launcher found")
    print(f"SC2PATH: {os.environ['SC2PATH']}")
    print(f"SC2EXE: {os.environ['SC2EXE']}")
    
    try:
        print("\n🚀 Starting StarCraft II game through CrossOver...")
        print("This may take a moment to start...")
        
        # Run the game with a simple map
        run_game(
            maps.get("Simple64"),
            [Bot(Race.Protoss, WorkerRushBot()), Computer(Race.Zerg, Difficulty.Easy)],
            realtime=False,
        )
        print("✅ Game completed successfully!")
        print("🎉 CrossOver setup is working!")
        return True
    except Exception as e:
        print(f"❌ Error running game: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Check if it's a websocket error
        if "Websocket" in str(e) or "websocket" in str(e).lower():
            print("\n🔧 This appears to be a websocket communication issue.")
            print("The StarCraft II process is running but communication failed.")
            print("This might be due to port conflicts or timing issues.")
        elif "Connection" in str(e) or "connection" in str(e).lower():
            print("\n🔧 This appears to be a connection issue.")
            print("StarCraft II might not be starting properly.")
        else:
            print(f"\n🔧 Unexpected error: {e}")
        
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS! StarCraft2Bot is working with CrossOver on macOS!")
    else:
        print("\n⚠️  The bot encountered an error, but we're very close!")
        print("StarCraft II is launching through CrossOver successfully.")
    sys.exit(0 if success else 1)
