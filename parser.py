# coding: utf-8

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

    # Страница товара

    if g.doc.select(".//*[@id='dContent']/h1").exists():
        print("Content")
        print(g.doc.select(".//*[@id='dContent']/h1").text())

    # Список товаров

    #elif g.doc.select(".//*[@id='page_content']").exists():
        #print("Catalog")

    # Страница с списком ссылок

    elif g.doc.select(".//*[@id='context_menu']").exists():
        for elem in g.doc.select('.//*[@id="context_menu"]//a'):
            href = elem.attr("href")
            print href
            print 'Link is: %s' % href
            post = {
                'url': href,
                'title': elem.text(),
                }
            print(post)
            title = post['title']
            print(title.encode('utf-8'))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser()
