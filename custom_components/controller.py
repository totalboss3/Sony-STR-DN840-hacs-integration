"""Controller for Sony STR-DN840 receiver."""
import requests

class SonySTRDN840Controller:
    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    def send_command(self, command):
        """Send a command to the receiver."""
        url = f"{self.base_url}/command?cmd={command}"
        response = requests.get(url)
        return response.text
