"""The PiKVM integration."""
import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, CONF_URL, CONF_USERNAME, CONF_PASSWORD, CONF_CERTIFICATE
from .coordinator import PiKVMDataUpdateCoordinator

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the PiKVM component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PiKVM from a config entry.

    This function is responsible for setting up the PiKVM integration in Home Assistant
    based on the provided config entry.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        entry (ConfigEntry): The config entry for the PiKVM integration.

    Returns:
        bool: True if the setup was successful, False otherwise.
    """
    hass.data.setdefault(DOMAIN, {})
    
    coordinator = PiKVMDataUpdateCoordinator(
        hass,
        entry.data[CONF_URL],
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        entry.data[CONF_CERTIFICATE]  # Pass the serialized certificate
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry.

    This function is responsible for unloading a configuration entry in Home Assistant.
    It forwards the entry unload signal to the 'sensor' component and removes the entry from the 'pikvm_ha' domain data.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        entry (ConfigEntry): The configuration entry to unload.

    Returns:
        bool: True if the entry was successfully unloaded, False otherwise.
    """
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)

    return True
