"""The Ghost integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL, Platform
from homeassistant.core import HomeAssistant

from .api import GhostAdminAPI
from .const import CONF_ADMIN_API_KEY, DOMAIN
from .coordinator import GhostDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Ghost from a config entry."""
    site_url = entry.data[CONF_URL]
    admin_api_key = entry.data[CONF_ADMIN_API_KEY]

    api = GhostAdminAPI(site_url, admin_api_key)
    
    # Get site info for the coordinator name
    try:
        site = await api.get_site()
        site_title = site.get("title", "Ghost")
    except Exception as err:
        _LOGGER.error("Failed to connect to Ghost: %s", err)
        await api.close()
        return False

    coordinator = GhostDataUpdateCoordinator(hass, api, site_title)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator: GhostDataUpdateCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.api.close()

    return unload_ok
