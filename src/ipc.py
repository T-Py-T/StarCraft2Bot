"""Safe, atomic state exchange between the SC2 bot and Gym environment."""

import os
from pathlib import Path
from typing import Any

import numpy as np

RUNTIME_DIR = Path(
    os.environ.get("SC2_RUNTIME_DIR", Path(__file__).resolve().parent / ".runtime")
)
STATE_PATH = RUNTIME_DIR / "state.npz"


def empty_observation() -> np.ndarray:
    return np.zeros((224, 224, 3), dtype=np.uint8)


def load_state(path: Path = STATE_PATH) -> dict[str, Any]:
    """Load state without allowing executable object payloads."""
    with np.load(path, allow_pickle=False) as archive:
        encoded_action = int(archive["action"])
        return {
            "state": archive["state"],
            "reward": float(archive["reward"]),
            "action": None if encoded_action == -1 else encoded_action,
            "done": bool(archive["done"]),
        }


def save_state(data: dict[str, Any], path: Path = STATE_PATH) -> None:
    """Atomically publish state so readers never observe a partial write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    with temporary_path.open("wb") as state_file:
        np.savez(
            state_file,
            state=np.asarray(data["state"], dtype=np.uint8),
            reward=float(data["reward"]),
            action=-1 if data["action"] is None else int(data["action"]),
            done=bool(data["done"]),
        )
    temporary_path.replace(path)


def add_reward(amount: float, path: Path = STATE_PATH) -> None:
    data = load_state(path)
    data["reward"] += amount
    save_state(data, path)
