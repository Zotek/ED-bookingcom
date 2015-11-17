# -*- coding: utf-8 -*-

from ed.db import Db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import desc
from ed.model import *
import utils
from collections import Counter


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

def opinions_per_tag():
    return session.query(Tag.id, func.count(Tag.id).label('count')).select_from(Tag).join(OpinionTag).join(Opinion).group_by(Tag.id).order_by(desc('count')).all()

def grades_and_stars():
    return session.query(Opinion.grade, Hotel.stars).join(Hotel).all()

def grades_hist_by_stars():
    groups = []
    for i in range(6):
        groups.append([])
    grades = grades_and_stars()
    for grade,star in grades:
        groups[star].append(grade)
    histograms = map(lambda it : make_histogram(it,0,10,10,-0.5), groups)
    return histograms

def opinions_per_month_per_city():
    return session.query(func.date_part('month',Opinion.date),City.name, func.count('*')).select_from(Opinion).join(Hotel).join(Address).join(City).group_by(City.name, func.date_part('month',Opinion.date)).all()


def make_histogram(iterable,low,high,bins,shift):
    step = (high - low + 0.0) / bins
    dist = Counter((float(x) - low + shift) // step for x in iterable)
    return [dist[b] for b in range(bins)]


subq1 = session.query(City.name,City.id,func.count(Hotel.id).label('count')).select_from(Opinion).join(Hotel).join(Address).join(City).group_by(City.id,Hotel.id).subquery()
subq2 = session.query(Hotel.stars,func.count(Hotel.id).label('count')).select_from(Opinion).join(Hotel).group_by(Hotel.id).subquery()

result = opinions_per_tag()
utils.to_csv(result, "opinions_per_tag.out")

result = hotel_dist(Hotel.stars)
utils.to_csv(result, "hotel_dist_stars.out")

result = hotel_dist(Hotel.price_level)
utils.to_csv(result, "hotel_dist_price.out")

result = avg_ops(subq1.c.name,subq1)
utils.to_csv(result, "avg_ops_hotel_cities.out")

result = avg_ops(subq2.c.stars,subq2)
utils.to_csv(result, "avg_ops_hotel_stars.out")

result = city_hotel_dist(Hotel.stars)
utils.to_csv(result, "city_hotel_stars.out")

result = grades_hist_by_stars()
utils.to_csv(result,"grades_histograms_stars.out")

result = opinions_per_month_per_city()
utils.to_csv(result,"opinions_per_month_per_city.out")

