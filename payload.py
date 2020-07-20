import json
import logging
import os
import sys


PAYLOAD_FILE = "payload.json"
PAYLOAD_TEST = "payload_test.json"

class Payload:
    def __init__(self, mode, test):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Payload.")

        self.mode = mode
        if test:
            self.payload_file = "./post/" + PAYLOAD_TEST 
        else:
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
    #def __remove_fluff__(self, value):
    #    content = value["content"]
    #    if ("fluff" in value):
    #        if not (isinstance(content, str)):
    #            self.log.error("Can't remove fluff from non-string value.")
    #            sys.exit()
    #            
    #        self.log.debug("Removing fluff from [" + str(content) + "].")
    #        for f in value["fluff"]:
    #            content = content.replace(f, "")
    #        self.log.debug(" => [" + str(content) + "].")
    #
    #    return content
    #def __validate_identifier__(self, identifier):
    #    self.log.debug("Validating element identifier.")
    #    if not "type" in identifier:
    #        self.log.error("Missing identifier type.")
    #        sys.exit()
    #    if not identifier["type"] in ["xpath", "id"]:
    #        self.log.error("Unrecognized identifier type [" + str(identifier["type"]) + "].")
    #        sys.exit()
    #    if not "value" in identifier:
    #        self.log.error("Missing identifier value.")
    #        sys.exit()
    #def __validate_offset__(self, offset):
    #    if not isinstance(offset, int):
    #        self.log.error("Offset is not an integer.")
    #        sys.exit()
    #    elif offset < 0:
    #        self.log.error("Offset must be positive.")
    #        sys.exit()
    #def __validate_content__(self, value):
    #    if not "content" in value:
    #        self.log.error("Missing element content.")
    #        sys.exit()

#TODO NOT UPDATED

    def set_value2(self, page, name, value, number):
        self.log.debug("Setting value for [" + str(page) + "/" + str(name) + "] (" + str(value) + ")")
        self.__add__element__(page, name, None, None, number, value)

    def get_bool(self, page, name): return self.elements[page][name]["value"] == "Y"
    def get_value(self, page, name): return self.elements[page][name]["value"]
    def id(self, page, name): return self.elements[page][name]["id"]
    def offset(self, page, name): return self.elements[page][name]["offset"]
    def set_value(self, page, name, value): self.elements[page][name]["value"] = value
    def xpath(self, page, name): return self.elements[page][name]["xpath"]
