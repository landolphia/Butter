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
    def start(self):
        self.login()
        #TODO Get listing id from... somewhere?
        self.process_list("4067267")
    def login(self):
        self.elements.go("login", "login url")
        self.elements.wait("login", "submit button")

        self.elements.fill_input("login", "username")
        self.elements.fill_input("login", "password")

        self.elements.click("login", "submit button")
    def process_list(self, identifier):
        self.elements.wait("list", "news")
        self.elements.go_id("list", "url", identifier)

        self.elements.wait("list", "listings")

        listings = self.elements.get_elements("list", "listings")

        for l in listings:
            self.log.debug("Listing: " + str(l))
