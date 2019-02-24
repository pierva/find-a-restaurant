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

def getVenuePicture(venueId):
    url = 'https://api.foursquare.com/v2/venues/%s/photos?' % venueId
    params = {
                'client_id': config.foursquare_client_id,
                'client_secret': config.foursquare_secret,
                'v': config.foursquare_v,
                'limit': 1
             }
    r = requests.get(url, params=params)
    results = r.json()
    if results['meta']['code'] == 200:
        details = results['response']['photos']['items']
        if len(details) > 0:
            return details[0]['prefix'] + "300x300" + details[0]['suffix']
        else:
            return 'No picture available.'
    else:
        return "Error code %s.\n %s" % (results['meta']['code'], results['meta']['errorDetail'])
