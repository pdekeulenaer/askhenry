import lib
import models
import geopy.distance, geopy.geocoders
from random import shuffle

WALK_RADIUS = 1.25	# max distance in km
BIKE_RADIUS = 3.5	# max distance in km
CAR_RADIUS = 10	# max distance in km

# address = 'Verbindingsdok Westakaai 18, 2000 Antwerpen'
# latlng = lib.geocode.latlng(address)

# Filter classes to get to final list
class Algorithm():
	def __init__(self):
		self.filters = []

	def add(self, f):
		self.filters.append(f)
		return self

	def execute(self, lst):
		l = lst
		for f in self.filters:
			print "Applying " + f.name()
			l = f.apply(l)

		self.list = l

class ListFilter():
	def apply(self, inlist):
		return self.list

	def name(self):
		return self.__class__.__name__


class Shuffle(ListFilter):
	def apply(self, l):
		shuffle(l)
		return l

class MaxFilter(ListFilter):
	def __init__(self, k):
		self.max = k

	def apply(self, l):
		return l[0:self.max]

class LunchFilter(ListFilter):
	def apply(self, l):
		return filter(lambda x: x.recom_lunch, l)

class BalancedFilter(ListFilter):
	def __init__(self, normalnr, advnr):
		self.normal_nr = normalnr
		self.adv_nr = advnr

	def apply(self, l):
		normal = filter(lambda (d,r): r.genre == 'Traditional', l)
		adventurous = filter(lambda (d,r): r.genre == 'Adventurous', l)

		return normal[0:self.normal_nr]+adventurous[0:self.adv_nr]

# Algorithm Configurations

basicAlg = Algorithm()
basicAlg.add(Shuffle()).add(MaxFilter(3))

balancedAlg = Algorithm()
balancedAlg.add(Shuffle()).add(BalancedFilter(2,1))

# FUNCTIONS

# Get all applicable restaurants in a certain radius
def query_restos(center, MAX_DIST):
	restos = models.Restaurant.query.all()
	distances = []
	for r in restos:
		d = geopy.distance.great_circle(center, (r.latitude, r.longitude)).km
		distances.append((d, r))
		
	res = filter(lambda (d,r): d <= MAX_DIST, distances)
	return res

# # randomly return k restaurants
# # TODO - build system that uses cached values
# def _select_list(res, k=3):
# 	if len(res) < k:
# 		print "Not enough restos found, returning whatever we found"
# 	shuffle(res)
# 	return res[0:k]


# Get the LATLNG of the address at the center, and find 3 restos nearby
def search(addr, radius=100, alg=basicAlg):
	center = lib.geocode.latlng(addr)
	l = query_restos(center, radius)
	if alg is None:
		return shuffle()
	
	alg.execute(l)
	return alg.list

# return the radius to be used
def radius(walk=0, bike=0, car=0):
	if walk == bike == car == 0:
		return 100;
	if car == 1: return CAR_RADIUS
	if bike == 1: return BIKE_RADIUS
	if walk == 1: return WALK_RADIUS

	return 100;


# HELP functions
def _print(l):
	for (d, r) in l:
		print "%s on %.2f km" % (r, d)

def test():
	r = search("Verbindingsdok westkaai 18 Antwerpen", radius=radius(walk=1, bike=1), alg=balancedAlg)
	_print(r)

if __name__ == '__main__':
	import main
	test()