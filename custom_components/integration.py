import requests
import time
import urllib.parse

class SonySTRDN840Controller:
    def __init__(self, host, port_status=80, port_control=80,
                 myid="default_id", mydevinfo="default_devinfo",
                 myuseragent="HomeAssistant", alternative=None,
                 myname="SonyReceiver", max_vol=20):
        self.host = host
        self.port_status = port_status
        self.port_control = port_control
        self.myid = myid
        self.mydevinfo = mydevinfo
        self.myuseragent = myuseragent
        self.alternative = alternative if alternative else {}
        self.myname = myname
        self.max_vol = max_vol
        self.inputs = ["BD", "DVD", "GAME", "SAT/CATV", "VIDEO", "TV",
                       "SA-CD/CD", "FM TUNER", "AM TUNER", "USB", "HOME NETWORK", "SEN"]
        self.commands = {
            "str_powermain":    "AAAAAgAAADAAAAAVAQ==",
            "mute":             "AAAAAgAAADAAAAAUAQ==",
            "muteon":           "AAAAAwAADRAAAAAgAQ==",
            "muteoff":          "AAAAAwAADRAAAAAhAQ==",
            "confirm":          "AAAAAgAAADAAAAAMAQ==",
            "home":             "AAAAAgAAADAAAABTAQ==",
            "display":          "AAAAAgAAADAAAABLAQ==",
            "return":           "AAAAAwAAARAAAAB9AQ==",
            "options":          "AAAAAwAAARAAAABzAQ==",
            "str_functionplus": "AAAAAgAAALAAAABpAQ==",
            "str_functionminus":"AAAAAgAAALAAAABqAQ==",
            "play":             "AAAAAwAAARAAAAAyAQ==",
            "pause":            "AAAAAwAAARAAAAA5AQ==",
            "stop":             "AAAAAwAAARAAAAA4AQ==",
            "next":             "AAAAAwAAARAAAAAxAQ==",
            "prev":             "AAAAAwAAARAAAAAwAQ==",
            "str_shuffle":      "AAAAAwAAARAAAAAqAQ==",
            "str_repeat":       "AAAAAwAAARAAAAAsAQ==",
            "str_ff":           "AAAAAwAAARAAAAA0AQ==",
            "str_fr":           "AAAAAwAAARAAAAAzAQ==",
            "volumeup":         "AAAAAgAAADAAAAASAQ==",
            "volumedown":       "AAAAAgAAADAAAAATAQ==",
            "up":               "AAAAAgAAALAAAAB4AQ==",
            "down":             "AAAAAgAAALAAAAB5AQ==",
            "left":             "AAAAAgAAALAAAAB6AQ==",
            "right":            "AAAAAgAAALAAAAB7AQ==",
            "str_num1":         "AAAAAgAAADAAAAAAAQ==",
            "str_num2":         "AAAAAgAAADAAAAABAQ==",
            "str_num3":         "AAAAAgAAADAAAAACAQ==",
            "str_num4":         "AAAAAgAAADAAAAADAQ==",
            "str_num5":         "AAAAAgAAADAAAAAEAQ==",
            "str_num6":         "AAAAAgAAADAAAAAFAQ==",
            "str_num7":         "AAAAAgAAADAAAAAGAQ==",
            "str_num8":         "AAAAAgAAADAAAAAHAQ==",
            "str_num9":         "AAAAAgAAADAAAAAIAQ==",
            "str_num0":         "AAAAAgAAADAAAAAJAQ==",
            "str_puredirect":   "AAAAAwAABRAAAAB5AQ=="
        }
        
    def get_current_input(self, alternativeNames=False):
        url = f"http://{self.host}:{self.port_status}/cers/getStatus"
        headers = {
            'X-CERS-DEVICE-ID': self.myid,
            'X-CERS-DEVICE-INFO': self.mydevinfo,
            'Connection': 'close',
            'User-Agent': self.myuseragent,
            'Host': f'{self.host}:{self.port_status}',
            'Accept-Encoding': 'gzip'
        }
        try:
            r = requests.get(url, headers=headers, timeout=0.75)
        except:
            return "offline"
        try:
            source = r.text.split("=")[3].split("\"")[1]
            if not alternativeNames:
                return source
            else:
                return self.alternative[source] if source in self.alternative else source
        except IndexError:
            return "error"

    def send_command(self, key, repeat=1):
        if key.lower() == "power":
            key = "str_powermain"
        if key.lower() not in self.commands:
            return f"Keycode for {key} not found."
        keycode = self.commands[key.lower()]
        url = f"http://{self.host}:{self.port_control}/upnp/control/IRCC"
        headers = {
            'soapaction': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
            'content-type': 'text/xml; charset=utf-8',
            'Connection': 'close',
            'User-Agent': self.myuseragent,
            'Host': f'{self.host}:{self.port_control}',
            'Accept-Encoding': 'gzip'
        }
        payload = "<?xml version=\"1.0\"?>"
        payload += "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">"
        payload += "<s:Body> <u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"> <IRCCCode>" + keycode + "==</IRCCCode>"
        payload += "</u:X_SendIRCC> </s:Body> </s:Envelope>"
        for _ in range(int(repeat)):
            try:
                requests.post(url, headers=headers, data=payload, timeout=5)
            except:
                pass
            time.sleep(0.5)
        return "Command sent"

    def switch_input_to(self, target):
        target = target.upper()
        if target == "SAT":
            target = "SAT/CATV"
        if target == "SACD":
            target = "SA-CD/CD"
        if target == "FM":
            target = "FM TUNER"
        if target == "AM":
            target = "AM TUNER"
        if target == "NET":
            target = "HOME NETWORK"
        if target not in self.inputs:
            return f"Can't switch to this source: {target}."
        idx = self.inputs.index(target)
        current = self.get_current_input()
        if current not in self.inputs:
            return f"Current input {current} not recognized."
        cidx = self.inputs.index(current)
        diff = idx - cidx
        if diff < 0:
            return self.send_command("STR_FunctionMinus", abs(diff))
        else:
            return self.send_command("STR_FunctionPlus", diff)

    def set_volume_to(self, volume):
        vol = int(volume)
        if vol > self.max_vol:
            vol = self.max_vol
        # Reset volume by lowering then raise to desired level
        self.send_command("VolumeDown", self.max_vol * 2)
        return self.send_command("VolumeUp", vol)

    def register(self):
        encodedid = urllib.parse.quote_plus(self.myid)
        url = f'http://{self.host}:{self.port_status}/cers/register?name={self.myname}&registrationType=initial&deviceId={encodedid}'
        headers = {
            'X-CERS-DEVICE-ID': self.myid,
            'X-CERS-DEVICE-INFO': self.mydevinfo,
            'Connection': 'close',
            'User-Agent': self.myuseragent,
            'Host': f'{self.host}:{self.port_status}',
            'Accept-Encoding': 'gzip'
        }
        try:
            requests.get(url, headers=headers, timeout=5)
            return "Registered"
        except Exception as e:
            return f"Registration failed: {e}"

    def change_power_state(self, action):
        current_input = self.get_current_input()
        is_powered = False if current_input == "BD" else True
        if (action == "on" and not is_powered) or (action == "off" and is_powered):
            return self.send_command("str_powermain", 1)
        return "No change needed"
