import logging
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class List_has_new_element(object):
    def __init__(self, xpath, old_count):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing List_has_new_element. [" + str(xpath) + " / " + str(old_count) + "]")

        self.xpath = xpath 
        self.old_count = old_count 
    def __call__(self, driver):
        elements = driver.find_elements_by_xpath(self.xpath)
        if len(elements) > self.old_count:
            self.log.debug("Found a new element, " + str(len(elements)) + " total.")
            return True 
        else:
            return False

class Elements:
    def __init__(self, payload):
            self.log = logging.getLogger("bLog")
            self.log.debug("Initializing Elements.")
            
            self.driver = webdriver.Chrome()
            self.hold = WebDriverWait(self.driver, 100)

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
    def __get_element_fp__(self, page, name, fp_nb, fp_id):
        name = name + str(fp_nb)
        identifier = self.payload.xpath(page, name)

        if identifier:
            identifier = identifier.replace("FP_ID", str(fp_id))
            element = self.driver.find_element_by_xpath(identifier)
        else:
            identifier = self.payload.id(page, name)
            if identifier:
                identifier = identifier.replace("FP_ID", str(fp_id))
            element = self.driver.find_element_by_id(identifier)
        if not element:
            self.log.error("The type of the element wasn't recognized. [" + page + "/" + name + "]")

        return element
    def checkbox(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)

        #FIXME Add a type field to the payload data for each element
        #self.log.debug("FIX ME NOW! Add type to payload.")
        # Temp fix for bools
        if str(value).lower() == "y": value = True
        if value == None: value = False 

        if value == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", element)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", element)
    def checkbox_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element_fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))

        #FIXME Add a type field to the payload data for each element
        #self.log.debug("FIX ME NOW! Add type to payload.")
        if str(value).lower() == "y": value = True
        if value == None: value = False 

        if value == True:
            self.driver.execute_script("arguments[0].setAttribute('checked','true')", element)
        else:
            self.driver.execute_script("arguments[0].removeAttribute('checked')", element)
    def clear(self, page, name): self.__get_element__(page, name).clear()
    def click(self, page, name): self.__get_element__(page, name).click()
    def click_fp(self, page, name, fp_nb, fp_id): self.__get_element_fp__(page, name, fp_nb, fp_id).click()
    def current_url(self):
        return self.driver.current_url
    def dropdown(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)

        for option in element.find_elements_by_tag_name('option'):
            if option.text.strip().lower() == str(value).lower():
                option.click()
    def dropdown_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element_fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))

        for option in element.find_elements_by_tag_name('option'):
            if option.text.strip().lower() == str(value).lower():
                option.click()
    def fill_input(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)
        if not value:
            self.log.warning("The value for " + str(page) + "/" + str(name) + " is missing. It will be replaced with [DEFAULT_VALUE].")
            value = "[DEFAULT_VALUE]"

        element.send_keys(value)
    def fill_input_date(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)
        if not value:
            self.log.ERROR("The value for " + str(page) + "/" + str(name) + " is missing.\nCheck the spreadsheet for errors.")
            sys.exit()

        self.driver.execute_script("arguments[0].value = '" + value + "'", element)
    def fill_input_date_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element_fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))
        if not value:
            self.log.warning("The value for " + str(page) + "/" + str(name) + " is missing. It will be replaced with [DEFAULT_VALUE].")
            self.log.ERROR("The value for " + str(page) + "/" + str(name) + " is missing.\nCheck the spreadsheet for errors.")
            sys.exit()

        self.driver.execute_script("arguments[0].value = '" + value + "'", element)
        self.log.debug("Check date.")
    def fill_input_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element_fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))
        if not value:
            self.log.warning("The value for " + str(page) + "/" + str(name) + " is missing. It will be replaced with [DEFAULT_VALUE].")
            value = "[DEFAULT_VALUE]"

        element.send_keys(value)
    def fill_input_money(self, page, name):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)

        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys("$" + str(value))
    def fill_input_money_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element_fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))

        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys("$" + str(value))
    def fill_input_not_null(self, page, name, default):
        element = self.__get_element__(page, name)
        value = self.payload.get_value(page, name)

        if not value:
            value = default

        element.send_keys(value)
    def go(self, page, name):
        url = self.payload.get_value(page, name) 
        self.log.debug("Navigating to \"" + str(url) + "\"")
        self.driver.get(url)
    def press_enter(self, page, name):
        element = self.__get_element__(page, name)
        element.send_keys(Keys.ENTER)
    def quit(self): self.driver.quit()
    def radio(self, page, name):
        value = self.payload.get_value(page, name)
        if value != None:
            self.click(page, name)

        return value
    def radio_fp(self, page, name, fp_nb, fp_id):
        value = self.payload.get_value(page, name + str(fp_nb))
        if value != None:
            self.click_fp(page, name, fp_nb, fp_id)

        return value
    def submit(self, page, name): self.__get_element__(page, name).submit()
    def submit_fp(self, page, name, fp_nb, fp_id): self.__get_element_fp__(page, name, fp_nb, fp_id).submit()
    def tinyMCE(self, page, name, iframe_page, iframe_name):
        #TODO maybe I could speed this up by setting the value instead of sending keys
        #TODO (only display warning if len>X
        self.log.warning("Filling in the description. This might take a while if it's long.")
        description = self.payload.get_value(page, name)

        iframe = self.__get_element__(iframe_page, iframe_name)
        self.driver.switch_to.frame(iframe)

        tinymce = self.__get_element__(page, name)
        tinymce.click()
        tinymce.send_keys(description)
        self.driver.switch_to.default_content()
    def wait(self, page, name):
        self.log.debug("Waiting for element to load. [" + page + "/" + name + "]")

        identifier = self.payload.xpath(page, name)

        if identifier:
            self.hold.until(EC.presence_of_element_located((By.XPATH, identifier)))
            self.log.debug("Element loaded.")

            return
        else:
            identifier = self.payload.id(page, name)

        if identifier:
            self.hold.until(EC.presence_of_element_located((By.ID, identifier)))
            self.log.debug("Element loaded.")
        else:
            self.log.error("The type of the element wasn't recognized. [" + page + "/" + name + "]")
            sys.exit()
    def wait_for_new_list_element(self, page, name, old_count):
        self.log.debug("Waiting for new element to be added to list. [" + str(page) + "/" + str(name) + "]")

        identifier = self.payload.xpath(page, name)

        if identifier:
            condition = List_has_new_element(identifier, old_count)
            self.hold.until(condition)
            self.log.debug("New element added.")

            return
        else:
            identifier = self.payload.id(page, name)

        if identifier:
            self.log.error("Waiting for new list elements by id hasn't been implemented.")
            sys.exit()
        else:
            self.log.error("The type of the element wasn't recognized. [" + page + "/" + name + "]")
            sys.exit()
