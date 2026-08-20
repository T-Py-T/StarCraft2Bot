from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest


def _load_incredibot(monkeypatch) -> ModuleType:
    source_dir = Path(__file__).parents[1] / "src"
    monkeypatch.syspath_prepend(str(source_dir))
    spec = importlib.util.spec_from_file_location(
        "incredibot_sct", source_dir / "incredibot-sct.py"
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _request(request_id: int, action: int = 4) -> dict[str, Any]:
    return {
        "episode_id": "episode-1",
        "request_id": request_id,
        "action": action,
        "ready": True,
    }


def test_on_start_async_publishes_correlated_ready_response(monkeypatch) -> None:
    module = _load_incredibot(monkeypatch)
    request = _request(7)
    writes: list[tuple[dict[str, Any], Path]] = []
    monkeypatch.setattr(module, "load_state", lambda _path: request.copy())
    monkeypatch.setattr(
        module,
        "save_state",
        lambda data, path: writes.append((data, path)),
    )
    bot = module.IncrediBot()
    bot._episode_id = "episode-1"
    bot.prev_stargate_count = 3
    bot.episode_reward = 250

    asyncio.run(bot.on_start_async())

    assert bot._request_id == 7
    assert bot.prev_stargate_count == 0
    assert bot.episode_reward == 0
    assert len(writes) == 1
    response, path = writes[0]
    assert path == module.RESPONSE_PATH
    assert response["episode_id"] == "episode-1"
    assert response["request_id"] == 7
    assert response["state"].shape == (224, 224, 3)
    assert response["reward"] == 0
    assert response["action"] is None
    assert response["done"] is False
    assert response["ready"] is True


def test_on_start_async_rejects_request_from_another_episode(monkeypatch) -> None:
    module = _load_incredibot(monkeypatch)
    request = _request(1)
    request["episode_id"] = "another-episode"
    writes: list[dict[str, Any]] = []
    monkeypatch.setattr(module, "load_state", lambda _path: request)
    monkeypatch.setattr(module, "save_state", lambda data, _path: writes.append(data))
    bot = module.IncrediBot()
    bot._episode_id = "episode-1"

    with pytest.raises(RuntimeError, match="no longer owns"):
        asyncio.run(bot.on_start_async())

    assert writes == []


def test_wait_for_action_ignores_consumed_request(monkeypatch) -> None:
    module = _load_incredibot(monkeypatch)
    requests = iter([_request(3), _request(4, action=5)])
    monkeypatch.setattr(module, "load_state", lambda _path: next(requests))
    bot = module.IncrediBot()
    bot._episode_id = "episode-1"
    bot._request_id = 3

    action, request_id = asyncio.run(bot._wait_for_action())

    assert (action, request_id) == (5, 4)


def test_wait_for_action_rejects_forward_gap(monkeypatch) -> None:
    module = _load_incredibot(monkeypatch)
    monkeypatch.setattr(module, "load_state", lambda _path: _request(5))
    bot = module.IncrediBot()
    bot._episode_id = "episode-1"
    bot._request_id = 3

    with pytest.raises(RuntimeError, match="out-of-order"):
        asyncio.run(bot._wait_for_action())
