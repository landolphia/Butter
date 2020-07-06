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
 
        self.elements = elements.Elements(payload, offline)
        self.payload = payload 
        
        self.units = None
        if not offline:
            self.units = self.start()
        else:
            if not os.path.isfile(OFFLINE_FILE):
                self.log.warning("Offline file doesn't exist. Downlaoding data to file.")
                self.units = self.start()
                self.elements.quit()
                with open(OFFLINE_FILE, 'w') as f:
                   json.dump(self.units, f) 

            if self.units == None:
                self.log.info("Loading data from offline file.")
                with open(OFFLINE_FILE) as f:
                    self.units = json.load(f)
                pprint.pprint(self.units)

    def get_units(self):
        return self.units
    def start(self):
        self.login()
        #TODO Get listing id from... somewhere?

        return self.get_rentals_list("4067267")
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
