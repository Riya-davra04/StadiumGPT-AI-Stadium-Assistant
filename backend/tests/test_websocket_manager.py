
"""Tests for :class:`app.utils.websocket.ConnectionManager`."""

from typing import Any, Dict, List

import pytest

from app.utils.websocket import ConnectionManager


class _FakeWebSocket:
    """Minimal awaitable stub mimicking the WebSocket surface used by the manager."""

    def __init__(self, fail_on_send: bool = False) -> None:
        self.accepted = False
        self.closed = False
        self.sent: List[Dict[str, Any]] = []
        self.fail_on_send = fail_on_send

    async def accept(self) -> None:
        self.accepted = True

    async def send_json(self, message: Dict[str, Any]) -> None:
        if self.fail_on_send:
            raise RuntimeError("send failed")
        self.sent.append(message)

    async def close(self) -> None:
        self.closed = True


@pytest.mark.asyncio
async def test_connect_and_send_personal_message() -> None:
    manager = ConnectionManager()
    ws = _FakeWebSocket()

    await manager.connect(ws, "c1")
    await manager.send_personal_message({"hello": "world"}, "c1")

    assert ws.accepted is True
    assert ws.sent == [{"hello": "world"}]
    assert manager.get_connection_count() == 1
    assert manager.get_active_clients() == ["c1"]


@pytest.mark.asyncio
async def test_broadcast_removes_stale_connections() -> None:
    manager = ConnectionManager()
    good = _FakeWebSocket()
    bad = _FakeWebSocket(fail_on_send=True)

    await manager.connect(good, "good")
    await manager.connect(bad, "bad")
    await manager.broadcast({"type": "ping"})

    assert manager.get_connection_count() == 1
    assert "bad" not in manager.get_active_clients()
    assert good.sent[0]["type"] == "ping"
    assert "broadcast_time" in good.sent[0]


@pytest.mark.asyncio
async def test_disconnect_is_idempotent() -> None:
    manager = ConnectionManager()
    ws = _FakeWebSocket()
    await manager.connect(ws, "c1")

    manager.disconnect("c1")
    manager.disconnect("c1")  # should not raise

    assert manager.get_connection_count() == 0


@pytest.mark.asyncio
async def test_close_all_connections() -> None:
    manager = ConnectionManager()
    ws1, ws2 = _FakeWebSocket(), _FakeWebSocket()
    await manager.connect(ws1, "a")
    await manager.connect(ws2, "b")

    await manager.close_all_connections()

    assert ws1.closed and ws2.closed
    assert manager.get_connection_count() == 0