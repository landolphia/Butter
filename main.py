import logging
import sys
import time

import navigation
import payload
import spreadsheet

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("run.log"),
            logging.StreamHandler()
        ]
    )
    log = logging.getLogger("root")

    log.info("Starting...\n")
    start_time = time.time()
    
    data = payload.Payload()
    ss = spreadsheet.Spreadsheet(data.get_value("hidden", "gmaps"))
    data.init(ss)
    data.disp()
    nav = navigation.Navigator()
    nav.login(data)
    nav.add_listing(data)
    nav.fill_address(data)
    print("Everything done until Rent Page.")
    input("Taste")

    nav.quit()

    log.info("Finished in %s seconds." % (time.time() - start_time))

main()

#        # Login page
#        self.form_id = "login"
#        self.user_id = "username"
#        self.pass_id = "password"
#        self.login_link = "//form[@id=\"login\"]/preceding-sibling::a"
#        self.address_input = "//*[@id=\"address_autocomplete\"]"
#        self.button = "//input[@type=\"submit\"]"
#        # Full address page
#        self.full_address_div_id = "address-autocomplete-place"
#        self.full_address_input_id = "address-autocomplete"
#        # Address page
#        self.address_id = "address"
#        self.city_id = "city"
#        self.state_id = "state"
#        self.zip_id = "zip"
#        self.exact_flag_id = "opt_street-0"
#        self.address_form_xpath = "//form[@action=\"/user/add-listing\"]"
#        # Location page
#        self.property_name_input_id = "property_name"
#        ###TODO!!!
#        # Rent page
#        self.rent_link =  "//a[@data-target=\"rent\"]"
#        self.building_type_select_id = "buildingtype"
#        self.multiple_floorplans_radio_no_id = "multi-unit-no"
#        self.multiple_floorplans_radio_yes_id = "multi-unit-yes"
#        self.reqs_broker_id = "security_deposit_amenities-231"
#        self.reqs_first_id = "security_deposit_amenities-161"
#        self.reqs_last_id = "security_deposit_amenities-162"
#        self.reqs_upfront_id = "security_deposit_amenities-165"
#        self.reqs_references_id = "security_deposit_amenities-164"
#        self.reqs_security_id = "security_deposit_amenities-163"
#        self.specials_id = "specials"
#        # Specifics page
#        self.specifics_link =  "//a[@data-target=\"details\"]"
#        self.max_occupants_id = "max-occupants"
#        self.allow_sublet_id = "allow_sublets-display"
#        self.is_sublet_id = "sublet-display"
#        self.roommate_situation_id = "shared-display"
#        self.available_now_id = "move-in-now"
#        self.available_date_id = "move-in-date"
#        self.available_date_start_id = "start"
#        self.available_range_id = "move-in-range"
#        self.available_date_end_id = "end"
#        self.available_renew_unk_id = "renew-option-unknown"
#        self.available_renew_yes_id = "renew-option-yes"
#        self.available_renew_no_id = "renew-option-no"
#        # Amenities page
#        # Features
#        self.amenities_link =  "//a[@data-target=\"amenities\"]"
#        self.pet_policy_id = "pet_policy"
#        self.lead_paint_id = "lead_paint"
#        self.ac_id = "amenity[1]-1"
#        self.carpet_id = "amenity[1]-20"
#        self.dining_room_id = "amenity[1]-202"
#        self.disability_access_id = "amenity[1]-15"
#        self.dishwasher_id = "amenity[1]-26"
#        self.fireplace_id = "amenity[1]-8"
#        self.furnished_id = "amenity[1]-7"
#        self.garbage_disp_id = "amenity[1]-82"
#        self.hardwood_id = "amenity[1]-21"
#        self.internet_id = "amenity[1]-303"
#        self.living_room_id = "amenity[1]-200"
#        self.microwave_id = "amenity[1]-204"
#        self.patio_id = "amenity[1]-6"
#        self.private_garden_id = "amenity[1]-205"
#        self.shared_garden_id = "amenity[1]-206"
#        self.smoke_free_id = "amenity[1]-41"
#        self.additional_storage_id = "amenity[1]-207"
#        self.included_storage_id = "amenity[1]-208"
#        self.study_id = "amenity[1]-203"
#        # Agency
#        self.agent_fee_id = "amenity[8]-50"
#        self.no_fee_id = "amenity[8]-51"
#        # Community
#        self.fitness_room_id = "amenity[2]-45"
#        self.individual_leases_id = "amenity[2]-46"
#        self.near_bus_id = "amenity[2]-19"
#        self.near_T_id = "amenity[2]-133"
#        self.pool_id = "amenity[2]-10"
#        self.roommate_matching_id = "amenity[2]-44"
#        self.tennis_court_id = "amenity[2]-11"
#        # Lease
#        self.twelve_months_id = "amenity[5]-16"
#        self.nine_months_id = "amenity[5]-17"
#        self.fall_sublet_id = "amenity[5]-76"
#        self.flexible_lease_id = "amenity[5]-18"
#        self.month_to_month_id = "amenity[5]-63"
#        self.short_term_lease_id = "amenity[5]-42"
#        self.spring_sublet_id = "amenity[5]-77"
#        self.summer_sublet_id = "amenity[5]-75"
#        # Security
#        self.courtesy_officer_id = "amenity[9]-120"
#        self.dead_bolt_id = "amenity[9]-95"
#        self.exterior_light_id = "amenity[9]-99"
#        self.intercom_id = "amenity[9]-97"
#        self.security_guard_id = "amenity[9]-100"
#        self.security_system_id = "amenity[9]-25"
#        self.video_surv_id = "amenity[9]-98"
#        # Utilities
#        self.cable_id = "amenity[3]-5"
#        self.electricity_id = "amenity[3]-4"
#        self.gas_id = "amenity[3]-3"
#        self.heat_id = "amenity[3]-2"
#        self.util_internet_id = "amenity[3]-35"
#        self.hot_water_id = "amenity[3]-226"
#        self.local_phone_id = "amenity[3]-39"
#        self.recycling_id = "amenity[3]-124"
#        self.trash_id = "amenity[3]-22"
#        self.water_id = "amenity[3]-23"
#        # Parking
#        self.garage_park_id = "amenity[4]-37"
#        self.no_parking_id = "amenity[4]-142"
#        self.off_street_park_id = "amenity[4]-36"
#        self.on_street_park_id = "amenity[4]-38"
#        # Laundry
#        self.laundry_in_comm_id = "amenity[7]-12"
#        self.no_laundry_id = "amenity[7]-143"
#        self.wd_hookups_id = "amenity[7]-33"
#        self.wd_in_unit = "amenity[7]-9"
#        # Description
#        #TODO !!!! FIXME
#        self.description_id = "mceu_13"
#        # Contact page
#        self.contact_link =  "//a[@data-target=\"contact\"]"
#        # Photos page
#        self.photos_link =  "//a[@data-target=\"images\"]"
#        #END TODO!!!
#        # Pages
#        self.login_url = "https://offcampus.bu.edu/login/"
#        self.add_listing_url = "https://offcampus.bu.edu/user/add-listing/"
#        # Listing data
#        self.listing = None
