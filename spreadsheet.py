#import xlsxwriter
import re
import pandas as pd

TEMP_LISTING = "listing_to_post.xlsx"

re_address = re.compile("(.*),(.*),(.*),(.*)")
re_num = re.compile("([a-zA-Z#\ .]*)([0-9]+)([a-zA-Z#\ .]*)")

class Spreadsheet:
    #  This object is used to store the info for an unit.
    def __init__(self, debug):
        self.debug = debug
        #Page 1 and 2
        self.full_address = None
        self.street_num = None
        self.street_name = None
        self.city = None
        self.state = None
        self.zip = None
        self.display_exact_address = None
        self.index = {
                "actual address": 0,
                "put in address": 1,
                "display exact address": 2,
                }
    def get_street_num(address):
        return "BLah"
    def get_street_name(address):
        return "BLah"
    def get_city(address):
        return "BLah"
    def get_state(address):
        return "BLah"
    def get_zip(address):
        return "Blah"
    def get_display_exact(string):
        return "Blah"
    def get_listing_data(self):
        listing = pd.read_excel(TEMP_LISTING, sheet_name = 6)

        for key in self.index:
            print (key + ": \t\t", listing.iloc[self.index[key]][3])

        print("\nParsing address: 1193 Commonwealth Ave., #15, Boston, MA\n")
        print(self.parse_address("1193 Commonwealth Ave., #15, Boston, MA"))
        
        return listing.head()
    def parse_address(self, address):
        old = address
        if self.debug != None:
            print ("-stripping whitespace.")
        address = address.strip()
        if self.debug != None:
            print ("-splitting address.")
        result = re_address.split(address)
        if self.debug != None:
            print ("-cleaning up entry.")
        result = list(filter(None, result))
        temp_add = re_num.split(result[0])
        if self.debug != None:
            print ("-cleaning up name.")
        temp_add = list(filter(None, temp_add))
        temp_add[0] = temp_add[0].strip()
        temp_add[1] = temp_add[1].strip()
        if self.debug != None:
            print ("-fetching unit# from: \"", result[1], "\"")
        if self.debug != None:
            print ("-cleaning up unit number.")
        temp_unit = result[1][1:].strip()

        return {
                "full": old,
                "number": temp_add[0],
                "name": temp_add[1],
                "unit": temp_unit[1:],
                "city": result[2],
                "zip": "NONE",
                "state": result[3]
                }    
