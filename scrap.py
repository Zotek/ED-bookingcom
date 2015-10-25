from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


def isNextPageLoaded(drv):
    pag = drv.find_elements_by_css_selector(".sr_pagination_item,.current")
    st = drv.find_elements_by_css_selector(".is_stuck")
    return len(pag)>0 and len(st)==0

driver = webdriver.Firefox()
driver.get('http://booking.com')
driver.find_element_by_css_selector("#destination").send_keys("Gdynia")
WebDriverWait(driver, 1, poll_frequency=0.1).\
    until(lambda drv: len(drv.find_elements_by_css_selector("ul.ui-autocomplete li")) > 0)
driver.find_element_by_css_selector("ul.ui-autocomplete li").click()
driver.find_element_by_css_selector(".b-checkbox__element").click()
driver.find_element_by_css_selector(".b-searchbox-button").submit()
while True:
    for link in driver.find_elements_by_css_selector("a.hotel_name_link"):
        print(link.get_attribute("href"))
    try:
        next_button = driver.find_element_by_css_selector(".paging-next")
    except NoSuchElementException:
        break
    next_button.click()
    WebDriverWait(driver,10,poll_frequency=1).until(isNextPageLoaded)


