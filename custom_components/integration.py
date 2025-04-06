"""Main integration module for Sony STR-DN840."""
import logging
from .controller import SonySTRDN840Controller

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up the integration based on configuration."""
    host = config.get('host')
    port = config.get('port', 80)
    if not host:
        _LOGGER.error("Host not specified in configuration")
        return

    controller = SonySTRDN840Controller(host, port)
    hass.data['sony_str_dn840']['controller'] = controller
    _LOGGER.info("Sony STR-DN840 integration setup complete")
