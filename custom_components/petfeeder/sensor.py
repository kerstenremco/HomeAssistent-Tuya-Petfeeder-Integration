from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from homeassistant.helpers.entity import DeviceInfo


async def async_setup_entry(hass, entry, async_add_entities):
    feeder = hass.data[DOMAIN][entry.entry_id]["feeder"]
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([PortionsDispensedSensor(coordinator, feeder)], True)


class PortionsDispensedSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, feeder):
        super().__init__(coordinator)
        self._feeder = feeder
        self._attr_name = "Pet Feeder Portions Dispensed"
        self._attr_unique_id = f"pet_feeder_portions_dispensed_{self._feeder.device.id}"
        self._attr_native_unit_of_measurement = "portions"

    @property
    def native_value(self):
        return self.coordinator.data.get("dispense_count", 0)

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._feeder.device.id)},
            name=self._feeder.name,
            manufacturer="Tuya",
            model="Pet Feeder",
        )
