import geohelper

import logging
import os.path
import pprint
import xlsxwriter
import re

from datetime import datetime


LISTING = "scrapings.xlsx"

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
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0,0, labels, bold)
        
        for col in range(len(labels)):
                width = len(labels[col])
                worksheet.set_column(col, col, width)
                

        row = 1
        for unit in data:
            col = 0
            for key in unit:
                worksheet.write(row, col, unit[key])
                col = col + 1
            row = row + 1

        workbook.close()
