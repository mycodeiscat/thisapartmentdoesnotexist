import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

attributes = {'realty-preview__price': 'div',
              'realty-preview__price--sqm': 'div',
              'realty-preview__title': 'h3',
              'realty-preview__description': 'p'}

csv_columns = ['Update', 'Found', 'JK', 'Микрорайон', 'район', 'town', 'price', 'price--sqm',
               'street', 'description']


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


def get_time(article):
    temp = []
    times = article.find_all('span', attrs={'class': 'realty-preview__info realty-preview__info--time'})
    for time in times:
        if (time is not None):
            temp.append(time.text)
        else:
            temp.append('-')
    return temp


def get_subtitle(article):
    temp = []
    subtitles = article.find_all('a', attrs={'class': 'realty-preview__sub-title'})
    if (len(subtitles) < 4):
        for i in range(4 - len(subtitles)):
            temp.append('-')

    for subttle in subtitles:
        if (subttle is not None):
            temp.append(subttle.text)
        else:
            temp.append('-')
    return temp


def get_attributes_data(article):
    templist = []
    subtitles = get_subtitle(article)
    times = get_time(article)

    times.extend(subtitles)
    templist.extend(times)

    for key in attributes:
        html_el = article.find(attributes[key], attrs={'class': key})
        if html_el is not None:
            templist.append(html_el.text)
        else:
            templist.append('-')

    return templist


def parse_url(url):
    soup = get_soup(get_html(url))
    articles_html = soup.find_all('article', attrs={'class': 'realty-preview'})

    articles_dict = {}

    for article in articles_html:
        if article.get('id') is not None:
            templist = get_attributes_data(article)
            articles_dict.update({article.get('id'): templist})

    print_dictionary(articles_dict)
    return articles_dict


def parse(url, filename, pages):
    page = '&page='
    for i in range(1, pages + 1):
        dict_data = parse_url(url + page + str(i))
        write_dict_to_csv(dict_data, filename)


def write_dict_to_csv(dict_data, filename):
    try:
        with open(filename, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            for key in dict_data:
                row = [key]
                row.extend(dict_data[key])
                writer.writerow(row)
    except IOError:
        print("I/O error")


def write_list_to_txt(data, filename):
    try:
        with open(filename, 'w') as filehandle:
            for listitem in data:
                filehandle.write('%s\n' % listitem)
    except IOError:
        print("I/O error")


def print_dictionary(dct):
    for _id, _list in dct.items():
        print('\n\n')
        print("{} - ".format(_id))
        for ls in _list:
            print(ls, end=', ')


def create_links(lun_ids, filename):
    links = [str(lun_id) for lun_id in lun_ids]
    write_list_to_txt(links, filename)


def main():
    url = 'https://flatfy.lun.ua/uk/search?geo_id=1&section_id=2'
    pages_count = 1
    parse(url, './new_result/orenda.csv', pages_count)
    # orenda_ids - туда вручную копирую айди с orenda.csv, это быстро
    df = pd.read_csv('./new_result/orenda.csv', sep = '|')
    col = df.columns
    lun_ids = pd.unique(df[col[0]]).tolist()
    create_links(lun_ids, './new_result/orenda_ursl.txt')
    # теперь в файле './new_result/orenda_ursl.txt' - чисто ссылки на объявления. начинаю парсить их в файле page.py


if __name__ == '__main__':
    main()
