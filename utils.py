import requests
from bs4 import BeautifulSoup
import re

core_url = 'https://pl.wikipedia.org/'
url = 'https://pl.wikipedia.org/wiki/Powiat_aleksandrowski'


def get_image(base):
    url = core_url + base.find('a').get_attribute_list('href')[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return 'https:' + soup.find('div', id='file').find('a').get_attribute_list('href')[0]


def remove_text_in_brackets(input_string):
    pattern = r'\[.*?\]'
    return re.sub(pattern, '', input_string)

# print(scrape_voivo(url))
