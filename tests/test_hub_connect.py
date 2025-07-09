import os
import sys
import pytest
from aiohttp import ContentTypeError
from homeassistant.core import HomeAssistant

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from custom_components.cozytouch.hub import Hub, CannotConnect

class FakeResponse:
    def __init__(self, status=200, json_data=None, exc=None):
        self.status = status
        self._json_data = json_data
        self._exc = exc
    async def json(self):
        if self._exc:
            raise self._exc
        return self._json_data
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, tb):
        return False

@pytest.mark.asyncio
async def test_connect_token_status_error(monkeypatch):
    hass = HomeAssistant('.')
    hub = Hub(hass, 'user', 'pass')

    def fake_post(*args, **kwargs):
        return FakeResponse(status=401, json_data={'error': 'invalid_grant'})

    monkeypatch.setattr(hub._session, 'post', fake_post)

    result = await hub.connect()
    assert result is False
    await hub._session.close()

@pytest.mark.asyncio
async def test_connect_token_invalid_json(monkeypatch):
    hass = HomeAssistant('.')
    hub = Hub(hass, 'user', 'pass')

    def fake_post(*args, **kwargs):
        req = type("req", (), {"real_url": "http://test"})
        return FakeResponse(status=200, exc=ContentTypeError(req, ()))

    monkeypatch.setattr(hub._session, 'post', fake_post)

    result = await hub.connect()
    assert result is False
    await hub._session.close()

@pytest.mark.asyncio
async def test_connect_setup_invalid_json(monkeypatch):
    hass = HomeAssistant('.')
    hub = Hub(hass, 'user', 'pass')

    def fake_post(*args, **kwargs):
        return FakeResponse(status=200, json_data={
            'access_token': '123',
            'token_type': 'Bearer'
        })

    def fake_get(*args, **kwargs):
        req = type("req", (), {"real_url": "http://test"})
        return FakeResponse(status=200, exc=ContentTypeError(req, ()))

    monkeypatch.setattr(hub._session, 'post', fake_post)
    monkeypatch.setattr(hub._session, 'get', fake_get)

    result = await hub.connect()
    assert result is False
    await hub._session.close()
