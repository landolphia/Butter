import sys
import time
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


DEBUG = 1

TEMP_LISTING = "listing_to_post.xlsx"

class Payload:
    def __init__(self):
        with open ("private.slr", "r") as slurp:
            data = slurp.readlines()
        if  len(data) != 2:
            print("Cannot find credential in private.slr.")
            sys.exit()
        else:
            if DEBUG != None:
                print ("Slurp: ", data)
                print ("Fixed:", data[0].rstrip(), " / ", data[1].rstrip())
            # IDs
            self.form_id = "login"
            self.user_id = "username"
            self.pass_id = "password"
            self.full_address_div_id = "address-autocomplete-place"
            self.full_address_input_id = "address-autocomplete"
            # XPATHs
            self.login_link = "//form[@id=\"login\"]/preceding-sibling::a"
            self.address_input = "//*[@id=\"address_autocomplete\"]"
            #self.add_listing_link = "//a[@href=\"/user/add-listing/"
            self.button = "//input[@type=\"submit\"]"
            self.username = data[0].rstrip()
            self.password = data[1].rstrip()
            # Pages
            self.login_url = "https://offcampus.bu.edu/login/"
            self.add_listing_url = "https://offcampus.bu.edu/user/add-listing/"
            # Dummy data


def login(driver, payload, wait):
    result = None
    
    if driver == None:
        print ("Driver not loaded. Exiting program. [", driver, "]")
        sys.exit()

    if DEBUG != None:
        print("Signing into ", payload.login_url)

    login = driver.get(payload.login_url)
    
    print("Waiting for page to load.")
    wait.until(EC.presence_of_element_located((By.ID, payload.form_id)))
    print("Page loaded.")
    link = driver.find_element(By.XPATH, payload.login_link)
    print("Clicking on link to show form.")
    link.click()

    print("Waiting for form to load.")
    wait.until(EC.presence_of_element_located((By.ID, payload.user_id)))
    print("Loaded.")

    driver.find_element_by_id(payload.user_id).send_keys(payload.username)

    driver.find_element_by_id(payload.pass_id).send_keys(payload.password)

    print("Waiting for submit button to load.")
    wait.until(EC.presence_of_element_located((By.XPATH, payload.button)))
    print("Loaded.")

    result = driver.find_element(By.XPATH, payload.button).click()

    return result

def add_listing(driver, payload, wait):
    print("Loading new listing page.")
    login = driver.get (payload.add_listing_url)

    return 
    
def fill_full_address(driver, payload, wait):
    result = None

    print("Waiting for address input to load.")
    wait.until(EC.presence_of_element_located((By.ID, payload.full_address_div_id)))
    print("Loaded.")

    result = driver.find_element_by_xpath(payload.address_input)
    print("Input: ", result)
    #result.send_keys(payload.full_address)

    return result

def get_listing_data()
    workbook   = xlsxwriter.Workbook('listing_to_post.xlsx')


    workbook.close()


def main():
    print ("Starting...\n")
    start_time = time.time()

    options = Options()
    if DEBUG != None:
        options.headless = False 
    else:
        options.headless = True


    driver = webdriver.Chrome()
    if DEBUG != None:
        print ("Driver: ", driver)

    payload = Payload()
    wait = WebDriverWait(driver, 100)

    print ("Login: \n", login(driver, payload, wait))
    print ("Add new listing: \n", add_listing(driver, payload, wait))
    print ("Enter full address: \n", fill_full_address(driver, payload, wait))

    #print("Getting listing data")
    #get_listing_data()

    input("Press enter.")
    driver.close()
    driver.quit()
    
    print ("\nDone in %s seconds." % (time.time() - start_time))

main()
