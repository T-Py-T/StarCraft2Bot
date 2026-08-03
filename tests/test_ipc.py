from pathlib import Path

import numpy as np
import pytest

from src.ipc import add_reward, empty_observation, load_state, save_state


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
        },
        state_path,
    )
    add_reward(2.5, state_path)

    state = load_state(state_path)
    np.testing.assert_array_equal(state["state"], observation)
    assert state["reward"] == pytest.approx(3.75)
    assert state["action"] is None
    assert state["done"] is False
    assert not state_path.with_suffix(".npz.tmp").exists()


def test_state_round_trip_preserves_action_and_done(tmp_path: Path) -> None:
    state_path = tmp_path / "state.npz"
    save_state(
        {
            "state": empty_observation(),
            "reward": -1,
            "action": 4,
            "done": True,
        },
        state_path,
    )

    state = load_state(state_path)
    assert state["action"] == 4
    assert state["done"] is True


def test_state_loader_rejects_object_payloads(tmp_path: Path) -> None:
    state_path = tmp_path / "unsafe.npz"
    with state_path.open("wb") as state_file:
        np.savez(
            state_file,
            state=np.array([object()], dtype=object),
            reward=0,
            action=-1,
            done=False,
        )

    with pytest.raises(ValueError, match="Object arrays cannot be loaded"):
        load_state(state_path)
