import re
import sys 
import pprint 
import pandas as pd

import geohelper

TEMP_LISTING = "listing_to_post.xlsx"

re_address = re.compile("(.*),(.*),(.*),(.*)")
re_num = re.compile("([a-zA-Z#\ .]*)([0-9]+)([a-zA-Z#\ .]*)")

class Spreadsheet:
    #  This object is used to store the info for an unit.
    def __init__(self, debug, creds):
        self.DEBUG = debug
        # Page 1 and 2
        self.full_address = None
        self.street_num = None
        self.street_name = None
        self.unit = None
        self.city = None
        self.state = None
        self.zip = None
        self.display_exact_address = None
        # Location page
        self.property_name = None
        # Rent page
        self.building_type = None
        self.multiple_floorplans = None
        self.req_broker_fee = None
        self.req_first_month = None
        self.req_last_month = None
        self.req_upfront_costs = None
        self.req_references = None
        self.req_security_deposit = None
        self.specials = None
        # Specifics page
        self.number_of_occupants = None
        self.allow_subletting = None
        self.is_sublet = None
        self.roommate_situation = None
        self.availability_date = None
        self.availability_renew = None
        # Amenities
        self.pet_policy = None
        self.lead_paint = None
        # Amenities/features
        self.ac = None
        self.carpet = None
        self.dining_room = None
        self.disability_access = None
        self.dishwasher = None
        self.fireplace = None
        self.furnished = None
        self.garbage_disposal = None
        self.hardwood_floors = None
        self.high_speed_internet = None
        self.living_room = None
        self.microwave = None
        self.patio = None
        self.private_garden = None
        self.shared_garden = None
        self.smoke_free = None
        self.storage_additional = None
        self.storage_included = None
        self.study = None
        # Amenities/agency
        self.fee_agent_broker = None
        self.no_fee = None
        # Amenities/community
        self.fitness_room = None
        self.individual_leases = None
        self.near_bus_stop = None
        self.near_T_stop = None
        self.pool = None
        self.roommate_matching = None
        self.tennis_court = None
        # Amenities/lease
        self.twelve_months = None
        self.nine_months = None
        self.fall_sublet = None
        self.flexible = None
        self.month_to_month = None
        self.short_term = None
        self.spring_sublet = None
        self.summer_sublet = None
        # Amenities/security
        self.courtesy_officer = None
        self.dead_bolt = None
        self.exterior_lighting = None
        self.intercom = None
        self.security_guard = None
        self.security_system = None
        self.video_surveillance = None
        # Amenities/utilities
        self.cable = None
        self.electricity = None
        self.gas = None
        self.heat = None
        self.high_speed_internet = None
        self.hot_water = None
        self.local_phone = None
        self.recycling = None
        self.trash_removal = None
        self.water_sewer = None
        # Amenities/parking
        self.garage_parking = None
        self.no_parking = None
        self.off_street_parking = None
        self.on_street_parking = None
        # Amenities/laundry
        self.laundry_room_in_community = None
        self.no_laundry_in_unit = None
        self.washer_dryer_hookups = None
        self.washer_dryer_in_unit = None
        # Amenities/description
        self.description = None
        # Extra
        self.index = {
                # Location
                "actual address": 0,
                "put in address": 1,
                "display exact address": 2,
                "property name": 3,
                # Rent
                "building type": 6,
                "multiple floorplans": 7,
                "broker": 13,
                "first": 14,
                "last": 15,
                "upfront": 16,
                "references": 17,
                "security": 18,
                "specials": 19,
                # Specifics
                "number of occupants": 22,
                "allow subletting": 23,
                "is sublet": 24,
                "roommate situation": 25,
                "availability date": 26,
                "availability renew": 27,
                # Amenities
                "pet policy": 29,
                "lead paint": 30,
                # Amenities/features
                "ac": 32,
                "carpet": 33,
                "dining room": 34,
                "disability access": 35,
                "dishwasher": 36,
                "fireplace": 37,
                "furnished": 38,
                "garbage disposal": 39,
                "hardwood floors": 40,
                "high-speed internet": 41,
                "living room": 42,
                "microwave": 43,
                "patio": 44,
                "private garden": 45,
                "shared garden": 46,
                "smoke free": 47,
                "storage additional": 48,
                "storage included": 49,
                "study": 50,
                # Amenities/agency
                "fee agent broker": 52,
                "no fee": 53,
                # Amenities/community
                "fitness room": 55,
                "individual leases": 56,
                "near bus stop": 57,
                "near T stop": 58,
                "pool": 59,
                "roommate matching": 60,
                "tennis court": 61,
                # Amenities/lease
                "12 months": 63,
                "9 months": 64,
                "fall sublet": 65,
                "flexible": 66,
                "month to month": 67,
                "short term": 68,
                "spring sublet": 69,
                "summer sublet": 70,
                # Amenities/security
                "courtesy officer": 72,
                "dead-bolt": 73,
                "exterior lighting": 74,
                "intercom": 75,
                "security guard": 76,
                "security system": 77,
                "video surveillance": 78,
                # Amenities/utilities
                "cable": 80,
                "electricity": 81,
                "gas": 82,
                "heat": 83,
                "high speed internet": 84,
                "hot water": 85,
                "local phone": 86,
                "recycling": 87,
                "trash removal": 88,
                "water sewer": 89,
                # Amenities/parking
                "garage parking": 91,
                "no parking": 92,
                "off street parking": 93,
                "on street parking": 94,
                # Amenities/laundry
                "laundry room in community": 96,
                "no laundry in unit": 97,
                "washer dryer hookups": 98,
                "washer dryer in unit": 99,
                # Amenities/description
                "description": 109
                }
        self.data = pd.read_excel(TEMP_LISTING, sheet_name = 6)
        # This replaces empty cells with None (instead of nan)
        self.data = self.data.where(pd.notnull(self.data), None)
        self.geo = geohelper.GeoHelper(debug, creds)
    def disp(self):
        pprint.pprint(vars(self))
    def get_key(self, key):
        return self.data.iloc[self.index[key]][3]
    def NY_to_bool(self, key):
        return True if self.get_key(key) == 'Y' else False 
    def format_rent_data(self):
        self.building_type = self.get_key("building type")
        self.multiple_floorplans = self.NY_to_bool("multiple floorplans")
        self.req_broker_fee = self.NY_to_bool("broker")
        self.req_first_month = self.NY_to_bool("first")
        self.req_last_month = self.NY_to_bool("last")
        self.req_upfront_costs = self.NY_to_bool("upfront")
        self.req_references = self.NY_to_bool("references")
        self.req_security_deposit = self.NY_to_bool("security")

        return True
    def disp_location(self):
        print("Location data\n")
        print("Full address: ", self.full_address)
        print("Street#: ", self.street_num)
        print("Street name: ", self.street_name)
        print("Unit: ", self.unit)
        print("City: ", self.city)
        print("State: ", self.state)
        print("Zip code: ", self.zip)
        print("Display exact address: ", self.display_exact_address)
        print("Property name: ", self.property_name)

        return True
    def disp_rent(self):
        print("Rent data\n")
        print("Building type: ", self.building_type)
        print("Multiple floorplans: ", self.multiple_floorplans)
        print("Broker fee: ", self.req_broker_fee)
        print("First month: ", self.req_first_month)
        print("Last month: ", self.req_last_month)
        print("Upfront costs: ", self.req_upfront_costs)
        print("References: ", self.req_references)
        print("Security deposit: ", self.req_security_deposit)

        return True
    def disp_amenities_features(self):
        print("Displaying features\n")

        print("Pet policy: ", self.pet_policy)
        print("Lead paint: ", self.lead_paint)
        print("Air conditioning: ", self.ac)
        print("Carpet: ", self.carpet)
        print("Dining room: ", self.dining_room)
        print("Disability access: ", self.disability_access)
        print("Dishwasher: ", self.dishwasher)
        print("Fireplace: ", self.fireplace)
        print("Furnished: ", self.furnished)
        print("Garbage disposal: ", self.garbage_disposal)
        print("Hardwood floors: ", self.hardwood_floors)
        print("High speed internet: ", self.high_speed_internet)
        print("Living room: ", self.living_room)
        print("Microwave: ", self.microwave)
        print("Patio: ", self.patio)
        print("Private garden: ", self.private_garden)
        print("Shared garden: ", self.shared_garden)
        print("Smoke free: ", self.smoke_free)
        print("Storage additional: ", self.storage_additional)
        print("Storage included: ", self.storage_included)
        print("Study: ", self.study)
        
        return True
    def disp_amenities_community(self):
        print("Displaying community\n")
        print("Fitness room: ", self.fitness_room)
        print("Individual leases: ", self.individual_leases)
        print("Near bus stop: ", self.near_bus_stop)
        print("New T stop: ", self.near_T_stop)
        print("Pool: ", self.pool)
        print("Roommate matching: ", self.roommate_matching)
        print("Tennis court: ", self.tennis_court)

        return True
    def disp_amenities_agency(self):
        print("Displaying agency\n")
        print("Fee agent broker: ", self.fee_agent_broker)
        print("No fee: ", self.no_fee)
        return True
    def disp_amenities_lease(self):
        print("Displaying lease\n")
        print("12 months: ", self.twelve_months)
        print("9 months: ", self.nine_months)
        print("Fall sublet: ", self.fall_sublet)
        print("Flexible: ", self.flexible)
        print("Month to month: ", self.month_to_month)
        print("Short term: ", self.short_term)
        print("Spring sublet: ", self.spring_sublet)
        print("Summer sublet: ", self.summer_sublet)

        return True
    def disp_amenities_security(self):
        print("Displaying security\n")
    
        print("Courtesy officer: ", self.courtesy_officer)
        print("Dead bolt: ", self.dead_bolt)
        print("Exterior lighting: ", self.exterior_lighting)
        print("Intercom: ", self.intercom)
        print("Security guard: ", self.security_guard)
        print("Security system: ", self.security_system)
        print("Video surveillance: ", self.video_surveillance)

        return True
    def disp_amenities_utilities(self):
        print("Displaying utilities\n")
        print("Cable: ", self.cable)
        print("Electricity: ", self.electricity)
        print("Gas: ", self.gas)
        print("Heat: ", self.heat)
        print("High speed internet: ", self.high_speed_internet)
        print("Hot water: ", self.hot_water)
        print("Local phone: ", self.local_phone)
        print("Recycling: ", self.recycling)
        print("Trash removal: ", self.trash_removal)
        print("Water sewer: ", self.water_sewer)

        return True
    def disp_amenities_parking(self):
        print("Displaying parking\n")
        print("Garage park: ", self.garage_parking)
        print("No park: ", self.no_parking)
        print("Off street park: ", self.off_street_parking)
        print("On street park: ", self.on_street_parking)

        return True
    def disp_amenities_laundry(self):
        print("Displaying laundry\n")
        print("Laundry room in community: ", self.laundry_room_in_community)
        print("Laundry in unit: ", self.no_laundry_in_unit)
        print("W/D hookups: ", self.washer_dryer_hookups)
        print("W/D in unit: ", self.washer_dryer_in_unit)

        return True
    def disp_amenities_description(self):
        print("Displaying description\n[THIS PART ISN'T FINISHED!!!!!]\n")
        print("Description: ", self.description)

        return True
    def disp_amenities(self):
        print("Displaying amenities\n")
        self.disp_amenities_features()
        self.disp_amenities_community()
        self.disp_amenities_agency()
        self.disp_amenities_lease()
        self.disp_amenities_security()
        self.disp_amenities_utilities()
        self.disp_amenities_parking()
        self.disp_amenities_laundry()
        self.disp_amenities_description()
        
        return True
    def format_amenities_features(self):
        self.ac = self.NY_to_bool("ac")
        self.carpet = self.NY_to_bool("carpet")
        self.carpet = True
        self.dining_room = self.NY_to_bool("dining room")
        self.disability_access = self.NY_to_bool("disability access")
        self.dishwasher = self.NY_to_bool("dishwasher")
        self.fireplace = self.NY_to_bool("fireplace")
        self.furnished = self.NY_to_bool("furnished")
        self.furnished = True
        self.garbage_disposal = self.NY_to_bool("garbage disposal")
        self.hardwood_floors = self.NY_to_bool("hardwood floors")
        self.high_speed_internet = self.NY_to_bool("high-speed internet")
        self.living_room = self.NY_to_bool("living room")
        self.microwave = self.NY_to_bool("microwave")
        self.microwave = True
        self.patio = self.NY_to_bool("patio")
        self.private_garden = self.NY_to_bool("private garden")
        self.shared_garden = self.NY_to_bool("shared garden")
        self.smoke_free = self.NY_to_bool("smoke free")
        self.storage_additional = self.NY_to_bool("storage additional")
        self.storage_included = self.NY_to_bool("storage included")
        self.study = self.NY_to_bool("study")

        return True
    def format_amenities_community(self):
        self.fitness_room = self.NY_to_bool("fitness room")
        self.individual_leases = self.NY_to_bool("individual leases")
        self.individual_leases = True
        self.near_bus_stop = self.NY_to_bool("near bus stop")
        self.near_T_stop = self.NY_to_bool("near T stop")
        self.pool = self.NY_to_bool("pool")
        self.pool = True
        self.roommate_matching = self.NY_to_bool("roommate matching")
        self.tennis_court = self.NY_to_bool("tennis court")

        return True
    def format_amenities_agency(self):
        self.fee_agent_broker = self.NY_to_bool("fee agent broker") 
        self.fee_agent_broker = True
        self.no_fee = self.NY_to_bool("no fee") 

        return True
    def format_amenities_lease(self):
        self.twelve_months = self.NY_to_bool("12 months")
        self.nine_months = self.NY_to_bool("9 months")
        self.fall_sublet = self.NY_to_bool("fall sublet")
        self.flexible = self.NY_to_bool("flexible")
        self.flexible = True
        self.month_to_month = self.NY_to_bool("month to month")
        self.short_term = self.NY_to_bool("short term")
        self.spring_sublet = self.NY_to_bool("spring sublet")
        self.spring_sublet = True
        self.summer_sublet = self.NY_to_bool("summer sublet")
        
        return True
    def format_amenities_security(self):
        self.courtesy_officer = self.NY_to_bool("courtesy officer")
        self.dead_bolt = self.NY_to_bool("dead-bolt")
        self.exterior_lighting = self.NY_to_bool("exterior lighting")
        self.exterior_lighting = True
        self.intercom = self.NY_to_bool("intercom")
        self.security_guard = self.NY_to_bool("security guard")
        self.security_system = self.NY_to_bool("security system")
        self.security_system = True
        self.video_surveillance = self.NY_to_bool("video surveillance")

        return True
    def format_amenities_utilities(self):
        self.cable = self.NY_to_bool("cable")
        self.electricity = self.NY_to_bool("electricity")
        self.gas = self.NY_to_bool("gas")
        self.gas = True
        self.heat = self.NY_to_bool("heat")
        self.high_speed_internet = self.NY_to_bool("high speed internet")
        self.hot_water = self.NY_to_bool("hot water")
        self.local_phone = self.NY_to_bool("local phone")
        self.recycling = self.NY_to_bool("recycling")
        self.recycling = True
        self.trash_removal = self.NY_to_bool("trash removal")
        self.water_sewer = self.NY_to_bool("water sewer")

        return True
    def format_amenities_parking(self):
        self.garage_parking = self.NY_to_bool("garage parking")
        self.no_parking = self.NY_to_bool("no parking")
        self.no_parking = True
        self.off_street_parking = self.NY_to_bool("off street parking")
        self.on_street_parking = self.NY_to_bool("on street parking")

        return True
    def format_amenities_laundry(self):
        self.laundry_room_in_community = self.NY_to_bool("laundry room in community")
        self.no_laundry_in_unit = self.NY_to_bool("no laundry in unit")
        self.no_laundry_in_unit = True
        self.washer_dryer_hookups = self.NY_to_bool("washer dryer hookups")
        self.washer_dryer_in_unit = self.NY_to_bool("washer dryer in unit")

        return True
    def format_amenities_description(self):
        self.description = self.get_key("description")

        return True
    def format_amenities_data(self):
        self.pet_policy = self.get_key("pet policy")
        if self.DEBUG != None: print("Fix the pet policy!!!!!!!!\n!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.lead_paint = self.get_key("lead paint")

        self.format_amenities_features()
        self.format_amenities_agency()
        self.format_amenities_community()
        self.format_amenities_lease()
        self.format_amenities_security()
        self.format_amenities_utilities()
        self.format_amenities_parking()
        self.format_amenities_laundry()
        self.format_amenities_description()

        return True
    def format_specifics_data(self):
        self.number_of_occupants = self.get_key("number of occupants")
        self.availability_date = self.get_key("availability date")
        self.allow_subletting = self.NY_to_bool("allow subletting")
        self.is_sublet = self.NY_to_bool("is sublet")
        self.roommate_situation = self.NY_to_bool("roommate situation")
        self.availability_renew = self.get_key("availability renew") # Because this can be unknown

        return True
    def disp_specifics(self):
        print("Number of occupants: ", self.number_of_occupants)
        print("Availability date: ", self.availability_date)
        print("Allow subletting: ", self.allow_subletting)
        print("Is sublet: ", self.is_sublet)
        print("Roommate situation: ", self.roommate_situation)
        print("Availability renew: ", self.availability_renew)
        
        return True
    def format_location_data(self):
        address = self.get_key("actual address")

        self.set_address(address)

        self.display_exact_address = self.NY_to_bool("display exact address")

        self.property_name = self.get_key("property name")
        print("This is the property name: ", self.property_name)
        if self.property_name == None:
            print("No property name found, using address.")
            self.property_name = "[JJ's testing supplies]" + self.full_address

        return True
    def get_listing_data(self):
        if self.DEBUG != None:
            for key in self.index:
                print (key + ": \t\t", self.get_key(key))

        self.format_location_data()
        self.format_rent_data()
        print("FIX ME!!!!!!!!!!!!!!!!!!!!!!!\n Should take care of floorplan details here.")
        self.format_specifics_data()
        self.format_amenities_data()
        
        self.disp_location()
        self.disp_rent()
        self.disp_specifics()
        self.disp_amenities()

        self.disp()

        return self
    def set_address(self, address):
        address = self.parse_address(address)
        self.full_address = address["full"]
        self.street_num = address["number"]
        self.street_name = address["name"]
        self.unit = address["unit"]
        self.city = address["city"]
        self.state = address["state"] 

        if self.DEBUG != None:
            print("Getting postal code.")
        self.zip = self.geo.get_zip(self.full_address)

    def parse_address(self, address):
        old = address
        if self.DEBUG != None:
            print ("Stripping whitespace.")
        address = address.strip()
        if self.DEBUG != None:
            print ("Splitting address.")
        result = re_address.split(address)
        if self.DEBUG != None:
            print ("Cleaning up entry.")
        result = list(filter(None, result))
        temp_add = re_num.split(result[0])
        if self.DEBUG != None:
            print ("Cleaning up name.")
        temp_add = list(filter(None, temp_add))
        temp_add[0] = temp_add[0].strip()
        temp_add[1] = temp_add[1].strip()
        if self.DEBUG != None:
            print ("Fetching unit# from: \"", result[1], "\"")
        if self.DEBUG != None:
            print ("Cleaning up unit number.")
        temp_unit = result[1][1:].strip()

        return {
                "full": old,
                "number": temp_add[0],
                "name": temp_add[1],
                "unit": temp_unit[1:],
                "city": result[2],
                "state": result[3]
                }    
