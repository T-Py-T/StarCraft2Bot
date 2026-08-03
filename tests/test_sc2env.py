from collections.abc import Iterator
from typing import Any

import numpy as np

from src import sc2env


def _state(
    *, action: int | None, reward: float = 0, done: bool = False
) -> dict[str, Any]:
    return {
        "state": sc2env.empty_observation(),
        "reward": reward,
        "action": action,
        "done": done,
    }


def test_step_publishes_action_then_waits_for_consumed_response(monkeypatch) -> None:
    responses: Iterator[dict[str, Any]] = iter(
        [
            _state(action=None),
            _state(action=4),
            _state(action=None, reward=2.5, done=True),
        ]
    )
    writes: list[dict[str, Any]] = []
    monkeypatch.setattr(sc2env, "load_state", lambda: next(responses))
    monkeypatch.setattr(sc2env, "save_state", lambda state: writes.append(state.copy()))
    monkeypatch.setattr(sc2env.time, "sleep", lambda _delay: None)

    environment = sc2env.Sc2Env()
    observation, reward, terminated, truncated, info = environment.step(4)

    assert writes[0]["action"] == 4
    assert observation.shape == (224, 224, 3)
    assert reward == 2.5
    assert terminated is True
    assert truncated is False
    assert info == {}


def test_step_returns_failure_after_retry_limit(monkeypatch) -> None:
    monkeypatch.setattr(sc2env, "MAX_ATTEMPTS", 2)
    monkeypatch.setattr(sc2env, "load_state", lambda: _state(action=1))
    monkeypatch.setattr(sc2env.time, "sleep", lambda _delay: None)

    observation, reward, terminated, truncated, info = sc2env.Sc2Env().step(2)

    np.testing.assert_array_equal(observation, sc2env.empty_observation())
    assert (reward, terminated, truncated, info) == (0.0, True, False, {})


class _FakeProcess:
    def __init__(self) -> None:
        self.terminated = False
        self.wait_calls = 0

    def poll(self) -> None:
        return None

    def terminate(self) -> None:
        self.terminated = True

    def wait(self, timeout: int) -> int:
        self.wait_calls += 1
        return 0


def test_reset_reuses_live_process_and_close_terminates_it(monkeypatch) -> None:
    process = _FakeProcess()
    starts: list[list[str]] = []
    monkeypatch.setattr(sc2env, "save_state", lambda _state: None)

    def fake_popen(command, env):
        starts.append(command)
        return process

    monkeypatch.setattr(sc2env.subprocess, "Popen", fake_popen)

    environment = sc2env.Sc2Env()
    first_observation, _ = environment.reset()
    second_observation, _ = environment.reset()
    environment.close()

    assert len(starts) == 1
    assert first_observation.shape == second_observation.shape == (224, 224, 3)
    assert process.terminated is True
    assert process.wait_calls == 1
