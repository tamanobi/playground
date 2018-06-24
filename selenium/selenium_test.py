# coding: utf-8
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://seleniumhq.org/')
browser.execute_script('window.scrollTo(0, 1000)')
a = browser.find_elements_by_css_selector('.downloadBox')
a[0].click()
# browser.quit()
