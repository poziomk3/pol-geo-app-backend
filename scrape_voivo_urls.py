import requests
from bs4 import BeautifulSoup

# Making a GET request
def get_voivo_urls():
    core_url = 'https://pl.wikipedia.org/'
    r = requests.get('https://pl.wikipedia.org/wiki/Wojew%C3%B3dztwo')

    soup = BeautifulSoup(r.content, 'html.parser')
    all_voivos_urls = [core_url + x.find_all('td')[1].find('a').get_attribute_list('href')[0] for x in
                       soup.find('table', class_='wikitable').find_all('tr')[1:]]
    print(all_voivos_urls)
    return all_voivos_urls
get_voivo_urls()