import csv
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from utils import remove_text_in_brackets, get_image, write_to_file, get_image_2

core_url = 'https://pl.wikipedia.org/'


@dataclass
class Powiat:
    teryt: str
    name: str
    voivodeship: str
    registration_plate: str
    area: str
    population: str
    flag: str
    symbol: str
    url: str
    photo: str
    detailed_map: str
    undetailed_map: str

    def __str__(self):
        return (
            f"{self.teryt:2}  {self.name:30}  {self.voivodeship:30}  {self.registration_plate:4}  {self.area:10}  {self.population:10}\n  "
            f"{self.flag:100}  {self.symbol:100}\n  {self.url:100}  {self.photo:100}\n  {self.detailed_map:100}  "
            f"{self.undetailed_map:100}")

    def __repr__(self):
        return self.__str__()


def get_powiats_urls():
    r = requests.get('https://pl.wikipedia.org/wiki/Lista_powiat%C3%B3w_w_Polsce')
    soup = BeautifulSoup(r.content, 'html.parser')
    return [core_url + x.find('a')['href'] for x in soup.find('table', class_='wikitable').find_all('tr')][1:]


test_url = 'https://pl.wikipedia.org/wiki/Powiat_g%C3%B3rowski'


def scrape_powiat(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    powiat = soup.find_all('table', class_='infobox')

    if powiat[0].find('caption') is None:
        powiat = powiat[1]
    else:
        powiat = powiat[0]
    name = powiat.find('caption').text.strip()
    print(name)

    trs = powiat.find_all('tr')
    infos = trs[4:25]
    data = {}
    for row in infos:
        cells = row.find_all(['th', 'td'])
        header = ""
        if "TERC" in cells[0].get_text(strip=True):
            data["TERYT"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Powierzchnia" in cells[0].get_text(strip=True):
            data["Powierzchnia"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Populacja" in cells[0].get_text(strip=True):
            data["Populacja"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Tablice rejestracyjne" in cells[0].get_text(strip=True):
            data["Rejestracja"] = remove_text_in_brackets(cells[1].get_text(strip=True))

    symbol, flag = None, None
    index = 2

    while(trs[index].get_attribute_list('class')[0]!=None):
        index+=1
    res=[]
    for item in trs[index].find_all('a'):
        if(item.find('img')!=None):
            res.append(item)
    if len(res)==2:
        symbol, flag = res
    elif len(res)==1:
        symbol = res[0]
    else:
        pass

    photo = powiat.find(class_='iboxs')
    voivo = data["TERYT"][0:2]
    map_dets, map = None, None
    if len(powiat.find_all(class_='iboxs'))  <2:
        pass
    else:
        if len(powiat.find_all(class_='iboxs')[1:]) == 2:
            map_dets, map = powiat.find_all(class_='iboxs')[1:]

        elif len(powiat.find_all(class_='iboxs')[1:]) == 1:
            map = powiat.find_all(class_='iboxs')[1]
        else:
            pass

    return Powiat(teryt=data["TERYT"], name=name, voivodeship=voivo, registration_plate=data["Rejestracja"],
                  area=data["Powierzchnia"], population=data["Populacja"],
                  flag=get_image_2(flag), symbol=get_image_2(symbol), url=url, photo=get_image(photo),
                  detailed_map=get_image(map_dets), undetailed_map=get_image(map))


powiats=get_powiats_urls()
# print(powiats[71:])
for x in powiats[71:]:
    powa=scrape_powiat(x)
    print(powa)
    write_to_file(powa, "powiaty.csv")
