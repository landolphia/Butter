import credentials
import spreadsheet

import logging
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
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

class Element_is_not_(object):
    def __init__(self, identifier, default_value):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Element_is_not_. [" + str(identifier) + "] [" + str(default_value) + "]")

        self.default_value = default_value
        self.identifier =identifier 
    def __call__(self, driver):
        if self.identifier["type"] == "xpath":
            element = driver.find_element_by_xpath(self.identifier["value"])
        elif self.identifier["type"] == "id":
            element = driver.find_element_by_id(self.identifier["value"])
        else:
            self.log.error("The type of identifier wasn't recognized. [" + self.identifier["type"]+ "]")
            sys.exit()

        if element:
            content = None
            while content == None:
                try:
                    content = element.get_attribute("innerText")
                except StaleElementReferenceException:
                    self.log.warning("Element stale. Trying again.")
                    if self.identifier["type"] == "xpath":
                        element = driver.find_element_by_xpath(self.identifier["value"])
                    elif self.identifier["type"] == "id":
                        element = driver.find_element_by_id(self.identifier["value"])

            loaded = not (self.default_value in content)
            if loaded:
                self.log.debug("Element is loaded.")

            return loaded
        else:
            return False

class DOM:
    def __init__(self):
        # TODO Reimplement offline
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing DOM.")
           
        self.driver = webdriver.Chrome()
        self.hold = WebDriverWait(self.driver, 100)

        if self.driver == None:
            self.log.error("ChromeDriver not found. Exiting. [%s]" % self.driver)
            sys.exit()

        g_key = credentials.Credentials().get_credentials("private.slr")["api_key"]
        self.ss = spreadsheet.Spreadsheet(slurp=g_key) 
    def process_actions(self, element, **kwargs):
        self.log.debug("Processing action list for [" + str(element) + "].")

        argument = None
        for k in kwargs:
            if k == "identifier":
                argument = kwargs[k]
            else:
                self.log.warning("Unrecognized argument [" + str(k) + "].")

        for a in element["actions"]:
            if a == "APPEND_AND_GO":
                if argument:
                    self.go(element["url"] + str(argument))
                else:
                    self.log.error("Missing argument.")
                    sys.exit()
            elif a == "CLICK": self.__click__(element)
            elif a == "FILL_INPUT": self.__fill_input__(element)
            elif a == "GET_ATTRIBUTE":
                result = "-"
                if not "attribute" in element:
                    self.log.error("Missing attribute.")
                    sys.exit()
                else:
                    self.log.debug("Attribute = " + str(element["attribute"]))

                e = self.__get_element__(element["identifier"])
                if e:
                    result = self.__get_attribute__(e, element["attribute"])
                
                if "fluff" in element:
                    result = result.replace(element["fluff"], "")
                
                return result
            elif a == "GET_CELL_DATA":
                identifier = element["cell"]
                element["get result"] = self.ss.get_key(identifier)
                self.log.debug("Getting cell #" + str(identifier) + " = [" + element["get result"] + "]")
            elif a == "GET_ELEMENTS_ATTRIBUTE":
                #TODO handle StaleElement exception
                if not "attribute" in element:
                    self.log.error("Missing attribute.")
                    sys.exit()
                else:
                    self.log.debug("Attribute = " + str(element["attribute"]))

                elements = self.__get_elements__(element["identifier"])
                result = []
                for e in elements:
                    result.append(self.__get_attribute__(e, element["attribute"]))

                return result
            elif a == "GET_PASSWORD":
                identifier = element["password"]
                self.log.debug("Password: " + str(identifier))
                element["get result"] = credentials.Credentials().get_credentials("private.slr")[str(identifier)]
            elif a == "GET_USERNAME": 
                identifier = element["username"]
                self.log.debug("Username: " + str(identifier))
                element["get result"] = credentials.Credentials().get_credentials("private.slr")[str(identifier)]
            elif a == "GO": self.go(element["url"])
            elif a == "IF_NOT_HARVARD":
                if "harvardhousingoffcampus" in self.current_url():
                    return True
            elif a == "UNFLUFF":
                self.log.warning("UNFLUIFF")
                input("LKJASF")
                return element
                #content = content.replace(data[l]["fluff"], "")
                #self.log.debug("LAKJSD")
                #sys.exit()
            elif a == "PRESS_ENTER":
                e = self.__get_element__(element["identifier"])
                if e: e.send_keys(Keys.ENTER)
            elif a == "WAIT": self.__wait__(element["identifier"])
            elif a == "WAIT_FOR_CONTENT": self.__wait_for_content__(element["identifier"])
            else:   
                self.log.error("Invalid action [" + str(a) + "]")
                sys.exit()
            # TODO a == "SPREADSHEET" and OFFSET isnumber
    def __click__(self, element):
        self.log.debug("Clicking on [" + element["identifier"]["value"] + "].")
        self.__get_element__(element["identifier"]).click()
    def __fill_input__(self, element):
        e = self.__get_element__(element["identifier"])
        value = element["get result"]
        self.log.debug("Filling input [" + element["identifier"]["value"] + "] with \"" + value + "\"")
        if not value: #FIXME Bail?
            self.log.warning("The value for " + str(element) + " is missing. It will be replaced with [DEFAULT_VALUE].")
            value = "[DEFAULT_VALUE]"

        e.send_keys(value)
    def __get_element__(self, identifier):
        element = None
        if identifier["type"] == "xpath":
            try:
                element = self.driver.find_element_by_xpath(identifier["value"])
            except NoSuchElementException:
                self.log.warning("Element was not found. [" + str(identifier) + "]")
        elif identifier["type"] == "id":
            try:
                element = self.driver.find_element_by_id(identifier["value"])
            except NoSuchElementException:
                self.log.warning("Element was not found. [" + str(identifier) + "]")
        else:
            self.log.error("The type of identifier wasn't recognized. [" + identifier["type"]+ "]")
            sys.exit()

        return element
    def __get_elements__(self, identifier):
        if identifier["type"] == "xpath":
            elements = self.driver.find_elements_by_xpath(identifier["value"])
        elif identifier["type"] == "id":
            elements = self.driver.find_elements_by_id(identifier["value"])
        else:
            self.log.error("The type of the element wasn't recognized. [" + identifier["type"] + "]")
            sys.exit()
            
        return elements
    def go(self, url):
        self.log.debug("Navigating to \"" + str(url) + "\"")
        self.driver.get(url)
    def __wait__(self, identifier):
        self.log.debug("Waiting for element to load. [" + str(identifier["value"]) + "]")

        if identifier["type"] == "xpath":
            self.hold.until(EC.presence_of_element_located((By.XPATH, identifier["value"])))
        elif identifier["type"] == "id":
            self.hold.until(EC.presence_of_element_located((By.ID, identifier["value"])))
        else:
            self.log.error("Unrecognized CSS selector type [" + str(identifier["type"]) + "].")
            sys.exit()

        self.log.debug("Element loaded.")
    def __wait_for_content__(self, identifier):
        self.log.debug("Waiting for content of element to be loaded. [" + str(identifier) + "]")

        condition = Element_is_not_(identifier, "-")
        self.hold.until(condition)




