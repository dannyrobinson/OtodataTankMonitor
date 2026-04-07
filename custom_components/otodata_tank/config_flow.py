"""Config flow for Otodata Tank Monitor."""

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_BASE_URL, CONF_DEVICE_CODE, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN


class OtodataTankConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Otodata Tank Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            device_code = user_input[CONF_DEVICE_CODE].strip()
            session = async_get_clientsession(self.hass)

            try:
                url = f"{API_BASE_URL}/{device_code}"
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 404:
                        errors["base"] = "device_not_found"
                    else:
                        resp.raise_for_status()
                        data = await resp.json()
                        serial = str(data["serialNumber"])

                        await self.async_set_unique_id(serial)
                        self._abort_if_unique_id_configured()

                        return self.async_create_entry(
                            title=f"Propane Tank ({serial})",
                            data={
                                CONF_DEVICE_CODE: device_code,
                                CONF_SCAN_INTERVAL: user_input.get(
                                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                                ),
                            },
                        )
            except (aiohttp.ClientError, TimeoutError):
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_CODE): str,
                    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
                }
            ),
            errors=errors,
        )
