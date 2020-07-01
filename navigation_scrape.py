import logging


class Navigator:
    def __init__(self, payload):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Navigator.")
            
    def start(self):
        self.login()

    def login(self):
        print("Borf")
