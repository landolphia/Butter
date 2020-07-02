import base64
import logging
import sys


class Credentials:
    def __init__(self):
        self.log = logging.getLogger("bLog")
    def get_credentials(self, slr):
        self.log.debug("Getting credentials from file [" + slr + "]")
        creds = {}
    
        with open (slr, "r") as slurp:
            data = slurp.readlines()
        if  len(data) != 5:
            self.log.error("Could not find credentials in 'private.slr'.")
            sys.exit()
    
        creds["username1"] = data[0].rstrip()
        creds["password1"] = data[1].rstrip()
        creds["api_key"] = data[2].rstrip()
        creds["username2"] = data[3].rstrip()
        creds["password2"] = data[4].rstrip()
    
        for i in creds:
            creds[i] = base64.b64decode(creds[i]).decode("utf-8")

        return creds 
