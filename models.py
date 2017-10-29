from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
import datetime
from database import db
import lib	
import random

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
	city = relationship('City')

	def foldername(self):
		return lib.util.cleanstr(str(self.id) + ' ' + self.name)

	def imglist(self):
		path = '\\static\\img\\restaurants\\'+self.foldername()
		imgs = lib.util.listfiles(path)
		return imgs

	def img(self):
		imgs = self.imglist()
		return random.choice(imgs)

	def __repr__(self):
		return self.name

class OpeningHours(db.Model):
	__tablename__ = 'hours'
	id = Column(Integer, primary_key=True)
	rest_id = Column(Integer, ForeignKey('restaurants.id'))
	day = Column(Integer, nullable=False)
	hr_open = Column(Integer, nullable=False)
	hr_close = Column(Integer, nullable=False)

	rest = relationship(Restaurant)

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