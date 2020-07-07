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

class Scrapings:
    def __init__(self):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Scrapings.")
    def get_columns(self, data):
        columns = []
        for unit in data:
            for v in unit:
                if not (v in columns):
                    self.log.debug("Adding column [" + str(v) + "]")
                    columns.append(v)
                else:
                    self.log.debug("Skipping duplicate column [" + str(v) + "]")

        return columns
    def create(self, data):
        if os.path.isfile(LISTING):
            self.log.warning("Deleting current scrapings [" + str(LISTING) + "].")
            os.remove(LISTING)

        labels = self.get_columns(data)
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
            color_formats[c] = {
                    "bright": bright,
                    "dim"   : dim
                                }

        # TODO When/if scraping multiple lists use multiple worksheets
        # and name them appropriately.
        worksheet = workbook.add_worksheet("Leads #" + str(leads_id))
        worksheet.write_row(0,0, labels, bold)

        # Getting columns width based on content
        widths = [0] * len(labels)
        for unit in data:
            col = 0
            for key in unit:
                widths[col] = min([max([len(labels[col]), len(unit[key])]), MAX_COLUMN_WIDTH])
                col = col + 1

        # Setting columns width based on results
        col = 0
        for w in widths:
            worksheet.set_column(col, col, widths[col])
            col = col + 1
        
        # Filling in worksheet with data
        row = 1
        for unit in data:
            col = 0
            for key in unit:
                kw_found = False
                for k in kw.get_keywords():
                    # TODO replace with appropriate color
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
