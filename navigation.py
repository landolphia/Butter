import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Navigator:
    def __init__(self):
            self.log = logging.getLogger("root")
            self.log.info("Initializing Navigator.")

            self.driver = webdriver.Chrome()
            self.wait = WebDriverWait(self.driver, 100)

            if self.driver == None:
                self.log.error("Driver not loaded. Exiting program. [%s]" % self.driver)
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
    def wait_for_xpath(self, element):
        self.log.info("Waiting for element to load. [%s]" % element)
        self.wait.until(EC.presence_of_element_located((By.XPATH, element)))
        self.log.info("Element loaded.")
    def wait_for_id(self, element):
        self.log.info("Waiting for element to load. [%s]" % element)
        self.wait.until(EC.presence_of_element_located((By.ID, element)))
        self.log.info("Element loaded.")
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
        logging.info("Loading new listing page.")
        login = self.driver.get(url)

        self.wait_for_id(payload.id("location", "full address"))
    
        result = self.driver.find_element_by_xpath(payload.xpath("location", "full address input"))
        result.send_keys(payload.get_value("location", "address"))
        result.send_keys(Keys.ENTER)
    def fill_address(self, payload):
        self.wait_for_id(payload.id("location", "address"))
   
        logging.info("Filling in address details.")
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

        print("TODO, fix floorplan, add loop for Y.")
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
        print("ENDTODO.")

        result = self.driver.find_element_by_id(payload.id("rent", "specials"))
        result.send_keys(Keys.ENTER)
    def fill_specifics(self, payload):
        print("TODO!!!!")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.specifics_link)))
    
        result = self.driver.find_element_by_xpath(payload.specifics_link)
        result.click()

        result = self.driver.find_element_by_id(payload.max_occupants_id)
        for option in result.find_elements_by_tag_name('option'):
            if option.text.strip() == str(payload.listing.number_of_occupants):
                option.click()
                break
        if option.text.strip() != str(payload.listing.number_of_occupants):
            print("The number of occupants needs to be manually adjusted. [", payload.listing.number_of_occupants, "]")

        result = self.driver.find_element_by_id(payload.allow_sublet_id)

        self.set_checkbox(payload.ac_id, payload.listing.ac)

        if payload.listing.allow_subletting == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", result)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", result)
            
        result = self.driver.find_element_by_id(payload.is_sublet_id)
        if payload.listing.is_sublet == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", result)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", result)

        result = self.driver.find_element_by_id(payload.roommate_situation_id)
        if payload.listing.roommate_situation == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", result)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", result)

        if str(payload.listing.availability_date).lower() == "now": #FIXME Now, date, between
            result = self.driver.find_element_by_id(payload.available_now_id)
        else: #FIXME check if date or range and enter range
            print("Fix me!!! range and date")
            print("With start and end input id's and spreadsheet cell parsing.")
            result = self.driver.find_element_by_id(payload.available_range_id)
            result = self.driver.find_element_by_id(payload.available_date_id)
        result.click()

        renew = str(payload.listing.availability_renew).lower()
        if renew == "unknown":
            result = self.driver.find_element_by_id(payload.available_renew_unk_id)
        elif renew == "y":
            result = self.driver.find_element_by_id(payload.available_renew_yes_id)
        else:
            result = self.driver.find_element_by_id(payload.available_renew_no_id)
        result.click()

        return True
    def fill_amenities(self, payload):
        print("Waiting for amenities link to load.")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.amenities_link)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.amenities_link)
        result.click()
    
        result = self.driver.find_element_by_id(payload.pet_policy_id)
        #FIXME Cat->allowed?
        print("FIXME: Meow")
        for option in result.find_elements_by_tag_name('option'):
            if option.text.strip() == payload.listing.pet_policy:
                option.click()

        result = self.driver.find_element_by_id(payload.lead_paint_id)
        lead = str(payload.listing.lead_paint).lower()
        for option in result.find_elements_by_tag_name('option'):
            if option.text.strip().lower == lead:
                option.click()

        # Features
        self.set_checkbox(payload.ac_id, payload.listing.ac)
        self.set_checkbox(payload.carpet_id, payload.listing.carpet)
        self.set_checkbox(payload.dining_room_id, payload.listing.dining_room)
        self.set_checkbox(payload.disability_access_id, payload.listing.disability_access)
        self.set_checkbox(payload.dishwasher_id, payload.listing.dishwasher)
        self.set_checkbox(payload.fireplace_id, payload.listing.fireplace)
        self.set_checkbox(payload.furnished_id, payload.listing.furnished)
        self.set_checkbox(payload.garbage_disp_id, payload.listing.garbage_disposal)
        self.set_checkbox(payload.hardwood_id, payload.listing.hardwood_floors)
        self.set_checkbox(payload.internet_id, payload.listing.high_speed_internet)
        self.set_checkbox(payload.living_room_id, payload.listing.living_room)
        self.set_checkbox(payload.microwave_id, payload.listing.microwave)
        self.set_checkbox(payload.patio_id, payload.listing.patio)
        self.set_checkbox(payload.private_garden_id, payload.listing.private_garden)
        self.set_checkbox(payload.shared_garden_id, payload.listing.shared_garden)
        self.set_checkbox(payload.smoke_free_id, payload.listing.smoke_free)
        self.set_checkbox(payload.additional_storage_id, payload.listing.storage_additional)
        self.set_checkbox(payload.included_storage_id, payload.listing.storage_included)
        self.set_checkbox(payload.study_id, payload.listing.study)
        # Agency
        self.set_checkbox(payload.agent_fee_id, payload.listing.fee_agent_broker)
        self.set_checkbox(payload.no_fee_id, payload.listing.no_fee)
        # Community
        self.set_checkbox(payload.fitness_room_id, payload.listing.fitness_room)
        self.set_checkbox(payload.individual_leases_id, payload.listing.individual_leases)
        self.set_checkbox(payload.near_bus_id, payload.listing.near_bus_stop)
        self.set_checkbox(payload.near_T_id, payload.listing.near_T_stop)
        self.set_checkbox(payload.pool_id, payload.listing.pool)
        self.set_checkbox(payload.roommate_matching_id, payload.listing.roommate_matching)
        self.set_checkbox(payload.tennis_court_id, payload.listing.tennis_court)
        # Lease
        self.set_checkbox(payload.twelve_months_id, payload.listing.twelve_months)
        self.set_checkbox(payload.nine_months_id, payload.listing.nine_months)
        self.set_checkbox(payload.fall_sublet_id, payload.listing.fall_sublet)
        self.set_checkbox(payload.flexible_lease_id, payload.listing.flexible)
        self.set_checkbox(payload.month_to_month_id, payload.listing.month_to_month)
        self.set_checkbox(payload.short_term_lease_id, payload.listing.short_term)
        self.set_checkbox(payload.spring_sublet_id, payload.listing.spring_sublet)
        self.set_checkbox(payload.summer_sublet_id, payload.listing.summer_sublet)
        # Security
        self.set_checkbox(payload.courtesy_officer_id, payload.listing.courtesy_officer)
        self.set_checkbox(payload.dead_bolt_id, payload.listing.dead_bolt)
        self.set_checkbox(payload.exterior_light_id, payload.listing.exterior_lighting)
        self.set_checkbox(payload.intercom_id, payload.listing.intercom)
        self.set_checkbox(payload.security_guard_id, payload.listing.security_guard)
        self.set_checkbox(payload.security_system_id, payload.listing.security_system)
        self.set_checkbox(payload.video_surv_id, payload.listing.video_surveillance)
        # Utilities
        self.set_checkbox(payload.cable_id, payload.listing.cable)
        self.set_checkbox(payload.electricity_id, payload.listing.electricity)
        self.set_checkbox(payload.gas_id, payload.listing.gas)
        self.set_checkbox(payload.heat_id, payload.listing.heat)
        self.set_checkbox(payload.util_internet_id, payload.listing.high_speed_internet)
        self.set_checkbox(payload.hot_water_id, payload.listing.hot_water)
        self.set_checkbox(payload.local_phone_id, payload.listing.local_phone)
        self.set_checkbox(payload.recycling_id, payload.listing.recycling)
        self.set_checkbox(payload.trash_id, payload.listing.trash_removal)
        self.set_checkbox(payload.water_id, payload.listing.water_sewer)
        # Parking
        self.set_checkbox(payload.garage_park_id, payload.listing.garage_parking)
        self.set_checkbox(payload.no_parking_id, payload.listing.no_parking)
        self.set_checkbox(payload.off_street_park_id, payload.listing.off_street_parking)
        self.set_checkbox(payload.on_street_park_id, payload.listing.on_street_parking)
        # Laundry
        self.set_checkbox(payload.laundry_in_comm_id, payload.listing.laundry_room_in_community)
        self.set_checkbox(payload.no_laundry_id, payload.listing.no_laundry_in_unit)
        self.set_checkbox(payload.wd_hookups_id, payload.listing.washer_dryer_hookups)
        self.set_checkbox(payload.wd_in_unit, payload.listing.washer_dryer_in_unit)
        # Description
        #TODO !!!! FIXME
        result = self.driver.find_element_by_id(payload.description_id)
        result.send_keys(payload.listing.description)

        return True
    def fill_contact_page(self, payload):
        print("TODO!!!!")
        print("Waiting for contact link to load.")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.contact_link)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.contacat_link)
        result.click()
    
        return True
    def fill_photos_page(self, payload):
        print("TODO!!!!")
        print("Waiting for photos link to load.")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.photos_link)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.photos_link)
        result.click()

        return True
    def close(self):
        self.driver.close()
    def quit(self):
        self.driver.quit()
