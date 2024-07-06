import csv
import inspect
import uuid
from dataclasses import  dataclass
import requests
from bs4 import BeautifulSoup
import re


@dataclass
class Image:
    primary_key: uuid.UUID
    date: str
    type: str
    url: str
    author: str
    src: str
    src_description: str
    alt: str
    foreign_key: int


core_url = 'https://pl.wikipedia.org/'


def get_infobox(soup):
    box = soup.find_all('table', class_='infobox')
    if box[0].find('caption') is None:
        box = box[1]
    else:
        box = box[0]
    return box


def get_maps(infobox, foreign_key):
    index = 2
    detailed_map = ''
    undetailed_map = ''
    detailed_map, undetailed_map = [x.find('a') for x in infobox.find_all(class_='iboxs')]
    # print(detailed_map, undetailed_map)
    # return None,None
    return get_image_2(detailed_map, foreign_key, 'detailed_map'), get_image_2(undetailed_map, foreign_key,
                                                                               'undetailed_map')


def get_symbol_and_flag(trs, foreign_key):
    index = 2
    symbol = ''
    flag = ''
    while trs[index].get_attribute_list('class')[0] is not None:
        index += 1
    res = []
    for item in trs[index].find_all('a'):
        if item.find('img') is not None:
            res.append(item)
    if len(res) == 2:
        symbol, flag = res
    elif len(res) == 1:
        symbol = res[0]
    else:
        pass
    return get_image_2(symbol, foreign_key, 'symbol'), get_image_2(flag, foreign_key, 'flag')


def get_image(base):
    if base is None:
        return ""
    url = core_url + base.find('a').get_attribute_list('href')[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return 'https:' + soup.find('div', id='file').find('a').get_attribute_list('href')[0]


def get_image_2(base, foreign_key, type):
    if base is None:
        return ""
    url = core_url + base.get_attribute_list('href')[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    trs = soup.find(class_='commons-file-information-table')
    src = 'https:' + soup.find('div', id='file').find('a').get_attribute_list('href')[0]
    if trs is None:
        return Image(primary_key=uuid.uuid4(), src=src, foreign_key=foreign_key, type=type, date='', author='',
                     src_description='', alt='', url=url)
    else:
        trs = trs.find_all('tr')
    data = {}
    data["date"] = ""
    data["author"] = ""
    data["src_description"] = ""
    data["alt"] = ""
    for row in trs:
        cells = row.find_all(['th', 'td'])
        if "Data" in cells[0].get_text(strip=True):
            data["date"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Autor" in cells[0].get_text(strip=True):
            data["author"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Źródło" in cells[0].get_text(strip=True):
            data["src_description"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Opis" in cells[0].get_text(strip=True):
            data["alt"] = remove_text_in_brackets(cells[1].get_text(strip=True))
    data["url"] = url

    return Image(primary_key=uuid.uuid4(), src=src, foreign_key=foreign_key, type=type, **data)


def read_from_file(filename, class_name):
    result = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result.append(class_name(*row))
    return result


def write_to_file(instance, filename):
    # Get the values of the attributes from the instance
    field_values = []

    for name, value in instance.__dict__.items():
        if not name.startswith('__') and not inspect.isfunction(value) and not inspect.ismethod(value):
            field_values.append(value)

    # Write the values to the CSV file
    with open(filename, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write data row with field values
        writer.writerow(field_values)


def remove_text_in_brackets(input_string):
    pattern = r'\[.*?\]'
    return re.sub(pattern, '', input_string)


def open_url(url: str):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')
