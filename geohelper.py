import googlemaps 

class GeoHelper:
    def __init__(self, creds):
        self.gmaps = googlemaps.Client(creds)
    def get_zip(self, address):
        result = self.gmaps.geocode(address)
        zipcode = None
        if len(result) > 0 and result[0]["address_components"] != None: 
            for c in result[0]["address_components"]:
                if c["types"][0] == "postal_code": zipcode = c["short_name"]
        return zipcode
    def get_street_and_state(self, address):
        result = self.gmaps.geocode(address)
        street = None
        number = None
        city = None
        if len(result) > 0 and result[0]["address_components"] != None: 
            for c in result[0]["address_components"]:
                if c["types"][0] == "street_number": number = c["short_name"]
                if c["types"][0] == "route": street = c["long_name"]
                if c["types"][0] == "locality": city = c["short_name"]
        return {
                "city" : city,
                "number" : number,
                "street" : street
                }

