"""Gymnasium environment for the StarCraft II bot."""

import os
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces

if __package__:
    from .config import WANDB_MODE
    from .ipc import empty_observation, load_state, save_state
else:
    from config import WANDB_MODE
    from ipc import empty_observation, load_state, save_state

os.environ["WANDB_MODE"] = WANDB_MODE

HEADLESS = True
MAX_ATTEMPTS = 200
RETRY_DELAY_SECONDS = 0.01


class Sc2Env(gym.Env):
    """Exchange Gym actions and observations with a managed SC2 bot process."""

    metadata = {"render_modes": []}

    def __init__(self) -> None:
        super().__init__()
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(224, 224, 3),
            dtype=np.uint8,
        )
        self._bot_process: subprocess.Popen[bytes] | None = None

    @staticmethod
    def _failure_response() -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        return empty_observation(), 0.0, True, False, {}

    @staticmethod
    def _wait_for_state(
        predicate: Callable[[dict[str, Any]], bool],
    ) -> dict[str, Any] | None:
        for _ in range(MAX_ATTEMPTS):
            try:
                state = load_state()
                if predicate(state):
                    return state
            except (OSError, KeyError, ValueError):
                pass
            time.sleep(RETRY_DELAY_SECONDS)
        return None

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        request_state = self._wait_for_state(lambda state: state["action"] is None)
        if request_state is None:
            print(f"[Error] step(): no action slot after {MAX_ATTEMPTS} attempts")
            return self._failure_response()

        request_state["action"] = int(action)
        save_state(request_state)

        response_state = self._wait_for_state(lambda state: state["action"] is None)
        if response_state is None:
            print(f"[Error] step(): no bot response after {MAX_ATTEMPTS} attempts")
            return self._failure_response()

        return (
            response_state["state"],
            response_state["reward"],
            response_state["done"],
            False,
            {},
        )

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        super().reset(seed=seed)
        observation = empty_observation()
        save_state(
            {
                "state": observation,
                "reward": 0,
                "action": None,
                "done": False,
            }
        )

        if self._bot_process is None or self._bot_process.poll() is not None:
            script_path = Path(__file__).resolve().with_name("incredibot-sct.py")
            environment = os.environ.copy()
            if HEADLESS:
                environment["SC2_HEADLESS"] = "1"
            self._bot_process = subprocess.Popen(
                [sys.executable, str(script_path)], env=environment
            )
        return observation, {}

    def close(self) -> None:
        if self._bot_process is None or self._bot_process.poll() is not None:
            return
        self._bot_process.terminate()
        try:
            self._bot_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._bot_process.kill()
            self._bot_process.wait(timeout=5)
        finally:
            self._bot_process = None
