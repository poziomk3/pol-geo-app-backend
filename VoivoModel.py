import csv
from dataclasses import dataclass, fields
import requests
from bs4 import BeautifulSoup
from utils import remove_text_in_brackets, get_image, read_from_file

core_url = 'https://pl.wikipedia.org/'


@dataclass
class Voivodeship:
    teryt: str
    iso: str
    country: str
    name: str
    area: str
    population: str
    flag: str
    symbol: str
    url: str
    admi_url: str
    detailed_map: str
    undetailed_map: str

    def __str__(self):
        return (
            f"{self.teryt:2}  {self.iso:4}  {self.country:6}  {self.name:30}  {self.area:10}  {self.population:10} \n "
            f"{self.flag:100}  {self.symbol:100}\n  {self.url:100}  {self.admi_url:100}\n  {self.detailed_map:100}  "
            f"{self.undetailed_map:100}")

    def __repr__(self):
        return self.__str__()


def read_voivos_from_file(filename):
    voivodeships = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 12:  # Ensure all fields are present
                voivodeship = Voivodeship(
                    country=row[2],
                    iso=row[1],
                    teryt=row[0],
                    area=row[4],
                    population=row[5],
                    name=row[3],
                    flag=row[6],
                    url=row[7],
                    admi_url=row[8],
                    symbol=row[9],
                    detailed_map=row[10],
                    undetailed_map=row[11]
                )
                voivodeships.append(voivodeship)
    return voivodeships


def scrape_voivo(url: str) -> Voivodeship:
    core_url = 'https://pl.wikipedia.org/'
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

    map_dets, map = voivo.find_all(class_='iboxs')
    symbol, flag = trs[2].find_all('tr')[0].find_all('td')
    return Voivodeship(name=name, country=data["Państwo"], iso=data["ISO"], teryt=data["TERYT"],
                       area=data["Powierzchnia"], population=data["Populacja"],
                       flag=get_image(flag),
                       url=url, admi_url=admi_url, symbol=get_image(symbol), detailed_map=get_image(map_dets),
                       undetailed_map=get_image(map))


def get_voivodeship_urls():
    r = requests.get('https://pl.wikipedia.org/wiki/Wojew%C3%B3dztwo')
    soup = BeautifulSoup(r.content, 'html.parser')
    all_voivos_urls = [
        core_url + x.find_all('td')[1].find('a')['href']
        for x in soup.find('table', class_='wikitable').find_all('tr')[1:]
    ]
    return all_voivos_urls


if __name__ == "__main__":
    voivodeships = read_from_file("wojewodztwa.csv", Voivodeship)
    print(*voivodeships, sep='\n\n')

# class Powiat:
#     area: str
#     population: str
#     name: str
#     flag: str
#     url: str
#     symbol: str
#     detailed_map: str
#     map: str
#
#
# @dataclass
# class Gmina:
#     name: str
#     type: 'GminaType'
#     flag: 'Image'
#     symbol: 'Image'
#
#
# @dataclass
# class City:
#     name: str
#     flag: 'Image'
#     symbol: 'Image'
#     is_capital: bool
#
#
# @dataclass
# class Image:
#     name: str
#     path: str
#
#
# from enum import Enum
#
#
# class GminaType(Enum):
#     MIASTO = 1
#     MIASTO_WIEJSKIE = 2
#     WIEJSKA = 3
