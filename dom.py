import credentials
import spreadsheet

import logging
import os
import pyautogui
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class List_has_new_element(object):
    def __init__(self, identifier, old_count):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing List_has_new_element. [" + str(identifier) + " / " + str(old_count) + "]")

        self.identifier = identifier 
        self.old_count = old_count 
    def __call__(self, driver):
        elements = []
        if self.identifier["type"] == "xpath":
            elements = driver.find_elements_by_xpath(self.identifier["value"])
        elif self.identifier["type"] == "id":
            elements = driver.find_elements_by_id(self.identifier["value"])
        else:
            self.log.error("The type of the element wasn't recognized. [" + self.identifier["type"] + "]")
            sys.exit()

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
        self.address = self.ss.parse_address(self.ss.get_key(0))
    def process_actions(self, element, **kwargs):
        self.log.debug("Processing action list for [" + str(element) + "].")

        argument = None
        for k in kwargs:
            if k == "identifier":
                argument = kwargs[k]
            if k == "iteration":
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
            elif a == "CHECKBOX":
                e = self.__get_element__(element["identifier"])
                if not e:
                    self.log.debug("Skipped [" + str(element["identifier"]) + "]")
                    return
                value = element["get result"]
                self.log.debug("Checkbox [" + str(element["identifier"]) + "] = " + str(value))

                if value == True:
                    self.driver.execute_script("arguments[0].setAttribute('checked','true')", e)
                else:
                    self.driver.execute_script("arguments[0].removeAttribute('checked')", e)
            elif a == "CLICK": self.__click__(element["identifier"])
            elif a == "DROPDOWN":
                e = self.__get_element__(element["identifier"])
                value = element["get result"]
                self.log.debug("Value for dropdown = " + str(value))

                for option in e.find_elements_by_tag_name('option'):
                    if option.text.strip().lower() == str(value).lower():
                        option.click()
            elif a == "FILL_INPUT": self.__fill_input__(element)
            elif a == "FILL_INPUT_FP":
                fp_nb = argument
                e = self.__get_element_fp__(element)
                cell = element["cell"] + (fp_nb * element["offset"])
                value = self.ss.get_key(cell).lower()

                if not value:
                    self.log.warning("The value for " + str(page) + "/" + str(name) + " is missing. It will be replaced with [DEFAULT_VALUE].")
                    value = "[DEFAULT_VALUE]"

                e.send_keys(value)
            elif a == "FILL_INPUT_DATE":
                e = self.__get_element__(element["identifier"])
                value = element["get result"]

                if not value:
                    self.log.ERROR("The value for " + str(element["identifier"]) + " is missing.\nCheck the spreadsheet for errors.")
                    sys.exit()

                value = self.ss.parse_date(value)
                self.driver.execute_script("arguments[0].value = '" + value + "'", e)
            elif a == "FILL_INPUT_MONEY":
                e = self.__get_element__(element["identifier"])
                value = element["get result"]

                e.send_keys(Keys.CONTROL + "a")
                e.send_keys(Keys.DELETE)
                e.send_keys("$" + str(value))
            elif a == "FILL_INPUT_NOT_NULL":
                e = self.__get_element__(element["identifier"])
                value = element["get result"]

                if not value:
                    value = element["default"]

                e.send_keys(value)
            elif a == "FILL_TINYMCE":
                iframe = self.__get_element__(element["iframe"])
                self.driver.switch_to.frame(iframe)

                tinymce = self.__get_element__(element["identifier"])
                
                javascript = "arguments[0].innerHTML = arguments[1];"
                self.driver.execute_script( javascript, tinymce, element["get result"].replace('\n', '<br>'))
                self.driver.switch_to.default_content()
            elif a == "GET_ADDRESS_STREET": element["get result"] = str(self.address["number"] + " " + self.address["name"])
            elif a == "GET_ADDRESS_CITY": element["get result"] = str(self.address["city"])
            elif a == "GET_ADDRESS_ZIP": element["get result"] = str(self.address["zip"])
            elif a == "GET_ADDRESS_STATE": element["get result"] = str(self.address["state"])
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
                self.log.debug("Getting cell #" + str(identifier) + " = [" + str(element["get result"]) + "]")
            elif a == "GET_DATE":
                identifier = element["date cell"]
                element["get result"] = self.ss.get_key(identifier)
                self.log.debug("Getting cell #" + str(identifier) + " = [" + str(element["get result"]) + "]")
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
            elif a == "GET_FP_ID":
                url = str(self.current_url())
                fp_id = url.rsplit('/', 1)[-1]
                element["FP_ID"] = fp_id
            elif a == "GET_PASSWORD":
                identifier = element["password"]
                self.log.debug("Password: " + str(identifier))
                element["get result"] = credentials.Credentials().get_credentials("private.slr")[str(identifier)]
            elif a == "GET_USERNAME": 
                identifier = element["username"]
                self.log.debug("Username: " + str(identifier))
                element["get result"] = credentials.Credentials().get_credentials("private.slr")[str(identifier)]
            elif a == "GO": self.go(element["url"])
            elif a == "IF_FALSE":
                element["get result"] = (not self.ss.get_key(element["cell"]))
            elif a == "IF_TRUE":
                element["get result"] = self.ss.get_key(element["cell"])
            elif a == "IF_DATE_NOW":
                self.log.warning("Do this instead. IF_VALUE_IS and add a test_value in the json object.")
                self.log.debug("Value = " + str(self.ss.get_key(element["cell"])))
                value = (self.ss.get_key(element["cell"]).lower() == "now")
                element["get result"] = value
                if not value:
                    return
            elif a == "IF_DATE_RANGE":
                value = (self.ss.get_key(element["cell"]).lower() == "between two dates")
                element["get result"] = value
                if not value:
                    return
            elif a == "IF_DATE_SPECIFIC":
                value = (self.ss.get_key(element["cell"]).lower() == "on a specific date")
                element["get result"] = value
                if not value:
                    return
            elif a == "IF_NOT_FP":
                if self.ss.get_key(element["fp cell"]):
                    return
            elif a == "IF_UNKNOWN":
                value = (self.ss.get_key(element["cell"]).lower() == "unknown")
                element["get result"] = value
                if not value:
                    return
            elif a == "IF_YES":
                value = (self.ss.get_key(element["cell"]).lower() == "yes")
                element["get result"] = value
                if not value:
                    return
            elif a == "IF_NO":
                value = (self.ss.get_key(element["cell"]).lower() == "no")
                element["get result"] = value
                if not value:
                    return
            elif a == "IF_NOT_HARVARD":
                if "harvardhousingoffcampus" in self.current_url():
                    return True
            elif a == "PRESS_ENTER":
                e = self.__get_element__(element["identifier"])
                if e: e.send_keys(Keys.ENTER)
            elif a == "RADIO":
                if element["get result"] == True:
                    e = self.__get_element__(element["identifier"])
                    e.click()
            elif a == "SUBMIT": self.__get_element__(element["identifier"]).submit()
            elif a == "UPLOAD_IMAGES":
                uploader = element["identifier"]
                photo_list = element["list"]
                self.upload_photos(uploader, photo_list)
            elif a == "UNFLUFF":
                self.log.warning("UNFLUIFF")
                input("LKJASF")
                return element
                #content = content.replace(data[l]["fluff"], "")
                #self.log.debug("LAKJSD")
                #sys.exit()
            elif a == "WAIT": self.__wait__(element["identifier"])
            elif a == "WAIT_FOR_CONTENT": self.__wait_for_content__(element["identifier"])
            else:   
                self.log.error("Invalid action [" + str(a) + "]")
                sys.exit()
            # TODO a == "SPREADSHEET" and OFFSET isnumber
    def __click__(self, identifier):
        self.log.debug("Clicking on [" + str(identifier) + "].")
        self.__get_element__(identifier).click()
    def __fill_input__(self, element):
        e = self.__get_element__(element["identifier"])
        value = element["get result"]
        self.log.debug("Filling input [" + element["identifier"]["value"] + "] with \"" + str(value) + "\"")
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
    def current_url(self):
        return self.driver.current_url
    def __get_element_fp__(self, element):
        self.log.debug("Identifier before : " + str(element["identifier"]["value"]))
        element["identifier"]["value"] = element["identifier"]["value"].replace("FP_ID", element["FP_ID"])
        self.log.debug("Identifier after : " + str(element["identifier"]["value"]))

        e = self.__get_element__(element["identifier"])

        return e
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

    def upload_photos(self, uploader, photo_list):
        photos = []
        for root, dirs, files in os.walk("./post/images/"):
            for f in files:
                if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".gif") or f.endswith(".png"):
                    path = os.path.join(root, f)
                    self.log.debug("Photo found. [" + path + "]")
                    photos.append(path)

        uploads = 0
        for i in range(len(photos)):
            path = os.path.abspath(photos[i])
            self.log.debug("Uploading file #" + str(i) + " [" + photos[i] + "] [" + path + "]")

            self.__wait__(uploader)
            self.__click__(uploader)

            if os.path.isfile(photos[i]):
                time.sleep(1)
                pyautogui.write(path, interval=0.075)
                pyautogui.press('enter')
                self.wait_for_new_list_element(photo_list, uploads)
                uploads = uploads + 1
            else:
                self.log.error("The file [" + path + "] doesn't exist.")
                sys.exit()
    def wait_for_new_list_element(self, identifier, old_count):
        self.log.debug("Waiting for new element to be added to list. [" + str(identifier) + "]")

        condition = List_has_new_element(identifier, old_count)
        self.hold.until(condition)
        self.log.debug("New element added.")

