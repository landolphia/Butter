import json
import os
import pprint
import sys

import credentials
import elements
import logging


OFFLINE_FILE = "offline_data.json"

class Scraper:
    def __init__(self, payload, offline):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Scraper.")
 
        self.payload = payload 
        self.lead_id = "4067267"
        
        self.units = None
        if not offline:
            self.elements = elements.Elements(payload, False)
            self.units = self.start()
        else:
            if not os.path.isfile(OFFLINE_FILE):
                self.log.warning("Offline file doesn't exist. Downloading data to file.")
                self.elements = elements.Elements(payload, False)
                self.units = self.start()
                with open(OFFLINE_FILE, 'w') as f:
                   json.dump(self.units, f) 
            else:
                self.log.info("Loading data from offline file.")
                with open(OFFLINE_FILE) as f:
                    self.units = json.load(f)
                self.elements = elements.Elements(payload, True)

    def get_units(self):
        return self.units
    def start(self):
        self.login()
        #TODO Get listing id from... somewhere?

        result = self.get_rentals_list(self.lead_id)

        self.elements.quit()

        return result
    def get_lead_id(self): return self.lead_id
    def login(self):
        self.elements.go("login", "login url")
        self.elements.wait("login", "submit button")

        self.elements.fill_input("login", "username")
        self.elements.fill_input("login", "password")

        self.elements.click("login", "submit button")
    def get_rentals_list(self, identifier):
        self.elements.wait("list", "news")
        self.elements.go_list("list", "url", identifier)

        self.elements.wait_for_content_to_load("list", "id")

        listings = self.elements.get_elements("list", "listings")

        ids = []
        for l in listings:
            rental_id = l.get_attribute("data-rental-id")
            ids.append(rental_id)

        units = []
        for i in ids:
            unit = self.process_rental(i)
            units.append(unit)

        return units
    def process_rental(self, identifier):
        self.elements.go_rental("rental", "url", identifier)
        self.elements.wait_for_content_to_load("unit", "id")

        unit = self.elements.scrape_unit(identifier)

        return unit
