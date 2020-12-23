import requests
from bs4 import BeautifulSoup
from dataBase import *


def get_html(url):
    response = requests.get(url)
    response.encoding = "utf8"
    return response.text


def get_models_printers(url):
    """
    Функция находит в таблице все совместимые принтеры
    и возвращает их список  
    """

    html = get_html(url)
    list_printers = []  # список принтеров
    soup = BeautifulSoup(html, 'lxml')

    # ищем все строки
    for tr in soup.find_all('tr'):
        if tr.td:  # проверка необходима для исключения None
            if 'Совместимость' in tr.td.get_text():
                for td in tr.find_all('td'):
                    if 'Совместимость' not in td.get_text():
                        list_printers = td.get_text().split('\n')

    return list_printers


def get_models_cartridge(url):
    """
    Функция возвращает номер картриджа
    """

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    name_cartridge = ''  # модель картриджа

    # находим номер картриджа
    for tr in soup.find_all('tr'):
        if tr.td:  # проверка необходима для исключения None
            if 'Модель' in tr.td.get_text():
                for td in tr.find_all('td'):
                    if 'Модель' not in td.get_text():
                        name_cartridge = td.get_text()
    return name_cartridge


def get_link_next_page(url):
    """
    функция возвращает ссылку на следующую страницу
    """

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    link_next_page = ''  # ссылка на следующую страницу

    for a in soup.find('div', class_='pagination').find_all('a'):
        if a.get('rel'):  # проверка необходима для исключения None
            if 'next' in a.get('rel'):
                link_next_page = a.get('href')

    return link_next_page


def get_link_cart_product(url):
    """
    функция возвращает ссылки на карточки товаров
    """

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    links_carts_product = []  # сиспок ссылок на карточки товаров

    for div in soup.find('div', class_='product-list row').find_all('div', class_='name'):
        links_carts_product.append(div.a.get('href'))

    return links_carts_product


def get_link_brand(url):
    """
    функция возвращает ссылки на произсводетелей
    """

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    links_brand = []  # список ссылок на производителей картриджей

    for a in soup.find('div', class_="category-list w-100 mb-4").find_all('a'):
        links_brand.append(a.get('href'))

    return links_brand


def format_list_printers(printers):
    """
    форматирует список принтеров (удаляет переносы строк)
    """
    while '\r' in printers:
        printers.remove('\r')
    return printers


def input_database(cartridge_name, list_printers):
    """
    занесение данных в бд
    """
    for printer in list_printers:
        if printer:  # проверка на пустые значения
            session.add(Cart(printer, cartridge_name))
            session.commit()


def main():
    """
    Основная функуция парсинга данных.
    """
    start_url = ['https://www.mrimage.ru/internet-magazin/kartridji/originalnie-kartridji',  # оригинальные картриджи
                 'https://www.mrimage.ru/internet-magazin/kartridji/sovmestimie-kartridji'  # совместимые картриджи
                 ]
    links_brand = [
        'https://www.mrimage.ru/internet-magazin/kartridji/sovmestimie-kartridji/sovmestimyie-kartridji-dlya-kyocera-mita',
        'https://www.mrimage.ru/internet-magazin/kartridji/sovmestimie-kartridji/sovmestimyie-kartridji-dlya-lexmark',
        'https://www.mrimage.ru/internet-magazin/kartridji/sovmestimie-kartridji/sovmestimyie-kartridji-dlya-oki',
        'https://www.mrimage.ru/internet-magazin/kartridji/sovmestimie-kartridji/sovmestimyie-kartridji-dlya-panasonic',
        'https://www.mrimage.ru/internet-magazin/kartridji/sovmestimie-kartridji/sovmestimyie-kartridji-dlya-ricoh',
        'https://www.mrimage.ru/internet-magazin/kartridji/sovmestimie-kartridji/sovmestimyie-kartridji-dlya-samsung',
        'https://www.mrimage.ru/internet-magazin/kartridji/sovmestimie-kartridji/sovmestimyie-kartridji-dlya-sharp',
        'https://www.mrimage.ru/internet-magazin/kartridji/sovmestimie-kartridji/sovmestimyie-kartridji-dlya-xerox',
    ]  # список всех ссылок по производителям картриджей
    links_carts_product = []  # список всех ссылок на карточку товаров картраджей

    # # заполняю список всех брендов (Совместимых и оригинальных)
    # for link in start_url:
    #     links_brand.extend(get_link_brand(link))

    print('список брендов готов')

    """
    заполняю список всех карточек продуктов.
    по бренду, с каждой страницы
    """
    for links in links_brand:

        # добавление лишней переменной для читаемости кода
        temp_carts = get_link_cart_product(links)  # список для ссылок на карточки картриджей
        links_carts_product.extend(temp_carts)  # добавление временного списка ссылок в общий список

        while get_link_next_page(links):  # проверка на наличие второй страницы

            next_link = get_link_next_page(links)  # временная переменная для ссылки на следующую страницу
            temp_carts = get_link_cart_product(next_link)  # присвоение новой ссылки
            links_carts_product.extend(temp_carts)  # добавление временного списка ссылок в общий список

            if get_link_next_page(links):  # проверка на наличие других ссылок
                links = next_link  # присвоение в переменную, ссылку на след. страницу

    print("списки всех картриджей готовы")

    """
    получение названия и списка принтеров
    """
    for link in links_carts_product:
        name = get_models_cartridge(link)  # название картриджа
        list_printers = get_models_printers(link)  # список всех принтеров, для данного картриджа

        if len(list_printers) >= 2: # проверка на хреновые записи в сайте.
            list_printers = format_list_printers(list_printers)  # отформатированный список принтеров
            input_database(name, list_printers)  # занесение данных в бд.
        else:
            print(f"картридж :{name} \nпринтер: {list_printers} \n{link} ")



main()
#

# links_carts_product = [
#     'https://www.mrimage.ru/internet-magazin/kartridji/originalnie-kartridji/brother/brother-kartridji-i-termoplenki/tn-326m-toner-kartridj-brother-malinovyi '
# ]
# for link in links_carts_product:
#     name = get_models_cartridge(link)  # название картриджа
#     list_printers = get_models_printers(link)  # список всех принтеров, для данного картриджа
#
#     if len(list_printers) >= 2: # проверка на хреновые записи в сайте.
#         list_printers = format_list_printers(list_printers)  # отформатированный список принтеров
#         input_database(name, list_printers)  # занесение данных в бд.
#     else:
#         print(f"картридж :{name} \nпринтер: {list_printers} \n{link} ")
