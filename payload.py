import logging
import pprint
import sys

class Payload:
    def __init__(self):
        self.log = logging.getLogger("root")
        self.log.info("Initializing Payload.")
    
        self.credentials = self.__get_credentials__("private.slr")

        self.__init__data__()
    def __get_credentials__(self, slr):
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
    def get_bool(self, page, name):
        return self.data[page][name]["value"] == "Y"
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
            self.log.error("Page = " + str(page))
            self.log.error("Name = " + str(name))
            self.log.error("CSS ID = " + str(css_id))
            self.log.error("CSS XPATH = " + str(css_xpath))
            self.log.error("Cell offset = " + str(cell_offset))
            self.log.error("Value = " + str(value))
            sys.exit()
    def __init__data__(self):
        self.data = {}
        # Login page
        self.__add__element__("login", "login url", None, None, None, "https://offcampus.bu.edu/login/")
        self.__add__element__("login", "add listing url", None, None, None, "https://offcampus.bu.edu/user/add-listing/")
        self.__add__element__("login", "username", "username", None, None, self.credentials["username"])
        self.__add__element__("login", "password", "password", None, None, self.credentials["password"])
        self.__add__element__("hidden", "gmaps", None, None, None, self.credentials["api_key"])
        self.credentials = None
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
        print("TODO, fix floorplan, add loop for Y.")
        self.__add__element__("rent", "floorplans no", "multi-unit-no", None, 7, None)
        self.__add__element__("rent", "floorplans yes", "multi-unit-yes", None, 7, None)
        print("ENDTODO.")
        self.__add__element__("rent", "bedrooms", "floorplan-0-bedrooms", None, 8, None)
        self.__add__element__("rent", "bathrooms", "floorplan-0-bathrooms", None, 9, None)
        self.__add__element__("rent", "square feet", "floorplan-0-sqft", None, 10, None)
        self.__add__element__("rent", "monthly rent", "floorplan-0-rent_value", None, 11, None)
        self.__add__element__("rent", "type", "floorplan-0-per_bedroom", None, 12, None)
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
        print("Should I get the values for pets here instead of in the navigator?")
        self.__add__element__("amenities", "cats", "pet_types-27", None, None, None)
        self.__add__element__("amenities", "dogs", "pet_types-28", None, None, None)
        self.__add__element__("amenities", "lead paint", "lead_paint", None, 30, None)
        self.__add__element__("amenities", "ac", "amenity[1]-1", None, 32, None)
        self.__add__element__("amenities", "carpet", "amenity[1]-20", None, 33, None)
        self.__add__element__("amenities", "dining room","amenity[1]-202", None, 34, None)
        self.__add__element__("amenities", "disability access","amenity[1]-15", None, 35, None)
        self.__add__element__("amenities", "dishwasher","amenity[1]-26", None, 36, None)
        self.__add__element__("amenities", "fireplace","amenity[1]-8", None, 37, None)
        self.__add__element__("amenities", "furnished","amenity[1]-7", None, 38, None)
        self.__add__element__("amenities", "garbage disposal","amenity[1]-82", None, 39, None)
        self.__add__element__("amenities", "hardwood","amenity[1]-21", None, 40, None)
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
        self.__add__element__("amenities", "pool", "amenity[2]-10", None, 59, None)
        self.__add__element__("amenities", "roommate matching", "amenity[2]-44", None, 60, None)
        self.__add__element__("amenities", "tennis court", "amenity[2]-11", None, 61, None)
        # Lease
        self.__add__element__("amenities", "12 months", "amenity[5]-16", None, 63, None)
        self.__add__element__("amenities", "9 months", "amenity[5]-17", None, 64, None)
        self.__add__element__("amenities", "fall sublet", "amenity[5]-76", None, 65, None)
        self.__add__element__("amenities", "flexible lease", "amenity[5]-18", None, 66, None)
        self.__add__element__("amenities", "month to month", "amenity[5]-63", None, 67, None)
        self.__add__element__("amenities", "short term lease", "amenity[5]-42", None, 68, None)
        self.__add__element__("amenities", "spring sublet", "amenity[5]-77", None, 69, None)
        self.__add__element__("amenities", "summer sublet", "amenity[5]-75", None, 70, None)
        # Security
        self.__add__element__("amenities", "courtesy officer", "amenity[9]-120", None, 72, None)
        self.__add__element__("amenities", "dead bolt", "amenity[9]-95", None, 73, None)
        self.__add__element__("amenities", "exterior light", "amenity[9]-99", None, 74, None)
        self.__add__element__("amenities", "intercom", "amenity[9]-97", None, 75, None)
        self.__add__element__("amenities", "security guard", "amenity[9]-100", None, 76, None)
        self.__add__element__("amenities", "security system", "amenity[9]-25", None, 77, None)
        self.__add__element__("amenities", "video surveillance", "amenity[9]-98", None, 78, None)
        # Utilities
        self.__add__element__("amenities", "cable", "amenity[3]-5", None, 80, None)
        self.__add__element__("amenities", "electricity", "amenity[3]-4", None, 81, None)
        self.__add__element__("amenities", "gas", "amenity[3]-3", None, 82, None)
        self.__add__element__("amenities", "heat", "amenity[3]-2", None, 83, None)
        self.__add__element__("amenities", "high-speed internet", "amenity[3]-35", None, 84, None)
        self.__add__element__("amenities", "hot water", "amenity[3]-226", None, 85, None)
        self.__add__element__("amenities", "local phone", "amenity[3]-39", None, 86, None)
        self.__add__element__("amenities", "recycling", "amenity[3]-124", None, 87, None)
        self.__add__element__("amenities", "trash", "amenity[3]-22", None, 88, None)
        self.__add__element__("amenities", "water", "amenity[3]-23", None, 89, None)
        # Parking
        self.__add__element__("amenities", "garage", "amenity[4]-37", None, 91, None)
        self.__add__element__("amenities", "no parking", "amenity[4]-142", None, 92, None)
        self.__add__element__("amenities", "off street parking", "amenity[4]-36", None, 93, None)
        self.__add__element__("amenities", "on street parking", "amenity[4]-38", None, 94, None)
        # Laundry
        self.__add__element__("amenities", "laundry room", "amenity[7]-12", None, 96, None)
        self.__add__element__("amenities", "no laundry", "amenity[7]-143", None, 97, None)
        self.__add__element__("amenities", "wd hookups", "amenity[7]-33", None, 98, None)
        self.__add__element__("amenities", "wd in unit", "amenity[7]-9", None, 99, None)
        # Description
        self.__add__element__("amenities", "tinymce", "description_ifr", None, None, None)
        self.__add__element__("amenities", "description", "tinymce", None, 109, None)
        #TODO
        # Contact page
        #self.contact_link =  "//a[@data-target=\"contact\"]"
        # Photos page
        #self.photos_link =  "//a[@data-target=\"images\"]"
        #END TODO!!!
