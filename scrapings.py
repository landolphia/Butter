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

        self.log.debug("FIXME Figure out all the fields. Not all fields are present on all units.")

        labels = self.get_columns(data)
        workbook = xlsxwriter.Workbook('scrapings.xlsx')
        bold = workbook.add_format({"bold": True})

        worksheet = workbook.add_worksheet()

        worksheet.write_row(0,0, labels, bold)
        
        for col in range(len(labels)):
                width = len(labels[col])
                worksheet.set_column(col, col, width)
                

        data = self.clean(data)

        row = 1
        for unit in data:
            col = 0
            for key in unit:
                worksheet.write(row, col, unit[key]["value"])
                col = col + 1
            row = row + 1

        workbook.close()
        
        #processed_data = []

        #row = 0
        #for unit in data:
        #    processed_data.append([])
        #    for v in unit:
        #        processed_data[row].append(unit[v]["value"])
        #    row = row + 1

        #df = pd.DataFrame(processed_data)

        #df.to_excel(LISTING ,
        #        sheet_name='Scrapings from #' + "add_listing_id",
        #        na_rep = "[MISSING DATA]",
        #        index = False)

        #self.log.warning("The data alignment is messed up. FIXME.")
    def clean(self, data):
#        {'address': {'value': 'On Market\xa099 Brainerd, #16, Boston, MA 02134 '
#                       '(Allston)'},
#  'application fee': {'value': 'Application Fee\n$15'},
#  'available date': {'value': 'Avail Date\n09/01/2020'},
#  'baths': {'value': 'Baths\n1'},
#  'beds': {'value': 'Beds\nStudio'},
#  'building type': {'value': 'Building Type\n-'},
#  'fee paid by owner': {'value': 'Fee Paid By Owner\n1 Month'},
#  'first month': {'value': 'First Month\n$1650'},
#  'heat source': {'value': 'Heat Source\n-'},
#  'id': {'value': 'ID\n123288634'},
#  'key deposit': {'value': 'Key Deposit\n$100'},
#  'key info': {'value': 'Key / Entry Info\nKeys in Office'},
#  'landlord contact': {'value': 'Contact\n39 Lancaster Terr, Brookline MA'},
#  'landlord email': {'value': 'Email\nmgreen@finebergcompanies.com'},
#  'landlord name': {'value': 'Name\nFineberg Companies (Internal)'},
#  'landlord phone': {'value': 'Phone\n781-239-1480'},
#  'last month': {'value': 'Last Month\n$1650'},
#  'laundry': {'value': 'Laundry\nLaundry in Building'},
#  'move in fee': {'value': 'Move In Fee\n$0'},
#  'notes': {'value': 'Internal Notes\n'
#                     'Fineberg Fax (888) 231-2683\n'
#                     'As a reminder, if your client cancels a deal after their '
#                     'application has been approved by Fineberg, there will be '
#                     'a $250.00 fee that the broker/agent will be responsible '
#                     'to collect.\n'
#                     '\n'
#                     'Policies to keep in mind:\n'
#                     '· $100 Key Fee – We have increased our key fee to $100. '
#                     'It has been updated on all of our documents which are '
#                     'available on our brokers portal and YGL.\n'
#                     'full commission on all rentals!'}
        pprint.pprint(data)

        return data
