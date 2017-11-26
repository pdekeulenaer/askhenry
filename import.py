import main
from database import db
import models, csv
import lib.geocode

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

file = 'build/newrestos.csv'

def parse_header(header):
	l = map(lambda l: l.lower(), header)
	l = map(lambda l: l.replace(" ", "_"), l)
	return l


class Data(object):
	def __init__(self, data, header):
		self.data = data
		self.header = header

	def __getattr__(self, name):
		try:
			index = self.header.index(name)
			return self.data[index]
		except ValueError:
			pass
		
f = open(file, 'rb')
reader = csv.reader(f)

header = parse_header(reader.next())		
print header

data = []

for line in reader:
	assert len(line) == len(header)
	data.append(Data(line, header))

# get the ID for Antwerp
r = db.session.query(models.City.id).filter_by(name = 'Antwerp').first()
city_id = r.id

counter = 0


def addhours(data, resto_obj):
	for day in ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']:
		h = models.OpeningHours()
		h.rest = resto_obj
		h.hours = eval('data.'+day)
		h.day = day
		if eval('data.'+day) == 'X':
			h.is_open = False
		db.session.add(h)
	db.session.commit()


for rest in data:
	r = models.Restaurant()

	name = unicode(rest.restaurant.decode())
	blurb = unicode(rest.blurb.decode())

	r.name = name
	
	r.cuisine = rest.cuisine
	r.price = rest.price.decode()
	r.address = rest.location.decode()
	r.phone = rest.phone.decode()
	r.website = rest.website
	r.blurb = blurb
	r.city_id = city_id

	r.genre = rest.genre
	r.recom_bf = (rest.recom_for_bf == 'X')
	r.recom_lunch = (rest.recom_for_lunch == 'X')

	#rating
	rating = 3.0
	try:
		rating = float(rest.tripadvisor_rating)
	except ValueError:
		pass
	try:
		rating = (float(rest.yelp_ration) + rating)/2
	except ValueError:
		rating = rating

	r.master_rating = rating
	r.has_reservation = (rest.reservation_online_tool == 'Y')
	(r.latitude, r.longitude) = lib.geocode.latlng(rest.location)

	print r.name.decode()

	db.session.add(r)
	db.session.commit()

	# adding the opening hours
	addhours(rest, r)

print "IN DATABASE ---------------------------"

restos = models.Restaurant.query.all()

for r in restos:
	print r