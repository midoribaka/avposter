# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from PIL import Image
import unittest, time, re


class Poster(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://m.avito.ru/"
        self.verificationErrors = []
        self.accept_next_alert = True


    def test_poster(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0")
        driver = webdriver.Firefox(profile)
        driver.get(self.base_url + "/profile/login")
        driver.find_element_by_name("login").clear()
        driver.find_element_by_name("login").send_keys("#")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("#")
        driver.find_element_by_xpath(u"//input[@value='Войти']").click()
        driver.find_element_by_link_text(u"Подать объявление").click()

        driver.save_screenshot('current_page')
        current_page_img = Image.open('current_page')
        w, h = current_page_img.size
        captcha_img = current_page_img#.crop((575, 505, w-155, h-1820))
        captcha_img.save('captcha.jpg', 'jpeg')

        Select(driver.find_element_by_id("category_id")).select_by_visible_text(u"Музыкальные инструменты")
        Select(driver.find_element_by_id("param_162")).select_by_visible_text(u"Гитары и другие струнные")
        driver.find_element_by_id("title").clear()
        driver.find_element_by_id("title").send_keys("Fender Stratocaster")
        driver.find_element_by_name("description").clear()
        driver.find_element_by_name("description").send_keys(u"Fender Stratocaster 1980 года выпуска.")

        captcha = raw_input("Enter captcha:")

        driver.find_element_by_id("captcha").clear()
        driver.find_element_by_id("captcha").send_keys(captcha)
        driver.find_element_by_xpath(u"//input[@value='Продолжить']").click()
        driver.find_element_by_id("service_no").click()
        driver.find_element_by_xpath(u"//input[@value='Продолжить']").click()
        driver.find_element_by_id("service_premium").click()
        driver.find_element_by_id("service_vip").click()
        driver.find_element_by_id("service_highlight").click()
        driver.find_element_by_xpath(u"//input[@value='Продолжить']").click()


if __name__ == "__main__":
    unittest.main()
