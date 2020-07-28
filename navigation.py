import json
import logging
import os
import sys

import dom
import payload


OFFLINE_CACHE = "./scrape/offline_data.json"
LEADS_IDS = "./scrape/leads.json"

class Navigator:
    def __init__(self, offline, mode, test):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Navigator.")

        self.pl = payload.Payload(mode, test)

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
            print("Posting has been disabled in this version.")
            sys.exit()
            self.dom = dom.DOM()
            self.__init_poster__()
        elif self.pl.mode == "POST_TEST":
            self.dom = dom.DOM()
            self.__init_poster_test__()
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

        return units
    # POSTER TEST
    def __get_sites__(self):
        return [
                #{
                #    "login" : "https://offcampus.bu.edu/login/",
                #    "add listing" : "https://offcampus.bu.edu/user/add-listing/"
                #},
                #{
                #    "login" : "https://offcampushousing.bc.edu/login/",
                #    "add listing" : "https://offcampushousing.bc.edu/user/add-listing/"
                #},
                #{
                #    "login" : "https://offcampus.massart.edu/login/",
                #    "add listing" : "https://offcampus.massart.edu/user/add-listing/"
                #},
                #{
                #    "login" : "https://www.harvardhousingoffcampus.com/login/",
                #    "add listing" : "https://www.harvardhousingoffcampus.com/user/add-listing/"
                #},
                {
                    "login" : "https://offcampushousing.suffolk.edu/login/",
                    "add listing" : "https://offcampushousing.suffolk.edu/user/add-listing/"
                }
        ]

    def __init_poster_test__(self):
        self.log.debug("Initializing Poster.")

        #TODO extract tasks to module?
        self.sites = self.__get_sites__()

        # Process run once 
        self.log.warning("Move everything but FPs into run once.")
        for s in self.sites:
            self.tasks = []
            self.dom.go(s["login"])
            for p in self.pl.run_once:
                if p == "add listing": self.dom.go(s["add listing"])
                if p in ["login", "location", "address", "rent", "specifics", "amenities", "contact", "photos"]:
                    self.log.debug("Run once : " + str(p))
                    for e in self.pl.run_once[p]:
                        self.dom.process_actions(e)

            self.add_task("TODO searchable neighborhoods")
            self.log.warning("Add date parsing.")
            self.log.warning("Email addresses and urls will be removed from the description, leading to the amenities maybe not saving.")
            self.log.warning("Check cells' #s after  amenities.")
            self.log.warning("Go through sites according to spreadsheet cells")
            self.add_task("Lease needs to be filled in manually in contact page.")
            self.add_task("The photos' descriptions and types need to be entered manually.")

            i = 0
            self.log.debug("Found " + str(self.dom.fp_number) + " floorplans")
            while i < self.dom.fp_number:
                for p in self.pl.repeat:
                    self.log.warning("Floorplan #" + str(i))
                    for e in self.pl.repeat[p]:
                        self.dom.process_actions(e, iteration = i)
                i = i + 1


            #self.task_list()
            input("One site down.")
    def add_task(self, task):
        self.log.debug(task)
        self.tasks.append(task)
    def task_list(self):
        self.dom.task_list(self.tasks)

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

#/FLOORPLANS
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
