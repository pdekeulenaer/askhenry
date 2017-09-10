from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
import config
import datetime

Base = declarative_base()
TYPE = 'sqlite'

def engine():
	if TYPE == 'sqlite':
		db_str = sqlite_str()
	else:
		db_str = mysql_str()

def sqlite_str():
	return 'sqlite:///askhenry.db'

def mysql_str():
	host = 'pdekeulenaer.mysql.pythonanywhere-services.com'
	username = 'pdekeulenaer'
	password = 'meghana8'
	dbname = 'pdekeulenaer$askhenry'
	mysql_string = 'mysql+mysqldb://%s:%s@%s/%s' % (username, password, host, dbname)
	return mysql_string	

class Restaurant(Base):
	__tablename__ = 'restaurants'
	id = Column(Integer, primary_key=True)
	name = Column(String(255), nullable=False)
	longitude = Column(Float, nullable=False)
	lattitude = Column(Float, nullable=False)
	address = Column(String(255))
	phone = Column(String(25), default='0')
	website = Column(String(255))
	has_reservation = Column(Boolean)
	blurb = Column(Text)
	price = Column(String(10), default="unknown")
	last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class OpeningHours(Base):
	__tablename__ = 'hours'
	rest_id = Column(Integer, ForeignKey('restaurants.id'))
	day = Column(Integer, nullable=False)
	hr_open = Column(Integer, nullable=False)
	hr_close = Column(Integer, nullable=False)

	rest = relationship(Restaurant)

class OpeningHoursExceptions(Base):
	__tablename__ = 'hour_exceptions'
	rest_id = Column(Integer, ForeignKey('restaurants.id'))
	date = Column(DateTime, nullable=False)
	hr_open = Column(Integer, nullable=False)
	hr_close = Column(Integer, nullable=False)
	is_closed = Column(Boolean, default=False)
	rest = relationship(Restaurant)

class Social(Base):
	__tablename__ = 'social'
	rest_id = Column(Integer, ForeignKey('restaurants.id'))
	fb_id = Column(String(255))
	twitter_id = Column(String(255))
	tripadvisor_id = Column(String(255))
	yelp_id = Column(String(255))

	tripadvisor_rating = Column(Float)
	yelp_rating = Column(Float)

	last_updated = Column(DateTime, default=datetime.datetime.utcnow)
	rest = relationship(Restaurant)
