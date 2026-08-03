"""Gymnasium environment for the StarCraft II bot."""

from __future__ import annotations

import os
import subprocess
import sys
import time
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces

if __package__:
    from .config import WANDB_MODE
    from .ipc import (
        REQUEST_PATH,
        RESPONSE_PATH,
        empty_observation,
        load_state,
        save_state,
    )
else:
    from config import WANDB_MODE
    from ipc import (
        REQUEST_PATH,
        RESPONSE_PATH,
        empty_observation,
        load_state,
        save_state,
    )

os.environ["WANDB_MODE"] = WANDB_MODE

HEADLESS = True
RETRY_DELAY_SECONDS = 0.01
READY_TIMEOUT_SECONDS = 120.0
RESPONSE_TIMEOUT_SECONDS = 30.0


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
        self._episode_id: str | None = None
        self._request_id = 0

    @staticmethod
    def _failure_response() -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        return empty_observation(), 0.0, True, False, {}

    @staticmethod
    def _matches_response(
        state: dict[str, Any], episode_id: str, request_id: int
    ) -> bool:
        return (
            state["episode_id"] == episode_id
            and state["ready"]
            and state["action"] is None
            and (state["done"] or state["request_id"] == request_id)
        )

    def _wait_for_state(
        self,
        path: Path,
        predicate: Callable[[dict[str, Any]], bool],
        timeout_seconds: float,
    ) -> dict[str, Any] | None:
        deadline = time.monotonic() + timeout_seconds
        while True:
            try:
                state = load_state(path)
                if predicate(state):
                    return state
            except (OSError, KeyError, ValueError):
                pass
            if self._bot_process is None or self._bot_process.poll() is not None:
                try:
                    final_state = load_state(path)
                    return final_state if predicate(final_state) else None
                except (OSError, KeyError, ValueError):
                    return None
            if time.monotonic() >= deadline:
                return None
            time.sleep(RETRY_DELAY_SECONDS)

    def _stop_bot_process(self) -> None:
        process = self._bot_process
        self._bot_process = None
        if process is None or process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

    def _invalidate_episode(self) -> None:
        self._stop_bot_process()
        self._episode_id = None
        save_state(
            {
                "state": empty_observation(),
                "reward": 0,
                "action": None,
                "done": True,
                "episode_id": uuid.uuid4().hex,
                "request_id": self._request_id,
                "ready": False,
            },
            REQUEST_PATH,
        )

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        episode_id = self._episode_id
        if episode_id is None:
            print("[Error] step(): environment has no active episode")
            return self._failure_response()

        request_state = self._wait_for_state(
            RESPONSE_PATH,
            lambda state: self._matches_response(state, episode_id, self._request_id),
            READY_TIMEOUT_SECONDS,
        )
        if request_state is None:
            print("[Error] step(): bot did not become ready")
            self._invalidate_episode()
            return self._failure_response()
        if request_state["done"]:
            return (
                request_state["state"],
                request_state["reward"],
                True,
                False,
                {},
            )

        self._request_id += 1
        save_state(
            {
                "state": empty_observation(),
                "reward": 0,
                "action": int(action),
                "done": False,
                "episode_id": episode_id,
                "request_id": self._request_id,
                "ready": True,
            },
            REQUEST_PATH,
        )

        response_state = self._wait_for_state(
            RESPONSE_PATH,
            lambda state: self._matches_response(state, episode_id, self._request_id),
            RESPONSE_TIMEOUT_SECONDS,
        )
        if response_state is None:
            print("[Error] step(): bot response timed out")
            self._invalidate_episode()
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
        self._stop_bot_process()
        observation = empty_observation()
        episode_id = uuid.uuid4().hex
        self._episode_id = episode_id
        self._request_id = 0
        save_state(
            {
                "state": observation,
                "reward": 0,
                "action": None,
                "done": False,
                "episode_id": episode_id,
                "request_id": 0,
                "ready": False,
            },
            REQUEST_PATH,
        )

        script_path = Path(__file__).resolve().with_name("incredibot-sct.py")
        environment = os.environ.copy()
        environment["SC2_EPISODE_ID"] = episode_id
        if HEADLESS:
            environment["SC2_HEADLESS"] = "1"
        self._bot_process = subprocess.Popen(
            [sys.executable, str(script_path)], env=environment
        )
        return observation, {}

    def close(self) -> None:
        self._stop_bot_process()
        self._episode_id = None
