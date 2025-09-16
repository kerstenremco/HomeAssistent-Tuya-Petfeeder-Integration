from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
from .feeder import Feeder
import logging


logger = logging.getLogger(__name__)


class PetFeederConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pet Feeder."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            name = user_input.get("name")
            host = user_input.get("host")
            device_id = user_input.get("device_id")
            local_key = user_input.get("local_key")
            api_key = None
            api_secret = None
            region = None
            # api_key = user_input.get("api_key")
            # api_secret = user_input.get("api_secret")
            # region = user_input.get("region")
            feeder = Feeder(
                name=name,
                device_id=device_id,
                local_key=local_key,
                host=host,
                api_key=api_key,
                api_secret=api_secret,
                region=region,
            )
            try:
                await feeder.async_check_local_connection()
                return self.async_create_entry(title=name, data=user_input)
            except Exception as e:
                logger.error(f"Connection error: {e}")
                errors["base"] = "Cannot connect to the device"

        data_schema = vol.Schema(
            {
                vol.Required("name", default="Pet Feeder"): str,
                vol.Optional("host", default="192.168.2.10"): str,
                vol.Required("device_id"): str,
                vol.Required("local_key"): str,
                # vol.Optional("api_key"): str,
                # vol.Optional("api_secret"): str,
                # vol.Optional("region", default="eu"): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
