from ed.db import Db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from ed.model import *



db = Db()
engine = db.getEngine()
Session = sessionmaker(bind=engine)
session = Session()


def hotel_dist(by):
    return session.query(by,func.count(Hotel.id)).group_by(by).all()


def avg_ops(c1,subq):
    return session.query(c1,func.avg(subq.c.count)).group_by(c1).all()

def city_hotel_dist(by):
    return  session.query(by,City.name,func.count(Hotel.id)).join(Address).join(City).group_by(by,City.name).all()

subq1 = session.query(City.name,City.id,func.count(Hotel.id).label('count')).select_from(Opinion).join(Hotel).join(Address).join(City).group_by(City.id,Hotel.id).subquery()
subq2 = session.query(Hotel.stars,func.count(Hotel.id).label('count')).select_from(Opinion).join(Hotel).group_by(Hotel.id).subquery()

print(hotel_dist(Hotel.stars))
print(hotel_dist(Hotel.price_level))
print(avg_ops(subq1.c.name,subq1))
print(avg_ops(subq2.c.stars,subq2))
print(city_hotel_dist(Hotel.stars))


