"""Config flow for Centurion Garage Door custom integration."""

import voluptuous as vol
from homeassistant import config_entries
from .const import (
    DOMAIN,
    CONF_IP_ADDRESS,
    CONF_API_KEY,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)


class CenturionGarageDoorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for the Centurion Garage Door controller."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> object:
        """
        Handle the initial step of the config flow.

        Args:
            user_input: Optional dictionary with user input from the form.

        Returns:
            ConfigFlowResult: The result of the config flow step.

        """
        if user_input is not None:
            scan_interval = user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            try:
                scan_interval = int(scan_interval)
            except (TypeError, ValueError):
                scan_interval = DEFAULT_SCAN_INTERVAL
            user_input[CONF_SCAN_INTERVAL] = scan_interval
            return self.async_create_entry(title="Centurion Garage", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP_ADDRESS): str,
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=DEFAULT_SCAN_INTERVAL,
                    ): int,
                }
            ),
        )

    async def async_step_options(self, user_input: dict | None = None) -> object:
        """Handle the options flow for scan_interval."""
        if user_input is not None:
            scan_interval = user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            try:
                scan_interval = int(scan_interval)
            except (TypeError, ValueError):
                scan_interval = DEFAULT_SCAN_INTERVAL
            return self.async_create_entry(
                title="Options",
                data={CONF_SCAN_INTERVAL: scan_interval},
            )

        return self.async_show_form(
            step_id="options",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=DEFAULT_SCAN_INTERVAL,
                    ): int,
                }
            ),
        )
