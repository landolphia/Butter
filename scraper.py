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
    def login(self):
        self.elements.go("login", "login url")
        self.elements.wait("login", "submit button")

        self.elements.fill_input("login", "username")
        self.elements.fill_input("login", "password")

        self.elements.click("login", "submit button")
