import googlemaps 

class GeoHelper:
    def __init__(self, debug, creds):
        self.DEBUG = debug
        self.gmaps = googlemaps.Client(creds)
    def get_zip(self, address):
        result = self.gmaps.geocode(address)
        zipcode = None
        if len(result) > 0 and result[0]["address_components"] != None: 
            for c in result[0]["address_components"]:
                if c["types"][0] == "postal_code": zipcode = c["short_name"]
        return zipcode
