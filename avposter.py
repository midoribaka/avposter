# -*-coding: utf-8 -*-
from grab import Grab, GrabError, DataNotFound
from lxml import html
import sys
import argparse
import os
import logging

parser = argparse.ArgumentParser(prog="avposter")
g = Grab()


def login():
    """login to avito.ru. Login and password will get from login.cfg.
    format login.cfg: first row - login, second - password.
    etc:
    admin@admin.ru
    megapassword
    """
    logging.basicConfig(level=logging.DEBUG)
    g = Grab(log_file="1.html")
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
    g.go('http://m.avito.ru/profile')
    g.doc.set_input('login', logindata[0])
    g.doc.set_input('password', logindata[1])
    add_advert() # Для теста
    g.doc.submit()
    g.cookies.save_to_file('cookies.txt')
    try:
        if g.doc.select('/html/body/div[1]/div[2]/div/div/h2').text() == u'Вход':
            raise GrabError('Wrong login/password')
    except DataNotFound:
        pass


def get_items(itemtype):
    """get items from profile.
    itemtype: 'old' for old items. 'active' for active items"""
    result = []
    g.go('https://www.avito.ru/profile/items/%s' % itemtype)
    for el in g.doc.select('//*[@id="overForm"]/div/div[2]//div[@class="description"]').node_list():
        item = el.xpath('h3/a')[0]
        item_id = item.get('name')[5:]
        result.append((item_id, item.text))
    return result


def choice_items(items):
    """promt user for choice item or items. always return list of items"""
    selected_items = []
    print_items(items)
    try:
        choice_numbers = eval(raw_input('choice items: ') + ",")
    except StandardError:
        print 'invalid choice number'
        return choice_items(items)
    if 0 in choice_numbers:
        return main_loop()
    print 'you was choice:'
    try:
        for number in choice_numbers:
            print items[number - 1][1]
            selected_items.append(items[number - 1])
        return selected_items
    except IndexError:
        print 'invalid choice number'
        choice_items(items)


def print_items(items):
    """print items for choise etc."""
    teamplate = "%d)(%s) %s"
    for number, item in enumerate(items, 1):
        print teamplate % (number, item[0], item[1])


def ids_form_settings():
    """get items ids from file settings.cfg"""
    try:
        with open('settings.cfg', 'r') as settings:
            exist_id = settings.readlines()
            return map(lambda x: str(int(x)), exist_id)
    except IOError:
        return []


def save_ids(exist_ids):
    """save items ids to file settings.cfg"""
    exist_ids = [x + '\n' for x in exist_ids]
    with open('settings.cfg', 'w') as settings:
        settings.writelines(exist_ids)


def add_to_settings(items_id):
    exist_id = ids_form_settings()
    for item in items_id:
        if (item[0]) not in exist_id:
            exist_id.append(item[0])
    save_ids(exist_id)


def check_id(item_id):
    web_id = [x[0] for x in (get_items('old') + get_items('active'))]
    if item_id not in web_id:
        return False
    return True


def add_to_autopub():
    """show all items, promt for adding to autopub list in setting.cfg"""
    old_items = get_items('old')
    active_items = get_items('active')
    print "0) exit"
    print "choise item for adding to autopub list:"
    selected = choice_items(active_items+old_items)
    add_to_settings(selected)


def items_from_settings():
    """return items from autopub list in settings.cfg file"""
    ids = ids_form_settings()
    all_web_items = get_items('active') + get_items('old')
    return filter(lambda item: item[0] in ids, all_web_items)


def remove_from_setting(items_id):
    """remove item by id from autopub list in setting.cfg"""
    exists_id = ids_form_settings()
    for item_id in items_id:
        try:
            exists_id.remove(item_id)
        except ValueError:
            return
    save_ids(exists_id)
    return True


def select_to_remove():
    """show items from autopub list, promt for removing from list and remove selected items ids"""
    print "Choice item for remove from autopub list:"
    settings_items = items_from_settings()
    print "0) exit"
    selected = choice_items(settings_items)
    remove_from_setting([x[0] for x in selected])


def apply_autopub():
    settings_ids = ids_form_settings()
    web_old_ids = [item[0] for item in get_items('old')]
    for id_item in settings_ids:
        if id_item in web_old_ids:
            g.go('https://www.avito.ru/profile/items/old?item_id[]=%s&start' % id_item)
            print "adding item with id '%s' to active list" % id_item

def login_test():
    g = Grab(log_file="1.html")
    g.go("http://m.avito.ru/profile")
    g.doc.set_input("login","login")
    g.doc.set_input("password","password")
    g.doc.submit()
    g.cookies.save_to_file('cookies.txt')


