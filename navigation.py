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
        #self.address_id = "address"
        #self.city_id = "city"
        #self.state_id = "state"
        #self.zip_id = "zip"
        #self.exact_flag_id = "opt_street-0
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
    def close(self):
        self.driver.close()
    def quit(self):
        self.driver.quit()
