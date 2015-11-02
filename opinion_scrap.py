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
    overall = {}
    overall['main'] = _findElementOrNone(parent,"#review_list_main_score")
    score_list = parent.find_element_by_css_selector("#review_list_score_breakdown")
    overall['clean'] = score_list.get_attribute("data-hotel_clean")
    overall['comfort'] = score_list.get_attribute("data-hotel_comfort")
    overall['location'] = score_list.get_attribute("data-hotel_location")
    overall['services'] = score_list.get_attribute("data-hotel_services")
    overall['staff'] = score_list.get_attribute("data-hotel_staff")
    overall['value'] = score_list.get_attribute("data-hotel_value")
    overall['wifi'] = score_list.get_attribute("data-hotel_wifi")
    return overall

def getReviewsAndOverall(driver,url):
    driver.get(url)


    ops = []
    overall = _getScore(driver)
    while True:
        reviews = driver.find_elements_by_css_selector("li.review_item")
        for review in reviews:
            op = {}
            reviewer = review.find_element_by_css_selector("div.review_item_reviewer")
            op['name'] = _findElementOrNone(reviewer,"h4")
            op['country'] = _findElementOrNone(reviewer,"span.reviewer_country")
            op['age_group'] = _findElementOrNone(reviewer,"div.user_age_group")
            op['visits'] = _findElementOrNone(reviewer,"div.review_item_user_review_count")
            op['title'] = _findElementOrNone(review,"div.review_item_header_content")
            op['tags'] = map(lambda x: x.text, review.find_elements_by_css_selector("li.review_info_tag"))
            op['positive'] = _findElementOrNone(review,"p.review_pos")
            op['negative'] = _findElementOrNone(review,"p.review_neg")
            op['grade'] = _findElementOrNone(review,"div.review_item_review_score")
            ops.append(op)
        try:
            nextbutton = driver.find_element_by_css_selector("#review_next_page_link")
            nextbutton.click()
        except NoSuchElementException:
            break
    return ops,overall

