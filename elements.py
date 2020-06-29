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
    def __get_element__fp__(self, page, name, fp_nb, fp_id):
        name = name + str(fp_nb)
        identifier = self.payload.xpath(page, name)
        if identifier:
            identifier = identifier.replace("FP_ID", str(fp_id))
            element = self.driver.find_element_by_xpath(identifier)
        else:
            identifier = self.payload.id(page, name)
            if identifier :
                identifier = identifier.replace("FP_ID", str(fp_id))
                element = self.driver.find_element_by_id(identifier)
        if not element:
            self.log.error("The type of the element wasn't recognized. [" + page + "/" + name + "]")

        return element
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
    def checkbox_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element__fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))

        #FIXME Add a type field to the payload data for each element
        self.log.debug("FIX ME NOW! Add type to payload.")
        if str(value).lower() == "y": value = True
        if value == None: value = False 

        if value == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", element)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", element)
    def click(self, page, name): self.__get_element__(page, name).click()
    def click_fp(self, page, name, fp_nb, fp_id): self.__get_element__fp__(page, name, fp_nb, fp_id).click()
    def current_url(self):
        return self.driver.current_url
    def dropdown(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)

        for option in element.find_elements_by_tag_name('option'):
            if option.text.strip().lower() == str(value).lower():
                option.click()
    def dropdown_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element__fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))

        for option in element.find_elements_by_tag_name('option'):
            if option.text.strip().lower() == str(value).lower():
                option.click()
    def go(self, page, name):
        url = self.payload.get_value(page, name) 
        self.log.debug("Navigating to \"" + str(url) + "\"")
        self.driver.get(url)
    def submit(self, page, name): self.__get_element__(page, name).submit()
    def submit_fp(self, page, name, fp_nb, fp_id): self.__get_element__fp__(page, name, fp_nb, fp_id).submit()
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
    def fill_input_money(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)

        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys("$" + str(value))
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
    def fill_input_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element__fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))
        if value:
            element.send_keys(value)
    def fill_input_money_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element__fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))

        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys("$" + str(value))
    def press_enter(self, page, name):
        element = self.__get_element__(page, name)
        element.send_keys(Keys.ENTER)
    def radio(self, page, name): self.click(page, name)
    def radio_fp(self, page, name, fp_nb, fp_id): self.click_fp(page, name, fp_nb, fp_id)

#NOT DONE below
    def wait_for_xpath_fp(self, element, fpid):
        self.log.debug("The floorplan id is " + str(fpid)) 
        self.log.debug("Need to parse element and inject fpid.")
        self.log.info("The program has semi-expectedly stopped. Some features are still being developed.")
        sys.exit()
        self.log.debug("Waiting for element to load. [" + str(element) + "]")
        self.wait.until(EC.presence_of_element_located((By.XPATH, element)))
        return xpath
