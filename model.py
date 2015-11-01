from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, BigInteger, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


Base = declarative_base()

class Hotel(Base):
	__tablename__ = "hotel"

	id = Column(BigInteger,primary_key=True)
	name = Column(String)
	description = Column(String)
	price_level = Column(Float)
	price = Column(Float)
	stars = Column(Integer)
	address_id = Column(BigInteger,ForeignKey('address.id'))
	hotel_grade_id = Column(BigInteger,ForeignKey('hotel_grade.id'))

class Address(Base):
	__tablename__ = "address"

	id = Column(BigInteger,primary_key=True)
	street = Column(String)
	city_id = Column(BigInteger, ForeignKey('city.id'))

class Cities(Base):
	__tablename__ = "city"

	id = Column(BigInteger,primary_key=True)
	street = Column(String)

class Country(Base):
	__tablename__ = "country"
	id = Column(String,primary_key=True)

class HotelGrade(Base):
	__tablename__ = "hotel_grade"

	id = Column(BigInteger,primary_key=True)
	grade = Column(Float)
	cleanliness = Column(Float)
	comfort = Column(Float)
	location = Column(Float)
	features = Column(Float)
	staff = Column(Float)
	price_to_quality_ratio = Column(Float)
	wifi = Column(Float)

class Opinion(Base):
	__tablename__ = "opinion"

	id = Column(BigInteger,primary_key=True)
	opinion = Column(String)
	user = Column(String)
	user_visits = Column(String)
	date = Column(Date)
	grade = Column(Float)
	title = Column(String)
	country = Column(ForeignKey('country.id'))
	age_range = Column(ForeignKey('age_range.id'))
	hotel_id = Column(ForeignKey('hotel.id'))



class OpinionTags(Base):
	__tablename__ = "opinion_tag"
	
	tag = Column(ForeignKey('tag.id'),primary_key=True)
	opinion = Column(ForeignKey('opinion.id'),primary_key=True)


class Tags(Base):
	__tablename__ = "tag"
	
	id = Column(String,primary_key=True)


class AgeRange(Base):
	__tablename__ = "age_range"
	
	id = Column(String,primary_key=True)


class PriceLevel(Base):
	__tablename__ = "price_level"
	id = Column(Integer,primary_key=True)
	description = Column(String)
