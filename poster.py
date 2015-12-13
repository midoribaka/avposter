# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from PIL import Image
import unittest
import os


category_id = {1: u"Автомобили",
               2: u"Мотоциклы и мототехника",
               3: u"Грузовики и спецтехника",
               4: u"Водный транспорт",
               5: u"Запчасти и аксессуары",
               6: u"Квартиры",
               7: u"Комнаты",
               8: u"Дома, дачи, коттеджи",
               9: u"Земельные участки",
               10: u"Гаражи и машиноместа",
               11: u"Коммерческая недвижимость",
               12: u"Недвижимость за рубежом",
               13: u"Вакансии",
               14: u"Резюме",
               15: u"Предложения услуг",
               16: u"Запросы на услуги",
               17: u"Одежда, обувь, аксессуары",
               18: u"Детская одежда и обувь",
               19: u"Товары для детей и игрушки",
               20: u"Часы и украшения",
               21: u"Красота и здоровье",
               22: u"Бытовая техника",
               23: u"Мебель и интерьер",
               24: u"Посуда и товары для кухни",
               25: u"Продукты питания",
               26: u"Ремонт и строительство",
               27: u"Растения",
               28: u"Аудио и видео",
               29: u"Игры, приставки и программы",
               30: u"Настольные компьютеры",
               31: u"Ноутбуки",
               32: u"Оргтехника и расходники",
               33: u"Планшеты и электронные книги",
               34: u"Телефоны",
               35: u"Товары для компьютера",
               36: u"Фототехника",
               37: u"Билеты и путешествия",
               38: u"Велосипеды",
               39: u"Книги и журналы",
               40: u"Коллекционирование",
               41: u"Музыкальные инструменты",
               42: u"Охота и рыбалка",
               43: u"Спорт и отдых",
               44: u"Собаки",
               45: u"Кошки",
               46: u"Птицы",
               47: u"Аквариум",
               48: u"Другие животные",
               49: u"Товары для животных",
               50: u"Готовый бизнес",
               51: u"Оборудование для бизнеса"
               }


content = {"title": u"Fender Stratocaster",
           "description": u"Fender Stratocaster 1980 года выпуска.",
           "price": u"20000"
           }


def print_categories():
    for key in category_id:
            print "%s - %s" % (key, category_id[key])


class Poster(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://m.avito.ru/"
        self.verificationErrors = []
        self.accept_next_alert = True


    def login(self):
        if os.path.exists('login.cfg'):
            with open('login.cfg') as logincfg:
                logindata = logincfg.readlines()
        else:
            print "Login.cfg doesn't exist. Creating."
            data = []
            logindata = raw_input('Login:')
            data.append(logindata)
            del logindata
            logindata = raw_input('Password:')
            data.append(logindata)
            with open ('login.cfg', 'w',) as logincfg:
                for item in data:
                    print>>logincfg, item
            with open ('login.cfg') as logincfg:
                logindata = logincfg.readlines()


    def test_poster(self):
        try:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0")
            driver = webdriver.Firefox(profile)
            driver.get(self.base_url + "/profile/login")
            driver.find_element_by_name("login").clear()
            driver.find_element_by_name("login").send_keys("#email")
            driver.find_element_by_name("password").clear()
            driver.find_element_by_name("password").send_keys("#password")
            driver.find_element_by_xpath(u"//input[@value='Войти']").click()
            driver.find_element_by_link_text(u"Подать объявление").click()
        except NoSuchElementException:
                driver.find_element_by_name("password").clear()
                driver.find_element_by_name("password").send_keys("#password")

                # Show captcha
                driver.save_screenshot('current_page')
                current_page_img = Image.open('current_page')
                w, h = current_page_img.size
                captcha_img = current_page_img#.crop((575, 505, w-155, h-1820))
                captcha_img.save('captcha.jpg', 'jpeg')
                captcha = raw_input("Enter the captcha:")

                driver.find_element_by_id("captcha").clear()
                driver.find_element_by_id("captcha").send_keys(captcha)
                driver.find_element_by_xpath(u"//input[@value='Войти']").click()
                driver.find_element_by_link_text(u"Подать объявление").click()
        finally:

            # Show captcha
            driver.save_screenshot('current_page')
            current_page_img = Image.open('current_page')
            w, h = current_page_img.size
            captcha_img = current_page_img#.crop((575, 505, w-155, h-1820))
            captcha_img.save('captcha.jpg', 'jpeg')

            print_categories()
            category = input("Choose category:")
            Select(driver.find_element_by_id("category_id")).select_by_visible_text(category_id[category])
            Select(driver.find_element_by_id("param_162")).select_by_visible_text(u"Гитары и другие струнные")
            driver.find_element_by_id("title").clear()
            driver.find_element_by_id("title").send_keys(content["title"])
            driver.find_element_by_name("description").clear()
            driver.find_element_by_name("description").send_keys(content["description"])
            driver.find_element_by_name("price").clear()
            driver.find_element_by_name("price").send_keys(content["price"])
            #driver.find_element_by_id("image_upload").send_keys("picture.jpg")

            captcha = raw_input("Enter the captcha:")

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
