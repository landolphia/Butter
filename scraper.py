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
        
        self.start()
        self.elements.quit()
    def start(self):
        self.login()
        #TODO Get listing id from... somewhere?
        self.get_rentals_list("4067267")
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
        for l in listings:
            self.log.debug("Listing: " + str(l))
            ids.append(l.get_attribute("data-rental-id"))

        for i in ids:
            self.log.debug("Processing #" + str(i))
            self.process_rental(i)
    def process_rental(self, identifier):
        self.elements.go_rental("rental", "url", identifier)
        self.elements.wait("rental", "rent")
        self.log.debug("Waited once.")
        self.elements.wait_for_content_to_load("rental", "rent")
        self.log.debug("This is super hacky, waiting twice seems to remove stale element issue.")
        self.elements.wait_for_content_to_load("rental", "rent")
        rent = self.elements.get_value("rental", "rent")
        self.log.debug("Rent for rental #" + str(identifier) + " = " + str(rent))
        self.log.info("Rent for rental #" + str(identifier) + " = " + str(rent))
