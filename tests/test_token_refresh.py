import os
import sys
import pytest
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

ha_core = types.ModuleType("homeassistant.core")
ha_core.HomeAssistant = type("HomeAssistant", (), {})

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

from importlib.machinery import SourceFileLoader
from importlib import util

hub_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "custom_components", "cozytouch", "hub.py"
    )
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


class DummyConfig:
    config_dir = "/tmp"


class DummyHass:
    config = DummyConfig()


class MockResponse:
    def __init__(self, status, data):
        self.status = status
        self._data = data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def json(self):
        return self._data


@pytest.mark.asyncio
async def test_refresh_on_401(monkeypatch):
    hass = DummyHass()
    hub = Hub(hass, "u", "p", deviceId=1)
    hub.online = True
    hub._access_token = "tok"
    hub._devices = [
        {
            "deviceId": 1,
            "name": "dev",
            "modelId": 0,
            "gatewaySerialNumber": "sn",
            "productId": 0,
            "zoneId": 0,
            "modelInfos": {},
            "capabilities": [],
        }
    ]

    calls = []

    async def mock_connect():
        calls.append(True)
        hub.online = True

    monkeypatch.setattr(hub, "connect", mock_connect)

    responses = [MockResponse(401, {}), MockResponse(200, [])]

    def mock_get(*args, **kwargs):
        return responses.pop(0)

    hub._session.get = mock_get

    await hub._async_update_data()
    await hub.close()
    assert calls


@pytest.mark.asyncio
async def test_refresh_on_invalid_grant(monkeypatch):
    hass = DummyHass()
    hub = Hub(hass, "u", "p", deviceId=1)
    hub.online = True
    hub._access_token = "tok"
    hub._devices = [
        {
            "deviceId": 1,
            "name": "dev",
            "modelId": 0,
            "gatewaySerialNumber": "sn",
            "productId": 0,
            "zoneId": 0,
            "modelInfos": {},
            "capabilities": [],
        }
    ]

    calls = []

    async def mock_connect():
        calls.append(True)
        hub.online = True

    monkeypatch.setattr(hub, "connect", mock_connect)

    responses = [MockResponse(200, {"error": "invalid_grant"}), MockResponse(200, [])]

    def mock_get(*args, **kwargs):
        return responses.pop(0)

    hub._session.get = mock_get

    await hub._async_update_data()
    await hub.close()
    assert calls
