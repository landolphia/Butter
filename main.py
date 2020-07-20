import logging
import sys
import time

import navigation

from logging import handlers


VERSION = "0.3"


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
        elif a == "WARNING":
            logLevel = logging.WARNING
        elif a == "INFO":
            logLevel = logging.INFO
        elif a == "POST":
            app_mode = "POST"
        elif a == "POST_TEST":
            app_mode = "POST_TEST"
        elif a == "SCRAPE":
            app_mode = "SCRAPE"
        elif a == "OFFLINE":
            offline = True
        elif a == "HELP":
            manual = True
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
        print("This script can run in two modes:")
        print("-SCRAPE crawls through online listings and creates a spreadsheet, highlighting keywords. \"py main.py SCRAPE\"")
        print("-POST takes the data from a spreadsheet to post an ad online. \"py main.py POST\"\n")
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
        print("***WARNING! Ad posting is disabled in this version.***")
        print("- listing.xlsx is a spreadsheet containing the data needed to post an ad online.")
        print("Check https://docs.google.com/spreadsheets/d/1ouOvF9nybzSelj8eB4efmsiA9Magd5Iq9yzJU1xIp58/edit?usp=sharing for the template.")
        print(" The following file should not be modified.")
        print("- payload.json contains data about HTML elements and the actions the script should take to scrape listings.")
        print("\n The script will run and go through the ad posting process, filling in information based on the spreadsheet.")
        print("When done, a list of tasks that need to be handled manually will pop up.")
def main():
    arguments = process_args(sys.argv)

    log = init_log(arguments["log level"])
    log.info("Butter v" + str(VERSION) + " is starting...")
    log.debug("Command line arguments: " + str(arguments))

    start_time = time.time()

    if not arguments["mode"] in ["SCRAPE", "POST", "POST_TEST"]:
        log.error("Invalid mode \'" + str(arguments["mode"]) + "\'. Use 'SCRAPE' or 'POST' to run the script in the appropriate mode.")
        instructions(None)
        sys.exit()

    navigation.Navigator(arguments["offline"], arguments["mode"],  arguments["mode"] == "POST_TEST")
    log.debug("Finished in %s seconds." % (time.time() - start_time))

main()
