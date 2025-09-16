from datetime import timedelta
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .feeder import Feeder
from homeassistant.helpers.storage import Store

_LOGGER = logging.getLogger(__name__)


class FeederCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, feeder: Feeder):
        super().__init__(
            hass,
            _LOGGER,
            name="Pet Feeder Coordinator",
            update_interval=timedelta(seconds=30),  # poll every 30s
        )
        self.feeder = feeder
        self._dispense_counter = 0
        self._store = Store(hass, 1, f"petfeeder_{feeder.device_id}_data")

    async def async_load_data(self):
        data = await self._store.async_load()
        if data is not None:
            self._dispense_counter = data.get("dispense_count", 0)

    async def _async_update_data(self):
        """Fetch data from feeder asynchronously."""
        try:
            await self.feeder.async_check_local_connection()
            led_status = await self.feeder.async_get_led_status()
            return {"online": True, "led_status": led_status, "dispense_count": self._dispense_counter}
        except Exception as err:
            return {"online": False, **self.data}

    async def increment_dispense_counter(self, amount: int):
        self._dispense_counter += amount
        await self._store.async_save({
            "dispense_count": self._dispense_counter
        })
        self.async_set_updated_data({
            **self.data,
            "dispense_count": self._dispense_counter
        })
