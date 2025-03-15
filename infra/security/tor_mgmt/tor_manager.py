from stem.control import Controller

class TorManager:
    def renew_identity(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal('NEWNYM')
