from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
from .feeder import Feeder


class PetFeederConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pet Feeder."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            name = user_input["name"]
            host = user_input["host"]
            device_id = user_input["device_id"]
            local_key = user_input["local_key"]
            feeder = Feeder(name, host, device_id, local_key)
            connected = await feeder.check_connection()
            if not connected:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=f"Pet Feeder", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required("name"): str,
                vol.Required("host"): str,
                vol.Required("device_id"): str,
                vol.Required("local_key"): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
