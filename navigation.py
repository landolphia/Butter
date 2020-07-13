#import os
#import pyautogui
#import time
#import sys

import json
import logging
import os
import sys

import dom
import payload
import spreadsheet


OFFLINE_CACHE = "offline_data.json"
LEADS_IDS = "leads.json"

class Navigator:
    def __init__(self, offline):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Navigator.")
            
        self.pl = payload.Payload()

        if self.pl.mode == "SCRAPE":
            if offline:
                self.units = self.__get_offline_data__()
            else:
                self.dom = dom.DOM()
                self.units = self.__init_scraper__()

            self.log.debug("Saving data to cache file.")
            with open(OFFLINE_CACHE, 'w') as f:
                json.dump(self.units, f) 

            #TODO FIXME scrape vs post?
            spreadsheet.Spreadsheet(output=self.units)
        elif self.pl.mode == "POST":
            self.dom = dom.DOM()
            self.__init_poster__()
        else:
            self.log.error("[" + self.pl.mode + "] is not a valid mode.")
            sys.exit()
    # SCRAPER
    def __get_leads__(self, f):
        self.leads = []

        if not os.path.isfile(LEADS_IDS):
            self.log.error("Couldn't find the leads ids file. [" + LEADS_IDS + "].")
            sys.exit()

        with open(LEADS_IDS, 'r') as f:
            self.leads = json.load(f)
        
        self.log.warning("This is the leads: " + str(self.leads))
    def __get_offline_data__(self):
        if not os.path.isfile(OFFLINE_CACHE):
            self.log.warning("Offline cache file doesn't exist. Downloading data to file.")
            self.dom = dom.DOM()
            return self.__init_scraper__()
        else:
            self.log.info("Loading data from offline cache.")
            with open(OFFLINE_CACHE) as f:
                return json.load(f)
    def __get_rentals_list__(self, identifier):
        self.log.error("Pick up here.")
        self.log.warnign("START BY CONVERTION payload.json to new format FULLY")
        #DECIDE HOW THE FLOW GOES
        #DO I HAVE PASSIVE ACTIONS VS ACTIVE (AUTO TRIGGER?)
        #HOW DO I DEFINE THE FLOW?

        sys.exit()
        unit_flow = self.pl["unit"]
    def __init_scraper__(self):
        self.log.debug("Initializing Scraper.")

        self.__get_leads__(LEADS_IDS)

        # Process run once 
        for p in self.pl.run_once:
            self.log.debug("Run once : " + str(p))
            for e in self.pl.run_once[p]:
                self.dom.process_actions(e)

        # Process repeat
        unit_ids = {}
        for l in self.leads:
            self.log.debug("Processing leads #" + str(l))
            for e in self.pl.repeat["leads"]:
                unit_ids[str(l)] = self.dom.process_actions(e, identifier=l)

        # Loop units for each leads id
        units = {}
        for l in self.leads:
            units[str(l)] = []
            for u in unit_ids[str(l)]:
                unit = {}
                for e in self.pl.repeat["unit"]:
                    result = self.dom.process_actions(e, identifier=u)
                    if "fluff" in e:
                        unit[e["fluff"].strip()] = result
                units[str(l)].append(unit)

        for l in self.leads:
            self.log.warning("L: " + str(l))
            for u in units[str(l)]:
                self.log.warning("Us: " + str(u))
        input("Patcha")

        return units
    # POSTER
    def __init_poster__(self):
        self.log.debug("Initializing Poster.")

        #TODO extract tasks to module?
        self.tasks = []

        # Process run once 
        for p in self.pl.run_once:
            self.log.debug("Run once : " + str(p))
            for e in self.pl.run_once[p]:
                self.dom.process_actions(e)
