import csv
from dataclasses import fields

import requests
from bs4 import BeautifulSoup
import re

core_url = 'https://pl.wikipedia.org/'


def get_image(base):
    url = core_url + base.find('a').get_attribute_list('href')[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return 'https:' + soup.find('div', id='file').find('a').get_attribute_list('href')[0]


def read_from_file(filename, class_name):
    result = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result.append(class_name(*row))
    return result


def write_to_file(cls, filename):
    with open(filename, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            field for field in fields(cls)
        ])


def remove_text_in_brackets(input_string):
    pattern = r'\[.*?\]'
    return re.sub(pattern, '', input_string)
