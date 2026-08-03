"""Safe, atomic state exchange between the SC2 bot and Gym environment."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

import numpy as np

RUNTIME_DIR = Path(
    os.environ.get("SC2_RUNTIME_DIR", Path(__file__).resolve().parent / ".runtime")
)
REQUEST_PATH = RUNTIME_DIR / "request.npz"
RESPONSE_PATH = RUNTIME_DIR / "response.npz"


def empty_observation() -> np.ndarray:
    return np.zeros((224, 224, 3), dtype=np.uint8)


def load_state(path: Path) -> dict[str, Any]:
    """Load state without allowing executable object payloads."""
    with np.load(path, allow_pickle=False) as archive:
        encoded_action = int(archive["action"])
        return {
            "state": archive["state"],
            "reward": float(archive["reward"]),
            "action": None if encoded_action == -1 else encoded_action,
            "done": bool(archive["done"]),
            "episode_id": str(archive["episode_id"]),
            "request_id": int(archive["request_id"]),
            "ready": bool(archive["ready"]),
        }


def save_state(data: dict[str, Any], path: Path) -> None:
    """Atomically publish state so readers never observe a partial write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as state_file:
            temporary_path = Path(state_file.name)
            np.savez(
                state_file,
                state=np.asarray(data["state"], dtype=np.uint8),
                reward=float(data["reward"]),
                action=-1 if data["action"] is None else int(data["action"]),
                done=bool(data["done"]),
                episode_id=str(data["episode_id"]),
                request_id=int(data["request_id"]),
                ready=bool(data["ready"]),
            )
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
