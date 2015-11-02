# -*- coding: utf-8 -*-
# !/usr/bin/python

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import re
from db import Db
from sqlalchemy.orm import sessionmaker
from model import HotelUrl

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
        for link in driver.find_elements_by_css_selector("a.hotel_name_link"):
            hotel,opinion = extractUrl(link.get_attribute("href"))
            hotelList.append(HotelUrl(hotel_name=link.text,hotel_url=hotel,hotel_opinion_url=opinion))
        try:
            next_button = driver.find_element_by_css_selector(".paging-next")
        except NoSuchElementException:

            break
        next_button.click()
        WebDriverWait(driver, 10, poll_frequency=1).until(isNextPageLoaded)
    session.add_all(hotelList)
    session.commit()