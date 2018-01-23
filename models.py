from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
import datetime
from database import db
import lib	
import random, os

class City(db.Model):
	__tablename__ = 'cities'
	id = Column(Integer, primary_key=True)
	name = Column(String(255), nullable=False)
	country = Column(String(255), nullable=False)

	def __repr__(self):
		return self.name


class Restaurant(db.Model):
	__tablename__ = 'restaurants'
	id = Column(Integer, primary_key=True)
	name = Column(String(255), nullable=False)
	city_id = Column(String(255), ForeignKey('cities.id'))
	longitude = Column(Float, nullable=False)
	latitude = Column(Float, nullable=False)
	address = Column(String(255), nullable=False)
	phone = Column(String(25), default='0')
	website = Column(String(255))
	has_reservation = Column(Boolean)
	master_rating = Column(Float, default=3.0)
	cuisine = Column(String(255))
	blurb = Column(Text)
	price = Column(String(10), default="20-30")
	last_updated = Column(DateTime, default=datetime.datetime.utcnow)
	genre = Column(String(255))
	recom_bf = Column(Boolean, default=False)
	recom_lunch = Column(Boolean, default=False)
	folder = Column(String(100))

	city = relationship('City')
	hours = relationship('OpeningHours', backref='restaurant', lazy='dynamic')


	def isopen(self, day, hour=0):
		h = self.hours.all()
		thisday = filter(lambda x: x.day == day, h)[0]
		return thisday.is_open

	# Deprecated - remove when all references are gone
	def foldername(self):
		return self.folder
		# return lib.util.cleanstr(str(self.id) + ' ' + self.name)

	def imglist(self):
		path = '/static/img/restaurants/'+self.foldername()
		imgs = lib.util.listfiles(path)
		return imgs

	def img(self):
		imgs = self.imglist()
		img = random.choice(imgs)
		return img

	def imgpath(self):
		if (os.path.exists('./static/img/restaurants/'+self.foldername()+'/')) :
			img = self.img()
			return 'img/restaurants/'+self.foldername()+'/'+img
		else:
			return 'img/restaurants/no_image_available.jpeg'

	def __repr__(self):
		return self.name

class OpeningHours(db.Model):
	__tablename__ = 'hours'
	id = Column(Integer, primary_key=True)
	rest_id = Column(Integer, ForeignKey('restaurants.id'))
	day = Column(Integer, nullable=False)
	hours = Column(String(255), nullable=False)
	is_open = Column(Boolean, default=True)

	rest = relationship(Restaurant)

	def __repr__(self):
		if self.is_open:
			return "%s: %s" % (self.day, self.hours)
		else:
			return  "%s : Closed" % (self.day)

class OpeningHoursExceptions(db.Model):
	__tablename__ = 'hour_exceptions'
	id = Column(Integer, primary_key=True)
	rest_id = Column(Integer, ForeignKey('restaurants.id'))
	date = Column(DateTime, nullable=False)
	hr_open = Column(Integer, nullable=False)
	hr_close = Column(Integer, nullable=False)
	is_closed = Column(Boolean, default=False)
	rest = relationship(Restaurant)

class Social(db.Model):
	__tablename__ = 'social'
	id = Column(Integer, primary_key=True)
	rest_id = Column(Integer, ForeignKey('restaurants.id'))
	fb_id = Column(String(255))
	twitter_id = Column(String(255))
	tripadvisor_id = Column(String(255))
	yelp_id = Column(String(255))

	tripadvisor_rating = Column(Float)
	yelp_rating = Column(Float)

	last_updated = Column(DateTime, default=datetime.datetime.utcnow)
	rest = relationship(Restaurant)

class Trace(db.Model):
	__tablename__ = 'traces'
	id = Column(Integer, primary_key=True)
	longitude = Column(Float, nullable=False)
	latitude = Column(Float, nullable=False)
	transport = Column(String(20))
	food_type = Column(String(20))
	resto1 = Column(Integer, ForeignKey('restaurants.id'))
	resto2 = Column(Integer, ForeignKey('restaurants.id'))
	resto3 = Column(Integer, ForeignKey('restaurants.id'))
	choice = Column(Integer)

	user_id = Column(Integer)
	email = Column(String(255))
	session_id = Column(Integer)

	timestamp = Column(DateTime, default=datetime.datetime.utcnow)

