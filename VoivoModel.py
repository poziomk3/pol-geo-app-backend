import enum


class Voivo:
    def __init__(self, name: str, flag: 'Image', symbol: 'Image', powiaty: list['Powiat'], area: float,
                 population: float, detailed_map: 'Image', map: 'Image'):
        self.name = name
        self.flag = flag
        self.symbol = symbol
        self.powiaty = powiaty
        self.area = area
        self.population = population
        self.detailed_map = detailed_map
        self.map = map


class Powiat:
    def __init__(self, name: str, flag: 'Image', symbol: 'Image', gminy: list['Gmina'], cities: list['City'],
                 registration: str, area: float, population: float, detailed_map: 'Image', map: 'Image'):
        self.name = name
        self.flag = flag
        self.symbol = symbol
        self.gminy = gminy
        self.cities = cities
        self.registration = registration
        self.area = area
        self.population = population
        self.detailed_map = detailed_map
        self.map = map


class Gmina:
    def __init__(self, name: str, type: 'GminaType', flag: 'Image', symbol: 'Image'):
        self.name = name
        self.flag = flag
        self.symbol = symbol
        self.type = type


class GminaType(enum.Enum):
    MIASTO = 1
    MIASTO_WIEJSKIE = 2
    WIEJSKA = 3


class City:
    def __init__(self, name: str, flag: 'Image', symbol: 'Image', isCapitol: bool):
        self.name = name
        self.flag = flag
        self.symbol = symbol
        self.isCapitol = isCapitol


class Image:
    def __init__(self, name, path):
        self.name = name
        self.path = path