def list_to_utf8(seq):
    t = ["    u'%s'" % s.encode('utf-8') for s in seq]
    return '[\n' + ',\n'.join(t) + '\n]'


def add_advert():
    print("Add new advertisement.")
    g = Grab(log_file="2.html")
    g.load_cookies('cookies.txt')
    g.go("http://m.avito.ru/add")
    login_test()
    """
    test = g.doc.rex_search('(<option.*?>(.*)<\/option>)').group(0)
    print test
    test = g.doc.rex_search('')
    """

    g.go("http://m.avito.ru/add")
    #html = g.response.body
    #print html
    g.tree
    text = g.doc.tree.xpath('/html/body/section/form/div[1]/div[2]/div/select/option[3]/text()')
    print list_to_utf8(text)

    """
    from lxml import html
    import requests
    page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
    tree = html.fromstring(page.content)
    #This will create a list of buyers:
    buyers = tree.xpath('//div[@title="buyer-name"]/text()')
    #This will create a list of prices
    prices = tree.xpath('//span[@class="item-price"]/text()')
    print 'Buyers: ', buyers
    print 'Prices: ', prices
    """
    description = ["велосипед для кросс-кантри", "рама: алюминиевый сплав", "колеса 29 дюймов", "дисковые тормоза", "амортизационная вилка", "24 скорости"]

    #g.set_input_by_id("category_id", "34") # Выбрать велосипеды
    #g.set_input_by_id("param_156", "660" ) # Горные
    #g.set_input_by_id('title', 'Merida Big Nine 20-MD') # Название объявления
    #g.set_input_by_id('description', description) # Описание
    #g.set_input_by_id('price', '27410') # Цена

    import urllib2
    url='http://www.avito.ru/registration'
    f = urllib2.open(url)
    c = f.info()['Set cookie'].split(';')[0]
    ts = c.split('.')[1]
    req = urllib2.Request(url='http://m.avito.ru/captcha?' + ts, headers = {
        'Referer':url,
        'Cookie':c
    })
    f = urllib2.urlopen(req)
    image_data = f.read()
    open ('test.jpg', 'wb').write(image_data)
    
    """
    from selenium.webdriver import Firefox
    from PIL import Image 

    browser = Firefox()
    browser.get(' интересующий сайт ')
    browser.save_screenshot('current_page')
    current_page_img = Image.open('current_page')
    w, h = current_page_img.size
    captcha_img = current_page_img.crop((575, 505, w-155, h-1820))
    captcha_img.save('captcha', 'jpeg')
    """

    from PIL import Image
    img = Image.open('test.png')
    img.show()
    #captcha = raw_input('Enter the captcha:') # Ввести капчу
    #g.set_input_by_id('captcha', captcha) # Отдать капчу полю


def main_loop():
    print "="*40
    print "autopub list:"
    print_items(items_from_settings())
    print "="*40
    actions = {'add': add_to_autopub,
           'remove': select_to_remove,
           'apply': apply_autopub,
           'exit': sys.exit}
    actions_order = ['add', 'remove', 'apply', 'exit']
    actions_num_list = tuple(enumerate(actions_order, 1))
    for number, action in actions_num_list:
        print "%d) %s" % (number, action)
    try:
        choice = int(raw_input('choice action:'))
        if not (1 <= choice <= len(actions_order)):
            raise ValueError
    except ValueError:
        print "invalid action number"
    else:
        actions[actions_num_list[choice-1][1]]()

    main_loop()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        login()
        main_loop()
    else:
        parser.add_argument("-p", "--apply", dest="apply", action='store_true', help="apply autopub list")
        parser.add_argument("-a", "--add", dest='ids_to_add', action='store', default=[], nargs="+",
                            help='add ids to autopub list')
        parser.add_argument("-r", "--remove", dest='ids_to_remove', action='store', default=[], nargs="+",
                            help='remove ids from autopub list')
        namespace = parser.parse_args(sys.argv[1:])
        for item_id in namespace.ids_to_add + namespace.ids_to_remove:
            if not item_id.isdigit():
                print 'ERROR: invalid id "%s"' % item_id
                sys.exit(1)
        checked_ids = []
        login()
        for item_id in namespace.ids_to_add:
            if check_id(item_id):
                checked_ids.append(item_id)
            else:
                print "id '%s' dont exist in avito" % item_id

        add_to_settings(checked_ids)
        remove_from_setting(namespace.ids_to_remove)

        if namespace.apply:  # if -p, -apply apply autpub list
            apply_autopub()
