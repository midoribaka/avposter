# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Poster(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://m.avito.ru/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def get_screenshot():
        browser.save_screenshot('current_page')
        current_page_img = Image.open('current_page')
        w, h = current_page_img.size
        captcha_img = current_page_img#.crop((575, 505, w-155, h-1820))
        captcha_img.save('captcha.jpg', 'jpeg')


    def test_poster(self):
        driver = self.driver
        driver.get(self.base_url + "/profile/login")
        driver.find_element_by_name("login").clear()
        driver.find_element_by_name("login").send_keys("#")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("#")
        driver.find_element_by_xpath(u"//input[@value='Войти']").click()
        driver.find_element_by_link_text(u"Подать объявление").click()
        Select(driver.find_element_by_id("category_id")).select_by_visible_text(u"Музыкальные инструменты")
        Select(driver.find_element_by_id("param_162")).select_by_visible_text(u"Гитары и другие струнные")
        driver.find_element_by_id("title").clear()
        driver.find_element_by_id("title").send_keys("Fender Stratocaster")
        driver.find_element_by_name("description").clear()
        driver.find_element_by_name("description").send_keys(u"Fender Stratocaster 1980 года выпуска.")
        driver.find_element_by_id("captcha").clear()
        driver.find_element_by_id("captcha").send_keys(u"фэюшф")
        driver.find_element_by_xpath(u"//input[@value='Продолжить']").click()
        driver.find_element_by_id("service_no").click()
        driver.find_element_by_xpath(u"//input[@value='Продолжить']").click()
        driver.find_element_by_id("service_premium").click()
        driver.find_element_by_id("service_vip").click()
        driver.find_element_by_id("service_highlight").click()
        driver.find_element_by_xpath(u"//input[@value='Продолжить']").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
