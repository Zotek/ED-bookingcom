from selenium import webdriver
from db import Db
from sqlalchemy.orm import sessionmaker
from model import HotelUrl
from opinion_scrap import getOpinionsAndHotelGrade
from selenium.common.exceptions import NoSuchElementException
from transaction import Transaction
from utils import extract_address
import atexit


profile = webdriver.FirefoxProfile()
profile.set_preference("intl.accept_languages", "pl")
driver = webdriver.Firefox(profile)
db = Db()
engine = db.getEngine()
Session = sessionmaker(bind=engine)
session = Session()

atexit.register(lambda : driver.quit())

def _findElementOrNone(parent,selector):
    try:
        return parent.find_element_by_css_selector(selector).text
    except NoSuchElementException:
        return None

for hotelurl in session.query(HotelUrl).filter(HotelUrl.crawled==None):



    driver.get(hotelurl.hotel_url)
    description = driver.find_element_by_css_selector("#summary").text
    address = driver.find_element_by_css_selector("#hp_address_subtitle")
    features = driver.find_elements_by_css_selector("div.facilitiesChecklistSection")
    
    hotel_features = {}
    for category in features:
        cat = category.find_element_by_css_selector("h5").text
        fs = map(lambda x: x.text, category.find_elements_by_css_selector("li"))
        hotel_features[cat]=fs

    address = extract_address(address.text)
    opinions,hotel_grade = getOpinionsAndHotelGrade(driver,hotelurl.hotel_opinion_url)

    #session, hotel_url, address, hotel_grade, description, opinions, features
    print description,address,hotel_features,opinions,hotel_grade

    transaction = Transaction(session,hotelurl,address,hotel_grade,description,opinions,hotel_features)
    transaction.commit()

    
    
