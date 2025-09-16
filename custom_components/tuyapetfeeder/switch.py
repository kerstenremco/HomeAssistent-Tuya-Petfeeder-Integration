from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    feeder = hass.data[DOMAIN][entry.entry_id]["feeder"]
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([PetFeederLed(coordinator, feeder)], True)


class PetFeederLed(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, feeder):
        super().__init__(coordinator)
        self._feeder = feeder
        self._attr_name = "Pet Feeder LED"
        self._attr_unique_id = f"pet_feeder_led_{self._feeder.device.id}"

    @property
    def name(self):
        return self._attr_name

    @property
    def is_on(self):
        return self.coordinator.data.get("led_status", False)

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._feeder.device.id)},
            name=self._feeder.name,
            manufacturer="Tuya",
            model="Pet Feeder",
        )

    async def async_turn_on(self, **kwargs):
        await self._feeder.async_toggle_light(True)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):
        await self._feeder.async_toggle_light(False)
        await self.coordinator.async_refresh()
