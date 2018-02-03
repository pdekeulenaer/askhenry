import requests, pprint
import geopy.geocoders, geopy.distance

api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
api_key = 'AIzaSyAeqNIPSlEAVVBSPi75QWh6vWgNnBi9O00'

params = {'key':api_key}

def _latlng_google_manual(addr, api='Google'):
	params['address'] = addr
	r = requests.get(api_url, params)
	results = r.json()['results']
	
	if len(results) == 0:
		return None

	loc = results[0]['geometry']['location']

	lat = loc['lat']
	lng = loc['lng']

	return (lat, lng)


def _latlng_geopy_nominatim(addr, api='Nomatim'):
	locator = geopy.geocoders.Nominatim()
	loc = locator.geocode(addr)
	return (loc.latitude, loc.longitude)

def latlng(addr, api='Google'):
	return _latlng_google_manual(addr)


if __name__ == '__main__':
	print latlng('18 Verbindingsdok Westkaai, 2000 Antwerpen')