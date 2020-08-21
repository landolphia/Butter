import logging
import sys
import time

import navigation

from logging import handlers


VERSION = "0.9"


def init_log(logLevel):
    log = logging.getLogger("bLog")
    log.setLevel(logging.DEBUG)
    log.propagate = False

    if (log.hasHandlers()):
        log.gerhandlers.clear()
    
    fileFormatter = logging.Formatter("%(asctime)s [%(levelname)s] from (%(module)s:%(lineno)s): %(message)s")
    fileHandler = logging.handlers.RotatingFileHandler("debug.log", mode='a', maxBytes=1*1024*1024, backupCount=0, encoding=None, delay=0)
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
    offline = False
    manual = False

    i = 1
    for a in args:
        if a == "DEBUG":
            logLevel = logging.DEBUG
        elif a == "HELP":
            manual = True
        elif a == "INFO":
            logLevel = logging.INFO
        elif a == "OFFLINE":
            offline = True
        elif a == "POST":
            app_mode = "POST"
        elif a == "SCRAPE":
            app_mode = "SCRAPE"
        elif a == "UNLEADED":
            app_mode = "UNLEADED"
        elif a == "WARNING":
            logLevel = logging.WARNING
        else:
            if i != 1:
                print("Argument #" + str(i) + " ignored. [" + str(a) + "]")
        i += 1

    if manual:
        instructions(app_mode)
        sys.exit()

    return { "log level": logLevel, "mode": app_mode, "offline": offline}

def instructions(mode):
    if not mode:
        print("This script can run in three modes:")
        print("-POST takes the data from a spreadsheet to post an ad online. \"py main.py POST\"\n")
        print("-SCRAPE crawls through online listings and creates a spreadsheet, highlighting keywords. \"py main.py SCRAPE\"")
        print("-UNLEADED crawls through online listings and matches the result against the unleaded database. \"py main.py UNLEADED\"")
    elif mode == "SCRAPE":
        print("SCRAPE: all the configuration files for scraping listings are in ./scrape/\n")
        print("- colors.json defines the colors used to highlight keywords.")
        print(" The format is: {\n\t\"color_name\" : [\"bright\", \"dim\"],\n\t...\n\t\"color_name\" : [\"bright\", \"dim\"]\n}")
        print(" The color format follows the HTML color format, e.g. #FF0000 for red.")
        print(" Note: as of now only the dim version of the color is used.\n")
        print("- keywords.json lists all the keywords you want to find in the listings and their associated color.")
        print(" The format is: {\n\t\"keyword\" : \"color\",\n\t...\n\t\"keyword\" : \"color\"\n}")
        print("Keywords are not case sensitive but will be matched exactly otherwise.")
        print("Colors refer to the color names defined in colors.js")
        print("Note: as of now the same keyword list is used to scrape multiple leads.\n")
        print("- leads.json contains a list of the leads IDs you'd like to scrape.")
        print("The format is: [ \"lead id\", ..., \"lead id\"]")
        print("The lead ID is the last part of the list's url. e.g, for https://app.yougotlistings.com/leads/123456 the ID is 123456.\n")
        print("\nThe two following files should not be modified.")
        print("- payload.json contains data about HTML elements and the actions the script should take to scrape listings.")
        print("- offline_data.json contains the data from the script's last run.")
        print("This enables you to use the OFFLINE argument when launching the script.")
        print("When doing that, you can modify the keywords and/or colors without having to fetch the data online again.")
        print("\nThe script will create a file named scrapings.xlsx in ./scrape/ when done.")
    elif mode == "POST":
        print("POST: all the configuration files for posting an ad are in ./post/\n")
        print("- listing.xlsx is a spreadsheet containing the data needed to post an ad online.")
        print("Check https://docs.google.com/spreadsheets/d/1ouOvF9nybzSelj8eB4efmsiA9Magd5Iq9yzJU1xIp58/edit?usp=sharing for the template.")
        print(" The following file should not be modified.")
        print("- payload.json contains data about HTML elements and the actions the script should take to scrape listings.")
        print("\n The script will run and go through the ad posting process, filling in information based on the spreadsheet.")
        print("When done, a list of tasks that need to be handled manually will pop up.")
    elif mode == "UNLEADED":
        print("UNLEADED: uses the config files in SCRAPE (./scrape/leads.json)")
        print("The script goes through the listings and creates a spreadsheet based on the data from https://eohhs.ehs.state.ma.us/")
def main():
    arguments = process_args(sys.argv)

    log = init_log(arguments["log level"])
    log.info("Butter v" + str(VERSION) + " is starting...")
    log.debug("Command line arguments: " + str(arguments))

    start_time = time.time()

    if not arguments["mode"] in ["SCRAPE", "POST", "UNLEADED"]:
        log.error("Invalid mode \'" + str(arguments["mode"]) + "\'. Use 'SCRAPE' or 'POST' to run the script in the appropriate mode.")
        instructions(None)
        sys.exit()

    navigation.Navigator(arguments["offline"], arguments["mode"])
    
    #That's for post
    log.error("TODO Compile payload element into arrays when actions are the same.")
    log.error("TODO Add required to json object?")
    log.error("TODO Add picture folders info in spreadsheet")
    log.error("TODO Missing visiting professor, and  medford/boston for tufts harvard.")

    #That's for unleaded
    log.error("Check that EXACT address is matched (11 vs 119)")
    log.error("Check whole building if unit isn't found.")
    log.error("Test None unit.")

    #That's  for scrape
    log.error("Look into features and keywords and other categories I might have missed.")
    log.error("-> Remove divs from features.")
    log.error("Do the things I said I was going to do with the scraper.")
    log.error("TODO multiple leads scraping (get ids from file), fuzzy keyword matching.")
    log.error("Working on: customizable lead id, store data cache on every run and date them, complete overhaul.")

    log.error("Finished in %s seconds." % (time.time() - start_time))
    input("Check that the data has been entered correctly and press ENTER.")

main()
