import geohelper

import logging
import os.path
import pprint 
import pandas as pd
import re
import sys 

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

        self.log.debug("FIXME Figure out all the fields. Not all fields are present on all units.")

        pprint.pprint(data)

        labels = self.get_columns(data)

        df = pd.DataFrame(columns = labels)
        pd.set_option('display.max_colwidth', 50)

        for l in labels:
            width = len(l) * 13
            self.log.debug("Width of [" + str(l) + "] = " + str(width))

            df.style.set_properties(subset=[l], **{'width': str(width) + 'px'})

        df.to_excel(LISTING ,
                sheet_name='Scrapings from #' + "add_listing_id",
                na_rep = "[MISSING DATA]",
                index = False)

        self.log.warning("The data alignment is messed up. FIXME.")


        input("Old below")

        processed_data = []

        row = 0
        for unit in data:
            processed_data.append([])
            for v in unit:
                processed_data[row].append(unit[v]["value"])
            row = row + 1

        pprint.pprint(processed_data)

        df = pd.DataFrame(processed_data)

        df.to_excel(LISTING ,
                sheet_name='Scrapings from #' + "add_listing_id",
                na_rep = "[MISSING DATA]",
                index = False)

        self.log.warning("The data alignment is messed up. FIXME.")
