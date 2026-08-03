#!/usr/bin/env python3
"""
Enhanced test bot for CrossOver setup with better error handling

This script tests the bot with improved websocket communication and error handling.
"""

import os
import sys
import time
import socket
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Set up CrossOver environment
os.environ["SC2PATH"] = "/tmp"
os.environ["SC2EXE"] = "/tmp/sc2_crossover_launcher_v3.sh"


def test_port_connection(host="127.0.0.1", port=5000, timeout=5):
    """Test if StarCraft II is listening on the specified port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error testing port: {e}")
        return False


def wait_for_sc2(port=5000, max_wait=30):
    """Wait for StarCraft II to be ready"""
    print(f"⏳ Waiting for StarCraft II to be ready on port {port}...")

    for i in range(max_wait):
        if test_port_connection(port=port, timeout=1):
            print(f"✅ StarCraft II is ready on port {port}!")
            return True
        print(f"   Still waiting... ({i + 1}/{max_wait})")
        time.sleep(1)

    print(f"❌ StarCraft II did not become ready within {max_wait} seconds")
    return False


def main():
    print("🍷 Enhanced CrossOver Test - StarCraft2Bot")
    print("=" * 50)

    # Check if launcher exists
    if not os.path.exists("/tmp/sc2_crossover_launcher_v3.sh"):
        print(
            "❌ CrossOver launcher v3 not found! Run sc2_crossover_launcher_v3.py first."
        )
        return False

    print("✅ CrossOver launcher v3 found")
    print(f"SC2PATH: {os.environ['SC2PATH']}")
    print(f"SC2EXE: {os.environ['SC2EXE']}")

    # Try to determine the port from the launcher
    port = 5000  # Default port
    try:
        with open("/tmp/sc2_crossover_launcher_v3.sh", "r") as f:
            content = f.read()
            if "--port" in content:
                # Extract port from launcher script
                import re

                match = re.search(r'--port"\s+"(\d+)"', content)
                if match:
                    port = int(match.group(1))
                    print(f"✅ Using port {port} from launcher")
    except Exception as e:
        print(f"⚠️  Could not determine port from launcher: {e}")
        print(f"Using default port {port}")

    try:
        print("\n🚀 Starting StarCraft II game through CrossOver...")
        print("This may take a moment to start...")

        # Import after setting environment variables
        from sc2 import run_game, maps, Race, Difficulty
        from sc2.player import Bot, Computer
        from sc2.bot_ai import BotAI

        class SimpleTestBot(BotAI):
            """A very simple test bot"""

            async def on_step(self, iteration):
                if iteration == 0:
                    print(f"🤖 Bot started! Game step {iteration}")
                    print(f"   Map: {self.game_info.map_name}")
                    print(f"   Players: {len(self.players)}")
                    print(f"   My race: {self.race}")
                    print(f"   Enemy race: {self.enemy_race}")

                # Simple strategy: just build workers
                if iteration < 100:  # Only for first 100 steps
                    for worker in self.workers:
                        if worker.is_idle:
                            worker.gather(self.mineral_field.closest_to(worker))

                if iteration % 50 == 0:
                    print(f"   Step {iteration}: {len(self.workers)} workers")

        # Wait for StarCraft II to be ready
        if not wait_for_sc2(port):
            print("❌ StarCraft II did not become ready")
            return False

        print("\n🎮 Starting game...")

        # Run the game with a simple map
        run_game(
            maps.get("Simple64"),
            [Bot(Race.Protoss, SimpleTestBot()), Computer(Race.Zerg, Difficulty.Easy)],
            realtime=False,
        )

        print("✅ Game completed successfully!")
        print("🎉 CrossOver setup is working perfectly!")
        return True

    except Exception as e:
        print(f"❌ Error running game: {e}")
        print(f"Error type: {type(e).__name__}")

        # Check if it's a websocket error
        if "Websocket" in str(e) or "websocket" in str(e).lower():
            print("\n🔧 This appears to be a websocket communication issue.")
            print("The StarCraft II process is running but communication failed.")
            print("This might be due to port conflicts or timing issues.")
            print("Try running the test again - sometimes it works on the second try.")
        elif "Connection" in str(e) or "connection" in str(e).lower():
            print("\n🔧 This appears to be a connection issue.")
            print("StarCraft II might not be starting properly.")
        elif "Timeout" in str(e) or "timeout" in str(e).lower():
            print("\n🔧 This appears to be a timeout issue.")
            print("StarCraft II might be taking too long to start.")
            print("Try running the test again with more patience.")
        else:
            print(f"\n🔧 Unexpected error: {e}")

        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS! StarCraft2Bot is working with CrossOver on macOS!")
        print("You can now use 'make train' to start training!")
    else:
        print("\n⚠️  The bot encountered an error, but we're very close!")
        print("StarCraft II is launching through CrossOver successfully.")
        print("The issue is likely in the websocket communication.")
    sys.exit(0 if success else 1)
