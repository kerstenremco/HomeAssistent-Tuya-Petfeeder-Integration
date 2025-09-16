from datetime import timedelta
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .feeder import Feeder

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

    async def _async_update_data(self):
        """Fetch data from feeder asynchronously."""
        try:
            await self.feeder.async_check_local_connection()
            led_status = await self.feeder.async_get_led_status()
            return {"online": True, "led_status": led_status, "dispense_count": self._dispense_counter}
        except Exception as err:
            return {"online": False, **self.data}

    def increment_dispense_counter(self, amount: int):
        self._dispense_counter += amount
        self.async_set_updated_data({
            **self.data,
            "dispense_count": self._dispense_counter
        })
