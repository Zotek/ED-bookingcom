from selenium import webdriver
from db import Db
from sqlalchemy.orm import sessionmaker
from model import HotelUrl
from opinion_scrap import getReviewsAndOverall
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Firefox()
db = Db()
engine = db.getEngine()
Session = sessionmaker(bind=engine)
session = Session()

def _findElementOrNone(parent,selector):
    try:
        return parent.find_element_by_css_selector(selector).text
    except NoSuchElementException:
        return None

for hotelurl in session.query(HotelUrl):

    driver.get(hotelurl.hotel_url)
    summ = driver.find_element_by_css_selector("#summary")
    address = driver.find_element_by_css_selector("#hp_address_subtitle")
    features = driver.find_elements_by_css_selector("div.facilitiesChecklistSection")
    print address.text

    hotel_features = {}
    for category in features:
        cat = category.find_element_by_css_selector("h5").text
        fs = map(lambda x: x.text, category.find_elements_by_css_selector("li"))
        hotel_features[cat]=fs

    reviews,overall = getReviewsAndOverall(driver,hotelurl.hotel_opinion_url)

    print summ
    print hotel_features
    print reviews
    print overall