#TODO Below

    def __get_attribute__(self, element, attribute): return element.get_attribute(attribute)
    def process_actions_with_context(self, element, context):
        result = None
        for a in element["actions"]["list"]:
            if a == "APPEND_AND_GO": self.go(element["value"]["content"] + context)
            if a == "WAIT_FOR_CONTENT": self.__wait_for_content__(element["identifier"])
            if a == "GET_ELEMENTS_ATTRIBUTES":
                elements = self.__get_elements__(element["identifier"])
                result = []
                for e in elements:
                    result.append(self.__get_attribute__(e, element["value"]["content"]))

        return result

#TODO NOT TREATED BELOW
#TODO
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
        description = self.payload.get_value(page, name)

        iframe = self.__get_element__(iframe_page, iframe_name)
        self.driver.switch_to.frame(iframe)

        tinymce = self.__get_element__(page, name)
        
        javascript = "arguments[0].innerHTML = arguments[1];"
        self.driver.execute_script( javascript, tinymce, description.replace('\n', '<br>'))
        self.driver.switch_to.default_content()
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
    def task_list(self, tasks):
        self.hold.until(EC.presence_of_element_located((By.XPATH, "//body")))
        self.driver.execute_script("window.open('', 'todo', 'height=400,width=400,top=0, left=0, toolbar=no,menubar=no,scrollbars=yes,location=no,status=no');")
        self.hold.until(EC.presence_of_element_located((By.XPATH, "//body")))
        self.driver.switch_to_window("todo")

        javascript = "l = document.createElement('ul'); l.id ='list'; document.body.appendChild(l);"
        self.driver.execute_script(javascript)

        for t in tasks:
            javascript = "l = document.getElementById('list');"
            javascript = javascript + str("i = document.createElement('li');")
            javascript = javascript + str("text = document.createTextNode(arguments[0]);")
            javascript = javascript + str("i.appendChild(text);")
            javascript = javascript + str("l.appendChild(i);")
            self.driver.execute_script(javascript, t)
    def get_value_money(self, page, name):
        element = self.__get_element__(page, name)
        value = element.get_attribute("innerText")

        return int(value.replace("Rent\n$", "").replace(",","").strip())
    def scrape_unit(self, identifier):
        data = self.payload.data["unit"]

        unit = {}

        for l in data:
            try:
                element = self.driver.find_element_by_xpath(data[l]["xpath"])
                content = element.get_attribute("innerText")
                content = content.replace(data[l]["fluff"], "")
            except NoSuchElementException:
                self.log.warning("Element was not found. [" + str(l) + "]")
                content = "-"
         
            unit[l] = content

        return unit
