import json
import logging
import os
import re
import sys

import credentials
import geohelper
import dom
import payload
import spreadsheet


OFFLINE_CACHE = "./scrape/offline_data.json"
LEADS_IDS = "./scrape/leads.json"
UN_OFFLINE_CACHE = "./unleaded/offline_data.json"
UN_LEADS_IDS = "./unleaded/leads.json"

class Navigator:
    def __init__(self, offline, mode):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Navigator.")

        self.pl = payload.Payload(mode)

        if self.pl.mode == "SCRAPE":
            if offline:
                self.units = self.__get_offline_data__(OFFLINE_CACHE, self.pl.mode)
            else:
                self.dom = dom.DOM()
                self.units = self.__init_scraper__()

            self.log.debug("Saving data to cache file.")
            with open(OFFLINE_CACHE, 'w') as f:
                json.dump(self.units, f) 

            spreadsheet.Spreadsheet(output=self.units)
        elif self.pl.mode == "POST":
            self.log.debug("Fix availability for mfps for new template.")
            #sys.exit()
            self.dom = dom.DOM()
            self.__init_poster__()
        elif self.pl.mode == "UNLEADED":
            if offline:
                self.units = self.__get_offline_data__(UN_OFFLINE_CACHE, self.pl.mode)
            else:
                self.dom = dom.DOM()
                self.units = self.__init_unleader__()

                self.log.debug("Saving data to cache file.")
                with open(UN_OFFLINE_CACHE, 'w') as f:
                    json.dump(self.units, f) 

            results = self.__check_unleaded_database__()

            spreadsheet.Spreadsheet(lead=results)
        else:
            self.log.error("[" + self.pl.mode + "] is not a valid mode.")
            sys.exit()
    # SCRAPER
    def __get_leads__(self, leads):
        self.leads = []

        if not os.path.isfile(leads):
            self.log.error("Couldn't find the leads ids file. [" + leads + "].")
            sys.exit()

        with open(leads, 'r') as f:
            self.leads = json.load(f)
        
        self.log.warning("Leads = " + str(self.leads))
    def __get_offline_data__(self, cache, mode):
        if not os.path.isfile(cache):
            self.log.warning("Offline cache file doesn't exist. Downloading data to file.")
            self.dom = dom.DOM()
            if mode == "SCRAPE":
                return self.__init_scraper__()
            elif mode == "UNLEADED":
                return self.__init_unleader__()
            else:
                self.log.error("Invalid mode [" + str(mode) + "]")
                sys.exit()
        else:
            self.log.info("Loading data from offline cache.")
            with open(cache) as f:
                return json.load(f)
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
        self.log.info(str(i) + " unit" + ("s" if i>1 else "") + " scraped.")

        return units
    # POSTER
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
    # UNLEADER
    def __init_unleader__(self):
        self.log.info("Initializing unleader.")
        self.__get_leads__(UN_LEADS_IDS)

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
        self.log.info(str(i) + " unit" + ("s" if i>1 else "") + " scraped.")

        self.log.info("THIS : " + str(units))
        return units
    def __get_addresses__(self):
        #g_key = credentials.Credentials().get_credentials("private.slr")["api_key"]
        #self.geo = geohelper.GeoHelper(g_key)

        #self.addresses = []
        #for leads in self.units:
        #    self.log.debug("Lead = " + str(leads))
        #    for u in self.units[leads]:
        #        self.log.debug("Unit = " + str(u))
        #        if ("On Market" in u):
        #            self.addresses.append(self.geo.get_street_city_and_unit(u["On Market"]))
        #        elif ("Off Market" in u):
        #            self.addresses.append(self.geo.get_street_city_and_unit(u["Off Market"]))
        #        elif ("Pending" in u):
        #            self.addresses.append(self.geo.get_street_city_and_unit(u["Pending"]))
        #        else:
        #            self.log.warning("No address in this unit.")
        #            self.log.warning(str(u))

        ## Checking for duplicate entries
        #i = 0
        #temp = []
        #for a in self.addresses:
        #    self.log.info("Address #" + str(i) + " = " + str(a))
        #    i = i + 1
        #    if not a in temp:
        #        temp.append(a)
        #        self.log.debug("Adding address")
        #    else:
        #        self.log.debug("Skipping dupe")

        #self.addresses = temp

        #self.log.debug("Saving data to cache file.")
        #with open("./unleaded/offline_addresses.json", 'w') as f:
        #    json.dump(self.addresses, f) 

        #input("Saved")
        with open("./unleaded/offline_addresses.json") as f:
            self.addresses = json.load(f)
    def __check_unleaded_database__(self):
        #self.__get_addresses__()

        #if not hasattr(self, "dom"):
        #    self.dom = dom.DOM()
       
        #self.pl = payload.Payload("unleaded", "unleaded")

        #results = []
        #for a in self.addresses:
        #    self.dom.go("https://eohhs.ehs.state.ma.us/leadsafehomes/default.aspx")
        #    self.pl.trigger["dropdown"]["get result"] = a["city"]
        #    self.pl.trigger["street"]["get result"] = a["street"]
        #    self.pl.trigger["number"]["get result"] = a["number"]
        #    self.pl.trigger["unit_link"]["get result"] = a["unit"]
        #    self.log.debug("Address = " + str(a))
        #    if (a["city"] != None) and (a["street"] != None) and (a["number"] != None):
        #        self.dom.process_actions(self.pl.trigger["street"])
        #        self.dom.process_actions(self.pl.trigger["number"])
        #        self.dom.process_actions(self.pl.trigger["dropdown"])
        #        self.dom.process_actions(self.pl.trigger["button"])
        #        rows = self.dom.process_actions(self.pl.trigger["no_result"])
        #        if rows != "No records are found. Please try another combination.":
        #            self.log.debug("Trying to find unit #" + str(self.pl.trigger["unit_link"]["get result"]))
        #            if self.dom.process_actions(self.pl.trigger["unit_link"]) == True:
        #                rows = self.dom.process_actions(self.pl.trigger["result"])
        #            else:
        #                rows = ["No information found for this unit."]
        #        else:
        #            rows = [rows]
        #    else:
        #        rows = ["Invalid address. Skipped."]
        #    self.log.debug("Rows = " + str(rows))
        #    results.append({
        #            "address" : a,
        #            "rows" : rows 
        #            })

        #self.log.debug("Saving data to cache file.")
        #with open("./unleaded/offline_results.json", 'w') as f:
        #    json.dump(results, f) 

        #input("Saved")
        with open("./unleaded/offline_results.json") as f:
            results = json.load(f)

        #for r in results:
        #    self.log.debug("Rows for [" + str(r["address"]) + "]")
        #    for row in r["rows"]:
        #        self.log.debug("-> [" + str(row) + "]")
        return results
