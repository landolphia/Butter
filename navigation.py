from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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
    def get_zip(self, address):
        result = None

        if self.driver == None:
            print ("Driver not loaded. Exiting program. [", self.driver, "]")
            sys.exit()

        result = self.driver.get(self.search_url+address+"+zip+code")
        print("result: ", result)
        input("Waity")

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
    
        return result
    def add_listing(self, payload):
        print("Loading new listing page.")
        login = self.driver.get(payload.add_listing_url)
    
        return  login
    def fill_full_address(self, payload):
        result = None
    
        print("Waiting for address input to load.")
        self.wait.until(EC.presence_of_element_located((By.ID, payload.full_address_div_id)))
        print("Loaded.")
    
        result = self.driver.find_element_by_xpath(payload.address_input)
        print("Input: ", result)
        #result.send_keys(payload.full_address)
    
        return result
    def close(self):
        self.driver.close()
    def quit(self):
        self.driver.quit()
