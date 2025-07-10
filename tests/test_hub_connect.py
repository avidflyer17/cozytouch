import os
import sys
import pytest
from aiohttp import ContentTypeError
import types

ha_core = types.ModuleType("homeassistant.core")

class StubHomeAssistant:
    def __init__(self, *args, **kwargs):
        pass

ha_core.HomeAssistant = StubHomeAssistant

ha_helpers_dev_reg = types.ModuleType("homeassistant.helpers.device_registry")
ha_helpers_dev_reg.DeviceEntryType = type("DeviceEntryType", (), {"SERVICE": "service"})
ha_helpers_dev_reg.DeviceInfo = type("DeviceInfo", (), {})

ha_exceptions = types.ModuleType("homeassistant.exceptions")
ha_exceptions.HomeAssistantError = Exception

ha_config_entries = types.ModuleType("homeassistant.config_entries")
ha_config_entries.ConfigEntry = type("ConfigEntry", (), {})

ha_helpers_update = types.ModuleType("homeassistant.helpers.update_coordinator")


class DummyCoordinator:
    def __init__(self, *args, **kwargs):
        pass


ha_helpers_update.DataUpdateCoordinator = DummyCoordinator

ha_util_dt = types.ModuleType("homeassistant.util.dt")
from datetime import timezone

ha_util_dt.DEFAULT_TIME_ZONE = timezone.utc

sys.modules["homeassistant"] = types.ModuleType("homeassistant")
sys.modules["homeassistant.core"] = ha_core
sys.modules["homeassistant.helpers"] = types.ModuleType("homeassistant.helpers")
sys.modules["homeassistant.helpers.device_registry"] = ha_helpers_dev_reg
sys.modules["homeassistant.helpers.update_coordinator"] = ha_helpers_update
sys.modules["homeassistant.exceptions"] = ha_exceptions
sys.modules["homeassistant.config_entries"] = ha_config_entries
sys.modules["homeassistant.util"] = types.ModuleType("homeassistant.util")
sys.modules["homeassistant.util.dt"] = ha_util_dt

from homeassistant.core import HomeAssistant

from importlib.machinery import SourceFileLoader
from importlib import util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

hub_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "custom_components", "cozytouch", "hub.py")
)

sys.modules.setdefault("custom_components", types.ModuleType("custom_components"))

cozy_pkg = types.ModuleType("custom_components.cozytouch")
cozy_pkg.__path__ = [os.path.dirname(hub_path)]
sys.modules["custom_components.cozytouch"] = cozy_pkg
stub_cap = types.ModuleType("custom_components.cozytouch.capability")
stub_cap.get_capability_infos = lambda *a, **k: {}
sys.modules["custom_components.cozytouch.capability"] = stub_cap
stub_model = types.ModuleType("custom_components.cozytouch.model")
stub_model.get_model_infos = lambda *a, **k: {}
sys.modules["custom_components.cozytouch.model"] = stub_model

spec = util.spec_from_loader(
    "custom_components.cozytouch.hub",
    SourceFileLoader("custom_components.cozytouch.hub", hub_path),
    origin=hub_path,
)
hub_module = util.module_from_spec(spec)
sys.modules[spec.name] = hub_module
spec.loader.exec_module(hub_module)
Hub = hub_module.Hub
CannotConnect = hub_module.CannotConnect

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
