# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

def _findElementOrNone(parent,selector):
    try:
        return parent.find_element_by_css_selector(selector).text
    except NoSuchElementException:
        return None

def _getScore(parent):
    hotel_grade  = {}
    hotel_grade ['main'] = _findElementOrNone(parent,"#review_list_main_score")
    score_list = parent.find_element_by_css_selector("#review_list_score_breakdown")
    hotel_grade ['clean'] = score_list.get_attribute("data-hotel_clean")
    hotel_grade ['comfort'] = score_list.get_attribute("data-hotel_comfort")
    hotel_grade ['location'] = score_list.get_attribute("data-hotel_location")
    hotel_grade ['services'] = score_list.get_attribute("data-hotel_services")
    hotel_grade ['staff'] = score_list.get_attribute("data-hotel_staff")
    hotel_grade ['value'] = score_list.get_attribute("data-hotel_value")
    hotel_grade ['wifi'] = score_list.get_attribute("data-hotel_wifi")
    hotel_grade = dict(map(lambda (k,v):(k,v.replace(",",".")),hotel_grade.iteritems()))
    return hotel_grade 

def getOpinionsAndHotelGrade(driver,url):
    driver.get(url)


    ops = []
    hotel_grade = _getScore(driver)
    while True:
        reviews = driver.find_elements_by_css_selector("li.review_item")
        for review in reviews:
            op = {}
            reviewer = review.find_element_by_css_selector("div.review_item_reviewer")
            op['name'] = _findElementOrNone(reviewer,"h4")
            op['country'] = _findElementOrNone(reviewer,"span.reviewer_country")
            op['age_range'] = _findElementOrNone(reviewer,"div.user_age_group")
            op['visits'] = _findElementOrNone(reviewer,"div.review_item_user_review_count")
            op['title'] = _findElementOrNone(review,"div.review_item_header_content")
            op['tags'] = map(lambda x: x.text, review.find_elements_by_css_selector("li.review_info_tag"))
            op['positive'] = _findElementOrNone(review,"p.review_pos")
            op['negative'] = _findElementOrNone(review,"p.review_neg")
            op['grade'] = _findElementOrNone(review,"div.review_item_review_score")
            op['date'] = _findElementOrNone(review,"p.review_item_date")
            ops.append(op)
        try:
            nextbutton = driver.find_element_by_css_selector("#review_next_page_link")
            nextbutton.click()
        except NoSuchElementException:
            break
    return ops,hotel_grade

