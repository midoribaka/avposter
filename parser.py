# coding: utf-8

"""
import logging
from grab import Grab
from grab.error import DataNotFound

links = ["http://lad-rostov.ru/shop/pilnye-diski-almaznye-diski/",
         "http://lad-rostov.ru/shop/sadovo-uborochnyj-instrument/",
         "http://lad-rostov.ru/shop/elektroinstrument1/",
         "http://lad-rostov.ru/shop/zamochno-skobianye-izdelia/",
         "http://lad-rostov.ru/shop/abrazivy-elektrody-otreznye-krugi/",
         "http://lad-rostov.ru/shop/ruchnoi-instrument/"
        ]


# Список страниц, с которых Spider начнёт работу
# для каждого адреса в этом списке будет сгенерировано
# задание с именем initial
base_url = "http://lad-rostov.ru"
category = input("Choose category:")
initial_urls = [links[category]]

g = Grab()

def task_initial():
    # Это функция-обработчик для заданий с именем initial
    # т.е. для тех заданий, что были созданы для
    # адреов указанных в self.initial_urls
    g.go(initial_urls)
    for elem in g.doc.select('.//*[@id="context_menu"]//a'):
        print elem.attr("href")


def task_parse():
    g.xpath_list('.//*[@id="context_menu"]//a')
    if g.response.error_code:
        print("Request failed")
    else:
        print 'Link is: %s' % task.url
        post = {
            'url': task.url,
            'title': g.doc.select('.//*[@id="context_menu"]//a').text(),
            }
        print(post)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    task_initial
"""

from grab import Grab
import logging


g = Grab()
links = ["http://lad-rostov.ru/shop/pilnye-diski-almaznye-diski/",
         "http://lad-rostov.ru/shop/sadovo-uborochnyj-instrument/",
         "http://lad-rostov.ru/shop/elektroinstrument1/",
         "http://lad-rostov.ru/shop/zamochno-skobianye-izdelia/",
         "http://lad-rostov.ru/shop/abrazivy-elektrody-otreznye-krugi/",
         "http://lad-rostov.ru/shop/ruchnoi-instrument/"
        ]

category = input("Choose category:")

def parser():
    g.go(links[category])
    if g.doc.select(".//*[@id='dContent']/h1").exists():
        print("Exists")
    else:
        for elem in g.doc.select('.//*[@id="context_menu"]//a'):
            href = elem.attr("href")
            print href
            print 'Link is: %s' % href
            post = {
                'url': href,
                'title': g.doc.select('.//*[@id="context_menu"]//a').text(),
                }
            print(post)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser()
