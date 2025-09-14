from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN
from .feeder import Feeder


async def async_setup_entry(hass, entry, async_add_entities):
    feeder = hass.data[DOMAIN][entry.entry_id]["feeder"]
    async_add_entities([PetFeederDispenseButton(feeder)], True)


class PetFeederDispenseButton(ButtonEntity):
    def __init__(self, feeder: Feeder):
        self._feeder = feeder
        self._attr_name = "Pet Feeder Dispense"
        self._attr_unique_id = f"pet_feeder_dispense_{self._feeder.device.id}"

    @property
    def name(self):
        return self._attr_name

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._feeder.device.id)},
            name=self._feeder.name,
            manufacturer="Tuya",
            model="Pet Feeder",
        )

    async def async_press(self):
        await self._feeder.feed_portion(1)
