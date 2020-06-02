import logging
import pprint
import sys

class Payload:
    def __init__(self):
        self.log = logging.getLogger("root")
        self.log.info("Initializing Payload.")
    
        self.credentials = self.__get_credentials("private.slr")

        self.__init__data__()
    def __get_credentials(self, slr):
        result = {}
        self.log.info("Getting credentials.")
    
        with open (slr, "r") as slurp:
            data = slurp.readlines()
        if  len(data) != 3:
            logging.error("Could not find credentials in 'private.slr'.")
            sys.exit()
    
        result["username"] = data[0].rstrip()
        result["password"] = data[1].rstrip()
        result["api_key"] = data[2].rstrip()
    
        return result
    def disp(self):
        pprint.pprint(self.data)
    def xpath(self, page, name):
        return self.data[page][name]["xpath"]
    def id(self, page, name):
        return self.data[page][name]["id"]
    def offset(self, page, name):
        return self.data[page][name]["offset"]
    def get_value(self, page, name):
        return self.data[page][name]["value"]
    def set_value(self, page, name, value):
        self.data[page][name]["value"] = value
    def __add__element__(self, page, name, css_id, css_xpath, cell_offset, value):
        if page not in self.data:
            self.data[page] = {}
        if name not in self.data[page]:
            if cell_offset != None:
                value = self.ss.get_key(cell_offset) 
            self.data[page][name] = {
                "id": css_id,
                "xpath": css_xpath,
                "offset": cell_offset,
                "value": value
            }
        else:
            self.log.error("Error parsing initial data.")
            sys.exit()
    def __init__data__(self):
        self.data = {}
        # Login page
        self.__add__element__("login", "login url", None, None, None, "https://offcampus.bu.edu/login/")
        self.__add__element__("login", "add listing url", None, None, None, "https://offcampus.bu.edu/user/add-listing/")
        self.__add__element__("login", "username", "username", None, None, self.credentials["username"])
        self.__add__element__("login", "password", "password", None, None, self.credentials["password"])
        self.__add__element__("hidden", "gmaps", None, None, None, self.credentials["api_key"])
    def init(self, ss):
        self.ss = ss
        self.__add__element__("login", "login link", None, "//form[@id=\"login\"]/preceding-sibling::a", None, None)
        self.__add__element__("login", "submit button", None, "//input[@type=\"submit\"]", None, None)
        # Location page
        self.__add__element__("location", "full address", "address-autocomplete-place", None, 0, None)
        self.__add__element__("location", "full address input", None, "//*[@id=\"address_autocomplete\"]", 1, None)
        self.__add__element__("location", "exact flag", "opt_street-0", None, 2, None)
        self.__add__element__("location", "property name", "property_name", None, 3, None)
        address = ss.parse_address(ss.get_key(0))
        self.__add__element__("location", "address", "address", None, None, str(address["number"] + " " + address["name"]))
        self.__add__element__("location", "city", "city", None, None, address["city"])
        self.__add__element__("location", "state", "state", None, None, address["state"])
        self.__add__element__("location", "zip", "zip", None, None, address["zip"])
        self.__add__element__("location", "unit", None, None, None, address["unit"])
        self.__add__element__("location", "address form", None, "//form[@action=\"/user/add-listing\"]", None, None)
        # Rent page
        self.__add__element__("rent", "rent link", None, "//a[@data-target=\"rent\"]", None, None)
        self.__add__element__("rent", "building type", "buildingtype", None, 6, None)
        self.__add__element__("rent", "floorplans no", "multi-unit-no", None, 7, None)
        self.__add__element__("rent", "floorplans yes", "multi-unit-yes", None, 7, None)
        self.__add__element__("rent", "broker", "security_deposit_amenities-231", None, 13, None)
        self.__add__element__("rent", "first", "security_deposit_amenities-161", None, 14, None)
        self.__add__element__("rent", "last", "security_deposit_amenities-162", None, 15, None)
        self.__add__element__("rent", "upfront", "security_deposit_amenities-165", None, 16, None)
        self.__add__element__("rent", "references", "security_deposit_amenities-164", None, 17, None)
        self.__add__element__("rent", "security", "security_deposit_amenities-163", None, 18, None)
        self.__add__element__("rent", "specials", "specials", None, 19, None)
        # Specifics page
        self.__add__element__("specifics", "link", None, "//a[@data-target=\"details\"]", None, None)
        self.__add__element__("specifics", "max occupants", "max-occupants", None, 22, None)
        self.__add__element__("specifics", "allow sublet", "allow_sublets-display", None, 23, None)
        self.__add__element__("specifics", "is sublet", "sublet-display", None, 24, None)
        self.__add__element__("specifics", "roommate situation", "shared-display", None, 25, None)
        print("FIX ME, requires thinking.")
        self.__add__element__("specifics", "available now", "move-in-now", None, 26, None)
        self.__add__element__("specifics", "available date", "move-in-date", None, 26, None)
        self.__add__element__("specifics", "available date start", "start", None, 26, None)
        self.__add__element__("specifics", "available range", "move-in-range", None, 26, None)
        self.__add__element__("specifics", "available date end", "end", None, 26, None)
        print("This be fixed.")
        self.__add__element__("specifics", "renew unknown", "renew-option-unknown", None, 27, None)
        self.__add__element__("specifics", "renew yes", "renew-option-yes", None, 27, None)
        self.__add__element__("specifics", "renew no", "renew-option-no", None, 27, None)
        # Amenities page
        # Features
        self.__add__element__("amenities", "link", None, "//a[@data-target=\"amenities\"]", None, None)
        self.__add__element__("amenities", "pet policy", "pet_policy", None, 29, None)
        self.__add__element__("amenities", "lead paint", "lead_paint", None, 30, None)
        self.__add__element__("amenities", "ac", "amenity[1]-1", None, 32, None)
        self.__add__element__("amenities", "carpet", "amenity[1]-20", None, 33, None)
        self.__add__element__("amenities", "dining room","amenity[1]-202", None, 34, None)
        self.__add__element__("amenities", "disability access","amenity[1]-15", None, 35, None)
        self.__add__element__("amenities", "dishwasher","amenity[1]-26", None, 36, None)
        self.__add__element__("amenities", "fireplace","amenity[1]-8", None, 37, None)
        self.__add__element__("amenities", "furnished","amenity[1]-7", None, 38, None)
        self.__add__element__("amenities", "garbage disposal","amenity[1]-82", None, 39, None)
        self.__add__element__("amenities", "hardwoord","amenity[1]-21", None, 40, None)
        self.__add__element__("amenities", "internet","amenity[1]-303", None, 41, None)
        self.__add__element__("amenities", "living room","amenity[1]-200", None, 42, None)
        self.__add__element__("amenities", "microwave","amenity[1]-204", None, 43, None)
        self.__add__element__("amenities", "patio","amenity[1]-6", None, None, 44)
        self.__add__element__("amenities", "private garden","amenity[1]-205", None, 45, None)
        self.__add__element__("amenities", "shared garden","amenity[1]-206", None, 46, None)
        self.__add__element__("amenities", "smoke free","amenity[1]-41", None, 47, None)
        self.__add__element__("amenities", "additional storage","amenity[1]-207", None, 48, None)
        self.__add__element__("amenities", "included storage","amenity[1]-208", None, 49, None)
        self.__add__element__("amenities", "study","amenity[1]-203", None, 50, None)
        # Agency
        self.__add__element__("amenities", "agent fee", "amenity[8]-50", None, 52, None)
        self.__add__element__("amenities", "no fee", "amenity[8]-51", None, 53, None)
        # Community
        self.__add__element__("amenities", "fitness room", "amenity[2]-45", None, 55, None)
        self.__add__element__("amenities", "individual leases", "amenity[2]-46", None, 56, None)
        self.__add__element__("amenities", "near bus", "amenity[2]-19", None, 57, None)
        self.__add__element__("amenities", "near T", "amenity[2]-133", None, 58, None)
        self.__add__element__("amenities", "pool", , "amenity[2]-10", None, 59, None)
        self.__add__element__("amenities", "roommate matching", "amenity[2]-44", None, 60, None)
        self.__add__element__("amenities", "tennis court", "amenity[2]-11", None, 61, None)
