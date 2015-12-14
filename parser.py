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


# Страница товара
def content_page():
    print("Content")
    print(g.doc.select(".//*[@id='dContent']/h1").text())


# Ссылки из контекстного меню
def context_menu():
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

# Выбрать, показать ссылки из контекстного меню или списка товаров
def choose_links():
    choose = raw_input("Do you want to choose context menu? y/n")
    if choose == "y":
        context_menu()
    elif choose == "n":
        catalog_page()
    else:
        print("Only y/n")
        choose_links()

# Список товаров
def catalog_page():
    print("Catalog")
    for elem in g.doc.select(".//*[@class='catalog_item_content']//a"):
        href = elem.attr("href")
        print (href + "-" + elem.text())


def parser():
    g.go(links[category])

    # Если это страница товара, выбрать информацию из нее

    if g.doc.select(".//*[@id='dContent']/h1").exists():
        content_page()

    # Если на странице есть контекстное меню, спросить, какие ссылки выводить - из него или из каталога

    elif g.doc.select(".//*[@id='context_menu']").exists():
        choose_links()
    else:
        catalog_page()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser()
