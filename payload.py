import json
import logging
import os
import sys


PAYLOAD_FILE = "payload.json"

class Payload:
    def __init__(self):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Payload.")
    
        if not os.path.isfile(PAYLOAD_FILE):
            self.log.error("Couldn't find the payload file. [" + PAYLOAD_FILE+ "].")
            sys.exit()

        self.log.debug("Loading payload configuration file [" + PAYLOAD_FILE + "].")

        data = None
        with open(PAYLOAD_FILE) as data_file:
            data = json.load(data_file)

        self.__init_data__(data)
    def __add__element__(self, element):
        self.log.debug("Adding element: " + str(element))

        page = None
        name = None

        if "page" in element:
            page = element["page"]
            if page not in self.elements:
                self.log.debug("Adding page [" + str(page) + "] to elements.")
                self.elements[page] = {}

            if "name" in element:
                name = element["name"]
                if name not in self.elements[page]:
                    self.elements[page][name] = element
                    self.log.debug("Element added.")
                else:
                    self.log.error("Found duplicate entry for [" + str(page) + "/" + str(name) + "].")
                    sys.exit()

        if not (page and name):
            self.log.error("Missing essential key, 'page' and 'name' are needed for each element.")
            sys.exit()

        element.pop("page")
        element.pop("name")

        for k in element:
            self.log.debug("Processing [" + str(k) + "] = " + str(element[k]))
            
            if k == "identifier": self.__validate_identifier__(element[k])
            if k == "offset": self.__validate_offset__(element[k])
            if k == "value":
                element[k] = self.__fill_value__(element[k])
                self.__validate_content__(element[k])
                element[k]["content"] = self.__remove_fluff__(element[k])

            self.elements[page][name] = element
            self.log.warning("Element = " + str(self.elements[page][name]))

        self.log.debug("Element processed.")
    def __remove_fluff__(self, value):
        content = value["content"]
        if ("fluff" in value):
            if not (isinstance(content, str)):
                self.log.error("Can't remove fluff from non-string value.")
                sys.exit()
                
            self.log.debug("Removing fluff from [" + str(content) + "].")
            for f in value["fluff"]:
                content = content.replace(f, "")
            self.log.debug(" => [" + str(content) + "].")
    
        return content
    def __fill_value__(self, value):
        if ("actions" in value) and (value["actions"]["exec"] == "auto"):
            for a in value["actions"]["list"]:
                self.log.debug("Processing value action: " + a)
                if a == "GET_USERNAME":
                    self.log.error("SUPER TEMPORARY,  HARCODED PASSWORD AND USERNAME")
                elif a == "GET_PASSWORD":
                    self.log.error("SUPER TEMPORARY,  HARCODED PASSWORD AND USERNAME")
                else:
                    self.log.error("Invalid value action [" + str(a) + "].")

        return value

    def __validate_identifier__(self, identifier):
        self.log.debug("Validating element identifier.")
        if not "type" in identifier:
            self.log.error("Missing identifier type.")
            sys.exit()
        if not identifier["type"] in ["xpath", "id"]:
            self.log.error("Unrecognized identifier type [" + str(identifier["type"]) + "].")
            sys.exit()
        if not "value" in identifier:
            self.log.error("Missing identifier value.")
            sys.exit()
    def __validate_offset__(self, offset):
        if not isinstance(offset, int):
            self.log.error("Offset is not an integer.")
            sys.exit()
        elif offset < 0:
            self.log.error("Offset must be positive.")
            sys.exit()
    def __validate_content__(self, value):
        if not "content" in value:
            self.log.error("Missing element content.")
            sys.exit()

#        if name not in self.data[page]:
#            if value == "[CALL.GET_USERNAME]":
#                value = self.credentials["username2"]
#            if value == "[CALL.GET_PASSWORD]":
#                value = self.credentials["password2"]

    def __init_data__(self, data):
        self.__init_mode__(data)

        self.elements= {}
        for i in data["elements"]:
            self.__add__element__(i)

        self.credentials = None
    def __init_mode__(self, data):
        if "mode" in data:
            if data["mode"] in ["SCRAPE", "POST"]:
                self.mode = data["mode"]
                self.log.debug("Setting mode to [" + self.mode + "]")
            else: 
                self.log.error("Invalid mode [" + data["mode"] + "].")
                sys.exit()
        else:
            self.log.error("Mode not found in [" + PAYLOAD_FILE + "].")
            sys.exit()

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
