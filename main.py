import sys
import time

import spreadsheet
import navigation

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

def main():
    print ("Starting...\n")
    start_time = time.time()

    navigator = navigation.Navigator(DEBUG)

    if DEBUG != None:
        print ("Driver: ", navigator.driver)

    payload = Payload()

    print ("Login: \n", navigator.login(payload))
    print ("Add new listing: \n", navigator.add_listing(payload))
    print ("Enter full address: \n", navigator.fill_full_address(payload))

    #print("Getting listing data")
    #get_listing_data()

    input("Press enter.")

    navigator.close()
    
    print ("\nDone in %s seconds." % (time.time() - start_time))

main()
