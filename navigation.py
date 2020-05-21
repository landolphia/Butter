from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Navigator:
    def __init__(self, debug):
            self.search_url = "https://www.google.com/search?q="
            self.driver = webdriver.Chrome()
            self.wait = WebDriverWait(self.driver, 100)
            self.DEBUG = debug
    def login(self, payload):
        result = None
        
        if self.driver == None:
            print ("Driver not loaded. Exiting program. [", self.driver, "]")
            sys.exit()
    
        if self.DEBUG != None:
            print("Signing into ", payload.login_url)
    
        login = self.driver.get(payload.login_url)
        
        print("Waiting for page to load.")
        self.wait.until(EC.presence_of_element_located((By.ID, payload.form_id)))
        print("Page loaded.")
        link = self.driver.find_element(By.XPATH, payload.login_link)
        print("Clicking on link to show form.")
        link.click()
    
        print("Waiting for form to load.")
        self.wait.until(EC.presence_of_element_located((By.ID, payload.user_id)))
        print("Loaded.")
    
        self.driver.find_element_by_id(payload.user_id).send_keys(payload.username)
    
        self.driver.find_element_by_id(payload.pass_id).send_keys(payload.password)
    
        print("Waiting for submit button to load.")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.button)))
        print("Loaded.")
    
        result = self.driver.find_element(By.XPATH, payload.button).click()
    
        return True 
    def add_listing(self, payload):
        print("Loading new listing page.")
        login = self.driver.get(payload.add_listing_url)
    
        return True 
    def fill_full_address(self, payload):
        print("Waiting for address input to load.")
        self.wait.until(EC.presence_of_element_located((By.ID, payload.full_address_div_id)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.address_input)
        print("Input: ", result)
        result.send_keys(payload.listing.full_address)
        result.send_keys(Keys.ENTER)
    
        return True 
    def fill_address(self, payload):
        print("Waiting for address input to load.")
        self.wait.until(EC.presence_of_element_located((By.ID, payload.address_id)))
        print("Loaded.")
   
        print("Filling in address details.")
        result = self.driver.find_element_by_id(payload.address_id)
        result.send_keys(payload.listing.street_num, " ", payload.listing.street_name)
        result = self.driver.find_element_by_id(payload.city_id)
        result.send_keys(payload.listing.city)
        result = self.driver.find_element_by_id(payload.zip_id)
        result.send_keys(payload.listing.zip)
    
        dd = self.driver.find_element_by_id(payload.state_id)
        for option in dd.find_elements_by_tag_name('option'):
            if option.text.strip() == payload.listing.state:
                option.click()

        result = self.driver.find_element_by_id(payload.exact_flag_id)
        if result.get_attribute("checked") != payload.listing.display_exact_address:
                result.click()

        result = self.driver.find_element_by_xpath(payload.address_form_xpath)
        result.submit()

        return True 
    def fill_location_page(self, payload):
        print("Waiting for headline input to load.")
        self.wait.until(EC.presence_of_element_located((By.ID, payload.property_name_input_id)))
        print("Loaded.")
    
        result = self.driver.find_element_by_id(payload.property_name_input_id)
        result.send_keys(payload.listing.property_name)
        result.send_keys(Keys.ENTER)
    
        return True 
    def fill_rent_page(self, payload):
        print("Waiting for rent link to load.")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.rent_link)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.rent_link)
        result.click()
        input("Press enter to go on.")
        #self.building_type_select_id = "buildingtype"
        #self.multiple_floorplans_radio_no_id = "multi-unit-no"
        #self.multiple_floorplans_radio_yes_id = "multi-unit-yes"
        #self.reqs_broker_id = "security_deposit_amenities-231"
        #self.reqs_first_id = "security_deposit_amenities-161"
        #self.reqs_last_id = "security_deposit_amenities-162"
        #self.reqs_upfront_id = "security_deposit_amenities-165"
        #self.reqs_references_id = "security_deposit_amenities-164"
        #self.reqs_security_id = "security_deposit_amenities-163"
        #self.specials_id = "specials 
    
        return True
    def fill_specifics_page(self, payload):
        print("Waiting for specifics link to load.")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.specifics_link)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.specifics_link)
        result.click()
        input("Press enter to go on.")
    
        return True
    def fill_amenities_page(self, payload):
        print("Waiting for amenities link to load.")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.amenities_link)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.amenities_link)
        result.click()
        input("Press enter to go on.")
    
        return True
    def fill_contact_page(self, payload):
        print("Waiting for contact link to load.")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.contact_link)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.contacat_link)
        result.click()
        input("Press enter to go on.")
    
        return True
    def fill_photos_page(self, payload):
        print("Waiting for photos link to load.")
        self.wait.until(EC.presence_of_element_located((By.XPATH, payload.photos_link)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.photos_link)
        result.click()
        input("Press enter to go on.")

        return True
    def close(self):
        self.driver.close()
    def quit(self):
        self.driver.quit()
