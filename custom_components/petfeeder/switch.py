from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN
from .feeder import Feeder


async def async_setup_entry(hass, entry, async_add_entities):
    feeder = hass.data[DOMAIN][entry.entry_id]["feeder"]
    async_add_entities([PetFeederLed(feeder)], True)


class PetFeederLed(SwitchEntity):
    def __init__(self, feeder: Feeder):
        self._feeder = feeder
        self._is_on = False
        self._attr_name = "Pet Feeder LED"
        self._attr_unique_id = f"pet_feeder_led_{self._feeder.device.id}"

    @property
    def name(self):
        return self._attr_name

    @property
    def is_on(self):
        return self._is_on

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._feeder.device.id)},
            name=self._feeder.name,
            manufacturer="Tuya",
            model="Pet Feeder",
        )

    async def async_turn_on(self, **kwargs):
        success = await self._feeder.turn_on_light()
        if success:
            self._is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        success = await self._feeder.turn_off_light()
        if success:
            self._is_on = False
            self.async_write_ha_state()