#        ###TODO!!!
#        # Lease
#        self.twelve_months_id = "amenity[5]-16"
#        self.nine_months_id = "amenity[5]-17"
#        self.fall_sublet_id = "amenity[5]-76"
#        self.flexible_lease_id = "amenity[5]-18"
#        self.month_to_month_id = "amenity[5]-63"
#        self.short_term_lease_id = "amenity[5]-42"
#        self.spring_sublet_id = "amenity[5]-77"
#        self.summer_sublet_id = "amenity[5]-75"
#        # Security
#        self.courtesy_officer_id = "amenity[9]-120"
#        self.dead_bolt_id = "amenity[9]-95"
#        self.exterior_light_id = "amenity[9]-99"
#        self.intercom_id = "amenity[9]-97"
#        self.security_guard_id = "amenity[9]-100"
#        self.security_system_id = "amenity[9]-25"
#        self.video_surv_id = "amenity[9]-98"
#        # Utilities
#        self.cable_id = "amenity[3]-5"
#        self.electricity_id = "amenity[3]-4"
#        self.gas_id = "amenity[3]-3"
#        self.heat_id = "amenity[3]-2"
#        self.util_internet_id = "amenity[3]-35"
#        self.hot_water_id = "amenity[3]-226"
#        self.local_phone_id = "amenity[3]-39"
#        self.recycling_id = "amenity[3]-124"
#        self.trash_id = "amenity[3]-22"
#        self.water_id = "amenity[3]-23"
#        # Parking
#        self.garage_park_id = "amenity[4]-37"
#        self.no_parking_id = "amenity[4]-142"
#        self.off_street_park_id = "amenity[4]-36"
#        self.on_street_park_id = "amenity[4]-38"
#        # Laundry
#        self.laundry_in_comm_id = "amenity[7]-12"
#        self.no_laundry_id = "amenity[7]-143"
#        self.wd_hookups_id = "amenity[7]-33"
#        self.wd_in_unit = "amenity[7]-9"
#        # Description
#        #TODO !!!! FIXME
#        self.description_id = "mceu_13"
#        # Contact page
#        self.contact_link =  "//a[@data-target=\"contact\"]"
#        # Photos page
#        self.photos_link =  "//a[@data-target=\"images\"]"
#        #END TODO!!!
