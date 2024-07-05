import csv
import inspect
from dataclasses import fields
import requests
from bs4 import BeautifulSoup
import re

core_url = 'https://pl.wikipedia.org/'


def get_image(base):
    if base is None:
        return ""
    url = core_url + base.find('a').get_attribute_list('href')[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return 'https:' + soup.find('div', id='file').find('a').get_attribute_list('href')[0]


def get_image_2(base):
    if base is None:
        return ""
    url = core_url + base.get_attribute_list('href')[0]
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
