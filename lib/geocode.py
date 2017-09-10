import requests, pprint

api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
api_key = 'AIzaSyAeqNIPSlEAVVBSPi75QWh6vWgNnBi9O00'
params = {'key':api_key}

def latlng(addr, api='Google'):
	params['address'] = addr
	r = requests.get(api_url, params)
	results = r.json()['results']
	loc = results[0]['geometry']['location']

	lat = loc['lat']
	lng = loc['lng']

	return (lat, lng)


if __name__ == '__main__':
	print latlng('18 Verbindingsdok Westkaai, 2000 Antwerpen')