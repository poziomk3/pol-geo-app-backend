import csv
import enum
import os
from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class Voivodeship:
    country: str
    iso: str
    teryt: str
    area: str
    population: str
    name: str
    flag:str
    url: str
    admi_url: str
    symbol: str
    detailed_map: str
    map: str

    def __str__(self):
        return f"{self.teryt},{self.iso},{self.country},{self.name},{self.area},{self.population},{self.flag},{self.url},{self.admi_url},{self.symbol},{self.detailed_map},{self.map}"

    def write_to_file(self, filename):

        with open(filename, 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.teryt, self.iso, self.country, self.name, self.area, self.population, self.flag, self.url, self.admi_url, self.symbol, self.detailed_map, self.map])
class Powiat:
    name: str
    flag: 'Image'
    symbol: 'Image'
    gminy: List['Gmina']
    cities: List['City']
    registration: str
    area: float
    population: float
    detailed_map: 'Image'
    map: 'Image'


@dataclass
class Gmina:
    name: str
    type: 'GminaType'
    flag: 'Image'
    symbol: 'Image'


@dataclass
class City:
    name: str
    flag: 'Image'
    symbol: 'Image'
    is_capital: bool


@dataclass
class Image:
    name: str
    path: str


from enum import Enum


class GminaType(Enum):
    MIASTO = 1
    MIASTO_WIEJSKIE = 2
    WIEJSKA = 3
