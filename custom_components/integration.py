import logging
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from .controller import SonySTRDN840Controller

_LOGGER = logging.getLogger(__name__)
DOMAIN = "sony_str_dn840"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required("host"): cv.string,
        vol.Optional("port_status", default=80): cv.positive_int,
        vol.Optional("port_control", default=80): cv.positive_int,
        vol.Optional("myid", default="default_id"): cv.string,
        vol.Optional("mydevinfo", default="default_devinfo"): cv.string,
        vol.Optional("myuseragent", default="HomeAssistant"): cv.string,
        vol.Optional("myname", default="SonyReceiver"): cv.string,
        vol.Optional("max_vol", default=20): cv.positive_int,
        # Optionally provide alternative names mapping for inputs
        vol.Optional("alternative", default={}): dict
    })
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Set up the Sony STR-DN840 integration."""
    conf = config[DOMAIN]
    controller = SonySTRDN840Controller(
        host=conf["host"],
        port_status=conf.get("port_status", 80),
        port_control=conf.get("port_control", 80),
        myid=conf.get("myid", "default_id"),
        mydevinfo=conf.get("mydevinfo", "default_devinfo"),
        myuseragent=conf.get("myuseragent", "HomeAssistant"),
        myname=conf.get("myname", "SonyReceiver"),
        max_vol=conf.get("max_vol", 20),
        alternative=conf.get("alternative", {})
    )
    hass.data[DOMAIN] = controller

    def handle_register(call):
        result = controller.register()
        _LOGGER.info("Register result: %s", result)

    def handle_cmd(call):
        cmd = call.data.get("cmd")
        repeat = call.data.get("repeat", 1)
        result = controller.send_command(cmd, repeat)
        _LOGGER.info("Command result: %s", result)

    def handle_switch(call):
        target = call.data.get("target")
        result = controller.switch_input_to(target)
        _LOGGER.info("Switch input result: %s", result)

    def handle_set_volume(call):
        volume = call.data.get("volume")
        result = controller.set_volume_to(volume)
        _LOGGER.info("Set volume result: %s", result)

    def handle_power(call):
        action = call.data.get("action")
        result = controller.change_power_state(action)
        _LOGGER.info("Change power state result: %s", result)

    def handle_status(call):
        status = controller.get_current_input()
        hass.states.set(f"{DOMAIN}.input", status)

    hass.services.register(DOMAIN, "register", handle_register)
    hass.services.register(DOMAIN, "cmd", handle_cmd, schema=vol.Schema({
        vol.Required("cmd"): cv.string,
        vol.Optional("repeat", default=1): cv.positive_int
    }))
    hass.services.register(DOMAIN, "switch", handle_switch, schema=vol.Schema({
        vol.Required("target"): cv.string
    }))
    hass.services.register(DOMAIN, "set_volume", handle_set_volume, schema=vol.Schema({
        vol.Required("volume"): cv.positive_int
    }))
    hass.services.register(DOMAIN, "power", handle_power, schema=vol.Schema({
        vol.Required("action"): vol.In(["on", "off"])
    }))
    hass.services.register(DOMAIN, "status", handle_status)

    _LOGGER.info("Sony STR-DN840 integration setup complete")
    return True
