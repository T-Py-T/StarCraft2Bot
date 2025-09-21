from sc2.main import run_game
from sc2 import maps
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer
from sc2.bot_ai import BotAI

class WorkerRushBot(BotAI):
    async def on_step(self, iteration):
        if iteration == 0:
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])

run_game(
    maps.get("Simple64"),
    [Bot(Race.Protoss, WorkerRushBot()), Computer(Race.Zerg, Difficulty.Easy)],
    realtime=False,
) 