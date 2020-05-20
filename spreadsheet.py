import re
import sys 
import pprint 
import pandas as pd

import geohelper

TEMP_LISTING = "listing_to_post.xlsx"

re_address = re.compile("(.*),(.*),(.*),(.*)")
re_num = re.compile("([a-zA-Z#\ .]*)([0-9]+)([a-zA-Z#\ .]*)")

class Spreadsheet:
    #  This object is used to store the info for an unit.
    def __init__(self, debug, creds):
        self.DEBUG = debug
        # Page 1 and 2
        self.full_address = None
        self.street_num = None
        self.street_name = None
        self.unit = None
        self.city = None
        self.state = None
        self.zip = None
        self.display_exact_address = None
        # Extra
        self.index = {
                "actual address": 0,
                "put in address": 1,
                "display exact address": 2,
                }
        self.data = pd.read_excel(TEMP_LISTING, sheet_name = 6)
        self.geo = geohelper.GeoHelper(debug, creds)
    def disp(self):
        pprint.pprint(vars(self))
    def get_key(self, key):
        return self.data.iloc[self.index[key]][3]
    def get_listing_data(self):
        if self.DEBUG != None:
            for key in self.index:
                print (key + ": \t\t", self.get_key(key))

        address = self.get_key("actual address")
        print("\nParsing address: ", address)

        self.set_address(address)
        self.display_exact_address = False if self.get_key("display exact address") == 'N' else True

        self.disp()
        return self
    def set_address(self, address):
        address = self.parse_address(address)
        self.full_address = address["full"]
        self.street_num = address["number"]
        self.street_name = address["name"]
        self.unit = address["unit"]
        self.city = address["city"]
        self.state = address["state"] 
        if self.DEBUG != None:
            print("Getting postal code.")
        self.zip = self.geo.get_zip(self.full_address)
    def parse_address(self, address):
        old = address
        if self.DEBUG != None:
            print ("Stripping whitespace.")
        address = address.strip()
        if self.DEBUG != None:
            print ("Splitting address.")
        result = re_address.split(address)
        if self.DEBUG != None:
            print ("Cleaning up entry.")
        result = list(filter(None, result))
        temp_add = re_num.split(result[0])
        if self.DEBUG != None:
            print ("Cleaning up name.")
        temp_add = list(filter(None, temp_add))
        temp_add[0] = temp_add[0].strip()
        temp_add[1] = temp_add[1].strip()
        if self.DEBUG != None:
            print ("Fetching unit# from: \"", result[1], "\"")
        if self.DEBUG != None:
            print ("Cleaning up unit number.")
        temp_unit = result[1][1:].strip()

        return {
                "full": old,
                "number": temp_add[0],
                "name": temp_add[1],
                "unit": temp_unit[1:],
                "city": result[2],
                "state": result[3]
                }    
