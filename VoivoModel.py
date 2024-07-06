from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from utils import get_infobox, remove_text_in_brackets, get_symbol_and_flag, get_maps, write_to_file, open_url

core_url = 'https://pl.wikipedia.org/'


@dataclass
class Voivodeship:
    teryt: int
    iso: str
    country: str
    name: str
    area: int
    population: int
    wojewoda: str
    marszalek: str
    uwo_address: str
    uma_address: str
    url: str
    admi_url: str

    def __str__(self):
        return (
            f"{self.teryt:2}  {self.iso:4}  {self.country:6}  {self.name:30}  {self.area:10}  {self.population:10}"
            f"{self.wojewoda:20}  {self.marszalek:20} "
            f"{self.url:120}  {self.admi_url:120}\n  "
        )

    def __repr__(self):
        return self.__str__()


def scrape_voivo(page, url) -> Voivodeship:
    soup = page
    admi_url = core_url + \
               soup.find(attrs={"title": lambda x: x and "Podział administracyjny wojew" in x}).get_attribute_list(
                   'href')[0]
    voivo = get_infobox(soup)

    name = voivo.find('caption').text.strip().lower().replace('województwo', '').strip()
    print(name, '\n')
    trs = voivo.find_all('tr')
    infos = trs[2:]

    data = {}
    for row in infos:
        cells = row.find_all(['th', 'td'])
        if "Państwo" in cells[0].get_text(strip=True):
            data["Państwo"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "kod" in cells[0].get_text(strip=True).lower():
            data["ISO"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "TERYT" in cells[0].get_text(strip=True):
            data["TERYT"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Powierzchnia" in cells[0].get_text(strip=True):
            data["Powierzchnia"] = remove_text_in_brackets(cells[1].get_text(strip=True)).replace('km²', '')
        elif "Populacja" in cells[0].get_text(strip=True):
            data["Populacja"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Tablice rejestracyjne" in cells[0].get_text(strip=True):
            data["Tablice rejestracyjne"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Marszałek" in cells[0].get_text(strip=True):
            data["Marszałek"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Wojewoda" in cells[0].get_text(strip=True):
            data["Wojewoda"] = remove_text_in_brackets(cells[1].get_text(strip=True))
        elif "Adres Urzędu Marszałkowskiego:" in cells[0].get_text(strip=True):
            data["Adres Urzędu Marszałkowskiego"] = remove_text_in_brackets(
                BeautifulSoup(str(cells[0]).replace('<br/>', ' '), 'html.parser').get_text(strip=True)).replace(
                'Adres Urzędu Marszałkowskiego:', '')
        elif "Adres Urzędu Wojewódzkiego:" in cells[0].get_text(strip=True):
            data["Adres Urzędu Wojewódzkiego"] = remove_text_in_brackets(
                BeautifulSoup(str(cells[0]).replace('<br/>', ' '), 'html.parser').get_text(strip=True)).replace(
                'Adres Urzędu Wojewódzkiego:', '')

    map_dets, undetailed_map = voivo.find_all(class_='iboxs')

    return Voivodeship(name=name, country=data["Państwo"], iso=data["ISO"], teryt=data["TERYT"],
                       area=data["Powierzchnia"], population=data["Populacja"],
                       wojewoda=data["Wojewoda"],
                       marszalek=data["Marszałek"],
                       uwo_address=data["Adres Urzędu Wojewódzkiego"],
                       uma_address=data["Adres Urzędu Marszałkowskiego"],
                       url=url, admi_url=admi_url)


def scrape_images(page):
    voivo = get_infobox(page)
    trs = voivo.find_all('tr')
    infos = trs[2:]
    primary_key = ''
    for row in infos:
        cells = row.find_all(['th', 'td'])
        if "TERYT" in cells[0].get_text(strip=True):
            primary_key = remove_text_in_brackets(cells[1].get_text(strip=True))
    print(primary_key)
    symbol, flag = get_symbol_and_flag(trs, primary_key)
    detailed_map, undetailed_map = get_maps(voivo, primary_key)
    return symbol, flag, detailed_map, undetailed_map


def scrape_voivos_to_file(file_name):
    for x in get_voivodeship_urls():
        write_to_file(scrape_voivo(open_url(x), x), file_name)


def scrape_images_to_file(file_name):
    for x in get_voivodeship_urls():
        for img in scrape_images(open_url(x)):
            write_to_file(img, file_name)


def get_voivodeship_urls():
    r = requests.get('https://pl.wikipedia.org/wiki/Wojew%C3%B3dztwo')
    soup = BeautifulSoup(r.content, 'html.parser')
    all_voivos_urls = [
        core_url + x.find_all('td')[1].find('a')['href']
        for x in soup.find('table', class_='wikitable').find_all('tr')[1:]
    ]
    return all_voivos_urls
