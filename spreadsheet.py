import logging
import geohelper
import os.path
import pprint 
import pandas as pd
import re
import sys 


TEMP_LISTING = "listing_to_post.xlsx"
SHEET_NAME = 0
HORIZ_OFFSET = 3
VERT_OFFSET = 0

re_address = re.compile("(.*),(.*),(.*),(.*)")
re_num = re.compile("([a-zA-Z#\ .]*)([0-9]+)([a-zA-Z#\ .]*)")

class Spreadsheet:
    def __init__(self, creds):
        self.log = logging.getLogger("root")
        self.log.info("Initializing scraper.")
        if not (os.path.exists(TEMP_LISTING)):
            self.log.error("Couldn't find the listing to post.\nThe file should be called '" + TEMP_LISTING + "' and be placed in the running directory.")
            sys.exit()
        self.data = pd.read_excel(TEMP_LISTING, sheet_name = SHEET_NAME)
        # This replaces empty cells with None (instead of nan)
        self.data = self.data.where(pd.notnull(self.data), None)
        self.geo = geohelper.GeoHelper(creds)
    def disp(self):
        pprint.pprint(vars(self))
    def get_key(self, key):
        return self.data.iloc[key+VERT_OFFSET][HORIZ_OFFSET]
    def parse_address(self, address):
        old = address
        address = address.strip()
        result = re_address.split(address)
        result = list(filter(None, result))

        temp_add = re_num.split(result[0])
        temp_add = list(filter(None, temp_add))
        temp_add[0] = temp_add[0].strip()
        temp_add[1] = temp_add[1].strip()
        temp_unit = result[1][1:].strip()

        zipcode = self.geo.get_zip(old)
        return {
                "full": old,
                "number": temp_add[0],
                "name": temp_add[1],
                "unit": temp_unit[1:],
                "city": result[2],
                "state": result[3],
                "zip": zipcode
                }    
