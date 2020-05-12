import sys
import re
import time
import phonenumbers
import xlsxwriter
from lxml import html

DEBUG = None 

class Entry:
    #  This object is used to store the info for an unit.
    def __init__(self, name, num, unit, tel):
        self.street_num = num 
        self.street_name = name 
        self.unit_num = unit 
        self.tel = tel
        self.additional_notes = [] 
        self.flags = []
    def flagged(self):
        return len(self.flags) != 0
    def add_flag(self, flag):
        if flag.capitalize() not in self.flags: 
            self.flags.append(flag.capitalize()) 
            if DEBUG != None:
                print ("Added [", flag,"] to entry.")
        elif DEBUG != None:
            print ("[", flag,"] not added to entry (dupe).")
    def add_note(self, note):
        if note not in self.additional_notes: 
            self.additional_notes.append(note)
            if DEBUG != None:
                print ("Added [", note,"] to entry.")
        elif DEBUG != None:
            print ("[", note,"] not added to entry (dupe).")
    def disp(self):
        print ("ST#: ", self.street_num, "\nSTN: ", self.street_name, "\nUnit: ", self.unit_num, "\nTel: ", self.tel)
        print ("Flags: ")
        for f in self.flags: 
            print ("-", f)
        print ("Notes: ")
        for n in self.additional_notes: 
            print ("-", n)

# Regular expressions used to extract the relevant info
# The address seems to be is formatted consistantly ( street num and street name, unit, zipcode city and state )
re_address = re.compile("(.*),(.*),(.*),(.*)")
# This is used to extract the street number from the address
re_num = re.compile("([a-zA-Z#\ .]*)([0-9]+)([a-zA-Z#\ .]*)")
keywords = []

def find_keyword(kw, data, entry):
    re_kw = re.compile(kw.lower())
    result = re_kw.search(data.lower())
    if result != None:
       entry.add_flag(kw) 
    if DEBUG != None:
        print ("Couldn't find '", kw, "' in '", data, "'")
    entry.add_note(data)

def add_keyword(kw):
    if kw not in keywords:
        keywords.append(kw)

def check_keywords(entry, data):
    for kw in keywords:
        find_keyword(kw, data, entry)


def generate_spreadsheet(data):
    workbook = xlsxwriter.Workbook('units.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.write('B1', 'Number', bold)
    worksheet.write('C1', 'Street', bold)
    worksheet.write('D1', 'Unit', bold)
    worksheet.write('E1', 'Phone', bold)
    worksheet.set_column(0, 0, 5)
    worksheet.set_column(1, 1, 5)
    worksheet.set_column(2, 2, 20)
    worksheet.set_column(3, 3, 5)
    worksheet.set_column(4, 7, 15)
    row = 2

    kw_color_hi = workbook.add_format()
    kw_color_hi.set_bg_color('lime')
    kw_color_hi.set_center_across()
    kw_color_lo = workbook.add_format()
    kw_color_lo.set_fg_color('#DDFFDD')

    for e in data:
        if e.flagged():
            worksheet.write(row, 0, "*", kw_color_hi)
            worksheet.write(row, 1, e.street_num, kw_color_lo)
            worksheet.write(row, 2, e.street_name, kw_color_lo)
            worksheet.write(row, 3, e.unit_num, kw_color_lo)
        else:
            worksheet.write(row, 1, e.street_num)
            worksheet.write(row, 2, e.street_name)
            worksheet.write(row, 3, e.unit_num)
        i = 0
        for n in e.tel:
            if e.flagged():
                worksheet.write(row, 4+i, n, kw_color_lo)
            else:
                worksheet.write(row, 4+i, n)
            i = i+1
        row = row+1

    worksheet.write(row+1, 0, "Key", kw_color_hi)
    col = 2
    for k in keywords:
        row = row+1
        worksheet.write(row, col, k, kw_color_lo)

    workbook.close()

def vet_nodes(tenants):
    #  Checks if the elements that have been scraped actually contains
    # the info we're looking for, aka the Tenant field.
    #  If so we add the text content in a list of numbers.
    result = []
    for p in tenants:
        if p.text == "Tenants:":
            number = p.getnext()
            number = number.text_content() + number.tail
            number = number.replace("&", "and")
            if DEBUG != None:
                print ("P: ", p.text)
                print ("N: ", number)
            result.append(number)

    return result

def parse_entry(address, number):
    #  Here we're parsing the HTML we've scraped, element by element.
    #  This returns an Entry object filled with the info from the page.
    add = parse_address(address)
    tel = parse_phone(number)
    app = Entry(add['name'], add['number'], add['unit'], tel)
    check_keywords(app, number)
    if DEBUG != None:
        app.disp()
    return app 

def parse_phone(number):
    #  Parsing phone number(s) from the tenant field and adding them
    # to a list of phone numbers for the unit.
    result = []
    if DEBUG != None:
        print ("-fetching numbers from: \"", number, "\"")
        print ("-cleaning up phone number.")
    for match in phonenumbers.PhoneNumberMatcher(number, "US"):
        result.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL))
    return result

def parse_address(address):
    #  Parses the address from the address div and returns an object
    # containing the number and name of the street, and the unit.
    old = address
    if DEBUG != None:
        print ("-stripping whitespace.")
    address = address.strip()
    if DEBUG != None:
        print ("-splitting address.")
    result = re_address.split(address)
    if DEBUG != None:
        print ("-cleaning up entry.")
    result = list(filter(None, result))
    temp_add = re_num.split(result[0])
    if DEBUG != None:
        print ("-cleaning up name.")
    temp_add = list(filter(None, temp_add))
    temp_add[0] = temp_add[0].strip()
    temp_add[1] = temp_add[1].strip()
    if DEBUG != None:
        print ("-fetching unit# from: \"", result[1], "\"")
    if DEBUG != None:
        print ("-cleaning up unit number.")
    temp_unit = result[1][1:].strip()
    #print ("Unit number ", temp_unit[1:])

    return {
            "number": temp_add[0],
            "name": temp_add[1],
            "unit": temp_unit[1:]
            }

def main():
    #  Open ./showing.html and loads it
    with open('showing.html', 'r') as myfile:
        data = myfile.read()

    tree = html.fromstring(data)
    addresses = tree.xpath('//div[@class="address"]/text()')
    pTenants = tree.xpath('//div[@class="feature_item "]/strong')
    numbers = []

#if len(addresses) != len(landlords):
#    print ("[ERROR #1] Mismatch, please contact your local JJ.")
#    sys.exit(1)

    appartments = []
    print ("Found ", len(addresses), " addresses.")
    print ("Found ", len(pTenants), " potential nodes.")
    numbers = vet_nodes(pTenants)
    print ("Found ", len(numbers), " actual tenants.\n")


    #  Iterate over all the addresses found, combines the info into
    # an object and adds it to the list of units.
    for i in range(0, len(addresses)):
        if DEBUG != None:
            print ("Procession unit#", i+1)
        app = parse_entry(addresses[i], numbers[i])
        appartments.append(app)


    print ("\nCreating Excel file.")
    generate_spreadsheet(appartments)
    return len(addresses)


print ("Starting.\n")
start_time = time.time()

#  Starting main loop
add_keyword("renewing")
add_keyword("renew")
add_keyword("do not contact")
add_keyword("works for")
add_keyword("work for")
add_keyword("employee")

address_count = main()

print ("\nProcessed ", address_count, " units in %s seconds." % (time.time() - start_time))
