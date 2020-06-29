import logging
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Elements:
    def __init__(self, payload):
            self.log = logging.getLogger("bLog")
            self.log.debug("Initializing Elements.")
            
            self.driver = webdriver.Chrome()
            self.hold = WebDriverWait(self.driver, 100)
            # TODO
            #FluentWait<WebDriver>(driver)
            #    .withTimeout(50, TimeUnit.SECONDS)
            #    .pollingevery(3, TimeUnit.SECONDS)
            #    .ignoring(NoSuchElementException.class)

            if self.driver == None:
                self.log.error("ChromeDriver not found. Exiting. [%s]" % self.driver)
                sys.exit()

            self.payload = payload
    def __get_element__(self, page, name):
        identifier = self.payload.xpath(page, name)
        if identifier:
            element = self.driver.find_element_by_xpath(identifier)
        else:
            identifier = self.payload.id(page, name)
            element = self.driver.find_element_by_id(identifier)
        if not element:
            self.log.error("The type of the element wasn't recognized. [" + page + "/" + name + "]")

        return element
    def checkbox(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)

        #FIXME Add a type field to the payload data for each element
        self.log.debug("FIX ME NOW! Add type to payload.")
        # Temp fix for bools
        if str(value).lower() == "y": value = True
        if value == None: value = False 

        if value == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", element)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", element)
    def click(self, page, name): self.__get_element__(page, name).click()
    def current_url(self):
        return self.driver.current_url
    def dropdown(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)

        for option in element.find_elements_by_tag_name('option'):
            if option.text.strip().lower() == str(value).lower():
                option.click()
    def go(self, page, name):
        url = self.payload.get_value(page, name) 
        self.log.debug("Navigating to \"" + str(url) + "\"")
        self.driver.get(url)
    def submit(self, page, name): self.__get_element__(page, name).submit()
    def wait(self, page, name):
        self.log.debug("Waiting for element to load. [" + page + "/" + name + "]")

        identifier = self.payload.xpath(page, name)

        if identifier:
            self.hold.until(EC.presence_of_element_located((By.XPATH, identifier)))
            self.log.debug("Element loaded.")

            return
        else:
            identifier = self.payload.id(page, name)
        self.log.debug("id = " + identifier)

        if identifier:
            self.hold.until(EC.presence_of_element_located((By.ID, identifier)))
            self.log.debug("Element loaded.")
        else:
            self.log.error("The type of the element wasn't recognized. [" + page + "/" + name + "]")
            sys.exit()
    def fill_input_not_null(self, page, name, default):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)

        if not value:
            value = default

        element.send_keys(value)
    def fill_input(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)
        if not value:
            value = "[DEFAULT_VALUE]"

        element.send_keys(value)
    def press_enter(self, page, name):
        element = self.__get_element__(page, name)
        element.send_keys(Keys.ENTER)

#NOT DONE below
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
    def wait_for_xpath_fp(self, element, fpid):
        self.log.debug("The floorplan id is " + str(fpid)) 
        self.log.debug("Need to parse element and inject fpid.")
        self.log.info("The program has semi-expectedly stopped. Some features are still being developed.")
        sys.exit()
        self.log.debug("Waiting for element to load. [" + str(element) + "]")
        self.wait.until(EC.presence_of_element_located((By.XPATH, element)))
        return xpath
