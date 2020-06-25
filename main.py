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

    nav = navigation.Navigator()
    nav.login(data)
    nav.add_listing(data)
    nav.fill_address(data)
    nav.fill_rent(data)
    nav.fill_specifics(data)
    input("Finished up to specifics page.")
    #nav.fill_amenities(data)
    #nav.fill_contact(data)
    #nav.fill_photos(data)

    nav.quit()

    log.info("Finished in %s seconds." % (time.time() - start_time))

main()
