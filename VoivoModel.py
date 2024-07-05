import csv
from dataclasses import dataclass, fields
import requests
from bs4 import BeautifulSoup
from utils import remove_text_in_brackets, get_image, read_from_file


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






def scrape_voivodeship(url: str) -> Voivodeship:
    core_url = 'https://pl.wikipedia.org/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    admi_url = core_url + soup.find(attrs={"title": lambda x: x and "Podział administracyjny wojew" in x})['href']
    infobox = soup.find_all('table', class_='infobox')[0]
    name = infobox.find('caption').text.strip()
    trs = infobox.find_all('tr')

    data = {}
    for row in trs:
        cells = row.find_all(['th', 'td'])
        if cells:
            header = cells[0].get_text(strip=True).lower()
            if header in ["państwo", "panstwo"]:
                data["Państwo"] = remove_text_in_brackets(cells[1].get_text(strip=True))
            elif "kod" in header:
                data["ISO"] = remove_text_in_brackets(cells[1].get_text(strip=True))
            elif "teryt" in header:
                data["TERYT"] = remove_text_in_brackets(cells[1].get_text(strip=True))
            elif "powierzchnia" in header:
                data["Powierzchnia"] = remove_text_in_brackets(cells[1].get_text(strip=True))
            elif "populacja" in header:
                data["Populacja"] = remove_text_in_brackets(cells[1].get_text(strip=True))

    symbol, flag = trs[2].find_all('tr')[0].find_all('td')
    detailed_map, undetailed_map = infobox.find_all(class_='iboxs')

    return Voivodeship(
        name=name, country=data["Państwo"], iso=data["ISO"], teryt=data["TERYT"],
        area=data["Powierzchnia"], population=data["Populacja"],
        flag=get_image(flag), symbol=get_image(symbol), url=url, admi_url=admi_url,
        detailed_map=get_image(detailed_map), undetailed_map=get_image(undetailed_map)
    )


def get_voivodeship_urls():
    core_url = 'https://pl.wikipedia.org/'
    r = requests.get('https://pl.wikipedia.org/wiki/Wojew%C3%B3dztwo')
    soup = BeautifulSoup(r.content, 'html.parser')
    all_voivos_urls = [
        core_url + x.find_all('td')[1].find('a')['href']
        for x in soup.find('table', class_='wikitable').find_all('tr')[1:]
    ]
    return all_voivos_urls


if __name__ == "__main__":
    voivodeships = read_from_file("wojewodztwa.csv",Voivodeship)
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
