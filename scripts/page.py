import requests
from bs4 import BeautifulSoup
import csv
import time
import requests
import urllib.request

link = 'https://flatfy.lun.ua/uk/realty/'

attributes = {'realty-preview__price': 'div',
              'realty-preview__price--sqm': 'div',
              'realty-preview__title': 'h3',
              'realty-preview__description': 'p'}

csv_columns = ['Url', 'Комнат', 'Цена за м²', 'Площадь', 'Этаж', 'Тип дома', 'Отопление', 'Год постройки',
               'Стены', 'Высота потолка', 'Найдено', 'Обновлено', 'Автор', 'Источник']


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def get_soup(html):
    return BeautifulSoup(html, 'lxml')


def downloadHTMLtext(url, fileName):
    r = requests.get(url)
    with open(fileName, 'w') as output_file:
        output_file.write(r.text)


def parse_url(url):
    soup = get_soup(get_html(url))
    table = soup.find('table', attrs={'class': 'realty-page-details__table'})
    carousel = soup.find('div', attrs={'class': 'image-carousel'})
    carousel_images = soup.findAll('img')
    for img in carousel_images:
        img_url = img.attrs['src']
        try:
            urllib.request.urlretrieve(img_url, 'images_v2/'+img_url.split("/")[:-1])
        except Exception as e:
            print(f"{e}")
    td_dict = {}
    td_dict.update({'Url': url})
    print(url)

    if (table is not None):
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if tds:
                if len(tds) == 2:
                    td_dict.update({tds[0].find(text=True): tds[1].find(text=True)})
                elif tds is not None:
                    if tds[0] is not None:
                        td_dict.update({tds[0].find(text=True): 'None'})
                    elif tds[1] is not None:
                        td_dict.update({'None': tds[1].find(text=True)})
    else:
        print(url + '|Объявление удалено автором')
    return td_dict


def parse(filenameUrls, filenameCsv):
    dict_data = {}
    data = []
    with open(filenameUrls) as f:
        filecontent = f.readlines()

    filecontent = [link+x.strip() for x in filecontent]
    for url in filecontent:
        dict_data = parse_url(url)
        write_dict_to_csv(dict_data, filenameCsv)
        time.sleep(1)


def write_dict_to_csv(data, filename):
    try:
        with open(filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter='|')
            # writer.writeheader() #только на первой итерации нужно
            print(data)
            writer.writerow(data)
    except Exception as e:
        print('-------------------------------------------------------------')
        print(f"\t\tERROR {e}")
        print('-------------------------------------------------------------')


def print_dictionary(dct):
    for _id, _list in dct.items():
        print('\n\n')
        print("{} - ".format(_id))
        for ls in _list:
            print(ls, end=', ')


def main():
    # parse('./urls/linksoasis.txt', './result/oasis.csv')
    parse('./new_result/orenda_ursl.txt', './new_result/orenda_final.csv')
    # в результате - вся инфа с отдела "Про оголошення"
    # но сейчас почему-то запись в файл не работает, вывод в консоле


if __name__ == '__main__':
    main()
