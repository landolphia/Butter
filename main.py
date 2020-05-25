import sys
import logging
import time

import spreadsheet
import navigation

class Payload:
    def __init__(self):
        logging.basicConfig(filename='run.log', filemode='w', level=logging.DEBUG)

        with open ("private.slr", "r") as slurp:
            data = slurp.readlines()
        if  len(data) != 3:
            logging.error("Could not find credentials in private.slr.")
            sys.exit()
        else:
            if DEBUG != None:
                print ("Slurp: ", data)
                print ("Fixed:", data[0].rstrip(), " / ", data[1].rstrip())
            # IDs
            # Login page
            self.form_id = "login"
            self.user_id = "username"
            self.pass_id = "password"
            #Full address page
            self.full_address_div_id = "address-autocomplete-place"
            self.full_address_input_id = "address-autocomplete"
            #Address page
            self.address_id = "address"
            self.city_id = "city"
            self.state_id = "state"
            self.zip_id = "zip"
            self.exact_flag_id = "opt_street-0"
            self.address_form_xpath = "//form[@action=\"/user/add-listing\"]"
            # XPATHs
            self.login_link = "//form[@id=\"login\"]/preceding-sibling::a"
            self.address_input = "//*[@id=\"address_autocomplete\"]"
            #self.add_listing_link = "//a[@href=\"/user/add-listing/"
            self.button = "//input[@type=\"submit\"]"
            self.username = data[0].rstrip()
            self.password = data[1].rstrip()
            self.api_key = data[2].rstrip()
            # Pages
            self.login_url = "https://offcampus.bu.edu/login/"
            self.add_listing_url = "https://offcampus.bu.edu/user/add-listing/"

            self.listing = None

def main():
    print ("Starting...\n")
    start_time = time.time()

    payload = Payload()

    #Retrieving data from the Excel spreadsheet
    parser = spreadsheet.Spreadsheet(DEBUG, payload.api_key)
    print("Getting listing data.\n")
    payload.listing = parser.get_listing_data()
    
    sys.exit()
    # Filling forms with the data
    navigator = navigation.Navigator(DEBUG)

    if DEBUG != None:
        print ("Driver: ", navigator.driver)

    print ("Login: ", navigator.login(payload))
    print ("Adding new listing: ", navigator.add_listing(payload))
    print ("Entering full address: ", navigator.fill_full_address(payload))
    print ("Entering address details: ", navigator.fill_address(payload))

    input("Press enter to quit.")
    navigator.quit()

    print ("\nDone in %s seconds." % (time.time() - start_time))

main()
