import json
import logging
import os
import sys


PAYLOAD_FILE = "payload.json"
PAYLOAD_UNLEADED_FILE = "payload_unleaded.json"

class Payload:
    def __init__(self, mode, *args):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Payload.")

        self.mode = mode
        
        self.payload_file = None
        for a in args:
            if a == "unleaded":
                self.payload_file = mode.lower() + "/" + PAYLOAD_UNLEADED_FILE 
            else:
                self.log.warning("Unrecognized argument for Payload [" + str(a) + "]")
        if self.payload_file == None:
            self.payload_file = mode.lower() + "/" + PAYLOAD_FILE 

        if not os.path.isfile(self.payload_file):
            self.log.error("Couldn't find the payload file. [" + self.payload_file+ "].")
            sys.exit()

        self.log.debug("Loading payload configuration file [" + self.payload_file + "].")

        data = None
        with open(self.payload_file) as data_file:
            data = json.load(data_file)

        self.__init_data__(data)
    def __init_data__(self, data):
        self.run_once = {}
        if "run once" in data:
            self.run_once = data["run once"]
        self.repeat = {}
        if "repeat" in data:
            self.repeat = data["repeat"]
        self.trigger = {}
        if "trigger" in data:
            self.trigger = data["trigger"]
