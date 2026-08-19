"""StarCraft II bot used by the reinforcement-learning environment."""

import asyncio
import math
import os
import random
import time
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from config import REALTIME, SAVE_REPLAY, WANDB_MODE
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer

from ipc import REQUEST_PATH, RESPONSE_PATH, empty_observation, load_state, save_state

SRC_DIR = Path(__file__).resolve().parent
RESULTS_PATH = SRC_DIR / ".runtime" / "results.txt"
os.environ["WANDB_MODE"] = WANDB_MODE

VERBOSE = True
ACTION_NAMES = {
    0: "Expand/Mine",
    1: "Build Stargate",
    2: "Build Voidray",
    3: "Scout",
    4: "Attack",
    5: "Flee",
}


class IncrediBot(BotAI):
    """Protoss bot controlled through the atomic RL state protocol."""

    def __init__(self) -> None:
        super().__init__()
        self.prev_stargate_count = 0
        self.episode_reward = 0
        self._step_reward = 0.0
        self._episode_id = os.environ.get("SC2_EPISODE_ID")
        self._request_id = 0

    async def on_start_async(self) -> None:
        if self._episode_id is None:
            raise RuntimeError("SC2_EPISODE_ID is required")
        data = await asyncio.to_thread(load_state, REQUEST_PATH)
        if data["episode_id"] != self._episode_id:
            raise RuntimeError("SC2 episode no longer owns the IPC state")
        self._request_id = data["request_id"]
        data.update(
            {
                "state": empty_observation(),
                "reward": 0,
                "action": None,
                "done": False,
                "ready": True,
            }
        )
        await asyncio.to_thread(save_state, data, RESPONSE_PATH)
        self.prev_stargate_count = 0
        self.episode_reward = 0

    def on_end(self, result: Any) -> None:
        reward = 1000 if str(result) == "Result.Victory" else -1000
        RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with RESULTS_PATH.open("a", encoding="utf-8") as results_file:
            results_file.write(f"{result}\n")
        save_state(
            {
                "state": empty_observation(),
                "reward": reward,
                "action": None,
                "done": True,
                "episode_id": self._episode_id,
                "request_id": self._request_id,
                "ready": True,
            },
            RESPONSE_PATH,
        )
        print(f"[Reward] Game ended with result {result}, reward written: {reward}")

    async def _wait_for_action(self) -> tuple[int, int]:
        while True:
            try:
                state = await asyncio.to_thread(load_state, REQUEST_PATH)
                if state["episode_id"] != self._episode_id:
                    raise RuntimeError("SC2 episode no longer owns the IPC state")
                action = state["action"]
                if action is None or not state["ready"]:
                    await asyncio.sleep(0.01)
                    continue
                request_id = state["request_id"]
                if request_id <= self._request_id:
                    await asyncio.sleep(0.01)
                    continue
                if request_id > self._request_id + 1:
                    raise RuntimeError("SC2 received an out-of-order action request")
                self._request_id = request_id
                return action, request_id
            except (OSError, KeyError, ValueError) as exc:
                print(f"[Error] Could not read action state: {exc}")
                await asyncio.sleep(0.01)

    async def _expand_or_mine(self) -> None:
        found_something = False
        if (
            self.supply_left < 4
            and self.already_pending(UnitTypeId.PYLON) == 0
            and self.can_afford(UnitTypeId.PYLON)
        ):
            await self.build(UnitTypeId.PYLON, near=self.townhalls.random)
            found_something = True

        if not found_something:
            for nexus in self.townhalls:
                worker_count = len(self.workers.closer_than(10, nexus))
                if (
                    worker_count < 22
                    and nexus.is_idle
                    and self.can_afford(UnitTypeId.PROBE)
                ):
                    nexus.train(UnitTypeId.PROBE)
                    found_something = True

                for geyser in self.vespene_geyser.closer_than(10, nexus):
                    if not self.can_afford(UnitTypeId.ASSIMILATOR):
                        break
                    nearby = self.structures(UnitTypeId.ASSIMILATOR).closer_than(
                        2.0, geyser
                    )
                    if not nearby.exists:
                        await self.build(UnitTypeId.ASSIMILATOR, geyser)
                        found_something = True

        if (
            not found_something
            and self.already_pending(UnitTypeId.NEXUS) == 0
            and self.can_afford(UnitTypeId.NEXUS)
        ):
            await self.expand_now()

    async def _build_stargate(self) -> None:
        for nexus in self.townhalls:
            if (
                not self.structures(UnitTypeId.GATEWAY).closer_than(10, nexus).exists
                and self.can_afford(UnitTypeId.GATEWAY)
                and self.already_pending(UnitTypeId.GATEWAY) == 0
            ):
                await self.build(UnitTypeId.GATEWAY, near=nexus)
            if (
                not self.structures(UnitTypeId.CYBERNETICSCORE)
                .closer_than(10, nexus)
                .exists
                and self.can_afford(UnitTypeId.CYBERNETICSCORE)
                and self.already_pending(UnitTypeId.CYBERNETICSCORE) == 0
            ):
                await self.build(UnitTypeId.CYBERNETICSCORE, near=nexus)
            if (
                not self.structures(UnitTypeId.STARGATE).closer_than(10, nexus).exists
                and self.can_afford(UnitTypeId.STARGATE)
                and self.already_pending(UnitTypeId.STARGATE) == 0
            ):
                await self.build(UnitTypeId.STARGATE, near=nexus)

        current_count = self.structures(UnitTypeId.STARGATE).amount
        if current_count > self.prev_stargate_count:
            reward = 100 * (current_count - self.prev_stargate_count)
            self._step_reward += reward
            self.episode_reward += reward
            print(
                f"[Reward] Built {current_count - self.prev_stargate_count} new "
                f"stargate(s): +{reward} reward (total: {self.episode_reward})"
            )
        self.prev_stargate_count = current_count

    def _build_voidrays(self) -> None:
        for stargate in self.structures(UnitTypeId.STARGATE).ready.idle:
            if self.can_afford(UnitTypeId.VOIDRAY):
                stargate.train(UnitTypeId.VOIDRAY)

    def _send_scout(self, iteration: int) -> bool:
        last_sent = getattr(self, "last_sent", 0)
        if iteration - last_sent <= 200:
            return False
        probes = self.units(UnitTypeId.PROBE)
        available_probes = probes.idle if probes.idle.exists else probes
        if not available_probes:
            return False
        probe = available_probes.random
        probe.attack(self.enemy_start_locations[0])
        self.last_sent = iteration
        return True

    def _attack(self) -> None:
        for voidray in self.units(UnitTypeId.VOIDRAY).idle:
            nearby_units = self.enemy_units.closer_than(10, voidray)
            nearby_structures = self.enemy_structures.closer_than(10, voidray)
            if nearby_units:
                target = nearby_units.random
            elif nearby_structures:
                target = nearby_structures.random
            elif self.enemy_units:
                target = self.enemy_units.random
            elif self.enemy_structures:
                target = self.enemy_structures.random
            elif self.enemy_start_locations:
                target = self.enemy_start_locations[0]
            else:
                continue
            voidray.attack(target)

    def _flee(self) -> None:
        for voidray in self.units(UnitTypeId.VOIDRAY):
            voidray.attack(self.start_location)

    async def _perform_action(self, action: int, iteration: int) -> bool:
        try:
            if action == 0:
                await self._expand_or_mine()
            elif action == 1:
                await self._build_stargate()
            elif action == 2:
                self._build_voidrays()
            elif action == 3:
                return self._send_scout(iteration)
            elif action == 4:
                self._attack()
            elif action == 5:
                self._flee()
            else:
                return False
            return True
        except (IndexError, RuntimeError, ValueError) as exc:
            print(f"[Action] {ACTION_NAMES.get(action, 'Unknown')} failed: {exc}")
            return False

    async def _perform_opportunistic_actions(self) -> None:
        idle_stargates = self.structures(UnitTypeId.STARGATE).ready.idle
        if (
            random.random() < 0.7
            and self.can_afford(UnitTypeId.VOIDRAY)
            and idle_stargates.exists
        ):
            idle_stargates.random.train(UnitTypeId.VOIDRAY)
            print("[Opportunistic] Trained a voidray")

        if (
            random.random() < 0.4
            and self.structures(UnitTypeId.CYBERNETICSCORE).ready.exists
            and self.can_afford(UnitTypeId.STARGATE)
            and self.already_pending(UnitTypeId.STARGATE) == 0
        ):
            await self.build(UnitTypeId.STARGATE, near=self.townhalls.random)
            print("[Opportunistic] Built a stargate")

        if (
            random.random() < 0.3
            and self.townhalls.exists
            and self.can_afford(UnitTypeId.GATEWAY)
            and self.already_pending(UnitTypeId.GATEWAY) == 0
        ):
            await self.build(UnitTypeId.GATEWAY, near=self.townhalls.random)
            print("[Opportunistic] Built a gateway")

    @staticmethod
    def _draw_health(
        observation: np.ndarray, unit: Any, color: tuple[int, int, int]
    ) -> None:
        position = unit.position
        fraction = unit.health / unit.health_max if unit.health_max > 0 else 0.0001
        observation[math.ceil(position.y)][math.ceil(position.x)] = [
            int(fraction * channel) for channel in color
        ]

    def _render_observation(self) -> np.ndarray:
        width, height = self.game_info.map_size
        observation = np.zeros((height, width, 3), dtype=np.uint8)

        for mineral in self.mineral_field:
            position = mineral.position
            color = (175, 255, 255)
            if mineral.is_visible:
                fraction = mineral.mineral_contents / 1800
                pixel = [int(fraction * channel) for channel in color]
            else:
                pixel = [20, 75, 50]
            observation[math.ceil(position.y)][math.ceil(position.x)] = pixel

        for location in self.enemy_start_locations:
            observation[math.ceil(location.y)][math.ceil(location.x)] = [0, 0, 255]
        for unit in self.enemy_units:
            self._draw_health(observation, unit, (100, 0, 255))
        for structure in self.enemy_structures:
            self._draw_health(observation, structure, (0, 100, 255))
        for structure in self.structures:
            color = (
                (255, 255, 175)
                if structure.type_id == UnitTypeId.NEXUS
                else (0, 255, 175)
            )
            self._draw_health(observation, structure, color)

        for geyser in self.vespene_geyser:
            position = geyser.position
            if geyser.is_visible:
                fraction = geyser.vespene_contents / 2250
                pixel = [int(fraction * channel) for channel in (255, 175, 255)]
            else:
                pixel = [50, 20, 75]
            observation[math.ceil(position.y)][math.ceil(position.x)] = pixel

        for unit in self.units:
            color = (
                (255, 75, 75) if unit.type_id == UnitTypeId.VOIDRAY else (175, 255, 0)
            )
            self._draw_health(observation, unit, color)

        if os.environ.get("SC2_HEADLESS") != "1":
            cv2.imshow(
                "map",
                cv2.flip(
                    cv2.resize(
                        observation,
                        None,
                        fx=4,
                        fy=4,
                        interpolation=cv2.INTER_NEAREST,
                    ),
                    0,
                ),
            )
            cv2.waitKey(1)
        return observation

    def _combat_reward(self) -> float:
        try:
            return sum(
                0.015
                for voidray in self.units(UnitTypeId.VOIDRAY)
                if voidray.is_attacking
                and voidray.target_in_range
                and (
                    self.enemy_units.closer_than(8, voidray)
                    or self.enemy_structures.closer_than(8, voidray)
                )
            )
        except (AttributeError, RuntimeError, TypeError) as exc:
            print(f"reward {exc}")
            return 0

    def _reward_new_voidrays(self) -> float:
        current_count = self.units(UnitTypeId.VOIDRAY).amount
        previous_count = getattr(self, "prev_voidray_count", 0)
        if current_count > previous_count:
            reward = 80 * (current_count - previous_count)
            self.episode_reward += reward
            print(
                f"[Reward] Trained {current_count - previous_count} new voidray(s): "
                f"+{reward} reward (total: {self.episode_reward})"
            )
        else:
            reward = 0
        self.prev_voidray_count = current_count
        return reward

    def _reward_command(
        self, action: int, iteration: int, action_performed: bool
    ) -> float:
        command_rewards = {
            3: ("prev_scout_sent", 30, "Scout reward"),
            4: ("prev_attack_issued", 50, "Attack command reward"),
        }
        if not action_performed or action not in command_rewards:
            return 0
        attribute, reward, description = command_rewards[action]
        if iteration == getattr(self, attribute, 0):
            return 0
        self.episode_reward += reward
        print(
            f"[Reward] {description}: +{reward} reward (total: {self.episode_reward})"
        )
        setattr(self, attribute, iteration)
        return reward

    def _inaction_penalty(self, action: int, iteration: int) -> float:
        last_action = getattr(self, "last_non_mining_action", iteration)
        if action != 0:
            self.last_non_mining_action = iteration
            return 0
        if iteration - last_action <= 300:
            self.last_non_mining_action = last_action
            return 0
        penalty = -40
        self.episode_reward += penalty
        print(f"[Penalty] Inaction too long: {penalty} (total: {self.episode_reward})")
        self.last_non_mining_action = iteration
        return penalty

    async def on_step(self, iteration: int) -> None:
        if not getattr(self, "mineral_field", None):
            return

        self._step_reward = 0
        action, request_id = await self._wait_for_action()
        await self.distribute_workers()
        action_performed = await self._perform_action(action, iteration)
        await self._perform_opportunistic_actions()

        observation = self._render_observation()
        if SAVE_REPLAY:
            cv2.imwrite(f"replays/{int(time.time())}-{iteration}.png", observation)

        reward = (
            self._combat_reward()
            + self._step_reward
            + self._reward_new_voidrays()
            + self._reward_command(action, iteration, action_performed)
            + self._inaction_penalty(action, iteration)
        )
        if iteration % 100 == 0:
            count = self.units(UnitTypeId.VOIDRAY).amount
            print(f"Iter: {iteration}. RWD: {reward}. VR: {count}")

        normalized_observation = cv2.resize(
            observation, (224, 224), interpolation=cv2.INTER_AREA
        )
        await asyncio.to_thread(
            save_state,
            {
                "state": normalized_observation,
                "reward": reward,
                "action": None,
                "done": False,
                "episode_id": self._episode_id,
                "request_id": request_id,
                "ready": True,
            },
            RESPONSE_PATH,
        )


if __name__ == "__main__":
    run_game(
        maps.get("AbyssalReefLE"),
        [Bot(Race.Protoss, IncrediBot()), Computer(Race.Zerg, Difficulty.Easy)],
        realtime=REALTIME,
    )