#    def add_task(self, task):
#        self.log.debug(task)
#        self.tasks.append(task)
#    def start(self):
#        self.login()
#        self.add_listing()
#        self.fill_address()
#        self.fill_rent()
#        self.fill_amenities()
#        self.fill_contact()
#        self.fill_photos()
#    def close(self):
#        self.elements.quit()
#    def login(self):
#        self.elements.go("login", "login url")
#
#        self.elements.wait("login", "link")
#        self.elements.click("login", "link")
#
#        self.elements.wait("login", "username")
#        
#        self.elements.fill_input("login", "username")
#        self.elements.fill_input("login", "password")
#
#        self.elements.click("login", "submit button")
#    def add_listing(self):
#        self.elements.go("login", "add listing url")
#
#        self.elements.wait("location", "full address")
#
#        self.elements.fill_input("location", "full address input")
#        self.elements.press_enter("location", "full address input")
#    def fill_address(self):
#        self.elements.wait("location", "address")
#
#        self.log.debug("Filling in address details for [" + self.payload.get_value("location", "full address") + "].")
#   
#        self.elements.fill_input("location", "address")
#        self.elements.fill_input("location", "city")
#        self.elements.fill_input("location", "zip")
#    
#        self.elements.dropdown("location", "state")
#
#        self.elements.checkbox("location", "exact flag")
#
#
#        self.elements.submit("location", "address form")
#
#        self.elements.wait("location", "property name")
#
#        self.elements.fill_input_not_null("location", "property name", "[TEST]") #FIXME Fix this before release
#        self.elements.press_enter("location", "property name")
#    def fill_rent(self):
#        self.elements.wait("rent", "rent link")
#        self.elements.click("rent", "rent link")
#
#        self.elements.dropdown("rent", "building type")
#
#        if self.payload.get_bool("rent", "floorplans yes"):
#            self.elements.radio("rent", "floorplans yes")
#        else:
#            self.elements.radio("rent", "floorplans no")
#
#        self.elements.checkbox("rent", "broker")
#        self.elements.checkbox("rent", "first")
#        self.elements.checkbox("rent", "last")
#        self.elements.checkbox("rent", "upfront")
#        self.elements.checkbox("rent", "references")
#        self.elements.checkbox("rent", "security")
#
#        self.elements.fill_input_not_null("rent", "specials", " ")
#        self.elements.press_enter("rent", "specials")
#
#        if self.payload.get_bool("rent", "floorplans yes"):
#            self.fill_floorplans()
#            self.fill_specifics(True)
#        else:
#            self.fill_floorplan()
#            self.fill_specifics(False)
#    def fill_floorplan(self):
#        self.elements.wait("rent", "bedrooms")
#        
#        self.elements.dropdown("rent", "bedrooms")
#        self.elements.dropdown("rent", "bathrooms")
#
#        self.elements.fill_input("rent", "square feet")
#        self.elements.fill_input_money("rent", "monthly rent")
#
#        self.elements.dropdown("rent", "type")
#
#        self.elements.press_enter("rent", "specials")
#    def fill_floorplans(self):
#        i = 0
#        fp_number = self.payload.get_value("floorplans", "total number")
#
#        while i < fp_number:
#            # FIXME Should click edit instead of add for the first floorplan
#            # I can probably find the element with some kind of sibling logic
#            self.elements.wait("floorplans", "link")
#            self.elements.click("floorplans", "link")
#
#            self.elements.wait("floorplans", "add link")
#            self.elements.click("floorplans", "add link")
#
#            url = str(self.elements.current_url())
#            fp_id = url.rsplit('/', 1)[-1]
#            self.log.debug("Filling floorplan #" + str(i) + " [ID=" + str(fp_id) + "]")
#
#            self.elements.fill_input_fp("floorplans", "name", i, fp_id)
#            self.elements.fill_input_fp("floorplans", "specials", i, fp_id)
#
#            self.elements.dropdown_fp("floorplans", "bedrooms", i, fp_id)
#            self.elements.dropdown_fp("floorplans", "bathrooms", i, fp_id)
#            self.elements.dropdown_fp("floorplans", "occupants", i, fp_id)
#
#            self.elements.fill_input_fp("floorplans", "square feet", i, fp_id)
#            self.elements.fill_input_money_fp("floorplans", "monthly rent", i, fp_id)
#
#            self.elements.dropdown_fp("floorplans", "rental type", i, fp_id)
#            self.elements.dropdown_fp("floorplans", "occupants", i, fp_id)
#
#            self.elements.checkbox_fp("floorplans", "ac", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "carpet", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "dining room", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "disability access", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "dishwasher", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "fireplace", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "furnished", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "garbage disposal", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "hardwood", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "high-speed internet", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "living room", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "microwave", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "patio", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "private garden", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "shared garden", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "smoke free", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "additional storage", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "included storage", i, fp_id)
#            self.elements.checkbox_fp("floorplans", "study", i, fp_id)
#
#            # Floorplans/Availability
#            self.elements.radio_fp("floorplans", "availability not", i, fp_id)
#            self.elements.radio_fp("floorplans", "availability ongoing", i, fp_id)
#
#            if self.elements.radio_fp("floorplans", "availability specific", i, fp_id):
#                self.elements.fill_input_date_fp("floorplans", "start date", i, fp_id)
#
#            if self.elements.radio_fp("floorplans", "availability range", i, fp_id):
#                self.elements.fill_input_date_fp("floorplans", "start date", i, fp_id)
#                self.elements.fill_input_date_fp("floorplans", "end date", i, fp_id)
#
#            # Floorplans/Description++
#
#            self.elements.fill_input_fp("floorplans", "description", i, fp_id)
#            self.elements.fill_input_fp("floorplans", "virtual tour", i, fp_id)
#            self.elements.fill_input_fp("floorplans", "webpage", i, fp_id)
#            self.elements.fill_input_fp("floorplans", "lease", i, fp_id)
#
#            self.add_task("If the specific floorplan [" + str(fp_id) + "] has a photo you need to add it manually.")
#            #self.send_keys_fp_by_id("floorplans", "image")
#
#            self.elements.submit_fp("floorplans", "name", i, fp_id)
#
#            i = i + 1
#    def fill_specifics(self, fp):
#        self.elements.wait("specifics", "link")
#        self.elements.click("specifics", "link")
#
#        if not fp:
#            self.elements.dropdown("specifics", "max occupants")
#
#        self.elements.checkbox("specifics", "allow sublet")
#        self.elements.checkbox("specifics", "is sublet")
#        self.elements.checkbox("specifics", "roommate situation")
#
#        self.elements.radio("specifics", "available ongoing")
#
#        if self.elements.radio("specifics", "available date") != None:
#            self.elements.fill_input_date("specifics", "start date")
#
#        if self.elements.radio("specifics", "available range") != None:
#            self.elements.fill_input_date("specifics", "start date")
#            self.elements.fill_input_date("specifics", "end date")
#
#        self.elements.radio("specifics", "renew yes")
#        self.elements.submit("specifics", "renew yes")
#    def fill_amenities(self):
#        self.elements.wait("amenities", "link")
#        self.elements.click("amenities", "link")
#
#        self.elements.dropdown("amenities", "pet policy")
#        self.elements.checkbox("amenities", "cats")
#        self.elements.checkbox("amenities", "dogs")
#
#        self.elements.dropdown("amenities", "lead paint")
#    
#        # Features
#        self.elements.checkbox("amenities", "ac")
#        self.elements.checkbox("amenities", "carpet")
#        self.elements.checkbox("amenities", "dining room")
#        self.elements.checkbox("amenities", "disability access")
#        self.elements.checkbox("amenities", "dishwasher")
#        self.elements.checkbox("amenities", "fireplace")
#        self.elements.checkbox("amenities", "furnished")
#        self.elements.checkbox("amenities", "garbage disposal")
#        self.elements.checkbox("amenities", "hardwood")
#        self.elements.checkbox("amenities", "internet")
#        self.elements.checkbox("amenities", "living room")
#        self.elements.checkbox("amenities", "microwave")
#        self.elements.checkbox("amenities", "patio")
#        self.elements.checkbox("amenities", "private garden")
#        self.elements.checkbox("amenities", "shared garden")
#        self.elements.checkbox("amenities", "smoke free")
#        self.elements.checkbox("amenities", "additional storage")
#        self.elements.checkbox("amenities", "included storage")
#        self.elements.checkbox("amenities", "study")
#        #Agency
#        self.elements.checkbox("amenities", "agent fee")
#        self.elements.checkbox("amenities", "no fee")
#        # Community
#        self.elements.checkbox("amenities", "fitness room")
#        self.elements.checkbox("amenities", "individual leases")
#        self.elements.checkbox("amenities", "near bus")
#        self.elements.checkbox("amenities", "near T")
#        self.elements.checkbox("amenities", "pool")
#        self.elements.checkbox("amenities", "roommate matching")
#        self.elements.checkbox("amenities", "tennis court")
#        # Lease
#        self.elements.checkbox("amenities", "12 months")
#        self.elements.checkbox("amenities", "9 months")
#        self.elements.checkbox("amenities", "fall sublet")
#        self.elements.checkbox("amenities", "flexible lease")
#        self.elements.checkbox("amenities", "month to month")
#        self.elements.checkbox("amenities", "short term lease")
#        self.elements.checkbox("amenities", "spring sublet")
#        self.elements.checkbox("amenities", "summer sublet")
#        # Security
#        self.elements.checkbox("amenities", "courtesy officer")
#        self.elements.checkbox("amenities", "dead bolt")
#        self.elements.checkbox("amenities", "exterior light")
#        self.elements.checkbox("amenities", "intercom")
#        self.elements.checkbox("amenities", "security guard")
#        self.elements.checkbox("amenities", "security system")
#        self.elements.checkbox("amenities", "video surveillance")
#        # Utilities
#        self.elements.checkbox("amenities", "cable")
#        self.elements.checkbox("amenities", "electricity")
#        self.elements.checkbox("amenities", "gas")
#        self.elements.checkbox("amenities", "heat")
#        self.elements.checkbox("amenities", "high-speed internet")
#        self.elements.checkbox("amenities", "hot water")
#        self.elements.checkbox("amenities", "local phone")
#        self.elements.checkbox("amenities", "recycling")
#        self.elements.checkbox("amenities", "trash")
#        self.elements.checkbox("amenities", "water")
#        # Parking
#        self.elements.checkbox("amenities", "garage")
#        self.elements.checkbox("amenities", "no parking")
#        self.elements.checkbox("amenities", "off street parking")
#        self.elements.checkbox("amenities", "on street parking")
#        # Laundry
#        self.elements.checkbox("amenities", "laundry room")
#        self.elements.checkbox("amenities", "no laundry")
#        self.elements.checkbox("amenities", "wd hookups")
#        self.elements.checkbox("amenities", "wd in unit")
#        # Description
#        self.elements.tinyMCE("amenities", "description", "amenities", "tinymce")
#        self.elements.submit("amenities", "wd in unit")
#    def fill_contact(self):
#        self.add_task("The contact page needs to be filled manually.")
#        #self.elements.wait("contact", "link")
#        #self.elements.click("contact", "link")
#
#        #self.elements.wait("contact", "name")
#        #self.elements.fill_input("contact", "name")
#        #self.elements.fill_input("contact", "phone")
#        #self.elements.fill_input("contact", "text")
#
#        #self.elements.click("contact", "email arrow")
#        #self.elements.fill_input("contact", "email")
#
#        #self.elements.fill_input("contact", "office hours")
#        #self.elements.fill_input("contact", "twitter")
#        #self.elements.fill_input("contact", "facebook")
#        #self.elements.fill_input("contact", "instagram")
#        #self.elements.fill_input("contact", "website")
#
#        #TODO
#        #self.elements.fill_input("contact", "lease link")
#        #self.elements.fill_input("contact", "lease button")
#    def fill_photos(self):
#        #TODO dropdown image type
#        #TODO input description
#        self.add_task("The photos' descriptions and types need to be entered manually.")
#
#        photos = []
#        for root, dirs, files in os.walk("./images/"):
#            for f in files:
#                if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".gif") or f.endswith(".png"):
#                    path = os.path.join(root, f)
#                    self.log.debug("Photo found. [" + path + "]")
#                    photos.append(path)
#
#        self.elements.wait("photos", "link")
#        self.elements.click("photos", "link")
#
#        uploads = 0
#        for i in range(len(photos)):
#            path = os.path.abspath(photos[i])
#            self.log.debug("Uploading file #" + str(i) + " [" + photos[i] + "] [" + path + "]")
#
#            self.elements.wait("photos", "uploader")
#            self.elements.click("photos", "uploader")
#
#            if os.path.isfile(photos[i]):
#                time.sleep(1)
#                pyautogui.write(path, interval=0.075)
#                pyautogui.press('enter')
#                self.elements.wait_for_new_list_element("photos", "li", uploads)
#                uploads = uploads + 1
#            else:
#                self.log.error("The file [" + path + "] doesn't exist.")
#                sys.exit()
#    def task_list(self):
#        self.elements.task_list(self.tasks)
