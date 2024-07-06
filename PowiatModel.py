from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from utils import remove_text_in_brackets, write_to_file, open_url, get_infobox, get_symbol_and_flag, get_maps

core_url = 'https://pl.wikipedia.org/'


@dataclass
class Powiat:
    teryt: int
    name: str
    voivodeship: int
    registration_plate: str
    area: str
    population: str
    responsible_person: str
    is_miasto_na_prawach_powiatu: bool
    address: str
    url: str

    # photo: str
    # detailed_map: str
    # undetailed_map: str

    def __str__(self):
        return (
            f"{self.teryt:2}  {self.name:30}  {self.voivodeship:30}  {self.registration_plate:4}  {self.area:10} "
            f" {self.population:10} {self.responsible_person:20}  {self.is_miasto_na_prawach_powiatu:5}  {self.address:50} "
            f"{self.url:100}\n ")

    def __repr__(self):
        return self.__str__()


def get_powiats_urls():
    r = requests.get('https://pl.wikipedia.org/wiki/Lista_powiat%C3%B3w_w_Polsce')
    soup = BeautifulSoup(r.content, 'html.parser')
    return [core_url + x.find('a')['href'] for x in soup.find('table', class_='wikitable').find_all('tr')][1:]


test_url = 'https://pl.wikipedia.org/wiki/Powiat_g%C3%B3rowski'


def remove_after_a(s):
    index = s.find('<a')  # Find the index of '<a' in the string
    if index != -1:  # If '<a' is found
        s = s[:index]  # Remove everything after '<a' by slicing the string
    return s


def scrape_powiat(page, url):
    soup = page
    powiat = get_infobox(soup)

    if powiat[0].find('caption') is None:
        powiat = powiat[1]
    else:
        powiat = powiat[0]
    name = powiat.find('caption').text.lower().replace('powiat', '').strip()
    print(name)

    trs = powiat.find_all('tr')
    infos = trs[4:25]
    data = {}
    data["TERYT"] = ''
    data["Person"] = ''
    data["Powierzchnia"] = ''
    data["Populacja"] = ''
    data["Rejestracja"] = ''
    data["Adres"] = ''
    is_miasto_na_prawach_powiatu = False
    for row in infos:
        cells = row.find_all(['th', 'td'])
        header = ""
        if "TERC" in cells[0].get_text(strip=True):
            data["TERYT"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Starosta" in cells[0].get_text(strip=True):
            data["Person"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Prezydent" in cells[0].get_text(strip=True):
            data["Person"] = remove_text_in_brackets(cells[1].get_text(strip=True))
            is_miasto_na_prawach_powiatu = True
        elif "Powierzchnia" in cells[0].get_text(strip=True):
            data["Powierzchnia"] = remove_text_in_brackets(cells[1].get_text(strip=True)).replace('km²', '')
        elif "Populacja" in cells[0].get_text(strip=True):
            data["Populacja"] = remove_text_in_brackets(
                BeautifulSoup(remove_after_a(str(cells[1])), 'html.parser').get_text(strip=True))
        elif "Tablice rejestracyjne" in cells[0].get_text(strip=True):
            data["Rejestracja"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Adres urzędu:" in cells[0].get_text(strip=True):
            data["Adres"] = remove_text_in_brackets(
                BeautifulSoup(str(cells[0]).replace('<br/>', ' '), 'html.parser').get_text(strip=True)).replace(
                'Adres urzędu:', '')
        elif 'Urząd miejski' in cells[0].get_text(strip=True):
            data["Adres"] = remove_text_in_brackets(
                BeautifulSoup(str(cells[0]).replace('<br/>', ' '), 'html.parser').get_text(strip=True)).replace(
                'Urząd miejski', '')

    # symbol, flag = None, None
    # index = 2
    #
    # while (trs[index].get_attribute_list('class')[0] != None):
    #     index += 1
    # res = []
    # for item in trs[index].find_all('a'):
    #     if (item.find('img') != None):
    #         res.append(item)
    # if len(res) == 2:
    #     symbol, flag = res
    # elif len(res) == 1:
    #     symbol = res[0]
    # else:
    #     pass
    #
    # photo = powiat.find(class_='iboxs')
    voivo = data["TERYT"][0:2]
    # map_dets, map = None, None
    # if len(powiat.find_all(class_='iboxs')) < 2:
    #     pass
    # else:
    #     if len(powiat.find_all(class_='iboxs')[1:]) == 2:
    #         map_dets, map = powiat.find_all(class_='iboxs')[1:]
    #
    #     elif len(powiat.find_all(class_='iboxs')[1:]) == 1:
    #         map = powiat.find_all(class_='iboxs')[1]
    #     else:
    #         pass

    return Powiat(teryt=data["TERYT"], name=name, voivodeship=voivo, registration_plate=data["Rejestracja"],
                  area=data["Powierzchnia"], population=data["Populacja"],
                  url=url, responsible_person=data["Person"], is_miasto_na_prawach_powiatu=is_miasto_na_prawach_powiatu,
                  address=data["Adres"])


def scrape_images(page):
    voivo = get_infobox(page)
    trs = voivo.find_all('tr')
    infos = trs[2:]
    primary_key = ''
    for row in infos:
        cells = row.find_all(['th', 'td'])
        if "TERC" in cells[0].get_text(strip=True):
            primary_key = remove_text_in_brackets(cells[1].get_text(strip=True))
    print(primary_key)
    symbol, flag = get_symbol_and_flag(trs, primary_key)
    photo, detailed_map, undetailed_map = get_maps(voivo, primary_key)
    return symbol, flag, photo, detailed_map, undetailed_map


def scrape_pows_to_file(file_name):
    for x in get_powiats_urls():
        write_to_file(scrape_powiat(open_url(x), x), file_name)


def scrape_images_to_file(file_name):
    for x in get_powiats_urls():
        for img in scrape_images(open_url(x)):
            if img is not None:
                write_to_file(img, file_name)



# for x in powiats[40:43]:
#     print(x)
#     for img in scrape_images(open_url(x)):
#         print(img)
# print(powiats[71:])
# for x in powiats[71:]:
#     powa = scrape_powiat(x)
#     print(powa)
#     write_to_file(powa, "powiaty.csv")
