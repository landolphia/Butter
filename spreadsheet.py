import geohelper

import logging
import os.path
import pprint 
import pandas as pd
import re
import sys 

from datetime import datetime


LISTING = "listing.xlsx"
SHEET_NAME = 0
HORIZ_OFFSET = 3
VERT_OFFSET = 0

re_address = re.compile("(.*),(.*),(.*),(.*)")
re_num = re.compile("([a-zA-Z#\ .]*)([0-9]+)([a-zA-Z#\ .]*)")

class Spreadsheet:
    def __init__(self, creds):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Scraper.")
        if not (os.path.exists(LISTING)):
            self.log.error("Couldn't find the listing to post.\nThe file should be called '" + LISTING + "' and be placed in the running directory.")
            sys.exit()
        self.data = pd.read_excel(LISTING, sheet_name = SHEET_NAME)
        # This replaces empty cells with None (instead of nan)
        self.data = self.data.where(pd.notnull(self.data), None)
        self.geo = geohelper.GeoHelper(creds)
    def cell_exists(self, depth): return self.data.shape[0] > depth 
    def get_key(self, key): return self.data.iloc[key+VERT_OFFSET][HORIZ_OFFSET]
    def parse_date(self, date):
        if date == None: return None
        if not isinstance(date, datetime):
            self.log.error("This date is not valid \'" + str(date) + "\'.\nPlease check the data in the spreadsheet.")
            self.log.warning("This is the only format accepted for dates 'DD/MM/202Y'.")

            sys.exit()
        date = date.strftime("%m/%d/%Y")

        return date
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
