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
        elif a == "SCRAPE":
            app_mode = "SCRAPE"
        elif a == "OFFLINE":
            offline = True
        else:
            if i != 1:
                print("Argument #" + str(i) + " ignored. [" + str(a) + "]")
        i += 1

    return { "log level": logLevel, "mode": app_mode, "offline": offline}

def main():
    arguments = process_args(sys.argv)

    log = init_log(arguments["log level"])
    log.info("Butter v" + str(VERSION) + " is starting...")
    log.debug("Command line arguments: " + str(arguments))

    start_time = time.time()

    
    if not arguments["mode"] in ["SCRAPE", "POST"]:
        log.error("Invalid mode \'" + str(arguments["mode"]) + "\'. Use 'SCRAPE' or 'POST' to run the script in the appropriate mode.")
        sys.exit()

    navigation.Navigator(arguments["offline"], arguments["mode"])
    log.debug("Finished in %s seconds." % (time.time() - start_time))

main()
