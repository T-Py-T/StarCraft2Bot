#!/usr/bin/env python3
"""
Test bot with headless mode and result logging
"""

import sys
import time
from sc2.main import run_game
from sc2 import maps
from sc2.data import Race, Difficulty, Result
from sc2.player import Bot, Computer
from sc2.bot_ai import BotAI


class WorkerRushBot(BotAI):
    async def on_step(self, iteration):
        if iteration == 0:
            print(f"Game started! Workers: {len(self.workers)}")
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])

        if iteration % 100 == 0:  # Log every 100 iterations
            print(
                f"Iteration {iteration}: Workers: {len(self.workers)}, Enemies: {len(self.enemy_units)}"
            )

    async def on_end(self, game_result):
        print(f"\n{'=' * 50}")
        print("GAME ENDED!")
        print(f"Result: {game_result}")
        if game_result == Result.Victory:
            print("🎉 WE WON!")
        elif game_result == Result.Defeat:
            print("😞 We lost...")
        else:
            print(f"Game ended with: {game_result}")
        print(f"{'=' * 50}\n")


def main():
    print("Starting StarCraft II bot test in HEADLESS mode...")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # Run in headless mode (no graphics)
        result = run_game(
            maps.get("Simple64"),
            [Bot(Race.Protoss, WorkerRushBot()), Computer(Race.Zerg, Difficulty.Easy)],
            realtime=False,
            disable_fog=True,  # Disable fog of war for easier debugging
            # Headless mode parameters
            rgb_render_config=None,  # No rendering
            # sc2_version="4.10.0",  # Specific version if needed
        )

        print(f"\nFINAL RESULT: {result}")
        return result

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    start_time = time.time()
    result = main()
    end_time = time.time()

    print(f"\nTest completed in {end_time - start_time:.2f} seconds")
    print(f"Final result: {result}")

    # Exit with appropriate code
    if result == Result.Victory:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure or error
