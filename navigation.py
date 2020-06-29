import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Navigator:
    def __init__(self):
            self.log = logging.getLogger("root")
            self.log.debug("Initializing Navigator.")

            self.driver = webdriver.Chrome()
            self.wait = WebDriverWait(self.driver, 100)
            # TODO
            #FluentWait<WebDriver>(driver)
            #    .withTimeout(50, TimeUnit.SECONDS)
            #    .pollingevery(3, TimeUnit.SECONDS)
            #    .ignoring(NoSuchElementException.class)

            if self.driver == None:
                self.log.error("ChromeDrivee not found. Exiting. [%s]" % self.driver)
                sys.exit()
    def dropdown(self, element, value):
        for option in element.find_elements_by_tag_name('option'):
            if option.text.strip().lower() == str(value).lower():
                option.click()
    def checkbox(self, element, value):
        if value == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", element)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", element)
    def wait_for_xpath_fp(self, element, fpid):
        self.log.debug("The floorplan id is " + str(fpid)) 
        self.log.debug("Need to parse element and inject fpid.")
        self.log.info("The program has semi-expectedly stopped. Some features are still being developed.")
        sys.exit()
        self.log.info("Waiting for element to load. [%s]" % element)
        self.wait.until(EC.presence_of_element_located((By.XPATH, element)))
        return xpath
    def wait_for_xpath(self, element):
        self.log.debug("Waiting for element to load. [%s]" % element)
        self.wait.until(EC.presence_of_element_located((By.XPATH, element)))
        self.log.debug("Element loaded.")
    def wait_for_id(self, element):
        self.log.debug("Waiting for element to load. [%s]" % element)
        self.wait.until(EC.presence_of_element_located((By.ID, element)))
        self.log.debug("Element loaded.")
    def login(self, payload):
        url = payload.get_value("login", "login url")
        logging.info("Log in to %s", url)
        login = self.driver.get(url)

        link = payload.xpath("login", "login link")
        self.wait_for_xpath(link)
        link = self.driver.find_element_by_xpath(link)
        link.click()

        username = payload.get_value("login", "username")
        password = payload.get_value("login", "password")
        user_input = payload.id("login", "username")
        password_input = payload.id("login", "password")

        self.wait_for_id(user_input)
        
        self.driver.find_element_by_id(user_input).send_keys(username)
        self.driver.find_element_by_id(password_input).send_keys(password)

        submit = payload.xpath("login", "submit button")
        self.driver.find_element(By.XPATH, submit).click()
    def add_listing(self, payload):
        url = payload.get_value("login", "add listing url")
        logging.debug("Loading new listing page.")
        login = self.driver.get(url)

        self.wait_for_id(payload.id("location", "full address"))
    
        result = self.driver.find_element_by_xpath(payload.xpath("location", "full address input"))
        result.send_keys(payload.get_value("location", "address"))
        result.send_keys(Keys.ENTER)
    def fill_address(self, payload):
        self.wait_for_id(payload.id("location", "address"))
   
        logging.debug("Filling in address details.")
        result = self.driver.find_element_by_id(payload.id("location", "address"))
        result.send_keys(payload.get_value("location", "address"))

        result = self.driver.find_element_by_id(payload.id("location", "city"))
        result.send_keys(payload.get_value("location", "city"))
        result = self.driver.find_element_by_id(payload.id("location", "zip"))
        result.send_keys(payload.get_value("location", "zip"))
    
        self.dropdown(self.driver.find_element_by_id(payload.id("location", "state")), payload.get_value("location", "state"))

        element = self.driver.find_element_by_id(payload.id("location", "exact flag"))
        self.checkbox(element , payload.get_bool("location", "exact flag"))

        form = self.driver.find_element_by_xpath(payload.xpath("location", "address form"))
        form.submit()

        self.wait_for_id(payload.id("location", "property name"))
    
        result = self.driver.find_element_by_id(payload.id("location", "property name"))
        description = payload.get_value("location", "property name")
        if description == None:
            description = ("[JJ] ", payload.get_value("location", "full address"))
        result.send_keys(description)
        result.send_keys(Keys.ENTER)
    def fill_rent(self, payload):
        self.wait_for_xpath(payload.xpath("rent", "rent link"))
        link = self.driver.find_element_by_xpath(payload.xpath("rent", "rent link"))
        link.click()

        self.dropdown(self.driver.find_element_by_id(payload.id("rent", "building type")), payload.get_value("rent", "building type"))

        if payload.get_bool("rent", "floorplans yes"):
            radio = self.driver.find_element_by_id(payload.id("rent", "floorplans yes"))
        else:
            radio = self.driver.find_element_by_id(payload.id("rent", "floorplans no"))
        radio.click()

        element = self.driver.find_element_by_id(payload.id("rent", "broker"))
        self.checkbox(element, payload.get_bool("rent", "broker"))
        element = self.driver.find_element_by_id(payload.id("rent", "first"))
        self.checkbox(element, payload.get_bool("rent", "first"))
        element = self.driver.find_element_by_id(payload.id("rent", "last"))
        self.checkbox(element, payload.get_bool("rent", "last"))
        element = self.driver.find_element_by_id(payload.id("rent", "upfront"))
        self.checkbox(element, payload.get_bool("rent", "upfront"))
        element = self.driver.find_element_by_id(payload.id("rent", "references"))
        self.checkbox(element, payload.get_bool("rent", "references"))
        element = self.driver.find_element_by_id(payload.id("rent", "security"))
        self.checkbox(element, payload.get_bool("rent", "security"))

        result = self.driver.find_element_by_id(payload.id("rent", "specials"))
        specials = payload.get_value("rent", "specials")
        if specials == None:
            specials = " "
        result.send_keys(specials)
        result.send_keys(Keys.ENTER)

        if payload.get_bool("rent", "floorplans yes"):
            self.log.warning("This listing contains multiple floorplans. They will need to be filled manually.")
            #self.fill_floorplans(payload)
        else:
            self.fill_floorplan(payload)
    def fill_floorplan(self, payload):
        self.wait_for_id(payload.id("rent", "bedrooms"))
        
        self.dropdown(self.driver.find_element_by_id(payload.id("rent", "bedrooms")), payload.get_value("rent", "bedrooms"))
        self.dropdown(self.driver.find_element_by_id(payload.id("rent", "bathrooms")), payload.get_value("rent", "bathrooms"))
        result = self.driver.find_element_by_id(payload.id("rent", "square feet"))
        result.send_keys(payload.get_value("rent", "square feet"))
        result = self.driver.find_element_by_id(payload.id("rent", "monthly rent"))
        result.send_keys(Keys.CONTROL + "a")
        result.send_keys(Keys.DELETE)
        result.send_keys("$" + str(payload.get_value("rent", "monthly rent")))
        self.dropdown(self.driver.find_element_by_id(payload.id("rent", "type")), payload.get_value("rent", "type"))

        result = self.driver.find_element_by_id(payload.id("rent", "specials"))
        result.send_keys(Keys.ENTER)
    def fill_floorplans(self, payload):
        self.log.warning("Floorplans are still being implemented.")
        # TODO Figure out how to replace fp id in the css id
        # TODO Figure out how to generate fp member names to include fp number

        self.wait_for_xpath(payload.xpath("floorplans", "link"))
        link = self.driver.find_element_by_xpath(payload.xpath("floorplans", "link"))
        link.click()

        i = 0
        fp_number = payload.get_value("floorplans", "total number")

        while i < fp_number:
            url = str(self.driver.current_url)
            fp_id = url.rsplit('/', 1)[-1]

            #FIXME Should click edit instead of add for the first floorplan
            xpath = self.wait_for_xpath(payload.xpath("floorplans", "add link"))
            link = self.driver.find_element_by_xpath(payload.xpath("floorplans", "add link"))
            link.click()
            self.log.warning("Some features are still being implemented. Exiting program.")
            sys.exit()

            xpath = self.wait_for_xpath_fp(payload.xpath("floorplans", "add link", fpid))

            result = self.driver.find_element_by_xpath(payload.xpath("floorplans", "name"))
            result.send_keys(payload.get_value("location", "address"))
            result.send_keys(Keys.ENTER)

            i = i+1
        sys.exit()
    def fill_specifics(self, payload):
        self.wait_for_xpath(payload.xpath("specifics", "link"))
        link = self.driver.find_element_by_xpath(payload.xpath("specifics", "link"))
        link.click()

        if not payload.get_bool("rent", "floorplans yes"):
            dd = payload.id("specifics", "max occupants")
            value = payload.get_value("specifics", "max occupants")
            self.dropdown(self.driver.find_element_by_id(dd), value)
        #if option.text.strip() != str(payload.listing.number_of_occupants):
        #    print("The number of occupants needs to be manually adjusted. [", payload.listing.number_of_occupants, "]")

        element = self.driver.find_element_by_id(payload.id("specifics", "allow sublet"))
        self.checkbox(element, payload.get_bool("specifics", "allow sublet"))
        element = self.driver.find_element_by_id(payload.id("specifics", "is sublet"))
        self.checkbox(element, payload.get_bool("specifics", "is sublet"))
        element = self.driver.find_element_by_id(payload.id("specifics", "roommate situation"))
        self.checkbox(element, payload.get_bool("specifics", "roommate situation"))
        
        self.log.warning("The move in date hasn't been implemented. It needs to be filled manually.")

        #if str(payload.listing.availability_date).lower() == "now": #FIXME Now, date, between
        #    result = self.driver.find_element_by_id(payload.available_now_id)
        #else: #FIXME check if date or range and enter range
        #    print("Fix me!!! range and date")
        #    print("With start and end input id's and spreadsheet cell parsing.")
        #    result = self.driver.find_element_by_id(payload.available_range_id)
        #    result = self.driver.find_element_by_id(payload.available_date_id)
        #result.click()

        renew = str(payload.get_value("specifics", "renew yes")).lower()
        if renew == "unknown":
            radio = self.driver.find_element_by_id(payload.id("specifics", "renew unknown"))
        elif renew == "y":
            radio = self.driver.find_element_by_id(payload.id("specifics", "renew yes"))
        else:
            radio = self.driver.find_element_by_id(payload.id("specifics", "renew no"))
        radio.click()
        radio.submit()
    def fill_amenities(self, payload):
        self.wait_for_xpath(payload.xpath("amenities", "link"))
        link = self.driver.find_element_by_xpath(payload.xpath("amenities", "link"))
        link.click()

        self.log.warning("The pet dropdown hasn't been fully implemented. Check that the data is accurate.")
        #FIXME
        dd = self.driver.find_element_by_id(payload.id("amenities", "pet policy"))
        pets = str(payload.get_value("amenities", "pet policy")).lower()
        if pets == "not allowed":
            self.dropdown(dd, "pets not allowed")
        elif "considered" in pets:
            self.dropdown(dd, "pets considered")
        else:
            self.dropdown(dd, "pets allowed")

        if "cat" in pets:
            element = self.driver.find_element_by_id(payload.id("amenities", "cats"))
            self.checkbox(element, True)
        if "dog" in pets:
            element = self.driver.find_element_by_id(payload.id("amenities", "dogs"))
            self.checkbox(element, True)

        self.dropdown(self.driver.find_element_by_id(payload.id("amenities", "lead paint")), payload.get_value("amenities", "lead paint"))
    
        # Features
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "ac")), payload.get_value("amenities", "ac"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "carpet")), payload.get_value("amenities", "carpet"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "dining room")), payload.get_value("amenities", "dining room"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "disability access")), payload.get_value("amenities", "disability access"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "dishwasher")), payload.get_value("amenities", "dishwasher"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "fireplace")), payload.get_value("amenities", "fireplace"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "furnished")), payload.get_value("amenities", "furnished"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "garbage disposal")), payload.get_value("amenities", "garbage disposal"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "hardwood")), payload.get_value("amenities", "hardwood"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "internet")), payload.get_value("amenities", "internet"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "living room")), payload.get_value("amenities", "living room"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "microwave")), payload.get_value("amenities", "microwave"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "patio")), payload.get_value("amenities", "patio"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "private garden")), payload.get_value("amenities", "private garden"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "shared garden")), payload.get_value("amenities", "shared garden"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "smoke free")), payload.get_value("amenities", "smoke free"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "additional storage")), payload.get_value("amenities", "additional storage"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "included storage")), payload.get_value("amenities", "included storage"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "study")), payload.get_value("amenities", "study"))
        #Agency
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "agent fee")), payload.get_value("amenities", "agent fee"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "no fee")), payload.get_value("amenities", "no fee"))
        # Community
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "fitness room")), payload.get_value("amenities", "fitness room"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "individual leases")), payload.get_value("amenities", "individual leases"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "near bus")), payload.get_value("amenities", "near bus"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "near T")), payload.get_value("amenities", "near T"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "pool")), payload.get_value("amenities", "pool"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "roommate matching")), payload.get_value("amenities", "roommate matching"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "tennis court")), payload.get_value("amenities", "tennis court"))
        # Lease
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "12 months")), payload.get_value("amenities", "12 months"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "9 months")), payload.get_value("amenities", "9 months"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "fall sublet")), payload.get_value("amenities", "fall sublet"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "flexible lease")), payload.get_value("amenities", "flexible lease"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "month to month")), payload.get_value("amenities", "month to month"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "short term lease")), payload.get_value("amenities", "short term lease"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "spring sublet")), payload.get_value("amenities", "spring sublet"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "summer sublet")), payload.get_value("amenities", "summer sublet"))
        # Security
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "courtesy officer")), payload.get_value("amenities", "courtesy officer"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "dead bolt")), payload.get_value("amenities", "dead bolt"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "exterior light")), payload.get_value("amenities", "exterior light"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "intercom")), payload.get_value("amenities", "intercom"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "security guard")), payload.get_value("amenities", "security guard"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "security system")), payload.get_value("amenities", "security system"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "video surveillance")), payload.get_value("amenities", "video surveillance"))
        # Utilities
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "cable")), payload.get_value("amenities", "cable"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "electricity")), payload.get_value("amenities", "electricity"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "gas")), payload.get_value("amenities", "gas"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "heat")), payload.get_value("amenities", "heat"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "high-speed internet")), payload.get_value("amenities", "high-speed internet"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "hot water")), payload.get_value("amenities", "hot water"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "local phone")), payload.get_value("amenities", "local phone"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "recycling")), payload.get_value("amenities", "recycling"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "trash")), payload.get_value("amenities", "trash"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "water")), payload.get_value("amenities", "water"))
        # Parking
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "garage")), payload.get_value("amenities", "garage"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "no parking")), payload.get_value("amenities", "no parking"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "off street parking")), payload.get_value("amenities", "off street parking"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "on street parking")), payload.get_value("amenities", "on street parking"))
        # Laundry
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "laundry room")), payload.get_value("amenities", "laundry room"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "no laundry")), payload.get_value("amenities", "no laundry"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "wd hookups")), payload.get_value("amenities", "wd hookups"))
        self.checkbox(self.driver.find_element_by_id(payload.id("amenities", "wd in unit")), payload.get_value("amenities", "wd in unit"))
        # Description
        description = payload.get_value("amenities", "description")
        iframe = self.driver.find_element_by_id(payload.id("amenities", "tinymce"))
        self.driver.switch_to.frame(iframe)
        tinymce = self.driver.find_element_by_id(payload.id("amenities", "description"))
        tinymce.click()
        tinymce.send_keys(description)
        self.driver.switch_to.default_content()

        self.driver.find_element_by_id(payload.id("amenities", "wd in unit")).submit()
    def fill_contact_page(self, payload):
        self.log.warning("The contact page hasn't been implemented. Fill manually.")
        #self.wait.until(EC.presence_of_element_located((By.XPATH, payload.contact_link)))
    
        #result = self.driver.find_element_by_xpath(payload.contacat_link)
        #result.click()
    
        return True
    def fill_photos_page(self, payload):
        self.log.warning("The photos page hasn't been implemented. Fill manually.")
        #self.wait.until(EC.presence_of_element_located((By.XPATH, payload.photos_link)))
    
        #result = self.driver.find_element_by_xpath(payload.photos_link)
        #result.click()

        return True
    def close(self):
        self.driver.close()
    def quit(self):
        self.driver.quit()
