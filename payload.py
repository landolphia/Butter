import logging
import pprint
import sys

FP_START = 137 
FP_LENGTH = 38

class Payload:
    def __init__(self):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Payload.")
        self.log.debug("FIXME! It should be pretty easy to get the kind of identifier. Either by adding a kind and having only one field, or just having the two fields and testing.")
        self.log.debug("FIXME! Add data type (string, number, etc)")
    
        self.credentials = self.__get_credentials__("private.slr")

        self.__init__data__()
    def __get_credentials__(self, slr):
        result = {}
        self.log.debug("Getting credentials.")
    
        with open (slr, "r") as slurp:
            data = slurp.readlines()
        if  len(data) != 3:
            logging.error("Could not find credentials in 'private.slr'.")
            sys.exit()
    
        result["username"] = data[0].rstrip()
        result["password"] = data[1].rstrip()
        result["api_key"] = data[2].rstrip()
    
        return result
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
        else: # Duplicate key
            self.log.error("Error scraping initial data. Exiting." +
                    "\nPage = " + str(page) +
                    "\nName = " + str(name) + 
                    "\nCSS ID = " + str(css_id) +
                    "\nCSS XPATH = " + str(css_xpath) +
                    "\nCell offset = " + str(cell_offset) +
                    "\nValue = " + str(value))
            sys.exit()
    def __init__data__(self):
        self.data = {}
        # Login page
        self.__add__element__("login", "login url", None, None, None, "https://offcampus.bu.edu/login/")
        self.__add__element__("login", "add listing url", None, None, None, "https://offcampus.bu.edu/user/add-listing/")
        self.__add__element__("login", "link", None, "//form[@id=\"login\"]/preceding-sibling::a", None, None)
        self.__add__element__("login", "submit button", None, "//input[@type=\"submit\"]", None, None)
        self.__add__element__("login", "username", "username", None, None, self.credentials["username"])
        self.__add__element__("login", "password", "password", None, None, self.credentials["password"])
        self.__add__element__("hidden", "gmaps", None, None, None, self.credentials["api_key"])
        self.credentials = None
    def xpath(self, page, name): return self.data[page][name]["xpath"]
    def id(self, page, name): return self.data[page][name]["id"]
    def offset(self, page, name): return self.data[page][name]["offset"]
    def get_value(self, page, name): return self.data[page][name]["value"]
    def get_bool(self, page, name): return self.data[page][name]["value"] == "Y"
    def set_value(self, page, name, value): self.data[page][name]["value"] = value
    def init(self, ss):
        self.ss = ss
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
        self.log.debug("FIX ME, requires thinking. Especially with the 2 row shift from the new format.")
        self.__add__element__("specifics", "available ongoing", "move-in-now", None, 26, None)
        self.__add__element__("specifics", "available date", "move-in-date", None, 26, None)
        self.__add__element__("specifics", "available date start", "start", None, 26, None)
        self.__add__element__("specifics", "available range", "move-in-range", None, 26, None)
        self.__add__element__("specifics", "available date end", "end", None, 26, None)
        self.log.debug("This be fixed.")
        self.__add__element__("specifics", "renew unknown", "renew-option-unknown", None, 27, None)
        self.__add__element__("specifics", "renew yes", "renew-option-yes", None, 27, None)
        self.__add__element__("specifics", "renew no", "renew-option-no", None, 27, None)
        # Amenities page
        # Features
        self.__add__element__("amenities", "link", None, "//a[@data-target=\"amenities\"]", None, None)
        self.__add__element__("amenities", "pet policy", "pet_policy", None, 31, None)
        self.log.debug("Should I get the values for pets here instead of in the navigator?")
        self.__add__element__("amenities", "cats", "pet_types-27", None, None, None)
        self.__add__element__("amenities", "dogs", "pet_types-28", None, None, None)
        self.__add__element__("amenities", "lead paint", "lead_paint", None, 32, None)
        self.__add__element__("amenities", "ac", "amenity[1]-1", None, 34, None)
        self.__add__element__("amenities", "carpet", "amenity[1]-20", None, 35, None)
        self.__add__element__("amenities", "dining room","amenity[1]-202", None, 36, None)
        self.__add__element__("amenities", "disability access","amenity[1]-15", None, 37, None)
        self.__add__element__("amenities", "dishwasher","amenity[1]-26", None, 38, None)
        self.__add__element__("amenities", "fireplace","amenity[1]-8", None, 39, None)
        self.__add__element__("amenities", "furnished","amenity[1]-7", None, 40, None)
        self.__add__element__("amenities", "garbage disposal","amenity[1]-82", None, 41, None)
        self.__add__element__("amenities", "hardwood","amenity[1]-21", None, 42, None)
        self.__add__element__("amenities", "internet","amenity[1]-303", None, 43, None)
        self.__add__element__("amenities", "living room","amenity[1]-200", None, 44, None)
        self.__add__element__("amenities", "microwave","amenity[1]-204", None, 45, None)
        self.__add__element__("amenities", "patio","amenity[1]-6", None, None, 46)
        self.__add__element__("amenities", "private garden","amenity[1]-205", None, 47, None)
        self.__add__element__("amenities", "shared garden","amenity[1]-206", None, 48, None)
        self.__add__element__("amenities", "smoke free","amenity[1]-41", None, 49, None)
        self.__add__element__("amenities", "additional storage","amenity[1]-207", None, 50, None)
        self.__add__element__("amenities", "included storage","amenity[1]-208", None, 51, None)
        self.__add__element__("amenities", "study","amenity[1]-203", None, 52, None)
        # Agency
        self.__add__element__("amenities", "agent fee", "amenity[8]-50", None, 54, None)
        self.__add__element__("amenities", "no fee", "amenity[8]-51", None, 55, None)
        # Community
        self.__add__element__("amenities", "fitness room", "amenity[2]-45", None, 57, None)
        self.__add__element__("amenities", "individual leases", "amenity[2]-46", None, 58, None)
        self.__add__element__("amenities", "near bus", "amenity[2]-19", None, 59, None)
        self.__add__element__("amenities", "near T", "amenity[2]-133", None, 60, None)
        self.__add__element__("amenities", "pool", "amenity[2]-10", None, 61, None)
        self.__add__element__("amenities", "roommate matching", "amenity[2]-44", None, 62, None)
        self.__add__element__("amenities", "tennis court", "amenity[2]-11", None, 63, None)
        # Lease
        self.__add__element__("amenities", "12 months", "amenity[5]-16", None, 65, None)
        self.__add__element__("amenities", "9 months", "amenity[5]-17", None, 66, None)
        self.__add__element__("amenities", "fall sublet", "amenity[5]-76", None, 67, None)
        self.__add__element__("amenities", "flexible lease", "amenity[5]-18", None, 68, None)
        self.__add__element__("amenities", "month to month", "amenity[5]-63", None, 69, None)
        self.__add__element__("amenities", "short term lease", "amenity[5]-42", None, 70, None)
        self.__add__element__("amenities", "spring sublet", "amenity[5]-77", None, 71, None)
        self.__add__element__("amenities", "summer sublet", "amenity[5]-75", None, 72, None)
        # Security
        self.__add__element__("amenities", "courtesy officer", "amenity[9]-120", None, 74, None)
        self.__add__element__("amenities", "dead bolt", "amenity[9]-95", None, 75, None)
        self.__add__element__("amenities", "exterior light", "amenity[9]-99", None, 76, None)
        self.__add__element__("amenities", "intercom", "amenity[9]-97", None, 77, None)
        self.__add__element__("amenities", "security guard", "amenity[9]-100", None, 78, None)
        self.__add__element__("amenities", "security system", "amenity[9]-25", None, 79, None)
        self.__add__element__("amenities", "video surveillance", "amenity[9]-98", None, 80, None)
        # Utilities
        self.__add__element__("amenities", "cable", "amenity[3]-5", None, 82, None)
        self.__add__element__("amenities", "electricity", "amenity[3]-4", None, 83, None)
        self.__add__element__("amenities", "gas", "amenity[3]-3", None, 84, None)
        self.__add__element__("amenities", "heat", "amenity[3]-2", None, 85, None)
        self.__add__element__("amenities", "high-speed internet", "amenity[3]-35", None, 86, None)
        self.__add__element__("amenities", "hot water", "amenity[3]-226", None, 87, None)
        self.__add__element__("amenities", "local phone", "amenity[3]-39", None, 88, None)
        self.__add__element__("amenities", "recycling", "amenity[3]-124", None, 89, None)
        self.__add__element__("amenities", "trash", "amenity[3]-22", None, 90, None)
        self.__add__element__("amenities", "water", "amenity[3]-23", None, 91, None)
        # Parking
        self.__add__element__("amenities", "garage", "amenity[4]-37", None, 93, None)
        self.__add__element__("amenities", "no parking", "amenity[4]-142", None, 94, None)
        self.__add__element__("amenities", "off street parking", "amenity[4]-36", None, 95, None)
        self.__add__element__("amenities", "on street parking", "amenity[4]-38", None, 96, None)
        # Laundry
        self.__add__element__("amenities", "laundry room", "amenity[7]-12", None, 98, None)
        self.__add__element__("amenities", "no laundry", "amenity[7]-143", None, 99, None)
        self.__add__element__("amenities", "wd hookups", "amenity[7]-33", None, 100, None)
        self.__add__element__("amenities", "wd in unit", "amenity[7]-9", None, 101, None)
        # Description
        self.__add__element__("amenities", "property id", None, None, 111, None)
        self.__add__element__("amenities", "tinymce", "description_ifr", None, None, None)
        self.__add__element__("amenities", "description", "tinymce", None, 112, None)

        i = 1
        if self.get_bool("rent", "floorplans yes"):
            i -= 1
            self.log.info("This listing contains multiple floorplans.")
            self.__add__element__("floorplans", "link", None, "//a[@data-target=\"floorplans\"]", None, None)
            self.__add__element__("floorplans", "add link", None, "//button[@name=\"create-floorplan\"]", None, None)
            while(self.floorplan_found(i)):
                self.init_floorplan(i)
                i = i + 1

        self.log.info(str(i) + " floorplan" + ("s" if i > 1 else "") + " found.")
        self.__add__element__("floorplans", "total number",  None, None, None, i)
    def floorplan_found(self, n):
        offset = FP_START + ( n * FP_LENGTH)

        return self.ss.cell_exists(offset)
    def init_floorplan(self, n):
        offset = FP_START + ( n * FP_LENGTH)
        # Floorplans/The following cell rows are relative to the offset above.
        self.__add__element__("floorplans", "name" + str(n), "floorplan-FP_ID-name", None, offset + 0, None)
        self.__add__element__("floorplans", "specials" + str(n), "floorplan-FP_ID-specials", None, offset + 1, None)
        self.__add__element__("floorplans", "bedrooms" + str(n), "floorplan-FP_ID-bedrooms", None, offset + 2, None)
        self.__add__element__("floorplans", "bathrooms" + str(n), "floorplan-FP_ID-bathrooms", None, offset + 3, None)
        self.__add__element__("floorplans", "occupants" + str(n), "floorplan-FP_ID-occupants", None, offset + 4, None)
        self.__add__element__("floorplans", "square feet" + str(n), "floorplan-FP_ID-sqft", None, offset + 5, None)
        self.__add__element__("floorplans", "monthly rent" + str(n), "floorplan-FP_ID-rent_value", None, offset + 6, None)
        self.__add__element__("floorplans", "rental type" + str(n), "floorplan-FP_ID-per_bedroom", None, offset + 7, None)
        # Floorplans/Amenities
        self.__add__element__("floorplans", "ac" + str(n), "floorplan-FP_ID-amenity[1]-1", None, offset + 9, None)
        self.__add__element__("floorplans", "carpet" + str(n), "floorplan-FP_ID-amenity[1]-20", None, offset + 10, None)
        self.__add__element__("floorplans", "dining room" + str(n), "floorplan-FP_ID-amenity[1]-202", None, offset + 11, None)
        self.__add__element__("floorplans", "disability access" + str(n), "floorplan-FP_ID-amenity[1]-15", None, offset + 12, None)
        self.__add__element__("floorplans", "dishwasher" + str(n), "floorplan-FP_ID-amenity[1]-26", None, offset + 13, None)
        self.__add__element__("floorplans", "fireplace" + str(n), "floorplan-FP_ID-amenity[1]-8", None, offset + 14, None)
        self.__add__element__("floorplans", "furnished" + str(n), "floorplan-FP_ID-amenity[1]-7", None, offset + 15, None)
        self.__add__element__("floorplans", "garbage disposal" + str(n), "floorplan-FP_ID-amenity[1]-82", None, offset + 16, None)
        self.__add__element__("floorplans", "hardwood" + str(n), "floorplan-FP_ID-amenity[1]-21", None, offset + 17, None)
        self.__add__element__("floorplans", "high-speed internet" + str(n), "floorplan-FP_ID-amenity[1]-303", None, offset + 18, None)
        self.__add__element__("floorplans", "living room" + str(n), "floorplan-FP_ID-amenity[1]-200", None, offset + 19, None)
        self.__add__element__("floorplans", "microwave" + str(n), "floorplan-FP_ID-amenity[1]-204", None, offset + 20, None)
        self.__add__element__("floorplans", "patio" + str(n), "floorplan-FP_ID-amenity[1]-6", None, offset + 21, None)
        self.__add__element__("floorplans", "private garden" + str(n), "floorplan-FP_ID-amenity[1]-205", None, offset + 22, None)
        self.__add__element__("floorplans", "shared garden" + str(n), "floorplan-FP_ID-amenity[1]-206", None, offset + 23, None)
        self.__add__element__("floorplans", "smoke free" + str(n), "floorplan-FP_ID-amenity[1]-41", None, offset + 24, None)
        self.__add__element__("floorplans", "additional storage" + str(n), "floorplan-FP_ID-amenity[1]-207", None, offset + 25, None)
        self.__add__element__("floorplans", "included storage" + str(n), "floorplan-FP_ID-amenity[1]-208", None, offset + 26, None)
        self.__add__element__("floorplans", "study" + str(n), "floorplan-FP_ID-amenity[1]-203", None, offset + 27, None)
        # Floorplans/Availability
        self.__add__element__("floorplans", "availability not" + str(n), "floorplan-FP_ID-move-in-not", None, offset + 28, None)
        self.__add__element__("floorplans", "availability ongoing" + str(n), "floorplan-FP_ID-move-in-now", None, offset + 28, None)
        self.__add__element__("floorplans", "availability specific" + str(n), "floorplan-FP_ID-move-in-date", None, offset + 28, None)
        self.__add__element__("floorplans", "availability range" + str(n), "floorplan-FP_ID-move-in-range", None, offset + 28, None)
        self.__add__element__("floorplans", "start date" + str(n), "floorplan-FP_ID-start", None, offset + 29, None)
        self.__add__element__("floorplans", "end date" + str(n), "floorplan-FP_ID-end", None, offset + 30, None)
        # Floorplans/Description++
        self.__add__element__("floorplans", "description" + str(n), "floorplan-FP_ID-description", None, offset + 31, None)
        self.__add__element__("floorplans", "virtual tour" + str(n), "floorplan-FP_ID-virtual-tour", None, offset + 33, None)
        self.__add__element__("floorplans", "webpage" + str(n), "floorplan-FP_ID-website", None, offset + 34, None)
        self.__add__element__("floorplans", "lease" + str(n), "floorplan-FP_ID-lease", None, offset + 35, None)
        self.__add__element__("floorplans", "image" + str(n), "floorplan-FP_ID-image", None, offset + 36, None)
        #TODO
        # Contact page
        #self.contact_link =  "//a[@data-target=\"contact\"]"
        # Photos page
        #self.photos_link =  "//a[@data-target=\"images\"]"
        #END TODO!!!
