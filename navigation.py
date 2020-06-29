import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Navigator:
    def __init__(self, payload):
            self.log = logging.getLogger("bLog")
            self.log.debug("Initializing Navigator.")
            self.driver = webdriver.Chrome()
            self.wait = WebDriverWait(self.driver, 100)
            # TODO
            #FluentWait<WebDriver>(driver)
            #    .withTimeout(50, TimeUnit.SECONDS)
            #    .pollingevery(3, TimeUnit.SECONDS)
            #    .ignoring(NoSuchElementException.class)

            if self.driver == None:
                self.log.error("ChromeDriver not found. Exiting. [%s]" % self.driver)
                sys.exit()

            self.payload = payload
    def send_keys_fp_by_id(self, page, name, fp_nb, fp_id):
        self.log.debug("send_keys_fp_by_id")
        self.log.debug("Name [" + name + "]")
        name = name + str(fp_nb)
        self.log.debug("=> " + name)

        element_id = self.payload.id(page, name)
        self.log.debug("Element [" + str(element_id) + "]")
        element_id = element_id.replace("FP_ID", str(fp_id))
        self.log.debug("=> " + element_id)

        value = self.payload.get_value(page, name)
        if value:
            element = self.driver.find_element_by_id(element_id)
            element.send_keys(value)
    def checkbox_fp_by_id(self, page, name, fp_nb, fp_id):
        self.log.debug("checkbox_fp_by_id")
        self.log.debug("Name [" + name + "]")
        name = name + str(fp_nb)
        self.log.debug("=> " + name)

        element_id = self.payload.id(page, name)
        self.log.debug("Element [" + str(element_id) + "]")
        element_id = element_id.replace("FP_ID", str(fp_id))
        self.log.debug("=> " + element_id)

        element = self.driver.find_element_by_id(element_id)
        value = self.payload.get_value(page, name)
        self.log.debug("Value = " + str(value))
        #FIXME Add a type field to the payload data for each element
        self.log.debug("FIX ME NOW! Add type to payload.")
        if str(value).lower() == "y": value = True
        if value == None: value = False 

        self.log.debug("Page = " + str(page) + "\nName = " + str(name))
        self.log.debug("Element = " + str(element) + "\nValue = " + str(value))
        if value == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", element)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", element)
    def dropdown_fp_by_id(self, page, name, fp_nb, fp_id):
        self.log.debug("dropdown_fp_by_id")
        self.log.debug("Name [" + name + "]")
        name = name + str(fp_nb)
        self.log.debug("=> " + name)
        

        element_id = self.payload.id(page, name)
        self.log.debug("Element [" + str(element_id) + "]")
        element_id = element_id.replace("FP_ID", str(fp_id))
        self.log.debug("=> " + element_id)

        element = self.driver.find_element_by_id(element_id)
        value = self.payload.get_value(page, name)
        for option in element.find_elements_by_tag_name('option'):
            if option.text.strip().lower() == str(value).lower():
                option.click()
    def dropdown_by_id(self, page, name):
        element = self.driver.find_element_by_id(self.payload.id(page, name))
        value = self.payload.get_value(page, name)
        for option in element.find_elements_by_tag_name('option'):
            if option.text.strip().lower() == str(value).lower():
                option.click()
    def checkbox_by_id(self, page, name):
        element = self.driver.find_element_by_id(self.payload.id(page, name))
        value = self.payload.get_value(page, name)
        #FIXME Add a type field to the payload data for each element
        self.log.debug("FIX ME NOW! Add type to payload.")
        if str(value).lower() == "y": value = True
        if value == None: value = False 

        self.log.debug("Page = " + str(page) + "\nName = " + str(name))
        self.log.debug("Element = " + str(element) + "\nValue = " + str(value))
        if value == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", element)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", element)
    def wait_for_xpath_fp(self, element, fpid):
        self.log.debug("The floorplan id is " + str(fpid)) 
        self.log.debug("Need to parse element and inject fpid.")
        self.log.info("The program has semi-expectedly stopped. Some features are still being developed.")
        sys.exit()
        self.log.debug("Waiting for element to load. [" + str(element) + "]")
        self.wait.until(EC.presence_of_element_located((By.XPATH, element)))
        return xpath
    def wait_for_xpath(self, element):
        self.log.debug("Waiting for element to load. [" + str(element) + "]")
        self.wait.until(EC.presence_of_element_located((By.XPATH, element)))
        self.log.debug("Element loaded.")
    def wait_for_id(self, element):
        self.log.debug("Waiting for element to load. [" + str(element) + "]")
        self.wait.until(EC.presence_of_element_located((By.ID, element)))
        self.log.debug("Element loaded.")
    def login(self):
        url = self.payload.get_value("login", "login url")
        logging.info("Log in to %s", url)
        login = self.driver.get(url)

        link = self.payload.xpath("login", "login link")
        self.wait_for_xpath(link)
        link = self.driver.find_element_by_xpath(link)
        link.click()

        username = self.payload.get_value("login", "username")
        password = self.payload.get_value("login", "password")
        user_input = self.payload.id("login", "username")
        password_input = self.payload.id("login", "password")

        self.wait_for_id(user_input)
        
        self.driver.find_element_by_id(user_input).send_keys(username)
        self.driver.find_element_by_id(password_input).send_keys(password)

        submit = self.payload.xpath("login", "submit button")
        self.driver.find_element(By.XPATH, submit).click()
    def add_listing(self):
        url = self.payload.get_value("login", "add listing url")
        logging.debug("Loading new listing page.")
        login = self.driver.get(url)

        self.wait_for_id(self.payload.id("location", "full address"))
    
        result = self.driver.find_element_by_xpath(self.payload.xpath("location", "full address input"))
        result.send_keys(self.payload.get_value("location", "address"))
        result.send_keys(Keys.ENTER)
    def fill_address(self):
        self.wait_for_id(self.payload.id("location", "address"))
   
        logging.debug("Filling in address details.")
        result = self.driver.find_element_by_id(self.payload.id("location", "address"))
        result.send_keys(self.payload.get_value("location", "address"))

        result = self.driver.find_element_by_id(self.payload.id("location", "city"))
        result.send_keys(self.payload.get_value("location", "city"))
        result = self.driver.find_element_by_id(self.payload.id("location", "zip"))
        result.send_keys(self.payload.get_value("location", "zip"))
    
        self.dropdown_by_id("location", "state")

        element = self.driver.find_element_by_id(self.payload.id("location", "exact flag"))
        self.checkbox_by_id("location", "exact flag")

        form = self.driver.find_element_by_xpath(self.payload.xpath("location", "address form"))
        form.submit()

        self.wait_for_id(self.payload.id("location", "property name"))
    
        result = self.driver.find_element_by_id(self.payload.id("location", "property name"))
        description = self.payload.get_value("location", "property name")
        if description == None:
            description = ("[Auto] ", self.payload.get_value("location", "full address"))
        result.send_keys(description)
        result.send_keys(Keys.ENTER)
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

            url = str(self.driver.current_url)
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
    def fill_contact_page(self):
        self.log.warning("The contact page hasn't been implemented. Fill manually.")
        #self.wait.until(EC.presence_of_element_located((By.XPATH, self.payload.contact_link)))
    
        #result = self.driver.find_element_by_xpath(self.payload.contacat_link)
        #result.click()
    
        return True
    def fill_photos_page(self):
        self.log.warning("The photos page hasn't been implemented. Fill manually.")
        #self.wait.until(EC.presence_of_element_located((By.XPATH, self.payload.photos_link)))
    
        #result = self.driver.find_element_by_xpath(self.payload.photos_link)
        #result.click()

        return True
    def close(self):
        self.driver.close()
    def quit(self):
        self.driver.quit()
