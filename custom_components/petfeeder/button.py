from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .feeder import Feeder


async def async_setup_entry(hass, entry, async_add_entities):
    feeder = hass.data[DOMAIN][entry.entry_id]["feeder"]
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([PetFeederDispenseButton(coordinator, feeder)], True)


class PetFeederDispenseButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, feeder: Feeder):
        super().__init__(coordinator)
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
        await self._feeder.async_feed_portion(1)
        await self.coordinator.increment_dispense_counter(1)