#TODO NOT TREATED BELOW
#TODO

    def clear(self, page, name): self.__get_element__(page, name).clear()
    def dropdown_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element_fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))

        for option in element.find_elements_by_tag_name('option'):
            if option.text.strip().lower() == str(value).lower():
                option.click()
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
    def fill_input_money_fp(self, page, name, fp_nb, fp_id):
        element = self.__get_element_fp__(page, name, fp_nb, fp_id)
        value = self.payload.get_value(page, name + str(fp_nb))

        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys("$" + str(value))
    def quit(self): self.driver.quit()
    def radio_fp(self, page, name, fp_nb, fp_id):
        value = self.payload.get_value(page, name + str(fp_nb))
        if value != None:
            self.click_fp(page, name, fp_nb, fp_id)

        return value
    def submit_fp(self, page, name, fp_nb, fp_id): self.__get_element_fp__(page, name, fp_nb, fp_id).submit()
    def tinyMCE(self, page, name, iframe_page, iframe_name):
        description = self.payload.get_value(page, name)

        iframe = self.__get_element__(iframe_page, iframe_name)
        self.driver.switch_to.frame(iframe)

        tinymce = self.__get_element__(page, name)
        
        javascript = "arguments[0].innerHTML = arguments[1];"
        self.driver.execute_script( javascript, tinymce, description.replace('\n', '<br>'))
        self.driver.switch_to.default_content()
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
