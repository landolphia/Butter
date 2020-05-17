import sys
import time
from selenium import webdriver

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
            self.user_id = "id"
            self.pass_id = "password"
            self.button = "//input[@type='submit']"
            self.username = data[0].rstrip()
            self.password = data[1].rstrip()
            self.login_url = "https://offcampus.bu.edu/"


def login(driver):
    payload = Payload()
    result = None
    
    #driver.get (payload.login_url)

    #driver.find_element_by_id(payload.user_id).send_keys(payload.username)
    #driver.find_element_by_id(payload.pass_id).send_keys(payload.password)

    #result = driver.find_element(By.XPATH, payload.button).click()

    return result


def main():
    print ("Starting...\n")
    start_time = time.time()

    #driver = webdriver.Chrome('./chromedriver.exe')
    print ("Result: \n", login(None))

    #driver.close()
    #driver.quit()
    
    print ("\nDone in %s seconds." % (time.time() - start_time))

main()
