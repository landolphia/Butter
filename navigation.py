import json
import logging
import os
import sys

import dom
import payload
import spreadsheet


OFFLINE_CACHE = "./scrape/offline_data.json"
LEADS_IDS = "./scrape/leads.json"

class Navigator:
    def __init__(self, offline, mode):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Navigator.")

        self.pl = payload.Payload(mode)

        if self.pl.mode == "SCRAPE":
            if offline:
                self.units = self.__get_offline_data__()
            else:
                self.dom = dom.DOM()
                self.units = self.__init_scraper__()

            self.log.debug("Saving data to cache file.")
            with open(OFFLINE_CACHE, 'w') as f:
                json.dump(self.units, f) 

            spreadsheet.Spreadsheet(output=self.units)
        elif self.pl.mode == "POST":
            self.log.debug("Fix availability for mfps for new template.")
            sys.exit()
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
        
        self.log.warning("Leads = " + str(self.leads))
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
        self.log.warning("START BY CONVERTION payload.json to new format FULLY")
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
        i = 0
        for l in self.leads:
            units[str(l)] = []
            for u in unit_ids[str(l)]:
                unit = {}
                i = i + 1
                for e in self.pl.repeat["unit"]:
                    result = self.dom.process_actions(e, identifier=u)
                    if "fluff" in e:
                        unit[e["fluff"].strip()] = result
                units[str(l)].append(unit)
        self.log.info(str(i) + "unit" + ("s" if i>1 else "") + " scraped.")

        return units
    # POSTER
    def __get_sites__(self):
        return [
                #{
                #    "login" : "https://offcampus.bu.edu/login/",
                #    "add listing" : "https://offcampus.bu.edu/user/add-listing/"
                #},
                {
                    "login" : "https://offcampushousing.bc.edu/login/",
                    "add listing" : "https://offcampushousing.bc.edu/user/add-listing/"
                },
                #{
                #    "login" : "https://offcampus.massart.edu/login/",
                #    "add listing" : "https://offcampus.massart.edu/user/add-listing/"
                #},
                #{
                #    "login" : "https://www.harvardhousingoffcampus.com/login/",
                #    "add listing" : "https://www.harvardhousingoffcampus.com/user/add-listing/"
                #},
                #{
                #    "login" : "https://offcampushousing.suffolk.edu/login/",
                #    "add listing" : "https://offcampushousing.suffolk.edu/user/add-listing/"
                #}
        ]

    def __init_poster__(self):
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
                if p in ["login", "location", "address", "neighborhoods", "rent", "specifics", "amenities", "contact", "photos"]:
                    self.log.debug("Run once : " + str(p))
                    for e in self.pl.run_once[p]:
                        self.dom.process_actions(e)

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


            self.task_list()
            input("One site down.")
    def add_task(self, task):
        self.log.debug(task)
        self.tasks.append(task)
    def task_list(self):
        self.dom.task_list(self.tasks)
