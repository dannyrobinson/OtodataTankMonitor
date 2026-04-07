"""The Otodata Tank Monitor integration."""

from datetime import timedelta
import logging

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, CONF_DEVICE_CODE, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Otodata Tank Monitor from a config entry."""
    device_code = entry.data[CONF_DEVICE_CODE]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    session = async_get_clientsession(hass)

    async def async_update_data() -> dict:
        """Fetch data from the Otodata API."""
        url = f"{API_BASE_URL}/{device_code}"
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                resp.raise_for_status()
                return await resp.json()
        except (aiohttp.ClientError, TimeoutError) as err:
            raise UpdateFailed(f"Error fetching data from Otodata: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=scan_interval),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
