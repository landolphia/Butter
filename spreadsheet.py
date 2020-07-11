import geohelper
import keywords

import logging
import os.path
import pprint
import xlsxwriter
import re

from datetime import datetime


LISTING = "scrapings.xlsx"
MAX_COLUMN_WIDTH = 60

class Spreadsheet:
    def __init__(self, **kwargs):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Spreadsheet.")

        argument = None
        for k in kwargs:
            if k == "output":
                self.create(kwargs[k])
            elif k == "input":
                self.log.error("Implement excel scraping")
                sys.exit()
            else:
                self.log.warning("Unrecognized argument [" + str(k) + "].")
                sys.exit()
    def get_columns(self, data):
        columns = []

        for unit in data:
            for k in unit:
                if not (k in columns):
                    self.log.debug("Adding column [" + str(k) + "]")
                    columns.append(k)
                else:
                    self.log.debug("Skipping duplicate column [" + str(k) + "]")

        return columns
    def create(self, data):
        if os.path.isfile(LISTING):
            self.log.warning("Deleting current scrapings [" + str(LISTING) + "].")
            os.remove(LISTING)

        workbook = xlsxwriter.Workbook('scrapings.xlsx')

        bold = workbook.add_format({"bold": True})
        not_bold = workbook.add_format({"bold": False})

        color_formats = {}
        kw = keywords.Keywords()
        colors = kw.get_colors()
        for c in colors:
            bright = workbook.add_format()
            bright.set_bg_color(colors[c][0])
            dim = workbook.add_format()
            dim.set_bg_color(colors[c][1])
            color_formats[c] = {"bright": bright, "dim"   : dim}

        for lead in data:
            self.log.warning("Processing #" + str(lead))
            worksheet = workbook.add_worksheet("Leads #" + str(lead))
            labels = self.get_columns(data[lead])
            worksheet.write_row(0,0, labels, bold)

            # Getting columns width based on content
            widths = [0] * len(labels)
            for unit in data[lead]:
                self.log.warning("Processing unit #" + unit["ID"])
                col = 0
                for key in unit:
                    widths[col] = min([max([len(labels[col]), len(unit[key])]), MAX_COLUMN_WIDTH])
                    col = col + 1

            # Setting columns width based on results
            col = 0
            for w in widths:
                worksheet.set_column(col, col, widths[col])
                col = col + 1
                row = 1
                
            # Filling in worksheet with data
            for unit in data[lead]:
                col = 0
                for key in unit:
                    kw_found = False
                    for k in kw.get_keywords():
                        if str(k).lower() in str(unit[key]).lower():
                            kw_found = k 
                            self.log.debug("Keyword found [" + str(k) + "] in (" + unit[key] + ")")
                            break
                    if not (kw_found == False):
                        worksheet.write(row, col, unit[key], color_formats[kw.get_keywords()[kw_found]]["dim"])
                    else:
                        worksheet.write(row, col, unit[key], not_bold)
                    worksheet.set_row(row, 16)
                    col = col + 1
                row = row + 1
        
            # Write key to spreadsheet
            row = row + 2
            for k in kw.get_keywords():
                worksheet.write(row, 0, "", color_formats[kw.get_keywords()[k]]["bright"])
                worksheet.write(row, 1, str(k), color_formats[kw.get_keywords()[k]]["dim"])
                row = row + 1
    
        workbook.close()

        self.log.info(str(LISTING) + " created.")

#import geohelper
#
#import logging
#import os.path
#import pprint 
#import pandas as pd
#import re
#import sys 
#
#from datetime import datetime
#
#
#LISTING = "listing.xlsx"
#SHEET_NAME = 0
#HORIZ_OFFSET = 3
#VERT_OFFSET = 0
#
#re_address = re.compile("(.*),(.*),(.*),(.*)")
#re_num = re.compile("([a-zA-Z#\ .]*)([0-9]+)([a-zA-Z#\ .]*)")
#
#class Spreadsheet:
#    def __init__(self, creds):
#        self.log = logging.getLogger("bLog")
#        self.log.debug("Initializing Scraper.")
#        if not (os.path.exists(LISTING)):
#            self.log.error("Couldn't find the listing to post.\nThe file should be called '" + LISTING + "' and be placed in the running directory.")
#            sys.exit()
#        self.data = pd.read_excel(LISTING, sheet_name = SHEET_NAME)
#        # This replaces empty cells with None (instead of nan)
#        self.data = self.data.where(pd.notnull(self.data), None)
#        self.geo = geohelper.GeoHelper(creds)
#    def cell_exists(self, depth): return self.data.shape[0] > depth 
#    def get_key(self, key): return self.data.iloc[key+VERT_OFFSET][HORIZ_OFFSET]
#    def parse_date(self, date):
#        if date == None: return None
#        if not isinstance(date, datetime):
#            self.log.error("This date is not valid \'" + str(date) + "\'.\nPlease check the data in the spreadsheet.")
#            self.log.warning("This is the only format accepted for dates 'DD/MM/202Y'.")
#
#            sys.exit()
#        date = date.strftime("%m/%d/%Y")
#
#        return date
#    def parse_address(self, address):
#        old = address
#        address = address.strip()
#        result = re_address.split(address)
#        result = list(filter(None, result))
#
#        temp_add = re_num.split(result[0])
#        temp_add = list(filter(None, temp_add))
#        temp_add[0] = temp_add[0].strip()
#        temp_add[1] = temp_add[1].strip()
#        temp_unit = result[1][1:].strip()
#
#        zipcode = self.geo.get_zip(old)
#        return {
#                "full": old,
#                "number": temp_add[0],
#                "name": temp_add[1],
#                "unit": temp_unit[1:],
#                "city": result[2],
#                "state": result[3],
#                "zip": zipcode
#                }    
