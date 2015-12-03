# coding: utf-8
import urllib
import csv
import logging

from grab.spider import Spider, Task

links = ["http://lad-rostov.ru/shop/pilnye-diski-almaznye-diski/",
         "http://lad-rostov.ru/shop/sadovo-uborochnyj-instrument/",
         "http://lad-rostov.ru/shop/elektroinstrument1/",
         "http://lad-rostov.ru/shop/zamochno-skobianye-izdelia/",
         "http://lad-rostov.ru/shop/abrazivy-elektrody-otreznye-krugi/",
         "http://lad-rostov.ru/shop/ruchnoi-instrument/"
        ]

class ExampleSpider(Spider):
    # Список страниц, с которых Spider начнёт работу
    # для каждого адреса в этом списке будет сгенерировано
    # задание с именем initial
    base_url = "http://lad-rostov.ru"
    category = input("Choose category:")
    initial_urls = [links[category]]

    def prepare(self):
        # Подготовим файл для записи результатов
        # Функция prepare вызываетя один раз перед началом
        # работы парсера

        self.result_file = csv.writer(open('result.txt', 'w'))
    def task_initial(self, grab, task):

        # Это функция-обработчик для заданий с именем initial
        # т.е. для тех заданий, что были созданы для
        # адреов указанных в self.initial_urls

        for elem in grab.xpath_list('.//*[@id="context_menu"]//a'):
            yield Task('parse', url=elem.get('href'))


    def task_parse(self, grab, task):
        print 'Link is: %s' % task.url

        post = {
            'url': task.url,
            'title': grab.doc.select('.//*[@id="context_menu"]//a').text(),
        }
        print(post)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    bot = ExampleSpider(thread_number=2)
    bot.run()
