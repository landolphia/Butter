import logging
from logging import handlers
import sys
import time

import navigation
import payload
import spreadsheet

VERSION = "0.1.8.5"

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

    i = 1
    for a in args:
        if a == "DEBUG":
            logLevel = logging.DEBUG
        elif a == "WARNING":
            logLevel = logging.WARNING
        elif a == "INFO":
            logLevel = logging.INFO
        else:
            if i != 1:
                print("Argument #" + str(i) + " ignored. [" + str(a) + "]")
        i += 1

    return logLevel

def main():
    logLevel = process_args(sys.argv)
    log = init_log(logLevel)
    log.info("Butter v" + str(VERSION) + " is starting...")
    log.debug("Todo:\n-finish refactoring\n-add data type to payload\n-finish multiple floorplans\n")

    start_time = time.time()
    
    data = payload.Payload()
    ss = spreadsheet.Spreadsheet(data.get_value("hidden", "gmaps"))
    data.init(ss)

    nav = navigation.Navigator(data)
    nav.start()
    nav.stop()

    log.info("Finished in %s seconds." % (time.time() - start_time))

    log.warning("Please check the messages above to see if some elements still need to be filled manually.")
    log.warning("This script is still under *heavy* development. It would be wise to manually check that the data is accurately filled.")

main()
