import credentials
import json
import logging
import sys

class Payload2:
    def __init__(self):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Payload2.")
    
        self.credentials = credentials.Credentials().get_credentials("private.slr")

        self.log.debug("Loading payload configuration file [payload.json].")
        with open('payload.json') as data_file:
            data = json.load(data_file)

        self.__init__data__(data)
    def __add__element__(self, page, name, css_id, css_xpath, cell_offset, value):
        if page not in self.data:
            self.data[page] = {}
        if name not in self.data[page]:
            if value == "[CALL.GET_USERNAME]":
                value = self.credentials["username2"]
            if value == "[CALL.GET_PASSWORD]":
                value = self.credentials["password2"]

            self.data[page][name] = {
                "id": css_id,
                "xpath": css_xpath,
                "offset": cell_offset,
                "value": value
            }
        else: # Duplicate key
            self.log.error("Error scraping initial data. Exiting." +
                    "\nPage = " + str(page) +
                    "\nName = " + str(name) + 
                    "\nCSS ID = " + str(css_id) +
                    "\nCSS XPATH = " + str(css_xpath) +
                    "\nCell offset = " + str(cell_offset) +
                    "\nValue = " + str(value))
            sys.exit()
    def __init__data__(self, data):
        self.data = {}
        # Login page
        for i in data["payload"]:
            self.__add__element__(i["page"], i["name"], i["id"], i["xpath"], i["offset"], i["value"])
        self.credentials = None
    def get_bool(self, page, name): return self.data[page][name]["value"] == "Y"
    def get_value(self, page, name): return self.data[page][name]["value"]
    def id(self, page, name): return self.data[page][name]["id"]
    def offset(self, page, name): return self.data[page][name]["offset"]
    def set_value(self, page, name, value): self.data[page][name]["value"] = value
    def xpath(self, page, name): return self.data[page][name]["xpath"]
