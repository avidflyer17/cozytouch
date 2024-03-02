"""Switches for Atlantic Cozytouch integration."""
from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .hub import Hub
from .sensor import CozytouchSensor

_LOGGER = logging.getLogger(__name__)


# config flow setup
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entry."""
    # Retrieve the hub object
    try:
        hub = hass.data[DOMAIN][config_entry.entry_id]
    except KeyError:
        _LOGGER.error(
            "%s: can not init selects: failed to get the hub object",
            config_entry.title,
        )
        return

    # Init selects
    selects = []
    capabilities = hub.get_capabilities_for_device(config_entry.data["deviceId"])
    for capability in capabilities:
        if capability["type"] == "select":
            selects.append(
                CozytouchSelect(
                    capability=capability,
                    config_title=config_entry.title,
                    config_uniq_id=config_entry.entry_id,
                    hub=hub,
                )
            )

    # Add the entities to HA
    if len(selects) > 0:
        async_add_entities(selects, True)


class CozytouchSelect(SelectEntity, CozytouchSensor):
    """Class for select entity."""

    def __init__(
        self,
        capability,
        config_title: str,
        config_uniq_id: str,
        hub: Hub,
        name: str | None = None,
        icon: str | None = None,
    ) -> None:
        """Initialize a Select entity."""
        super().__init__(
            capability=capability,
            config_title=config_title,
            config_uniq_id=config_uniq_id,
            hub=hub,
            name=name,
            icon=icon,
        )
        modelInfos = self._hub.get_model_infos(capability["deviceId"])
        if "modelList" in capability and capability["modelList"] in modelInfos:
            self._list = modelInfos.get(capability["modelList"], None)
        else:
            self._list = {-1: "Undefined"}

        self.options = list(self._list.values())
        self.current_option = self.options[0]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        for value in self._list:
            if self._list[value] == option:
                await self._set_capability_value(
                    self._capability["capabilityId"],
                    str(value),
                )
                break

    def get_value(self) -> str:
        """Retrieve value from hub."""
        value = int(self._get_capability_value(self._capability["capabilityId"]))
        if value in self._list:
            self.current_option = self._list[value]
