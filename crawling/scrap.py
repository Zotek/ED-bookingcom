# -*- coding: utf-8 -*-
# !/usr/bin/python

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import re
from ed.db import Db
from sqlalchemy.orm import sessionmaker
from ed.model import HotelUrl

cities = [u"Białystok",
          u"Bielsko-Biała",
          u"Bydgoszcz",
          u"Gdańsk",
          u"Gdynia",
          u"Jastrzębia Góra",
          u"Karpacz",
          u"Katowice",
          u"Kielce",
          u"Kołobrzeg",
          u"Kościelisko",
          u"Kraków",
          u"Krynica Zdrój",
          u"Lublin",
          u"Międzyzdroje",
          u"Olsztyn",
          u"Poznań",
          u"Rzeszów",
          u"Sopot",
          u"Szczecin",
          u"Szczyrk",
          u"Toruń",
          u"Warszawa",
          u"Wisła",
          u"Wrocław",
          u"Władysławowo",
          u"Zakopane",
          u"Zielona Góra",
          u"Łódź",
          u"Świnoujście"]


def isNextPageLoaded(drv):
    pag = drv.find_elements_by_css_selector(".sr_pagination_item,.current")
    st = drv.find_elements_by_css_selector(".is_stuck")
    return len(pag) > 0 and len(st) == 0


def extractUrl(href):
    regex = "\S+\.html"
    s = re.search(regex, href).group(0)

    s2 = re.sub("hotel/pl", "reviews/pl/hotel", s)
    return (s, s2)

def extractItem(item):

    try:
        stars_element = item.find_element_by_css_selector("i.stars")
        stars = re.search("ratings_stars_(\d)",stars_element.get_attribute("class")).group(1)
    except NoSuchElementException:
        stars = 0
    hotel_element = item.find_element_by_css_selector("a.hotel_name_link")
    link = hotel_element.get_attribute("href")
    name = hotel_element.text
    try:
        price_element = item.find_element_by_css_selector("div.sr_price_estimate__values")
        price = re.search("sr_price_estimate__val(\d)",price_element.get_attribute("class")).group(1)
    except NoSuchElementException:
        price = 0
    hotel,reviews = extractUrl(link)

    return name,hotel,reviews,stars,price



driver = webdriver.Firefox()
db = Db()
engine = db.getEngine()
Session = sessionmaker(bind=engine)
session = Session()

for city in cities:
    driver.get('http://booking.com')
    dest = driver.find_element_by_css_selector("#destination")
    dest.clear()
    dest.send_keys(city)
    WebDriverWait(driver, 1, poll_frequency=0.1). \
        until(lambda drv: len(drv.find_elements_by_css_selector("ul.ui-autocomplete li")) > 0)
    driver.find_element_by_css_selector("ul.ui-autocomplete li").click()
    driver.find_element_by_css_selector(".b-checkbox__element").click()
    driver.find_element_by_css_selector(".b-searchbox-button").submit()
    hotelList = []
    while True:
        for item in driver.find_elements_by_css_selector("div.sr_item"):
            name,hotel,reviews,stars,price = extractItem(item)
            hotelList.append(HotelUrl(hotel_name=name,	hotel_url = hotel,hotel_opinion_url=reviews,hotel_stars=stars,hotel_price=price))
        try:
            next_button = driver.find_element_by_css_selector(".paging-next")
        except NoSuchElementException:

            break
        next_button.click()
        WebDriverWait(driver, 10, poll_frequency=1).until(isNextPageLoaded)
    session.add_all(hotelList)
    session.commit()