import logging
import sys
import time

import navigation
import payload
import spreadsheet

from logging import handlers

VERSION = "0.2.2"

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
    log.debug("Butter v" + str(VERSION) + " is starting...")
    log.debug("TODO:\n-alert at the end of script\n-faster description filling\n-ask kyle about contact page.")

    start_time = time.time()

    data = payload.Payload()
    ss = spreadsheet.Spreadsheet(data.get_value("hidden", "gmaps"))
    data.init(ss)

    nav = navigation.Navigator(data)
    nav.start()

    log.debug("Finished in %s seconds." % (time.time() - start_time))

    log.warning("Please check the messages above to see if some elements still need to be filled manually.")

    input("\nPress enter when you're done filling in missing details in the ad.")
    nav.close()

main()
