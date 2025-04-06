"""Sony STR-DN840 integration for Home Assistant."""
import logging
from . import integration

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up the integration."""
    if "sony_str_dn840" not in config:
        _LOGGER.error("No configuration for sony_str_dn840 found")
        return False

    hass.data.setdefault("sony_str_dn840", {})
    return integration.setup(hass, config)
