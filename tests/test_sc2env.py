from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import numpy as np

from src import sc2env


def _state(
    *,
    action: int | None,
    episode_id: str = "episode-1",
    request_id: int = 0,
    ready: bool = True,
    reward: float = 0,
    done: bool = False,
) -> dict[str, Any]:
    return {
        "state": sc2env.empty_observation(),
        "reward": reward,
        "action": action,
        "done": done,
        "episode_id": episode_id,
        "request_id": request_id,
        "ready": ready,
    }


class _FakeProcess:
    def __init__(self) -> None:
        self.terminated = False
        self.killed = False
        self.wait_calls = 0

    def poll(self) -> int | None:
        return 0 if self.terminated or self.killed else None

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.killed = True

    def wait(self, timeout: int) -> int:
        self.wait_calls += 1
        return 0


def _active_environment(process: _FakeProcess) -> sc2env.Sc2Env:
    environment = sc2env.Sc2Env()
    environment._bot_process = process
    environment._episode_id = "episode-1"
    return environment


def test_step_waits_for_ready_correlated_response(monkeypatch) -> None:
    responses: Iterator[dict[str, Any]] = iter(
        [
            _state(action=None, ready=False),
            _state(action=None),
            _state(action=None, episode_id="stale", request_id=1),
            _state(action=None, request_id=0),
            _state(action=4, request_id=1),
            _state(action=None, request_id=1, reward=2.5, done=True),
        ]
    )
    writes: list[tuple[dict[str, Any], object]] = []
    monkeypatch.setattr(sc2env, "load_state", lambda _path: next(responses))
    monkeypatch.setattr(
        sc2env, "save_state", lambda state, path: writes.append((state.copy(), path))
    )
    monkeypatch.setattr(sc2env.time, "sleep", lambda _delay: None)

    environment = _active_environment(_FakeProcess())
    observation, reward, terminated, truncated, info = environment.step(4)

    assert writes[0][0]["action"] == 4
    assert writes[0][0]["episode_id"] == "episode-1"
    assert writes[0][0]["request_id"] == 1
    assert writes[0][1] == sc2env.REQUEST_PATH
    assert observation.shape == (224, 224, 3)
    assert reward == 2.5
    assert terminated is True
    assert truncated is False
    assert info == {}


def test_step_timeout_invalidates_episode_and_stops_child(monkeypatch) -> None:
    responses: Iterator[dict[str, Any]] = iter(
        [
            _state(action=None),
            _state(action=2, request_id=1),
        ]
    )
    writes: list[tuple[dict[str, Any], object]] = []
    monkeypatch.setattr(sc2env, "RESPONSE_TIMEOUT_SECONDS", 0)
    monkeypatch.setattr(sc2env, "load_state", lambda _path: next(responses))
    monkeypatch.setattr(
        sc2env, "save_state", lambda state, path: writes.append((state.copy(), path))
    )

    process = _FakeProcess()
    environment = _active_environment(process)
    observation, reward, terminated, truncated, info = environment.step(2)

    np.testing.assert_array_equal(observation, sc2env.empty_observation())
    assert (reward, terminated, truncated, info) == (0.0, True, False, {})
    assert writes[0][0]["episode_id"] == "episode-1"
    assert writes[0][0]["request_id"] == 1
    assert writes[1][0]["episode_id"] != "episode-1"
    assert writes[1][0]["ready"] is False
    assert all(path == sc2env.REQUEST_PATH for _, path in writes)
    assert environment._episode_id is None
    assert process.terminated is True
    assert process.wait_calls == 1


def test_reset_restarts_child_for_each_episode(monkeypatch) -> None:
    processes = [_FakeProcess(), _FakeProcess()]
    starts: list[tuple[list[str], dict[str, str]]] = []
    writes: list[tuple[dict[str, Any], object]] = []
    monkeypatch.setattr(
        sc2env, "save_state", lambda state, path: writes.append((state.copy(), path))
    )

    def fake_popen(command, env):
        starts.append((command, env))
        return processes[len(starts) - 1]

    monkeypatch.setattr(sc2env.subprocess, "Popen", fake_popen)

    environment = sc2env.Sc2Env()
    first_observation, _ = environment.reset()
    second_observation, _ = environment.reset()
    environment.close()

    assert len(starts) == 2
    assert first_observation.shape == second_observation.shape == (224, 224, 3)
    assert writes[0][0]["episode_id"] != writes[1][0]["episode_id"]
    assert starts[0][1]["SC2_EPISODE_ID"] == writes[0][0]["episode_id"]
    assert starts[1][1]["SC2_EPISODE_ID"] == writes[1][0]["episode_id"]
    assert all(path == sc2env.REQUEST_PATH for _, path in writes)
    assert processes[0].terminated is True
    assert processes[0].wait_calls == 1
    assert processes[1].terminated is True
    assert processes[1].wait_calls == 1


def test_step_reads_final_response_after_child_exit(monkeypatch) -> None:
    responses: Iterator[dict[str, Any]] = iter(
        [
            _state(action=None),
            _state(action=4, request_id=1),
            _state(action=None, request_id=1, reward=9, done=True),
        ]
    )
    writes: list[tuple[dict[str, Any], object]] = []
    monkeypatch.setattr(sc2env, "load_state", lambda _path: next(responses))
    monkeypatch.setattr(
        sc2env, "save_state", lambda state, path: writes.append((state.copy(), path))
    )
    process = _FakeProcess()
    process.terminated = True
    environment = _active_environment(process)

    _, reward, terminated, truncated, info = environment.step(4)

    assert writes[0][1] == sc2env.REQUEST_PATH
    assert reward == 9
    assert terminated is True
    assert truncated is False
    assert info == {}


def test_step_prefers_terminal_response_over_new_request(monkeypatch) -> None:
    responses: Iterator[dict[str, Any]] = iter(
        [
            _state(action=None),
            _state(action=None, request_id=0, reward=1000, done=True),
        ]
    )
    writes: list[tuple[dict[str, Any], object]] = []
    monkeypatch.setattr(sc2env, "load_state", lambda _path: next(responses))
    monkeypatch.setattr(
        sc2env, "save_state", lambda state, path: writes.append((state.copy(), path))
    )
    environment = _active_environment(_FakeProcess())

    _, reward, terminated, truncated, info = environment.step(4)

    assert writes[0][0]["request_id"] == 1
    assert reward == 1000
    assert terminated is True
    assert truncated is False
    assert info == {}
