import logging
import sys
import time

import credentials
import navigation
import payload
import payload2
import scraper
import scrapings
import spreadsheet

from logging import handlers


VERSION = "0.2.5" #Bump up to 0.3 when done

#TODO Investergate this
#def install(package):
#    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def init_log(logLevel):
    log = logging.getLogger("bLog")
    log.setLevel(logging.DEBUG)
    log.propagate = False

    if (log.hasHandlers()):
        log.gerhandlers.clear()
    
    fileFormatter = logging.Formatter("%(asctime)s [%(levelname)s] from (%(module)s:%(lineno)s): %(message)s")
    fileHandler = logging.handlers.RotatingFileHandler("debug.log", mode='a', maxBytes=1*1024*1024, backupCount=2, encoding=None, delay=0)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(fileFormatter)
    
    streamFormatter = logging.Formatter("[%(levelname)s]: %(message)s")
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logLevel)
    streamHandler.setFormatter(streamFormatter)

    log.addHandler(fileHandler)
    log.addHandler(streamHandler)

    return log

def process_args(args):
    logLevel = logging.INFO
    app_mode = None

    i = 1
    for a in args:
        # Logging level
        if a == "DEBUG":
            logLevel = logging.DEBUG
        elif a == "WARNING":
            logLevel = logging.WARNING
        elif a == "INFO":
            logLevel = logging.INFO
        # Which mode to run as
        elif a == "POST":
            app_mode = "POST"
        elif a == "SCRAPE":
            app_mode = "SCRAPE"
        else:
            if i != 1:
                print("Argument #" + str(i) + " ignored. [" + str(a) + "]")
        i += 1

    return { "log level": logLevel, "mode": app_mode}

def main():
    arguments = process_args(sys.argv)
    log = init_log(arguments["log level"])
    log.info("Butter v" + str(VERSION) + " is starting...")
    log.debug("Command line arguments: " + str(arguments))

    start_time = time.time()
    
    if arguments["mode"] == "POST":
        data = payload.Payload()
        ss = spreadsheet.Spreadsheet(data.get_value("hidden", "gmaps"))
        data.init(ss)

        input("Wait")
        nav = navigation.Navigator(data)
        nav.start()
        nav.task_list()

        log.warning("Please check the messages above to see if some elements still need to be filled manually.")

        input("\nPress enter when you're done filling in missing details in the ad.")
        nav.close()
    elif arguments["mode"] == "SCRAPE":
        #TODO check id field becaus if it's loaded everything *should* be loaded.
        log.debug("TODO figure out how to make difference between not loaded and empty field. Just wait for 5 secs?")
        log.debug("TODO USE LOADING SIGN presence to check loading state.")
        
        log.debug("TODO figure out what to do with optional elements (key/entry info isn't always there.)")
        payload = payload2.Payload2()
        scr  = scraper.Scraper(payload)
        scr.close()
        units = scr.get_units()
        log.debug("Scraped " + str(len(units)) + "unit" + ("s" if len(units) > 1 else "") + ".")
        scrapings.Scrapings().create(units)
    else:
        log.error("Invalid mode \'" + str(arguments["mode"]) + "\'. You can use 'SCRAPE' or 'POST' to run the script in the appropriate mode.")

    log.debug("Finished in %s seconds." % (time.time() - start_time))

main()
