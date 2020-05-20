import sys
import time

import googlemaps 

import spreadsheet
import navigation

DEBUG = None 

class Payload:
    def __init__(self):
        with open ("private.slr", "r") as slurp:
            data = slurp.readlines()
        if  len(data) != 3:
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
            self.api_key = data[2].rstrip()
            # Pages
            self.login_url = "https://offcampus.bu.edu/login/"
            self.add_listing_url = "https://offcampus.bu.edu/user/add-listing/"
            # Dummy data

def main():
    print ("Starting...\n")
    start_time = time.time()

    payload = Payload()
    gmaps = googlemaps.Client(payload.api_key)
    address = "1193 Commonwealth Ave., #45, Boston, MA"

    geocode_result = gmaps.geocode(address)
    for a in geocode_result[0]:
       print("A:", a)
    for a in geocode_result[0]["address_components"]:
        if a["types"][0] == "postal_code": print("B:", a["short_name"])
    sys.exit()

    #navigator = navigation.Navigator(DEBUG)
    #navigator.get_zip("1193 Commonwealth Ave., #45, Boston, MA")

    #if DEBUG != None:
    #    print ("Driver: ", navigator.driver)


    #print ("Login: \n", navigator.login(payload))
    #print ("Add new listing: \n", navigator.add_listing(payload))
    #print ("Enter full address: \n", navigator.fill_full_address(payload))

    #input("Press enter.")

    #navigator.quit()

    parser = spreadsheet.Spreadsheet(DEBUG)
    print("Getting listing data.\n")
    result = parser.get_listing_data()
    #print("Data:\n", result)
    
    print ("\nDone in %s seconds." % (time.time() - start_time))

main()
