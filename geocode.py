import json
import config
import requests

def getGeocodeLocation(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {
                'sensor': 'false',
                'address': address,
                'key' : config.GEOCODER_API_KEY
             }
    r = requests.get(url, params=params)
    results = r.json()
    if results['meta']['code'] == 200:
        venues = results['response']['venues'][0]
        if len(venues) > 0:
            return results['response']['venues'][0]
        else:
            return 'No restaurants available.'
    else:
        return "Error code %s.\n %s" % (results['meta']['code'], results['meta']['errorDetail'])
