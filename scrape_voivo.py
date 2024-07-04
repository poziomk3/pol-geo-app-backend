import requests
from bs4 import BeautifulSoup
import re

from VoivoModel import Voivodeship

core_url = 'https://pl.wikipedia.org/'
url = 'https://pl.wikipedia.org/wiki/Powiat_aleksandrowski'


def scrape_voivo(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    admi_url = core_url + \
               soup.find(attrs={"title": lambda x: x and "Podział administracyjny wojew" in x}).get_attribute_list(
                   'href')[0]
    voivo = soup.find_all('table', class_='infobox')

    if voivo[0].find('caption') is None:
        voivo = voivo[1]
    else:
        voivo = voivo[0]
    name = voivo.find('caption').text.strip()
    trs = voivo.find_all('tr')
    infos = trs[5:15]

    data = {}

    for row in infos:
        cells = row.find_all(['th', 'td'])
        header = ""
        if cells[0].get_text(strip=True).lower() in ["państwo", "panstwo"]:
            data["Państwo"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "kod" in cells[0].get_text(strip=True).lower():
            data["ISO"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "TERYT" in cells[0].get_text(strip=True):
            data["TERYT"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Powierzchnia" in cells[0].get_text(strip=True):
            data["Powierzchnia"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Populacja" in cells[0].get_text(strip=True):
            data["Populacja"] = remove_text_in_brackets(cells[1].get_text(strip=True))

    # Print the extracted data
    # print(data)
    # print(*infos, sep='\n\n\n\n')
    map_dets, map = voivo.find_all(class_='iboxs')
    symbol, flag = trs[2].find_all('tr')[0].find_all('td')
    return Voivodeship(name=name, country=data["Państwo"], iso=data["ISO"], teryt=data["TERYT"],
                       area=data["Powierzchnia"], population=data["Populacja"],
                       flag=get_image(flag),
                       url=url, admi_url=admi_url, symbol=get_image(symbol), detailed_map=get_image(map_dets),
                       map=get_image(map))


def get_image(base):
    url = core_url + base.find('a').get_attribute_list('href')[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return 'https:' + soup.find('div', id='file').find('a').get_attribute_list('href')[0]


def remove_text_in_brackets(input_string):
    pattern = r'\[.*?\]'
    return re.sub(pattern, '', input_string)

# print(scrape_voivo(url))
