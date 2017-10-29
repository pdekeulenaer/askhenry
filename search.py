import lib
import models
import geopy.distance, geopy.geocoders
from random import shuffle

WALK_RADIUS = 1.25	# max distance in km
BIKE_RADIUS = 3.5	# max distance in km
CAR_RADIUS = 10	# max distance in km

# address = 'Verbindingsdok Westakaai 18, 2000 Antwerpen'
# latlng = lib.geocode.latlng(address)

def _print(l):
	for (d, r) in l:
		print "%s on %.2f km" % (r, d)

# Get all applicable restaurants in a certain radius
def _list_restos(center, MAX_DIST):
	restos = models.Restaurant.query.all()
	distances = []
	for r in restos:
		d = geopy.distance.great_circle(center, (r.latitude, r.longitude)).km
		distances.append((d, r))
		
	res = filter(lambda (d,r): d <= MAX_DIST, distances)
	return res

# randomly return k restaurants
# TODO - build system that uses cached values
def _select_list(res, k=3):
	if len(res) < k:
		print "Not enough restos found, returning whatever we found"
	shuffle(res)
	return res[0:k]

def get_restos(center, k=3, radius=100):
	restos = _list_restos(center, radius)
	finallist = _select_list(restos, k)
	return finallist

# Get the LATLNG of the address at the center, and find 3 restos nearby
def search(addr, radius=100):
	center = lib.geocode.latlng(addr)
	res = get_restos(center, 3, radius)
	return res

# return the radius to be used
def radius(walk=0, bike=0, car=0):
	if walk == bike == car == 0:
		return 100;
	if car == 1: return CAR_RADIUS
	if bike == 1: return BIKE_RADIUS
	if walk == 1: return WALK_RADIUS

	return 100;
