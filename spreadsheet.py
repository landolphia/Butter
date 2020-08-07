import geohelper
import keywords

import logging
import os.path
import pandas as pd
import pprint
import xlsxwriter
import re
import sys

from datetime import datetime


# Pulk 
PULK_FILE = "./unleaded/leadyleads.xlsx"

# Output
SCRAPINGS = "./scrape/scrapings.xlsx"
MAX_COLUMN_WIDTH = 60

# Slurp
LISTING = "./post/listings.xlsx"
SHEET_NAME = 9
HORIZ_OFFSET = 3
VERT_OFFSET = 0

FP_START = 173
FP_LENGTH = 47

re_address = re.compile("(.*),(.*),(.*),(.*)")
re_num = re.compile("([a-zA-Z#\ .]*)([0-9]+)([a-zA-Z#\ .]*)")


class Spreadsheet:
    def __init__(self, **kwargs):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Spreadsheet.")

        argument = None
        for k in kwargs:
            if k == "output":
                self.create(kwargs[k])
            elif k == "slurp":
                self.slurp(kwargs[k])
            elif k == "lead":
                self.pulk(kwargs[k])
            else:
                self.log.warning("Unrecognized argument [" + str(k) + "].")
                sys.exit()
    # Slurp
    def slurp(self, creds):
        if not (os.path.exists(LISTING)):
            self.log.error("Couldn't find the listing to post.\nThe file should be called '" + LISTING + "' and be placed in ./post/.")
            sys.exit()

        self.data = pd.read_excel(LISTING, sheet_name = SHEET_NAME, converters={"Value" : str})
        # This replaces empty cells with None (instead of nan)
        self.data = self.data.where(pd.notnull(self.data), None)
        self.geo = geohelper.GeoHelper(creds)
        self.fp_offset =  FP_LENGTH
    def cell_exists(self, depth): return self.data.shape[0] > depth  # Used to determine if there are any more floorplans
    def get_floorplan_number(self):
        toggle = self.get_key(36)
        i = 0
        if toggle:
            offset = FP_START
            while (self.cell_exists(offset)):
                offset = offset + FP_LENGTH
                i = i+1

        return i
    def get_key(self, key):
        result = self.data.iloc[key+VERT_OFFSET][HORIZ_OFFSET]

        if result == "True": result = True
        if result == "False": result = False 
        if result == "None": result = None 

        return result
    def parse_date(self, date):
        if date == None: return None
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        if not isinstance(date , datetime):
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
    # Pulk
    def pulk(self, data):
        if os.path.isfile(PULK_FILE):
            self.log.warning("Deleting current scrapings [" + str(PULK_FILE) + "].")
            os.remove(PULK_FILE)

        workbook = xlsxwriter.Workbook(PULK_FILE)
        worksheet = workbook.add_worksheet("Lead safety")

        row = 1
        for lead in data:
            number = lead["address"]["number"]
            number = (number if not number == None else "N/A")
            street = lead["address"]["street"]
            street = (street if not street == None else "N/A")
            city = lead["address"]["city"]
            city = (city if not city == None else "N/A")
            address = str(number + " " + street + ", " + city)
            results = [address]
            for r in lead["rows"]:
                result = []
                if "date" in r:
                    date = r["date"]
                    date = (date if not date == None else "[No date]")
                    insp = r["ins_type"]
                    insp = (insp if not insp == None else "[No type]")
                    outcome = r["outcome"] 
                    outcome = (outcome if not outcome == None else "[No outcome]")
                    result = (str(date) + ": " + str(insp) + "->" + str(outcome))
                else:
                    result = r
                results.append(result)
            row = row + 1    
            worksheet.write_row(row, 0, results)

        workbook.close()

        self.log.info(str(PULK_FILE) + " created.")
    # Output
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
        if os.path.isfile(SCRAPINGS):
            self.log.warning("Deleting current scrapings [" + str(SCRAPINGS) + "].")
            os.remove(SCRAPINGS)

        workbook = xlsxwriter.Workbook(SCRAPINGS)

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
                col = 0
                for key in unit:
                    widths[col] = min([max([len(labels[col]), len(unit[key])]), MAX_COLUMN_WIDTH])
                    col = col + 1

            # Setting columns width based on results
            col = 0
            for w in widths:
                worksheet.set_column(col, col, widths[col])
                col = col + 1

            # Writing keywords labels
            row = 0
            key_start = col + 1
            for k in kw.get_keywords():
                col = col + 1
                worksheet.write(row, col, ", ".join(k["keywords"]), color_formats[k["color"]]["bright"])

            # Filling in worksheet with data
            row = 2
            for unit in data[lead]:
                col = 0
                for key in unit:
                    kw_found = False
                    color = False
                    key_offset = 0
                    for group in kw.get_keywords():
                        for k in group["keywords"]:
                            if str(k).lower() in str(unit[key]).lower():
                                color = group["color"]
                                kw_found = k 
                                self.log.debug("Keyword found [" + str(k) + "] in (%s)"% str(unit[key]).encode('utf-8'))
                                worksheet.write(row, key_start + key_offset, "", color_formats[color]["dim"])
                        key_offset = key_offset + 1
                    if not (kw_found == False):
                        worksheet.write(row, col, unit[key], color_formats[color]["dim"])
                    else:
                        worksheet.write(row, col, unit[key], not_bold)
                    worksheet.set_row(row, 16)
                    col = col + 1
                row = row + 1

        workbook.close()

        self.log.info(str(SCRAPINGS) + " created.")
        self.log.debug("Fix broker notes (elements vs element) and features (remove divs)")
