import sys
import time

import googlemaps 

import spreadsheet
import navigation

DEBUG = None 

class Payload:
    def __init__(self):
        # Login page
        self.form_id = "login"
        self.user_id = "username"
        self.pass_id = "password"
        self.login_link = "//form[@id=\"login\"]/preceding-sibling::a"
        self.address_input = "//*[@id=\"address_autocomplete\"]"
        self.button = "//input[@type=\"submit\"]"
        # Full address page
        self.full_address_div_id = "address-autocomplete-place"
        self.full_address_input_id = "address-autocomplete"
        # Address page
        self.address_id = "address"
        self.city_id = "city"
        self.state_id = "state"
        self.zip_id = "zip"
        self.exact_flag_id = "opt_street-0"
        self.address_form_xpath = "//form[@action=\"/user/add-listing\"]"
        # Location page
        self.property_name_input_id = "property_name"
        ###TODO!!!
        # Rent page
        self.rent_link =  "//a[@data-target=\"rent\"]"
        self.building_type_select_id = "buildingtype"
        self.multiple_floorplans_radio_no_id = "multi-unit-no"
        self.multiple_floorplans_radio_yes_id = "multi-unit-yes"
        self.reqs_broker_id = "security_deposit_amenities-231"
        self.reqs_first_id = "security_deposit_amenities-161"
        self.reqs_last_id = "security_deposit_amenities-162"
        self.reqs_upfront_id = "security_deposit_amenities-165"
        self.reqs_references_id = "security_deposit_amenities-164"
        self.reqs_security_id = "security_deposit_amenities-163"
        self.specials_id = "specials"
        # Specifics page
        self.specifics_link =  "//a[@data-target=\"details\"]"
        # Amenities page
        self.amenities_link =  "//a[@data-target=\"amenities\"]"
        # Contact page
        self.contact_link =  "//a[@data-target=\"contact\"]"
        # Photos page
        self.photos_link =  "//a[@data-target=\"images\"]"
        #END TODO!!!
        # Credentials
        with open ("private.slr", "r") as slurp:
            data = slurp.readlines()
        if  len(data) != 3:
            print("Cannot find credential in private.slr.")
            sys.exit()
        else:
            if DEBUG != None:
                print ("Slurp: ", data)
                print ("Fixed:", data[0].rstrip(), " / ", data[1].rstrip())
        self.username = data[0].rstrip()
        self.password = data[1].rstrip()
        self.api_key = data[2].rstrip()
        # Pages
        self.login_url = "https://offcampus.bu.edu/login/"
        self.add_listing_url = "https://offcampus.bu.edu/user/add-listing/"
        # Listing data
        self.listing = None

def main():
    print ("Starting...\n")
    start_time = time.time()

    payload = Payload()

    # Retrieving data from the Excel spreadsheet
    parser = spreadsheet.Spreadsheet(DEBUG, payload.api_key)
    print("Getting listing data.\n")
    payload.listing = parser.get_listing_data()

    input("Press enter to exit.")
    sys.exit()
    
    # Filling forms with the data
    navigator = navigation.Navigator(DEBUG)

    if DEBUG != None:
        print ("Driver: ", navigator.driver)

    print ("Login: ", navigator.login(payload))
    print ("Adding new listing: ", navigator.add_listing(payload))
    print ("Entering full address: ", navigator.fill_full_address(payload))
    print ("Entering address details: ", navigator.fill_address(payload))
    print ("Filling location details: ", navigator.fill_location_page(payload))

    #TODO !!!
    print ("Filling rent: ", navigator.fill_rent_page(payload))
    #print ("Filling specifics: ", navigator.fill_specifics_page(payload))
    #print ("Filling amenities: ", navigator.fill_amenities_page(payload))
    #print ("Filling contact: ", navigator.fill_contact_page(payload))
    #print ("Filling photos: ", navigator.fill_photos_page(payload))
    #END TODO!!!

    input("Press enter to quit.")
    navigator.quit()

    print ("\nDone in %s seconds." % (time.time() - start_time))

main()
