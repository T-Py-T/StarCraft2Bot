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
