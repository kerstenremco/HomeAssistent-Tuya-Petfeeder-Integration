import logging
from homeassistant.core import HomeAssistant, ServiceCall
from .feeder import feed_portion, turn_on_light, turn_off_light

DOMAIN = "petfeeder"
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up petfeeder integration."""

    async def handle_feed(call: ServiceCall):
        _LOGGER.info("Feeding")
        portions = call.data.get("portions")
        feed_portion(portions)

    async def handle_toggle_light(call: ServiceCall):
        state = call.data.get("state")
        if state == "on":
            _LOGGER.info("Turning light on")
            turn_on_light()
        else:
            _LOGGER.info("Turning light off")
            turn_off_light()

    hass.services.async_register(DOMAIN, "feed", handle_feed)
    hass.services.async_register(DOMAIN, "toggle_light", handle_toggle_light)

    return True
