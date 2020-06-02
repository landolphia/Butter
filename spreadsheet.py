import re
import sys 
import pprint 
import pandas as pd

import geohelper

TEMP_LISTING = "listing_to_post.xlsx"

re_address = re.compile("(.*),(.*),(.*),(.*)")
re_num = re.compile("([a-zA-Z#\ .]*)([0-9]+)([a-zA-Z#\ .]*)")

class Spreadsheet:
    def __init__(self, creds):
        self.data = pd.read_excel(TEMP_LISTING, sheet_name = 6)
        # This replaces empty cells with None (instead of nan)
        self.data = self.data.where(pd.notnull(self.data), None)
        self.geo = geohelper.GeoHelper(creds)

    def disp(self):
        pprint.pprint(vars(self))
    def get_key(self, key):
        return self.data.iloc[key][3]
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

        zip = self.geo.get_zip(old)
        return {
                "full": old,
                "number": temp_add[0],
                "name": temp_add[1],
                "unit": temp_unit[1:],
                "city": result[2],
                "state": result[3],
                "zip": zip
                }    
#    def NY_to_bool(self, key):
#        return True if self.get_key(key) == 'Y' else False 
#    def format_rent_data(self):
#        self.building_type = self.get_key("building type")
#        self.multiple_floorplans = self.NY_to_bool("multiple floorplans")
#        self.req_broker_fee = self.NY_to_bool("broker")
#        self.req_first_month = self.NY_to_bool("first")
#        self.req_last_month = self.NY_to_bool("last")
#        self.req_upfront_costs = self.NY_to_bool("upfront")
#        self.req_references = self.NY_to_bool("references")
#        self.req_security_deposit = self.NY_to_bool("security")
#
#        return True
#    def format_amenities_features(self):
#        self.ac = self.NY_to_bool("ac")
#        self.carpet = self.NY_to_bool("carpet")
#        self.carpet = True
#        self.dining_room = self.NY_to_bool("dining room")
#        self.disability_access = self.NY_to_bool("disability access")
#        self.dishwasher = self.NY_to_bool("dishwasher")
#        self.fireplace = self.NY_to_bool("fireplace")
#        self.furnished = self.NY_to_bool("furnished")
#        self.furnished = True
#        self.garbage_disposal = self.NY_to_bool("garbage disposal")
#        self.hardwood_floors = self.NY_to_bool("hardwood floors")
#        self.high_speed_internet = self.NY_to_bool("high-speed internet")
#        self.living_room = self.NY_to_bool("living room")
#        self.microwave = self.NY_to_bool("microwave")
#        self.microwave = True
#        self.patio = self.NY_to_bool("patio")
#        self.private_garden = self.NY_to_bool("private garden")
#        self.shared_garden = self.NY_to_bool("shared garden")
#        self.smoke_free = self.NY_to_bool("smoke free")
#        self.storage_additional = self.NY_to_bool("storage additional")
#        self.storage_included = self.NY_to_bool("storage included")
#        self.study = self.NY_to_bool("study")
#
#        return True
#    def format_amenities_community(self):
#        self.fitness_room = self.NY_to_bool("fitness room")
#        self.individual_leases = self.NY_to_bool("individual leases")
#        self.individual_leases = True
#        self.near_bus_stop = self.NY_to_bool("near bus stop")
#        self.near_T_stop = self.NY_to_bool("near T stop")
#        self.pool = self.NY_to_bool("pool")
#        self.pool = True
#        self.roommate_matching = self.NY_to_bool("roommate matching")
#        self.tennis_court = self.NY_to_bool("tennis court")
#
#        return True
#    def format_amenities_agency(self):
#        self.fee_agent_broker = self.NY_to_bool("fee agent broker") 
#        self.fee_agent_broker = True
#        self.no_fee = self.NY_to_bool("no fee") 
#
#        return True
#    def format_amenities_lease(self):
#        self.twelve_months = self.NY_to_bool("12 months")
#        self.nine_months = self.NY_to_bool("9 months")
#        self.fall_sublet = self.NY_to_bool("fall sublet")
#        self.flexible = self.NY_to_bool("flexible")
#        self.flexible = True
#        self.month_to_month = self.NY_to_bool("month to month")
#        self.short_term = self.NY_to_bool("short term")
#        self.spring_sublet = self.NY_to_bool("spring sublet")
#        self.spring_sublet = True
#        self.summer_sublet = self.NY_to_bool("summer sublet")
#        
#        return True
#    def format_amenities_security(self):
#        self.courtesy_officer = self.NY_to_bool("courtesy officer")
#        self.dead_bolt = self.NY_to_bool("dead-bolt")
#        self.exterior_lighting = self.NY_to_bool("exterior lighting")
#        self.exterior_lighting = True
#        self.intercom = self.NY_to_bool("intercom")
#        self.security_guard = self.NY_to_bool("security guard")
#        self.security_system = self.NY_to_bool("security system")
#        self.security_system = True
#        self.video_surveillance = self.NY_to_bool("video surveillance")
#
#        return True
#    def format_amenities_utilities(self):
#        self.cable = self.NY_to_bool("cable")
#        self.electricity = self.NY_to_bool("electricity")
#        self.gas = self.NY_to_bool("gas")
#        self.gas = True
#        self.heat = self.NY_to_bool("heat")
#        self.high_speed_internet = self.NY_to_bool("high speed internet")
#        self.hot_water = self.NY_to_bool("hot water")
#        self.local_phone = self.NY_to_bool("local phone")
#        self.recycling = self.NY_to_bool("recycling")
#        self.recycling = True
#        self.trash_removal = self.NY_to_bool("trash removal")
#        self.water_sewer = self.NY_to_bool("water sewer")
#
#        return True
#    def format_amenities_parking(self):
#        self.garage_parking = self.NY_to_bool("garage parking")
#        self.no_parking = self.NY_to_bool("no parking")
#        self.no_parking = True
#        self.off_street_parking = self.NY_to_bool("off street parking")
#        self.on_street_parking = self.NY_to_bool("on street parking")
#
#        return True
#    def format_amenities_laundry(self):
#        self.laundry_room_in_community = self.NY_to_bool("laundry room in community")
#        self.no_laundry_in_unit = self.NY_to_bool("no laundry in unit")
#        self.no_laundry_in_unit = True
#        self.washer_dryer_hookups = self.NY_to_bool("washer dryer hookups")
#        self.washer_dryer_in_unit = self.NY_to_bool("washer dryer in unit")
#
#        return True
#    def format_amenities_description(self):
#        self.description = self.get_key("description")
#
#        return True
#    def format_amenities_data(self):
#        self.pet_policy = self.get_key("pet policy")
#        if self.DEBUG != None: print("Fix the pet policy!!!!!!!!\n!!!!!!!!!!!!!!!!!!!!!!!!!!")
#        self.lead_paint = self.get_key("lead paint")
#
#        self.format_amenities_features()
#        self.format_amenities_agency()
#        self.format_amenities_community()
#        self.format_amenities_lease()
#        self.format_amenities_security()
#        self.format_amenities_utilities()
#        self.format_amenities_parking()
#        self.format_amenities_laundry()
#        self.format_amenities_description()
#
#        return True
#    def format_specifics_data(self):
#        self.number_of_occupants = self.get_key("number of occupants")
#        self.availability_date = self.get_key("availability date")
#        self.allow_subletting = self.NY_to_bool("allow subletting")
#        self.is_sublet = self.NY_to_bool("is sublet")
#        self.roommate_situation = self.NY_to_bool("roommate situation")
#        self.availability_renew = self.get_key("availability renew") # Because this can be unknown
#
#        return True
#    def format_location_data(self):
#        address = self.get_key("actual address")
#
#        self.set_address(address)
#
#        self.display_exact_address = self.NY_to_bool("display exact address")
#
#        self.property_name = self.get_key("property name")
#        print("This is the property name: ", self.property_name)
#        if self.property_name == None:
#            print("No property name found, using address.")
#            self.property_name = "[JJ's testing supplies]" + self.full_address
#
#        return True
#    def get_listing_data(self):
#        if self.DEBUG != None:
#            for key in self.index:
#                print (key + ": \t\t", self.get_key(key))
#
#        self.format_location_data()
#        self.format_rent_data()
#        print("FIX ME!!!!!!!!!!!!!!!!!!!!!!!\n Should take care of floorplan details here.")
#        self.format_specifics_data()
#        self.format_amenities_data()
#        
#        self.disp_location()
#        self.disp_rent()
#        self.disp_specifics()
#        self.disp_amenities()
#
#        self.disp()
#
#        return self
#    def set_address(self, address):
#        address = self.parse_address(address)
#        self.full_address = address["full"]
#        self.street_num = address["number"]
#        self.street_name = address["name"]
#        self.unit = address["unit"]
#        self.city = address["city"]
#        self.state = address["state"] 
#
#        if self.DEBUG != None:
#            print("Getting postal code.")
#        self.zip = self.geo.get_zip(self.full_address)
#
#    def parse_address(self, address):
#        old = address
#        if self.DEBUG != None:
#            print ("Stripping whitespace.")
#        address = address.strip()
#        if self.DEBUG != None:
#            print ("Splitting address.")
#        result = re_address.split(address)
#        if self.DEBUG != None:
#            print ("Cleaning up entry.")
#        result = list(filter(None, result))
#        temp_add = re_num.split(result[0])
#        if self.DEBUG != None:
#            print ("Cleaning up name.")
#        temp_add = list(filter(None, temp_add))
#        temp_add[0] = temp_add[0].strip()
#        temp_add[1] = temp_add[1].strip()
#        if self.DEBUG != None:
#            print ("Fetching unit# from: \"", result[1], "\"")
#        if self.DEBUG != None:
#            print ("Cleaning up unit number.")
#        temp_unit = result[1][1:].strip()
#
#        return {
#                "full": old,
#                "number": temp_add[0],
#                "name": temp_add[1],
#                "unit": temp_unit[1:],
#                "city": result[2],
#                "state": result[3]
#                }    
