import logging
from logging import handlers
import sys
import time

import navigation
import payload
import spreadsheet

def init_log(logLevel):
    log = logging.getLogger("root")
    log.setLevel(logging.DEBUG)
    
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
    if len(args) == 2:
        if args[1] == "DEBUG":
            logLevel = logging.DEBUG
        elif args[1] == "WARNING":
            logLevel = logging.WARNING

    return logLevel

def main():
    logLevel = process_args(sys.argv)
    log = init_log(logLevel)
    log.info("Starting...")

    start_time = time.time()
    
    data = payload.Payload()
    ss = spreadsheet.Spreadsheet(data.get_value("hidden", "gmaps"))
    data.init(ss)

    nav = navigation.Navigator()
    #nav.login(data)
    #nav.add_listing(data)
    #nav.fill_address(data)
    #nav.fill_rent(data)
    input("Rent filled.")
    #nav.fill_specifics(data)
    #nav.fill_amenities(data)
    #nav.fill_contact(data)
    #nav.fill_photos(data)

    nav.quit()

    log.info("Finished in %s seconds." % (time.time() - start_time))

main()
