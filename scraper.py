import sys

import credentials
import elements
import logging


class Scraper:
    def __init__(self, payload):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Scraper.")
 
        self.elements = elements.Elements(payload)
        self.payload = payload 
        
        self.units = self.start()
    def close(self):
        self.elements.quit()
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

        self.elements.wait("list", "listings")

        listings = self.elements.get_elements("list", "listings")

        ids = []
        #FIXME Can listings get stale?
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
        #self.elements.wait("rental", "rent")
        #FIXME figure out how to precisely wait for all the data to load, not just elements
        self.elements.wait_for_content_to_load("unit", "rent")
        self.elements.wait_for_content_to_load("unit", "address")

        unit = self.elements.scrape_unit(identifier)

        return unit
