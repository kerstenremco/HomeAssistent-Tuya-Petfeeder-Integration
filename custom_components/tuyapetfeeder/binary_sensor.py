from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    async_add_entities([FeederOnlineBinarySensor(coordinator, data["feeder"])])


class FeederOnlineBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, feeder):
        super().__init__(coordinator)
        self._feeder = feeder
        self._attr_name = "Pet Feeder Online"
        self._attr_unique_id = f"pet_feeder_online_{self._feeder.device.id}"
        self._attr_device_class = "connectivity"

    @property
    def is_on(self):
        return self.coordinator.data.get("online", False)

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._feeder.device.id)},
            name=self._feeder.name,
            manufacturer="Tuya",
            model="Pet Feeder",
        )
