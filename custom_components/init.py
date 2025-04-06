"""Sony STR-DN840 integration for Home Assistant."""
import logging
from . import integration

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up the integration."""
    conf = config.get('sony_str_dn840')
    if conf is None:
        _LOGGER.error("No configuration found for sony_str_dn840")
        return False

    hass.data.setdefault('sony_str_dn840', {})
    integration.setup(hass, conf)
    return True
