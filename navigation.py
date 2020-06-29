import logging
import elements


class Navigator:
    def __init__(self, payload):
            self.log = logging.getLogger("bLog")
            self.log.debug("Initializing Navigator.")
            
            self.payload = payload
            self.elements = elements.Elements(payload)
    def start(self):
        self.login()
        self.add_listing()
        self.fill_address()
        input("Done done")
        self.fill_rent()
        self.fill_specifics()
        self.fill_amenities()
        self.fill_contact()
        self.fill_photos()
    def login(self):
        self.elements.go("login", "login url")

        self.elements.wait("login", "link")
        self.elements.click("login", "link")

        self.elements.wait("login", "username")
        
        self.elements.fill_input("login", "username")
        self.elements.fill_input("login", "password")

        self.elements.click("login", "submit button")
    def add_listing(self):
        self.elements.go("login", "add listing url")

        self.elements.wait("location", "full address")

        self.elements.fill_input("location", "full address input")
        self.elements.press_enter("location", "full address input")
    def fill_address(self):
        self.elements.wait("location", "address")

        logging.debug("Filling in address details.")
   
        self.elements.fill_input("location", "address")
        self.elements.fill_input("location", "city")
        self.elements.fill_input("location", "zip")
    
        self.elements.dropdown("location", "state")

        self.elements.checkbox("location", "exact flag")


        self.elements.submit("location", "address form")

        self.elements.wait("location", "property name")

        self.elements.fill_input_not_null("location", "property name", "[TEST]")
        self.elements.press_enter("location", "property name")
        input("UHUH")
        sys.exit()
    def fill_rent(self):
        self.wait_for_xpath(self.payload.xpath("rent", "rent link"))
        link = self.driver.find_element_by_xpath(self.payload.xpath("rent", "rent link"))
        link.click()

        self.dropdown_by_id("rent", "building type")

        if self.payload.get_bool("rent", "floorplans yes"):
            radio = self.driver.find_element_by_id(self.payload.id("rent", "floorplans yes"))
        else:
            radio = self.driver.find_element_by_id(self.payload.id("rent", "floorplans no"))
        radio.click()

        self.checkbox_by_id("rent", "broker")
        self.checkbox_by_id("rent", "first")
        self.checkbox_by_id("rent", "last")
        self.checkbox_by_id("rent", "upfront")
        self.checkbox_by_id("rent", "references")
        self.checkbox_by_id("rent", "security")

        result = self.driver.find_element_by_id(self.payload.id("rent", "specials"))
        specials = self.payload.get_value("rent", "specials")
        if specials == None:
            specials = " "
        result.send_keys(specials)
        result.send_keys(Keys.ENTER)

        if self.payload.get_bool("rent", "floorplans yes"):
            self.fill_floorplans()
        else:
            self.fill_floorplan()
    def fill_floorplan(self):
        self.wait_for_id(self.payload.id("rent", "bedrooms"))
        
        self.dropdown_by_id("rent", "bedrooms")
        self.dropdown_by_id("rent", "bathrooms")
        element = self.driver.find_element_by_id(self.payload.id("rent", "square feet"))
        element.send_keys(self.payload.get_value("rent", "square feet"))
        element = self.driver.find_element_by_id(self.payload.id("rent", "monthly rent"))
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys("$" + str(self.payload.get_value("rent", "monthly rent")))
        self.dropdown_by_id("rent", "type")

        element = self.driver.find_element_by_id(self.payload.id("rent", "specials"))
        element.send_keys(Keys.ENTER)
    def fill_floorplans(self):
        self.log.warning("Floorplans are still being implemented.")

        self.wait_for_xpath(self.payload.xpath("floorplans", "link"))
        link = self.driver.find_element_by_xpath(self.payload.xpath("floorplans", "link"))
        link.click()

        i = 0
        fp_number = self.payload.get_value("floorplans", "total number")

        while i < fp_number:
            # FIXME Should click edit instead of add for the first floorplan
            # I can probably find the element with some kind of sibling logic
            xpath = self.wait_for_xpath(self.payload.xpath("floorplans", "add link"))
            link = self.driver.find_element_by_xpath(self.payload.xpath("floorplans", "add link"))
            link.click()

            url = str(self.elements.current_url())
            fp_id = url.rsplit('/', 1)[-1]
            self.log.debug("Filling floorplan #" + str(i) + " [ID=" + str(fp_id) + "]")

            self.send_keys_fp_by_id("floorplans", "name", i, fp_id)
            self.send_keys_fp_by_id("floorplans", "specials", i, fp_id)

            self.dropdown_fp_by_id("floorplans", "bedrooms", i, fp_id)
            self.dropdown_fp_by_id("floorplans", "bathrooms", i, fp_id)
            self.dropdown_fp_by_id("floorplans", "occupants", i, fp_id)

            self.send_keys_fp_by_id("floorplans", "square feet", i, fp_id)
            self.send_keys_fp_by_id("floorplans", "monthly rent", i, fp_id)

            self.dropdown_fp_by_id("floorplans", "rental type", i, fp_id)
            self.dropdown_fp_by_id("floorplans", "occupants", i, fp_id)

            self.checkbox_fp_by_id("floorplans", "ac", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "carpet", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "dining room", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "disability access", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "dishwasher", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "fireplace", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "furnished", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "garbage disposal", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "hardwood", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "high-speed internet", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "living room", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "microwave", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "patio", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "private garden", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "shared garden", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "smoke free", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "additional storage", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "included storage", i, fp_id)
            self.checkbox_fp_by_id("floorplans", "study", i, fp_id)
            self.log.warning("The date hasn't been implemented for floorplans. This must be filled manually.")
            # Floorplans/Availability
            #self.send_keys_fp_by_id("floorplans", "availability not")
            #self.send_keys_fp_by_id("floorplans", "availability ongoing")
            #self.send_keys_fp_by_id("floorplans", "availability specific")
            #self.send_keys_fp_by_id("floorplans", "availability range")
            #self.send_keys_fp_by_id("floorplans", "start date")
            #self.send_keys_fp_by_id("floorplans", "end date")
            # Floorplans/Description++
            self.log.warning("The description/virtual tour/webpage/lease/image haven't been implemented for floorplans. They must be filled manually.")
            #self.send_keys_fp_by_id("floorplans", "description")
            #self.send_keys_fp_by_id("floorplans", "virtual tour")
            #self.send_keys_fp_by_id("floorplans", "webpage")
            #self.send_keys_fp_by_id("floorplans", "lease")
            #self.send_keys_fp_by_id("floorplans", "image")
    def fill_amenities(self):
        self.wait_for_xpath(self.payload.xpath("amenities", "link"))
        link = self.driver.find_element_by_xpath(self.payload.xpath("amenities", "link"))
        link.click()

        self.log.warning("The pet dropdown hasn't been fully implemented. Check that the data is accurate.")
        self.log.debug("FIX the pets!")
        #FIXME
        #dd = self.driver.find_element_by_id(self.payload.id("amenities", "pet policy"))
        #pets = str(self.payload.get_value("amenities", "pet policy")).lower()
        #if pets == "not allowed":
        #    self.dropdown_by_id(dd, "pets not allowed")
        #elif "considered" in pets:
        #    self.dropdown_by_id(dd, "pets considered")
        #else:
        #    self.dropdown_by_id(dd, "pets allowed")

        #if "cat" in pets:
        #    element = self.driver.find_element_by_id(self.payload.id("amenities", "cats"))
        #    self.checkbox_by_id(element, True)
        #if "dog" in pets:
        #    element = self.driver.find_element_by_id(self.payload.id("amenities", "dogs"))
        #    self.checkbox_by_id(element, True)

        self.dropdown_by_id("amenities", "lead paint")
    
        # Features
        self.checkbox_by_id("amenities", "ac")
        self.checkbox_by_id("amenities", "carpet")
        self.checkbox_by_id("amenities", "dining room")
        self.checkbox_by_id("amenities", "disability access")
        self.checkbox_by_id("amenities", "dishwasher")
        self.checkbox_by_id("amenities", "fireplace")
        self.checkbox_by_id("amenities", "furnished")
        self.checkbox_by_id("amenities", "garbage disposal")
        self.checkbox_by_id("amenities", "hardwood")
        self.checkbox_by_id("amenities", "internet")
        self.checkbox_by_id("amenities", "living room")
        self.checkbox_by_id("amenities", "microwave")
        self.checkbox_by_id("amenities", "patio")
        self.checkbox_by_id("amenities", "private garden")
        self.checkbox_by_id("amenities", "shared garden")
        self.checkbox_by_id("amenities", "smoke free")
        self.checkbox_by_id("amenities", "additional storage")
        self.checkbox_by_id("amenities", "included storage")
        self.checkbox_by_id("amenities", "study")
        #Agency
        self.checkbox_by_id("amenities", "agent fee")
        self.checkbox_by_id("amenities", "no fee")
        # Community
        self.checkbox_by_id("amenities", "fitness room")
        self.checkbox_by_id("amenities", "individual leases")
        self.checkbox_by_id("amenities", "near bus")
        self.checkbox_by_id("amenities", "near T")
        self.checkbox_by_id("amenities", "pool")
        self.checkbox_by_id("amenities", "roommate matching")
        self.checkbox_by_id("amenities", "tennis court")
        # Lease
        self.checkbox_by_id("amenities", "12 months")
        self.checkbox_by_id("amenities", "9 months")
        self.checkbox_by_id("amenities", "fall sublet")
        self.checkbox_by_id("amenities", "flexible lease")
        self.checkbox_by_id("amenities", "month to month")
        self.checkbox_by_id("amenities", "short term lease")
        self.checkbox_by_id("amenities", "spring sublet")
        self.checkbox_by_id("amenities", "summer sublet")
        # Security
        self.checkbox_by_id("amenities", "courtesy officer")
        self.checkbox_by_id("amenities", "dead bolt")
        self.checkbox_by_id("amenities", "exterior light")
        self.checkbox_by_id("amenities", "intercom")
        self.checkbox_by_id("amenities", "security guard")
        self.checkbox_by_id("amenities", "security system")
        self.checkbox_by_id("amenities", "video surveillance")
        # Utilities
        self.checkbox_by_id("amenities", "cable")
        self.checkbox_by_id("amenities", "electricity")
        self.checkbox_by_id("amenities", "gas")
        self.checkbox_by_id("amenities", "heat")
        self.checkbox_by_id("amenities", "high-speed internet")
        self.checkbox_by_id("amenities", "hot water")
        self.checkbox_by_id("amenities", "local phone")
        self.checkbox_by_id("amenities", "recycling")
        self.checkbox_by_id("amenities", "trash")
        self.checkbox_by_id("amenities", "water")
        # Parking
        self.checkbox_by_id("amenities", "garage")
        self.checkbox_by_id("amenities", "no parking")
        self.checkbox_by_id("amenities", "off street parking")
        self.checkbox_by_id("amenities", "on street parking")
        # Laundry
        self.checkbox_by_id("amenities", "laundry room")
        self.checkbox_by_id("amenities", "no laundry")
        self.checkbox_by_id("amenities", "wd hookups")
        self.checkbox_by_id("amenities", "wd in unit")
        # Description
        description = self.payload.get_value("amenities", "description")
        iframe = self.driver.find_element_by_id(self.payload.id("amenities", "tinymce"))
        self.driver.switch_to.frame(iframe)
        tinymce = self.driver.find_element_by_id(self.payload.id("amenities", "description"))
        tinymce.click()
        tinymce.send_keys(description)
        self.driver.switch_to.default_content()

        self.driver.find_element_by_id(self.payload.id("amenities", "wd in unit")).submit()
    def fill_contact(self):
        self.log.warning("The contact page hasn't been implemented. Fill manually.")
        #self.wait.until(EC.presence_of_element_located((By.XPATH, self.payload.contact_link)))
    
        #result = self.driver.find_element_by_xpath(self.payload.contacat_link)
        #result.click()
    
        return True
    def fill_photos(self):
        self.log.warning("The photos page hasn't been implemented. Fill manually.")
        #self.wait.until(EC.presence_of_element_located((By.XPATH, self.payload.photos_link)))
    
        #result = self.driver.find_element_by_xpath(self.payload.photos_link)
        #result.click()

        return True
    def close(self):
        self.driver.close()
    def quit(self):
        self.driver.quit()
