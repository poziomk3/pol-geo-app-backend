import requests
from bs4 import BeautifulSoup
import re
from VoivoModel import Voivodeship

core_url = 'https://pl.wikipedia.org/'
url = 'https://pl.wikipedia.org//wiki/Wojew%C3%B3dztwo_%C5%82%C3%B3dzkie'


def scrape_voivo(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
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
    return Voivodeship(name, data["Państwo"], data["ISO"], data["TERYT"], data["Powierzchnia"], data["Populacja"], get_image(flag),
                       url, get_image(symbol), get_image(map_dets), get_image(map))


def get_image(base):
    url = core_url + base.find('a').get_attribute_list('href')[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return 'https:' + soup.find('div', id='file').find('a').get_attribute_list('href')[0]

def remove_text_in_brackets(input_string):
    pattern = r'\[.*?\]'
    return re.sub(pattern, '', input_string)