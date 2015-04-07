# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import time

success = True
wd = WebDriver()
wd.implicitly_wait(60)

def is_alert_present(wd):
    try:
        wd.switch_to_alert().text
        return True
    except:
        return False

try:

    wd.find_element_by_css_selector("div.spoiler-head.active").click()
    wd.find_element_by_xpath("//div[@id='projects_list']/div[2]/div[1]").click()
    wd.find_element_by_xpath("//div[@id='projects_list']/div[3]/div[1]").click()
    wd.find_element_by_xpath("//div[@id='projects_list']/div[4]/div[1]").click()
finally:
    wd.quit()
    if not success:
        raise Exception("Test failed.")
