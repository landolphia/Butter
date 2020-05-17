import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

DEBUG = 1

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
            self.user_id = "username"
            self.pass_id = "password"
            self.login_link = "//form[@id=\"login\"]/preceding-sibling::a"
            self.button = "//input[@type=\"submit\"]"
            self.form = "login"
            self.username = data[0].rstrip()
            self.password = data[1].rstrip()
            self.login_url = "https://offcampus.bu.edu/login/"


def login(driver):
    payload = Payload()
    result = None
    
    if driver == None:
        print ("Driver not loaded. Exiting program. [", driver, "]")
        sys.exit()

    if DEBUG != None:
        print("Signing into ", payload.login_url)

    wait = WebDriverWait(driver, 100)
    login = driver.get (payload.login_url)
    
    print("Waiting for page to load.")
    wait.until(EC.presence_of_element_located((By.ID, payload.form)))
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
    print ("Result: \n", login(driver))

    driver.close()
    driver.quit()
    
    print ("\nDone in %s seconds." % (time.time() - start_time))
    input("Press enter.")

main()
