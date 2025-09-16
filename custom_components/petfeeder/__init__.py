from .const import PLATFORMS, DOMAIN
import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import logging
import voluptuous as vol
from .feeder import Feeder
from .coordinator import FeederCoordinator

logger = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from a config entry."""
    name = entry.data.get("name")
    host = entry.data.get("host")
    device_id = entry.data.get("device_id")
    local_key = entry.data.get("local_key")
    api_key = entry.data.get("api_key")
    api_secret = entry.data.get("api_secret")
    region = entry.data.get("region")
    feeder = Feeder(
        name=name,
        device_id=device_id,
        local_key=local_key,
        host=host,
        api_key=api_key,
        api_secret=api_secret,
        region=region,
    )
    coordinator = FeederCoordinator(hass, feeder)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "feeder": feeder,
        "coordinator": coordinator
    }

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )

    async def dispense_service(call):
        amount = call.data.get("amount", 1)
        await feeder.feed_portion(amount)
        coordinator.increment_dispense_counter(amount)

    dispense_schema = vol.Schema({
        vol.Optional("amount", default=1): int
    })

    hass.services.async_register(
        DOMAIN, "dispense", dispense_service, schema=dispense_schema)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(entry, platform)
            for platform in PLATFORMS
        ]
    )
    if all(unload_ok):
        hass.data[DOMAIN].pop(entry.entry_id)
    return all(unload_ok)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
