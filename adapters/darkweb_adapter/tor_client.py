import requests
from stem import Signal
from stem.control import Controller

class TorClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.proxies = {'http': 'socks5h://127.0.0.1:9050'}

    def renew_identity(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
