from pathlib import Path

import numpy as np
import pytest

from src import ipc
from src.ipc import empty_observation, load_state, save_state


def test_state_round_trip_and_reward_update(tmp_path: Path) -> None:
    state_path = tmp_path / "state.npz"
    observation = empty_observation()
    observation[1, 2] = [3, 4, 5]

    save_state(
        {
            "state": observation,
            "reward": 1.25,
            "action": None,
            "done": False,
            "episode_id": "episode-1",
            "request_id": 3,
            "ready": True,
        },
        state_path,
    )
    state = load_state(state_path)
    np.testing.assert_array_equal(state["state"], observation)
    assert state["reward"] == pytest.approx(1.25)
    assert state["action"] is None
    assert state["done"] is False
    assert state["episode_id"] == "episode-1"
    assert state["request_id"] == 3
    assert state["ready"] is True
    assert list(tmp_path.glob("*.tmp")) == []


def test_state_round_trip_preserves_action_and_done(tmp_path: Path) -> None:
    state_path = tmp_path / "state.npz"
    save_state(
        {
            "state": empty_observation(),
            "reward": -1,
            "action": 4,
            "done": True,
            "episode_id": "episode-2",
            "request_id": 7,
            "ready": False,
        },
        state_path,
    )

    state = load_state(state_path)
    assert state["action"] == 4
    assert state["done"] is True
    assert state["episode_id"] == "episode-2"
    assert state["request_id"] == 7
    assert state["ready"] is False


def test_state_loader_rejects_object_payloads(tmp_path: Path) -> None:
    state_path = tmp_path / "unsafe.npz"
    with state_path.open("wb") as state_file:
        np.savez(
            state_file,
            state=np.array([object()], dtype=object),
            reward=0,
            action=-1,
            done=False,
            episode_id="episode-unsafe",
            request_id=0,
            ready=False,
        )

    with pytest.raises(ValueError, match="Object arrays cannot be loaded"):
        load_state(state_path)


def test_state_publication_retries_windows_sharing_violation(
    monkeypatch, tmp_path: Path
) -> None:
    state_path = tmp_path / "state.npz"
    original_replace = Path.replace
    attempts = 0
    delays: list[float] = []

    def replace_after_sharing_violations(source: Path, destination: Path) -> Path:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise PermissionError("destination is open")
        return original_replace(source, destination)

    monkeypatch.setattr(Path, "replace", replace_after_sharing_violations)
    monkeypatch.setattr(ipc.time, "sleep", delays.append)

    save_state(
        {
            "state": empty_observation(),
            "reward": 4,
            "action": None,
            "done": False,
            "episode_id": "episode-retry",
            "request_id": 8,
            "ready": True,
        },
        state_path,
    )

    assert attempts == 3
    assert delays == [
        ipc.REPLACE_RETRY_DELAY_SECONDS,
        ipc.REPLACE_RETRY_DELAY_SECONDS * 2,
    ]
    assert load_state(state_path)["request_id"] == 8
